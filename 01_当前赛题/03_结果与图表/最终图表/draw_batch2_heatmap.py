# -*- coding: utf-8 -*-
"""
Batch 2: 彩色热力图/云图 (4张)
图06,07,14,15
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _fig_common_remastered import *
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def _interp_field(t, Z, n_r=200):
    """用 RegularGridInterpolator 做 spline 插值（替代已移除的 interp2d）"""
    r = np.linspace(0, 2, Z.shape[1])
    interp = RegularGridInterpolator((t, r), Z, method="cubic", bounds_error=False, fill_value=None)
    r_fine = np.linspace(0, 2, n_r)
    t_fine = np.linspace(t[0], t[-1], Z.shape[0])
    tg, rg = np.meshgrid(t_fine, r_fine, indexing="ij")
    Z_fine = interp(np.column_stack([tg.ravel(), rg.ravel()])).reshape(len(t_fine), len(r_fine))
    return r_fine, t_fine, Z_fine


def fig06():
    """图06-Q1温度场时空分布"""
    t, Z = read_matrix("fig_q1_field_T.csv")
    _, t_fine, Z_fine = _interp_field(t, Z)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    im = ax.imshow(Z_fine, extent=[0, 2, t[-1], t[0]], aspect="auto", cmap="viridis", vmin=28, vmax=37)
    c = fig.colorbar(im, ax=ax, shrink=0.8)
    c.set_label("温度 / ℃")
    ax.set_xlabel("到药材中心的距离 r / cm")
    ax.set_ylabel("时间 t / s")
    ax.set_title("Q1 温度场 T(r,t) 时空分布")
    savefig(fig, "图06-Q1温度场时空分布.pdf")


def fig07():
    """图07-Q1水分浓度场时空分布"""
    t, Z = read_matrix("fig_q1_field_C.csv")
    _, t_fine, Z_fine = _interp_field(t, Z)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    im = ax.imshow(Z_fine, extent=[0, 2, t[-1], t[0]], aspect="auto", cmap="viridis", vmin=1.5, vmax=2.55)
    c = fig.colorbar(im, ax=ax, shrink=0.8)
    c.set_label("水分浓度 / (kg/kg)")
    ax.set_xlabel("到药材中心的距离 r / cm")
    ax.set_ylabel("时间 t / s")
    ax.set_title("Q1 水分浓度场 C(r,t) 时空分布")
    savefig(fig, "图07-Q1水分浓度场时空分布.pdf")


def fig14():
    """图14-Q2温度场时空分布（0-3 h）"""
    t, Z = read_matrix("fig_q2_field_T.csv")
    _, t_fine, Z_fine = _interp_field(t, Z)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    im = ax.imshow(Z_fine, extent=[0, 2, t[-1], t[0]], aspect="auto", cmap="viridis", vmin=28, vmax=55)
    c = fig.colorbar(im, ax=ax, shrink=0.8)
    c.set_label("温度 / ℃")
    ax.axhline(1800, color="white", ls="--", lw=0.8)
    ax.text(0.05, 1700, "Q1结束", color="white", fontsize=7)
    ax.set_xlabel("到药材中心的距离 r / cm")
    ax.set_ylabel("时间 t / s")
    ax.set_title("Q2 温度场 T(r,t) 时空分布（0-3 h）")
    savefig(fig, "图14-Q2温度场时空分布.pdf")


def fig15():
    """图15-Q2水分浓度场时空分布（0-3 h）"""
    t, Z = read_matrix("fig_q2_field_C.csv")
    _, t_fine, Z_fine = _interp_field(t, Z)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    im = ax.imshow(Z_fine, extent=[0, 2, t[-1], t[0]], aspect="auto", cmap="viridis", vmin=0.9, vmax=2.55)
    c = fig.colorbar(im, ax=ax, shrink=0.8)
    c.set_label("水分浓度 / (kg/kg)")
    ax.axhline(1800, color="gray", ls="--", lw=0.8)
    ax.text(0.05, 1700, "Q1结束", color="black", fontsize=7)
    ax.set_xlabel("到药材中心的距离 r / cm")
    ax.set_ylabel("时间 t / s")
    ax.set_title("Q2 水分浓度场 C(r,t) 时空分布（0-3 h）")
    savefig(fig, "图15-Q2水分浓度场时空分布.pdf")


if __name__ == "__main__":
    print("=" * 50)
    print("Batch 2: 彩色热力图/云图")
    print(f"输出: {OUTPUT_DIR}")
    print("=" * 50)
    for f in [fig06, fig07, fig14, fig15]:
        print(f"  {f.__name__}...")
        try:
            f()
        except Exception as e:
            print(f"  [FAIL] {e}")
    print(f"\n完成: {OUTPUT_DIR}")