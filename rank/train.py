import time

import numpy as np
import polars as pl
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from . import config

LOGREG_FEATURES = [
    "u_rec_lp_rate_30d", "u_rec_lp_rate_1h", "u_org_share_30d", "i_rec_lp_smooth_30d", "i_len",
    "ui_cnt_all", "ui_lp_rate_all", "ui_recency_h", "ua_cnt_30d", "ua_lp_rate_all", "ua_share_30d",
    "ui_like_state", "ui_dislike_state", "c_prev1_lp_rate", "c_prev3_lp_rate", "c_session_lp_rate", "x_novelty",
]
SINGLE_FEATURES = ["u_rec_lp_rate_30d", "i_rec_lp_smooth_30d", "c_prev3_lp_rate"]
FINAL_ITERATION_FACTOR = 1.15


def catboost_params(task_type, iterations, learning_rate=0.08, depth=8, seed=config.SEED):
    params = dict(
        loss_function="Logloss",
        eval_metric="Logloss",
        iterations=iterations,
        learning_rate=learning_rate,
        depth=depth,
        l2_leaf_reg=3,
        random_seed=seed,
        task_type=task_type,
        metric_period=50,
        verbose=500,
    )
    if task_type == "CPU":
        params["thread_count"] = 4
    return params


def matrix(df, cols):
    return df.select(cols).to_numpy().astype(np.float32)


def signed_log(x):
    return np.sign(x) * np.log1p(np.abs(x))


class LinearModel:
    def __init__(self, cols):
        self.cols = cols

    def transform(self, df):
        x = matrix(df, self.cols)
        return signed_log(np.where(np.isnan(x), self.median, x))

    def fit(self, df):
        x = matrix(df, self.cols)
        self.median = np.nan_to_num(np.nanmedian(x, axis=0))
        x = signed_log(np.where(np.isnan(x), self.median, x))
        self.scaler = StandardScaler().fit(x)
        self.model = LogisticRegression(max_iter=500).fit(self.scaler.transform(x), df["label"].to_numpy())
        return self

    def predict(self, df):
        return self.model.predict_proba(self.scaler.transform(self.transform(df)))[:, 1]


def fit_catboost(train, val, cols, task_type, iterations, seed=config.SEED):
    model = CatBoostClassifier(**catboost_params(task_type, iterations, seed=seed), od_type="Iter", od_wait=200, use_best_model=True)
    started = time.time()
    model.fit(matrix(train, cols), train["label"].to_numpy(), eval_set=(matrix(val, cols), val["label"].to_numpy()))
    return model, time.time() - started


def refit_catboost(data, cols, task_type, best_iteration, seed=config.SEED):
    model = CatBoostClassifier(**catboost_params(task_type, int(best_iteration * FINAL_ITERATION_FACTOR), seed=seed))
    started = time.time()
    model.fit(matrix(data, cols), data["label"].to_numpy())
    return model, time.time() - started


def predict(model, df, cols):
    return model.predict_proba(matrix(df, cols))[:, 1]


def simple_baselines(train, val, test):
    trainval = pl.concat([train, val], how="vertical")
    val_preds = {"constant": np.full(val.height, train["label"].mean())}
    test_preds = {"constant": np.full(test.height, trainval["label"].mean())}
    for feat in SINGLE_FEATURES:
        val_preds[f"single:{feat}"] = LinearModel([feat]).fit(train).predict(val)
        test_preds[f"single:{feat}"] = LinearModel([feat]).fit(trainval).predict(test)
    val_preds["logreg"] = LinearModel(LOGREG_FEATURES).fit(train).predict(val)
    test_preds["logreg"] = LinearModel(LOGREG_FEATURES).fit(trainval).predict(test)
    return val_preds, test_preds
