import argparse
import json
import shutil
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
KERNELS_DIR = ROOT / "kaggle" / "kernels"
MODULES = [
    "__init__.py", "config.py", "prepare.py", "windows.py", "cf.py", "basis.py", "user_features.py",
    "entity_features.py", "features.py", "metrics.py", "leakage.py", "train.py", "experiments.py",
    "learned.py", "stats.py", "discovery.py", "seeds.py", "alphabet.py", "ablation.py", "prune.py", "sparse.py", "scale.py",
]
FEATURES_KERNEL = "rabochi1024/yambda-features"
STAGES = {
    "features": {
        "id": FEATURES_KERNEL,
        "notebook": "yambda_features.ipynb",
        "feature_kwargs": "dict(basis=True)",
        "gpu": False,
    },
    "ladder": {
        "id": "rabochi1024/yambda-catboost-baseline",
        "notebook": "yambda_catboost_baseline.ipynb",
        "feature_kwargs": "dict(basis=False)",
    },
    "discovery": {
        "id": "rabochi1024/yambda-feature-discovery",
        "notebook": "yambda_feature_discovery.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
    },
    "ablation": {
        "id": "rabochi1024/yambda-grammar-ablation",
        "notebook": "yambda_grammar_ablation.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
    },
    "prune": {
        "id": "rabochi1024/yambda-grammar-prune",
        "notebook": "yambda_grammar_prune.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
        "sources": ["rabochi1024/yambda-grammar-seeds"],
        "run_kwargs": "seeds=(42, 7)",
    },
    "sparse": {
        "id": "rabochi1024/yambda-grammar-sparse",
        "notebook": "yambda_grammar_sparse.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
    },
    "scale": {
        "id": "rabochi1024/yambda-grammar-scale",
        "notebook": "yambda_grammar_scale.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
    },
    "seeds": {
        "id": "rabochi1024/yambda-grammar-seeds",
        "notebook": "yambda_grammar_seeds.ipynb",
        "feature_kwargs": "dict(taus=(), basis=True)",
    },
}

