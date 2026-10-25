import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import polars as pl

from rank.stats import ALPHA, N_PERM, POWER, run_stat_tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions")
    parser.add_argument("--out", default=None)
    parser.add_argument("--reference", default="human")
    parser.add_argument("--n-perm", type=int, default=N_PERM)
    parser.add_argument("--alpha", type=float, default=ALPHA)
    parser.add_argument("--power", type=float, default=POWER)
    parser.add_argument("--models", nargs="+", default=None)
    args = parser.parse_args()
    out = Path(args.out or Path(args.predictions).parent)
    out.mkdir(parents=True, exist_ok=True)
    rows = run_stat_tests(args.predictions, out, args.reference, args.n_perm, args.alpha, args.power, args.models)
    cols = ["comparison", "metric", "n_seeds", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "power_at_delta", "reject_h0"]
    with pl.Config(tbl_rows=100, tbl_cols=20, tbl_width_chars=250):
        print(pl.DataFrame([{c: r[c] for c in cols} for r in rows]).with_columns(pl.col(pl.Float64).round(5)))


if __name__ == "__main__":
    main()
