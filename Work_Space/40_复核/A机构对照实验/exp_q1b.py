# -*- coding: utf-8 -*-
"""
Q1 补充实验：把"时间步误差"与"表面边界格式误差"彻底分离
=========================================================
在机构同一网格（N=20，Δr=1 mm）上：
  ① 表面＝准稳态 Robin（机构原样）  ×  Δt = 1 / 0.1 / 0.01 / 0.0025 s
  ② 表面＝半格元体（含储能）        ×  Δt = 1 / 0.1 / 0.01 / 0.0025 s
若 ① 不随 Δt 收敛而 ② 收敛 → 误差来源就是"表面节点无储能"这一**格式缺陷**（与时间步无关）。
"""
import io
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import explicit_fv, make_env, T1, TAIR, CAIR, find_root

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
import q1_core as our_core        # noqa: E402

OUT = os.path.join(HERE, 'exp_q1b_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def main():
    Tex, Cex = make_env('pchip')
    Tle, Cle = make_env('linear')
    say('=' * 100)
    say('Q1 补充实验：时间步误差 vs 表面边界格式误差（N=20，Δr=1 mm，机构网格）')
    say('=' * 100)
    say(f'{"表面格式":<26s} {"Δt/s":>9} {"步数":>9} {"C(0)@1800":>11} {"C(1.5)@1800":>12} '
        f'{"C(R)@1800":>11} {"T(0)@1800":>10} {"T(R)@1800":>10}')
    for surf in ('quasi', 'halfcell'):
        for dt in (1.0, 0.1, 0.01, 0.0025):
            r = explicit_fv(20, 0.02, dt, 1800, 1.0, Tex, Cex, prop='q1',
                            surf=surf, ifmode='arith', quasi_use_new=True)
            say(f'{surf:<26s} {dt:9.4f} {int(1800/dt):9d} {r["C"][-1][0]:11.6f} '
                f'{r["C"][-1][15]:12.6f} {r["C"][-1][20]:11.6f} '
                f'{r["T"][-1][0]:10.4f} {r["T"][-1][20]:10.4f}')
    say('')
    # 我方求解核（N=20 与 N=80）作为"网格内 时间已收敛"的参照
    p = dict(our_core.DEF)
    Tenv = lambda s: float(np.interp(s, T1, TAIR))
    Cenv = lambda s: float(np.interp(s, T1, CAIR))
    for N in (20, 80):
        dr = 0.02 / N
        r = our_core.run_sim(N=N, dr=dr, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                             center='fv', surf='fvm')
        say(f'我方核(全隐式,Δt=1/32)      N={N:<3d}  Δr={dr*1e3:.4f} mm  '
            f'{"":>9} {r["C_end"][0]:11.6f} {r["C_end"][int(round(.015/dr))]:12.6f} '
            f'{r["C_end"][-1]:11.6f} {r["T_end"][0]:10.4f} {r["T_end"][-1]:10.4f}')
    say('')
    # 早期时刻的解析基准（半无限介质 + 常边界 erfc 精确式；t 越小与"时变边界+有限半径"的偏差越小）
    from exp_common import semi_infinite_C
    say('半无限介质 Robin 解析解（erfc 精确式；用 ΔC 区间的 D 平均做一次迭代修正）：')
    say(f'{"t/s":>7} {"C_air(t)":>9} {"解析 C(0,t)":>12}')
    for s in (100, 300, 600, 900):
        ca = float(np.interp(s, T1, CAIR))
        D0 = 7e-9 * np.exp(-0.89 / 2.55)
        c1 = float(semi_infinite_C(np.array([float(s)]), D0, 8e-7, 2.55, ca)[0])
        Cm = 0.5 * (c1 + 2.55)
        D1 = 7e-9 * np.exp(-0.89 / Cm)
        c2 = float(semi_infinite_C(np.array([float(s)]), D1, 8e-7, 2.55, ca)[0])
        say(f'{s:7d} {ca:9.5f} {c2:12.4f}')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
