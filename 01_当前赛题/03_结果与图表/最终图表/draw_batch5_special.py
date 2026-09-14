# -*- coding: utf-8 -*-
"""
Batch 5+6: 子图验证 + 特殊图 (10张)
图09,10,17,26,27,33,34,39,42,43
(图20已跳过-MATLAB；图01,02,19已有)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _fig_common_remastered import *


# ============ 子图验证 ============

def fig09():
    """图09-解析级数解对拍"""
    d = read_csv("fig_series_check.csv")
    sel = d[d.case == "E2a_dr0.25mm"]
    t = sel.t.values; yn = sel.Tc_num.values; ya = sel.Tc_ana.values; dev = yn - ya
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5))
    ax1.plot(t, ya, color=GOLD, lw=1.5, zorder=2)
    ax1.plot(t, yn, "--", color=BLUE, lw=1.5, zorder=3)
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1 温度解析对拍（解析级数解 对比 数值解，r=0）")
    ax1.legend(["数值解(0.25mm)", "解析级数解"], loc="best")
    ax1.grid(True, alpha=0.3)
    ax2.plot(t, dev, color=GREEN, lw=1.5, label=r"偏差 $\Delta$")
    ax2.axhline(0, color=GRAY, ls="--", lw=0.8)
    ax2.set_xlabel("时间 t / s"); ax2.set_ylabel(r"偏差 $\Delta$ / ℃")
    ax2.set_ylim(-9e-3, 9e-3)
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)
    savefig(fig, "图09-解析级数解对拍.pdf")


def fig10():
    """图10-独立实现互验"""
    d = read_csv("fig_e3_check.csv")
    dev = d.Ts_main.values - d.Ts_expl.values
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5))
    ax1.plot(d.t, d.Ts_expl, color=GOLD, lw=1.5, zorder=2)
    ax1.plot(d.t, d.Ts_main, "--", color=BLUE, lw=1.5, zorder=3)
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1 独立实现互验（表面温度，t≤3h）")
    ax1.legend(["主力解(全隐式)", "独立实现(FTCS)"], loc="best")
    ax1.grid(True, alpha=0.3)
    ax2.plot(d.t, dev, color=GREEN, lw=1.5, label=r"偏差 $\Delta T$")
    ax2.axhline(0, color=GRAY, ls="--", lw=0.8)
    ax2.set_xlabel("时间 t / s"); ax2.set_ylabel(r"偏差 $\Delta T$ / ℃")
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)
    savefig(fig, "图10-独立实现互验.pdf")


def fig17():
    """图17-Q1Q2重叠段差异归因"""
    d = read_csv("fig_q1q2_overlap.csv")
    dT = d.T_surface_q2 - d.T_surface_q1
    dC = d.C_surface_q2 - d.C_surface_q1
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.2))
    ax1.plot(d.t, d.T_surface_q1, "--", color=GOLD, lw=1.5)
    ax1.plot(d.t, d.T_surface_q2, "-", color=GOLD, lw=2)
    ax1.set_ylabel("温度 / ℃")
    ax1.set_title("Q1与Q2重叠段(0-1800s)差异归因")
    ax1.legend([r"$T_R$ Q1(常物性)", r"$T_R$ Q2(变物性)"], loc="lower right")
    ax1.grid(True, alpha=0.3)
    ax2.plot(d.t, dT, color=RED, lw=1.5)
    ax2.plot(d.t, dC, "-.", color=GREEN, lw=1.5)
    ax2.axhline(0, color=GRAY, ls="--", lw=0.8)
    ax2.set_xlabel("时间 t / s"); ax2.set_ylabel("偏差")
    ax2.legend([r"$\Delta T_R$(Q2-Q1)", r"$\Delta C_R$(Q2-Q1)"], loc="best")
    ax2.grid(True, alpha=0.3)
    savefig(fig, "图17-Q1Q2重叠段差异归因.pdf")


# ============ 特殊图 ============

def fig26():
    """图26-Q2精度效率帕累托图"""
    d = read_csv("fig_q2_pareto.csv")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(d.wall_s, d.rel_err, "o", color=BLUE, ms=10, mfc=BLUE)
    for _, r in d.iterrows():
        ax.text(r.wall_s * 1.08, r.rel_err, r.scheme, fontsize=6,
                va="center", ha="left")
    ax.set_xlabel("计算耗时 / s"); ax.set_ylabel("相对误差")
    ax.set_title("Q2 精度-效率帕累托图")
    # 右侧留空给标签
    ax.set_xlim(left=d.wall_s.min() * 0.8, right=d.wall_s.max() * 2.5)
    ax.grid(True, which="both", alpha=0.35)
    ax.grid(True, which="major", alpha=0.55)
    fig.tight_layout()
    savefig(fig, "图26-Q2精度效率帕累托图.pdf")


def fig27():
    """图27-Q2全局灵敏度热力图"""
    d = read_csv("fig_q2_gs_sobol.csv")
    outputs = d.output.unique(); params = d.parameter.unique()
    n_o, n_p = len(outputs), len(params)
    M = np.zeros((n_p, n_o))
    for _, r in d.iterrows():
        ri = list(params).index(r.parameter)
        ci = list(outputs).index(r.output)
        M[ri, ci] = r.ST
    # 翻译输出标签
    out_labels = {"T_center": "T 中心", "T_surface": "T 表面",
                  "C_center": "C 中心", "C_surface": "C 表面"}
    xlbl = [out_labels.get(o, o) for o in outputs]
    vmax = M.max() * 1.1
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    im = ax.imshow(M, cmap="jet_r", aspect="auto", vmin=0, vmax=vmax)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label(r"$S_T$")
    ax.set_xticks(range(n_o)); ax.set_xticklabels(xlbl, rotation=30, fontsize=8, ha="center")
    ax.set_yticks(range(n_p))
    param_labels_map = {"h": r"$h$", "km": r"$k_m$", "D0": r"$D_0$",
                        "Tinf": r"$T_\infty$", "Cinf": r"$C_\infty$"}
    ax.set_yticklabels([param_labels_map.get(p, p) for p in params], fontsize=8)
    for i in range(n_p):
        for j in range(n_o):
            ax.text(j, i, f"{M[i,j]:.3f}", ha="center", va="center", fontsize=7.5, color="black")
    ax.set_title("Q2 全局灵敏度 Sobol ST 热力图")
    ax.grid(False)
    fig.tight_layout(pad=1.5)
    savefig(fig, "图27-Q2全局灵敏度热力图.pdf")


def fig33():
    """图33-Q3全局灵敏度（Morris + Sobol）"""
    math_map = {"T_inf": r"$T_\infty$", "C_inf": r"$C_\infty$",
                "h": r"$h$", "k_m": r"$k_m$", "D0": r"$D_0$"}
    m = read_csv("fig_q3_gs_morris.csv")
    s = read_csv("fig_q3_gs_sobol.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))

    ax1.scatter(m.mu_star, m.sigma, s=40, color=INK, edgecolors="none")
    for _, r in m.iterrows():
        lbl = math_map.get(r.param, r.param)
        ax1.text(r.mu_star * 1.15, r.sigma * 1.15, lbl, fontsize=7, va="center")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel(r"$\mu^*$"); ax1.set_ylabel(r"$\sigma$")
    ax1.set_title(r"Morris $\mu^*$-$\sigma$")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.grid(True, which="major", alpha=0.5)

    # Sobol 右图
    x = np.arange(len(s))
    w = 0.35
    ax2.bar(x - w/2, s.S1, w, color=BLUE, label="S1")
    ax2.bar(x + w/2, s.ST, w, color=GOLD, label="ST")
    ax2.set_xticks(x); ax2.set_xticklabels([math_map.get(p, p) for p in s.param], fontsize=7)
    ax2.set_ylabel("灵敏度指数"); ax2.set_title("Sobol S1 对比 ST")
    ax2.legend(fontsize=7)
    ax2.grid(True, alpha=0.3)
    savefig(fig, "图33-Q3全局灵敏度.pdf")


def fig34():
    """图34-Q3低C端外推不确定度"""
    dg = read_csv("fig_q3_uq_grid.csv")
    dl = read_csv("fig_q3_uq_lhs.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5))
    ax1.plot(dg.C_fr, dg.t_end_h, "o-", color=BLUE, mfc=BLUE, ms=4, lw=1.5)
    ax1.set_xlabel(r"$C_{fr}$"); ax1.set_ylabel(r"$t_{end}$ / h")
    ax1.set_title("(a) 截断族曲线"); ax1.grid(True, alpha=0.3)
    ax2.scatter(dl.C_fr, dl.t_end_h, s=20, c="#4DAF4A", edgecolors="none")
    ax2.set_xlabel(r"$C_{fr}$"); ax2.set_ylabel(r"$t_{end}$ / h")
    ax2.set_title(f"(b) 拉丁超立方抽样 (n={len(dl)})"); ax2.grid(True, alpha=0.3)
    savefig(fig, "图34-Q3低C端外推不确定度.pdf")


def fig39():
    """图39-全局灵敏度与OAT并置"""
    math_map = {"h": r"$h$", "km": r"$k_m$", "D0": r"$D_0$",
                "Tinf_off": r"$T_\infty(off)$", "Cinf_off": r"$C_\infty(off)$"}
    d = read_csv("fig_q1_gs.csv")
    sel = d[d.output == "CR"].copy()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    x = np.arange(len(sel)); w = 0.35
    ax.bar(x - w/2, sel.S1, w, color=BLUE, label="S1")
    ax.bar(x + w/2, sel.ST, w, color=GOLD, label="ST")
    ax.set_xticks(x); ax.set_xticklabels([math_map.get(p, p) for p in sel.param], fontsize=7)
    ax.set_ylabel("灵敏度指数"); ax.set_title(r"Q1 全局灵敏度 Sobol（$C_R$）")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    savefig(fig, "图39-全局灵敏度与OAT并置.pdf")


def fig42():
    """图42-Q4全局灵敏度（Morris）"""
    math_map = {"d_fac": r"$d_{fac}$", "h": r"$h$", "km": r"$k_m$",
                "Tinf": r"$T_\infty$", "Cinf": r"$C_\infty$", "C_fr": r"$C_{fr}$"}
    d = read_csv("fig_q4_INV3_morris.csv")
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.scatter(d.mu_star, d.sigma, s=40, color=INK, edgecolors="none", zorder=3)
    # 点半径约 0.003 数据单位，标签紧贴点上方；Cinf/Tinf 左右微调错开
    dy_close = 0.008
    pos = {
        "h":    (0, dy_close),
        "km":   (0, dy_close),
        "d_fac": (0, dy_close),
        "C_fr": (0, dy_close),
        "Cinf": (-0.005, dy_close),
        "Tinf": (+0.005, dy_close),
    }
    for _, r in d.iterrows():
        lbl = math_map.get(r.param, r.param)
        dx, dy = pos.get(r.param, (0, dy_close))
        ax.text(r.mu_star + dx, r.sigma + dy, lbl, fontsize=7, ha="center", va="bottom")
    ax.set_xlim(-0.02, d.mu_star.max() + 0.06)
    ax.set_ylim(-0.005, d.sigma.max() + 0.03)
    ax.set_xlabel(r"$\mu^*$ (均值影响)"); ax.set_ylabel(r"$\sigma$ (非线性/交互)")
    ax.set_title("Q4 全局灵敏度 Morris (6参数)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    savefig(fig, "图42-Q4全局灵敏度.pdf")


def fig43():
    """图43-Q4收缩物性双效应分解"""
    base = 57.53; prop = 71.9; shrink = -78.8; actual = 50.78
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.bar(0, base, 0.45, color=BLUE)
    ax.bar(1, prop, 0.45, color=GOLD, bottom=base)
    ax.bar(2, shrink, 0.45, color=GREEN, bottom=base+prop+shrink)
    ax.bar(3, actual, 0.45, color=BLUE)
    y0 = base; y1 = base + prop; y2 = base + prop + shrink
    ax.plot([-0.2, 0.2], [y0, y0], "k", lw=1.2)
    ax.plot([0.8, 1.2], [y1, y1], "k", lw=1.2)
    ax.plot([1.8, 2.2], [y2, y2], "k", lw=1.2)
    ax.text(0, base + 5, f"{base:.1f} h", ha="center", fontsize=8)
    ax.text(1, y1 + 5, f"+{prop:.1f} h", ha="center", color=RED, fontsize=8)
    ax.text(2, y2 - 10, f"{shrink:.1f} h", ha="center", color=GREEN, fontsize=8)
    ax.text(3, actual + 5, f"{actual:.2f} h", ha="center", fontsize=8)
    net = base + prop + shrink
    ax.text(0.98, 0.9, f"净= {net:+.1f} h", transform=ax.transAxes, ha="right",
            fontsize=10, fontweight="bold", bbox=dict(facecolor="white", alpha=0.8))
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["Q3基准", "物性+71.9", "收缩-78.8", "Q4实际"], rotation=30, fontsize=8)
    ax.set_ylabel("烘干时间 / h")
    ax.set_title("Q4 收缩-物性双效应分解")
    ax.grid(True, alpha=0.3)
    savefig(fig, "图43-Q4收缩物性双效应分解.pdf")


if __name__ == "__main__":
    print("=" * 50)
    print("Batch 5+6: 子图验证 + 特殊图")
    print("=" * 50)
    funcs = [fig09, fig10, fig17, fig26, fig27, fig33, fig34, fig39, fig42, fig43]
    for f in funcs:
        print(f"  {f.__name__}...")
        try:
            f()
        except Exception as e:
            print(f"  [FAIL] {f.__name__}: {e}")
    print(f"\n完成: {OUTPUT_DIR}")