import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from rank.basis import ALPHABETS, RELATIONS

OUT = ROOT / "docs" / "figures"
RUNS = ROOT / "outputs"
SURFACE = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e4e3df"
OURS = "#2a78d6"
BRUTE = "#eb6834"
HYBRID = "#1baf7a"
HUMAN = "#52514e"
RAMP = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
RELATION_NAMES = {"u": "любой трек", "ui": "тот же трек", "ua": "тот же артист", "ual": "тот же альбом", "cf": "CF-похожие"}
KERNEL_NAMES = {
    "r1": "посл. 1", "r3": "посл. 3", "r10": "посл. 10", "sess": "сессия", "t1h": "1ч", "t6h": "6ч", "t1d": "1д",
    "t3d": "3д", "t7d": "7д", "t30d": "30д", "t90d": "90д", "all": "всё", "x1d": "давн. 1д", "x30d": "давн. 30д",
}


def style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2, "xtick.color": TEXT_2, "ytick.color": TEXT_2,
        "text.color": TEXT, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "font.size": 11, "axes.titlesize": 13,
        "axes.titleweight": "bold", "axes.titlelocation": "left", "legend.frameon": False,
    })


def mean_metric(path, model_prefix, metric="gauc"):
    t = pl.read_csv(path).filter(pl.col("slice") == "all")
    t = t.filter(pl.col("model").str.replace(r"_s\d+$", "") == model_prefix)
    return float(t[metric].mean())


def stat_row(path, comparison, metric="gauc"):
    t = pl.read_csv(path).filter((pl.col("comparison") == comparison) & (pl.col("metric") == metric))
    return t.row(0, named=True)


def fig_search():
    path = RUNS / "kaggle_discovery_rich" / "outputs" / "test_metrics.csv"
    get = lambda m: mean_metric(path, m)
    ks = [8, 16, 32]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(ks, [get(f"brute_top{k}") for k in ks], color=BRUTE, lw=2, marker="o", ms=8, label="перебор: top-K по важности CatBoost")
    grammar = [get(f"grammar{k}") for k in ks] + [mean_metric(RUNS / "kaggle_scale" / "outputs" / "test_metrics.csv", "grammar64")]
    ax.plot(ks + [64], grammar, color=OURS, lw=2, marker="o", ms=8, label="градиент: обучаемая грамматика")
    ax.scatter([822], [get("brute_all")], color=BRUTE, marker="s", s=70, zorder=3)
    ax.annotate("перебор: все 822\nкандидата", (822, get("brute_all")), xytext=(-8, -34), textcoords="offset points",
                ha="right", color=TEXT_2, fontsize=10)
    ax.scatter([64], [get("human")], color=HUMAN, marker="D", s=70, zorder=3)
    ax.annotate("ручные признаки, 64", (64, get("human")), xytext=(10, -18), textcoords="offset points", color=TEXT_2, fontsize=10)
    ax.annotate(f"16 случайных: {get('random16'):.3f} (ниже оси)", (16, 0.7315), color=TEXT_2, fontsize=10, ha="center")
    ax.set_xscale("log")
    ax.set_xticks([8, 16, 32, 64, 822])
    ax.set_xticklabels(["8", "16", "32", "64", "822"])
    ax.set_ylim(0.73, 0.761)
    ax.set_xlabel("число признаков по истории (лог. шкала)")
    ax.set_ylabel("test GAUC")
    ax.set_title("При любом бюджете градиент находит признаки лучше перебора")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "search.png", dpi=150)
    plt.close(fig)


