# -*- coding: utf-8 -*-
"""
Q1 图表渲染脚本（12张：F-03/F-07/F-08/F-09/F-10/F-11/F-12/F-13/F-14/F-41/F-42/F-43）
========================================================
数据源：Work_Space/20_交付包/04_图表包/data/*.csv
输出：01_当前赛题/03_结果与图表/最终图表/
设计语言：Nature 色板四色，Hiragino Sans GB 中文，300 DPI PDF+PNG
术语：水分浓度（非含水率）、到药材中心的距离（非径向距离）
"""
from _fig_common import *  # 共享配置：配色/字体/尺寸/layout()
import os, sys, csv
import numpy as np

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "Work_Space", "20_交付包", "04_图表包", "data"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT_DIR, exist_ok=True)

print(f"数据目录: {DATA_DIR}")
print(f"输出目录: {OUT_DIR}")
def load_csv(name):
    return np.genfromtxt(os.path.join(DATA_DIR, name), delimiter=",",
                         names=True, dtype=float, encoding="utf-8")


def load_csv_dict(name):
    rows = list(csv.DictReader(open(os.path.join(DATA_DIR, name), encoding="utf-8")))
    return rows


def save(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"{stem}.{ext}"))
    plt.close(fig)
    print(f"  [OK] {stem}")


def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ===================================================================
# F-03 烘房环境时序（双轴折线）
# ===================================================================


def draw_f03():
    d = load_csv("fig_env_timeseries.csv")
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

    # 阶段标注
    ax.axvline(8160, color=GRAY, ls=":", lw=1.0)
    ax.text(8300, 29.2, "进入平台段", color=GRAY, fontsize=7.5)
    ax.text(900, 45, "升温段\n(Q1: 0-1800 s)", fontsize=7.5, color=INK)
    ax.annotate("", xy=(1800, 48), xytext=(900, 44.5),
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))

    ax.legend(handles=[l1, l2], loc="lower right", frameon=False)
    ax.set_title("烘房环境条件时序（附件1）")
    save(fig, "图_F03_烘房环境时序")


