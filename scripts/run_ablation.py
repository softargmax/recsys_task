import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import polars as pl

from rank.ablation import SEEDS, run_ablation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "ablation"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    args = parser.parse_args()
    summary = run_ablation(args.features, args.out, args.task_type, args.device, args.iterations, tuple(args.seeds))
    print(pl.DataFrame(summary["channel_effects"]))


if __name__ == "__main__":
    main()
