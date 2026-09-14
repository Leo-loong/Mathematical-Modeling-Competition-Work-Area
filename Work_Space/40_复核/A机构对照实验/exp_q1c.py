# -*- coding: utf-8 -*-
"""
Q1 复核：我方已发布表2 第 4 位小数的可复现性核查
==================================================
背景：复核实验用 q1_core 复算 N=80 时得到 C(R,1800)=1.510381（4 位小数 → 1.5104），
      而《A_Q1求解记录》§4.3／§九 登记为 1.510332（→ 1.5103）。两者相差 4.9e-5，
      恰好跨在第 4 位小数的进位边界（1.51035）两侧。本实验判定哪个可复现。
"""
import io
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import T1, TAIR, CAIR, find_root

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
import q1_core as our_core        # noqa: E402

OUT = os.path.join(HERE, 'exp_q1c_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def main():
    p = dict(our_core.DEF)
    N, dr = 80, 0.00025
    Tenv = lambda s: float(np.interp(s, T1, TAIR))
    Cenv = lambda s: float(np.interp(s, T1, CAIR))
    say('=' * 96)
    say('Q1 复核：C(R,1800) 第 4 位小数的可复现性')
    say('=' * 96)
    say(f'{"调用":<34s} {"sub":>4} {"Δt_int/s":>10} {"C(R,1800) 全精度":>22} {"4 位":>8}')
    for sub in (1, 2, 4, 8, 10, 20, 40):
        r = our_core.run_sim(N=N, dr=dr, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, sub=sub, subT=32,
                             center='fv', surf='fvm')
        v = float(r['C_end'][-1])
        say(f'{"run_sim":<34s} {sub:4d} {1.0/sub:10.4f} {v:22.10f} {round(v,4):8.4f}')
    # 与主力完全相同的调用路径
    res, tabT, tabC = our_core.run_sim_collect(
        N=N, dr=dr, dt_out=1.0, nsteps=1800, p=p, Tenv_fn=Tenv, Cenv_fn=Cenv,
        sub=10, subT=32, center='fv', surf='fvm', tol=1e-9, omega=0.7, maxit=30,
        cols=np.arange(0, N + 1, 4), snap_at={300, 1800})
    v = float(res['C_end'][-1])
    say(f'{"run_sim_collect（主力同路径）":<34s} {10:4d} {0.1:10.4f} {v:22.10f} {round(v,4):8.4f}')
    say('')
    say('《A_Q1求解记录》E1-c 的时间收敛表（原文照录）：')
    say('   1 s → 1.5104056508 ｜ 0.5 s → 1.5103626682 ｜ 0.25 s → 1.5103412843 ｜ 0.125 s → 1.5103338247')
    say('   登记的主力全精度值（§4.3/§九，v5）＝ 1.510332 / 1.5103323')
    say('')
    say('判读要点：第 4 位小数进位边界为 1.510350。')
    say('  · 若复算值落在边界之下（≈1.510332）→ 表值 1.5103 正确；')
    say('  · 若落在边界之上（≈1.510381）→ 表值应为 1.5104。')
    say('  · 数值解在 Δt→0 时的极限由时间收敛序列外推得到；请对照上面实测序列判断。')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
