import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.experiments import run_experiments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "experiments"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--n-boot", type=int, default=100)
    parser.add_argument("--no-ablation", action="store_true")
    args = parser.parse_args()
    summary = run_experiments(args.features, args.out, args.task_type, args.iterations, args.n_boot, not args.no_ablation)
    print(json.dumps(summary["test_paired_deltas"], indent=2))


if __name__ == "__main__":
    main()
