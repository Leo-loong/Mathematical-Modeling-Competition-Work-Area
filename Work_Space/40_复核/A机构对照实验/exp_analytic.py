# -*- coding: utf-8 -*-
"""
Q1 补充实验：把"解析基准差异"拆成 几何效应 / D(C) 非线性 / 时变边界 三个来源
==============================================================================
用我方 Q1 求解核（只读调用）依次做三组：
  ① D≡D(C0)、C∞≡0.01963（= 半无限解析解的严格同题）→ 差异只来自"圆柱 vs 半无限平面"
  ② D=D(C)、C∞≡0.01963                                → 再加上 D(C) 非线性
  ③ D=D(C)、C∞=C∞(t)（真实）                           → 再加上时变边界
把每一组在 t=100…1800 s 的表面含水率与半无限 erfc 解析解对比。
"""
import io
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import make_env, semi_infinite_C, T1, TAIR, CAIR, find_root

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
import q1_core as our_core        # noqa: E402

OUT = os.path.join(HERE, 'exp_analytic_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def main():
    Tle, Cle = make_env('linear')
    p = dict(our_core.DEF)
    N, dr = 80, 0.02 / 80
    D0 = 7e-9 * np.exp(-0.89 / 2.55)
    km = 8e-7
    C_AIR0 = 0.01963
    SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
    Tenvf = lambda s: float(np.interp(s, T1, TAIR))     # Q1 温度场与传质无关，随便给
    const_c = lambda s: C_AIR0

    runs = [
        ('① D≡D(C0)、C∞≡0.01963（解析同题）', dict(dmode='const'), const_c, D0),
        ('② D=D(C)、C∞≡0.01963', dict(dmode='func'), const_c, D0),
        ('③ D=D(C)、C∞=C∞(t)（真实）', dict(dmode='func'), Cle, D0),
    ]
    say('=' * 100)
    say('Q1：半无限解析基准 vs 我方圆柱解 —— 差异来源分解（N=80，Δr=0.25 mm）')
    say('=' * 100)
    say(f'D(C0=2.55) = {D0:.5e} m²/s ； km = {km:g} m/s ； Bi_m = km·R0/D = {km*0.02/D0:.5f}')
    say('')
    for name, kw, Cenv, Dref in runs:
        r = our_core.run_sim(N=N, dr=dr, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenvf, Cenv_fn=Cenv, sub=10, subT=32,
                             center='fv', surf='fvm', snap_at=set(SNAP), **kw)
        say(f'--- {name} ---')
        say(f'{"t/s":>6} {"圆柱解 C(R,t)":>14} {"半无限 erfc（D(C0)）":>20} {"半无限 erfc（D 迭代修正）":>22} {"差值①-②":>12}')
        for s in SNAP:
            ca = float(Cenv(s))
            a1 = float(semi_infinite_C(np.array([float(s)]), D0, km, 2.55, ca)[0])
            Cm = 0.5 * (a1 + 2.55)
            D1 = 7e-9 * np.exp(-0.89 / Cm)
            a2 = float(semi_infinite_C(np.array([float(s)]), D1, km, 2.55, ca)[0])
            v = float(r['C_snap'][s][-1])
            say(f'{s:6d} {v:14.4f} {a1:20.4f} {a2:22.4f} {v-a2:12.4f}')
        say('')
    say('说明：① 组与解析解是"同一个数学问题"（常 D、常边界），两者之差即"圆柱几何 vs 半无限平面"的效应；')
    say('      100 s 时渗透深度 √(Dt)=0.70 mm 仅为半径的 3.5%，几何效应可忽略，故 ① 组应几乎重合。')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
