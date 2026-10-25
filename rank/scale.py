import gc
import json

from .basis import ALPHABETS
from .discovery import REFERENCE, add_columns, fit_set, load_frames, make_dirs, save_predictions, write_descriptions
from .experiments import results_table
from .learned import describe, fit_grammar, save_grammar, transform
from .stats import run_stat_tests

SEEDS = (42, 7, 13)
SIZES = (32, 64)


def run_scale(features_dir, out_dir, task_type="GPU", device="cuda", iterations=3000, seeds=SEEDS, sizes=SIZES):
    out_dir = make_dirs(out_dir)
    alphabet = ALPHABETS["rich"]
    fixed, human, (train, val, test) = load_frames(features_dir, alphabet)
    records, val_preds, test_preds, history = {}, {}, {}, {}
    for seed in seeds:
        run = dict(train=train, val=val, test=test, rates={}, task_type=task_type, iterations=iterations, out_dir=out_dir,
                   records=records, val_preds=val_preds, test_preds=test_preds, seed=seed)
        fit_set(f"{REFERENCE}_s{seed}", fixed + human, **run)
        added = []
        for k in sizes:
            model, inputs, history[f"k{k}_s{seed}"] = fit_grammar(train, val, fixed, k // 2, k - k // 2, device, alphabet, seed=seed)
            cols = [f"g{k}_s{seed}_{j:02d}" for j in range(k)]
            write_descriptions(out_dir, f"{k}_s{seed}", describe(model))
            save_grammar(out_dir / "grammar" / f"model_k{k}_s{seed}.pt", model, inputs)
            train, val, test = (add_columns(df, cols, transform(model, inputs, df, device)[1]) for df in (train, val, test))
            del model, inputs
            added += cols
            run.update(train=train, val=val, test=test)
            fit_set(f"grammar{k}_s{seed}", fixed + cols, **run)
            fit_set(f"human+grammar{k}_s{seed}", fixed + human + cols, **run)
            gc.collect()
        train, val, test = (df.drop(added) for df in (train, val, test))
        gc.collect()

    results_table(val_preds, val).write_csv(out_dir / "val_metrics.csv")
    results_table(test_preds, test).write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)
    models = [m for k in sizes for m in (f"grammar{k}", f"human+grammar{k}")]
    vs_human = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE, models=models,
                              name="stat_tests_vs_human")
    big = max(sizes)
    vs_small = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=f"grammar{min(sizes)}",
                              models=[f"grammar{big}"], name="stat_tests_k")
    vs_small_hybrid = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=f"human+grammar{min(sizes)}",
                                     models=[f"human+grammar{big}"], name="stat_tests_hybrid_k")
    summary = {
        "reference": REFERENCE, "seeds": list(seeds), "sizes": list(sizes), "records": records, "grammar_history": history,
        "stat_tests_vs_human": vs_human, "stat_tests_k": vs_small, "stat_tests_hybrid_k": vs_small_hybrid,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
