import gc
import json
from pathlib import Path

import numpy as np
import polars as pl
import torch

from .basis import ALPHABETS, RELATIONS
from .discovery import REFERENCE, add_columns, fit_set, load_frames, make_dirs, save_predictions
from .experiments import results_table
from .learned import GrammarModel, Inputs
from .stats import run_stat_tests

SEEDS = (42, 7)
K = 32
THRESHOLDS = (0.001, 0.01, 0.05)
VARIANTS = ["dense"] + [f"t{t}" for t in THRESHOLDS] + ["readable"]
BATCH = 65536


def load_grammar(path):
    ckpt = torch.load(path, weights_only=False, map_location="cpu")
    alphabet = ALPHABETS[ckpt["alphabet"]]
    model = GrammarModel(ckpt["n_count"], ckpt["n_rate"], len(ckpt["fixed_cols"]), alphabet)
    model.load_state_dict(ckpt["state"])
    model.grammar.hard = ckpt.get("hard", False)
    model.eval()
    inputs = Inputs(ckpt["fixed_cols"], alphabet)
    for key in ["scale", "median", "mean", "std"]:
        setattr(inputs, key, ckpt[key])
    return model, inputs


@torch.no_grad()
def cell_weights(model):
    relation, kernel, numerator, denominator = (w.cpu() for w in model.grammar.weights())
    top = torch.einsum("fr,fm,fe->frem", relation, kernel, numerator)
    bottom = torch.einsum("fr,fm,fe->frem", relation, kernel, denominator)
    bottom[:model.grammar.n_count] = 0
    return top, bottom


def threshold_weights(model, threshold):
    top, bottom = cell_weights(model)
    return torch.where(top >= threshold, top, 0), torch.where(bottom >= threshold, bottom, 0)


@torch.no_grad()
def readable_weights(model):
    relation, kernel, numerator, denominator = (w.cpu() for w in model.grammar.weights())
    top = torch.zeros(relation.shape[0], *model.grammar.alphabet.shape)
    bottom = torch.zeros_like(top)
    r, m = relation.argmax(1), kernel.argmax(1)
    for f in range(relation.shape[0]):
        top[f, r[f], :, m[f]] = (numerator[f] >= 0.5).float()
        if f >= model.grammar.n_count:
            bottom[f, r[f], :, m[f]] = (denominator[f] >= 0.5).float()
    return top, bottom


def variant_weights(model):
    out = {"dense": threshold_weights(model, 0.0)}
    for t in THRESHOLDS:
        out[f"t{t}"] = threshold_weights(model, t)
    out["readable"] = readable_weights(model)
    return out


@torch.no_grad()
def features_from_weights(basis, top, bottom, n_count, device="cpu"):
    top, bottom = top.to(device), bottom.to(device)
    out = []
    for start in range(0, len(basis), BATCH):
        b = basis[start:start + BATCH].to(device)
        num = torch.einsum("brem,frem->bf", b, top)
        den = torch.einsum("brem,frem->bf", b, bottom)
        counts = torch.log1p(num[:, :n_count].clamp(min=0))
        rates = (num[:, n_count:] + 0.5) / (den[:, n_count:].clamp(min=0) + 1)
        out.append(torch.cat([counts, rates], 1).cpu())
    return torch.cat(out).numpy()


def used_cells(top, bottom, alphabet):
    used = ((top > 0) | (bottom > 0)).any(0).numpy()
    return [(RELATIONS[r], alphabet.atoms[e], alphabet.kernels[m]) for r, e, m in zip(*np.nonzero(used))]


def find_weights(root, seed):
    return next(Path(root).rglob(f"model_k{K}_s{seed}.pt"))


def run_prune(features_dir, weights_root, out_dir, task_type="GPU", device="cuda", iterations=3000, seeds=SEEDS, variants=tuple(VARIANTS)):
    out_dir = make_dirs(out_dir)
    alphabet = ALPHABETS["rich"]
    fixed, human, (train, val, test) = load_frames(features_dir, alphabet)
    records, val_preds, test_preds, cells = {}, {}, {}, {}
    for seed in seeds:
        run = dict(train=train, val=val, test=test, rates={}, task_type=task_type, iterations=iterations, out_dir=out_dir,
                   records=records, val_preds=val_preds, test_preds=test_preds, seed=seed)
        fit_set(f"{REFERENCE}_s{seed}", fixed + human, **run)
        model, inputs = load_grammar(find_weights(weights_root, seed))
        assert inputs.fixed_cols == fixed, "fixed columns differ from the grammar checkpoint"
        basis = {name: inputs.basis(df) for name, df in zip(["train", "val", "test"], (train, val, test))}
        for variant, (top, bottom) in variant_weights(model).items():
            if variant not in variants:
                continue
            cells[f"{variant}_s{seed}"] = used_cells(top, bottom, alphabet)
            name = f"g{K}_{variant}_s{seed}"
            cols = [f"{name}_{j:02d}" for j in range(K)]
            feats = {s: features_from_weights(basis[s], top, bottom, model.grammar.n_count, device) for s in basis}
            train, val, test = (add_columns(df, cols, feats[s]) for s, df in zip(["train", "val", "test"], (train, val, test)))
            run.update(train=train, val=val, test=test)
            fit_set(name, fixed + cols, **run)
            train, val, test = (df.drop(cols) for df in (train, val, test))
            run.update(train=train, val=val, test=test)
            print(f"{name}: {len(cells[f'{variant}_s{seed}'])} cells")
            del feats
            gc.collect()
        del basis, model, inputs
        gc.collect()

    val_table = results_table(val_preds, val)
    val_table.write_csv(out_dir / "val_metrics.csv")
    test_table = results_table(test_preds, test)
    test_table.write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)
    vs_dense = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=f"g{K}_dense",
                              models=[f"g{K}_{v}" for v in variants if v != "dense"], name="stat_tests_vs_dense")
    vs_human = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE,
                              models=[f"g{K}_{v}" for v in variants], name="stat_tests_vs_human")
    summary = {
        "reference": REFERENCE,
        "seeds": list(seeds),
        "thresholds": list(THRESHOLDS),
        "records": records,
        "cells": cells,
        "cells_count": {k: len(v) for k, v in cells.items()},
        "stat_tests_vs_dense": vs_dense,
        "stat_tests_vs_human": vs_human,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
