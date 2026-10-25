import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.discovery import run_discovery


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(ROOT / "data" / "yambda" / "derived" / "50m" / "features"))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "discovery"))
    parser.add_argument("--task-type", default="CPU", choices=["CPU", "GPU"])
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--n-boot", type=int, default=100)
    parser.add_argument("--alphabet", default="rich", choices=["base", "rich"])
    args = parser.parse_args()
    summary = run_discovery(args.features, args.out, args.task_type, args.device, args.iterations, args.n_boot, args.alphabet)
    print(json.dumps(summary["test_paired_deltas"], indent=2))


if __name__ == "__main__":
    main()
