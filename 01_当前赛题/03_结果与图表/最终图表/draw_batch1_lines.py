# -*- coding: utf-8 -*-
"""
Batch 1: 折线/双Y轴/简单曲线 (16张)
图03,04,08,13,16,21,22,25,28,29,36,37,44,45,41a,41b
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _fig_common_remastered import *


def fig03():
    """图03-烘房环境时序（双Y轴）"""
    d = read_csv("fig_env_timeseries.csv")
    fig, ax1 = plt.subplots(figsize=(5.8, 3.8))
    ax1.plot(d.t_s, d.T_env_C, color=GOLD, lw=1.5)
    ax1.set_ylabel("烘房温度 / ℃", color=GOLD)
    ax1.tick_params(axis="y", labelcolor=GOLD)
    ax1.spines["left"].set_color(GOLD)
    ax2 = ax1.twinx()
    ax2.plot(d.t_s, d.C_env_kgkg, "--", color=GREEN, lw=1.5)
    ax2.set_ylabel("烘房水分浓度 / (kg/kg)", color=GREEN)
    ax2.tick_params(axis="y", labelcolor=GREEN)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(GREEN)
    ax1.set_ylim(24, 54)
    ax2.set_ylim(0.00, 0.062)
    ax1.set_xlabel("时间 t / s")
    ax1.set_title("烘房环境条件时序（附件1）")
    ax1.axvline(8160, color=GRAY, ls=":", lw=0.8)
    ax1.text(8400, 29.5, "进入平台段", color=GRAY, fontsize=7)
    ax1.text(900, 44, "升温段(Q1)", color=INK, fontsize=7)
    ax1.grid(True, alpha=0.3)
    savefig(fig, "图03-烘房环境时序.pdf")


def fig04():
    """图04-药材半径收缩曲线"""
    d = read_csv("fig_q4_shrinkage.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(d.t_h, d.R_cm, color=BLUE, lw=1.8)
    ax.set_xlabel("时间 t / h"); ax.set_ylabel("药材半径 R / cm")
    ax.set_title("药材半径随干燥时间收缩（附件2）")
    ax.text(1, d.R_cm.iloc[0] - 0.05, "$R_0$=2.00 cm", fontsize=7)
    ax.text(d.t_h.iloc[-1] * 0.55, d.R_cm.iloc[-1] + 0.04,
            f"R={d.R_cm.iloc[-1]:.4f} cm", color=RED, fontsize=7)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图04-药材半径收缩曲线.pdf")


def fig08():
    """图08-Q1关键点时程曲线（双Y轴）"""
    d = read_csv("fig_q1_curves.csv")
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(d.time_s, d.T_center, color=BLUE, lw=1.5)
    ax1.plot(d.time_s, d.T_surface, "--", color=GOLD, lw=1.5)
    ax1.set_ylabel("温度 / ℃", color="#2166AC")
    ax1.tick_params(axis="y", labelcolor="#2166AC")
    ax1.spines["left"].set_color("#2166AC")
    ax1.set_ylim(27.4, 39.4)
    ax2 = ax1.twinx()
    ax2.plot(d.time_s, d.C_center, color=GREEN, lw=1.5)
    ax2.plot(d.time_s, d.C_surface, "--", color=RED, lw=1.5)
    ax2.set_ylabel("水分浓度 / (kg/kg)", color=GREEN)
    ax2.tick_params(axis="y", labelcolor=GREEN)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(GREEN)
    ax2.set_ylim(1.38, 2.80)
    ax1.set_xlabel("时间 t / s")
    ax1.set_title("Q1 中心与表面温度、水分浓度时程曲线")
    t_end = d.time_s.iloc[-1]
    dx = t_end * 0.01
    ax1.text(t_end + dx, d.T_center.iloc[-1], f"T中心={d.T_center.iloc[-1]:.2f}",
             color=BLUE, fontsize=5, va="center")
    ax1.text(t_end + dx, d.T_surface.iloc[-1], f"T表面={d.T_surface.iloc[-1]:.2f}",
             color=GOLD, fontsize=5, va="center")
    ax2.text(t_end + dx, d.C_center.iloc[-1], f"C中心={d.C_center.iloc[-1]:.4f}",
             color=GREEN, fontsize=5, va="center")
    ax2.text(t_end + dx, d.C_surface.iloc[-1], f"C表面={d.C_surface.iloc[-1]:.4f}",
             color=RED, fontsize=5, va="center")
    ax1.set_xlim(left=-50, right=t_end * 1.12)
    ax1.grid(True, alpha=0.3)
    savefig(fig, "图08-Q1关键点时程曲线.pdf")


def fig13():
    """图13-Q2变物性演化"""
    d = read_csv("fig_q2_props.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(d.C, d.rho_rel, color=BLUE, lw=1.5)
    ax.plot(d.C, d.cp_rel, color=GOLD, lw=1.5)
    ax.plot(d.C, d.k_rel, color=GREEN, lw=1.5)
    ax.plot(d.C, d.D_rel_T28, color=RED, lw=1.5)
    ax.plot(d.C, d.D_rel_T50, "--", color=RED, lw=1.2)
    ax.axvline(d.C.iloc[0], color=GRAY, ls=":", lw=0.8)
    ax.axvline(d.C.iloc[-1], color=GRAY, ls=":", lw=0.8)
    ax.set_xlabel("水分浓度 C / (kg/kg)")
    ax.set_ylabel("相对初值（C0=2.55处=1）")
    ax.set_title("Q2 物性参数随水分浓度的演化")
    ax.legend([r"$\rho/\rho_0$", r"$c_p/c_{p,0}$", r"$k/k_0$",
               r"$D/D_0$(T=28℃)", r"$D/D_0$(T=50℃)"], loc="upper right",
              bbox_to_anchor=(0.85, 0.85), fontsize=7)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图13-Q2变物性演化.pdf")


def fig16():
    """图16-Q2关键点时程曲线（双Y轴）"""
    d = read_csv("fig_q2_curves.csv")
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(d.time_s, d.T_center, color=BLUE, lw=1.5)
    ax1.plot(d.time_s, d.T_surface, "--", color=GOLD, lw=1.5)
    ax1.set_ylabel("温度 / ℃", color="#2166AC")
    ax1.tick_params(axis="y", labelcolor="#2166AC")
    ax1.spines["left"].set_color("#2166AC")
    ax2 = ax1.twinx()
    ax2.plot(d.time_s, d.C_center, color=GREEN, lw=1.5)
    ax2.plot(d.time_s, d.C_surface, "--", color=RED, lw=1.5)
    ax2.set_ylabel("水分浓度 / (kg/kg)", color=GREEN)
    ax2.tick_params(axis="y", labelcolor=GREEN)
    ax2.spines["left"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(GREEN)
    ax1.axvline(1800, color=GRAY, ls=":", lw=0.8)
    ax1.text(2000, 30, "Q1结束", color=GRAY, fontsize=7)
    ax1.set_xlabel("时间 t / s")
    ax1.set_title("Q2 中心与表面温度、水分浓度时程（0-3 h）")
    t_end = d.time_s.iloc[-1]
    dx = t_end * 0.008
    ax1.text(t_end + dx, d.T_center.iloc[-1] - 2, f"T中心={d.T_center.iloc[-1]:.1f}",
             color=BLUE, fontsize=5, va="center")
    ax1.text(t_end + dx, d.T_surface.iloc[-1] + 2, f"T表面={d.T_surface.iloc[-1]:.1f}",
             color=GOLD, fontsize=5, va="center")
    ax2.text(t_end + dx, d.C_center.iloc[-1], f"C中心={d.C_center.iloc[-1]:.4f}",
             color=GREEN, fontsize=5, va="center")
    ax2.text(t_end + dx, d.C_surface.iloc[-1], f"C表面={d.C_surface.iloc[-1]:.4f}",
             color=RED, fontsize=5, va="center")
    ax1.set_xlim(left=-50, right=t_end * 1.12)
    ax1.grid(True, alpha=0.3)
    savefig(fig, "图16-Q2关键点时程曲线.pdf")


def fig21():
    """图21-Q2温度含水率相轨迹"""
    d = read_csv("fig_q2_curves.csv")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(d.C_center, d.T_center, color=BLUE, lw=1.8)
    ax.plot(d.C_surface, d.T_surface, color=RED, lw=1.8)
    marks = [1800, 5400, 10800]
    # x轴反转，往右=减小C值，用负偏移
    offsets = {1800: (-0.04, 0.5), 5400: (-0.04, -0.8), 10800: (0.02, 0.5)}
    for mt in marks:
        i = (d.time_s - mt).abs().idxmin()
        ax.plot(d.C_center[i], d.T_center[i], "o", color=GRAY, ms=5, mfc=GRAY)
        ax.plot(d.C_surface[i], d.T_surface[i], "s", color=GRAY, ms=5, mfc=GRAY)
        dx, dy = offsets[mt]
        ax.text(d.C_center[i] + dx, d.T_center[i] + dy, f"t={mt}s", fontsize=7)
    ax.set_xlabel("水分浓度 C / (kg/kg)")
    ax.set_ylabel("温度 T / ℃")
    ax.set_title("Q2 温度-水分浓度相轨迹")
    ax.legend(["中心 r=0", "表面 r=R0"], loc="best")
    ax.invert_xaxis()
    ax.grid(True, alpha=0.3)
    savefig(fig, "图21-Q2温度含水率相轨迹.pdf")


def fig22():
    """图22-Q2全断面失水瀑布图"""
    t_all, Z = read_matrix("fig_q2_field_C.csv")
    r = np.linspace(0, 2, Z.shape[1])
    skip = max(1, len(t_all) // 30)
    idx = range(0, len(t_all), skip)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    n = len(idx)
    for j, k in enumerate(idx):
        col = j / n
        ax.plot(r, Z[k, :], color=(col, 0.5 * (1 - col), 0.8 * (1 - col)), lw=1)
    ax.plot(r, Z[0, :], "--", color=GRAY, lw=1.5)
    ax.plot(r, Z[-1, :], color=RED, lw=2.5)
    ax.set_xlabel("到药材中心的距离 r / cm")
    ax.set_ylabel("水分浓度 / (kg/kg)")
    ax.set_title("Q2 全断面失水演化（浅→深=时间推进）")
    ax.legend(["t=0", "t=3 h"], loc="best")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图22-Q2全断面失水瀑布图.pdf")


def fig25():
    """图25-Q2潜热对照双联图"""
    d = read_csv("fig_q2_latent.csv")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.2))
    ax1.plot(d.t_h, d.dT_center, color=BLUE, lw=1.5)
    ax1.plot(d.t_h, d.dT_surface, color=GOLD, lw=1.5)
    ax1.axhline(0, color=GRAY, ls="--", lw=0.8)
    ax1.set_ylabel("温度偏差 / ℃")
    ax1.set_title("潜热效应对照（计入潜热 − 忽略潜热）")
    ax1.legend([r"$\Delta T_0$", r"$\Delta T_R$"], loc="best")
    ax1.grid(True, alpha=0.3)
    ax2.plot(d.t_h, d.dC_center, color=GREEN, lw=1.5)
    ax2.plot(d.t_h, d.dC_surface, color=RED, lw=1.5)
    ax2.axhline(0, color=GRAY, ls="--", lw=0.8)
    ax2.set_xlabel("时间 t / h")
    ax2.set_ylabel("水分浓度偏差 / (kg/kg)")
    ax2.legend([r"$\Delta C_0$", r"$\Delta C_R$"], loc="best")
    ax2.grid(True, alpha=0.3)
    savefig(fig, "图25-Q2潜热对照双联图.pdf")


def fig28():
    """图28-Q2自适应步长轨迹图"""
    d = read_csv("fig_q2_adaptive.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.step(d.t_s, d.h_from_s, color=BLUE, lw=1.8, where="post")
    ax.plot(d.t_s, d.rel_change * max(d.h_from_s), "o-", color=RED, lw=1.2, ms=2)
    ax.set_xlabel("时间 t / s"); ax.set_ylabel("步长 h / s")
    ax.set_title("Q2 自适应步长轨迹")
    ax.legend(["步长 h", "相对变化"], loc="best")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图28-Q2自适应步长轨迹图.pdf")


def fig29():
    """图29-Q3长时程含水率演化"""
    d = read_csv("fig_q3_history.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(d.t_h, d.C_center, color=BLUE, lw=1.5)
    ax.plot(d.t_h, d.C_surface, color=RED, lw=1.5)
    ax.axhline(0.15, color=GRAY, ls="--", lw=0.8)
    ax.text(0.3, 0.160, "达标阈值 C=0.15", color=GRAY, fontsize=7)
    ax.axhline(0.04999, color="#B0B0B0", ls="--", lw=0.6)
    ax.text(d.t_h.iloc[-1] * 0.15 - 4, 0.058, r"$C_\infty$=0.04999", color="#B0B0B0", fontsize=6.5)
    ax.axvline(d.t_h.iloc[-1], color=RED, ls=":", lw=0.8)
    ax.set_xlabel("时间 t / h"); ax.set_ylabel("水分浓度 / (kg/kg)")
    ax.set_title("Q3 中心与表面水分浓度长时程演化")
    ax.legend([r"$C_0$ 中心", r"$C_R$ 表面"], loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图29-Q3长时程含水率演化.pdf")


def fig36():
    """图36-Q3干燥速率曲线"""
    d = read_csv("fig_q3_drying_rate.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(d.t_h, d.u_kg_per_kg_h, color=BLUE, lw=1.5)
    i = d.u_kg_per_kg_h.iloc[:int(len(d) * 0.3)].idxmax()
    ax.text(d.t_h[i] + 2, d.u_kg_per_kg_h[i] * 1.5,
            f"峰值 {d.u_kg_per_kg_h[i]:.4f}", color=RED, fontsize=7)
    ax.set_xlabel("时间 t / h")
    ax.set_ylabel(r"干燥速率 / ($kg \cdot kg^{-1} \cdot h^{-1}$)")
    ax.set_title("Q3 干燥速率曲线")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图36-Q3干燥速率曲线.pdf")


def fig37():
    """图37-自适应步长轨迹"""
    d = read_csv("fig_q3_stepsize_adaptive.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.step(d.t_h, d.dt_s, color=BLUE, lw=1.2, where="post")
    ax.set_yscale("log")
    ax.set_xlabel("时间 t / h"); ax.set_ylabel("步长 h / s")
    ax.set_title("Q3 误差驱动自适应步长轨迹")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图37-自适应步长轨迹.pdf")


def fig44():
    """图44-Q4潜热中段温降曲线"""
    d = read_csv("fig_q4_INV4_latent_dT.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(d.t_h, d.dT_K, color=RED, lw=1.5)
    ax.axhline(0, color=GRAY, ls="--", lw=0.8)
    i = d.dT_K.idxmax()
    ax.text(d.t_h[i] + 1.5, d.dT_K[i] + max(d.dT_K) * 0.3,
            f"峰值 {d.dT_K[i]:.4f} K @ {d.t_h[i]:.2f} h", fontsize=7)
    ax.set_xlabel("时间 t / h"); ax.set_ylabel(r"$\Delta T$ / K")
    ax.set_title("Q4 潜热中段温降曲线")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图44-Q4潜热中段温降曲线.pdf")


def fig45():
    """图45-Q4压缩温升机理与绝热包络"""
    d = read_csv("fig_q4_INV5_compression.csv")
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.plot(d.t_h, d.TR, color=BLUE, lw=1.5)
    ax.plot(d.t_h, d.T_ad, "--", color=RED, lw=1.2)
    ax.plot(d.t_h, d.theta_meas, color=GREEN, lw=1.2)
    ax.plot(d.t_h, d.theta_qs, "-.", color=GOLD, lw=1.2)
    ax.set_xlabel("时间 t / h"); ax.set_ylabel("温度 / ℃")
    ax.set_title("Q4 压缩温升机理与绝热包络")
    ax.legend([r"$T_R$ 表面", r"$T_{ad}$ 绝热包络",
               r"$\theta_{meas}$ 实测", r"$\theta_{qs}$ 准稳态"], loc="best", fontsize=7)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图45-Q4压缩温升机理与绝热包络.pdf")


def fig41a():
    """图41a-Q4低C端外推UQ-a（截断族曲线）"""
    d = read_csv("fig_q4_INV2_uq_family.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.plot(d.C_fr, d.t_dry_h, "o-", color=BLUE, mfc=BLUE, lw=1.5, ms=4)
    ax.set_xlabel(r"$C_{fr}$"); ax.set_ylabel(r"$t_{dry}$ / h")
    ax.set_title("Q4 低C端外推不确定度 — 截断族曲线")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图41a-Q4低C端外推UQ-a.pdf")


def fig41b():
    """图41b-Q4低C端外推UQ-b（LHS分位）"""
    d = read_csv("fig_q4_INV2_uq_lhs.csv")
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.scatter(d.C_fr, d.t_dry_h, s=25, c="#4DAF4A", edgecolors="none")
    ax.set_xlabel(r"$C_{fr}$"); ax.set_ylabel(r"$t_{dry}$ / h")
    ax.set_title(f"Q4 低C端外推不确定度 — LHS分位 (n={len(d)})")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图41b-Q4低C端外推UQ-b.pdf")


if __name__ == "__main__":
    print("=" * 50)
    print("Batch 1: 折线/双Y轴/简单曲线")
    print(f"输出: {OUTPUT_DIR}")
    print("=" * 50)
    funcs = [fig03, fig04, fig08, fig13, fig16, fig21, fig22,
             fig25, fig28, fig29, fig36, fig37, fig44, fig45, fig41a, fig41b]
    for i, f in enumerate(funcs, 1):
        print(f"[{i}/{len(funcs)}] {f.__name__}...")
        try:
            f()
        except Exception as e:
            print(f"  [FAIL] {e}")
    print(f"\n完成: {OUTPUT_DIR}")