import numpy as np
import polars as pl
from sklearn.metrics import log_loss, roc_auc_score

from . import config

NOVELTY = {0: "repeat_track", 1: "new_track_known_artist", 2: "new_artist"}
METRICS = ("logloss", "auc", "gauc", "ndcg@10")


def per_user_auc(frame):
    return (
        frame.with_columns(pl.col("pred").rank("average").over("uid").alias("r"))
        .group_by("uid")
        .agg(
            pl.len().alias("n"),
            pl.col("label").sum().alias("pos"),
            pl.col("r").filter(pl.col("label") == 1).sum().alias("rank_pos"),
        )
        .filter((pl.col("pos") > 0) & (pl.col("pos") < pl.col("n")))
        .with_columns(
            ((pl.col("rank_pos") - pl.col("pos") * (pl.col("pos") + 1) / 2) / (pl.col("pos") * (pl.col("n") - pl.col("pos")))).alias("auc")
        )
        .select("uid", "n", "auc")
    )


def per_group_ndcg(frame, k=10):
    position = pl.int_range(1, pl.len() + 1).cast(pl.Float64)
    gain = 1.0 / (position + 1).log(2)
    return (
        frame.group_by("uid", "day")
        .agg(
            (pl.col("label").sort_by("pred", descending=True).cast(pl.Float64) * gain).head(k).sum().alias("dcg"),
            (pl.col("label").sort(descending=True).cast(pl.Float64) * gain).head(k).sum().alias("idcg"),
        )
        .filter(pl.col("idcg") > 0)
        .with_columns((pl.col("dcg") / pl.col("idcg")).alias("ndcg"))
        .select("uid", "day", "ndcg")
    )


class Scorer:
    def __init__(self, frame):
        self.frame = frame
        self.y = frame["label"].to_numpy()
        self.p = np.clip(frame["pred"].to_numpy(), 1e-6, 1 - 1e-6)
        self.uid = frame["uid"].to_numpy()
        self.users = per_user_auc(frame)
        self.groups = per_group_ndcg(frame)

    def score(self, user_weights=None):
        if user_weights is None:
            w = None
            users_w = self.users["n"].to_numpy().astype(np.float64)
            groups_w = np.ones(self.groups.height)
        else:
            w = user_weights[self.uid]
            users_w = self.users["n"].to_numpy() * user_weights[self.users["uid"].to_numpy()]
            groups_w = user_weights[self.groups["uid"].to_numpy()].astype(np.float64)
        has_both = len(np.unique(self.y)) > 1
        return {
            "n": int(len(self.y)),
            "logloss": float(log_loss(self.y, self.p, sample_weight=w, labels=[0, 1])),
            "auc": float(roc_auc_score(self.y, self.p, sample_weight=w)) if has_both else float("nan"),
            "gauc": float(np.average(self.users["auc"].to_numpy(), weights=users_w)) if users_w.sum() > 0 else float("nan"),
            "ndcg@10": float(np.average(self.groups["ndcg"].to_numpy(), weights=groups_w)) if groups_w.sum() > 0 else float("nan"),
        }


def prepare_frame(df, pred):
    return pl.DataFrame({
        "uid": df["uid"].cast(pl.Int64),
        "day": df["days_before_end"],
        "label": df["label"].cast(pl.Int32),
        "pred": np.asarray(pred, dtype=np.float64),
        "novelty": df["x_novelty"].cast(pl.Int32),
    })


def evaluate_slices(df, pred):
    frame = prepare_frame(df, pred)
    rows = [{"slice": "all", **Scorer(frame).score()}]
    for code, name in NOVELTY.items():
        part = frame.filter(pl.col("novelty") == code)
        if part.height:
            rows.append({"slice": name, **Scorer(part).score()})
    return rows


def bootstrap(df, preds, n_boot=100, seed=config.SEED):
    scorers = {name: Scorer(prepare_frame(df, p)) for name, p in preds.items()}
    uids = np.unique(df["uid"].to_numpy()).astype(np.int64)
    rng = np.random.default_rng(seed)
    samples = {name: [] for name in preds}
    for _ in range(n_boot):
        counts = np.bincount(rng.integers(0, len(uids), len(uids)), minlength=len(uids)).astype(np.float64)
        weights = np.zeros(uids.max() + 1)
        weights[uids] = counts
        for name, scorer in scorers.items():
            samples[name].append(scorer.score(weights))
    return samples


def interval(values):
    values = np.asarray(values)
    return {"mean": float(values.mean()), "lo": float(np.quantile(values, 0.025)), "hi": float(np.quantile(values, 0.975))}


def summarize(samples):
    return {name: {m: interval([r[m] for r in runs]) for m in METRICS} for name, runs in samples.items()}


def paired_delta(samples, a, b):
    return {m: interval([x[m] - y[m] for x, y in zip(samples[a], samples[b])]) for m in METRICS}
