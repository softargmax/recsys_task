import gc
import json
import time
from pathlib import Path

import numpy as np
import polars as pl

from . import config
from .basis import ALPHABETS, RELATIONS, basis_name, degenerate_columns
from .experiments import results_table, slug
from .learned import describe, fit_grammar, save_grammar, transform
from .metrics import bootstrap, paired_delta, summarize
from .stats import run_stat_tests
from .train import fit_catboost, predict, refit_catboost

FIXED_PREFIXES = ("i_", "a_", "al_")
FIXED_EXTRA = [
    "c_hour", "c_weekday", "cf_user_score", "u_like_cnt_30d", "u_dislike_cnt_30d",
    "ui_like_state", "ui_dislike_state", "ua_liked_tracks", "ua_disliked_tracks",
]
REFERENCE = "human"
GRAMMAR_SIZES = (8, 16, 32)
BRUTE_SIZES = (8, 16, 32)
RANDOM_SIZE = 16
HYBRID_SIZE = 16
BRUTE_SAMPLE = 1_000_000
EVAL_COLS = ["uid", "days_before_end", "label"]


def fixed_and_human(meta):
    groups = meta["groups"]
    excluded = set(groups.get("decay", [])) | set(groups.get("basis", []))
    base = [c for c in meta["features"] if c not in excluded]
    fixed = [c for c in base if c.startswith(FIXED_PREFIXES) or c in FIXED_EXTRA]
    human = [c for c in base if c not in fixed]
    return fixed, human


def rate_candidates(alphabet):
    degenerate = degenerate_columns()
    out = {}
    for r in RELATIONS:
        for k in alphabet.kernels:
            if basis_name(r, "rec_lp", k) in degenerate:
                continue
            atom = {a: pl.col(basis_name(r, a, k)) for a in alphabet.atoms}
            listened = atom["rec_lp"] + atom["org_lp"]
            total = listened + atom["rec_skip"] + atom["org_skip"]
            recommended = atom["rec_lp"] + atom["rec_skip"]
            organic = atom["org_lp"] + atom["org_skip"]
            out[f"q_{r}_{k}_lp_rate"] = (listened + 0.5) / (total.clip(lower_bound=0) + 1)
            out[f"q_{r}_{k}_rec_lp_rate"] = (atom["rec_lp"] + 0.5) / (recommended.clip(lower_bound=0) + 1)
            out[f"q_{r}_{k}_org_share"] = (organic + 0.5) / (total.clip(lower_bound=0) + 1)
            if "ratio" in atom:
                out[f"q_{r}_{k}_mean_ratio"] = (atom["ratio"] + 0.5) / (total.clip(lower_bound=0) + 1)
            if "novel_lp" in atom:
                novel = atom["novel_lp"] + atom["novel_skip"]
                out[f"q_{r}_{k}_novel_lp_rate"] = (atom["novel_lp"] + 0.5) / (novel.clip(lower_bound=0) + 1)
    return out


def candidate_columns(alphabet):
    degenerate = degenerate_columns()
    return [c for c in alphabet.columns() if c not in degenerate] + list(rate_candidates(alphabet))


def view(df, cols, rates):
    return df.select([rates[c].cast(pl.Float32).alias(c) if c in rates else pl.col(c) for c in cols] + [pl.col("label")])


def importance_frame(model, cols):
    return pl.DataFrame({"feature": cols, "importance": model.get_feature_importance()}).sort("importance", descending=True)


