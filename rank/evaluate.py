import json
from pathlib import Path

import numpy as np
import polars as pl
import torch
from catboost import CatBoostClassifier

from .basis import ALPHABETS
from .discovery import EVAL_COLS, fixed_and_human
from .experiments import results_table, slug
from .prune import load_grammar
from .stats import run_stat_tests

SETS = {
    "human": (None, "human"),
    "grammar32": (32, None),
    "human+grammar16": (16, "human"),
}


def metrics_from_predictions(predictions_path, out_dir, reference="human", models=None, n_perm=100_000):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pl.read_parquet(predictions_path)
    preds = {c[len("pred_"):]: df[c].to_numpy() for c in df.columns if c.startswith("pred_")}
    table = results_table(preds, df)
    table.write_csv(out_dir / "test_metrics.csv")
    tests = run_stat_tests(predictions_path, out_dir, reference=reference, models=models, n_perm=n_perm)
    return table, tests


def evaluate_weights(features_dir, artifacts_dir, out_dir, seed=42, kaggle_predictions=None):
    features_dir, artifacts_dir, out_dir = Path(features_dir), Path(artifacts_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = json.loads((features_dir / "meta.json").read_text())
    fixed, human = fixed_and_human(meta)
    alphabet = ALPHABETS["rich"]
    cols = list(dict.fromkeys(EVAL_COLS + ["x_novelty"] + fixed + human + alphabet.columns()))
    test = pl.read_parquet(features_dir / "test.parquet", columns=cols)
    preds = {}
    for name, (k, extra) in SETS.items():
        parts = [test.select(fixed + (human if extra == "human" else [])).to_numpy().astype(np.float32)]
        if k is not None:
            model, inputs = load_grammar(artifacts_dir / "grammar" / f"model_k{k}_s{seed}.pt")
            with torch.no_grad():
                parts.append(model.grammar(inputs.basis(test)).numpy().astype(np.float32))
        cb = CatBoostClassifier()
        cb.load_model(str(artifacts_dir / "models" / f"{slug(name)}_s{seed}.cbm"))
        preds[name] = cb.predict_proba(np.hstack(parts))[:, 1]
    table = results_table(preds, test)
    table.write_csv(out_dir / f"test_metrics_from_weights_s{seed}.csv")
    report = {"rows": test.height, "seed": seed}
    if kaggle_predictions is not None:
        kaggle = pl.read_parquet(kaggle_predictions).head(test.height)
        aligned = kaggle["uid"].cast(pl.Int64).equals(test["uid"].cast(pl.Int64))
        report["aligned_with_kaggle"] = bool(aligned)
        if aligned:
            report["max_abs_diff"] = {
                name: float(np.abs(p - kaggle[f"pred_{name}_s{seed}"].to_numpy()).max()) for name, p in preds.items()
            }
            report["mean_abs_diff"] = {
                name: float(np.abs(p - kaggle[f"pred_{name}_s{seed}"].to_numpy()).mean()) for name, p in preds.items()
            }
    (out_dir / f"weights_check_s{seed}.json").write_text(json.dumps(report, indent=2))
    return table, report
