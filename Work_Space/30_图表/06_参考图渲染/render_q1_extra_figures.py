# -*- coding: utf-8 -*-
"""
A 题 · 问题1 创新项参考图渲染（F-41 ～ F-43）
================================================================
本脚本位于【工作区】30_图表/06_参考图渲染/，**不属于交接包**——
按分工，最终绘图由写作者按规格卡执行；本脚本只生成「参考图」供对照。

读取 交接包/04_图表包/data/ 下的 Q1 创新项数据，输出至
      交接包/04_图表包/figures_reference/（300 DPI PNG ＋ PDF）

设计语言（见 04-2_项目图表设计语言.md）：
  主色 #1F3A93 ｜ #F39C12 ｜ #27AE60 ｜ #C0392B ｜ 参考线 #9E9E9E ｜ 文字 #333333

数据纪律：**只读** data/*.csv，不重算、不改数；缺列时降级而非编造。

三条硬纪律（本轮据规格卡与《A_数值口径总表》§8.6 落实）：
  · F-41：**必须** `step(where='post')` ＋ 对数纵轴；注明数据已抽稀；
  · F-42：区间＝**严格样本极差（n=40）**，**不得**与网格离散误差带相加、**不得**写分位；
  · F-43：Q1 的 **Sobol $S_1$ 越界** ⟹ 按 §8.6「T2-3 的 Sobol 数值不得引用」，
          故只用 **Morris $\\mu^*$／$\\sigma$** 与 OAT 并置，不画 Sobol 数值。
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BLUE, GOLD, GREEN, RED = "#1F3A93", "#F39C12", "#27AE60", "#C0392B"
GRAY, INK, GRID = "#9E9E9E", "#333333", "#E0E0E0"

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "font.size": 8, "axes.titlesize": 10, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.4,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", "..", "20_交付包", "04_图表包"))
DATA = os.path.join(PKG, "data")
OUT = os.path.join(PKG, "figures_reference")
os.makedirs(OUT, exist_ok=True)
CM = 1 / 2.54


def save(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{stem}.{ext}"))
    plt.close(fig)
    print("  [OK]", stem, flush=True)


def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def rd(name, nskip=0):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        for _ in range(nskip):
            f.readline()
        return list(csv.DictReader(f))


def fnum(x, default=float("nan")):
    try:
        s = str(x).strip()
        return float(s) if s != "" else default
    except Exception:
        return default


# ==================================================================
# F-41 误差驱动自适应步长的步长轨迹（阶梯图，对数纵轴）
# ==================================================================
def f41():
    rows = rd("fig_q1_stepsize.csv")
    t = np.array([fnum(r["t_s"]) for r in rows])
    h = np.array([fnum(r["h_next_s"]) for r in rows])
    o = np.argsort(t)
    t, h = t[o], h[o]

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.step(t, h, where="post", color=BLUE, lw=1.0)
    ax.set_yscale("log")
    ax.set_xlim(0, 1800)
    ax.set_ylim(5e-4, 2.2)
    ax.set_yticks([1.0, 0.1, 0.01, 0.001])
    ax.set_yticklabels(["1", "0.1", "0.01", "0.001"])
    ax.yaxis.set_minor_locator(mticker.NullLocator())

    ax.axhline(1 / 32.0, color=GRAY, ls="--", lw=1.0)
    ax.text(1250, 1 / 32.0 * 1.30, "稳定段 $h\\approx1/32$ s", color=GRAY, fontsize=7.5)
    ax.annotate("初始急剧细化段", xy=(2.0, 0.02), xytext=(260, 2.4e-3),
                fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("步长 $h$ / s（对数轴）")
    ax.set_title("Q1 误差驱动自适应步长的步长轨迹")
    ax.text(0.985, 0.035, "数据已抽稀：257403 → 4964 行（阶梯形态不变）",
            transform=ax.transAxes, ha="right", fontsize=6.3, color=GRAY)
    despine(ax)
    save(fig, "F-41_自适应步长轨迹")


# ==================================================================
# F-42 边界不确定度 → 关键输出的散布区间（区间标尺图，双联）
# ==================================================================
_LBL = {"T0": "$T(0)$", "TR": "$T(R)$", "C0": "$C(0)$", "CR": "$C(R)$"}


def f42():
    rows = rd("fig_q1_uq.csv", nskip=4)
    q = {r["quantity"]: r for r in rows if r.get("quantity")}

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16 * CM, 6 * CM),
                                 gridspec_kw=dict(wspace=0.32))

    def band(ax, keys, color, unit, note):
        for i, k in enumerate(keys):
            r = q[k]
            lo, hi, base = fnum(r["lo"]), fnum(r["hi"]), fnum(r["base"])
            y = len(keys) - 1 - i
            ax.plot([lo, hi], [y, y], color=color, lw=8, alpha=0.25,
                    solid_capstyle="butt")
            ax.plot([base], [y], marker="o", ms=5.5, color=color, zorder=3)
            pad = max(hi - lo, abs(base) * 1e-4)
            ax.text(hi + pad * 0.8, y, "基准 %.6f" % base, fontsize=6.8, color=color)
        ax.set_yticks(range(len(keys)))
        ax.set_yticklabels([_LBL[k] for k in reversed(keys)])
        ax.set_ylim(-0.6, len(keys) - 0.25)
        ax.set_xlabel(unit)
        lo0 = min(fnum(q[k]["lo"]) for k in keys)
        hi0 = max(fnum(q[k]["hi"]) for k in keys)
        xp = (hi0 - lo0) * 0.45 + abs(hi0) * 1e-4
        ax.set_xlim(lo0 - xp * 0.15, hi0 + xp)
        ax.text(0.02, 0.03, note, transform=ax.transAxes, fontsize=6.3, color=GRAY)

    band(a1, ["T0", "TR"], BLUE, "温度 / ℃",
         "区间＝严格样本极差（$n=40$ 解样本）；与网格离散误差带分列、不相加")
    a1.set_title("(a) 温度")
    band(a2, ["C0", "CR"], GREEN, "水分浓度 / (kg/kg)",
         "$C(0)$ 区间宽度 $<10^{-8}$，图上不可见（非零即基准点）")
    a2.set_title("(b) 水分浓度")
    for a in (a1, a2):
        despine(a)
    a1.plot([], [], color=BLUE, lw=8, alpha=0.25, label="严格样本区间")
    a1.plot([], [], marker="o", ls="", color=BLUE, label="正式交付值（基准）")
    a1.legend(frameon=False, loc="lower right")
    save(fig, "F-42_边界不确定度散布区间")


# ==================================================================
# F-43 全局灵敏度（Morris）与 OAT 并置（双联）
# ==================================================================
def f43():
    gs = rd("fig_q1_gs.csv")
    ot = rd("fig_tornado_data.csv")
    out = "CR"
    pmap = [("h", "h"), ("km", "km"), ("D0", "D0"),
            ("Tinf_off", "$T_\\infty$"), ("Cinf_off", "$C_\\infty$")]
    mus = {r["param"]: fnum(r["mu_star"]) for r in gs if r["output"] == out}
    sig = {r["param"]: fnum(r["sigma"]) for r in gs if r["output"] == out}
    osn = {r["parameter"]: abs(fnum(r["S_norm"]))
           for r in ot if r["output"] == "C_surface"}

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16 * CM, 6 * CM),
                                 gridspec_kw=dict(wspace=0.30))

    for p, lbl in pmap:
        a1.errorbar(mus[p], sig[p], marker="o", ms=5.5, color=BLUE, lw=0)
        a1.annotate(lbl, (mus[p], sig[p]), textcoords="offset points",
                    xytext=(5, 3), fontsize=7.5, color=INK)
    a1.set_xlabel("Morris $\\mu^*$（绝对效应）")
    a1.set_ylabel("Morris $\\sigma$")
    a1.set_title("(a) 全局灵敏度（Morris，$C(R)$）")
    a1.set_xlim(-0.02, max(mus.values()) * 1.25 + 1e-3)
    a1.set_ylim(-0.005, max(sig.values()) * 1.45 + 1e-3)
    despine(a1)

    common = ["h", "km", "D0"]
    m = np.array([abs(mus[c]) for c in common], dtype=float)
    oo = np.array([osn.get(c, np.nan) for c in common], dtype=float)
    if np.nanmax(m) > 0:
        m = m / np.nanmax(m)
    if np.nanmax(oo) > 0:
        oo = oo / np.nanmax(oo)
    x = np.arange(len(common))
    a2.bar(x - 0.19, m, 0.36, color=BLUE, label="Morris $\\mu^*$（归一）")
    a2.bar(x + 0.19, oo, 0.36, color=GOLD, label="OAT $|S_{\\rm norm}|$（归一）")
    a2.set_xticks(x)
    a2.set_xticklabels(common)
    a2.set_ylim(0, 1.30)
    a2.set_ylabel("归一化灵敏度")
    a2.set_title("(b) 全局 vs 单因素（公共参数）")
    a2.legend(frameon=False, loc="upper right")
    a2.text(0.02, 0.04,
            "Sobol $S_1$ 越界 → 按《口径总表》§8.6 不引用其数值\n"
            "仅 Morris 侧含 $T_\\infty/C_\\infty$；OAT 侧含 $T_0/C_0$（未列入公共轴）",
            transform=a2.transAxes, fontsize=6.3, color=RED)
    despine(a2)
    save(fig, "F-43_全局灵敏度与OAT并置")


if __name__ == "__main__":
    for fn in (f41, f42, f43):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            print("  [FAIL]", fn.__name__, repr(exc), flush=True)
