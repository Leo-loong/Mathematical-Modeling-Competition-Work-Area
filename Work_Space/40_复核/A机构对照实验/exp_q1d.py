# -*- coding: utf-8 -*-
"""
Q1 复核（续）：把 C(R,1800) 的"网格极限值"钉死，并检验登记值 1.510332 的可能来源
=================================================================================
· 网格极限：q1_core N=320 与 BDF N=320 两条独立路径
· 口径排查：主力同网格(N=80)下切换表面离散（精确半格 / 一阶近似 ghost）与界面平均方式
"""
import io
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import bdf_mol, make_env, T1, TAIR, CAIR, find_root

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
import q1_core as our_core        # noqa: E402

OUT = os.path.join(HERE, 'exp_q1d_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def main():
    p = dict(our_core.DEF)
    Tenv = lambda s: float(np.interp(s, T1, TAIR))
    Cenv = lambda s: float(np.interp(s, T1, CAIR))
    Tle, Cle = make_env('linear')

    say('=' * 96)
    say('Q1 复核（续）：C(R,1800) 网格极限与口径排查')
    say('=' * 96)

    # ---- 网格极限 ----
    say('[A] 我方主力核 q1_core（sub=10，Δt_int=0.1 s，主力同口径）网格序列')
    for N in (80, 160, 320):
        t1 = time.time()
        r = our_core.run_sim(N=N, dr=0.02 / N, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                             center='fv', surf='fvm')
        v = float(r['C_end'][-1])
        say(f'   N={N:4d}  Δr={0.02/N*1e3:7.4f} mm   C(R,1800)={v:.10f}  → 4 位 {round(v,4):.4f}  ({time.time()-t1:.0f}s)')

    say('')
    say('[B] 第三方 BDF 参考（自适应步长、与 A 完全不同的算法）')
    for N in (80, 160, 320):
        t1 = time.time()
        r = bdf_mol(N, 0.02, 1800.0, Tle, Cle, prop='q1', ifmode='integral',
                    dt_samp=1.0, rtol=1e-11, atol=1e-13)
        v = float(r['C'][-1][-1])
        say(f'   N={N:4d}  Δr={0.02/N*1e3:7.4f} mm   C(R,1800)={v:.10f}  → 4 位 {round(v,4):.4f}  ({time.time()-t1:.0f}s)')

    say('')
    say('[C] 主力同网格 N=80 下切换口径（排查登记值 1.510332 的来源）')
    for tag, surf in [('精确半格 fvm（当前主力）', 'fvm'), ('一阶近似 ghost（对照口径）', 'ghost')]:
        r = our_core.run_sim(N=80, dr=0.00025, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                             center='fv', surf=surf)
        v = float(r['C_end'][-1])
        say(f'   {tag:<28s} C(R,1800)={v:.10f}  → 4 位 {round(v,4):.4f}')
    say('')
    say('参照：《A_Q1求解记录》登记 全精度 1.510332（→1.5103）；交付文件 result1.xlsx 实测 1.5104')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
