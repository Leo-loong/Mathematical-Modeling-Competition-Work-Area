# -*- coding: utf-8 -*-
"""
A 题 · 第二问（Q2）参考图渲染（F-15 ～ F-20）
================================================================
本脚本位于【工作区】30_图表/06_参考图渲染/，**不属于交接包**——
按分工，最终绘图由写作者按规格卡执行；本脚本只生成「参考图」供对照。

读取 交接包/04_图表包/data/ 下的 Q2 数据，输出至
      交接包/04_图表包/figures_reference/（300 DPI PNG ＋ PDF）

设计语言与 Q1 一致（见 04-2_项目图表设计语言.md）：
  主色 #1F3A93 ｜ #F39C12 ｜ #27AE60 ｜ #C0392B ｜ 参考线 #9E9E9E ｜ 文字 #333333
  场量色阶 viridis ｜ 中文字体 微软雅黑 ｜ 导出 300 DPI PNG + PDF
"""
import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
    "axes.grid.axis": "y",
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


def rd(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.reader(f))


# ==================================================================
def f15():
    rows = rd("fig_q2_props.csv")[1:]
    C = np.array([float(r[0]) for r in rows])
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    for i, (lab, col) in enumerate([("$\\rho$", BLUE), ("$c_p$", GOLD),
                                    ("$k$", GREEN)], start=1):
        ax.plot(C, [float(r[i]) for r in rows], color=col, lw=1.8, label=lab)
    ax.plot(C, [float(r[4]) for r in rows], color=RED, lw=1.8, label="$D$（28 ℃）")
    ax.plot(C, [float(r[5]) for r in rows], color=RED, lw=1.4, ls="--",
            label="$D$（50 ℃）")
    ax.axvline(2.55, color=GRAY, ls=":", lw=1.0)
    ax.text(2.54, 0.86, "初值 $C_0$=2.55", rotation=90, color=GRAY,
            fontsize=7, va="bottom", ha="right")
    ax.set_xlabel("含水率 $C$ / (kg/kg，干基)")
    ax.set_ylabel("相对 $C_0$ 处的比值（无量纲）")
    ax.set_title("第二问物性随含水率的演化")
    ax.legend(frameon=False, loc="lower left")
    despine(ax)
    save(fig, "F-15_Q2变物性演化")


def _field(name, stem, title, cbl, vmin, vmax, note, note_xy):
    rows = rd(name)
    hdr = rows[0]
    t = np.array([float(r[0]) for r in rows[1:]])
    r = np.linspace(0.0, 2.0, len(hdr) - 1)
    Z = np.array([[float(v) for v in row[1:]] for row in rows[1:]])
    fig, ax = plt.subplots(figsize=(9 * CM, 9 * CM))
    im = ax.pcolormesh(r, t, Z, cmap="viridis", vmin=vmin, vmax=vmax,
                       shading="auto", rasterized=True)
    cb = fig.colorbar(im, ax=ax, pad=0.03)
    cb.set_label(cbl, color=INK)
    cb.ax.tick_params(labelsize=8)
    cb.outline.set_edgecolor(INK); cb.outline.set_linewidth(0.5)
    ax.axhline(1800, color="w", ls="--", lw=1.0)
    ax.text(0.05, 1900, "第一问窗口末端 $t$=1800 s", color="w", fontsize=7)
    ax.set_xlabel("到药材中心距离 $r$ / cm")
    ax.set_ylabel("时间 $t$ / s")
    ax.set_title(title)
    ax.grid(False)
    ax.text(note_xy[0], note_xy[1], note, color="w", fontsize=7.5,
            ha="right", va="top")
    save(fig, stem)


def f16():
    _field("fig_q2_field_T.csv", "F-16_Q2温度场时空分布",
           "第二问温度场 $T(r,t)$（0–3 h）", "温度 / ℃", 28.0, 50.0,
           "", (1.95, 10600))


def f17():
    _field("fig_q2_field_C.csv", "F-17_Q2水分浓度场时空分布",
           "第二问水分浓度场 $C(r,t)$（0–3 h）", "水分浓度 / (kg/kg，干基)",
           0.9, 2.55, "", (1.95, 10600))


