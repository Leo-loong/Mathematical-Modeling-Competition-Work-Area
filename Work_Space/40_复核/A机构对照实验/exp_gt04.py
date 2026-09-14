# -*- coding: utf-8 -*-
"""
补充实验：解释机构《GT04：A题解题步骤》Q1 表1 的"物理不可能值"
==============================================================
GT04 表1（1800 s）给出中心 47.3203 ℃、表面 48.5448 ℃，而 1800 s 烘房温度只有 41.5130 ℃。
GS05/GT04 采用**球坐标** + **显式**格式（Δt=1 s、Δr=0.1 cm）。

关键点：球坐标中心节点的显式稳定条件为 6αΔt/Δr² ≤ 1（即 Fo ≤ 1/6），
而 α=1.6886e-7、Δr=1 mm、Δt=1 s 时 6Fo = 1.0132 > 1 ⟹ **中心节点处在显式稳定域之外**。
本实验按 GS05/GT04 的描述复现该格式，检验是否能复现其公布值。
"""
import io
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import T1, TAIR, props_q1, props_q2

OUT = os.path.join(HERE, 'exp_gt04_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def explicit(pg, N=20, R0=0.02, dt=1.0, t_end=1800.0, prop='q1',
             Tamb=50.0, Cenv=0.01963, surf='quasi'):
    nsteps = int(round(t_end / dt))
    dr = R0 / N
    r = np.arange(N + 1) * dr
    h, km = 25.0, 8.0e-7
    T = np.full(N + 1, 28.0)
    C = np.full(N + 1, 2.55)
    rl = r[:-1] + dr / 2                      # 内部界面 r_{i+1/2}
    Tmax_hist = []
    for n in range(nsteps):
        if prop == 'q1':
            rho, cp, kk, DD = props_q1(C)
        else:
            rho, cp, kk, DD = props_q2(C, T)
        Ta = Tamb
        Tn = T.copy()
        # 内部（几何指数 pg）
        Tn[1:N] = T[1:N] + (dt / (rho[1:N] * cp[1:N] *
                                  ((r[1:N] + dr / 2) ** (pg + 1) - (r[1:N] - dr / 2) ** (pg + 1)) / (pg + 1))) * (
            (r[1:N] + dr / 2) ** pg * kk[1:N] * (T[2:] - T[1:N]) / dr
            - (r[1:N] - dr / 2) ** pg * kk[:N - 1] * (T[1:N] - T[:N - 1]) / dr)
        # 中心（球：6α/Δr²；柱：4α/Δr²）
        coefC = 6.0 if pg == 2 else 4.0
        Tn[0] = T[0] + (coefC * kk[0] * dt / (rho[0] * cp[0] * dr ** 2)) * (T[1] - T[0])
        # 表面：准稳态 Robin 边界节点
        Tn[N] = (kk[N] * Tn[N - 1] + h * dr * Ta) / (kk[N] + h * dr)
        Cn = C.copy()
        Cn[1:N] = C[1:N] + (dt / (((r[1:N] + dr / 2) ** (pg + 1) -
                                   (r[1:N] - dr / 2) ** (pg + 1)) / (pg + 1))) * (
            (r[1:N] + dr / 2) ** pg * DD[1:N] * (C[2:] - C[1:N]) / dr
            - (r[1:N] - dr / 2) ** pg * DD[:N - 1] * (C[1:N] - C[:N - 1]) / dr)
        coefD = 6.0 if pg == 2 else 4.0
        Cn[0] = C[0] + (coefD * DD[0] * dt / dr ** 2) * (C[1] - C[0])
        Cn[N] = (DD[N] * Cn[N - 1] + km * dr * Cenv) / (DD[N] + km * dr)
        T, C = Tn, np.maximum(Cn, 0.0)
        Tmax_hist.append(T.max())
    return T, C, np.array(Tmax_hist)


def main():
    say('=' * 100)
    say('补充实验：机构《GT04》Q1 公布值（中心 47.3203 / 表面 48.5448 ℃）的复现尝试')
    say('=' * 100)
    a = 0.36 / (820 * 2600)
    for N, dt in [(20, 1.0), (20, 0.125), (40, 0.25)]:
        dr = 0.02 / N
        say(f'N={N}（Δr={dr*1e3:.3f} mm） Δt={dt:g} s ：柱 4αΔt/Δr²={4*a*dt/dr**2:.4f}'
            f'（限 ≤1）；球 6αΔt/Δr²={6*a*dt/dr**2:.4f}（限 ≤1）')
    say('')
    say(f'{"几何":<8s} {"物性":<10s} {"边界":<14s} {"Δt/s":>6} {"T(0,1800)":>11} {"T(R,1800)":>11} {"max_t T":>10} {"C(0)":>8} {"C(R)":>8}')
    cases = [
        ('柱 p=1', 'q1', 50.0, 1.0), ('球 p=2', 'q1', 50.0, 1.0),
        ('球 p=2', 'q2', 50.0, 1.0), ('球 p=2', 'q1', 41.5130, 1.0),
        ('球 p=2', 'q1', 50.0, 0.125), ('柱 p=1', 'q1', 50.0, 0.125),
    ]
    for g, pr, Ta, dt in cases:
        pg = 2 if g.startswith('球') else 1
        T, C, Tm = explicit(pg, prop=pr, Tamb=Ta, dt=dt)
        say(f'{g:<8s} {pr:<10s} {"恒定 %.4f"%Ta:<14s} {dt:6g} {T[0]:11.4f} {T[-1]:11.4f} '
            f'{Tm.max():10.4f} {C[0]:8.4f} {C[-1]:8.4f}')
    say('')
    say('判读：① 球 + Δt=1 s 时 6αΔt/Δr² = 1.0132 > 1，中心节点落在显式稳定域之外；')
    say('      ② 把 Δt 缩到 0.125 s 即恢复稳定，可对比两次结果是否一致；')
    say('      ③ 无论何种几何/物性/边界组合，只要格式稳定，1800 s 的药材温度都不可能超过同刻烘房温度。')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
