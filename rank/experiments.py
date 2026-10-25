import json
from pathlib import Path

import numpy as np
import polars as pl

from . import config
from .features import decay_features_for
from .metrics import bootstrap, evaluate_slices, paired_delta, summarize
from .train import fit_catboost, predict, refit_catboost, simple_baselines

REFERENCE = "L0+cf"
MATCHED_TAUS = ("1h", "1d", "7d", "30d", "90d")


def feature_sets(meta):
    cols = meta["features"]
    groups = meta["groups"]
    decay, cf, window = set(groups["decay"]), set(groups["cf"]), set(meta["window_features"])
    cols = [c for c in cols if c not in set(groups.get("basis", []))]
    l0 = [c for c in cols if c not in decay and c not in cf]
    l0_cf = l0 + [c for c in cols if c in cf]
    without_windows = [c for c in l0_cf if c not in window]
    return {
        "L0": l0,
        "L0+cf": l0_cf,
        "L1": without_windows + decay_features_for(cols, MATCHED_TAUS),
        "L1-wide": without_windows + [c for c in cols if c in decay],
        "L0+L1": cols,
    }


def slug(name):
    return name.replace("+", "_plus_").replace(":", "_")


def results_table(preds, df):
    rows = []
    for name, p in preds.items():
        rows.extend({"model": name, **r} for r in evaluate_slices(df, p))
    return pl.DataFrame(rows)


def ablation(train, val, cols, groups, reference_rows, task_type, iterations):
    rows = []
    base = {r["slice"]: r for r in reference_rows}
    for group, group_cols in groups.items():
        dropped = [c for c in group_cols if c in cols]
        if not dropped:
            continue
        keep = [c for c in cols if c not in dropped]
        model, seconds = fit_catboost(train, val, keep, task_type, iterations)
        for r in evaluate_slices(val, predict(model, val, keep)):
            b = base[r["slice"]]
            rows.append({
                "dropped_group": group, "n_dropped": len(dropped), "slice": r["slice"],
                "auc": r["auc"], "gauc": r["gauc"], "logloss": r["logloss"], "ndcg@10": r["ndcg@10"],
                "delta_auc": r["auc"] - b["auc"], "delta_gauc": r["gauc"] - b["gauc"], "delta_logloss": r["logloss"] - b["logloss"],
                "best_iter": model.get_best_iteration() + 1, "train_s": round(seconds, 1),
            })
        print(f"ablation {group}: {seconds:.0f}s")
    return pl.DataFrame(rows)


def importance_by_scale(importance, prefix, scale_names):
    rows = []
    for name, value in zip(importance["feature"], importance["importance"]):
        if not name.startswith(prefix):
            continue
        scale = next((s for s in scale_names if name.endswith(f"_{s}")), None)
        if scale is None:
            continue
        body = name[len(prefix):-len(scale) - 1]
        relation = body.split("_")[0]
        rows.append({"relation": relation, "feature_base": body, "scale": scale, "importance": value})
    return pl.DataFrame(rows)


def run_experiments(features_dir, out_dir, task_type="GPU", iterations=3000, n_boot=100, with_ablation=True, sets=None):
    features_dir, out_dir = Path(features_dir), Path(out_dir)
    for sub in ["models", "importance"]:
        (out_dir / sub).mkdir(parents=True, exist_ok=True)
    meta = json.loads((features_dir / "meta.json").read_text())
    sets = sets or feature_sets(meta)
    train, val, test = (pl.read_parquet(features_dir / f"{s}.parquet") for s in config.SPLITS)
    trainval = pl.concat([train, val], how="vertical")
    print(f"train {train.height}, val {val.height}, test {test.height}; sets {[(k, len(v)) for k, v in sets.items()]}")

    val_preds, test_preds = simple_baselines(train, val, test)
    records = {}
    for name, cols in sets.items():
        model, seconds = fit_catboost(train, val, cols, task_type, iterations)
        records[name] = {"features": len(cols), "best_iteration": model.get_best_iteration() + 1, "val_fit_s": round(seconds, 1)}
        val_preds[name] = predict(model, val, cols)
        print(f"{name}: {len(cols)} features, best iteration {records[name]['best_iteration']}, {seconds:.0f}s")

    val_table = results_table(val_preds, val)
    val_table.write_csv(out_dir / "val_metrics.csv")
    print(val_table.filter(pl.col("slice") == "all").select("model", "logloss", "auc", "gauc", "ndcg@10"))

    if with_ablation:
        reference_rows = val_table.filter(pl.col("model") == REFERENCE).drop("model").to_dicts()
        ablation(train, val, sets[REFERENCE], meta["groups"], reference_rows, task_type, iterations).write_csv(out_dir / "ablation_val.csv")

    importances = {}
    for name, cols in sets.items():
        model, seconds = refit_catboost(trainval, cols, task_type, records[name]["best_iteration"])
        records[name]["final_fit_s"] = round(seconds, 1)
        model.save_model(str(out_dir / "models" / f"{slug(name)}.cbm"))
        test_preds[name] = predict(model, test, cols)
        importances[name] = pl.DataFrame({"feature": cols, "importance": model.get_feature_importance()}).sort("importance", descending=True)
        importances[name].write_csv(out_dir / "importance" / f"{slug(name)}.csv")

    test_table = results_table(test_preds, test)
    test_table.write_csv(out_dir / "test_metrics.csv")
    print(test_table.filter(pl.col("slice") == "all").select("model", "logloss", "auc", "gauc", "ndcg@10"))

    boot_models = list(sets) + ["logreg"]
    samples = bootstrap(test, {k: test_preds[k] for k in boot_models}, n_boot=n_boot)
    deltas = {f"{name}_vs_{REFERENCE}": paired_delta(samples, name, REFERENCE) for name in boot_models if name != REFERENCE}

    if "L1-wide" in importances:
        importance_by_scale(importances["L1-wide"], "d_", meta["taus"]).write_csv(out_dir / "tau_importance.csv")
    importance_by_scale(importances[REFERENCE], "", ["1h", "1d", "7d", "30d", "all"]).filter(
        pl.col("feature_base").is_in([c.rsplit("_", 1)[0] for c in meta["window_features"]])
    ).write_csv(out_dir / "window_importance.csv")

    pred_cols = {f"pred_{slug(k)}": np.asarray(test_preds[k], dtype=np.float32) for k in boot_models}
    test.select("uid", "timestamp", "item_id", "days_before_end", "label", "x_novelty").with_columns(
        [pl.Series(k, v) for k, v in pred_cols.items()]
    ).write_parquet(out_dir / "test_predictions.parquet")

    summary = {
        "reference": REFERENCE,
        "rows": {"train": train.height, "val": val.height, "test": test.height},
        "feature_sets": {k: v for k, v in sets.items()},
        "records": records,
        "task_type": task_type,
        "n_boot": n_boot,
        "test_bootstrap_ci": summarize(samples),
        "test_paired_deltas": deltas,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