# ===================================================================
# F-07 Q1 求解原理示意图
# ===================================================================
def draw_f07():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16 * CM, 7 * CM))

    # (a) 圆柱截面 + 边界条件
    theta = np.linspace(0, 2*np.pi, 200)
    r_circle = 1.0
    ax1.fill(np.cos(theta)*r_circle, np.sin(theta)*r_circle,
             facecolor=BLUE_BG, edgecolor=BLUE, lw=1.5, alpha=0.7)
    ax1.set_aspect("equal")
    ax1.set_xlim(-1.4, 1.4)
    ax1.set_ylim(-1.4, 1.4)
    # 中心点
    ax1.plot(0, 0, "o", color=INK, ms=6)
    ax1.text(0.05, -0.15, "$r=0$\n$\\partial_r T=0,\\;\\partial_r C=0$",
             fontsize=6.5, ha="left", va="top")
    # 表面标注
    ax1.annotate("", xy=(1, 0), xytext=(1.3, 0.3),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax1.text(1.25, 0.35, "表面\n$-k\\partial_r T=h(T_R-T_\\infty)$\n$-D\\partial_r C=k_m(C_R-C_\\infty)$",
             fontsize=6.5, color=RED, ha="left")
    # 半径标注
    ax1.annotate("$R_0=2$ cm", xy=(0.5, 0), xytext=(0.3, -0.85),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=0.8),
                fontsize=7, ha="center")
    # 热流方向
    for x0, y0 in [(0.6, 0.35), (0.35, 0.6), (-0.35, 0.6), (-0.6, 0.35)]:
        ax1.arrow(x0*0.7, y0*0.7, -x0*0.1, -y0*0.1,
                  head_width=0.06, color=GOLD, alpha=0.7)
    ax1.text(0.25, 0.3, "热/湿流\n(外→内)", fontsize=6, color=GOLD, ha="center")
    ax1.set_title("(a) 圆柱截面与边界", fontsize=9, pad=10)
    ax1.axis("off")

    # (b) 径向控制体
    # 画外圆
    ax2.add_patch(plt.Circle((0, 0), 1, fill=False, ec=BLUE, lw=1.2))
    # 画径向线
    for ang in [0, np.pi/6, 2*np.pi/6, 3*np.pi/6, 4*np.pi/6, 5*np.pi/6]:
        ax2.plot([0, np.cos(ang)], [0, np.sin(ang)], color=GRAY, lw=0.3)
    # 画格子环
    for r_level in [0.25, 0.5, 0.75]:
        ax2.add_patch(plt.Circle((0, 0), r_level, fill=False, ec=GRAY, lw=0.5, ls="--"))
    # 标注控制体
    ax2.fill_between([0.08, 0.12], -0.02, 0.02, color=GREEN, alpha=0.5)
    ax2.text(-0.2, 0.2, "$\\Delta r=0.25$ mm\n$N=80$ 区间", fontsize=6.5, ha="center")
    ax2.text(1.1, 0, "$r=R_0=2$ cm", fontsize=6.5, color=BLUE, va="center")
    ax2.set_aspect("equal")
    ax2.set_xlim(-1.3, 1.5)
    ax2.set_ylim(-1.3, 1.3)
    ax2.set_title("(b) 径向控制体网格", fontsize=9, pad=10)
    ax2.axis("off")

    # (c) 时空离散网格
    nr, nt = 6, 8
    for i in range(nr+1):
        ax3.axhline(i, color=GRAY, lw=0.4, ls="--")
    for j in range(nt+1):
        ax3.axvline(j, color=GRAY, lw=0.4, ls="--")

    # 三点示意
    for i in [1, 3, 5]:
        for j in [1, 3, 6]:
            ax3.plot(j, i+0.5, "o", color=BLUE, ms=3, alpha=0.5)

    ax3.arrow(3.5, 7, 3, 0, head_width=0.15, head_length=0.3, color=RED, lw=1.2)
    ax3.text(5.0, 7.2, "时间推进→", fontsize=7, color=RED, ha="center")

    ax3.set_xlim(-0.2, 9.5)
    ax3.set_ylim(-0.3, 8.5)
    ax3.text(8.5, 0.8, "△t=1 s (输出)\n子步 1/32 s", fontsize=6.5, ha="center")
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_xlabel("径向 $r$ (0→$R_0$)", fontsize=7)
    ax3.set_title("(c) 时空离散与推进", fontsize=9, pad=10)
    despine(ax3)
    for sp in ["left", "bottom"]:
        ax3.spines[sp].set_visible(False)

    fig.suptitle("Q1 求解原理示意图（圆柱药材热湿耦合离散）", fontsize=11, y=1.02)
    layout(fig)
    save(fig, "图_F07_Q1求解原理示意图")


# ===================================================================
# F-08 / F-09 场分布热力图
# ===================================================================
def _draw_field(csv_name, stem, title, cbl, vmin, vmax, t_end_label):
    d = load_csv(csv_name)
    t = d["time_s"]
    cols = [n for n in d.dtype.names if n != "time_s"]
    assert len(cols) == 21, f"期望21列，实得{len(cols)}"
    r = np.linspace(0.0, 2.0, len(cols))
    Z = np.column_stack([d[n] for n in cols])

    fig, ax = plt.subplots(figsize=(9 * CM, 9 * CM))
    im = ax.pcolormesh(r, t, Z, cmap="viridis", vmin=vmin, vmax=vmax,
                       shading="auto", rasterized=True)
    cb = fig.colorbar(im, ax=ax, pad=0.03)
    cb.set_label(cbl, color=INK)
    cb.ax.tick_params(labelsize=7)
    cb.outline.set_edgecolor(INK)
    cb.outline.set_linewidth(0.5)

    ax.set_xlabel("到药材中心的距离 $r$ / cm")
    ax.set_ylabel("时间 $t$ / s")
    ax.set_title(title)
    ax.grid(False)

    zR_end = Z[-1, -1]
    ax.text(1.98, 1780, f"$t$=1800 s 表面 {zR_end:.4f}",
            color="w", fontsize=7, ha="right", va="top")
    ax.text(0.02, 60, f"$t$=0 初值 {Z[0,0]:.4f}",
            color="w", fontsize=7, ha="left", va="bottom")

    save(fig, stem)


