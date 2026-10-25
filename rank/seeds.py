import gc
import json
import time
from itertools import combinations

import numpy as np
import polars as pl

from . import config
from .basis import ALPHABETS
from .discovery import REFERENCE, add_columns, fit_set, load_frames, make_dirs, save_predictions, write_descriptions
from .experiments import results_table
from .learned import describe, fit_grammar, save_grammar, transform
from .metrics import METRICS, bootstrap, paired_delta, summarize
from .stats import run_stat_tests

SEEDS = (42, 7, 13, 101, 2024)
GRAMMAR_K = 32
HYBRID_K = 16
STABILITY_ROWS = 100_000


def seed_name(model, seed):
    return f"{model}_s{seed}"


def mean_over_seeds(samples, model, seeds):
    runs = [samples[seed_name(model, s)] for s in seeds]
    return [{m: float(np.mean([r[i][m] for r in runs])) for m in METRICS} for i in range(len(runs[0]))]


def value_overlap(a, b):
    k = a.shape[1]
    corr = np.nan_to_num(np.corrcoef(a.T, b.T)[:k, k:])
    return float(np.abs(corr).max(axis=1).mean())


def signature(rows):
    return {(max(r["relation"], key=r["relation"].get), max(r["kernel"], key=r["kernel"].get), r["kind"]) for r in rows}


def stability(val_feats, descriptions):
    rows = []
    for a, b in combinations(sorted(val_feats), 2):
        sa, sb = signature(descriptions[a]), signature(descriptions[b])
        rows.append({
            "seed_a": a, "seed_b": b,
            "value_overlap": value_overlap(val_feats[a], val_feats[b]),
            "signature_jaccard": len(sa & sb) / len(sa | sb),
        })
    return rows


def run_seeds(features_dir, out_dir, task_type="GPU", device="cuda", iterations=3000, n_boot=100, alphabet="rich", seeds=SEEDS):
    out_dir = make_dirs(out_dir)
    alphabet = ALPHABETS[alphabet]
    fixed, human, (train, val, test) = load_frames(features_dir, alphabet)
    rows = np.sort(np.random.default_rng(config.SEED).choice(val.height, min(STABILITY_ROWS, val.height), replace=False))
    print(f"alphabet {alphabet.name}; train {train.height}, val {val.height}, test {test.height}; seeds {list(seeds)}")

    records, val_preds, test_preds, timings = {}, {}, {}, {}
    val_feats, descriptions = {}, {}
    hybrid = f"human+grammar{HYBRID_K}"
    for seed in seeds:
        started = time.time()
        run = dict(train=train, val=val, test=test, rates={}, task_type=task_type, iterations=iterations, out_dir=out_dir,
                   records=records, val_preds=val_preds, test_preds=test_preds, seed=seed)
        fit_set(seed_name(REFERENCE, seed), fixed + human, **run)
        names = {}
        for k in (HYBRID_K, GRAMMAR_K):
            model, inputs, _ = fit_grammar(train, val, fixed, k // 2, k - k // 2, device, alphabet, seed=seed)
            names[k] = [f"g{k}_s{seed}_{j:02d}" for j in range(k)]
            train = add_columns(train, names[k], transform(model, inputs, train, device)[1])
            val_preds[seed_name(f"grammar_nn{k}", seed)], feats = transform(model, inputs, val, device)
            val = add_columns(val, names[k], feats)
            test_preds[seed_name(f"grammar_nn{k}", seed)], feats = transform(model, inputs, test, device)
            test = add_columns(test, names[k], feats)
            rows_k = describe(model)
            write_descriptions(out_dir, f"{k}_s{seed}", rows_k)
            save_grammar(out_dir / "grammar" / f"model_k{k}_s{seed}.pt", model, inputs)
            if k == GRAMMAR_K:
                val_feats[seed] = val.select(names[k]).to_numpy()[rows]
                descriptions[seed] = rows_k
            del model, inputs
            gc.collect()
        run.update(train=train, val=val, test=test)
        fit_set(seed_name(f"grammar{GRAMMAR_K}", seed), fixed + names[GRAMMAR_K], **run)
        fit_set(seed_name(hybrid, seed), fixed + human + names[HYBRID_K], **run)
        added = names[HYBRID_K] + names[GRAMMAR_K]
        train, val, test = (df.drop(added) for df in (train, val, test))
        gc.collect()
        timings[f"seed_{seed}_s"] = round(time.time() - started, 1)
        print(f"seed {seed} done in {timings[f'seed_{seed}_s']:.0f}s")

    val_table = results_table(val_preds, val)
    val_table.write_csv(out_dir / "val_metrics.csv")
    test_table = results_table(test_preds, test)
    test_table.write_csv(out_dir / "test_metrics.csv")
    save_predictions(out_dir, test, test_preds)

    samples = bootstrap(test, test_preds, n_boot=n_boot)
    compared = [f"grammar{GRAMMAR_K}", hybrid, f"grammar_nn{GRAMMAR_K}"]
    per_seed = {
        f"{m}_vs_{REFERENCE}": {str(s): paired_delta(samples, seed_name(m, s), seed_name(REFERENCE, s)) for s in seeds}
        for m in compared
    }
    for m in compared + [REFERENCE]:
        samples[f"{m}_mean"] = mean_over_seeds(samples, m, seeds)
    seed_mean = {f"{m}_vs_{REFERENCE}": paired_delta(samples, f"{m}_mean", f"{REFERENCE}_mean") for m in compared}

    point = test_table.filter(pl.col("slice") == "all")
    spread = {}
    for m in compared + [REFERENCE]:
        for metric in METRICS:
            values = [point.filter(pl.col("model") == seed_name(m, s))[metric].item() for s in seeds]
            spread.setdefault(m, {})[metric] = {"mean": float(np.mean(values)), "std": float(np.std(values, ddof=1)), "values": values}
    wins = {
        m: sum(per_seed[f"{m}_vs_{REFERENCE}"][str(s)]["gauc"]["mean"] > 0 for s in seeds) for m in compared
    }

    stab = stability(val_feats, descriptions)
    pl.DataFrame(stab).write_csv(out_dir / "stability.csv")
    summary = {
        "reference": REFERENCE,
        "alphabet": alphabet.name,
        "seeds": list(seeds),
        "records": records,
        "timings": timings,
        "test_point_spread": spread,
        "test_seed_mean_deltas": seed_mean,
        "test_per_seed_deltas": per_seed,
        "gauc_wins_vs_reference": wins,
        "stability_mean": {k: float(np.mean([r[k] for r in stab])) for k in ["value_overlap", "signature_jaccard"]},
        "test_bootstrap_ci": summarize({k: v for k, v in samples.items() if k.endswith("_mean")}),
        "n_boot": n_boot,
    }
    summary["stat_tests"] = run_stat_tests(out_dir / "test_predictions.parquet", out_dir, reference=REFERENCE, models=compared)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
