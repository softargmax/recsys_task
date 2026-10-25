import json
import time
from pathlib import Path

import numpy as np
import polars as pl
import torch
from catboost import CatBoostClassifier

from . import config
from .basis import CF_HISTORY, RELATIONS, ROW_KERNELS
from .discovery import fixed_and_human
from .features import scan_listens_dir
from .prune import features_from_weights, load_grammar, used_cells, variant_weights
from .metrics import Scorer, prepare_frame
from .user_features import user_part_features

O1_KERNELS_STATE = 1
HUMAN_EVENT_FIELDS = 8
HUMAN_KEY_STATE = {"u": 20, "ui": 5, "ua": 4, "ual": 3}
HUMAN_RECENT_EVENTS = 10


def state_per_key(cells):
    out = {}
    for rel in RELATIONS:
        rel_cells = [(a, k) for r, a, k in cells if r == rel]
        if not rel_cells:
            continue
        row = [(a, k) for a, k in rel_cells if k in ROW_KERNELS]
        other = [(a, k) for a, k in rel_cells if k not in ROW_KERNELS]
        ring = max((ROW_KERNELS[k] for _, k in row), default=0) * len({a for a, _ in row})
        timestamps = 1 if any(k != "all" for _, k in other) else 0
        out[rel] = {"o1_cells": len(other), "ring_buffer": ring, "timestamps": timestamps,
                    "numbers": len(other) * O1_KERNELS_STATE + ring + timestamps}
    return out


def user_statistics(listens_dir, t_end):
    rows = []
    for path in sorted(Path(listens_dir).glob("part_*.parquet")):
        rows.append(
            pl.scan_parquet(path)
            .group_by("uid")
            .agg(
                pl.len().alias("events"),
                pl.col("item_id").n_unique().alias("tracks"),
                pl.col("artist_id").drop_nulls().n_unique().alias("artists"),
                pl.col("album_id").drop_nulls().n_unique().alias("albums"),
                (pl.col("timestamp") >= t_end - 30 * config.DAY).sum().alias("events_30d"),
            )
            .collect()
        )
    return pl.concat(rows)


def describe_users(users):
    return {c: {"mean": float(users[c].mean()), "median": float(users[c].median()), "p90": float(users[c].quantile(0.9))}
            for c in ["events", "tracks", "artists", "albums", "events_30d"]}


def grammar_state(cells, users):
    per_key = state_per_key(cells)
    keys = {"u": 1, "ui": users["tracks"], "ua": users["artists"], "ual": users["albums"]}
    total = sum(keys[r] * s["numbers"] for r, s in per_key.items() if r != "cf")
    if "cf" in per_key:
        atoms = {a for r, a, _ in cells if r == "cf"}
        total = total + CF_HISTORY * (2 + len(atoms))
    return per_key, total


def human_state(users):
    keyed = sum(HUMAN_KEY_STATE[r] * k for r, k in
                [("u", 1), ("ui", users["tracks"]), ("ua", users["artists"]), ("ual", users["albums"])])
    return users["events_30d"] * HUMAN_EVENT_FIELDS + keyed + HUMAN_RECENT_EVENTS * HUMAN_EVENT_FIELDS


def series_stats(s):
    s = pl.Series(s).cast(pl.Float64)
    return {"mean": float(s.mean()), "median": float(s.median()), "p90": float(s.quantile(0.9))}