def draw_f08():
    _draw_field("fig_q1_field_T.csv", "图_F08_Q1温度场时空分布",
                "Q1 温度 $T(r,t)$ 时空分布",
                "温度 / ℃", 28.0, 37.0, "1800 s")


def draw_f09():
    _draw_field("fig_q1_field_C.csv", "图_F09_Q1水分浓度场时空分布",
                "Q1 水分浓度 $C(r,t)$ 时空分布",
                "水分浓度 / (kg/kg)", 1.5, 2.55, "1800 s")


# ===================================================================
# F-10 关键点时程曲线（双纵轴）
# ===================================================================
def draw_f10():
    d = load_csv("fig_q1_curves.csv")
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))

    ax.plot(d["time_s"], d["T_center"], color=BLUE, lw=1.6,
            marker="o", ms=3, markevery=300, label="温度 中心 $T_0$")
    ax.plot(d["time_s"], d["T_surface"], color=GOLD, lw=1.6,
            marker="^", ms=3, markevery=300, label="温度 表面 $T_R$")
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("温度 / ℃")
    ax.set_ylim(27.4, 39.4)

    ax2 = ax.twinx()
    ax2.plot(d["time_s"], d["C_center"], color=GREEN, lw=1.6,
             marker="s", ms=3, markevery=300, label="水分浓度 中心 $C_0$")
    ax2.plot(d["time_s"], d["C_surface"], color=RED, lw=1.6,
             marker="D", ms=3, markevery=300, label="水分浓度 表面 $C_R$")
    ax2.set_ylabel("水分浓度 / (kg/kg)")
    ax2.set_ylim(1.38, 2.80)
    ax2.grid(False)
    despine(ax2)

    # 关键数值标注
    t_end = -1
    ax.text(0.30, 0.96, f"$T_0$(1800 s)={d['T_center'][t_end]:.4f} ℃",
            transform=ax.transAxes, color=BLUE, fontsize=7, va="top")
    ax.text(0.30, 0.885, f"$T_R$(1800 s)={d['T_surface'][t_end]:.4f} ℃",
            transform=ax.transAxes, color=GOLD, fontsize=7, va="top")
    ax.text(0.40, 0.04, f"$C_0$(1800 s)={d['C_center'][t_end]:.4f}",
            transform=ax.transAxes, color=GREEN, fontsize=7, va="bottom")
    ax.text(0.40, 0.11, f"$C_R$(1800 s)={d['C_surface'][t_end]:.4f}",
            transform=ax.transAxes, color=RED, fontsize=7, va="bottom")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center left", frameon=False,
              bbox_to_anchor=(0.22, 0.50))
    ax.set_title("Q1 中心与表面温度、水分浓度时程曲线")
    layout(fig)
    save(fig, "图_F10_Q1关键点时程曲线")