def fit_set(name, cols, train, val, test, rates, task_type, iterations, out_dir, records, val_preds, test_preds, seed=config.SEED):
    tr, va = view(train, cols, rates), view(val, cols, rates)
    model, seconds = fit_catboost(tr, va, cols, task_type, iterations, seed)
    best = model.get_best_iteration() + 1
    val_preds[name] = predict(model, va, cols)
    importance = importance_frame(model, cols)
    del model
    trainval = pl.concat([tr, va], how="vertical")
    del tr, va
    final, final_seconds = refit_catboost(trainval, cols, task_type, best, seed)
    del trainval
    final.save_model(str(out_dir / "models" / f"{slug(name)}.cbm"))
    test_preds[name] = predict(final, view(test, cols, rates), cols)
    records[name] = {"features": len(cols), "best_iteration": best, "val_fit_s": round(seconds, 1), "final_fit_s": round(final_seconds, 1)}
    print(f"{name}: {len(cols)} features, best iteration {best}, fit {seconds:.0f}s + {final_seconds:.0f}s")
    gc.collect()
    return importance


def add_columns(df, names, values):
    return df.with_columns([pl.Series(n, values[:, j]) for j, n in enumerate(names)])


def save_predictions(out_dir, df, preds):
    cols = [pl.Series(f"pred_{name}", np.asarray(p, dtype=np.float32)) for name, p in preds.items()]
    df.select(EVAL_COLS + ["x_novelty"]).with_columns(cols).write_parquet(out_dir / "test_predictions.parquet")


def write_descriptions(out_dir, k, rows):
    (out_dir / "grammar" / f"features_k{k}.json").write_text(json.dumps(rows, indent=2))
    lines = [f"# Learned features, K = {k}", ""] + [f"{r['feature']:2d}. {r['text']}" for r in rows]
    (out_dir / "grammar" / f"features_k{k}.md").write_text("\n".join(lines) + "\n")


def fit_sampled(name, cols, train, val, test, rates, task_type, iterations, out_dir, records, val_preds, test_preds):
    sample = train.sample(n=min(BRUTE_SAMPLE, train.height), seed=config.SEED)
    va = view(val, cols, rates)
    model, seconds = fit_catboost(view(sample, cols, rates), va, cols, task_type, iterations)
    del sample
    val_preds[name] = predict(model, va, cols)
    del va
    test_preds[name] = predict(model, view(test, cols, rates), cols)
    model.save_model(str(out_dir / "models" / f"{slug(name)}.cbm"))
    records[name] = {"features": len(cols), "best_iteration": model.get_best_iteration() + 1, "val_fit_s": round(seconds, 1),
                     "train_rows": min(BRUTE_SAMPLE, train.height), "refit": False}
    print(f"{name}: {len(cols)} features on {records[name]['train_rows']} rows, best iteration {records[name]['best_iteration']}, fit {seconds:.0f}s")
    importance = importance_frame(model, cols)
    del model
    gc.collect()
    return importance


def load_frames(features_dir, alphabet):
    meta = json.loads((Path(features_dir) / "meta.json").read_text())
    assert meta.get("basis"), "features must be built with basis=True"
    fixed, human = fixed_and_human(meta)
    load_cols = list(dict.fromkeys(EVAL_COLS + fixed + human + alphabet.columns()))
    frames = [pl.read_parquet(Path(features_dir) / f"{s}.parquet", columns=load_cols) for s in config.SPLITS]
    for name, df in zip(config.SPLITS, frames):
        bad = [c for c in alphabet.columns() if not np.isfinite(df[c].to_numpy()).all()]
        assert not bad, f"{name}: non-finite basis columns {bad[:5]}"
    return fixed, human, frames


def make_dirs(out_dir):
    out_dir = Path(out_dir)
    for sub in ["models", "importance", "grammar"]:
        (out_dir / sub).mkdir(parents=True, exist_ok=True)
    return out_dir


