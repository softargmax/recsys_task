import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import polars as pl

from rank.features import dataset_end, history_prior
from rank.leakage import check_leakage


def main():
    data = ROOT / "data" / "yambda"
    parser = argparse.ArgumentParser()
    parser.add_argument("--listens", default=str(data / "derived" / "50m" / "listens"))
    parser.add_argument("--events", default=str(data / "flat" / "50m" / "multi_event.parquet"))
    parser.add_argument("--mappings", default=str(data))
    parser.add_argument("--work", default=str(data / "derived" / "50m" / "leakage"))
    parser.add_argument("--max-parts", type=int, default=1)
    parser.add_argument("--out", default=str(ROOT / "outputs" / "baseline" / "leakage_report.json"))
    args = parser.parse_args()
    t_end = dataset_end(args.events)
    prior = history_prior(pl.scan_parquet(str(Path(args.listens) / "part_*.parquet")), t_end)
    report = check_leakage(args.listens, args.events, args.mappings, args.work, t_end, prior, max_parts=args.max_parts)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