def timed(fn, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        started = time.perf_counter()
        out = fn()
        best = min(best, time.perf_counter() - started)
    return out, best


def feature_build_cost(listens_dir, events_path, mappings_dir, t_end, cf):
    from .features import load_explicit
    from .prepare import load_mappings

    path = sorted(Path(listens_dir).glob("part_*.parquet"))[0]
    chunk = pl.read_parquet(path)
    artist_of, _ = load_mappings(events_path, mappings_dir)
    explicit = load_explicit(events_path, artist_of).filter(pl.col("uid").is_between(chunk["uid"].min(), chunk["uid"].max()))
    out = {"events": chunk.height}
    for name, kwargs in {"human": dict(taus=(), basis=False), "human+basis": dict(taus=(), basis=True)}.items():
        started = time.perf_counter()
        feats = user_part_features(chunk, explicit, t_end, cf=cf, **kwargs)
        out[f"{name}_s"] = round(time.perf_counter() - started, 1)
        out[f"{name}_objects"] = feats.height
        del feats
    out["basis_us_per_event"] = (out["human+basis_s"] - out["human_s"]) / chunk.height * 1e6
    out["human_us_per_event"] = out["human_s"] / chunk.height * 1e6
    return out


def run_cost_report(features_dir, run_dir, listens_dir, out_dir, seed=42, t_end=None, build_cost=None):
    features_dir, run_dir, out_dir = Path(features_dir), Path(run_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = json.loads((features_dir / "meta.json").read_text())
    fixed, human = fixed_and_human(meta)
    model, inputs = load_grammar(run_dir / "grammar" / f"model_k32_s{seed}.pt")
    alphabet = inputs.alphabet
    test = pl.read_parquet(features_dir / "test.parquet", columns=list(dict.fromkeys(["uid", "days_before_end", "label", "x_novelty"] + fixed + human + alphabet.columns())))
    basis, fixed_x = inputs.basis(test), inputs.fixed(test)
    report = {"rows": test.height, "seed": seed}

    with torch.no_grad():
        reference = model.grammar(basis).numpy()
    grammar_cb = CatBoostClassifier()
    grammar_cb.load_model(str(run_dir / "models" / f"grammar32_s{seed}.cbm"))
    human_cb = CatBoostClassifier()
    human_cb.load_model(str(run_dir / "models" / f"human_s{seed}.cbm"))
    x_fixed = test.select(fixed).to_numpy().astype(np.float32)

    def gauc(pred):
        return Scorer(prepare_frame(test, pred)).score()["gauc"]

    prune = []
    for variant, (top, bottom) in variant_weights(model).items():
        feats = features_from_weights(basis, top, bottom, model.grammar.n_count)
        corr = [np.corrcoef(feats[:, j], reference[:, j])[0, 1] for j in range(feats.shape[1])]
        cells = used_cells(top, bottom, alphabet)
        pred = grammar_cb.predict_proba(np.hstack([x_fixed, feats.astype(np.float32)]))[:, 1]
        prune.append({"variant": variant, "cells_used": len(cells), "cells_total": int(np.prod(alphabet.shape)),
                      "min_corr": float(np.nanmin(corr)), "gauc_without_refit": gauc(pred), "cells": cells})
    report["pruning"] = prune

    x_grammar = np.hstack([x_fixed, reference.astype(np.float32)])
    x_human = test.select(fixed + human).to_numpy().astype(np.float32)
    p_grammar = grammar_cb.predict_proba(x_grammar)[:, 1]
    p_human = human_cb.predict_proba(x_human)[:, 1]

    kaggle = pl.read_parquet(run_dir / "test_predictions.parquet").head(test.height)
    same_rows = kaggle["uid"].cast(pl.Int64).equals(test["uid"].cast(pl.Int64)) and kaggle["label"].cast(pl.Int64).equals(test["label"].cast(pl.Int64))
    report["reproduction"] = {"rows_aligned": bool(same_rows)}
    if same_rows:
        for name, local in [("grammar32", p_grammar), ("human", p_human)]:
            remote = kaggle[f"pred_{name}_s{seed}"].to_numpy()
            diff = np.abs(local - remote)
            report["reproduction"][name] = {
                "mean_abs_diff": float(diff.mean()), "share_diff_gt_1e-2": float((diff > 1e-2).mean()),
                "gauc_local": gauc(local), "gauc_kaggle": gauc(remote),
            }

    torch.set_num_threads(4)
    _, t_layer = timed(lambda: model.grammar(inputs.basis(test)))
    _, t_grammar_cb = timed(lambda: grammar_cb.predict_proba(x_grammar, thread_count=4))
    _, t_human_cb = timed(lambda: human_cb.predict_proba(x_human, thread_count=4))
    per_k = 1000 / test.height * 1000
    report["latency_ms_per_1k"] = {
        "grammar_layer": t_layer * per_k,
        "catboost_grammar32": t_grammar_cb * per_k,
        "catboost_human": t_human_cb * per_k,
        "trees_grammar32": grammar_cb.tree_count_,
        "trees_human": human_cb.tree_count_,
    }

    t_end = t_end if t_end is not None else meta["t_end"]
    users = user_statistics(listens_dir, t_end)
    report["users"] = describe_users(users)
    full_cells = [(r, a, k) for r in RELATIONS for a in alphabet.atoms for k in alphabet.kernels]
    report["state_numbers_per_user"] = {"human_estimate": series_stats(human_state(users))}
    for name, cells in [("full_basis", full_cells)] + [(f"grammar32_{p['variant']}", [tuple(c) for c in p["cells"]]) for p in prune]:
        per_key, total = grammar_state(cells, users)
        report["state_numbers_per_user"][name] = {**series_stats(total), "per_key": per_key}
    if build_cost is not None:
        report["feature_build"] = build_cost
    (out_dir / "cost_report.json").write_text(json.dumps(report, indent=2))
    return report