# ===================================================================
# F-11 解析级数解对拍
# ===================================================================
def draw_f11():
    rows = load_csv_dict("fig_series_check.csv")
    sel = [r for r in rows if r["case"] == "E2a_dr0.25mm"]
    t = np.array([float(r["t"]) for r in sel])
    y_num = np.array([float(r["Tc_num"]) for r in sel])
    y_ana = np.array([float(r["Tc_ana"]) for r in sel])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 9 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.22))

    ax1.plot(t, y_num, color=BLUE, lw=1.6, marker="o", ms=3, label="数值解 (0.25 mm)")
    ax1.plot(t, y_ana, color=GOLD, lw=1.2, ls="--", marker="^", ms=3,
             label="解析级数解（常边界特例）")
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1 温度解析对拍（解析级数解 vs 数值解，$r=0$）")
    ax1.legend(frameon=False, loc="lower right")
    despine(ax1)

    dev = y_num - y_ana
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.plot(t, dev, color=RED, lw=1.4, marker="D", ms=3)
    ax2.set_xlabel("时间 $t$ / s")
    ax2.set_ylabel("偏差 $\\Delta$ / ℃")
    ax2.set_ylim(-6e-3, 6e-3)
    i_max = int(np.argmax(np.abs(dev)))
    ax2.annotate(f"max $|\\Delta|$={np.max(np.abs(dev)):.2e} ℃",
                 xy=(t[i_max], dev[i_max]),
                 xytext=(0.35, 0.78), textcoords="axes fraction",
                 fontsize=7, color=RED,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    despine(ax2)
    layout(fig)
    save(fig, "图_F11_解析级数解对拍")


# ===================================================================
# F-12 独立实现互验
# ===================================================================
def draw_f12():
    d = load_csv("fig_e3_check.csv")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 9 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.22))

    ax1.plot(d["t"], d["Ts_main"], color=BLUE, lw=1.6, marker="o", ms=4,
             label="主力解 (全隐式)")
    ax1.plot(d["t"], d["Ts_expl"], color=GOLD, lw=1.2, ls="--", marker="^", ms=4,
             label="独立实现 (显式 FTCS)")
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1 独立实现互验（表面温度，$t\\leq3$ h）")
    ax1.legend(frameon=False, loc="upper right")
    despine(ax1)

    dev = d["Ts_main"] - d["Ts_expl"]
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.plot(d["t"], dev, color=RED, lw=1.4, marker="D", ms=4)
    ax2.set_xlabel("时间 $t$ / s")
    ax2.set_ylabel("偏差 $\\Delta T$ / ℃")
    i_max = int(np.argmax(np.abs(dev)))
    ax2.annotate(f"max $|\\Delta T|$={np.max(np.abs(dev)):.2e} ℃",
                 xy=(d["t"][i_max], dev[i_max]),
                 xytext=(0.05, 0.72), textcoords="axes fraction", fontsize=7,
                 color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    despine(ax2)
    layout(fig)
    save(fig, "图_F12_独立实现互验")


# ===================================================================
# F-13 参数灵敏度龙卷风图（2×2子图）
# ===================================================================
def draw_f13():
    rows = load_csv_dict("fig_tornado_data.csv")
    outs = ["T_center", "T_surface", "C_center", "C_surface"]
    nice_labels = {
        "T_center": "温度 中心",
        "T_surface": "温度 表面",
        "C_center": "水分浓度 中心",
        "C_surface": "水分浓度 表面"
    }

    fig, axes = plt.subplots(2, 2, figsize=(16 * CM, 10 * CM))
    for ax, o in zip(axes.ravel(), outs):
        sel = [r for r in rows if r["output"] == o]
        sel.sort(key=lambda r: abs(float(r["S_norm"])))
        names = [r["parameter"] for r in sel]
        vals = np.array([float(r["S_norm"]) for r in sel])
        y = np.arange(len(names))
        cols = [BLUE if v >= 0 else RED for v in vals]
        ax.barh(y, vals, color=cols, height=0.6)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=7)
        ax.axvline(0, color=GRAY, ls="--", lw=1.0)
        ax.set_title(nice_labels[o], fontsize=8)
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
        mx = max(abs(min(vals)), abs(max(vals)), 0.1)
        ax.set_xlim(-mx * 1.3, mx * 1.3)
        for yi, v in zip(y, vals):
            offset = mx * 0.12
            ax.text(v + (offset if v >= 0 else -offset), yi,
                    f"{v:+.3f}", va="center",
                    ha="left" if v >= 0 else "right", fontsize=6.5)
        despine(ax)
    fig.supxlabel("归一化灵敏度系数 $S_{norm}$", fontsize=9)
    fig.suptitle("Q1 参数灵敏度龙卷风图（OAT ±20%）", fontsize=10, y=1.04)
    layout(fig)
    save(fig, "图_F13_参数灵敏度龙卷风图")


