import json
import re
from pathlib import Path

import numpy as np
import polars as pl
from scipy import stats

from .metrics import per_group_ndcg, per_user_auc

ALPHA = 0.05
POWER = 0.8
N_PERM = 100_000
PERM_CHUNK = 1000
TEST_METRICS = ("gauc", "ndcg@10", "logloss")
SEED_SUFFIX = re.compile(r"^(.*)_s(\d+)$")


def model_frame(df, col):
    return df.select(
        pl.col("uid").cast(pl.Int64),
        pl.col("days_before_end").alias("day"),
        pl.col("label").cast(pl.Int32),
        pl.col(col).cast(pl.Float64).clip(1e-6, 1 - 1e-6).alias("pred"),
    )


def user_terms(df, col):
    f = model_frame(df, col)
    auc = per_user_auc(f).select("uid", (pl.col("n") * pl.col("auc")).alias("value"), pl.col("n").cast(pl.Float64).alias("weight"))
    ndcg = per_group_ndcg(f).group_by("uid").agg(pl.col("ndcg").sum().alias("value"), pl.len().cast(pl.Float64).alias("weight"))
    loss = -(pl.col("label") * pl.col("pred").log() + (1 - pl.col("label")) * (1 - pl.col("pred")).log())
    logloss = f.group_by("uid").agg(loss.sum().alias("value"), pl.len().cast(pl.Float64).alias("weight"))
    return {m: t.sort("uid") for m, t in zip(TEST_METRICS, (auc, ndcg, logloss))}


def sign_flip_pvalue(s, delta, total_weight, n_perm=N_PERM, seed=0):
    rng = np.random.default_rng(seed)
    exceed, done = 0, 0
    while done < n_perm:
        k = min(PERM_CHUNK, n_perm - done)
        signs = rng.integers(0, 2, size=(k, len(s)), dtype=np.int8).astype(np.float64) * 2 - 1
        null = signs @ s / total_weight
        exceed += int((np.abs(null) >= abs(delta) * (1 - 1e-12)).sum())
        done += k
    return (exceed + 1) / (n_perm + 1)


def paired_test(s, w, n_perm=N_PERM, alpha=ALPHA, power=POWER):
    total = w.sum()
    delta = s.sum() / total
    n = len(s)
    se = np.sqrt(((s - w * delta) ** 2).sum() * n / (n - 1)) / total
    z = delta / se
    z_alpha, z_power = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    return {
        "delta": float(delta),
        "se": float(se),
        "ci_lo": float(delta - z_alpha * se),
        "ci_hi": float(delta + z_alpha * se),
        "z": float(z),
        "p_z": float(2 * stats.norm.sf(abs(z))),
        "p_perm": float(sign_flip_pvalue(s, delta, total, n_perm)),
        "mde": float((z_alpha + z_power) * se),
        "power_at_delta": float(stats.norm.sf(z_alpha - abs(z)) + stats.norm.cdf(-z_alpha - abs(z))),
        "n_users": int(n),
    }


def holm(pvalues):
    p = np.asarray(pvalues, dtype=np.float64)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adjusted[i] = min(running, 1.0)
    return adjusted


def comparisons_from_columns(columns, reference):
    runs = {}
    for col in columns:
        if not col.startswith("pred_"):
            continue
        name = col[len("pred_"):]
        match = SEED_SUFFIX.match(name)
        base, seed = (match.group(1), int(match.group(2))) if match else (name, None)
        runs.setdefault(base, {})[seed] = col
    ref = runs[reference]
    out = {}
    for base, by_seed in runs.items():
        if base == reference:
            continue
        common = sorted(set(by_seed) & set(ref), key=lambda x: -1 if x is None else x)
        if common:
            out[f"{base}_vs_{reference}"] = [(by_seed[s], ref[s]) for s in common]
    return out


def run_stat_tests(predictions_path, out_dir, reference="human", n_perm=N_PERM, alpha=ALPHA, power=POWER, models=None, name="stat_tests"):
    df = pl.read_parquet(predictions_path)
    comparisons = comparisons_from_columns(df.columns, reference)
    if models is not None:
        comparisons = {f"{m}_vs_{reference}": comparisons[f"{m}_vs_{reference}"] for m in models}
    cache = {}

    def terms(col):
        if col not in cache:
            cache[col] = user_terms(df, col)
        return cache[col]

    rows = []
    for comparison, pairs in comparisons.items():
        for metric in TEST_METRICS:
            diffs, per_seed, weight, uid = [], [], None, None
            for a, b in pairs:
                ta, tb = terms(a)[metric], terms(b)[metric]
                assert ta["uid"].equals(tb["uid"]), f"user sets differ for {a} and {b}"
                d = (ta["value"] - tb["value"]).to_numpy()
                weight = ta["weight"].to_numpy()
                uid = ta["uid"] if uid is None else uid
                assert uid.equals(ta["uid"]), "user sets differ between seeds"
                diffs.append(d)
                per_seed.append(float(d.sum() / weight.sum()))
            row = {"comparison": comparison, "metric": metric, "n_seeds": len(pairs),
                   **paired_test(np.mean(diffs, axis=0), weight, n_perm, alpha, power)}
            row["per_seed_delta"] = per_seed
            if len(pairs) > 1:
                t = stats.ttest_1samp(per_seed, 0.0)
                row["seed_t"], row["seed_p"] = float(t.statistic), float(t.pvalue)
            rows.append(row)
    adjusted = holm([r["p_perm"] for r in rows])
    for r, p in zip(rows, adjusted):
        r["p_holm"] = float(p)
        r["reject_h0"] = bool(p < alpha)
    out_dir = Path(out_dir)
    (out_dir / f"{name}.json").write_text(json.dumps(
        {"alpha": alpha, "power": power, "beta": 1 - power, "n_perm": n_perm, "reference": reference, "tests": rows}, indent=2))
    pl.DataFrame([{k: v for k, v in r.items() if k != "per_seed_delta"} for r in rows]).write_csv(out_dir / f"{name}.csv")
    return rows