def fig_deltas():
    rows = [
        ("grammar32, 32 выученных", RUNS / "kaggle_seeds_v2" / "outputs" / "stat_tests.csv", "grammar32_vs_human", OURS, "5 сидов"),
        ("grammar64, 64 выученных", RUNS / "kaggle_scale" / "outputs" / "stat_tests_vs_human.csv", "grammar64_vs_human", OURS, "3 сида"),
        ("ручные + 32 выученных", RUNS / "kaggle_scale" / "outputs" / "stat_tests_vs_human.csv", "human+grammar32_vs_human", HYBRID, "3 сида"),
        ("ручные + 64 выученных", RUNS / "kaggle_scale" / "outputs" / "stat_tests_vs_human.csv", "human+grammar64_vs_human", HYBRID, "3 сида"),
        ("«читаемые» 32 (ровно как словами)", RUNS / "kaggle_prune" / "outputs" / "stat_tests_vs_human.csv", "g32_readable_vs_human", TEXT_2, "2 сида"),
        ("слой без бустинга", RUNS / "kaggle_seeds_v2" / "outputs" / "stat_tests.csv", "grammar_nn32_vs_human", TEXT_2, "5 сидов"),
    ]
    fig, ax = plt.subplots(figsize=(10, 4.4))
    for i, (name, path, comp, color, seeds) in enumerate(rows):
        r = stat_row(path, comp)
        y = len(rows) - 1 - i
        ax.plot([r["ci_lo"], r["ci_hi"]], [y, y], color=color, lw=2.5, solid_capstyle="round")
        ax.scatter([r["delta"]], [y], color=color, s=64, zorder=3, edgecolor=SURFACE, linewidth=2)
        p = r["p_holm"]
        sig = f"p_holm {p:.0e}" if p < 0.01 else f"p_holm {p:.2f}"
        ax.annotate(f"{r['delta']:+.4f}  ({sig}, {seeds})", (r["ci_hi"], y), xytext=(8, -4), textcoords="offset points",
                    color=TEXT_2, fontsize=9.5)
    ax.axvline(0, color=HUMAN, lw=1.2, ls="--")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows][::-1])
    ax.set_xlim(-0.0055, 0.0115)
    ax.set_xticks([-0.004, -0.002, 0, 0.002, 0.004, 0.006])
    ax.set_xlabel("разница test GAUC с ручными признаками, 95% интервал")
    ax.set_title("Разница с ручными признаками")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(OUT / "deltas.png", dpi=150)
    plt.close(fig)


def fig_ablation():
    path = RUNS / "kaggle_ablation" / "outputs"
    effects = pl.read_csv(path / "channel_effects.csv").filter(pl.col("metric") == "gauc")
    names = {"ratio": "доля прослушанного", "novel": "события новых артистов", "sess": "текущая сессия", "recency": "давность события"}
    channels = ["ratio", "sess", "recency", "novel"]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
    for ax, column, title, color in [
        (axes[0], "add_to_base", "добавить к старому алфавиту", OURS),
        (axes[1], "drop_from_rich", "убрать из полного алфавита", BRUTE),
    ]:
        values = [effects.filter(pl.col("channel") == c)[column].item() for c in channels]
        ys = np.arange(len(channels))[::-1]
        ax.barh(ys, values, color=color, height=0.55)
        for y, v in zip(ys, values):
            ax.annotate(f"{v:+.4f}", (v, y), xytext=(4 if v >= 0 else -4, 0), textcoords="offset points",
                        ha="left" if v >= 0 else "right", va="center", fontsize=9.5, color=TEXT_2)
        ax.axvline(0, color=TEXT_2, lw=1)
        ax.set_title(title, fontsize=11, fontweight="normal")
        ax.set_yticks(ys)
        ax.set_yticklabels([names[c] for c in channels])
        ax.grid(axis="y", visible=False)
        lim = 0.026
        ax.set_xlim(-lim if column == "drop_from_rich" else -0.004, 0.006 if column == "drop_from_rich" else lim)
        ax.set_xticks([-0.02, -0.01, 0] if column == "drop_from_rich" else [0, 0.01, 0.02])
        ax.set_xlabel("изменение test GAUC")
    fig.suptitle("Весь прирост алфавита даёт один канал: доля прослушанного", x=0.02, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "ablation.png", dpi=150)
    plt.close(fig)


