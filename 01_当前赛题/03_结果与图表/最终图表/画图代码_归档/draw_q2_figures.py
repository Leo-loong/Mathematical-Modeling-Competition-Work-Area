# -*- coding: utf-8 -*-
"""
Q2 图表渲染脚本（18张：F-15~F-32）
数据源：Work_Space/20_交付包/04_图表包/data/*.csv
输出：01_当前赛题/03_结果与图表/最终图表/
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
def load_csv(name):
    return np.genfromtxt(os.path.join(DATA_DIR, name), delimiter=",",
                         names=True, dtype=float, encoding="utf-8")

def load_dict(name):
    return list(csv.DictReader(open(os.path.join(DATA_DIR, name), encoding="utf-8")))

def save(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT_DIR, f"{stem}.{ext}"))
    plt.close(fig)
    print(f"  [OK] {stem}")

def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ====== F-15 变物性演化 ======


def draw_f15():
    d = load_csv("fig_q2_props.csv")
    fig, ax = plt.subplots(figsize=(9 * CM, 6 * CM))
    ax.plot(d["C"], d["rho_rel"], color=BLUE, lw=1.5, label="$\\rho/\\rho_0$ 密度")
    ax.plot(d["C"], d["cp_rel"], color=GOLD, lw=1.5, label="$c_p/c_{p,0}$ 比热容")
    ax.plot(d["C"], d["k_rel"], color=GREEN, lw=1.5, label="$k/k_0$ 热传导系数")
    ax.plot(d["C"], d["D_rel_T28"], color=RED, lw=1.5, ls="-", label="$D/D_0$ ($T$=28 ℃)")
    ax.plot(d["C"], d["D_rel_T50"], color=RED, lw=1.2, ls="--", label="$D/D_0$ ($T$=50 ℃)")
    ax.axvline(2.55, color=GRAY, ls=":", lw=1.0)
    ax.axvline(d["C"][-1], color=GRAY, ls=":", lw=1.0)
    ax.text(2.53, 0.65, "$C_0$", color=GRAY, fontsize=7, rotation=90, va="bottom")
    ax.set_xlabel("水分浓度 $C$ / (kg/kg)")
    ax.set_ylabel("相对于 $C_0$=2.55 初值的比值")
    ax.set_title("Q2 物性参数随水分浓度的演化")
    ax.legend(frameon=False, loc="upper left", fontsize=7)
    ax.set_xlim(d["C"][-1]-0.1, d["C"][0]+0.1)
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xlabel("← 低含水率                        高含水率 →", fontsize=7, color=GRAY)
    ax2.tick_params(labelbottom=False)
    despine(ax)
    layout(fig)
    save(fig, "图_F15_Q2变物性演化")


# ====== F-16 / F-17 热力图 ======
def _field_q2(name, stem, title, cbl, vmin, vmax, t_h_line, label_val):
    d = load_csv(name)
    t = d["time_s"]
    cols = [n for n in d.dtype.names if n != "time_s"]
    assert len(cols) >= 20, f"期望≥20列，实得{len(cols)}"
    r = np.linspace(0.0, 2.0, len(cols))
    Z = np.column_stack([d[n] for n in cols])
    fig, ax = plt.subplots(figsize=(9 * CM, 9 * CM))
    im = ax.pcolormesh(r, t, Z, cmap="viridis", vmin=vmin, vmax=vmax,
                       shading="auto", rasterized=True)
    cb = fig.colorbar(im, ax=ax, pad=0.03)
    cb.set_label(cbl, color=INK)
    cb.ax.tick_params(labelsize=7)
    if t_h_line:
        ax.axhline(y=t_h_line, color="white", ls="--", lw=0.8)
        ax.text(0.02, t_h_line * 0.95, f"t={label_val}", color="white",
                fontsize=7, ha="left", va="bottom")
    ax.set_xlabel("到药材中心的距离 $r$ / cm")
    ax.set_ylabel("时间 $t$ / s")
    ax.set_title(title)
    ax.grid(False)
    z0 = Z[0, 0]
    zR = Z[-1, -1]
    ax.text(1.98, t[-1] - 100, f"$t$=10800 s: {zR:.4f}",
            color="w", fontsize=7, ha="right")
    ax.text(0.02, 100, f"$t$=0: {z0:.4f}",
            color="w", fontsize=7, ha="left")
    save(fig, stem)

def draw_f16():
    _field_q2("fig_q2_field_T.csv", "图_F16_Q2温度场时空分布",
              "Q2 温度 $T(r,t)$ 时空分布（0–3 h）",
              "温度 / ℃", 28.0, 55.0, 1800.0, "1800 s (Q1结束)")

def draw_f17():
    _field_q2("fig_q2_field_C.csv", "图_F17_Q2水分浓度场时空分布",
              "Q2 水分浓度 $C(r,t)$ 时空分布（0–3 h）",
              "水分浓度 / (kg/kg)", 0.9, 2.55, 1800.0, "1800 s (Q1结束)")


# ====== F-18 关键点时程 ======
def draw_f18():
    d = load_csv("fig_q2_curves.csv")
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.plot(d["time_s"], d["T_center"], color=BLUE, lw=1.5,
            label="温度 中心 $T_0$")
    ax.plot(d["time_s"], d["T_surface"], color=GOLD, lw=1.5,
            label="温度 表面 $T_R$")
    ax.set_xlabel("时间 $t$ / s")
    ax.set_ylabel("温度 / ℃")
    ax2 = ax.twinx()
    ax2.plot(d["time_s"], d["C_center"], color=GREEN, lw=1.5,
             label="水分浓度 中心 $C_0$")
    ax2.plot(d["time_s"], d["C_surface"], color=RED, lw=1.5,
             label="水分浓度 表面 $C_R$")
    ax2.set_ylabel("水分浓度 / (kg/kg)")
    ax2.grid(False); despine(ax2)
    ax.axvline(1800, color=GRAY, ls=":", lw=1.0)
    # Q1 标注放在图例区域上方避免与曲线重叠
    ax.text(0.42, 0.95, "$\leftarrow$ Q1 窗口 (0--1800 s)",
            transform=ax.transAxes, color=GRAY, fontsize=7, va="top")
    t_end = -1
    # 数值标注集中在右上角，避开曲线
    ax.text(0.97, 0.70, f"$T_0$(3 h)={d['T_center'][t_end]:.2f} ℃",
            transform=ax.transAxes, color=BLUE, fontsize=7, ha="right")
    ax.text(0.97, 0.62, f"$T_R$(3 h)={d['T_surface'][t_end]:.2f} ℃",
            transform=ax.transAxes, color=GOLD, fontsize=7, ha="right")
    ax.text(0.97, 0.54, f"$C_0$(3 h)={d['C_center'][t_end]:.4f}",
            transform=ax.transAxes, color=GREEN, fontsize=7, ha="right")
    ax.text(0.97, 0.46, f"$C_R$(3 h)={d['C_surface'][t_end]:.4f}",
            transform=ax.transAxes, color=RED, fontsize=7, ha="right")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False)
    ax.set_title("Q2 中心与表面温度、水分浓度时程（0–3 h）")
    layout(fig)
    save(fig, "图_F18_Q2关键点时程曲线")


# ====== F-19 Q1/Q2 重叠段差异归因 ======
def draw_f19():
    d = load_csv("fig_q1q2_overlap.csv")
    t = d["t"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 10 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.25))
    ax1.plot(t, d["T_surface_q1"], color=GOLD, lw=1.5, ls="--",
             label="$T_R$ Q1 (常物性)")
    ax1.plot(t, d["T_surface_q2"], color=GOLD, lw=1.5, ls="-",
             label="$T_R$ Q2 (变物性)")
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1 与 Q2 重叠段 (0–1800 s) 差异归因")
    ax1.legend(frameon=False, fontsize=7, loc="lower right")
    despine(ax1)

    dT = d["T_surface_q2"] - d["T_surface_q1"]
    dC_diff = d["C_surface_q2"] - d["C_surface_q1"]
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.plot(t, dT, color=RED, lw=1.4, label="$\\Delta T_R$ (Q2$-$Q1)")
    ax2.plot(t, dC_diff, color=GREEN, lw=1.4, ls="-.", label="$\\Delta C_R$ (Q2$-$Q1)")
    ax2.set_xlabel("时间 $t$ / s")
    ax2.set_ylabel("偏差")
    ax2.legend(frameon=False, fontsize=7, loc="lower left")
    despine(ax2)
    ax2.text(0.03, 0.92, f"max $|\\Delta T_R|$={np.max(np.abs(dT)):.2f} ℃\nmax $|\\Delta C_R|$={np.max(np.abs(dC_diff)):.2f} kg/kg",
             transform=ax2.transAxes, fontsize=7, color=RED, va="top")
    layout(fig)
    save(fig, "图_F19_Q1Q2重叠段差异归因")


# ====== F-20 Q2 收敛性 ======
def draw_f20():
    rows = load_dict("fig_q2_gci.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 9 * CM))
    for grp, lab, mk, col, key in [("spatial", "空间 Δr", "o", BLUE, "TR"),
                               ("time", "时间 T", "^", GREEN, "T0"),
                               ("time", "时间 C", "D", RED, "CR")]:
        sel = sorted([r for r in rows if r["group"] == grp],
                     key=lambda r: float(r["delta"]))
        x = np.array([float(r["delta"]) for r in sel])
        y = np.array([float(r[key]) for r in sel])
        ax1.plot(x, y, marker=mk, ms=4, lw=1.3, color=col, label=lab)
        ref_v = float(sel[-1][key]) if float(sel[-1][key]) != 0 else 1
        rc = np.array([abs(float(r[key]) - ref_v) / abs(ref_v) for r in sel])
        ax2.plot(x, rc, marker=mk, ms=4, lw=1.3, color=col, label=lab)
    ax1.set_xscale("log"); ax2.set_xscale("log"); ax2.set_yscale("log")
    ax1.set_xlabel("步长"); ax1.set_ylabel("终态值")
    ax1.set_title("(a) 收敛趋势")
    ax2.set_xlabel("步长"); ax2.set_ylabel("相对变化")
    ax2.set_title("(b) 相对变化与参考线")
    ax2.axhline(5e-5, color=GRAY, ls="--", lw=1.0)
    ax2.text(0.13, 6e-5, "$5\\times10^{-5}$", color=GRAY, fontsize=7)
    despine(ax1); despine(ax2)
    ax1.legend(frameon=False, loc="lower left"); ax2.legend(frameon=False, loc="lower left")
    fig.suptitle("Q2 空间与时间收敛性", fontsize=10, y=1.04)
    save(fig, "图_F20_Q2收敛性")


# ====== F-21 双向耦合关系图 ======
def draw_f21():
    fig, ax = plt.subplots(figsize=(14*CM, 9*CM))
    ax.set_xlim(0, 14); ax.set_ylim(0, 9); ax.axis("off")

    # 温度场（左侧上方）
    add_box(ax, 3.5, 6.0, 5.5, 2.0,
        "温度场 $T(r,t)$\n\n热传导方程\n$\\rho c_p\\frac{\\partial T}{\\partial t}"
        "=\\frac{1}{r}\\frac{\\partial}{\\partial r}(kr\\frac{\\partial T}{\\partial r})$",
        BLUE_BG, BLUE, 7.5)

    # 水分浓度（左侧下方）
    add_box(ax, 3.5, 2.8, 5.5, 2.0,
        "水分浓度 $C(r,t)$\n\nFick 扩散方程\n$\\frac{\\partial C}{\\partial t}"
        "=\\frac{1}{r}\\frac{\\partial}{\\partial r}(Dr\\frac{\\partial C}{\\partial r})$",
        GREEN_BG, GREEN, 7.5)

    # T ↔ C 双向箭头
    add_arrow(ax, 1.0, 4.8, 1.0, 3.8, RED, 1.6)
    add_arrow(ax, 1.0, 3.8, 1.0, 4.8, RED, 1.6)
    ax.text(0.35, 4.3, "双向\n强耦合", ha="center", va="center",
            fontsize=7.5, color=RED)

    # 物性参数模块（右侧）
    add_box(ax, 10.0, 4.4, 5.8, 4.8,
        "物性参数（附录3）\n\n"
        "$\\rho=650+128C$\n"
        "$c_p=1450+2736\\frac{C}{C+1}$\n"
        "$k=0.21+0.38\\frac{C}{C+1}$\n"
        "$D=2.4{\\times}10^{-3}e^{-0.45/C}e^{-3850/T}$",
        GOLD_BG, GOLD, 7)

    # 耦合箭头：T → Prop
    add_arrow(ax, 6.25, 6.6, 7.1, 5.8, RED, 1.2)
    ax.text(6.35, 6.9, "$T$ 影响 $D$", fontsize=6.5, ha="center", color=RED)

    # C → Prop
    add_arrow(ax, 6.25, 2.5, 7.1, 3.2, RED, 1.2)
    ax.text(6.35, 2.3, "$C$ 影响 $\\rho,c_p,k,D$", fontsize=6.5, ha="center", color=RED)

    # Prop → T（反馈）
    add_arrow(ax, 7.1, 5.2, 6.25, 6.8, RED, 1.2)
    ax.text(7.0, 5.9, "$\\rho,c_p,k$ 更新", fontsize=6.5, ha="center", color=RED)

    # Prop → C（反馈）
    add_arrow(ax, 7.1, 3.5, 6.25, 3.9, RED, 1.2)
    ax.text(7.0, 3.4, "$D$ 更新", fontsize=6.5, ha="center", color=RED)

    # IMEX 标注框
    add_box(ax, 10.0, 1.5, 5.0, 0.9,
        "IMEX 交替推进\n每子步更新物性，Picard $\\omega{=}0.7$, tol${=}10^{-10}$",
        GRAY_BG, GRAY, 6)

    # Q1 对比说明
    add_box(ax, 7.0, 0.3, 13.0, 0.7,
        "Q1：单向耦合（附录2 常物性，$\\rho,c_p,k$ 常数，$D{=}D(C)$ 仅单向）  |  "
        "Q2 起：闭环双向强耦合（附录3 全变物性，IMEX 交替推进）",
        GRAY_BG, GRAY, 6.5)

    fig.suptitle("Q2 热–湿双向耦合关系", fontsize=11, y=1.02)
    layout(fig)
    save(fig, "图_F21_Q2双向耦合关系图")


# ====== F-22 IMEX 算法流程图 ======
def draw_f22():
    fig, ax = plt.subplots(figsize=(14*CM, 14*CM))
    ax.set_xlim(0, 14); ax.set_ylim(0, 14); ax.axis("off")

    xc = 7.0   # 主轴中心 x
    xr = 11.5  # 右支中心 x
    w3 = 7.0
    h  = 0.85
    hh = 0.75  # 矮节点高度

    # === 节点 ===
    add_box(ax, xc, 13.0, w3, h,
        "开始：$t=0$, $T_0=28$ ℃, $C_0=2.55$ kg/kg", RED_BG, RED, 8)
    add_box(ax, xc, 11.5, w3, h,
        "更新物性 $\\rho,c_p,k,D(C,T)$（附录3）", GOLD_BG, GOLD, 7.5)
    add_box(ax, xc, 10.2, w3, h,
        "隐式求解温度 $T^{n+1}$（三对角矩阵直接求解）", BLUE_BG, BLUE, 7.5)
    add_box(ax, xc, 8.9, w3, h,
        "重算 $D(C,T^{n+1})$（温度已更新）", GOLD_BG, GOLD, 7.5)
    add_box(ax, xc, 7.3, w3, 1.1,
        "隐式求解水分浓度 $C^{n+1}$\nPicard 迭代 ($\\omega{=}0.7$, tol${=}10^{-10}$, 最多 30 次)",
        GREEN_BG, GREEN, 7.5)
    add_box(ax, xc, 5.7, w3, hh,
        "Picard 收敛？", GOLD_BG, GOLD, 7.5)
    add_box(ax, xc, 4.3, w3, h,
        "$t$ += $\\Delta t$（时间推进）", BLUE_BG, BLUE, 7.5)
    add_box(ax, xc, 2.9, w3, hh,
        "$t < t_{\\max}$ ?", GOLD_BG, GOLD, 7.5)
    add_box(ax, xc, 1.3, w3, h,
        "结束：输出 result.xlsx", RED_BG, RED, 8)
    # Picard 右侧节点
    add_box(ax, xr, 7.3, 4.0, 0.7,
        "未收敛：继续迭代", RED_BG, RED, 6.5)

    # === 主流程直箭头 ===
    steps = [
        (13.0, h,  11.5, h),    # Init → Props
        (11.5, h,  10.2, h),    # Props → SolveT
        (10.2, h,  8.9,  h),    # SolveT → UpdateD
        (8.9,  h,  7.3,  1.1),  # UpdateD → SolveC
        (7.3,  1.1, 5.7, hh),   # SolveC → Converge
        (5.7,  hh, 4.3,  h),    # Converge → Advance
        (4.3,  h,  2.9,  hh),   # Advance → Check
        (2.9,  hh, 1.3,  h),    # Check → End
    ]
    for y1, h1, y2, h2 in steps:
        add_arrow(ax, xc, y1-h1/2, xc, y2+h2/2, INK, 0.9)

    # 标签
    ax.text(xc+0.35, 5.0, "是", fontsize=7, color=GREEN)
    ax.text(xc+0.35, 2.1, "否", fontsize=7, color=RED)

    # === Picard 侧回路（用 annotate 画弧线） ===
    ax.annotate("", xy=(xr, 7.65), xytext=(xc+w3/2, 5.7),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.text(9.5, 6.0, "否\n(≤30次)", fontsize=6, color=RED, ha="center")
    ax.annotate("", xy=(xc+w3/2, 7.85), xytext=(xr, 7.65),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0,
                              connectionstyle="arc3,rad=0.5"))

    # === 外层循环（左侧回到 Props） ===
    ax.annotate("", xy=(xc-w3/2, 11.5), xytext=(xc-w3/2, 2.9),
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.9,
                              connectionstyle="arc3,rad=-0.3"))
    ax.text(xc-w3/2-0.6, 7.2, "是\n$\\Delta t{=}1$ s\n$\\times$10800 步",
            fontsize=6.5, ha="center", va="center")

    # === 注释 ===
    ax.text(12.5, 2.5, "(Q3 用事件驱动终止)",
            fontsize=7, color=GRAY, ha="center")

    fig.suptitle("IMEX 交替推进算法流程", fontsize=11, y=1.02)
    layout(fig)
    save(fig, "图_F22_IMEX交替推进算法流程图")


# ====== F-23 3D 演化曲面 ======
def draw_f23():
    dT = load_csv("fig_q2_field_T.csv")
    dC = load_csv("fig_q2_field_C.csv")
    cols = [n for n in dT.dtype.names if n != "time_s"]
    r = np.linspace(0.0, 2.0, len(cols))
    t_all = dT["time_s"]

    # 抽样 ≤200 时间点 + 所有半径
    skip = max(1, len(t_all) // 200)
    t_idx = np.arange(0, len(t_all), skip)
    t_sampled = t_all[t_idx]

    fig = plt.figure(figsize=(14 * CM, 10 * CM))
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=22, azim=-58)

    for ti in t_idx:
        Ct = np.array([dC[cn][ti] for cn in cols])
        Tt = np.array([dT[cn][ti] for cn in cols])
        color = plt.cm.viridis(t_all[ti] / t_all[-1])
        ax.plot(r, Ct, Tt, color=color, lw=0.5, alpha=0.7)

    # 初值和终值线
    C0 = np.array([dC[cn][0] for cn in cols])
    T0 = np.array([dT[cn][0] for cn in cols])
    Cend = np.array([dC[cn][-1] for cn in cols])
    Tend = np.array([dT[cn][-1] for cn in cols])
    ax.plot(r, C0, T0, color=RED, lw=2.5, label="$t$=0")
    ax.plot(r, Cend, Tend, color=BLUE, lw=2.5, label="$t$=3 h")

    ax.set_xlabel("$r$ / cm"); ax.set_ylabel("$C$ / (kg/kg)"); ax.set_zlabel("$T$ / ℃")
    ax.set_title("Q2 三维演化曲面 $T$–$C$–$t$")
    ax.legend(fontsize=8)
    save(fig, "图_F23_Q2三维演化曲面")


# ====== F-24 相轨迹图 ======
def draw_f24():
    d = load_csv("fig_q2_curves.csv")
    fig, ax = plt.subplots(figsize=(8 * CM, 8 * CM))
    ax.plot(d["C_center"], d["T_center"], color=BLUE, lw=1.8, label="中心 $r=0$")
    ax.plot(d["C_surface"], d["T_surface"], color=RED, lw=1.8, label="表面 $r=R_0$")
    # 时间标记——用不同偏移避免重叠
    offsets = [(10, 15), (-40, -15), (-60, 10)]
    for idx, (ti, ts) in enumerate([(1800-1, 1800), (5400-1, 5400), (-1, 10800)]):
        col = GRAY
        ox, oy = offsets[idx]
        ax.annotate(f"$t$={ts} s", (d["C_center"][ti_actual := ti if ti >= 0 else -1], d["T_center"][ti_actual]),
                   textcoords="offset points", xytext=(ox, oy), fontsize=7, color=col,
                   arrowprops=dict(arrowstyle="->", color=col, lw=0.6))
    ax.set_xlabel("水分浓度 $C$ / (kg/kg) ← 方向为干燥")
    ax.set_ylabel("温度 $T$ / ℃")
    ax.set_title("Q2 温度–水分浓度相轨迹")
    ax.legend(frameon=False, loc="lower right")
    ax.invert_xaxis()  # 干燥方向从右到左
    despine(ax)
    layout(fig)
    save(fig, "图_F24_Q2温度含水率相轨迹")


# ====== F-25 全断面失水瀑布图 ======
def draw_f25():
    dC = load_csv("fig_q2_field_C.csv")
    cols = [n for n in dC.dtype.names if n != "time_s"]
    r = np.linspace(0.0, 2.0, len(cols))
    t_all = dC["time_s"]
    skip = max(1, len(t_all) // 30)
    indices = np.arange(0, len(t_all), skip)

    fig, ax = plt.subplots(figsize=(10 * CM, 6 * CM))
    # 每条曲线=一个时刻的径向C分布
    for i, ti in enumerate(indices):
        Ct = np.array([dC[cn][ti] for cn in cols])
        color = plt.cm.viridis(i / (len(indices) - 1))
        ax.plot(r, Ct, color=color, lw=0.8 if i < len(indices) - 2 else 1.5)

    # 标注初值和终值
    C0_init = np.array([dC[cols[j]][0] for j in range(len(cols))])
    C0_end = np.array([dC[cols[j]][-1] for j in range(len(cols))])
    ax.plot(r, C0_init, color=GRAY, lw=1.5, ls="--", label="初始 $t$=0")
    ax.plot(r, C0_end, color=RED, lw=2.0, label="终态 $t$=3 h")

    # 标注失水方向
    ax.annotate("失水方向 $\\downarrow$", xy=(1.0, 1.7), fontsize=9, color=INK,
                ha="center", bbox=dict(boxstyle="round", fc="white", alpha=0.8))

    ax.set_xlabel("到药材中心的距离 $r$ / cm")
    ax.set_ylabel("水分浓度 / (kg/kg)")
    ax.set_title("Q2 全断面失水演化（浅→深=时间推进）")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax.set_ylim(0.9, 2.6)
    despine(ax)
    layout(fig)
    save(fig, "图_F25_Q2全断面失水瀑布图")


# ====== F-26 灵敏度雷达图 ======
def draw_f26():
    # Q1 data
    rows_q1 = load_dict("fig_tornado_data.csv")
    d_out = {}
    for r in rows_q1:
        o = r["output"]; p = r["parameter"]; s = abs(float(r["S_norm"]))
        d_out.setdefault(o, {})[p] = s
    # Q2 data
    rows_q2 = load_dict("fig_q2_sens_S.csv")
    d_out2 = {}
    for r in rows_q2:
        o = r["output"]; p = r["parameter"]; s = abs(float(r["S_half"]))
        d_out2.setdefault(o, {})[p] = s

    # 取C_surface对比
    out_key = "C_surface"
    params_sorted = sorted(d_out[out_key].keys())
    n = len(params_sorted)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False).tolist() + [0]
    vals1 = [d_out[out_key].get(p, 0) for p in params_sorted] + [d_out[out_key].get(params_sorted[0], 0)]
    vals2 = [d_out2[out_key].get(p, 0) for p in params_sorted] + [d_out2[out_key].get(params_sorted[0], 0)]

    fig, ax = plt.subplots(figsize=(7 * CM, 7 * CM), subplot_kw=dict(polar=True))
    ax.fill(angles, vals1, alpha=0.15, color=BLUE)
    ax.plot(angles, vals1, "o-", lw=1.5, color=BLUE, ms=4, label="Q1")
    ax.fill(angles, vals2, alpha=0.15, color=GOLD)
    ax.plot(angles, vals2, "s-", lw=1.5, color=GOLD, ms=4, label="Q2")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(params_sorted, fontsize=7)
    ax.set_title("Q1 vs Q2 灵敏度结构\n($C_R$ 归一化)", fontsize=9, pad=20)
    ax.legend(fontsize=7, loc="upper right")
    save(fig, "图_F26_Q2灵敏度雷达图")


# ====== F-27 耦合强度分解图 ======
def draw_f27():
    rows = load_dict("fig_q2_coupling.csv")
    modes = [r["mode"] for r in rows]
    x = np.arange(len(modes))
    vals = [float(r["rel_CR_vs_strong"]) for r in rows]
    cols = [BLUE, GOLD, GREEN]
    fig, ax = plt.subplots(figsize=(9 * CM, 6 * CM))
    bars = ax.bar(x, vals, color=cols, width=0.5)
    for b, v, m in zip(bars, vals, modes):
        ax.text(b.get_x() + b.get_width()/2, v + (0.01 if v>=0 else -0.01),
                f"{v:+.4f}", ha="center", fontsize=8, va="bottom" if v>=0 else "top")
    ax.axhline(0, color=GRAY, lw=1.0)
    ax.set_xticks(x)
    labels = {"strong": "强耦合\n(基准)", "decoupled": "解耦\n(T=C固定)", "frozen": "冻结\n(物性常数)"}
    ax.set_xticklabels([labels.get(m, m) for m in modes], fontsize=8)
    ax.set_ylabel("相对偏差 (以强耦合 $C_R$ 为基准)")
    ax.set_title("Q2 耦合强度分解（3 h 末 $C_R$ 偏差）")
    ax.axhline(0, color=GRAY, lw=1.0)
    despine(ax)
    layout(fig)
    save(fig, "图_F27_Q2耦合强度分解图")


# ====== F-28 守恒性总账图 ======
def draw_f28():
    rows = load_dict("fig_q2_conservation.csv")
    mass_rows = [r for r in rows if r["kind"] == "mass"]
    energy_rows = [r for r in rows if r["kind"] == "energy"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16 * CM, 7 * CM))

    for ax, sub, title, unit in [(ax1, mass_rows, "质量守恒", "水分储变量 / (相对值)"),
                                  (ax2, energy_rows, "能量守恒", "能量储变量 / (相对值)")]:
        # 提取各分量
        d_items = {r["item"]: float(r["value"]) for r in sub}
        items_display = ["初始储量", "终值储量", "变化量\n(终-初)", "边界流出", "物性项",
                         "残差\n(闭合误差)"]
        vals = [d_items.get(k, 0.0) for k in ["initial", "final", "change", "flux",
                                                "property_term", "residual"]]
        # 正值蓝色，负值红色
        colors = [BLUE if v >= 0 else RED for v in vals]
        x = np.arange(len(items_display))
        ax.bar(x, vals, color=colors, width=0.55, edgecolor="white", lw=0.5)
        ax.axhline(0, color=GRAY, lw=1.0)
        for i, v in enumerate(vals):
            offset = 0.02 * max(abs(max(vals)), abs(min(vals)), 1e-10)
            ax.text(i, v + (offset if v >= 0 else -offset * 2),
                    f"{v:.2e}", ha="center", fontsize=6.5)
        ax.set_xticks(x)
        ax.set_xticklabels(items_display, fontsize=7, rotation=30, ha='right')
        ax.set_title(title, fontsize=9)
        ax.set_ylabel(unit)
        despine(ax)
        ax.grid(axis="y")
        ax.grid(axis="x", visible=False)

    # 标注闭合误差
    mass_resid = abs(float([r for r in mass_rows if r["item"] == "residual"][0]["value"]))
    mass_init = abs(float([r for r in mass_rows if r["item"] == "initial"][0]["value"]))
    energy_resid = abs(float([r for r in energy_rows if r["item"] == "residual"][0]["value"]))
    energy_init = abs(float([r for r in energy_rows if r["item"] == "initial"][0]["value"]))

    # 残差标注放在标题区（top=0.90以上），不遮挡柱子
    ax1.text(0.98, 0.10, f"闭合误差: {mass_resid/mass_init:.2e}",
             transform=ax1.transAxes, fontsize=7, ha="right", va="bottom", color=RED)
    ax2.text(0.98, 0.10, f"闭合误差: {energy_resid/energy_init:.2e}",
             transform=ax2.transAxes, fontsize=7, ha="right", va="bottom", color=RED)

    fig.suptitle("Q2 守恒性总账（质量/能量）", fontsize=10, y=1.04)
    layout(fig)
    save(fig, "图_F28_Q2守恒性总账瀑布图")


# ====== F-29 潜热对照双联图 ======
def draw_f29():
    d = load_csv("fig_q2_latent.csv")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16 * CM, 9 * CM), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1], hspace=0.22))
    ax1.plot(d["t_h"], d["dT_center"], color=BLUE, lw=1.5, label="$\\Delta T_0$ (计入−忽略)")
    ax1.plot(d["t_h"], d["dT_surface"], color=GOLD, lw=1.5, label="$\\Delta T_R$")
    ax1.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax1.set_ylabel("温度偏差 / ℃")
    ax1.set_title("潜热效应对照（计入潜热 − 忽略潜热）")
    ax1.legend(frameon=False, loc="upper right")
    despine(ax1)

    ax2.plot(d["t_h"], d["dC_center"], color=GREEN, lw=1.5, label="$\\Delta C_0$")
    ax2.plot(d["t_h"], d["dC_surface"], color=RED, lw=1.5, label="$\\Delta C_R$")
    ax2.axhline(0, color=GRAY, ls="--", lw=1.0)
    ax2.set_xlabel("时间 $t$ / h")
    ax2.set_ylabel("水分浓度偏差 / (kg/kg)")
    ax2.legend(frameon=False, loc="lower right")
    despine(ax2)

    dT_max = np.max(np.abs(d["dT_center"]))
    dC_max = np.max(np.abs(d["dC_center"]))
    note = f"3 h 末: |ΔT|≤{dT_max:.2e} ℃\n|ΔC|≤{dC_max:.2e} kg/kg"
    ax2.text(0.7, 0.12, note, transform=ax2.transAxes, fontsize=7, color=INK)
    layout(fig)
    save(fig, "图_F29_Q2潜热对照双联图")


# ====== F-30 帕累托图 ======
def draw_f30():
    rows = load_dict("fig_q2_pareto.csv")
    labels = [r["scheme"] for r in rows]
    errors = np.array([float(r["rel_err"]) for r in rows])
    times = np.array([float(r["wall_s"]) for r in rows])
    fig, ax = plt.subplots(figsize=(8 * CM, 6 * CM))
    ax.scatter(times, errors, s=60, color=BLUE, zorder=5)
    for i, lab in enumerate(labels):
        # 用不同偏移避免标注重叠
        ox = 10 if i % 2 == 0 else -50
        oy = -15 if i % 3 == 0 else 10
        ax.annotate(lab, (times[i], errors[i]),
                    textcoords="offset points", xytext=(ox, oy), fontsize=6.5,
                    zorder=10, ha="center",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=GRAY, alpha=0.8))
    # 帕累托前沿
    idx = np.argsort(times)
    front_x, front_y = [], []
    best = np.inf
    for i in idx:
        if errors[i] < best:
            front_x.append(times[i]); front_y.append(errors[i])
            best = errors[i]
    ax.plot(front_x, front_y, color=RED, lw=1.2, ls="--", marker="o", ms=4)
    ax.set_xlabel("计算耗时 / s"); ax.set_ylabel("相对误差")
    ax.set_yscale("log")
    ax.set_title("Q2 精度–效率帕累托图")
    despine(ax)
    layout(fig)
    save(fig, "图_F30_Q2精度效率帕累托图")


# ====== F-31 Sobol 热力图 ======
def draw_f31():
    rows = load_dict("fig_q2_gs_sobol.csv")
    outputs = sorted(set(r["output"] for r in rows))
    params = sorted(set(r["parameter"] for r in rows))
    n_o, n_p = len(outputs), len(params)
    matrix = np.zeros((n_p, n_o))
    for r in rows:
        pi = params.index(r["parameter"])
        oi = outputs.index(r["output"])
        matrix[pi, oi] = float(r["ST"])
    fig, ax = plt.subplots(figsize=(8 * CM, 7 * CM))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=0, vmax=np.max(matrix)*1.1, aspect="auto")
    ax.set_xticks(range(n_o)); ax.set_xticklabels(outputs, fontsize=7, rotation=30, ha="right")
    ax.set_yticks(range(n_p)); ax.set_yticklabels(params, fontsize=7)
    for i in range(n_p):
        for j in range(n_o):
            ax.text(j, i, f"{matrix[i,j]:.3f}", ha="center", va="center", fontsize=7)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("$S_T$ 总效应指数")
    ax.set_title("Q2 全局灵敏度 Sobol 热力图")
    save(fig, "图_F31_Q2全局灵敏度热力图")


# ====== F-32 自适应步长轨迹 ======
def draw_f32():
    d = load_csv("fig_q2_adaptive.csv")
    fig, ax = plt.subplots(figsize=(9 * CM, 6 * CM))
    ax.step(d["t_s"], d["h_from_s"], where="pre", color=BLUE, lw=1.5,
            label="步长 $h$ (阶梯)")
    ax.plot(d["t_s"], d["rel_change"], color=RED, lw=1.2,
            marker="o", ms=4, label="相对变化")
    ax.set_xlabel("时间 $t$ / s"); ax.set_ylabel("步长 $h$ / s")
    ax2 = ax.twinx()
    ax2.set_ylabel("相对变化")
    ax2.grid(False); despine(ax2)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("Q2 自适应步长轨迹")
    despine(ax)
    layout(fig)
    save(fig, "图_F32_Q2自适应步长轨迹图")


if __name__ == "__main__":
    figs = [
        ("F-15", draw_f15), ("F-16", draw_f16), ("F-17", draw_f17),
        ("F-18", draw_f18), ("F-19", draw_f19), ("F-20", draw_f20),
        ("F-23", draw_f23),
        ("F-24", draw_f24), ("F-25", draw_f25), ("F-26", draw_f26),
        ("F-27", draw_f27), ("F-28", draw_f28), ("F-29", draw_f29),
        ("F-30", draw_f30), ("F-31", draw_f31), ("F-32", draw_f32),
    ]
    print(f"== 开始渲染 Q2 图表（{len(figs)}张）==")
    for name, func in figs:
        try:
            func()
        except Exception as e:
            print(f"  [FAIL] {name} -> {repr(e)}")
            import traceback; traceback.print_exc()
    print("== Q2 图表渲染完成 ==")