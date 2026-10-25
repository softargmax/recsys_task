import gc
import json

import polars as pl

from .basis import ALPHABETS
from .discovery import REFERENCE, add_columns, fit_set, load_frames, make_dirs, save_predictions, write_descriptions
from .experiments import results_table
from .learned import describe, fit_grammar, save_grammar, transform
from .prune import threshold_weights, used_cells
from .stats import run_stat_tests

SEEDS = (42, 7, 13)
K = 32
MODES = {
    "dense": dict(),
    "hard": dict(epochs=10, hard_from=4, hard_lr_factor=0.1),
    "frozen": dict(epochs=8, hard_from=4, hard_lr_factor=0.0),
}


def run_sparse(features_dir, out_dir, task_type="GPU", device="cuda", iterations=3000, seeds=SEEDS):
    out_dir = make_dirs(out_dir)
    alphabet = ALPHABETS["rich"]
    fixed, human, (train, val, test) = load_frames(features_dir, alphabet)
    records, val_preds, test_preds, cells, history = {}, {}, {}, {}, {}
    for seed in seeds:
        run = dict(train=train, val=val, test=test, rates={}, task_type=task_type, iterations=iterations, out_dir=out_dir,
                   records=records, val_preds=val_preds, test_preds=test_preds, seed=seed)
        fit_set(f"{REFERENCE}_s{seed}", fixed + human, **run)
        for mode, kwargs in MODES.items():
            model, inputs, history[f"{mode}_s{seed}"] = fit_grammar(train, val, fixed, K // 2, K - K // 2, device, alphabet, seed=seed, **kwargs)
            name = f"g{K}_{mode}_s{seed}"
            cells[name] = used_cells(*threshold_weights(model, 1e-12), alphabet)
            write_descriptions(out_dir, f"{K}_{mode}_s{seed}", describe(model))
            save_grammar(out_dir / "grammar" / f"model_k{K}_{mode}_s{seed}.pt", model, inputs)
            cols = [f"{name}_{j:02d}" for j in range(K)]
            train, val, test = (add_columns(df, cols, transform(model, inputs, df, device)[1]) for df in (train, val, test))
            del model, inputs
            run.update(train=train, val=val, test=test)
            fit_set(name, fixed + cols, **run)
            train, val, test = (df.drop(cols) for df in (train, val, test))
            run.update(train=train, val=val, test=test)
            print(f"{name}: {len(cells[name])} cells")
            gc.collect()

    results_table(val_preds, val).write_csv(out_dir / "val_metrics.csv")
    results_table(test_preds, test).write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)
    vs_dense = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=f"g{K}_dense", models=[f"g{K}_{m}" for m in MODES if m != "dense"],
                              name="stat_tests_vs_dense")
    vs_human = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE,
                              models=[f"g{K}_{m}" for m in MODES], name="stat_tests_vs_human")
    summary = {
        "reference": REFERENCE, "seeds": list(seeds), "modes": MODES, "records": records,
        "cells": cells, "cells_count": {k: len(v) for k, v in cells.items()}, "grammar_history": history,
        "stat_tests_vs_dense": vs_dense, "stat_tests_vs_human": vs_human,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