def fig_memory():
    path = RUNS / "kaggle_prune" / "outputs" / "test_metrics.csv"
    state = json.loads((RUNS / "cost" / "cost_report.json").read_text())["state_numbers_per_user"]
    variants = [("dense", "плотный, 490 ячеек"), ("t0.001", "обрезка 0.001, 162"), ("t0.01", "обрезка 0.01, 145"),
                ("t0.05", "обрезка 0.05, 132"), ("readable", "как словами, 95")]
    xs = [state[f"grammar32_{v}"]["mean"] / 1000 for v, _ in variants]
    ys = [mean_metric(path, f"g32_{v}") for v, _ in variants]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(xs, ys, color=OURS, lw=2, marker="o", ms=8)
    offsets = {"dense": (-8, 8, "right"), "t0.001": (-8, 8, "right"), "t0.01": (-8, 6, "right"), "t0.05": (8, -4, "left"),
               "readable": (8, -4, "left")}
    for (v, label), x, y in zip(variants, xs, ys):
        dx, dy, ha = offsets[v]
        ax.annotate(f"grammar32, {label}", (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=9.5, color=TEXT_2, ha=ha)
    hx, hy = state["human_estimate"]["mean"] / 1000, mean_metric(path, "human")
    ax.scatter([hx], [hy], color=HUMAN, marker="D", s=70, zorder=3)
    ax.annotate("ручные признаки", (hx, hy), xytext=(0, 10), textcoords="offset points", fontsize=9.5, color=TEXT_2, ha="center")
    ax.set_xscale("log")
    ticks = [20, 50, 100, 200, 500]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.minorticks_off()
    ax.set_xlim(14, 700)
    ax.set_ylim(0.7540, 0.7578)
    ax.set_xlabel("чисел состояния на пользователя, тыс. (оценка, лог. шкала)")
    ax.set_ylabel("test GAUC")
    ax.set_title("Качество против памяти на пользователя")
    fig.tight_layout()
    fig.savefig(OUT / "memory.png", dpi=150)
    plt.close(fig)


def fig_feature_map():
    grammar_dir = RUNS / "kaggle_seeds_v2" / "outputs" / "grammar"
    alphabet = ALPHABETS["rich"]
    counts = Counter()
    files = sorted(grammar_dir.glob("features_k32_s*.json"))
    for path in files:
        for row in json.loads(path.read_text()):
            rel = max(row["relation"], key=row["relation"].get)
            ker = max(row["kernel"], key=row["kernel"].get)
            counts[(rel, ker)] += 1
    grid = np.array([[counts[(r, k)] for k in alphabet.kernels] for r in RELATIONS], dtype=float)
    fig, ax = plt.subplots(figsize=(11, 3.8))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("blue", RAMP)
    ax.imshow(grid, cmap=cmap, aspect="auto", vmin=0)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j]:
                ax.text(j, i, int(grid[i, j]), ha="center", va="center", fontsize=9.5,
                        color=SURFACE if grid[i, j] > grid.max() * 0.55 else TEXT)
    ax.set_xticks(range(len(alphabet.kernels)))
    ax.set_xticklabels([KERNEL_NAMES[k] for k in alphabet.kernels], rotation=30, ha="right", fontsize=9)
    ax.set_yticks(range(len(RELATIONS)))
    ax.set_yticklabels([RELATION_NAMES[r] for r in RELATIONS])
    ax.set_xticks(np.arange(-0.5, len(alphabet.kernels)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(RELATIONS)), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.grid(which="major", visible=False)
    ax.tick_params(which="minor", length=0)
    ax.set_title(f"Связь и ядро у {len(files) * 32} выученных признаков ({len(files)} сидов)")
    fig.tight_layout()
    fig.savefig(OUT / "feature_map.png", dpi=150)
    plt.close(fig)


def fig_scheme():
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.6)
    ax.axis("off")
    boxes = [
        (0.1, "История пользователя", "прослушивания, скипы,\nлайки, сессии", GRID, TEXT),
        (2.55, "Базис: 490 чисел", "5 связей × 7 событий\n× 14 ядер, считается\nодин раз", "#cde2fb", TEXT),
        (5.0, "Обучаемый слой", "softmax по связям и ядрам,\nкраны событий,\n1056 параметров", OURS, SURFACE),
        (7.45, "32 признака-фразы", "«доля дослушиваний\nэтого трека\nза месяц»", "#cde2fb", TEXT),
        (9.9, "CatBoost", "финальная модель,\nнейросеть больше\nне нужна", GRID, TEXT),
    ]
    width, height, y = 2.0, 1.9, 1.15
    for x, title, body, face, ink in boxes:
        ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    facecolor=face, edgecolor=face, linewidth=0))
        ax.text(x + width / 2, y + height - 0.38, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color=ink)
        ax.text(x + width / 2, y + 0.72, body, ha="center", va="center", fontsize=9.5, color=ink, linespacing=1.35)
    for (x0, *_), (x1, *_) in zip(boxes, boxes[1:]):
        ax.add_patch(FancyArrowPatch((x0 + width + 0.05, y + height / 2), (x1 - 0.05, y + height / 2),
                                     arrowstyle="-|>", mutation_scale=16, color=TEXT_2, linewidth=1.6))
    loop = FancyArrowPatch((5.35, y), (6.65, y), connectionstyle="arc3,rad=0.9", arrowstyle="-|>",
                           mutation_scale=14, color=OURS, linewidth=1.6)
    ax.add_patch(loop)
    ax.text(6.0, 0.18, "обучение: маленькая нейросеть предсказывает метку, градиент logloss меняет веса выбора",
            ha="center", va="center", fontsize=9.5, color=TEXT_2)
    fig.tight_layout()
    fig.savefig(OUT / "scheme.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    fig_scheme()
    fig_search()
    fig_deltas()
    fig_ablation()
    fig_memory()
    fig_feature_map()
    print(f"figures -> {OUT}")


if __name__ == "__main__":
    main()
