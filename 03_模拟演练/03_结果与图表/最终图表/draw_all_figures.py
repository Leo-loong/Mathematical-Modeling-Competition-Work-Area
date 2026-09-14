# -*- coding: utf-8 -*-
"""
论文图表 seaborn 重绘 — 全中文版
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import os
import seaborn as sns

DATA = "/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/03_模拟演练/交接材料/03_结果与图表包/data"
OUT  = "/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/03_模拟演练/03_结果与图表/最终图表"
os.makedirs(OUT, exist_ok=True)

C10, C15, CFIT, CBG, CRES, CGREEN = "#2166AC", "#B2182B", "#D6604D", "#4393C3", "#5E3C99", "#4DAF4A"
COLS_3 = ["#66C2A5", "#FC8D62", "#8DA0CB"]

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.0)

def setup_chinese():
    candidates = ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei","SimHei","Arial Unicode MS"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "Arial", "DejaVu Sans"]
            plt.rcParams["font.family"] = "sans-serif"
            plt.rcParams["axes.unicode_minus"] = False
            return name
    return None
print("font:", setup_chinese())

plt.rcParams.update({"figure.dpi":150, "savefig.dpi":300, "font.size":10,
    "axes.titlesize":11, "axes.labelsize":9, "legend.fontsize":7.5,
    "xtick.labelsize":8, "ytick.labelsize":8,
    "axes.spines.top":False, "axes.spines.right":False})

def draw_fig2():
    df = pd.read_csv(os.path.join(DATA, "fig2_data.csv"))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.8), sharex=True)
    ax1.plot(df["sigma10"], df["R10"], "-", lw=0.35, color=C10, label="实测谱 10°")
    ax1.plot(df["sigma10"], df["bg10"], "--", lw=1.0, color=CBG, label="poly7 背景")
    ax1.axvline(x=1100, color="gray", ls=":", lw=0.7)
    ax1.axvspan(df["sigma10"].min(), 1100, color="#F5A9A9", alpha=0.08)
    ax1.set_ylabel("反射率 R (%)")
    ax1.legend(loc="upper right")
    ax2.plot(df["sigma15"], df["R15"], "-", lw=0.35, color=C15, label="实测谱 15°")
    ax2.plot(df["sigma15"], df["bg15"], "--", lw=1.0, color=CBG, label="poly7 背景")
    ax2.axvline(x=1100, color="gray", ls=":", lw=0.7)
    ax2.axvspan(df["sigma15"].min(), 1100, color="#F5A9A9", alpha=0.08)
    ax2.set_xlabel("波数 σ (cm⁻¹)")
    ax2.set_ylabel("反射率 R (%)")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_spectrum.png"), dpi=300, pad_inches=0.05)
    plt.close(fig); print("fig2 done")

def draw_fig3():
    df = pd.read_csv(os.path.join(DATA, "fig3_data.csv"))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.2), sharex=True, gridspec_kw={"height_ratios":[2.5,1]})
    ax1.plot(df["sigma"], df["F_meas"], ".", ms=0.6, color=C10, alpha=0.25, label="实测条纹分量")
    ax1.plot(df["sigma"], df["F_fit"], "-", lw=0.8, color=CFIT, label="v1.0 模型拟合")
    ax1.set_ylabel("条纹分量")
    ax1.legend(loc="upper right")
    res = df["residual"].values
    ax2.plot(df["sigma"], res, "-", lw=0.35, color=CRES)
    ax2.axhline(y=0, color="gray", ls="--", lw=0.6)
    ax2.set_xlabel("波数 σ (cm⁻¹)")
    ax2.set_ylabel("残差")
    ax2.text(0.02, 0.92, "标准差 = {:.2f}%".format(np.std(res)),
             transform=ax2.transAxes, fontsize=8, va="top",
             bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.8))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig3_fitresidual.png"), dpi=300, pad_inches=0.05)
    plt.close(fig); print("fig3 done")

def draw_fig4():
    df = pd.read_csv(os.path.join(DATA, "fig4_data.csv"))
    df_alg = df[~df["method"].str.contains("融合")].copy()
    df_alg["label_short"] = df_alg["method"].map({"E1 极值回归":"E1","E2 谱域FFT":"E2","E3 全谱拟合":"E3"})
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    methods_order = ["E1","E2","E3"]
    y_positions = {m: i*2.5 for i,m in enumerate(methods_order)}
    for _, row in df_alg.iterrows():
        m = row["label_short"]; ang = int(row["angle"])
        yc = y_positions[m] + (0.35 if ang==10 else -0.35)
        color = C10 if ang==10 else C15; marker = "o" if ang==10 else "s"
        ax.errorbar(row["d_hat_um"], yc, xerr=row["sigma_stat_um"],
                    fmt=marker, color=color, mec="white", mew=0.5,
                    capsize=3, capthick=1.2, ms=7, elinewidth=1.0, zorder=5)
    ax.axvline(x=8.03, color=CGREEN, ls="--", lw=2.0, zorder=2)
    ax.axvspan(8.0, 8.9, alpha=0.08, color=CGREEN, zorder=1)
    ax.set_yticks(list(y_positions.values())); ax.set_yticklabels(methods_order)
    ax.set_xlabel("厚度估计 d (μm)"); ax.set_xlim(7.5, 9.4)
    ax.set_ylim(-1.2, max(y_positions.values())+1.2)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([],[], marker="o", color=C10, ls="none", ms=7, mec="white", mew=0.5, label="10°"),
        Line2D([],[], marker="s", color=C15, ls="none", ms=7, mec="white", mew=0.5, label="15°"),
        Line2D([],[], color=CGREEN, ls="--", lw=2, label="融合 8.03 μm"),
        plt.Rectangle((0,0),1,1, fc=CGREEN, alpha=0.08, label="系统区间 [8.0, 8.9]"),
    ]
    ax.legend(handles=handles, fontsize=7.5, loc="lower right", ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4_crosscomparison.png"), dpi=300, pad_inches=0.05)
    plt.close(fig); print("fig4 done")

def draw_fig5():
    df_spread = pd.read_csv(os.path.join(DATA, "fig5_spread.csv"))
    df_boot = pd.read_csv(os.path.join(DATA, "fig5_boot.csv"))
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 8.0))
    methods=["E1","E2","E3"]; x=np.arange(3); w=0.22; all_vals=[]
    for i, (_, row) in enumerate(df_spread.iterrows()):
        d0 = int(row["d0_um"])
        vals = [row["E1"], row["E2"], row["E3"]]
        all_vals.extend(vals)
        bars = ax1.bar(x+(i-1)*w, vals, w, label="d₀={} μm".format(d0),
                       color=COLS_3[i], alpha=0.85, edgecolor="white", lw=0.3)
        for bar, v in zip(bars, vals):
            if v>0.001:
                ax1.text(bar.get_x()+bar.get_width()/2, v+max(all_vals)*0.02,
                         "{:.4f}".format(v), ha="center", fontsize=5.8, rotation=90, va="bottom", color="#333")
    ax1.set_xticks(x); ax1.set_xticklabels(methods)
    ax1.set_ylabel("|Δd| (μm)")
    ax1.axhline(y=0.06, color="red", ls="--", lw=1.0, alpha=0.5)
    ax1.text(2.8, 0.062, "阈值 0.06 μm", fontsize=7, color="red", ha="right")
    ax1.set_ylim(0, max(max(all_vals),0.06)*1.3)
    ax1.legend(fontsize=7, loc="upper left")
    d10 = df_boot["fused10"].dropna().values; d15 = df_boot["fused15"].dropna().values
    sns.histplot(d10, bins=30, alpha=0.35, color=C10, label="10°", ax=ax2, edgecolor="white", lw=0.3, stat="density")
    sns.histplot(d15, bins=30, alpha=0.35, color=C15, label="15°", ax=ax2, edgecolor="white", lw=0.3, stat="density")
    sns.kdeplot(d10, color=C10, lw=1.5, ax=ax2, bw_adjust=0.5)
    sns.kdeplot(d15, color=C15, lw=1.5, ax=ax2, bw_adjust=0.5)
    ax2.set_xlabel("d (μm)"); ax2.set_ylabel("概率密度")
    ax2.set_title("Bootstrap (N={:d})".format(len(d10)), fontweight="bold")
    fig.tight_layout(pad=1.5)
    _, yhi = ax2.get_ylim(); ax2.set_ylim(0, yhi*1.4)
    ax2.axvline(x=8.03, ymin=0, ymax=0.75, color=CGREEN, ls="-", lw=2.0, label="融合 8.03 μm")
    ax2.legend(fontsize=7.5, loc="upper left")
    ax2.text(0.98, 0.97, "10°: {:.3f} ± {:.3f} μm\n15°: {:.3f} ± {:.3f} μm".format(
        np.mean(d10), np.std(d10), np.mean(d15), np.std(d15)),
        transform=ax2.transAxes, fontsize=7, va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.8))
    fig.savefig(os.path.join(OUT, "fig5_closedloop.png"), dpi=300, pad_inches=0.08)
    plt.close(fig); print("fig5 done")

if __name__ == "__main__":
    draw_fig2(); draw_fig3(); draw_fig4(); draw_fig5()
    print("all done")