def f18():
    rows = rd("fig_q2_curves.csv")[1:]
    t = np.array([float(r[0]) for r in rows])
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.plot(t, [float(r[1]) for r in rows], color=BLUE, lw=1.8, label="温度 · 中心")
    ax.plot(t, [float(r[2]) for r in rows], color=GOLD, lw=1.8, label="温度 · 表面")
    ax.axvline(1800, color=GRAY, ls="--", lw=1.0)
    ax.text(1900, 30.4, "第一问窗口末端", color=GRAY, fontsize=7)
    ax.set_xlabel("时间 $t$ / s"); ax.set_ylabel("温度 / ℃")
    ax.set_ylim(27.4, 52.4)
    ax2 = ax.twinx()
    ax2.plot(t, [float(r[3]) for r in rows], color=GREEN, lw=1.8, label="含水率 · 中心")
    ax2.plot(t, [float(r[4]) for r in rows], color=RED, lw=1.8, label="含水率 · 表面")
    ax2.set_ylabel("水分浓度 / (kg/kg)"); ax2.set_ylim(0.9, 2.75)
    ax2.grid(False); despine(ax2)
    ax.text(0.30, 0.96, f"$T(0,10800)$ = {float(rows[-1][1]):.4f} ℃",
            transform=ax.transAxes, color=BLUE, fontsize=7.5, va="top")
    ax.text(0.30, 0.885, f"$T(R,10800)$ = {float(rows[-1][2]):.4f} ℃",
            transform=ax.transAxes, color=GOLD, fontsize=7.5, va="top")
    ax.text(0.42, 0.045, f"$C(0,10800)$ = {float(rows[-1][3]):.6f}",
            transform=ax.transAxes, color=GREEN, fontsize=7.5, va="bottom")
    ax.text(0.42, 0.115, f"$C(R,10800)$ = {float(rows[-1][4]):.6f}",
            transform=ax.transAxes, color=RED, fontsize=7.5, va="bottom")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center left", frameon=False,
              bbox_to_anchor=(0.24, 0.52))
    ax.set_title("第二问关键点时程曲线（0–3 h）")
    save(fig, "F-18_Q2关键点时程曲线")


def f19():
    rows = rd("fig_q1q2_overlap.csv")[1:]
    t = np.array([float(r[0]) for r in rows])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM))
    # 左：温度
    ax1.plot(t, [float(r[1]) for r in rows], color=BLUE, lw=1.8,
             label="第一问（附录2 常物性）")
    ax1.plot(t, [float(r[2]) for r in rows], color=BLUE, lw=1.4, ls="--",
             label="第二问（附录3 变物性）")
    ax1.set_xlabel("时间 $t$ / s"); ax1.set_ylabel("中心温度 / ℃")
    ax1.set_title("(a) 中心温度")
    ax1.legend(frameon=False, loc="upper left")
    despine(ax1)
    # 右：表面含水率
    ax2.plot(t, [float(r[5]) for r in rows], color=RED, lw=1.8, label="第一问")
    ax2.plot(t, [float(r[6]) for r in rows], color=RED, lw=1.4, ls="--", label="第二问")
    ax2.set_xlabel("时间 $t$ / s"); ax2.set_ylabel("表面含水率 / (kg/kg)")
    ax2.set_title("(b) 表面含水率")
    ax2.legend(frameon=False, loc="upper right")
    despine(ax2)
    fig.suptitle("两问重叠段（0–30 min）差异归因：物性体系不同（$\\alpha$ 相差约 14%）",
                 fontsize=9.5, y=1.02)
    save(fig, "F-19_Q1与Q2重叠段差异归因")


def f20():
    rows = rd("fig_q2_gci.csv")[1:]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM))
    styles = {"spatial": (BLUE, "o", "空间"), "time_T": (GREEN, "^", "时间·温度"),
              "time_C": (RED, "D", "时间·含水率")}
    for grp, (col, mk, lab) in styles.items():
        sel = [r for r in rows if r[0] == grp]
        sel.sort(key=lambda r: float(r[2]))
        x = [float(r[2]) for r in sel]; y = [float(r[3]) for r in sel]
        ax1.plot(x, y, marker=mk, ms=4.5, lw=1.3, color=col, label=lab)
    ax1.set_xscale("log")
    ax1.set_xlabel("步长（$\\Delta r$/mm 或内部步长/s）")
    ax1.set_ylabel("终态关键量（℃ 或 kg/kg）")
    ax1.set_title("(a) 终态值随步长")
    ax1.legend(frameon=False, loc="center right")
    ax1.set_xticks([0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0])
    ax1.set_xticklabels(["1/64", "1/32", "1/16", "1/8", "1/4", "1/2", "1"])
    ax1.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    for grp, (col, mk, lab) in styles.items():
        sel = [r for r in rows if r[0] == grp]
        sel.sort(key=lambda r: float(r[2]))
        x = [float(r[2]) for r in sel]; rel = [float(r[4]) for r in sel]
        rel = [v if v > 0 else np.nan for v in rel]
        ax2.plot(x, rel, marker=mk, ms=4.5, lw=1.3, color=col, label=lab)
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.axhline(5e-5, color=GRAY, ls="--", lw=1.0)
    ax2.text(0.02, 6e-5, "判定阈值 $5\\times10^{-5}$", color=GRAY, fontsize=7)
    ax2.set_xlabel("步长（$\\Delta r$/mm 或内部步长/s）")
    ax2.set_ylabel("相对变化（无量纲）")
    ax2.set_title("(b) 相对变化与判定阈值")
    ax2.legend(frameon=False, loc="lower right")
    ax2.set_xticks([0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0])
    ax2.set_xticklabels(["1/64", "1/32", "1/16", "1/8", "1/4", "1/2", "1"])
    ax2.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    despine(ax1); despine(ax2)
    fig.suptitle("第二问收敛性（空间二阶／时间一阶）", fontsize=10, y=1.02)
    save(fig, "F-20_Q2收敛性")


if __name__ == "__main__":
    print("Q2 参考图输出目录：", OUT)
    for fn in (f15, f16, f17, f18, f19, f20):
        try:
            fn()
        except Exception as e:
            print("  [FAIL]", fn.__name__, "->", repr(e))
    print("完成。")
