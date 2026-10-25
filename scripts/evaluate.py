import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import polars as pl

from rank.evaluate import evaluate_weights, metrics_from_predictions

RUN = ROOT / "outputs" / "kaggle_seeds_v2" / "outputs"


def show(table):
    with pl.Config(tbl_rows=100, tbl_cols=12, tbl_width_chars=200):
        print(table.select("model", "slice", "n", "logloss", "auc", "gauc", "ndcg@10").with_columns(pl.col(pl.Float64).round(4)))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("predictions")
    p.add_argument("--predictions", default=str(RUN / "test_predictions.parquet"))
    p.add_argument("--out", default=str(ROOT / "outputs" / "evaluate"))
    p.add_argument("--reference", default="human")
    p.add_argument("--models", nargs="+", default=["grammar32", "human+grammar16", "grammar_nn32"])
    p.add_argument("--n-perm", type=int, default=100_000)
    w = sub.add_parser("weights")
    w.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    w.add_argument("--artifacts", default=str(RUN))
    w.add_argument("--out", default=str(ROOT / "outputs" / "evaluate"))
    w.add_argument("--seed", type=int, default=42)
    w.add_argument("--kaggle-predictions", default=str(RUN / "test_predictions.parquet"))
    args = parser.parse_args()
    if args.mode == "predictions":
        table, tests = metrics_from_predictions(args.predictions, args.out, args.reference, args.models, args.n_perm)
        show(table.filter(pl.col("slice") == "all"))
        cols = ["comparison", "metric", "n_seeds", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "reject_h0"]
        with pl.Config(tbl_rows=100, tbl_cols=12, tbl_width_chars=220):
            print(pl.DataFrame([{c: r[c] for c in cols} for r in tests]).with_columns(pl.col(pl.Float64).round(5)))
    else:
        kaggle = args.kaggle_predictions if Path(args.kaggle_predictions).exists() else None
        table, report = evaluate_weights(args.features, args.artifacts, args.out, args.seed, kaggle)
        show(table)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
