import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rank.cf import fit_item_factors
from rank.cost import feature_build_cost, run_cost_report
from rank.features import cf_cutoff, dataset_end, scan_listens_dir


def main():
    data = ROOT / "data" / "yambda"
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", default=str(data / "derived" / "50m" / "features_rich_part0"))
    parser.add_argument("--run", default=str(ROOT / "outputs" / "kaggle_seeds_v2" / "outputs"))
    parser.add_argument("--listens", default=str(data / "derived" / "50m" / "listens"))
    parser.add_argument("--events", default=str(data / "flat" / "50m" / "multi_event.parquet"))
    parser.add_argument("--mappings", default=str(data))
    parser.add_argument("--out", default=str(ROOT / "outputs" / "cost"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()
    t_end = dataset_end(args.events)
    build = None
    if not args.skip_build:
        cf = fit_item_factors(scan_listens_dir(args.listens), cf_cutoff(t_end))
        build = feature_build_cost(args.listens, args.events, args.mappings, t_end, cf)
        del cf
    report = run_cost_report(args.features, args.run, args.listens, args.out, args.seed, t_end, build)
    brief = {k: v for k, v in report.items() if k not in ("pruning", "state_numbers_per_user")}
    brief["pruning"] = [{k: v for k, v in p.items() if k != "cells"} for p in report["pruning"]]
    brief["state_numbers_per_user"] = {k: {m: v[m] for m in ("mean", "median", "p90")} for k, v in report["state_numbers_per_user"].items()}
    print(json.dumps(brief, indent=2))


if __name__ == "__main__":
    main()
