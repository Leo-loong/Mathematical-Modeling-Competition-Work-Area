# -*- coding: utf-8 -*-
"""
A 题 · 第二问（Q2）增强参考图渲染（F-21 ～ F-32）
================================================================
本脚本位于【工作区】30_图表/06_参考图渲染/，**不属于交接包**——
按分工，最终绘图由写作者按规格卡执行；本脚本只生成「参考图」供对照。

读取 交接包/04_图表包/data/ 下的 Q2 数据，输出至
      交接包/04_图表包/figures_reference/（300 DPI PNG ＋ PDF）

设计语言（见 04-2_项目图表设计语言.md）：
  主色 #1F3A93 ｜ #F39C12 ｜ #27AE60 ｜ #C0392B ｜ 参考线 #9E9E9E ｜ 文字 #333333
  场量色阶 viridis ｜ 中文字体 微软雅黑 ｜ 导出 300 DPI PNG + PDF

数据纪律：**只读** data/*.csv，不重算、不改数；缺项降级而非编造。
两处降级已在代码内注明：
  · F-29：本包仅有"潜热偏差"，无两条绝对时程 ⟹ 上下两联改为"温度偏差／含水率偏差"；
  · F-30：第 4 方案（自适应）的偏差基准不同（相对固定解），**不并置** ⟹ 仅画 3 点。
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE, GOLD, GREEN, RED = "#1F3A93", "#F39C12", "#27AE60", "#C0392B"
GRAY, INK, GRID, DGRAY = "#9E9E9E", "#333333", "#E0E0E0", "#424242"

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

RADII = ["%.1f" % (0.1 * i) for i in range(21)]   # 0.0 … 2.0


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
        return list(csv.DictReader(f))


def fnum(x, default=float("nan")):
    try:
        s = str(x).strip()
        return float(s) if s != "" else default
    except Exception:
        return default


def box(ax, x, y, w, h, text, fc="#FFFFFF", ec=INK, fs=7.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012",
                                fc=fc, ec=ec, lw=0.9))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=INK)


def arrow(ax, p, q, color=INK, ls="-", rad=0.0, lw=1.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=9,
                                 color=color, ls=ls, lw=lw,
                                 connectionstyle="arc3,rad=%.2f" % rad))


# ==================================================================
# F-21 双向耦合关系图（机理示意，无数据）
# ==================================================================
def f21():
    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    box(ax, 0.9, 3.0, 3.2, 1.5, "温度场 $T(r,t)$\n（能量方程，变 $\\rho c_p$、变 $k$）",
        fc="#EAF0FB", ec=BLUE)
    box(ax, 5.9, 3.0, 3.2, 1.5, "水分浓度场 $C(r,t)$\n（质量方程，变 $D$）",
        fc="#FDF3E2", ec=GOLD)
    arrow(ax, (4.15, 4.15), (5.85, 4.15), color=RED)
    ax.text(5.0, 4.45, "$D=D_0e^{-0.45/C}e^{-3850/T}$\n（温度 $\\uparrow\\Rightarrow D\\uparrow$）",
            ha="center", fontsize=7.2, color=RED)
    arrow(ax, (5.85, 3.35), (4.15, 3.35), color=GREEN)
    ax.text(5.0, 2.72, "$\\rho=650+128C$，$c_p,k$ 随 $C$ 变\n（含水率 $\\downarrow\\Rightarrow$ 升温 $\\uparrow$）",
            ha="center", fontsize=7.2, color=GREEN)
    box(ax, 2.6, 1.05, 4.8, 0.85, "IMEX 交替推进：物性**逐内部子步**更新（滞后量 $\\propto$ 子步长）",
        fc="#F2F2F2", ec=GRAY, fs=7.0)
    arrow(ax, (3.4, 2.98), (3.4, 1.95), color=GRAY, ls="--")
    arrow(ax, (6.6, 2.98), (6.6, 1.95), color=GRAY, ls="--")
    ax.text(0.25, 5.25, "Q2 双向强耦合：两条通道均以变物性为物理载体", fontsize=9, color=INK)
    despine(ax)
    save(fig, "F-21_Q2 双向耦合关系图")


# ==================================================================
# F-22 IMEX 交替推进算法流程图（无数据）
# ==================================================================
def f22():
    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    box(ax, 3.4, 5.25, 3.2, 0.7, "输出步 $t_n\\to t_{n+1}$（1 s）", fc="#F2F2F2", ec=GRAY)
    box(ax, 3.4, 4.25, 3.2, 0.7, "内部子步 $h=1/32$ s（32 次）", fc="#F2F2F2", ec=GRAY)
    box(ax, 3.4, 3.25, 3.2, 0.7, "① 按局部状态更新物性\n$\\rho(C),c_p(C),k(C),D(C,T)$",
        fc="#EAF0FB", ec=BLUE, fs=6.8)
    box(ax, 0.6, 2.15, 3.6, 0.7, "② 温度：全隐式（三对角追赶）", fc="#EAF0FB", ec=BLUE, fs=7.0)
    box(ax, 5.8, 2.15, 3.6, 0.7, "③ 由 $T$ 更新 $D$，含水率全隐式", fc="#FDF3E2", ec=GOLD, fs=7.0)
    box(ax, 5.8, 1.05, 3.6, 0.75,
        "④ Picard 迭代：$\\omega=0.7$、$tol=10^{-10}$、上限 30", fc="#FDF3E2", ec=GOLD, fs=6.8)
    arrow(ax, (5.0, 5.25), (5.0, 4.95))
    arrow(ax, (5.0, 4.25), (5.0, 3.95))
    arrow(ax, (5.0, 3.25), (5.0, 2.85))
    arrow(ax, (5.0, 2.85), (2.4, 2.85))
    arrow(ax, (2.4, 2.85), (2.4, 2.15))
    arrow(ax, (2.4, 1.8), (5.8, 1.8))
    arrow(ax, (7.6, 2.15), (7.6, 1.80))
    arrow(ax, (5.8, 1.42), (5.0, 1.42), color=GRAY, ls="--", lw=0.9)
    arrow(ax, (5.0, 1.42), (5.0, 2.85), color=GRAY, ls="--", lw=0.9, rad=-0.35)
    ax.text(4.2, 1.05, "未收敛 → 回代 ②③（本子步内迭代）", fontsize=6.8, color=GRAY)
    ax.text(0.6, 0.35, "整个算例规模：$3\\ \\mathrm{h}=10800$ 输出步 $\\times\\ 32$ 内部子步", fontsize=7.2, color=INK)
    ax.text(0.25, 6.0, "Q2 求解算法（IMEX 交替推进）", fontsize=9, color=INK)
    despine(ax)
    save(fig, "F-22_IMEX 交替推进算法流程图")


# ==================================================================
# F-23 三维演化曲面（$T$–$C$–$t$）
# ==================================================================
def f23():
    Tr = rd("fig_q2_field_T.csv")
    Cr = rd("fig_q2_field_C.csv")
    t = np.array([fnum(x["time_s"]) for x in Tr])
    r = np.array([float(k) for k in RADII])
    T = np.array([[fnum(x[k]) for k in RADII] for x in Tr])
    C = np.array([[fnum(x[k]) for k in RADII] for x in Cr])

    idx = np.unique(np.linspace(0, len(t) - 1, 400).astype(int))
    norm = plt.Normalize(float(t[0]), float(t[-1]))
    cmap = plt.get_cmap("viridis")

    fig = plt.figure(figsize=(16 * CM, 10 * CM))
    ax = fig.add_subplot(111, projection="3d")
    for i in idx:
        ax.plot(r, C[i], T[i], color=cmap(norm(t[i])), lw=0.6, alpha=0.85)
    X = np.tile(r, (len(idx), 1))
    ax.contour(X, C[idx], T[idx], levels=10, zdir="z", offset=float(T.min()),
               cmap="viridis", linewidths=0.5, alpha=0.65)
    ax.plot(r, C[idx[0]], T[idx[0]], color=RED, lw=1.6)
    ax.plot(r, C[idx[-1]], T[idx[-1]], color=RED, lw=1.6, ls="--")
    ax.set_xlabel("半径 $r$ / cm", labelpad=2)
    ax.set_ylabel("含水率 $C$ / (kg/kg)", labelpad=2)
    ax.set_zlabel("温度 $T$ / ℃", labelpad=2)
    ax.view_init(elev=22, azim=-58)
    ax.tick_params(labelsize=7)
    m = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    m.set_array(t)
    fig.colorbar(m, ax=ax, shrink=0.60, pad=0.10, label="时间 $t$ / s")
    ax.set_title("Q2 三维演化曲面（$r$–$C$–$T$，底面为等温线投影；视角 elev=22°, azim=-58°）",
                 fontsize=9)
    fig.text(0.30, 0.012, "红色实线＝$t=0$；红虚线＝$t=3$ h（曲线族已抽样至 400 条）",
             fontsize=6.5, color=RED)
    save(fig, "F-23_Q2 三维演化曲面（$T$–$C$–$t$）")


# ==================================================================
# F-24 温度–含水率相轨迹图
# ==================================================================
def f24():
    Tr = rd("fig_q2_field_T.csv")
    Cr = rd("fig_q2_field_C.csv")
    picks = ["0.0", "0.5", "1.0", "1.5", "2.0"]
    cmap = plt.get_cmap("viridis")

    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    for j, rr in enumerate(picks):
        tt = np.array([fnum(x[rr]) for x in Tr])
        cc = np.array([fnum(x[rr]) for x in Cr])
        col = cmap(j / (len(picks) - 1.0))
        ax.plot(cc, tt, lw=1.5, color=col, label="r = %s cm" % rr)
        ax.plot(cc[0], tt[0], "o", ms=4.2, color=col)
        ax.plot(cc[-1], tt[-1], "^", ms=4.8, color=col)
    ax.axvline(2.55, color=GRAY, ls=":", lw=1.0)
    ax.text(2.545, 28.6, "初值 $C_0=2.55$（完全解耦参照）", rotation=90,
            fontsize=6.8, color=GRAY, ha="right", va="bottom")
    ax.set_xlabel("含水率 $C$ / (kg/kg)")
    ax.set_ylabel("温度 $T$ / ℃")
    ax.set_title("Q2 温度–含水率相轨迹（○ 起点 $t=0$，▲ 终点 $t=3$ h）")
    ax.legend(frameon=False, ncol=2, loc="lower left")
    despine(ax)
    save(fig, "F-24_温度–含水率相轨迹图")


# ==================================================================
# F-25 全断面失水瀑布图（分层堆叠面积，相对降幅）
# ==================================================================
def f25():
    Cr = rd("fig_q2_field_C.csv")
    t = np.array([fnum(x["time_s"]) for x in Cr])
    picks = ["0.0", "0.4", "0.8", "1.2", "1.6", "2.0"]
    C0 = 2.55
    series = [100.0 * (C0 - np.array([fnum(x[k]) for x in Cr])) / C0 for k in picks]
    cmap = plt.get_cmap("viridis")

    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    ax.stackplot(t, *series, colors=[cmap(j / 5.0) for j in range(6)],
                 labels=["r = %s cm" % k for k in picks], alpha=0.9)
    ax.set_xlim(0, 10800)
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("分层相对降幅 $100(C_0-C)/C_0$ / %（堆叠）")
    ax.set_title("Q2 全断面失水（分层相对降幅，堆叠；$t=3$ h）")
    ax.legend(frameon=False, ncol=3, loc="upper left")
    ax.text(0.985, 0.03, "中心层降幅最小 → 中心始终是最慢点",
            transform=ax.transAxes, ha="right", fontsize=6.8, color=GRAY)
    despine(ax)
    save(fig, "F-25_全断面失水瀑布图")


# ==================================================================
# F-26 灵敏度结构雷达图（Q1 vs Q2，双联）
# ==================================================================
def f26():
    gs = rd("fig_q1_gs.csv")
    s2 = rd("fig_q2_sens_S.csv")
    axes_p = ["h", "km", "D0", "Tinf", "Cinf"]
    q1map = {"h": "h", "km": "km", "D0": "D0", "Tinf": "Tinf_off", "Cinf": "Cinf_off"}
    panels = [("TR", "T_surface", "(a) 输出 $T(R)$"), ("CR", "C_surface", "(b) 输出 $C(R)$")]

    fig, axs = plt.subplots(1, 2, subplot_kw=dict(polar=True),
                            figsize=(16 * CM, 8.5 * CM))
    ang = np.linspace(0, 2 * np.pi, len(axes_p), endpoint=False).tolist()
    angc = ang + ang[:1]

    for ax, (q1o, q2o, title) in zip(axs, panels):
        v1 = []
        v2 = []
        for p in axes_p:
            m = [r for r in gs if r["output"] == q1o and r["param"] == q1map[p]]
            v1.append(abs(fnum(m[0]["mu_star"])) if m else 0.0)
            n = [r for r in s2 if r["output"] == q2o and r["parameter"] == p]
            v2.append(abs(fnum(n[0]["S_half"])) if n else 0.0)
        v1 = np.array(v1, dtype=float)
        v2 = np.array(v2, dtype=float)
        v1 = v1 / v1.max() if v1.max() > 0 else v1
        v2 = v2 / v2.max() if v2.max() > 0 else v2
        v1 = np.r_[v1, v1[0]]
        v2 = np.r_[v2, v2[0]]
        ax.plot(angc, v1, color=BLUE, lw=1.6)
        ax.fill(angc, v1, color=BLUE, alpha=0.35, label="Q1（Morris $\\mu^*$）")
        ax.plot(angc, v2, color=GOLD, lw=1.6)
        ax.fill(angc, v2, color=GOLD, alpha=0.35, label="Q2（OAT $|S_{\\rm half}|$）")
        ax.set_xticks(ang)
        ax.set_xticklabels(["h", "km", "D0", r"$T_\infty$", r"$C_\infty$"])
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0.5, 1.0])
        ax.set_yticklabels(["0.5", "1.0"], fontsize=6.3)
        ax.set_title(title, pad=14)
    axs[0].legend(loc="upper right", bbox_to_anchor=(1.30, 1.14),
                  frameon=False, fontsize=7)
    fig.text(0.02, 0.02, "两层按各自最大 $|S|$ 归一；两层度量口径不同（Morris 绝对效应 vs OAT 半差）"
                         "故只比较形状与排序，不得跨层比较绝对高度。",
             fontsize=6.3, color=GRAY)
    save(fig, "F-26_灵敏度结构雷达图（Q1 vs Q2）")


# ==================================================================
# F-27 耦合强度分解图
# ==================================================================
def f27():
    rows = rd("fig_q2_coupling.csv")
    modes = ["strong", "decoupled", "frozen"]
    label = {"strong": "强耦合", "decoupled": "单向 (decoupled)", "frozen": "冻结 (frozen)"}
    cols = [("T_center", "$T(0)$"), ("T_surface", "$T(R)$"),
            ("C_center", "$C(0)$"), ("C_surface", "$C(R)$")]
    colors = {"strong": BLUE, "decoupled": GOLD, "frozen": GREEN}
    get = {r["mode"]: r for r in rows}

    x = np.arange(len(cols))
    w = 0.26
    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    for j, m in enumerate(modes):
        vals = [fnum(get[m][c]) for c, _ in cols]
        ax.bar(x + (j - 1) * w, vals, w, color=colors[m], label=label[m])
    ax.set_xticks(x)
    ax.set_xticklabels([lb for _, lb in cols])
    ax.set_ylabel("末端值（1800 s）")
    ax.set_title("Q2 耦合强度分解（强耦合／单向／冻结三模式）")
    ax.legend(frameon=False, ncol=3)
    try:
        rc = float(get["decoupled"]["rel_CR_vs_strong"])
        rf = float(get["frozen"]["rel_CR_vs_strong"])
        ax.annotate("$C(R)$ 单向 vs 强耦合：%+.1f%%" % (100 * rc),
                    xy=(3 - w, fnum(get["decoupled"]["C_surface"])), xytext=(1.6, 2.30),
                    fontsize=7, color=GOLD, arrowprops=dict(arrowstyle="->", color=GOLD, lw=0.8))
        ax.annotate("冻结 vs 强耦合：%+.1f%%" % (100 * rf),
                    xy=(3 + w, fnum(get["frozen"]["C_surface"])), xytext=(2.1, 0.75),
                    fontsize=7, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.8))
    except Exception:
        pass
    despine(ax)
    save(fig, "F-27_耦合强度分解图")


# ==================================================================
# F-28 守恒性总账瀑布图（质量／能量分两张子图）
# ==================================================================
def f28():
    rows = rd("fig_q2_conservation.csv")
    by = {}
    for r in rows:
        by[(r["kind"], r["item"])] = fnum(r["value"])

    def wf(ax, kind, title, items):
        initial = by[(kind, "initial")]
        seq = [("初值", initial, "start")]
        cum = initial
        for name, key in items:
            v = by[(kind, key)]
            seq.append((name, v, "inc" if v >= 0 else "dec"))
            cum += v
        seq.append(("终值", by[(kind, "final")], "total"))
        for i, (name, v, kindv) in enumerate(seq):
            if kindv == "start":
                y0, hgt = 0.0, v
                cum = v
            elif kindv == "total":
                y0, hgt = 0.0, v
            else:
                y0, hgt = cum - v, v
            col = {"start": BLUE, "inc": BLUE, "dec": GOLD,
                   "total": GREEN}[kindv]
            ax.bar(i, hgt, 0.62, bottom=y0, color=col)
            ax.text(i, y0 + hgt + initial * 0.03, "%.2f" % (v / initial),
                    ha="center", fontsize=6.4, color=INK)
        ax.set_xticks(range(len(seq)))
        ax.set_xticklabels([s[0] for s in seq], fontsize=7)
        ax.set_ylabel("归一化储量（初值＝1）")
        ax.set_title(title)
        ax.axhline(1.0, color=GRAY, ls=":", lw=0.9)
        return seq

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16 * CM, 6.5 * CM),
                                 gridspec_kw=dict(wspace=0.28))
    wf(a1, "mass", "(a) 质量收支（$2.384\\times10^{-4}$ kg/kg 量级）",
       [("表面流出", "flux"), ("残差", "residual")])
    wf(a2, "energy", "(b) 能量收支（须含物性变化项）",
       [("边界流入", "flux"), ("物性变化项", "property_term"), ("残差", "residual")])
    a1.text(0.03, 0.93, "相对残差 $1.903\\times10^{-3}$", transform=a1.transAxes,
            fontsize=7, color=RED)
    a2.text(0.03, 0.93, "相对残差 $1.803\\times10^{-2}$", transform=a2.transAxes,
            fontsize=7, color=RED)
    for a in (a1, a2):
        despine(a)
    save(fig, "F-28_守恒性总账瀑布图")


# ==================================================================
# F-29 潜热对照双联图（本包仅有偏差 ⟹ 上温度偏差／下含水率偏差）
# ==================================================================
def f29():
    rows = rd("fig_q2_latent.csv")
    t = np.array([fnum(r["t_h"]) for r in rows])
    dTc = np.array([fnum(r["dT_center"]) for r in rows])
    dTs = np.array([fnum(r["dT_surface"]) for r in rows])
    dCc = np.array([fnum(r["dC_center"]) for r in rows])
    dCs = np.array([fnum(r["dC_surface"]) for r in rows])

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8 * CM, 10 * CM),
                                 gridspec_kw=dict(hspace=0.45))
    a1.axhline(0.0, color=GRAY, lw=0.9)
    a1.plot(t, dTc, marker="o", ms=4, lw=1.4, color=BLUE, label="$\\Delta T(0)$（中心）")
    a1.plot(t, dTs, marker="s", ms=4, lw=1.4, color=GOLD, label="$\\Delta T(R)$（表面）")
    a1.set_xlabel("时间 $t$ / h")
    a1.set_ylabel("$\\Delta T$ / ℃（计入 − 忽略）")
    a1.set_title("(a) 潜热项对温度的偏差")
    a1.legend(frameon=False)
    despine(a1)

    a2.axhline(0.0, color=GRAY, lw=0.9)
    a2.plot(t, dCc, marker="o", ms=4, lw=1.4, color=GREEN, label="$\\Delta C(0)$（中心）")
    a2.plot(t, dCs, marker="s", ms=4, lw=1.4, color=RED, label="$\\Delta C(R)$（表面）")
    a2.set_xlabel("时间 $t$ / h")
    a2.set_ylabel("$\\Delta C$ / (kg/kg)")
    a2.set_title("(b) 潜热项对含水率的偏差")
    a2.legend(frameon=False)
    despine(a2)
    a2.text(0.02, 0.06, "上下两联量纲不同、纵轴独立；本包仅有偏差、无两条绝对时程",
            transform=a2.transAxes, fontsize=6.3, color=GRAY)
    save(fig, "F-29_潜热对照双联图")


# ==================================================================
# F-30 精度–效率帕累托图（仅 3 点；第 4 方案基准不同，不并置）
# ==================================================================
def f30():
    rows = rd("fig_q2_pareto.csv")
    xs = np.array([fnum(r["wall_s"]) for r in rows])
    ys = np.array([fnum(r["rel_err"]) for r in rows])
    names = [r["scheme"] for r in rows]

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    for x, y, nm in zip(xs, ys, names):
        col = BLUE if "BE" in nm else GOLD
        mk = "o" if "BE" in nm else ("s" if "1/8" in nm else "^")
        ax.plot([x], [y], mk, ms=6.5, color=col)
        ax.annotate(nm, (x, y), textcoords="offset points", xytext=(6, 4),
                    fontsize=7, color=INK)
    o = np.argsort(xs)
    ax.plot(xs[o], ys[o], color=GRAY, ls="--", lw=1.0)
    ax.axhline(5e-5, color=RED, ls=":", lw=1.0)
    ax.text(xs.min(), 5e-5 * 1.06, "判据阈值 $5\\times10^{-5}$", fontsize=6.8, color=RED)
    ax.set_yscale("log")
    ax.set_xlabel("单机单线程墙钟 / s")
    ax.set_ylabel("相对误差（对数轴）")
    ax.set_title("Q2 精度–效率帕累托")
    ax.text(0.02, 0.03,
            "点稀疏：第 4 方案（自适应，9.9 s）的偏差基准不同（相对固定解），\n"
            "不满足“同基准”→ 按 F-30 卡不并置，仅画 3 点。",
            transform=ax.transAxes, fontsize=6.3, color=GRAY)
    despine(ax)
    save(fig, "F-30_精度–效率帕累托图")


# ==================================================================
# F-31 全局灵敏度热力图（Sobol $S_T$ 矩阵）
# ==================================================================
def f31():
    rows = rd("fig_q2_gs_sobol.csv")
    params = ["h", "km", "D0", "Tinf", "Cinf"]
    outs = ["T_center", "T_surface", "C_center", "C_surface"]
    plab = ["h", "km", "D0", r"$T_\infty$", r"$C_\infty$"]
    olab = ["$T(0)$", "$T(R)$", "$C(0)$", "$C(R)$"]
    M = np.full((len(params), len(outs)), np.nan)
    for r in rows:
        if r["parameter"] in params and r["output"] in outs:
            M[params.index(r["parameter"]), outs.index(r["output"])] = fnum(r["ST"])

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    im = ax.imshow(M, cmap="viridis", aspect="auto", vmin=0, vmax=np.nanmax(M))
    ax.set_xticks(range(len(outs)))
    ax.set_xticklabels(olab)
    ax.set_yticks(range(len(params)))
    ax.set_yticklabels(plab)
    for i in range(len(params)):
        for j in range(len(outs)):
            v = M[i, j]
            ax.text(j, i, "%.3f" % v, ha="center", va="center", fontsize=6.6,
                    color="white" if v > 0.55 * np.nanmax(M) else INK)
    fig.colorbar(im, ax=ax, shrink=0.85, label="Sobol 总效应 $S_T$")
    ax.set_title("Q2 全局灵敏度 $S_T$ 矩阵")
    ax.grid(False)
    ax.text(0.02, -0.20, "采样 $N=32$：个别 $S_T>1$／$S_T<S_1$ 系采样量偏小 → 仅用于排序、不可引用绝对值。",
            transform=ax.transAxes, fontsize=6.3, color=RED)
    save(fig, "F-31_全局灵敏度热力图（Sobol）")


# ==================================================================
# F-32 自适应步长轨迹图（阶梯 ＋ 双纵轴，点稀疏、不得插值）
# ==================================================================
def f32():
    rows = rd("fig_q2_adaptive.csv")
    t0 = np.array([fnum(r["t_s"]) for r in rows])
    hf = np.array([fnum(r["h_from_s"]) for r in rows])
    ht = np.array([fnum(r["h_to_s"]) for r in rows])
    rc = np.array([fnum(r["rel_change"]) for r in rows])

    xs = np.r_[0.0, t0, 10800.0]
    ys = np.r_[hf[0], ht, ht[-1]]

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.step(xs, ys, where="post", color=BLUE, lw=1.6)
    ax.set_yscale("log")
    ax.set_yticks([1 / 32.0, 1 / 16.0, 1 / 8.0, 1 / 4.0])
    ax.set_yticklabels(["1/32", "1/16", "1/8", "1/4"])
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("内部步长 $h$ / s（对数轴）")
    ax.set_xlim(0, 10800)
    ax.set_ylim(1 / 40.0, 1 / 3.0)

    a2 = ax.twinx()
    a2.plot(t0, rc, "o", ms=6, color=GOLD, label="相对变化率")
    a2.set_yscale("log")
    a2.set_ylabel("触发放大的相对变化率", color=GOLD)
    a2.tick_params(axis="y", colors=GOLD)
    a2.grid(False)
    despine(a2)
    for x, h in zip(t0, ht):
        ax.annotate("$h\\to$1/%.0f" % round(1 / h), (x, h), textcoords="offset points",
                    xytext=(6, -10), fontsize=6.6, color=BLUE)
    ax.set_title("Q2 自适应步长轨迹（阶梯，仅 3 个调步点）")
    ax.text(0.02, 0.04, "点稀疏属事实 → 不得插值连线；本图仅画实际调步时刻",
            transform=ax.transAxes, fontsize=6.3, color=GRAY)
    despine(ax)
    save(fig, "F-32_自适应步长轨迹图")


if __name__ == "__main__":
    for fn in (f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            print("  [FAIL]", fn.__name__, repr(exc), flush=True)
