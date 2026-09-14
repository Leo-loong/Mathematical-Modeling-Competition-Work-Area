# -*- coding: utf-8 -*-
"""
Batch 6: 新增图表 — F-26 雷达图 + 图42重做版（F-46 三面板）
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _fig_common_remastered import *
from scipy.stats import rankdata, pearsonr
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


# ============================================================
# F-26 灵敏度结构雷达图（Q1 vs Q2）
# ============================================================
def fig47():
    """图47-F26：灵敏度结构雷达图（Q1 vs Q2），双叠层5轴"""
    param_map = {"h": r"$h$", "km": r"$k_m$", "D0": r"$D_0$",
                 "Tinf_off": r"$T_\infty$", "Tinf": r"$T_\infty$",
                 "Cinf_off": r"$C_\infty$", "Cinf": r"$C_\infty$"}
    common_params = ["h", "km", "D0", "Tinf", "Cinf"]
    param_labels = [param_map[p] for p in common_params]

    # Q1: CR output, mu_star
    q1 = read_csv("fig_q1_gs.csv")
    q1 = q1[q1.output == "CR"]  # use C surface
    q1_map = {"h": "h", "km": "km", "D0": "D0", "Tinf_off": "Tinf", "Cinf_off": "Cinf"}
    q1_vals = {}
    for _, r in q1.iterrows():
        key = q1_map.get(r.param, r.param)
        if key in common_params:
            q1_vals[key] = abs(r.mu_star)
    q1_arr = np.array([q1_vals.get(p, 0) for p in common_params])
    m1 = q1_arr.max()
    q1_norm = q1_arr / m1 if m1 > 0 else q1_arr

    # Q2: C_surface output, abs(S_half)
    q2 = read_csv("fig_q2_sens_S.csv")
    q2 = q2[q2.output == "C_surface"]
    q2_vals = {}
    for _, r in q2.iterrows():
        if r.parameter in common_params:
            q2_vals[r.parameter] = abs(r.S_half)
    q2_arr = np.array([q2_vals.get(p, 0) for p in common_params])
    m2 = q2_arr.max()
    q2_norm = q2_arr / m2 if m2 > 0 else q2_arr

    # Radar plot
    n = len(common_params)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    q1_norm_c = np.append(q1_norm, q1_norm[0])
    q2_norm_c = np.append(q2_norm, q2_norm[0])

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, q1_norm_c, color=BLUE, alpha=0.25)
    ax.plot(angles, q1_norm_c, "o-", color=BLUE, lw=1.5, ms=5, label=r"Q1 ($C_R$)")
    ax.fill(angles, q2_norm_c, color=GOLD, alpha=0.25)
    ax.plot(angles, q2_norm_c, "s-", color=GOLD, lw=1.5, ms=5, label=r"Q2 ($C_R$)")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(param_labels, fontsize=9)
    ax.set_yticklabels([])
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.10), fontsize=7)
    ax.set_title("灵敏度结构雷达图（Q1 对比 Q2）", pad=18, fontsize=11)
    # Annotate self-normalized
    ax.text(0, -0.25, "各层按自身最大 |S| 归一；仅比较形状与排序",
            transform=ax.transAxes, ha="center", fontsize=6.5, color=GRAY)
    fig.tight_layout()
    savefig(fig, "图47-F26_灵敏度雷达图.pdf")


# ============================================================
# 图42重做版 — F-46 Q4 全局灵敏度（三面板）
# ============================================================
def _prcc(data, param_cols, target_col):
    """Compute partial rank correlation coefficients (basic version)."""
    X = data[param_cols].values
    y = data[target_col].values
    n_params = len(param_cols)
    prcc_vals = np.zeros(n_params)
    # Rank transform
    Xr = np.apply_along_axis(rankdata, 0, X)
    yr = rankdata(y)
    for i in range(n_params):
        # Residual of X_i from other X
        others = [j for j in range(n_params) if j != i]
        if len(others) == 0:
            prcc_vals[i], _ = pearsonr(Xr[:, 0], yr)
        else:
            # Regress X_i on others, get residual
            Xo = np.column_stack([Xr[:, j] for j in others])
            # Simple approach: partial correlation via inversion
            # Build correlation matrix of [X_i, all others, y]
            all_cols = np.column_stack([Xr[:, i], Xo, yr])
            corr = np.corrcoef(all_cols.T)
            # Partial correlation of X_i and y controlling for others
            # Using the 3-variable formula iteratively
            prec = np.linalg.pinv(corr)
            # Partial corr = -prec[0,-1] / sqrt(prec[0,0] * prec[-1,-1])
            denom = np.sqrt(max(prec[0, 0] * prec[-1, -1], 1e-15))
            prcc_vals[i] = -prec[0, -1] / denom
    return prcc_vals


def fig42_remastered():
    """图42重做版：Q4 全局灵敏度（Morris + PRCC + Sobol 三面板）"""
    math_map = {"d_fac": r"$d_{fac}$", "h": r"$h$", "km": r"$k_m$",
                "Tinf": r"$T_\infty$", "Cinf": r"$C_\infty$", "C_fr": r"$C_{fr}$"}

    # Panel order: C_fr, d_fac, km, Tinf, h, Cinf (sorted by mu_star descending)
    param_order = ["C_fr", "d_fac", "km", "Tinf", "Cinf", "h"]
    y_labels = [math_map[p] for p in param_order]

    # ---- Morris ----
    morris = read_csv("fig_q4_INV3_morris.csv")
    morris_idx = {r.param: r.mu_star for _, r in morris.iterrows()}
    morris_vals = [morris_idx.get(p, 0) for p in param_order]
    m_max = max(morris_vals) * 1.15

    # ---- PRCC from LHS ----
    lhs = read_csv("fig_q4_INV3_lhs.csv")
    param_cols = ["d_fac", "h", "km", "Tinf", "Cinf", "C_fr"]
    prcc_raw = _prcc(lhs, param_cols, "t_rel")
    prcc_idx = {p: prcc_raw[i] for i, p in enumerate(param_cols)}
    prcc_vals = [prcc_idx.get(p, 0) for p in param_order]

    # ---- Sobol ----
    sobol = read_csv("fig_q4_INV6_sobol.csv")
    sobol_idx_s1 = {r.param: r.S1 for _, r in sobol.iterrows()}
    sobol_idx_st = {r.param: r.ST for _, r in sobol.iterrows()}
    sobol_s1 = [sobol_idx_s1.get(p, 0) for p in param_order]
    sobol_st = [sobol_idx_st.get(p, 0) for p in param_order]

    fig, axes = plt.subplots(1, 3, figsize=(10, 4.5))

    # Panel 1: Morris mu*
    yp = range(len(param_order))[::-1]
    axes[0].barh(yp, morris_vals, color=BLUE, height=0.6)
    axes[0].set_yticks(yp)
    axes[0].set_yticklabels(y_labels, fontsize=8)
    axes[0].set_xlabel(r"$\mu^*$")
    axes[0].set_title(r"(a) Morris $\mu^*$")
    axes[0].set_xlim(0, m_max)
    axes[0].grid(True, alpha=0.3)

    # Panel 2: PRCC
    prcc_colors = [RED if abs(v) > 0.3 else GRAY for v in prcc_vals]
    axes[1].barh(yp, prcc_vals, color=prcc_colors, height=0.6)
    axes[1].set_yticks(yp)
    axes[1].set_yticklabels([])
    axes[1].set_xlabel(r"PRCC $\rho$")
    axes[1].set_title(r"(b) LHS-PRCC")
    axes[1].axvline(0, color=INK, lw=0.8)
    axes[1].set_xlim(-1, 1)
    axes[1].grid(True, alpha=0.3)

    # Panel 3: Sobol S1/ST grouped bar
    bar_h = 0.25
    axes[2].barh([y + bar_h for y in yp], sobol_s1, bar_h, color=BLUE, label=r"$S_1$")
    axes[2].barh([y - bar_h for y in yp], sobol_st, bar_h, color=GOLD, alpha=0.5, label=r"$S_T$")
    axes[2].set_yticks(yp)
    axes[2].set_yticklabels([])
    axes[2].set_xlabel("Sobol 指数")
    axes[2].set_title(r"(c) Sobol $S_1$ / $S_T$")
    axes[2].legend(fontsize=7, loc="lower right")
    axes[2].grid(True, alpha=0.3)

    fig.suptitle("Q4 全局灵敏度（Morris + PRCC + Sobol）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    savefig(fig, "图42-重做版_Q4全局灵敏度.pdf")


if __name__ == "__main__":
    print("=" * 50)
    print("Batch 6: 新增图表")
    print("=" * 50)
    for f in [fig47, fig42_remastered]:
        print(f"  {f.__name__}...")
        try:
            f()
        except Exception as e:
            import traceback
            print(f"  [FAIL] {e}")
            traceback.print_exc()
    print(f"\n完成: {OUTPUT_DIR}")