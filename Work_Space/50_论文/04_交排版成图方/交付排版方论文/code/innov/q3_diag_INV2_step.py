# -*- coding: utf-8 -*-
"""
IN-2 诊断 | 单步／多步对照：CN（IN-2 独立实现） vs BE（主力 q3_core）
================================================================================
目的：IN-2 的 3 h 结果（C(0)=2.2864）与基线（1.7662）不符 ⟹ 定位差异来源：
  · 若**单步**差异即为 O(1e-3) ⟹ **装配/边界实现错误**；
  · 若单步差异 ~1e-5 但**多步累积**迅速放大 ⟹ 格式/稳定性问题。
用法：python q3_diag_INV2_step.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
import openpyxl


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
Q3DIR = os.path.dirname(HERE)
WS = _find_root(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, Q3DIR)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))

import q3_core as q3                                        # noqa: E402
import q3_e3_INV2_cn as inv2                                # noqa: E402

N = 80
DR = 2.5e-4
NSUB = 1920
HH = 60.0 / NSUB
R0, HC, KM = 0.02, 25.0, 8e-7

wb = openpyxl.load_workbook(os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'),
                            data_only=True)
sh = wb.active
rows = [r for r in sh.iter_rows(values_only=True)][1:]
d = [r for r in rows if r[0] is not None]
ta = np.array([float(r[0]) for r in d])
Ta = np.array([float(r[1]) for r in d])
Ca = np.array([float(r[2]) for r in d])
wb.close()
ts, Tv, Cv = q3.env_tables_from_att1(ta, Ta, Ca)
geo = inv2.Geo(N, DR)

print('=' * 84)
print('IN-2 诊断：CN（独立实现） vs BE（主力核），逐步对照')
print('=' * 84)
print('  %-6s %-12s %-12s %-12s %-12s %-11s %-11s'
      % ('输出步', 'C(0)_BE', 'C(0)_CN', 'C(R)_BE', 'C(R)_CN', 'max|ΔT|', 'max|ΔC|'))

Tb = np.full(N + 1, 28.0)
Cb = np.full(N + 1, 2.55)
Tc = np.full(N + 1, 28.0)
Cc = np.full(N + 1, 2.55)

for n in range(1, 6):
    t_start = (n - 1) * 60.0
    Tb, Cb, _ = q3.step_imex_fast(N, DR, HH, NSUB, R0, HC, KM, Tb, Cb, ts, Tv, Cv, t_start)[:3]
    for s in range(NSUB):
        tsx = t_start + (s + 1) * HH
        Tinf = 50.0 if tsx >= ta[-1] else float(np.interp(tsx, ta, Ta))
        Cinf = 0.04999 if tsx >= ta[-1] else float(np.interp(tsx, ta, Ca))
        Tc, Cc = inv2.step(geo, Tc, Cc, HH, Cinf, Tinf, theta=0.5)
    print('  %-6d %-12.6f %-12.6f %-12.6f %-12.6f %-11.3e %-11.3e'
          % (n, Cb[0], Cc[0], Cb[-1], Cc[-1],
             float(np.max(np.abs(Tb - Tc))), float(np.max(np.abs(Cb - Cc)))))

print('-' * 84)
print('  判读：')
print('   · 若第 1 步 max|ΔC| 已达 1e-3 量级 ⟹ **装配/边界实现错误**（CN 与 BE 的一步差应为 O(HH²)~1e-9）')
print('   · 若第 1 步 ~1e-9 而 5 步后迅速放大 ⟹ **稳定性/物性滞后问题**')