# ===================================================================
# F-14 数据预处理对照
# ===================================================================
def draw_f14():
    rows = load_csv_dict("fig_smooth_check.csv")
    groups = ["dT0", "dTR", "dC0", "dCR", "field_max_T"]
    labs = ["$\\Delta T_0$\n/ ℃", "$\\Delta T_R$\n/ ℃",
            "$\\Delta C_0$\n/ (kg/kg)", "$\\Delta C_R$\n/ (kg/kg)",
            "全场最大\n$T$偏差 / ℃"]
    FLOOR = 1e-9

    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    x = np.arange(len(groups))
    w = 0.36
    for k, (r, c) in enumerate(zip(rows, [BLUE, GOLD])):
        v = [max(abs(float(r[g])), FLOOR) for g in groups]
        b = ax.bar(x + (k - 0.5) * w, v, w, color=c, label=r["case"])
        for xi, vi in zip(b, v):
            ax.text(xi.get_x() + xi.get_width() / 2, vi * 1.35,
                    "≈0" if vi <= FLOOR else f"{vi:.1e}",
                    ha="center", fontsize=6, color=INK)

    ax.set_yscale("log")
    ax.set_ylim(1e-9, 1e-0)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=7)
    ax.set_ylabel("偏差绝对值 (对数轴)")
    ax.axhline(1e-2, color=GRAY, ls="--", lw=1.0)
    ax.text(len(groups) - 0.45, 1.5e-2, "$10^{-2}$ 参考", color=GRAY, fontsize=7, ha="right")
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Q1 边界平滑 vs 不平滑对照（基准=不平滑）")
    despine(ax)
    layout(fig)
    save(fig, "图_F14_数据预处理对照")


