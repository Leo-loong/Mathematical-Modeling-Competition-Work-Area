# -*- coding: utf-8 -*-
"""
A 题 · 图表渲染脚本（交付包 04_图表包 内自包含运行）
================================================================
用途：读取本包 data/*.csv，按《04-2_项目图表设计语言.md》与各规格卡渲染图件，
      输出至 figures_reference/（300 DPI PNG ＋ PDF 矢量）。

运行：python render_figures.py          （在 04_图表包 目录下）
依赖：numpy / matplotlib（版本见 09_代码与复现/requirements.txt）

设计语言锁定（不得擅自更改）：
  主色 #1F3A93（温度中心）｜对比 #F39C12（温度表面）｜第三 #27AE60（含水率中心）｜第四 #C0392B（含水率表面/强调）
  参考线 #9E9E9E 虚线 1.0pt｜轴线文字 #333333｜网格 #E0E0E0 仅横向（可省）
  场量色阶 viridis｜中文字体 微软雅黑｜西文 Arial｜导出 300 DPI PNG + PDF
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

# ---------- 全局样式 ----------
BLUE, GOLD, GREEN, RED = "#1F3A93", "#F39C12", "#27AE60", "#C0392B"
GRAY, INK, GRID = "#9E9E9E", "#333333", "#E0E0E0"

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "font.size": 8,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.4,
    "axes.grid.axis": "y",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# 本脚本位于【工作区】30_图表/06_参考图渲染/，**不属于交接包**——按分工，最终绘图由写作者执行。
# 用途：读取交接包内的图表数据，渲染「参考图」供写作者直观对照，输出写回交接包 figures_reference/。
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, "..", "..", "20_交付包", "04_图表包"))
DATA = os.path.join(PKG, "data")
OUT = os.path.join(PKG, "figures_reference")
os.makedirs(OUT, exist_ok=True)

CM = 1 / 2.54  # cm -> inch


def load(name, **kw):
    return np.genfromtxt(os.path.join(DATA, name), delimiter=",", names=True,
                         dtype=float, encoding="utf-8", **kw)


def save(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{stem}.{ext}"))
    plt.close(fig)
    print("  [OK]", stem)


def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _tick(ax):
    """对数横轴统一刻度：去掉 minor 刻度标签，避免重叠。"""
    ax.set_xticks([0.125, 0.25, 0.5, 1.0])
    ax.set_xticklabels(["0.125", "0.25", "0.5", "1"])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlim(0.1, 1.3)


# ==================================================================
# F-03 烘房环境时序（双纵轴折线）
# ==================================================================
def f03():
    d = load("fig_env_timeseries.csv")
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    l1, = ax.plot(d["t_s"], d["T_env_C"], color=GOLD, lw=1.6, label="烘房温度")
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("烘房温度 / ℃", color=GOLD)
    ax.tick_params(axis="y", colors=GOLD)
    ax.set_ylim(28, 51)

    ax2 = ax.twinx()
    l2, = ax2.plot(d["t_s"], d["C_env_kgkg"], color=GREEN, lw=1.4, ls="--",
                   label="烘房水分浓度")
    ax2.set_ylabel("烘房水分浓度 / (kg/kg)", color=GREEN)
    ax2.tick_params(axis="y", colors=GREEN)
    ax2.set_ylim(0.019, 0.051)
    ax2.grid(False)
    despine(ax2)

    # 阶段分界（升温趋稳 -> 平台，约 8e3 s）
    ax.axvline(8160, color=GRAY, ls=":", lw=1.0)
    ax.text(8300, 29.2, "进入平台段", color=GRAY, fontsize=7.5)
    ax.annotate("升温段\n（Q1 窗口 0–1800 s 全在此段内）",
                xy=(900, 45), xytext=(1500, 33.5), fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

    ax.legend(handles=[l1, l2], loc="lower right", frameon=False)
    ax.set_title("烘房环境条件时序")
    save(fig, "F-03_烘房环境时序")


# ==================================================================
# F-06 网格与时间收敛（双联：值-步长 ＋ 相邻差-步长）
# ==================================================================
def f06():
    """(a) 终态值随步长（温度，℃）；(b) 无量纲相对偏差 ＋ 理论收敛阶参考线。"""
    import csv
    rows = list(csv.DictReader(open(os.path.join(DATA, "fig_gci_data.csv"),
                                    encoding="utf-8")))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM))

    # ---- (a) 终态值（同为温度量纲，可比） ----
    for grp, key, lab, mk, col in [("spatial", "Tc", "空间 · $T(0)$", "o", BLUE),
                                   ("spatial", "Ts", "空间 · $T(R)$", "s", GOLD),
                                   ("temporal_T", "Tc", "时间 · $T(0)$", "^", GREEN)]:
        sel = [r for r in rows if r["group"] == grp]
        sel.sort(key=lambda r: float(r["delta"]))
        x = np.array([float(r["delta"]) for r in sel])
        y = np.array([float(r[key]) for r in sel])
        ax1.plot(x, y, marker=mk, ms=4.5, lw=1.3, color=col, label=lab)

    ax1.set_xscale("log")
    ax1.set_xlabel("步长（$\\Delta r$ / mm 或 $\\Delta t$ / s）")
    ax1.set_ylabel("终态温度 / ℃")
    ax1.set_title("(a) 终态值随步长（收敛于 4 位小数）")
    ax1.legend(frameon=False, loc="center right")
    _tick(ax1)

    # ---- (b) 无量纲相对偏差（|相邻差| / 终值），可跨量纲比较 ----
    for grp, key, lab, mk, col in [("spatial", "Tc", "空间 · $T(0)$", "o", BLUE),
                                   ("spatial", "Cs", "空间 · $C(R)$", "s", GOLD),
                                   ("temporal_T", "Tc", "时间 · $T(0)$", "^", GREEN),
                                   ("temporal_C", "Cs", "时间 · $C(R)$", "D", RED)]:
        sel = [r for r in rows if r["group"] == grp]
        sel.sort(key=lambda r: float(r["delta"]))
        x = np.array([float(r["delta"]) for r in sel])
        y = np.array([float(r[key]) for r in sel])
        rel = np.abs(np.diff(y)) / abs(y[-1])
        rel = np.where(rel <= 0, np.nan, rel)
        xd = x[:-1]
        p_obs = (abs(np.log2(rel[0] / rel[1]))
                 if np.isfinite(rel[1]) and rel[1] > 0 else float("nan"))
        ax2.plot(xd, rel, marker=mk, ms=4.5, lw=1.3, color=col,
                 label=f"{lab} (p = {p_obs:.2f})")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("步长（$\\Delta r$ / mm 或 $\\Delta t$ / s）")
    ax2.set_ylabel("相对偏差 $|\\Delta v|/v$（无量纲）")
    ax2.set_title("(b) 收敛阶：相对偏差与理论参考线")
    xr = np.array([0.1, 1.25])
    ax2.plot(xr, 3e-5 * xr, color=GRAY, ls="--", lw=1.0)
    ax2.plot(xr, 3e-6 * xr ** 2, color=GRAY, ls="-.", lw=1.0)
    ax2.text(1.10, 3e-5 * 1.10, "$O(h)$", color=GRAY, fontsize=7.5)
    ax2.text(1.05, 2.2e-6, "$O(h^2)$", color=GRAY, fontsize=7.5)
    _tick(ax2)
    ax2.legend(frameon=False, loc="lower right")

    despine(ax1); despine(ax2)
    fig.suptitle("网格与时间收敛性（空间二阶／时间一阶，与实测一致）", fontsize=10, y=1.02)
    save(fig, "F-06_网格与时间收敛")


# ==================================================================
# F-08 / F-09 场分布热力图
# ==================================================================
def _field(name, stem, title, cbl, vmin, vmax):
    d = load(name)
    t = d["time_s"]
    cols = [n for n in d.dtype.names if n != "time_s"]
    # 输出列固定为 r = 0, 0.1, ..., 2.0 cm（共 21 列）；显式构造轴，避免列名数字化歧义
    assert len(cols) == 21, f"期望 21 列，实得 {len(cols)}"
    r = np.linspace(0.0, 2.0, len(cols))
    Z = np.column_stack([d[n] for n in cols])

    fig, ax = plt.subplots(figsize=(9 * CM, 9 * CM))
    im = ax.pcolormesh(r, t, Z, cmap="viridis", vmin=vmin, vmax=vmax,
                       shading="auto", rasterized=True)
    cb = fig.colorbar(im, ax=ax, pad=0.03)
    cb.set_label(cbl, color=INK)
    cb.ax.tick_params(labelsize=8)
    cb.outline.set_edgecolor(INK)
    cb.outline.set_linewidth(0.5)
    ax.set_xlabel("到药材中心距离 $r$ / cm")
    ax.set_ylabel("时间 $t$ / s")
    ax.set_title(title)
    ax.grid(False)
    # 关键结论标注
    z00 = Z[0, 0]
    zR = Z[-1, -1]
    ax.text(1.98, 1780, f"$t$=1800 s 表面 {zR:.4f}", color="w", fontsize=7.5,
            ha="right", va="top")
    ax.text(0.02, 60, f"$t$=0 初值 {z00:.4f}", color="w", fontsize=7.5,
            ha="left", va="bottom")
    save(fig, stem)


def f08():
    _field("fig_q1_field_T.csv", "F-08_Q1温度场时空分布",
           "第一问温度场 $T(r,t)$ 时空分布", "温度 / ℃", 28.0, 37.0)


def f09():
    _field("fig_q1_field_C.csv", "F-09_Q1水分浓度场时空分布",
           "第一问水分浓度场 $C(r,t)$ 时空分布", "水分浓度 / (kg/kg，干基)", 1.5, 2.55)


# ==================================================================
# F-10 关键点时程曲线（双纵轴）
# ==================================================================
def f10():
    d = load("fig_q1_curves.csv")
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.plot(d["time_s"], d["T_center"], color=BLUE, lw=1.8, marker="o", ms=3.5,
            markevery=300, label="温度 · 中心")
    ax.plot(d["time_s"], d["T_surface"], color=GOLD, lw=1.8, marker="^", ms=3.5,
            markevery=300, label="温度 · 表面")
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("温度 / ℃")
    ax.set_ylim(27.4, 39.4)

    ax2 = ax.twinx()
    ax2.plot(d["time_s"], d["C_center"], color=GREEN, lw=1.8, marker="s", ms=3.5,
             markevery=300, label="含水率 · 中心")
    ax2.plot(d["time_s"], d["C_surface"], color=RED, lw=1.8, marker="D", ms=3.5,
             markevery=300, label="含水率 · 表面")
    ax2.set_ylabel("水分浓度 / (kg/kg)")
    ax2.set_ylim(1.38, 2.80)
    ax2.grid(False)
    despine(ax2)

    # 关键值标注：用坐标轴相对位置排布，避免与曲线／图例重叠
    # （规格卡要求：关键结论图必须带量化值）
    ax.text(0.33, 0.96, f"$T(0,1800)$ = {d['T_center'][-1]:.4f} ℃",
            transform=ax.transAxes, color=BLUE, fontsize=7.5, va="top")
    ax.text(0.33, 0.885, f"$T(R,1800)$ = {d['T_surface'][-1]:.4f} ℃",
            transform=ax.transAxes, color=GOLD, fontsize=7.5, va="top")
    ax.text(0.44, 0.045, f"$C(0,1800)$ = {d['C_center'][-1]:.4f}",
            transform=ax.transAxes, color=GREEN, fontsize=7.5, va="bottom")
    ax.text(0.44, 0.115, f"$C(R,1800)$ = {d['C_surface'][-1]:.4f}",
            transform=ax.transAxes, color=RED, fontsize=7.5, va="bottom")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center left", frameon=False,
              bbox_to_anchor=(0.25, 0.52))
    ax.set_title("关键点温度与含水率时程")
    save(fig, "F-10_Q1关键点时程曲线")


# ==================================================================
# F-11 / F-12 上折线 ＋ 下偏差（双联）
# ==================================================================
def _dual(t, yn, ya, dn, ln_n, ln_a, stem, title, ylab, dev_floor):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 9 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.12))
    ax1.plot(t, yn, color=BLUE, lw=1.8, marker="o", ms=3.5, label=ln_n)
    ax1.plot(t, ya, color=GOLD, lw=1.4, ls="--", marker="^", ms=3.5, label=ln_a)
    ax1.set_ylabel(ylab)
    ax1.set_title(title)
    ax1.legend(frameon=False, loc="best")
    despine(ax1)

    dev = np.asarray(yn) - np.asarray(ya)
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.plot(t, dev, color=RED, lw=1.6, marker="D", ms=3.5)
    ax2.set_xlabel("时间 $t$ / s")
    ax2.set_ylabel("偏差 $\\Delta$")
    ax2.set_ylim(*dev_floor)
    ax2.annotate(f"最大 $|\\Delta|$={np.max(np.abs(dev)):.2e}",
                 xy=(t[int(np.argmax(np.abs(dev)))], dev[int(np.argmax(np.abs(dev)))]),
                 xytext=(0.35, 0.75), textcoords="axes fraction",
                 fontsize=7.5, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    despine(ax2)
    save(fig, stem)


def f11():
    import csv
    rows = list(csv.DictReader(open(os.path.join(DATA, "fig_series_check.csv"),
                                    encoding="utf-8")))
    sel = [r for r in rows if r["case"] == "E2a_dr0.25mm"]
    t = np.array([float(r["t"]) for r in sel])
    _dual(t,
          [float(r["Tc_num"]) for r in sel], [float(r["Tc_ana"]) for r in sel],
          None, "数值解（0.25 mm）", "解析级数解",
          "F-11_解析级数解对拍", "温度解析对拍（常边界特例，$r=0$）",
          "温度 / ℃", (-6e-3, 6e-3))


def f12():
    d = load("fig_e3_check.csv")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 9 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.12))
    ax1.plot(d["t"], d["Ts_main"], color=BLUE, lw=1.8, marker="o", ms=4,
             label="主力解（全隐式）")
    ax1.plot(d["t"], d["Ts_expl"], color=GOLD, lw=1.4, ls="--", marker="^", ms=4,
             label="独立实现（显式 FTCS）")
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("独立实现互验（表面温度，$t\\leq3$ h）")
    ax1.legend(frameon=False)
    despine(ax1)

    dev = d["Ts_main"] - d["Ts_expl"]
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.plot(d["t"], dev, color=RED, lw=1.6, marker="D", ms=4)
    ax2.set_xlabel("时间 $t$ / s")
    ax2.set_ylabel("偏差 $\\Delta T$ / ℃")
    ax2.annotate(f"最大 $|\\Delta T|$={np.max(np.abs(dev)):.2e} ℃",
                 xy=(d["t"][int(np.argmax(np.abs(dev)))],
                     dev[int(np.argmax(np.abs(dev)))]),
                 xytext=(0.05, 0.72), textcoords="axes fraction", fontsize=7.5,
                 color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    despine(ax2)
    save(fig, "F-12_独立实现互验")


# ==================================================================
# F-13 参数灵敏度龙卷风图（2×2）
# ==================================================================
def f13():
    import csv
    rows = list(csv.DictReader(open(os.path.join(DATA, "fig_tornado_data.csv"),
                                    encoding="utf-8")))
    outs = ["T_center", "T_surface", "C_center", "C_surface"]
    nice = {"T_center": "温度 · 中心", "T_surface": "温度 · 表面",
            "C_center": "含水率 · 中心", "C_surface": "含水率 · 表面"}

    fig, axes = plt.subplots(2, 2, figsize=(16 * CM, 9 * CM))
    for ax, o in zip(axes.ravel(), outs):
        sel = [r for r in rows if r["output"] == o]
        sel.sort(key=lambda r: abs(float(r["S_norm"])))
        names = [r["parameter"] for r in sel]
        vals = [float(r["S_norm"]) for r in sel]
        y = np.arange(len(names))
        cols = [BLUE if v >= 0 else RED for v in vals]
        ax.barh(y, vals, color=cols, height=0.62)
        ax.set_yticks(y)
        ax.set_yticklabels(names)
        ax.axvline(0, color=GRAY, ls="--", lw=1.0)
        ax.set_title(nice[o], fontsize=9)
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
        mx = max(abs(min(vals)), abs(max(vals)), 0.1)
        ax.set_xlim(-mx * 1.25, mx * 1.25)
        for yi, v in zip(y, vals):
            ax.text(v + (mx * 0.05 if v >= 0 else -mx * 0.05), yi,
                    f"{v:+.3f}", va="center",
                    ha="left" if v >= 0 else "right", fontsize=7)
        despine(ax)
    fig.supxlabel("归一化灵敏度系数 $S$", fontsize=9)
    fig.suptitle("参数灵敏度（OAT ±20%，归一化系数）", fontsize=10, y=1.0)
    fig.tight_layout()
    save(fig, "F-13_参数灵敏度龙卷风图")


# ==================================================================
# F-14 数据预处理对照（分组柱状，对数轴）
# ==================================================================
def f14():
    import csv
    rows = list(csv.DictReader(open(os.path.join(DATA, "fig_smooth_check.csv"),
                                    encoding="utf-8")))
    groups = ["dT0", "dTR", "dC0", "dCR", "field_max_T"]
    labs = ["$\\Delta T(0)$\n/℃", "$\\Delta T(R)$\n/℃", "$\\Delta C(0)$\n/(kg/kg)",
            "$\\Delta C(R)$\n/(kg/kg)", "全场最大\n偏差 $T$ /℃"]
    FLOOR = 1e-9  # 对数轴下的零值显示下限（≈0）

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    x = np.arange(len(groups))
    w = 0.36
    cols = [BLUE, GOLD]
    for k, (r, c) in enumerate(zip(rows, cols)):
        v = [max(abs(float(r[g])), FLOOR) for g in groups]
        b = ax.bar(x + (k - 0.5) * w, v, w, color=c, label=r["case"])
        for xi, vi in zip(b, v):
            ax.text(xi.get_x() + xi.get_width() / 2, vi * 1.35,
                    "≈0" if vi <= FLOOR else f"{vi:.1e}",
                    ha="center", fontsize=6.5, color=INK)

    ax.set_yscale("log")
    ax.set_ylim(1e-9, 1e-0)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=7.5)
    ax.set_ylabel("偏差绝对值（对数轴）")
    ax.axhline(1e-2, color=GRAY, ls="--", lw=1.0)
    ax.text(len(groups) - 0.45, 1.5e-2, "$10^{-2}$ 参考", color=GRAY, fontsize=7,
            ha="right")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("边界平滑与否的对照（基准＝不平滑）")
    despine(ax)
    save(fig, "F-14_数据预处理对照")


# ==================================================================
if __name__ == "__main__":
    print("渲染输出目录：", OUT)
    for fn in (f03, f06, f08, f09, f10, f11, f12, f13, f14):
        try:
            fn()
        except Exception as e:
            print("  [FAIL]", fn.__name__, "->", repr(e))
    print("完成。")
