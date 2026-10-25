import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import polars as pl

from rank.scale import SEEDS, SIZES, run_scale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "scale"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    parser.add_argument("--sizes", type=int, nargs="+", default=list(SIZES))
    args = parser.parse_args()
    summary = run_scale(args.features, args.out, args.task_type, args.device, args.iterations, tuple(args.seeds), tuple(args.sizes))
    print(pl.DataFrame([{k: r[k] for k in ("comparison", "metric", "delta", "p_holm")} for r in summary["stat_tests_vs_human"]]))


if __name__ == "__main__":
    main()
