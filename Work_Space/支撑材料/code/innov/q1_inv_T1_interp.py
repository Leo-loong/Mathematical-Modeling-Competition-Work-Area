# -*- coding: utf-8 -*-
"""T1-4 边界插值口径对照：线性插值（现行） vs PCHIP（单调三次）

现行口径 L3-06：$T_\\infty(t),C_\\infty(t)$ 一律**线性插值**、**不动原始数据**。
本项量化"若改用 PCHIP 会差多少"，结论用于"数据说明"节；**不替换原始数据、不改交付口径**。

运行：python q1_inv_T1_interp.py
"""
import os
import numpy as np
from scipy.interpolate import PchipInterpolator

from q1_inv_lib import Rec, env_fns
import q1_core as core

rec = Rec('q1_inv_T1_interp.log')
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
RHO = [0.0, 0.25, 0.5, 0.75, 1.0]


def run(t, Tinf, Cinf, p, kind):
    if kind == 'linear':
        Tf = lambda s: float(np.interp(s, t, Tinf))
        Cf = lambda s: float(np.interp(s, t, Cinf))
    else:
        iT = PchipInterpolator(t, Tinf)
        iC = PchipInterpolator(t, Cinf)
        Tf = lambda s: float(iT(s))
        Cf = lambda s: float(iC(s))
    res, _, _ = core.run_sim_collect(
        N=80, dr=0.25e-3, dt_out=1.0, nsteps=1800, p=p,
        Tenv_fn=Tf, Cenv_fn=Cf,
        sub=10, subT=1, cols=np.arange(0, 81, 4), snap_at=set(SNAP))
    return res


def main():
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(core.DEF)
    rec('=== T1-4 边界插值口径对照（线性 vs PCHIP）===')
    rec('注：两者都**只作用于连续化**，节点处均严格复现原始数据；不改动附件1 原始序列。')
    rec('')
    rl = run(t, Tinf, Cinf, p, 'linear')
    rp = run(t, Tinf, Cinf, p, 'pchip')
    idx = [int(round(r * 0.02 / 0.25e-3)) for r in RHO]
    dT = dC = 0.0
    for s in SNAP:
        dT = max(dT, float(np.max(np.abs(rl['T_snap'][s][idx] - rp['T_snap'][s][idx]))))
        dC = max(dC, float(np.max(np.abs(rl['C_snap'][s][idx] - rp['C_snap'][s][idx]))))
    rec('终端（1800 s）关键量对照：')
    rec('  %-14s %14s %14s' % ('量', '线性(现行)', 'PCHIP'))
    rec('  %-14s %14.6f %14.6f' % ('T(0)', rl['T_end'][0], rp['T_end'][0]))
    rec('  %-14s %14.6f %14.6f' % ('T(R)', rl['T_end'][-1], rp['T_end'][-1]))
    rec('  %-14s %14.6f %14.6f' % ('C(0)', rl['C_end'][0], rp['C_end'][0]))
    rec('  %-14s %14.6f %14.6f' % ('C(R)', rl['C_end'][-1], rp['C_end'][-1]))
    rec('')
    rec('全场最大差：|ΔT| = %.3e ℃ ; |ΔC| = %.3e kg/kg' % (dT, dC))
    rec('')
    rec('结论：插值口径对 4 位小数输出的影响%s（阈值：T 1e-4 ℃／C 5e-5 kg/kg）。'
        % ('可忽略' if (dT < 1e-4 and dC < 5e-5) else '可辨识'))
    rec('     现行**线性插值、不动原始数据**的立场保守且可交代 ⟹ **口径不变**。')
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
