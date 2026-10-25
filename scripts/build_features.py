import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.features import build_features


def main():
    data = ROOT / "data" / "yambda"
    parser = argparse.ArgumentParser()
    parser.add_argument("--listens", default=str(data / "derived" / "50m" / "listens"))
    parser.add_argument("--events", default=str(data / "flat" / "50m" / "multi_event.parquet"))
    parser.add_argument("--mappings", default=str(data))
    parser.add_argument("--out", default=str(data / "derived" / "50m" / "features"))
    parser.add_argument("--max-parts", type=int, default=None)
    parser.add_argument("--no-cf", action="store_true")
    parser.add_argument("--taus", nargs="*", default=None)
    parser.add_argument("--basis", action="store_true")
    args = parser.parse_args()
    kwargs = {"cf": None} if args.no_cf else {}
    kwargs["basis"] = args.basis
    if args.taus is not None:
        kwargs["taus"] = tuple(args.taus)
    build_features(args.listens, args.events, args.mappings, args.out, max_parts=args.max_parts, **kwargs)


if __name__ == "__main__":
    main()
