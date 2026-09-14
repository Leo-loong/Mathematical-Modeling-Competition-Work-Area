# -*- coding: utf-8 -*-
"""
Q2 创新 · 交付容限的**收敛充分性**裁决：现行 tol=1e-10 是否已足够？
==================================================================
由来
  `q2_inv_tol_delivery.py` 在**交付口径**（3 h / n_sub=32 / 时变边界）下发现：
  tol 由 1e-10 放宽到 1e-09，含水率整表最大差达 **1.568e-04**（超 4 位小数最小位 3.1 倍），
  C(R,3h) 由 1.008113 变为 1.008212 ⟹ **不可放宽**。
  （⟹ INV-Q2-2 在 1 h／恒定边界下的"可放宽"结论**不可外推**。）

随之而来的关键问题
  若每放松一个数量级即带来 ~1e-4 量级的解偏移，则**必须反问：现行 1e-10 自己收敛了吗？**
  本实验即回答此问题——对 tol 做**由松到严**的扫描，以**最严档为参考**逐格比对。

口径：完全等同交付（N=80 / dt_out=1 s / n_sub=32 / 时变边界 / mode=coupled / ω=0.7 / maxit=30）
      单变量隔离：**只变 tol**。

判据
  · 若某档与最严档逐格差 ≤5e-05（4 位小数最小位）⟹ 该档**已收敛**，可作交付容限；
  · 现行 1e-10 若满足 ⟹ 交付数值**站得住**（本轮结论：放宽不可行，但现口径安全）；
  · 现行 1e-10 若不满足 ⟹ **交付口径本身未收敛**，须收紧并重出交付文件（重大）。

输出：`logs/q2_inv_tol_converge.log`
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

import q2_solver as S
from q2_core_c import run_q2

LOG = os.path.join(HERE, 'logs', 'q2_inv_tol_converge.log')
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


TOLS = [1e-9, 1e-10, 1e-11, 1e-12]
TH = 5e-5

say('=' * 78)
say('Q2 创新 · 交付容限收敛充分性裁决：现状 tol=1e-10 是否足够收敛？')
say('=' * 78)
say('交付口径：N=%d（Δr=%.2f mm）/ dt_out=%.0f s / n_sub=%d / mode=coupled / ω=0.7 / maxit=30'
    % (S.N, S.DR * 1e3, S.DT_OUT, S.NSUB))
say('          时程 %d 步 = %g h / 时变边界（附件1）＋ H6 外推'
    % (S.NSTEP, S.NSTEP * S.DT_OUT / 3600.0))
say('单变量隔离：**只变 tol**；参考档 = 最严档 %s' % ('%.0e' % TOLS[-1]))
say('')

R = {}
for tol in TOLS:
    res, TT, CC, w = run(tol)
    R[tol] = (res, TT, CC, w)
    say('tol=%.0e  墙钟 %6.1f s   内层均 %5.2f 次/子步   残差统计 %.2e'
        % (tol, w, res['stats']['inner_tot'] / max(1, res['stats']['nsub']) / S.NSUB,
           res['stats']['resC_max']))

REF = TOLS[-1]
_, TREF, CREF, _ = R[REF]

say('')
say('【与最严档（tol=%.0e）的逐格差】阈值 = %.0e（4 位小数最小位）' % (REF, TH))
say('  %-9s %-13s %-15s %-10s' % ('tol', 'max|ΔT|/℃', 'max|ΔC|/(kg/kg)', '判定'))
VERD = {}
for tol in TOLS[:-1]:
    _, TT, CC, _ = R[tol]
    dT = float(np.max(np.abs(TT - TREF)))
    dC = float(np.max(np.abs(CC - CREF)))
    ok = (dT <= TH) and (dC <= TH)
    VERD[tol] = ok
    say('  %-9.0e %-13.3e %-15.3e %-10s' % (tol, dT, dC, '一致' if ok else '**有差**'))

say('')
say('【表3/表4 含水率关键值随 tol 的变化】（对照 4 位小数输出）')
say('  %-6s | %-33s | %-33s' % ('t/h', 'C(0) / C(R)  tol=%.0e' % REF, 'C(0) / C(R)  tol=1e-10'))
for s_ in S.SNAP:
    i = s_ - 1
    say('  %-6.1f | %11.6f / %11.6f     | %11.6f / %11.6f'
        % (s_ / 3600.0, CREF[i][0], CREF[i][-1], R[1e-10][2][i][0], R[1e-10][2][i][-1]))

say('')
say('【裁决】')
if VERD.get(1e-10, False):
    say('  · 现行交付容限 tol=1e-10 与最严档（%.0e）**逐格一致（≤%.0e）**' % (REF, TH))
    say('    ⟹ **交付数值已收敛，站得住**；1e-10 不是"保守冗余"而是**临界必要档**。')
    say('  · 放宽至 1e-09 **不可行**（见 `q2_inv_tol_delivery.log`：ΔC=1.568e-04）。')
    say('  · ⟹ **结论：交付容限维持 1e-10 不变，`result2.xlsx` 无需重出。**')
else:
    say('  · ⚠⚠ 现行 tol=1e-10 **与最严档不一致** ⟹ **交付口径本身未收敛**！')
    say('    ⟹ 须收紧容限、重出 `result2.xlsx`，并同步全部文档口径（重大修订）。')
say('')
say('总耗时 %.0f s' % sum(R[t][3] for t in TOLS))
flush()
