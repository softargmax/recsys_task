import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.sparse import SEEDS, run_sparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "sparse"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    args = parser.parse_args()
    summary = run_sparse(args.features, args.out, args.task_type, args.device, args.iterations, tuple(args.seeds))
    print(json.dumps(summary["cells_count"], indent=2))


if __name__ == "__main__":
    main()