INTRO = {
    "features": """
# Yambda-50M: признаки для всех экспериментов

Ноутбук один раз строит все признаки (ручные окна, счётчики с затуханием, базис грамматики) и проверяет их на утечки.
Остальные ноутбуки подключают его вывод как вход и берут признаки отсюда, если хеш кода, который строит признаки, совпадает.
Если код поменялся, они пересчитывают признаки сами.
""",
    "ladder": """
# Yambda-50M: CatBoost baseline (L0) и счётчики с затуханием (L1)

Наборы признаков для CatBoost:
- `L0` - ручные признаки с окнами 1ч / 1д / 7д / 30д / вся история;
- `L0+cf` - плюс коллаборативные признаки (SVD по истории до начала train), опорный набор;
- `L1` - оконные счётчики пользователя и пар заменены счётчиками с затуханием `exp(-dt / tau)`, tau из {1ч, 1д, 7д, 30д, 90д};
- `L1-wide` - то же с сеткой tau из 7 значений;
- `L0+L1` - всё вместе.
""",
    "discovery": """
# Yambda-50M: кто лучше придумывает признаки - человек, перебор или градиент

Все наборы делят общую часть `fixed`: признаки трека, артиста и альбома, лайки, час и день недели, SVD-скор.
Сравниваются способы получить признаки по истории пользователя:
- `human` - признаки по истории, придуманные вручную (окна, сессия, повторы, CF-похожести);
- `brute_all` / `brute_topK` - перебор: все базисные суммы и доли из грамматики «связь x событие x ядро», отбор top-K по важности CatBoost (`brute_all` обучается на выборке 1M строк train);
- `randomK` - случайные K кандидатов из той же грамматики;
- `grammarK` - K признаков, которые выучил градиентом обучаемый слой: веса по связям, ядрам и типам событий в числителе и знаменателе;
- `grammar_nnK` - сам обучаемый слой с MLP-головой как модель без бустинга;
- `human+grammar16` - гибрид.

Алфавит `rich`: события «рекомендация / органика x дослушал / скипнул», доля прослушанного, дослушивания и скипы новых артистов;
ядра: последние 1 / 3 / 10 треков, текущая сессия, затухание 1ч - 90д, вся история, давность последнего события связи (1д, 30д).
Алфавит `base` первого эксперимента - его подмножество без новых событий и ядер.
""",
    "ablation": """
# Yambda-50M: какие каналы алфавита дают прирост

Алфавит `rich` отличается от `base` четырьмя каналами:
- `ratio` - доля прослушанного;
- `novel` - дослушивания и скипы новых для пользователя артистов;
- `sess` - ядро текущей сессии;
- `recency` - давность последнего события связи (ядра `x1d`, `x30d`).

Для `grammar32` обучаются 10 алфавитов: `rich`, `base`, `rich` без одного канала (leave-one-out) и `base` с одним каналом (add-one-in), на 2 сидах.
Значимость - парный перестановочный тест по пользователям против `rich` и против `human` с поправкой Холма.
""",
    "prune": """
# Yambda-50M: сколько ячеек базиса нужно выученным признакам

Слой грамматики берётся из ноутбука `yambda-grammar-seeds` (сиды 42 и 7), его веса не переобучаются.
Из весов строятся варианты 32 признаков, и на каждом CatBoost обучается заново:
- `dense` - исходные веса (все 490 ячеек базиса);
- `t0.001`, `t0.01`, `t0.05` - ячейки с весом ниже порога обнуляются;
- `readable` - каждый признак ровно такой, как его описание словами: одна связь, одно ядро, события с весом от 0.5.

Сравнение - парный перестановочный тест по пользователям против `dense` и против `human` с поправкой Холма.
""",
    "sparse": """
# Yambda-50M: дискретная грамматика

Слой обучается 4 эпохи как обычно (мягкие веса), затем переключается в жёсткий режим:
одна связь, одно ядро и события с весом от 0.5 на признак, градиент проходит через straight-through.
- `dense` - обычный слой с мягкими весами;
- `hard` - в жёсткой фазе выбор продолжает обучаться с lr грамматики x 0.1;
- `frozen` - в жёсткой фазе выбор заморожен, дообучается только голова.

Каждый признак `hard` и `frozen` ровно совпадает со своим описанием словами и использует одну ячейку базиса на каждое событие.
Сравнение на 3 сидах - парный перестановочный тест по пользователям против `dense` и против `human` с поправкой Холма.
""",
    "scale": """
# Yambda-50M: сколько выученных признаков нужно

На 3 сидах сравниваются `grammar32` и `grammar64` (32 и 64 выученных признака по истории) и гибриды с ручными признаками `human+grammar32`, `human+grammar64`.
Значимость - парный перестановочный тест по пользователям против `human` и между K, с поправкой Холма.
""",
    "seeds": """
# Yambda-50M: устойчивость выученных признаков к сиду

Проверка главного результата `discovery`: обходит ли `grammar32` ручные признаки не только на одном сиде.
Для каждого из 5 сидов заново обучаются слой грамматики и CatBoost, у всех наборов с одним и тем же сидом:
- `human` - общая часть и ручные признаки по истории;
- `grammar32` - общая часть и 32 выученных признака (алфавит `rich`);
- `human+grammar16` - гибрид;
- `grammar_nn32` - слой с MLP-головой без бустинга.

Считаются парные разницы с `human` того же сида, их среднее по сидам с bootstrap-интервалом,
и стабильность признаков между сидами: средняя максимальная корреляция значений и совпадение пар «связь x ядро».
""",
}

COMMON_INTRO = """
Постановка A: объект - прослушивание, которое включил рекомендатель (`is_organic = 0`), метка - дослушал ли пользователь трек (`played_ratio_pct >= 50`).
Признаки считаются на момент конца предыдущего прослушивания пользователя, только по строго предыдущим событиям.
Разбиение: train 28 дней, val 7 дней, test 7 дней; финальные модели переобучаются на train + val, test оценивается один раз.

Ноутбук сгенерирован `kaggle/build_notebook.py` из модуля `rank/` репозитория, код записывается ячейками `%%writefile`.
Артефакты сохраняются в `/kaggle/working/outputs`.
Если на входе есть сохранённые признаки ноутбука `yambda-features` с тем же хешем кода, шаги 1-3 берут их оттуда.
"""