def run_discovery(features_dir, out_dir, task_type="GPU", device="cuda", iterations=3000, n_boot=100, alphabet="rich"):
    out_dir = make_dirs(out_dir)
    alphabet = ALPHABETS[alphabet]
    fixed, human, (train, val, test) = load_frames(features_dir, alphabet)
    rates = rate_candidates(alphabet)
    candidates = candidate_columns(alphabet)
    print(f"alphabet {alphabet.name} {alphabet.shape}; train {train.height}, val {val.height}, test {test.height}; "
          f"fixed {len(fixed)}, human {len(human)}, candidates {len(candidates)}")

    records, val_preds, test_preds, timings = {}, {}, {}, {}
    run = dict(train=train, val=val, test=test, rates=rates, task_type=task_type, iterations=iterations, out_dir=out_dir,
               records=records, val_preds=val_preds, test_preds=test_preds)

    fit_set("fixed", fixed, **run)
    fit_set(REFERENCE, fixed + human, **run).write_csv(out_dir / "importance" / "human.csv")

    started = time.time()
    importance = fit_sampled("brute_all", fixed + candidates, **run)
    timings["brute_search_s"] = round(time.time() - started, 1)
    importance.write_csv(out_dir / "importance" / "brute_all.csv")
    ranked = importance.filter(pl.col("feature").is_in(candidates))["feature"].to_list()
    for k in BRUTE_SIZES:
        fit_set(f"brute_top{k}", fixed + ranked[:k], **run)
    random_pick = list(np.random.default_rng(config.SEED).choice(candidates, RANDOM_SIZE, replace=False))
    fit_set(f"random{RANDOM_SIZE}", fixed + random_pick, **run)

    grammar_history = {}
    for k in GRAMMAR_SIZES:
        started = time.time()
        model, inputs, history = fit_grammar(train, val, fixed, k // 2, k - k // 2, device, alphabet)
        timings[f"grammar{k}_fit_s"] = round(time.time() - started, 1)
        grammar_history[k] = history
        names = [f"g{k}_{j:02d}" for j in range(k)]
        train = add_columns(train, names, transform(model, inputs, train, device)[1])
        val_preds[f"grammar_nn{k}"], val_feats = transform(model, inputs, val, device)
        val = add_columns(val, names, val_feats)
        test_preds[f"grammar_nn{k}"], test_feats = transform(model, inputs, test, device)
        test = add_columns(test, names, test_feats)
        write_descriptions(out_dir, k, describe(model))
        save_grammar(out_dir / "grammar" / f"model_k{k}.pt", model, inputs)
        run.update(train=train, val=val, test=test)
        fit_set(f"grammar{k}", fixed + names, **run).write_csv(out_dir / "importance" / f"grammar{k}.csv")
        del model, inputs
        gc.collect()

    hybrid = f"human+grammar{HYBRID_SIZE}"
    fit_set(hybrid, fixed + human + [f"g{HYBRID_SIZE}_{j:02d}" for j in range(HYBRID_SIZE)], **run).write_csv(
        out_dir / "importance" / f"{slug(hybrid)}.csv"
    )

    val_table = results_table(val_preds, val)
    val_table.write_csv(out_dir / "val_metrics.csv")
    test_table = results_table(test_preds, test)
    test_table.write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)
    print(test_table.filter(pl.col("slice") == "all").select("model", "logloss", "auc", "gauc", "ndcg@10"))

    boot_models = [REFERENCE, "fixed", "brute_all", f"brute_top{HYBRID_SIZE}", f"random{RANDOM_SIZE}",
                   f"grammar{HYBRID_SIZE}", f"grammar_nn{HYBRID_SIZE}", hybrid] + [f"grammar{k}" for k in GRAMMAR_SIZES if k != HYBRID_SIZE]
    samples = bootstrap(test, {k: test_preds[k] for k in boot_models}, n_boot=n_boot)
    summary = {
        "reference": REFERENCE,
        "alphabet": {"name": alphabet.name, "atoms": alphabet.atoms, "kernels": alphabet.kernels, "candidates": len(candidates)},
        "fixed": fixed,
        "human": human,
        "brute_ranking_top32": ranked[:32],
        "random_pick": random_pick,
        "records": records,
        "timings": timings,
        "grammar_history": grammar_history,
        "test_bootstrap_ci": summarize(samples),
        "test_paired_deltas": {f"{m}_vs_{REFERENCE}": paired_delta(samples, m, REFERENCE) for m in boot_models if m != REFERENCE},
        "n_boot": n_boot,
    }
    summary["stat_tests"] = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
