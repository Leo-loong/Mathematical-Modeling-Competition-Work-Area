# -*- coding: utf-8 -*-
"""
Q2 创新 INV-Q2-2（后续）· **交付口径**容限裁决：内层 Picard tol 是否可放宽至 1e-09
================================================================================
背景
  INV-Q2-2（`q2_inv_tol_tradeoff.py`）测得"与最严档（1e-11）逐格一致的最松容限 = 1e-09"，
  但该实验口径为 **1 h 时程 / n_sub=16 / 恒定边界**，与交付口径不同，
  故原实验明确标注："替换交付口径须另行授权 + 四闸门（本实验仅覆盖 1 h 时程）"。

本实验（裁决，经授权执行）
  在 **交付口径**下重做单变量对照：
      3 h 全程 / n_sub=32 / **时变边界（附件1 实测）** / mode=coupled / ω=0.7 / maxit=30
  只变 tol：**1e-10（现行交付）** vs **1e-09（拟放宽）**
  判据：整表逐格最大差 ≤ 5e-05（4 位小数最小位）⟹ 一致，可放宽；否则不可放宽。

输出：`logs/q2_inv_tol_delivery.log`
"""
import io
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
Q2CODE = os.path.abspath(os.path.join(HERE, '..', 'code'))
sys.path.insert(0, Q2CODE)
os.environ.setdefault('Q2_CORE', 'c')
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import q2_solver as S                       # 复用交付口径常量与附件读取 ⟹ 输入完全一致
from q2_core_c import run_q2                # 交付核（C 版，M6 界面口径）

LOG = os.path.join(HERE, 'logs', 'q2_inv_tol_delivery.log')
_BUF = []


def say(s=''):
    print(s, flush=True)
    _BUF.append(s)


def flush():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with io.open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(_BUF) + '\n')


t1, T1, C1, _hdr = S.load_att1()


def Tenv(t):
    return float(np.interp(t, t1, T1)) if t <= t1[-1] else S.T_EXT


def Cenv(t):
    return float(np.interp(t, t1, C1)) if t <= t1[-1] else S.C_EXT


def run(tol):
    t0 = time.time()
    res, TT, CC = run_q2(N=S.N, dr=S.DR, dt_out=S.DT_OUT, nsteps=S.NSTEP,
                         Tenv_fn=Tenv, Cenv_fn=Cenv, n_sub=S.NSUB,
                         mode='coupled', cols=S.COLS, snap_at=S.SNAP,
                         omega=0.7, tol=tol, maxit=30, progress=10 ** 9)
    return res, np.asarray(TT), np.asarray(CC), time.time() - t0


say('=' * 78)
say('Q2 创新 · 交付口径容限裁决：内层 Picard tol 能否由 1e-10 放宽至 1e-09')
say('=' * 78)
say('交付口径：N=%d（Δr=%.2f mm）/ dt_out=%.0f s / n_sub=%d / mode=coupled / ω=0.7 / maxit=30'
    % (S.N, S.DR * 1e3, S.DT_OUT, S.NSUB))
say('          时程 %d 步 = %g h / 时变边界（附件1）＋ H6 外推（t>%d s）'
    % (S.NSTEP, S.NSTEP * S.DT_OUT / 3600.0, t1[-1]))
say('单变量隔离：**只变 tol**；其余一切相同')
say('')

r10, T10, C10, w10 = run(1e-10)
say('[A 现行交付 tol=1e-10] 墙钟 %6.1f s   内层均 %.2f 次/子步   残差统计 %.2e'
    % (w10, r10['stats']['inner_tot'] / max(1, r10['stats']['nsub']) / S.NSUB,
       r10['stats']['resC_max']))

r9, T9, C9, w9 = run(1e-09)
say('[B 拟放宽   tol=1e-09] 墙钟 %6.1f s   内层均 %.2f 次/子步   残差统计 %.2e'
    % (w9, r9['stats']['inner_tot'] / max(1, r9['stats']['nsub']) / S.NSUB,
       r9['stats']['resC_max']))

say('')
say('【整表逐格差】（以 A 为参考；表 10800×%d）' % len(S.COLS))
dT = float(np.max(np.abs(T9 - T10)))
dC = float(np.max(np.abs(C9 - C10)))
TH = 5e-5
say('  max|ΔT| = %.3e ℃      max|ΔC| = %.3e kg/kg' % (dT, dC))
say('  阈值（4 位小数最小位）= %.0e ⟹ 温度：%s   含水率：%s'
    % (TH, '一致' if dT <= TH else '**有差**', '一致' if dC <= TH else '**有差**'))

say('')
say('【表3/表4 取用时刻关键值】')
say('  %-6s | %-26s | %-26s' % ('t/h', 'A: T(0)/T(R) ℃', 'B: T(0)/T(R) ℃'))
for s_ in S.SNAP:
    i = s_ - 1
    say('  %-6.1f | %9.4f / %9.4f      | %9.4f / %9.4f'
        % (s_ / 3600.0, T10[i][0], T10[i][-1], T9[i][0], T9[i][-1]))
say('  %-6s | %-26s | %-26s' % ('t/h', 'A: C(0)/C(R)', 'B: C(0)/C(R)'))
for s_ in S.SNAP:
    i = s_ - 1
    say('  %-6.1f | %9.6f / %9.6f    | %9.6f / %9.6f'
        % (s_ / 3600.0, C10[i][0], C10[i][-1], C9[i][0], C9[i][-1]))

say('')
say('【裁决】')
ok = (dT <= TH) and (dC <= TH)
if ok:
    say('  · tol=1e-09 与现行 1e-10 在**交付口径整表**（%d×%d）上逐格一致（≤%.0e）' % (T10.shape[0], T10.shape[1], TH))
    say('    ⟹ **放宽安全**，可替换交付容限。')
    say('  · 墙钟 %.1f s → %.1f s ⟹ 省 **%.2f×**' % (w10, w9, w10 / w9))
    say('  · 交付数值 **不变**（4 位小数输出逐格不变）⟹ 论文表 3／表 4 与 `result2.xlsx` 无需改动。')
else:
    say('  · ⚠ 出现超阈值差异（ΔT=%.3e、ΔC=%.3e）⟹ **不可放宽**，交付容限维持 1e-10。' % (dT, dC))
say('')
say('总耗时 %.0f s' % (w10 + w9))
flush()
