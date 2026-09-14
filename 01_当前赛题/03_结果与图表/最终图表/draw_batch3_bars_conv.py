# -*- coding: utf-8 -*-
"""
Batch 3+4: 柱状图+收敛验证图 (16张)
图11,12,23,24,30c,31,35,40,46,05a,05b,18,30a,30b,32,38
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _fig_common_remastered import *


# ============ 柱状图 ============

def fig11():
    """图11-参数灵敏度龙卷风图（4子图）"""
    d = read_csv("fig_tornado_data.csv")
    outs = ["C_center", "C_surface", "T_center", "T_surface"]
    sub_t = ["水分浓度 中心", "水分浓度 表面", "温度 中心", "温度 表面"]
    fig, axes = plt.subplots(2, 2, figsize=(7.5, 7.0))
    for k, ax in enumerate(axes.flat):
        sel = d[d.output == outs[k]].copy()
        sel = sel.iloc[sel.S_norm.abs().argsort().values]
        ax.barh(sel.parameter, sel.S_norm, color=BLUE, height=0.6)
        ax.axvline(0, color=GRAY, ls="--", lw=0.8)
        m = max(abs(sel.S_norm).max() * 0.2, 0.15)
        ax.set_xlim(-m, sel.S_norm.max() + m)
        ax.set_title(sub_t[k], fontsize=10)
        if k >= 2:
            ax.set_xlabel("归一化灵敏度 S")
        ax.grid(True, alpha=0.3)
    fig.suptitle("Q1 参数灵敏度龙卷风图（单因素法 ±20%）", fontsize=11)
    fig.tight_layout(pad=1.5, h_pad=3.0, w_pad=2.5, rect=[0, 0, 1, 0.93])
    savefig(fig, "图11-参数灵敏度龙卷风图.pdf")


def fig12():
    """图12-数据预处理对照"""
    d = read_csv("fig_smooth_check.csv")
    vals = np.array([abs(d.dT0), abs(d.dTR), abs(d.dC0), abs(d.dCR), abs(d.field_max_T)])
    labels = [r"$\Delta T_0$ / ℃", r"$\Delta T_R$ / ℃",
              r"$\Delta C_0$", r"$\Delta C_R$", "全场T偏差 / ℃"]
    vals[vals == 0] = 1e-12
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    x = np.arange(len(labels))
    w = 0.35
    ax.bar(x - w/2, vals[:, 0], w, color=BLUE, label="MA-3平滑")
    ax.bar(x + w/2, vals[:, 1], w, color=GOLD, label="MA-5平滑")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_yscale("log")
    ax.set_ylabel("偏差绝对值（对数轴）")
    ax.set_title("Q1 边界平滑 对比 不平滑")
    ax.legend(fontsize=7)
    ax.axhline(1e-2, color=GRAY, ls="--", lw=0.8)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图12-数据预处理对照.pdf")


def fig23():
    """图23-Q2耦合强度分解图"""
    d = read_csv("fig_q2_coupling.csv")
    modes = ["强耦合(基准)", "解耦(T=C固定)", "冻结(物性常数)"]
    colors_bar = [BLUE, GOLD, GREEN]
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bars = ax.bar(modes, d.rel_CR_vs_strong, color=colors_bar, width=0.5)
    for b, v in zip(bars, d.rel_CR_vs_strong):
        ax.text(b.get_x() + b.get_width() / 2, v + (0.01 if v >= 0 else -0.03),
                f"{v:.4f}", ha="center", fontsize=7, color=INK)
    ax.set_ylabel(r"相对偏差（以强耦合 $C_R$ 为基准）")
    ax.set_title(r"Q2 耦合强度分解（3 h末 $C_R$ 偏差）")
    ax.axhline(0, color=INK, lw=0.8)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图23-Q2耦合强度分解图.pdf")


def fig24():
    """图24-Q2守恒性总账瀑布图"""
    d = read_csv("fig_q2_conservation.csv")
    label_map = {"initial": "初始储量", "final": "终值储量", "change": "变化量",
                 "flux": "边界流出", "residual": "残差", "property_term": "物性项"}
    dm = d[d.kind == "mass"].copy()
    de = d[d.kind == "energy"].copy()
    fig, axes = plt.subplots(1, 2, figsize=(8, 4.8))
    # 质量守恒
    dm_labels = [label_map.get(x, x) for x in dm.item]
    x_m = range(len(dm))
    axes[0].bar(x_m, dm.value, color=BLUE, width=0.5)
    axes[0].set_xticks(x_m)
    axes[0].set_xticklabels(dm_labels, fontsize=6, rotation=20)
    axes[0].set_ylabel("水分储变量"); axes[0].set_title("质量守恒")
    axes[0].grid(True, alpha=0.3)
    # 能量守恒
    de_labels = [label_map.get(x, x) for x in de.item]
    x_e = range(len(de))
    axes[1].bar(x_e, de.value, color=GOLD, width=0.5)
    axes[1].set_xticks(x_e)
    axes[1].set_xticklabels(de_labels, fontsize=6, rotation=20)
    axes[1].set_ylabel("能量储变量"); axes[1].set_title("能量守恒")
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("Q2 守恒性总账")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    savefig(fig, "图24-Q2守恒性总账瀑布图.pdf")


def fig30c():
    """图30c-Q3收敛性-各位置收敛情况"""
    d = read_csv("fig_q3_conv_pos.csv")
    d = d.reindex(d.rel_change.abs().sort_values().index)
    names = [s[:15].replace(" vs ", " 对比 ") for s in d.pair]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(names, d.rel_change, color=BLUE, height=0.6)
    ax.set_xlabel("相对变化")
    ax.set_title("Q3 收敛性 — 各位置收敛情况")
    ax.text(0.98, 0.02, "图示为相邻网格原始相对变化，非GCI外推",
            transform=ax.transAxes, ha="right", fontsize=6, color=GRAY)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    savefig(fig, "图30c-Q3收敛性与网格裁决-c.pdf")


def fig31():
    """图31-Q3参数灵敏度"""
    d = read_csv("fig_q3_sensitivity.csv")
    params = d.param.unique()
    S_vals = [max(abs(d[d.param == p].S)) for p in params]
    order = np.argsort(S_vals)
    math_map = {"T_inf": r"$T_\infty$", "C_inf": r"$C_\infty$",
                "h": r"$h$", "k_m": r"$k_m$", "D0": r"$D_0$"}
    ylbl = [math_map.get(p, p) for p in params]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.barh([ylbl[i] for i in order], [S_vals[i] for i in order], color=BLUE, height=0.5)
    ax.set_xlabel("灵敏度系数 S")
    ax.set_title("Q3 参数灵敏度")
    ax.axvline(0, color=GRAY, ls="--", lw=0.8)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图31-Q3参数灵敏度.pdf")


def fig35():
    """图35-Q3界面取法与网格对照"""
    d = read_csv("fig_q3_iface_grid.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    colors = [BLUE, BLUE, GREEN, GREEN, RED, GOLD][:len(d)]
    ax.bar(d.case, d.t_dry_h, color=colors, width=0.5)
    ax.set_xticklabels(d.case, fontsize=7, rotation=15)
    ax.set_ylabel(r"$t_{dry}$ / h")
    ax.set_title("Q3 界面取法×网格分辨率对照")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图35-Q3界面取法与网格对照.pdf")


def fig40():
    """图40-Q4离散误差带GCI"""
    d = read_csv("fig_q4_INV1_gci.csv")
    d["t_dry_h"] = d.t_dry_s / 3600
    kind_map = {"space": "空间", "time": "时间"}
    labels = [f"{kind_map.get(r.kind, r.kind)} N={r.N}" for _, r in d.iterrows()]
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.barh(labels, d.t_dry_h, color=BLUE, height=0.5)
    ax.set_xlabel(r"$t_{dry}$ / h")
    ax.set_title("Q4 离散误差带 (GCI)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    savefig(fig, "图40-Q4离散误差带GCI.pdf")


def fig46():
    """图46-Q4界面取法与网格对照"""
    d = read_csv("fig_q4_INV4_iface_grid.csv")
    iface_map = {"harmonic": "调和平均", "integral": "积分平均"}
    labels = [f"{iface_map.get(r.iface, r.iface)} N={r.N}" for _, r in d.iterrows()]
    colors_bar = [BLUE, BLUE, GOLD, GOLD][:len(d)]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(labels, d.t_dry_h, color=colors_bar, width=0.5)
    ax.axhline(d.t_dry_h.iloc[0], color=GRAY, ls="--", lw=0.8)
    ax.set_ylabel(r"$t_{dry}$ / h")
    ax.set_title("Q4 界面取法 × 网格对照")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图46-Q4界面取法与网格对照.pdf")


# ============ 收敛验证图 ============

def fig05a():
    """图05a-网格与时间收敛-a（终态值随步长）"""
    d = read_csv("fig_gci_data.csv")
    grps = d.groupby("group")
    spatial = grps.get_group("spatial").sort_values("delta")
    temporal_T = grps.get_group("temporal_T").sort_values("delta")

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.set_xscale("log")

    # 左轴：Ts（金线，≈36.79），量级大放左边
    ax1.plot(spatial.delta, spatial.Ts, "s-", color=GOLD, mfc=GOLD, ms=5, zorder=4)
    ax1.set_ylabel("T(R) / ℃", color=GOLD)
    ax1.tick_params(axis="y", labelcolor=GOLD)
    ax1.spines["left"].set_color(GOLD)
    ts_min, ts_max = spatial.Ts.min(), spatial.Ts.max()
    pad = (ts_max - ts_min) * 0.5
    ax1.set_ylim(ts_min - pad, ts_max + pad)

    # 右轴：Tc（蓝=空间, 绿=时间，≈33.576），窄范围拆开蓝绿线
    ax2 = ax1.twinx()
    ax2.plot(spatial.delta, spatial.Tc, "o-", color=BLUE, mfc=BLUE, ms=6, zorder=5)
    ax2.plot(temporal_T.delta, temporal_T.Tc, "^-", color=GREEN, mfc=GREEN, ms=6, zorder=5)
    ax2.set_ylabel("T(0) / ℃", color=BLUE)
    ax2.tick_params(axis="y", labelcolor=BLUE)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(BLUE)
    tc_min = min(spatial.Tc.min(), temporal_T.Tc.min())
    tc_max = max(spatial.Tc.max(), temporal_T.Tc.max())
    pad = (tc_max - tc_min) * 2.0  # 放大局部差异
    ax2.set_ylim(tc_min - pad, tc_max + pad)

    ax1.set_xlabel("步长")
    ax1.set_title("网格与时间收敛 — 终态值随步长")

    # 合并图例
    ln1 = ax1.get_lines()
    ln2 = ax2.get_lines()
    ax1.legend(ln1 + ln2,
               [r"空间 T(R)", r"空间 T(0)", r"时间 T(0)"],
               loc="upper left")
    ax1.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    savefig(fig, "图05a-网格与时间收敛-a.pdf")


def fig05b():
    """图05b-网格与时间收敛-b（收敛阶）"""
    d = read_csv("fig_gci_data.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    grps = d.groupby("group")
    for gname, s in grps:
        s = s.sort_values("delta")
        if gname == "spatial":
            y = s.Tc.values; rc = abs(np.diff(y)) / abs(y[-1])
            ax.plot(s.delta.values[1:], rc, "o-", color=BLUE, ms=4)
            y = s.Cs.values; rc = abs(np.diff(y)) / abs(y[-1])
            ax.plot(s.delta.values[1:], rc, "s-", color=GOLD, ms=4)
        elif gname == "temporal_T":
            y = s.Tc.values; rc = abs(np.diff(y)) / abs(y[-1])
            ax.plot(s.delta.values[1:], rc, "^-", color=GREEN, ms=4)
        elif gname == "temporal_C":
            y = s.Cs.values; rc = abs(np.diff(y)) / abs(y[-1])
            ax.plot(s.delta.values[1:], rc, "D-", color=RED, ms=4)
    xr = np.array([0.1, 1.25])
    ax.plot(xr, 3e-5 * xr, "--", color=GRAY)
    ax.plot(xr, 3e-6 * xr**2, "-.", color=GRAY)
    ax.text(1.1, 6e-5, "$O(h)$", color=GRAY, fontsize=7)
    ax.text(1.05, 1.2e-6, r"$O(h^2)$", color=GRAY, fontsize=7)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("步长"); ax.set_ylabel("相对偏差")
    ax.set_title("网格与时间收敛 — 收敛阶")
    ax.legend([r"空间 T(0)", r"空间 C(R)", r"时间 T(0)", r"时间 C(R)"], loc="upper left")
    ax.grid(True, which="both", alpha=0.3)
    savefig(fig, "图05b-网格与时间收敛-b.pdf")


def fig18():
    """图18-Q2收敛性"""
    d = read_csv("fig_q2_gci.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.8))
    # (a) 收敛趋势
    grps = d.groupby("group")
    for gname, s in grps:
        s = s.sort_values("delta")
        if gname == "spatial":
            axes[0].plot(s.delta, s.TR, "o-", color=BLUE, mfc=BLUE, ms=5)
        else:
            axes[0].plot(s.delta, s.T0, "^-", color=GREEN, mfc=GREEN, ms=5)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("步长"); axes[0].set_ylabel("终态值")
    axes[0].set_title("(a) 收敛趋势")
    axes[0].legend([r"空间 $\Delta r$", r"时间 $\Delta t$"], loc="best")
    axes[0].grid(True, which="both", alpha=0.3)
    # (b) 收敛阶
    for gname, s in grps:
        s = s.sort_values("delta")
        if gname == "spatial":
            y = s.TR.values; rc = abs(np.diff(y)) / abs(y[-1])
            axes[1].plot(s.delta.values[1:], rc, "o-", color=BLUE, ms=4)
        else:
            y = s.T0.values; rc = abs(np.diff(y)) / abs(y[-1])
            axes[1].plot(s.delta.values[1:], rc, "^-", color=GREEN, ms=4)
    axes[1].set_xscale("log"); axes[1].set_yscale("log")
    axes[1].set_xlabel("步长"); axes[1].set_ylabel("相对偏差")
    axes[1].set_title("(b) 收敛阶")
    axes[1].axhline(5e-5, color=GRAY, ls="--", lw=0.8)
    axes[1].grid(True, which="both", alpha=0.3)
    savefig(fig, "图18-Q2收敛性.pdf")


def fig30a():
    """图30a-Q3收敛性与网格裁决-a"""
    d = read_csv("fig_q3_conv.csv")
    s = d[d.kind == "space"].sort_values("dr_mm")
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.plot(s.dr_mm, s.C0, "o-", color=BLUE, mfc=BLUE, ms=5)
    ax.plot(s.dr_mm, s.CR, "s-", color=RED, mfc=RED, ms=5)
    ax.set_xscale("log")
    ax.set_xlabel(r"$\Delta r$ / mm"); ax.set_ylabel("水分浓度 / (kg/kg)")
    ax.set_title("Q3 收敛性 — 固定时刻浓度随步长（≈24 h）")
    ax.legend([r"$C_0$ 中心", r"$C_R$ 表面"], loc="lower right", bbox_to_anchor=(1.0, 0.3))
    ax.grid(True, alpha=0.3)
    savefig(fig, "图30a-Q3收敛性与网格裁决-a.pdf")


def fig30b():
    """图30b-Q3收敛性与网格裁决-b"""
    d = read_csv("fig_q3_conv.csv")
    s = d[d.kind == "space"].sort_values("dr_mm")
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.plot(s.dr_mm, s.rel_change, "o-", color=INK, ms=5)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.set_xticks(s.dr_mm)
    ax.set_xticklabels([f"{v:.3f}" for v in s.dr_mm], fontsize=7)
    ax.set_xlabel(r"$\Delta r$ / mm"); ax.set_ylabel("相对变化")
    ax.set_title("Q3 收敛性 — 收敛阶")
    ax.axhline(1e-5, color=GRAY, ls="--", lw=0.8)
    ax.text(0.95, 0.05, "相邻网格原始变化，非GCI外推",
            transform=ax.transAxes, ha="right", fontsize=6, color=GRAY)
    ax.grid(True, which="both", alpha=0.35)
    ax.grid(True, which="major", alpha=0.55)
    savefig(fig, "图30b-Q3收敛性与网格裁决-b.pdf")


def fig32():
    """图32-Q3离散不确定度与误差带"""
    d = read_csv("fig_q3_gci.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.5))
    s_s = d[d.kind.str.contains("space")].sort_values("dr_mm")
    s_t = d[d.kind.str.contains("time")].sort_values("h_in_s")
    axes[0].plot(s_s.dr_mm, s_s.t_end_h, "o-", color=BLUE, ms=5)
    axes[0].plot(s_t.h_in_s, s_t.t_end_h, "^-", color=GOLD, ms=5)
    axes[0].set_xlabel("空间步长 / mm, 时间步长 / s"); axes[0].set_ylabel(r"$t_{end}$ / h")
    axes[0].set_title("(a) 终态值"); axes[0].legend(["空间", "时间"], loc="best")
    axes[0].grid(True, alpha=0.3)
    rc_s = abs(np.diff(s_s.t_end_h)) / abs(s_s.t_end_h.iloc[-1])
    axes[1].plot(s_s.dr_mm.values[1:], rc_s, "o-", color=BLUE, ms=4)
    rc_t = abs(np.diff(s_t.t_end_h)) / abs(s_t.t_end_h.iloc[-1])
    axes[1].plot(s_t.h_in_s.values[1:], rc_t, "^-", color=GOLD, ms=4)
    axes[1].set_yscale("log")
    axes[1].set_xlabel("空间步长 / mm, 时间步长 / s"); axes[1].set_ylabel("相对偏差")
    axes[1].set_title("(b) 收敛趋势")
    axes[1].grid(True, alpha=0.3)
    savefig(fig, "图32-Q3离散不确定度与误差带.pdf")


def fig38():
    """图38-边界不确定度散布区间（MATLAB: 粗横线 + 黑圆点）"""
    d = read_csv("fig_q1_uq.csv")
    math_map = {"T0": r"$T_0$", "TR": r"$T_R$", "C0": r"$C_0$", "CR": r"$C_R$"}
    n = len(d)
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    bar_h = 0.25
    for i in range(n):
        # 用 Rectangle patch 替代 alpha plot，PDF 矢量可靠
        rect = plt.Rectangle((d.lo.iloc[i], i - bar_h),
                             d.hi.iloc[i] - d.lo.iloc[i], 2 * bar_h,
                             fc=BLUE_BG, ec=BLUE, lw=1.2, zorder=2)
        ax.add_patch(rect)
        # 黑圆点 = 基准值 base
        ax.plot(d.base.iloc[i], i, "o", color="black", ms=8, mfc="black", zorder=3)
    ax.set_yticks(range(n))
    ax.set_yticklabels([math_map.get(q, q) for q in d.quantity], fontsize=10)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_xlabel("数值")
    ax.set_title("Q1 边界不确定度传播区间")
    ax.grid(True, alpha=0.3, zorder=0)
    fig.tight_layout()
    savefig(fig, "图38-边界不确定度散布区间.pdf")


if __name__ == "__main__":
    print("=" * 50)
    print("Batch 3+4: 柱状图 + 收敛验证图")
    print("=" * 50)
    funcs = [fig11, fig12, fig23, fig24, fig30c, fig31, fig35, fig40, fig46,
             fig05a, fig05b, fig18, fig30a, fig30b, fig32, fig38]
    for f in funcs:
        print(f"  {f.__name__}...")
        try:
            f()
        except Exception as e:
            print(f"  [FAIL] {f.__name__}: {e}")
    print(f"\n完成: {OUTPUT_DIR}")