# -*- coding: utf-8 -*-
"""
A 题 · 第三问（Q3）参考图渲染（F-33 ～ F-40）
================================================================
本脚本位于【工作区】30_图表/06_参考图渲染/，**不属于交接包**——
按分工，最终绘图由写作者按规格卡执行；本脚本只生成「参考图」供对照。

读取 交接包/04_图表包/data/ 下的 Q3 数据，输出至
      交接包/04_图表包/figures_reference/（300 DPI PNG ＋ PDF）

设计语言与 Q1／Q2 一致（见 04-2_项目图表设计语言.md）：
  主色 #1F3A93 ｜ #F39C12 ｜ #27AE60 ｜ #C0392B ｜ 参考线 #9E9E9E ｜ 文字 #333333
  中文字体 微软雅黑 ｜ 导出 300 DPI PNG + PDF

数据纪律：**只读** data/*.csv，不重算、不改数；缺列时降级而非编造。
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
        return list(csv.DictReader(f))


def fnum(x, default=float("nan")):
    try:
        s = str(x).strip()
        return float(s) if s != "" else default
    except Exception:
        return default


# ==================================================================
# F-33 长时程含水率演化 ＋ 内嵌（中心—表面差）
# ==================================================================
def f33():
    rows = rd("fig_q3_history.csv")
    t = np.array([fnum(r["t_h"]) for r in rows])
    cc = np.array([fnum(r["C_center"]) for r in rows])
    cs = np.array([fnum(r["C_surface"]) for r in rows])

    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    ax.axvspan(24.0, 57.5314, color="k", alpha=0.06, lw=0)
    ax.plot(t, cc, color=BLUE, lw=1.8, label="中心 $C(0)$")
    ax.plot(t, cs, color=RED, lw=1.8, label="表面 $C(R_0)$")
    ax.axhline(0.15, color=GRAY, ls="--", lw=1.0)
    ax.text(88, 0.185, "判据 $C=0.15$", color=GRAY, fontsize=7.5, ha="right")
    ax.axhline(0.04999, color=GREEN, ls=":", lw=1.0)
    ax.text(88, 0.070, "环境平衡 $C_\\infty=0.04999$", color=GREEN,
            fontsize=7.5, ha="right")

    i_end = int(np.argmin(np.abs(t - 57.5314)))
    ax.plot([57.5314], [cc[i_end]], marker="o", ms=5, color=BLUE)
    ax.annotate("烘干结束 57.5 h\n中心 $C=0.1500$",
                xy=(57.5314, cc[i_end]), xytext=(60, 0.78),
                fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.text(25.5, 2.42, "前期 24 h 脱除约九成", fontsize=7.5, color=INK)
    ax.text(38.0, 2.18, "降速段", fontsize=7.5, color=INK)

    ax.set_xlim(0, 90)
    ax.set_ylim(0, 2.6)
    ax.set_xlabel("时间 $t$ / h")
    ax.set_ylabel("水分浓度 $C$ / (kg/kg，干基)")
    ax.set_title("第三问中心与表面含水率的长时程演化")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False)
    despine(ax)

    axi = fig.add_axes([0.60, 0.56, 0.28, 0.28])
    axi.plot(t, cc - cs, color=INK, lw=1.2)
    axi.set_title("中心 − 表面 差值", fontsize=8)
    axi.tick_params(labelsize=6.5)
    axi.set_xlabel("$t$ / h", fontsize=7, labelpad=1)
    despine(axi)

    save(fig, "F-33_Q3长时程含水率演化与烘干结束时间")


# ==================================================================
# F-34 长时程收敛性与网格裁决（三联）
# ==================================================================
def f34():
    conv = rd("fig_q3_conv.csv")
    pos = rd("fig_q3_conv_pos.csv")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17 * CM, 9 * CM),
                                        gridspec_kw=dict(wspace=0.42))

    # (左) 时间收敛：相对变化 vs 内部步长
    tt = [r for r in conv if r["kind"] == "time"]
    tt = [r for r in tt if np.isfinite(fnum(r["rel_change"]))]
    xs = np.array([1.0 / fnum(r["nsub"]) for r in tt])
    ys = np.array([fnum(r["rel_change"]) for r in tt])
    o = np.argsort(xs)
    xs, ys = xs[o], ys[o]
    ax1.plot(xs, ys, marker="o", ms=4.5, lw=1.3, color=GREEN, label="$C(0)$")
    ax1.axhline(5e-5, color=GRAY, ls="--", lw=1.0)
    ax1.axhline(1e-3, color=GRAY, ls=":", lw=1.0)
    ax1.text(0.0165, 5.6e-5, "$5\\times10^{-5}$", color=GRAY, fontsize=7)
    ax1.text(0.0165, 1.12e-3, "$0.1\\%$", color=GRAY, fontsize=7)
    ax1.axvline(1 / 32.0, color=GRAY, ls=":", lw=1.0)
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xticks([1 / 64.0, 1 / 32.0, 1 / 16.0])
    ax1.set_xticklabels(["1/64", "1/32", "1/16"])
    ax1.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax1.set_xlabel("内部时间步 $\\Delta t$ / s")
    ax1.set_ylabel("相邻相对变化（无量纲）")
    ax1.set_title("(a) 时间收敛")
    ax1.legend(frameon=False, loc="upper left")

    # (中) 空间收敛：相对变化 vs Δr
    sp = [r for r in conv if r["kind"] == "space" and np.isfinite(fnum(r["rel_change"]))]
    xr = np.array([fnum(r["dr_mm"]) for r in sp])
    yr = np.array([fnum(r["rel_change"]) for r in sp])
    o = np.argsort(xr)
    xr, yr = xr[o], yr[o]
    ax2.plot(xr, yr, marker="s", ms=4.5, lw=1.3, color=BLUE, label="$C(0)$")
    ax2.axhline(5e-5, color=GRAY, ls="--", lw=1.0)
    ax2.axhline(1e-3, color=GRAY, ls=":", lw=1.0)
    ax2.axvline(0.25, color=GRAY, ls=":", lw=1.0)
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xticks([0.125, 0.25, 0.5, 1.0])
    ax2.set_xticklabels(["0.125", "0.25", "0.5", "1.0"])
    ax2.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax2.set_xlabel("空间步长 $\\Delta r$ / mm")
    ax2.set_ylabel("相邻相对变化（无量纲）")
    ax2.set_title("(b) 空间收敛")
    ax2.legend(frameon=False, loc="upper left")

    # (右) 各位置相邻网格相对变化（分组柱）
    pairs = []
    for r in pos:
        if r["pair"] not in pairs:
            pairs.append(r["pair"])
    locs = [0.0, 0.5, 1.0, 1.5, 2.0]
    w = 0.26
    x = np.arange(len(locs))
    for k, pr in enumerate(pairs):
        vals = [abs(fnum(next((r["rel_change"] for r in pos
                               if r["pair"] == pr and abs(fnum(r["loc_cm"]) - L) < 1e-9),
                              "nan"))) for L in locs]
        ax3.bar(x + (k - (len(pairs) - 1) / 2) * w, vals, w,
                color=[BLUE, GREEN, GOLD][k % 3], label=pr + " mm")
    ax3.axhline(0.1, color=GRAY, ls="--", lw=1.0)
    ax3.text(-0.42, 0.102, "$0.1\\%$ 判据", color=GRAY, fontsize=7, ha="left")
    ax3.set_xticks(x)
    ax3.set_xticklabels(["0", "0.5", "1.0", "1.5", "2.0"])
    ax3.set_xlabel("到药材中心距离 / cm")
    ax3.set_ylabel("相对变化 / %")
    ax3.set_title("(c) 各位置网格裁决")
    ax3.legend(frameon=False, loc="center right", fontsize=6.5)
    ax3.set_ylim(0, 0.12)

    for a in (ax1, ax2, ax3):
        despine(a)
    fig.suptitle("第三问长时程收敛性与网格裁决（内部与表面列均达 4 位小数稳定）",
                 fontsize=9.5, y=1.03)
    save(fig, "F-34_Q3收敛性与网格裁决")


# ==================================================================
# F-35 参数灵敏度（龙卷风式水平条形）
# ==================================================================
def f35():
    rows = rd("fig_q3_sensitivity.csv")
    rows.sort(key=lambda r: abs(fnum(r["S"])), reverse=True)
    names = [f'{r["param"]} {r["level"]}' for r in rows]
    vals = [fnum(r["dt_end_h"]) for r in rows]
    S = [fnum(r["S"]) for r in rows]
    y = np.arange(len(names))[::-1]

    fig, ax = plt.subplots(figsize=(16 * CM, 9 * CM))
    cols = [GREEN if v <= 0 else RED for v in vals]
    ax.barh(y, vals, color=cols, height=0.62)
    ax.axvline(0, color=INK, lw=1.0)
    mx = max(abs(min(vals)), abs(max(vals)))
    for yi, v, s in zip(y, vals, S):
        off = 0.25 if v >= 0 else -0.25
        ax.text(v + off, yi, f"{v:+.2f} h  ($S$={s:+.3f})", va="center",
                ha="left" if v >= 0 else "right", fontsize=7)
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlim(-mx * 1.55, mx * 1.55)
    ax.set_xlabel("烘干结束时间的变化量 $\\Delta t_{\\rm end}$ / h")
    ax.set_title("第三问烘干结束时间的参数灵敏度（基准 $57.53$ h）")
    ax.annotate("风速 $h$ 几乎无影响", xy=(0.02, y[-1]), xytext=(-mx * 0.55, y[-1] + 1.2),
                fontsize=7.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    ax.text(mx * 1.35, y[0] + 0.9, "缩短（负）", color=GREEN, fontsize=7.5, ha="right")
    ax.text(mx * 1.35, y[-1] - 0.9, "延长（正）", color=RED, fontsize=7.5, ha="right")
    despine(ax)
    save(fig, "F-35_Q3参数灵敏度")


# ==================================================================
# F-36 离散不确定度与误差带（双联）
# ==================================================================
def f36():
    rows = rd("fig_q3_gci.csv")
    sp = [r for r in rows if r["kind"] == "space"]
    tm = [r for r in rows if r["kind"] == "time"]
    sp.sort(key=lambda r: fnum(r["dr_mm"]), reverse=True)
    tm.sort(key=lambda r: fnum(r["h_in_s"]), reverse=True)

    xsp = np.array([fnum(r["dr_mm"]) for r in sp])
    ysp = np.array([fnum(r["t_end_h"]) for r in sp])
    xtm = np.array([fnum(r["h_in_s"]) for r in tm])
    ytm = np.array([fnum(r["t_end_h"]) for r in tm])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM),
                                   gridspec_kw=dict(wspace=0.28))

    ax1.axhspan(57.5275 - 0.0006, 57.5275 + 0.0006, color=GRAY, alpha=0.25, lw=0)
    ax1.plot(xsp, ysp, marker="o", ms=5, lw=1.4, color=BLUE, label="数值解")
    ax1.plot([0.0625], [57.5275], marker="*", ms=11, color=GOLD,
             label="Richardson 外推")
    ax1.axhline(57.5314, color=GRAY, ls="--", lw=1.0)
    ax1.text(0.065, 57.5317, "正式答案 57.53 h", color=GRAY, fontsize=7, ha="right")
    ax1.set_xscale("log")
    ax1.set_xticks([0.25, 0.125, 0.0625])
    ax1.set_xticklabels(["0.25", "0.125", "0.0625"])
    ax1.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax1.set_ylim(57.526, 57.533)
    ax1.set_xlabel("空间步长 $\\Delta r$ / mm")
    ax1.set_ylabel("$t_{\\rm end}$ / h")
    ax1.set_title("(a) 空间维：$p=1.650$，$\\mathrm{GCI}=0.0011\\%$")
    ax1.legend(frameon=False, loc="lower left")

    ax2.plot(xtm, ytm, marker="^", ms=5, lw=1.4, color=GREEN)
    ax2.axhline(57.5314, color=GRAY, ls="--", lw=1.0)
    ax2.annotate("三档非单调\n保守上界 $0.0802$ h", xy=(1 / 16.0, ytm[0]),
                 xytext=(1 / 40.0, 57.553), fontsize=7.5, color=INK,
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    ax2.set_xscale("log")
    ax2.set_xticks([1 / 64.0, 1 / 32.0, 1 / 16.0])
    ax2.set_xticklabels(["1/64", "1/32", "1/16"])
    ax2.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax2.set_ylim(57.49, 57.585)
    ax2.set_xlabel("内部时间步 $\\Delta t$ / s")
    ax2.set_ylabel("$t_{\\rm end}$ / h")
    ax2.set_title("(b) 时间维：非单调（不适用 Richardson）")
    for a in (ax1, ax2):
        despine(a)
    fig.suptitle("第三问核心答案的离散不确定度（合成口径取较大者，得 $t_{\\rm end}=57.53\\pm0.08$ h）",
                 fontsize=9.5, y=1.03)
    save(fig, "F-36_Q3离散不确定度与误差带")


# ==================================================================
# F-37 全局灵敏度（Morris ＋ Sobol，三联）
# ==================================================================
def f37():
    mo = rd("fig_q3_gs_morris.csv")
    so = rd("fig_q3_gs_sobol.csv")
    nice = {"T_inf": "$T_\\infty$", "D0": "$D_0$", "k_m": "$k_m$",
            "C_inf": "$C_\\infty$", "h": "$h$"}
    mo.sort(key=lambda r: fnum(r["S_norm"]), reverse=True)
    so.sort(key=lambda r: fnum(r["ST"]), reverse=True)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17 * CM, 9 * CM),
                                        gridspec_kw=dict(wspace=0.45))

    # (左) Morris μ*-σ 散点（气泡＝S_norm）
    mu = np.array([fnum(r["mu_star"]) for r in mo])
    sg = np.array([fnum(r["sigma"]) for r in mo])
    sn = np.array([fnum(r["S_norm"]) for r in mo])
    sz = 20 + 180 * sn / sn.max()
    ax1.scatter(mu, sg, s=sz, color=BLUE, alpha=0.65, edgecolor=INK, lw=0.5)
    for m, s, r in zip(mu, sg, mo):
        ax1.annotate(nice[r["param"]], (m, s), fontsize=7.5,
                     xytext=(3, 3), textcoords="offset points")
    ax1.set_xlabel("$\\mu^*$（平均绝对效应，无量纲归一）")
    ax1.set_ylabel("$\\sigma$（离散度）")
    ax1.set_title("(a) Morris $\\mu^*$–$\\sigma$")

    # (中) Morris S_norm 条形
    y2 = np.arange(len(mo))[::-1]
    ax2.barh(y2, [fnum(r["S_norm"]) for r in mo], color=BLUE, height=0.6)
    for yi, r in zip(y2, mo):
        ax2.text(fnum(r["S_norm"]) + 0.05, yi, f'{fnum(r["S_norm"]):.3f}',
                 va="center", fontsize=7)
    ax2.set_yticks(y2)
    ax2.set_yticklabels([nice[r["param"]] for r in mo])
    ax2.set_xlabel("相对灵敏度 $S_{\\rm norm}$")
    ax2.set_title("(b) Morris $S_{\\rm norm}$")

    # (右) Sobol S1 / ST 分组条形
    y3 = np.arange(len(so))[::-1]
    h = 0.36
    ax3.barh(y3 + h / 2, [fnum(r["ST"]) for r in so], h, color="#E67E22", label="$S_T$（总效应）")
    ax3.barh(y3 - h / 2, [fnum(r["S1"]) for r in so], h, color=BLUE, label="$S_1$（主效应）")
    ax3.axvline(0, color=INK, lw=0.8)
    ax3.annotate("$D_0$：$S_T=0.962$，交互 $=0.209$", xy=(0.96, y3[0] + h / 2),
                 xytext=(0.30, y3[0] - 1.15), fontsize=7.5, color=INK,
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    ax3.set_yticks(y3)
    ax3.set_yticklabels([nice[r["param"]] for r in so])
    ax3.set_xlabel("方差贡献比例")
    ax3.set_xlim(-0.15, 1.12)
    ax3.set_title("(c) Sobol $S_1$／$S_T$")
    ax3.legend(frameon=False, loc="lower right", fontsize=7)

    for a in (ax1, ax2, ax3):
        despine(a)
    fig.suptitle("第三问全局灵敏度：Morris 筛选与 Sobol 分解（$D_0$ 主导且交互显著）",
                 fontsize=9.5, y=1.03)
    save(fig, "F-37_Q3全局灵敏度")


# ==================================================================
# F-38 低含水率端外推不确定度（双联）
# ==================================================================
def f38():
    g = rd("fig_q3_uq_grid.csv")
    l = rd("fig_q3_uq_lhs.csv")
    xg = np.array([fnum(r["C_fr"]) for r in g])
    yg = np.array([fnum(r["t_end_h"]) for r in g])
    yl = np.array([fnum(r["t_end_h"]) for r in l])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM),
                                   gridspec_kw=dict(wspace=0.28))

    ax1.axhspan(19.82, 44.30, color=GRAY, alpha=0.20, lw=0)
    ax1.plot(xg, yg, marker="o", ms=4.5, lw=1.6, color="#8E44AD", label="截断族 $t_{\\rm end}(C_{\\rm fr})$")
    ax1.plot([0.0], [yg[0]], marker="*", ms=12, color="#E74C3C",
             label="无截断基线（正式答案）")
    for cf in (0.2, 0.3, 0.5):
        i = int(np.argmin(np.abs(xg - cf)))
        ax1.plot([cf], [yg[i]], marker="o", ms=4, color=INK)
        ax1.annotate(f"{yg[i]:.2f} h", (cf, yg[i]), fontsize=6.5,
                     xytext=(2, -8), textcoords="offset points")
    ax1.text(0.52, 47, "阴影：外推段贡献 43%–66% 时长", fontsize=7, color=INK)
    ax1.set_xlabel("$D$ 公式可信下限 $C_{\\rm fr}$（0＝无截断）")
    ax1.set_ylabel("$t_{\\rm end}$ / h")
    ax1.set_ylim(15, 62)
    ax1.set_title("(a) 确定性截断族")
    ax1.legend(frameon=False, loc="upper right")

    qs = [5, 25, 50, 75, 95]
    vals = np.percentile(yl, qs)
    xq = np.arange(len(qs))
    ax2.plot(xq, vals, marker="o", ms=5, lw=1.4, color="#8E44AD")
    ax2.axhline(57.53, color=GRAY, ls="--", lw=1.0)
    ax2.text(4.0, 57.9, "正式答案 57.53 h（不在此区间）", color=GRAY,
             fontsize=7, ha="right")
    for xi, v in zip(xq, vals):
        ax2.annotate(f"{v:.2f}", (xi, v), fontsize=7, xytext=(0, 5),
                     textcoords="offset points", ha="center")
    ax2.set_xticks(xq)
    ax2.set_xticklabels([f"P{q}" for q in qs])
    ax2.set_xlabel("分位")
    ax2.set_ylabel("$t_{\\rm end}$ / h")
    ax2.set_ylim(14, 62)
    ax2.set_title("(b) 分位区间（先验 $C_{\\rm fr}\\sim U[0.15,1.0]$，主观设定）")
    for a in (ax1, ax2):
        despine(a)
    fig.suptitle("第三问低含水率端扩散系数外推的不确定度（模型外推不确定度，不得与离散误差带相加）",
                 fontsize=9.5, y=1.03)
    save(fig, "F-38_Q3低C端外推不确定度")


# ==================================================================
# F-39 界面取法 × 网格对照（同一求解器，A–F 六例）
# ==================================================================
def f39():
    rows = rd("fig_q3_iface_grid.csv")
    d = {r["case"]: fnum(r["t_dry_h"]) for r in rows}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17 * CM, 9 * CM),
                                   gridspec_kw=dict(wspace=0.42))

    # (左) 2x2（A/F/C/E）
    x = np.arange(2)
    w = 0.34
    v_h = [d.get("A", float("nan")), d.get("F", float("nan"))]   # 调和: N20, N80
    v_i = [d.get("C", float("nan")), d.get("E", float("nan"))]   # 积分: N20, N80
    ax1.bar(x - w / 2, v_h, w, color="#E74C3C", label="两端点调和平均（错误）")
    ax1.bar(x + w / 2, v_i, w, color=GREEN, label="沿 $C$ 积分平均（采用）")
    for xi, v in zip(x - w / 2, v_h):
        ax1.text(xi, v * 1.06, f"{v:.2f}", ha="center", fontsize=7.5)
    for xi, v in zip(x + w / 2, v_i):
        ax1.text(xi, v * 1.06, f"{v:.2f}", ha="center", fontsize=7.5)
    ax1.axhline(57.5314, color=GRAY, ls="--", lw=1.0)
    ax1.set_xlim(-0.5, 2.05)
    ax1.annotate("正式答案 57.53 h", xy=(1.55, 57.5314), xytext=(2.02, 210),
                 fontsize=7, color=GRAY, ha="right",
                 arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.6))
    ax1.set_yscale("log")
    ax1.set_ylim(40, 900)
    ax1.set_xticks(x)
    ax1.set_xticklabels(["$\\Delta r=1.0$ mm\n($N=20$)", "$\\Delta r=0.25$ mm\n($N=80$)"])
    ax1.set_ylabel("$t_{\\rm end}$ / h（对数轴）")
    ax1.set_title("(a) 取法 × 网格：错误取法下加密仍不收敛")
    ax1.legend(frameon=False, loc="upper right", fontsize=7)

    # (右) 六例 A–F 单变量旁证（对数横轴）
    order = ["A", "B", "C", "D", "E", "F"]
    labels = ["A 原版", "B 仅收敛迭代", "C 仅改取法", "D 取法+迭代",
              "E 我方主力", "F 仅加密网格"]
    yv = np.arange(len(order))[::-1]
    cols = [RED, GOLD, GREEN, GREEN, GREEN, GOLD]
    ax2.barh(yv, [d[c] for c in order], color=cols, height=0.6)
    for yi, c in zip(yv, order):
        ax2.text(d[c] * 1.05, yi, f'{d[c]:.2f} h', va="center", fontsize=7)
    ax2.axvline(57.5314, color=GRAY, ls="--", lw=1.0)
    ax2.set_xscale("log")
    ax2.set_xlim(40, 1500)
    ax2.set_yticks(yv)
    ax2.set_yticklabels(labels)
    ax2.set_xlabel("$t_{\\rm end}$ / h（对数轴）")
    ax2.set_title("(b) 单变量旁证（A–F）")
    for a in (ax1, ax2):
        despine(a)
    fig.suptitle("第三问界面变系数取法与网格分辨率的对照（本文同一求解器上的对照实验）",
                 fontsize=9.5, y=1.03)
    save(fig, "F-39_Q3界面取法与网格对照")


# ==================================================================
# F-40 干燥速率曲线（双 y 轴 ＋ 内嵌分段平均速率）
# ==================================================================
def f40():
    rows = rd("fig_q3_drying_rate.csv")
    th = np.array([fnum(r["t_h"]) for r in rows])
    u = np.array([fnum(r["u_kg_per_kg_h"]) for r in rows])
    cb = np.array([fnum(r["Cbar"]) for r in rows])

    fig, (ax, axb) = plt.subplots(1, 2, figsize=(17 * CM, 9 * CM),
                                  gridspec_kw=dict(width_ratios=[2.4, 1], wspace=0.52))
    ax.axvspan(24.0, 57.5314, color="k", alpha=0.06, lw=0)
    ax.plot(th, u, color=BLUE, lw=1.3, label="干燥速率 $u=-\\mathrm{d}\\bar C/\\mathrm{d}t$")
    ax.set_yscale("log")
    ax.set_ylim(5e-4, 1.2)
    ax.set_xlim(0, 58)
    ax.set_xlabel("时间 $t$ / h")
    ax.set_ylabel("干燥速率 $u$ / (kg·kg$^{-1}$·h$^{-1}$)")

    ax2 = ax.twinx()
    ax2.plot(th, cb, color=RED, ls="--", lw=1.6, label="截面平均含水率 $\\bar C$")
    ax2.axhline(0.15, color=GRAY, ls=":", lw=1.0)
    ax2.set_ylabel("截面平均含水率 $\\bar C$ / (kg/kg)")
    ax2.set_ylim(0, 2.6)
    ax2.grid(False)
    despine(ax2)

    i24 = int(np.argmin(np.abs(th - 24.0)))
    ax.annotate(f"$u(0)={u[0]:.3f}$", xy=(th[0], u[0]), xytext=(5, 0.55),
                fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.annotate(f"$u(24\\,\\mathrm{{h}})={u[i24]:.4f}$", xy=(24, u[i24]),
                xytext=(26, 1.1e-2), fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.annotate(f"$u(t_{{\\rm end}})={u[-1]:.4f}$", xy=(th[-1], u[-1]),
                xytext=(41, 4.5e-3), fontsize=8, color=BLUE,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.8))
    ax.text(25.2, 0.42, "降速段（24–57.5 h）", fontsize=7.5, color=INK)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower left", frameon=False)
    ax.set_title("截面平均含水率与干燥速率的时间演化（速率取对数轴）")
    despine(ax)

    # 右：两段平均速率柱
    bars = [0.0980, 0.0018]
    axb.bar([0, 1], bars, color=[BLUE, GREEN], width=0.55)
    for xi, v in zip([0, 1], bars):
        axb.text(xi, v * 1.18, f"{v:.4f}", ha="center", fontsize=8)
    axb.set_yscale("log")
    axb.set_ylim(1e-3, 0.4)
    axb.set_xticks([0, 1])
    axb.set_xticklabels(["0–24 h", "24–57.5 h"])
    axb.set_ylabel("分段平均速率 / (kg·kg$^{-1}$·h$^{-1}$)")
    axb.set_title("分段平均速率（相差约 54 倍）")
    despine(axb)

    fig.suptitle("第三问干燥速率曲线（全程降速，无恒速段）", fontsize=9.5, y=1.02)
    save(fig, "F-40_Q3干燥速率曲线")


# ==================================================================
if __name__ == "__main__":
    print("Q3 参考图输出目录：", OUT)
    for fn in (f33, f34, f35, f36, f37, f38, f39, f40):
        try:
            fn()
        except Exception as e:
            print("  [FAIL]", fn.__name__, "->", repr(e))
    print("完成。")
