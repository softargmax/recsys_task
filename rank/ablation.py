import gc
import json
import time

import numpy as np
import polars as pl

from .alphabet import CHANNELS, ablation_alphabets
from .basis import ALPHABETS
from .discovery import REFERENCE, add_columns, fit_set, load_frames, make_dirs, save_predictions, write_descriptions
from .experiments import results_table
from .learned import describe, fit_grammar, save_grammar, transform
from .metrics import METRICS
from .stats import run_stat_tests

SEEDS = (42, 7)
K = 32


def model_name(variant):
    return f"g{K}_{variant}"


def channel_effects(point, seeds):
    def value(variant, metric):
        return float(np.mean([point[f"{model_name(variant)}_s{s}"][metric] for s in seeds]))

    rows = []
    for c in CHANNELS:
        for metric in METRICS:
            rows.append({
                "channel": c, "metric": metric,
                "drop_from_rich": value(f"rich-{c}", metric) - value("rich", metric),
                "add_to_base": value(f"base+{c}", metric) - value("base", metric),
            })
    return rows


def run_ablation(features_dir, out_dir, task_type="GPU", device="cuda", iterations=3000, seeds=SEEDS):
    out_dir = make_dirs(out_dir)
    alphabets = ablation_alphabets()
    fixed, human, (train, val, test) = load_frames(features_dir, ALPHABETS["rich"])
    print(f"train {train.height}, val {val.height}, test {test.height}; variants {list(alphabets)}; seeds {list(seeds)}")

    records, val_preds, test_preds, timings = {}, {}, {}, {}
    for seed in seeds:
        run = dict(train=train, val=val, test=test, rates={}, task_type=task_type, iterations=iterations, out_dir=out_dir,
                   records=records, val_preds=val_preds, test_preds=test_preds, seed=seed)
        fit_set(f"{REFERENCE}_s{seed}", fixed + human, **run)
        for variant, alphabet in alphabets.items():
            started = time.time()
            model, inputs, _ = fit_grammar(train, val, fixed, K // 2, K - K // 2, device, alphabet, seed=seed)
            name = f"{model_name(variant)}_s{seed}"
            cols = [f"{name}_{j:02d}" for j in range(K)]
            train = add_columns(train, cols, transform(model, inputs, train, device)[1])
            val = add_columns(val, cols, transform(model, inputs, val, device)[1])
            test = add_columns(test, cols, transform(model, inputs, test, device)[1])
            write_descriptions(out_dir, f"{K}_{variant}_s{seed}", describe(model))
            save_grammar(out_dir / "grammar" / f"model_k{K}_{variant}_s{seed}.pt", model, inputs)
            del model, inputs
            run.update(train=train, val=val, test=test)
            fit_set(name, fixed + cols, **run)
            train, val, test = (df.drop(cols) for df in (train, val, test))
            run.update(train=train, val=val, test=test)
            gc.collect()
            timings[name] = round(time.time() - started, 1)
            print(f"{name} done in {timings[name]:.0f}s")

    val_table = results_table(val_preds, val)
    val_table.write_csv(out_dir / "val_metrics.csv")
    test_table = results_table(test_preds, test)
    test_table.write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)

    point = {r["model"]: r for r in test_table.filter(pl.col("slice") == "all").to_dicts()}
    effects = channel_effects(point, seeds)
    pl.DataFrame(effects).write_csv(out_dir / "channel_effects.csv")
    variants = [model_name(v) for v in alphabets if v != "rich"]
    vs_rich = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=model_name("rich"), models=variants,
                             name="stat_tests_vs_rich")
    vs_human = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE,
                              models=[model_name(v) for v in alphabets], name="stat_tests_vs_human")
    summary = {
        "reference": REFERENCE,
        "seeds": list(seeds),
        "k": K,
        "alphabets": {k: {"atoms": a.atoms, "kernels": a.kernels} for k, a in alphabets.items()},
        "records": records,
        "timings": timings,
        "channel_effects": effects,
        "stat_tests_vs_rich": vs_rich,
        "stat_tests_vs_human": vs_human,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
