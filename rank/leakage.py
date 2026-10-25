import json
from pathlib import Path

import numpy as np
import polars as pl
from sklearn.metrics import roc_auc_score

from . import config
from .cf import fit_item_factors
from .features import build_features, cf_cutoff, scan_listens_dir


def load_all(features_dir):
    return pl.concat([pl.read_parquet(Path(features_dir) / f"{s}.parquet") for s in config.SPLITS], how="vertical")


def compare(full, trunc, columns):
    report = {}
    for c in columns:
        a = full[c].to_numpy().astype(np.float64)
        b = trunc[c].to_numpy().astype(np.float64)
        both_nan = np.isnan(a) & np.isnan(b)
        close = np.isclose(a, b, rtol=1e-5, atol=1e-6)
        report[c] = int((~(both_nan | close)).sum())
    return report


def single_feature_auc(df, columns):
    y = df["label"].to_numpy()
    out = {}
    for c in columns:
        x = df[c].to_numpy().astype(np.float64)
        ok = ~np.isnan(x)
        if ok.sum() > 100 and len(np.unique(y[ok])) > 1:
            auc = roc_auc_score(y[ok], x[ok])
            out[c] = float(max(auc, 1 - auc))
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def check_leakage(listens_dir, events_path, mappings_dir, work_dir, t_end, prior, max_parts=1, cut_days_before_end=10, **feature_kwargs):
    work_dir = Path(work_dir)
    cut = t_end - cut_days_before_end * config.DAY
    cf = fit_item_factors(scan_listens_dir(listens_dir), cf_cutoff(t_end))
    common = dict(listens_dir=listens_dir, events_path=events_path, mappings_dir=mappings_dir, t_end=t_end, max_parts=max_parts, canary=True, prior=prior, cf=cf, **feature_kwargs)
    build_features(out_dir=work_dir / "leak_full", **common)
    build_features(out_dir=work_dir / "leak_trunc", max_ts=cut, **common)

    window = (pl.col("timestamp") >= cut - config.DAY) & (pl.col("timestamp") < cut)
    full = load_all(work_dir / "leak_full")
    trunc = load_all(work_dir / "leak_trunc")
    full_w = full.filter(window).sort("uid", "timestamp", "obj_id")
    trunc_w = trunc.filter(window).sort("uid", "timestamp", "obj_id")
    assert full_w.height == trunc_w.height, (full_w.height, trunc_w.height)

    meta = json.loads((work_dir / "leak_full" / "meta.json").read_text())
    canaries = [c for c in full.columns if c.startswith("canary_")]
    mismatches = compare(full_w, trunc_w, meta["features"] + canaries)
    real = {c: n for c, n in mismatches.items() if not c.startswith("canary_")}
    val = full.filter(pl.col("split") == "val")
    aucs = single_feature_auc(val, meta["features"] + canaries)
    report = {
        "cut_ts": cut,
        "objects_compared": full_w.height,
        "features_with_mismatch": {c: n for c, n in real.items() if n > 0},
        "canary_mismatches": {c: mismatches[c] for c in canaries},
        "passed": all(n == 0 for n in real.values()) and mismatches.get("canary_next_ratio", 0) > 0,
        "single_feature_auc_top10": dict(list({c: a for c, a in aucs.items() if not c.startswith("canary_")}.items())[:10]),
        "canary_auc": {c: aucs.get(c) for c in canaries},
    }
    return report