def build(stage):
    spec = STAGES[stage]
    cells = []

    def md(text):
        cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))

    def code(text):
        cells.append(nbf.v4.new_code_cell(text.strip("\n")))

    md(INTRO[stage] + COMMON_INTRO)
    code("!pip install -q polars==1.38.1")
    code("""
import os

os.environ["_RJEM_MALLOC_CONF"] = "background_thread:true,dirty_decay_ms:500,muzzy_decay_ms:500"
os.environ["POLARS_MAX_THREADS"] = "4"

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

CODE = Path("/kaggle/working/code")
OUT = Path("/kaggle/working/outputs")
WORK = Path("/tmp/work")
for p in [CODE / "rank", OUT, WORK]:
    p.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(CODE))

events_path = next(Path("/kaggle/input").rglob("multi_event.parquet"))
mappings_dir = next(Path("/kaggle/input").rglob("artist_item_mapping.parquet")).parent
print(f"events: {events_path}")
GPU_INFO = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True).stdout.strip() if shutil.which("nvidia-smi") else "none"
print(GPU_INFO)
""")
    for name in MODULES:
        code(f"%%writefile /kaggle/working/code/rank/{name}\n{(ROOT / 'rank' / name).read_text()}")
    code(f"""
import catboost
import polars as pl
import torch
from catboost.utils import get_gpu_device_count

from rank.features import build_features, code_hash, dataset_end, find_cached, history_prior
from rank.leakage import check_leakage
from rank.prepare import prepare_listens

TASK_TYPE = "GPU" if get_gpu_device_count() > 0 else "CPU"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
FEATURE_KWARGS = {spec["feature_kwargs"]}
STAGE = "{stage}"
FEATURES_OUT = Path("/kaggle/working/features") if STAGE == "features" else WORK / "features"
FEATURES = None if STAGE == "features" else find_cached("/kaggle/input", **FEATURE_KWARGS)
print(f"feature code hash {{code_hash()}}, cached features: {{FEATURES}}")
pl.Config.set_tbl_rows(60)
pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_width_chars(200)
print(f"polars {{pl.__version__}}, catboost {{catboost.__version__}}, torch {{torch.__version__}}, task type {{TASK_TYPE}}, device {{DEVICE}}")
timings = {{}}
""")
    md("## 1. Подготовка прослушиваний")
    code("""
if FEATURES is None:
    started = time.time()
    prepare_listens(events_path, mappings_dir, WORK / "listens")
    timings["prepare_s"] = round(time.time() - started, 1)
    t_end = dataset_end(events_path)
    prior = history_prior(pl.scan_parquet(str(WORK / "listens" / "part_*.parquet")), t_end)
    print(f"t_end {t_end}, prior {prior:.4f}")
else:
    print(f"using cached features from {FEATURES}")
""")
    md("""
## 2. Проверка утечек

Для первой тысячи пользователей признаки считаются по полным данным и по данным, обрезанным в середине валидации; для объектов за сутки до обрезки все признаки должны совпасть.
Канарейка `canary_next_ratio` смотрит в будущее, и тест обязан её поймать.
""")
    code("""
if FEATURES is None:
    started = time.time()
    leak = check_leakage(WORK / "listens", events_path, mappings_dir, WORK / "leakage", t_end, prior, max_parts=1, **FEATURE_KWARGS)
    timings["leakage_check_s"] = round(time.time() - started, 1)
else:
    leak = json.loads((FEATURES / "leakage_report.json").read_text())
(OUT / "leakage_report.json").write_text(json.dumps(leak, indent=2))
print(json.dumps({k: v for k, v in leak.items() if k != "single_feature_auc_top10"}, indent=2))
assert leak["passed"], "leakage check failed"
""")
    md("## 3. Признаки")
    code("""
if FEATURES is None:
    started = time.time()
    meta = build_features(WORK / "listens", events_path, mappings_dir, FEATURES_OUT, t_end=t_end, prior=prior, **FEATURE_KWARGS)
    timings["features_s"] = round(time.time() - started, 1)
    (FEATURES_OUT / "leakage_report.json").write_text(json.dumps(leak, indent=2))
    FEATURES = FEATURES_OUT
else:
    meta = json.loads((FEATURES / "meta.json").read_text())
(OUT / "features_meta.json").write_text(json.dumps(meta, indent=2))
print({g: len(c) for g, c in meta["groups"].items()})
""")
    if stage != "features":
        md("## 4. Эксперименты")
        {"ladder": stage_cells_ladder, "discovery": stage_cells_discovery, "seeds": stage_cells_seeds,
         "ablation": stage_cells_ablation, "prune": lambda c: stage_cells_prune(c, spec["run_kwargs"]),
         "sparse": stage_cells_sparse, "scale": stage_cells_scale}[stage](code)
    code("""
run_info = {
    "timings": timings,
    "feature_code_hash": code_hash(),
    "cached_features": str(FEATURES) if STAGE != "features" else None,
    "records": globals().get("summary", {}).get("records", {}),
    "task_type": TASK_TYPE,
    "polars": pl.__version__,
    "catboost": catboost.__version__,
    "torch": torch.__version__,
    "gpu": GPU_INFO,
}
(OUT / "run_info.json").write_text(json.dumps(run_info, indent=2))
print(json.dumps(run_info, indent=2))
""")
    return spec, cells


