import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.prune import SEEDS, run_prune


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--weights", default=str(ROOT / "outputs" / "kaggle_seeds_v2" / "outputs" / "grammar"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "prune"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    args = parser.parse_args()
    summary = run_prune(args.features, args.weights, args.out, args.task_type, args.device, args.iterations, tuple(args.seeds))
    print(json.dumps(summary["cells_count"], indent=2))


if __name__ == "__main__":
    main()