# ===================================================================
# F-41 自适应步长轨迹（阶梯图，对数Y）
# ===================================================================
def draw_f41():
    d = load_csv("fig_q1_stepsize.csv")
    fig, ax = plt.subplots(figsize=(9 * CM, 6 * CM))
    ax.step(d["t_s"], d["h_next_s"], where="post", color=BLUE, lw=1.2)
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("步长 $h$ / s")
    ax.set_yscale("log")
    ax.set_title("Q1 误差驱动自适应步长轨迹（阶梯图，对数纵轴）")
    ax.text(0.55, 0.92, "后期步长稳定≈1 s\n反证时间离散误差已消除",
            transform=ax.transAxes, fontsize=7, color=INK,
            va="top", bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    despine(ax)
    layout(fig)
    save(fig, "图_F41_自适应步长轨迹")


# ===================================================================
# F-42 边界不确定度区间标尺图
# ===================================================================
def draw_f42():
    rows = []
    with open(os.path.join(DATA_DIR, "fig_q1_uq.csv"), encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            rows.append(line)
    header = rows[0].split(",")
    data_rows = []
    for r in rows[1:]:
        vals = r.split(",")
        row = {}
        for i in range(len(header)):
            k = header[i].strip()
            v = vals[i].strip()
            if k == "quantity":
                row[k] = v
            else:
                row[k] = float(v)
        data_rows.append(row)
    n = len(data_rows)
    bases = [data_rows[i]["base"] for i in range(n)]
    los   = [data_rows[i]["lo"] for i in range(n)]
    his   = [data_rows[i]["hi"] for i in range(n)]
    qnames = ["$T_0$ 中心温度", "$T_R$ 表面温度",
              "$C_0$ 中心水分浓度", "$C_R$ 表面水分浓度"]
    units = ["℃", "℃", "kg/kg", "kg/kg"]

    # 温度子图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10 * CM, 9 * CM))
    # 噪声传播样本量
    n_sample = 40

    for idx, labels, ax, qs, u in [(0, qnames[:2], ax1, [0, 1], units[:2]),
                                   (1, qnames[2:], ax2, [2, 3], units[2:])]:
        for j, qi in enumerate(qs):
            y0 = -j
            ax.barh(y0, his[qi] - los[qi], left=los[qi], height=0.5,
                    color=BLUE if qi < 2 else GREEN, alpha=0.25)
            ax.plot(bases[qi], y0, "o", color=INK, ms=6, zorder=5)
            ax.axvline(bases[qi], ymin=y0 - 0.25, ymax=y0 + 0.25,
                       color=INK, ls="--", lw=0.8)
            ax.text(los[qi], y0 + 0.35, f"{los[qi]:.6f}", fontsize=6, va="bottom")
            ax.text(his[qi], y0 + 0.35, f"{his[qi]:.6f}", fontsize=6, va="bottom")
            ax.text(bases[qi], y0 - 0.4, f"{bases[qi]:.6f}", fontsize=6.5,
                    ha="center", va="top", color=INK, fontweight="bold")
        ax.set_yticks([-j for j in range(len(qs))])
        ax.set_yticklabels(labels, fontsize=8)
        ax.set_xlabel(f"数值 / {u[0]}")
        ax.set_ylim(-len(qs) + 0.5, 0.8)
        ax.grid(axis="x")
        despine(ax)

    ax1.set_title(f"Q1 边界不确定度传播区间（$n$={n_sample} 严格样本，$t$=1800 s）", fontsize=9)
    layout(fig)
    save(fig, "图_F42_边界不确定度散布区间")


# ===================================================================
# F-43 全局灵敏度与OAT并置
# ===================================================================
def draw_f43():
    d = load_csv("fig_q1_gs.csv")
    # 列: output, param, mu_star, sigma, S1, ST
    outputs = []
    all_rows = load_csv_dict("fig_q1_gs.csv")
    # 取第一个output
    out_names = sorted(set(r["output"] for r in all_rows))
    out0 = out_names[0]

    sel = [r for r in all_rows if r["output"] == out0]
    params = [r["param"] for r in sel]
    mu_star = np.array([float(r["mu_star"]) for r in sel])
    sigma = np.array([float(r["sigma"]) for r in sel])
    S1 = np.array([float(r["S1"]) for r in sel])
    ST = np.array([float(r["ST"]) for r in sel])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 7 * CM))

    # 左：Morris mu*-sigma 散点（交错偏移避免标注重叠）
    ax1.scatter(mu_star, sigma, s=50, color=INK, zorder=5)
    for i, p in enumerate(params):
        if i % 2 == 0:
            ax1.annotate(p, (mu_star[i], sigma[i]),
                         textcoords="offset points", xytext=(10+i*2, 6), fontsize=7)
        else:
            ax1.annotate(p, (mu_star[i], sigma[i]),
                         textcoords="offset points", xytext=(-35+i*2, -8), fontsize=7)
    ax1.set_xlabel("$\\mu^*$ (均值影响)")
    ax1.set_ylabel("$\\sigma$ (非线性/交互)")
    ax1.set_title("Morris 全局灵敏度")
    ax1.axhline(0, color=GRAY, ls="--", lw=0.8)
    despine(ax1)
    ax1.grid(True, axis="both")

    # 右：Sobol S1 vs ST 分组条形
    x = np.arange(len(params))
    w = 0.35
    ax2.bar(x - w/2, S1, w, color=BLUE, label="$S_1$ (一阶)")
    ax2.bar(x + w/2, ST, w, color=GOLD, label="$S_T$ (总效应)")
    # 画交互差值连线
    for i in range(len(params)):
        ax2.plot([x[i], x[i]], [S1[i], ST[i]], color=RED, lw=1.2, marker="")

    ax2.set_xticks(x)
    ax2.set_xticklabels(params, fontsize=7)
    ax2.set_ylabel("灵敏度指数")
    ax2.set_title("Sobol 全局灵敏度 ($S_1$ vs $S_T$)")
    ax2.legend(frameon=False, loc="upper right")
    ax2.grid(axis="y")
    ax2.grid(axis="x", visible=False)
    despine(ax2)

    # 注意S1可能为负（数值噪声），如实保留
    if np.any(S1 < 0):
        fig.text(0.5, 0.01, "注意：$S_1$ 负值属采样噪声（≈0），如实保留未截断",
                 ha="center", fontsize=7, color=INK)

    fig.suptitle("Q1 全局灵敏度（Morris + Sobol）与 OAT 对照", fontsize=10, y=1.04)
    layout(fig)
    save(fig, "图_F43_全局灵敏度与OAT并置")


# ===================================================================
if __name__ == "__main__":
    print("== 开始渲染 Q1 图表（12张）==")
    fig_funcs = [
        ("F-03", draw_f03),
        ("F-08", draw_f08),
        ("F-09", draw_f09),
        ("F-10", draw_f10),
        ("F-11", draw_f11),
        ("F-12", draw_f12),
        ("F-13", draw_f13),
        ("F-14", draw_f14),
        ("F-41", draw_f41),
        ("F-42", draw_f42),
        ("F-43", draw_f43),
    ]
    for name, func in fig_funcs:
        try:
            func()
        except Exception as e:
            print(f"  [FAIL] {name} -> {repr(e)}")
            import traceback; traceback.print_exc()
    print("== Q1 图表渲染完成 ==")