import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.prepare import prepare_listens


def main():
    data = ROOT / "data" / "yambda"
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", default=str(data / "flat" / "50m" / "multi_event.parquet"))
    parser.add_argument("--mappings", default=str(data))
    parser.add_argument("--out", default=str(data / "derived" / "50m" / "listens"))
    parser.add_argument("--users-per-chunk", type=int, default=1000)
    args = parser.parse_args()
    prepare_listens(args.events, args.mappings, args.out, args.users_per_chunk)


if __name__ == "__main__":
    main()