def print_metrics_cell(code):
    code("""
cols = ["model", "slice", "n", "logloss", "auc", "gauc", "ndcg@10"]
print("validation")
print(pl.read_csv(OUT / "val_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("test")
print(pl.read_csv(OUT / "test_metrics.csv").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("paired test deltas vs reference (mean, 95% interval)")
for name, d in summary["test_paired_deltas"].items():
    print(name, {m: (round(v["mean"], 4), round(v["lo"], 4), round(v["hi"], 4)) for m, v in d.items()})
""")


def stage_cells_ladder(code):
    code("""
from rank.experiments import run_experiments

started = time.time()
summary = run_experiments(FEATURES, OUT, task_type=TASK_TYPE, iterations=3000, n_boot=100, with_ablation=True)
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    print_metrics_cell(code)
    code("""
print(pl.read_csv(OUT / "ablation_val.csv").filter(pl.col("slice") == "all").select(
    "dropped_group", "n_dropped", "delta_auc", "delta_gauc", "delta_logloss", "best_iter"
).with_columns(pl.col(pl.Float64).round(4)))
tau = pl.read_csv(OUT / "tau_importance.csv")
print(tau.group_by("relation", "scale").agg(pl.col("importance").sum()).pivot(on="scale", index="relation", values="importance").fill_null(0))
""")


def stage_cells_discovery(code):
    code("""
from rank.discovery import run_discovery

started = time.time()
summary = run_discovery(FEATURES, OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000, n_boot=100, alphabet="rich")
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    print_metrics_cell(code)
    code("""
for k in [8, 16, 32]:
    print((OUT / "grammar" / f"features_k{k}.md").read_text())
print("brute force top-16:", summary["brute_ranking_top32"][:16])
print(json.dumps(summary["timings"], indent=2))
""")
    stat_tests_cell(code)


def stat_tests_cell(code):
    code("""
print("paired sign-flip tests by users, alpha 0.05, power 0.8, Holm correction")
print(pl.read_csv(OUT / "stat_tests.csv").select(
    "comparison", "metric", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "power_at_delta", "reject_h0"
).with_columns(pl.col(pl.Float64).round(5)))
""")


def stage_cells_ablation(code):
    code("""
from rank.ablation import run_ablation

started = time.time()
summary = run_ablation(FEATURES, OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000)
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    code("""
cols = ["model", "logloss", "auc", "gauc", "ndcg@10"]
print(pl.read_csv(OUT / "test_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("channel effects, mean over seeds")
print(pl.read_csv(OUT / "channel_effects.csv").with_columns(pl.col(pl.Float64).round(5)))
for name in ["stat_tests_vs_rich", "stat_tests_vs_human"]:
    print(name)
    print(pl.read_csv(OUT / f"{name}.csv").filter(pl.col("metric") == "gauc").select(
        "comparison", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "reject_h0"
    ).with_columns(pl.col(pl.Float64).round(5)))
""")


def stage_cells_prune(code, run_kwargs):
    code(f"""
from rank.prune import run_prune

started = time.time()
summary = run_prune(FEATURES, "/kaggle/input", OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000, {run_kwargs})
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    code("""
cols = ["model", "logloss", "auc", "gauc", "ndcg@10"]
print(pl.read_csv(OUT / "test_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("cells used:", summary["cells_count"])
for name in ["stat_tests_vs_dense", "stat_tests_vs_human"]:
    print(name)
    print(pl.read_csv(OUT / f"{name}.csv").select(
        "comparison", "metric", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "reject_h0"
    ).with_columns(pl.col(pl.Float64).round(5)))
""")


def stage_cells_sparse(code):
    code("""
from rank.sparse import run_sparse

started = time.time()
summary = run_sparse(FEATURES, OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000)
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    code("""
cols = ["model", "logloss", "auc", "gauc", "ndcg@10"]
print(pl.read_csv(OUT / "test_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("cells used:", summary["cells_count"])
for name in ["stat_tests_vs_dense", "stat_tests_vs_human"]:
    print(name)
    print(pl.read_csv(OUT / f"{name}.csv").select(
        "comparison", "metric", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "reject_h0"
    ).with_columns(pl.col(pl.Float64).round(5)))
""")


def stage_cells_scale(code):
    code("""
from rank.scale import run_scale

started = time.time()
summary = run_scale(FEATURES, OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000)
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    code("""
cols = ["model", "logloss", "auc", "gauc", "ndcg@10"]
print(pl.read_csv(OUT / "test_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
for name in ["stat_tests_vs_human", "stat_tests_k", "stat_tests_hybrid_k"]:
    print(name)
    print(pl.read_csv(OUT / f"{name}.csv").select(
        "comparison", "metric", "delta", "ci_lo", "ci_hi", "p_perm", "p_holm", "mde", "reject_h0"
    ).with_columns(pl.col(pl.Float64).round(5)))
""")


def stage_cells_seeds(code):
    code("""
from rank.seeds import run_seeds

started = time.time()
summary = run_seeds(FEATURES, OUT, task_type=TASK_TYPE, device=DEVICE, iterations=3000, n_boot=100, alphabet="rich")
timings["train_eval_s"] = round(time.time() - started, 1)
""")
    code("""
cols = ["model", "logloss", "auc", "gauc", "ndcg@10"]
print(pl.read_csv(OUT / "test_metrics.csv").filter(pl.col("slice") == "all").select(cols).with_columns(pl.col(pl.Float64).round(4)))
print("seed-averaged test deltas vs human (mean, 95% interval)")
for name, d in summary["test_seed_mean_deltas"].items():
    print(name, {m: (round(v["mean"], 4), round(v["lo"], 4), round(v["hi"], 4)) for m, v in d.items()})
print("gauc wins over seeds:", summary["gauc_wins_vs_reference"])
print("stability:", summary["stability_mean"])
print(pl.read_csv(OUT / "stability.csv"))
""")
    stat_tests_cell(code)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=list(STAGES))
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    spec, cells = build(args.stage)
    out_dir = KERNELS_DIR / args.stage
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, out_dir / spec["notebook"])
    metadata = {
        "id": spec["id"],
        "title": spec["id"].split("/")[1],
        "code_file": spec["notebook"],
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": spec.get("gpu", True),
        "enable_internet": True,
        "dataset_sources": ["rabochi1024/yambda-50m-flat"],
        "competition_sources": [],
        "kernel_sources": ([] if args.stage == "features" or args.no_cache else [FEATURES_KERNEL]) + spec.get("sources", []),
    }
    if spec.get("gpu", True):
        metadata["machine_shape"] = "NvidiaTeslaT4"
    (out_dir / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"written {len(cells)} cells -> {out_dir / spec['notebook']}")


if __name__ == "__main__":
    main()
