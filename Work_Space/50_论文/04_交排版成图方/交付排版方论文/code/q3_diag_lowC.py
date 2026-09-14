# -*- coding: utf-8 -*-
"""
Q3 诊断：低含水率端（D 极小）的 Picard 收敛行为
================================================
目的：查明主力求解中"内层最大残差 1.386e-04（tol=1e-10）"的来源，
     并确认低 C 端是否出现 Picard 跑满 maxit 的截断现象（类似 Q2 的 F-1）。

做法：取若干代表性 C 值（均匀场），各推进 200 个内部子步，
     统计每子步的 Picard 迭代次数与末端残差。

级别：T1（≤60 s 时程；不产出交付物；标 SMOKE）
"""
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))
import q2_core_c as base          # noqa: E402
import q3_core as q3              # noqa: E402

WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
_ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
wb = openpyxl.load_workbook(_ATT1, data_only=True)
_ws = wb.active
_rows = [r for r in _ws.iter_rows(values_only=True)][1:]
_d = [r for r in _rows if r[0] is not None]
t_a1 = np.array([float(r[0]) for r in _d])
T_a1 = np.array([float(r[1]) for r in _d])
C_a1 = np.array([float(r[2]) for r in _d])
wb.close()
ts, Tv, Cv = q3.env_tables_from_att1(t_a1, T_a1, C_a1)

NC, N, DR = 81, 80, 2.5e-4
HH = 1.0 / 32.0
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']

print('[SMOKE] ============================================================')
print('[SMOKE] Q3 诊断：低含水率端的 Picard 收敛行为')
print('[SMOKE] ============================================================')
print('[SMOKE] 每档推进 200 个内部子步（时程 6.25 s），maxit=30, tol=1e-10')
print('[SMOKE]')
print('[SMOKE] %-10s %-13s %-24s %-14s %s'
      % ('C_典型', 'D(m2/s)', 'Picard 迭代（均/最大）', '末端残差', '判定'))

for Ctyp in (1.000, 0.300, 0.150, 0.100, 0.055, 0.020):
    Tc = np.full(NC, 50.0)
    Cc = np.full(NC, Ctyp)
    D = 2.4e-3 * np.exp(-0.45 / max(Ctyp, 1e-9)) * np.exp(-3850.0 / 323.15)
    its = []
    res_last = 0.0
    for k in range(200):
        Tc, Cc, info = q3.step_imex_fast(
            N, DR, HH, 1, R0, HC, KM, Tc, Cc, ts, Tv, Cv, 20000.0 + k * HH)
        its.append(info['inner_tot'])
        res_last = info['res_max']
    its = np.array(its)
    verdict = '跑满上限!' if its.max() >= 30 else 'OK'
    print('[SMOKE] %-10.4f %-13.3e %-24s %-14.3e %s'
          % (Ctyp, D, '均 %.1f / 最大 %d' % (its.mean(), its.max()),
             res_last, verdict))

print('[SMOKE]')
print('[SMOKE] 判据：若"最大"达到 30，说明该档 Picard **跑满上限**（未收敛）。')
print('[SMOKE] 本脚本未运行完整求解、未写出任何交付物。')
