# -*- coding: utf-8 -*-
"""
Q3 网格裁决实验：确定"够用且最省"的网格
================================================================================
背景：W2 重验（**修正口径前的留痕**）曾显示 C(R) 随网格加密单调上升且未收敛，
     而主结果 t_end 由**中心点**决定（C(0) 在 0.125→0.0625 间仅变 0.08%）。
     ⚠ 界面口径修正（M6）后本脚本已复跑；**现行结论以本日志与《A_数值口径总表》§10.3 为准**。

判据重新校准（关键）：
  Q2 用的是"关键量相对变化 < 5e-5"（针对**解本身的收敛**）；
  但 Q3 的**交付要求是表 5 与 result3 的 4 位小数输出** ⟹ 真正的判据是
  **相邻网格的变化不得影响第 4 位小数**，即相对变化 ≲ 0.1%（对 C~0.05 而言）。

实验：
  · 网格序列：0.25 / 0.125 / 0.0625 / 0.03125 mm（N=80/160/320/640）
  · 比较时刻：24 h（省时；且已进入降速段，对离散误差敏感）
  · 逐列检查**表 5 用到的位置**：0 / 0.5 / 1.0 / 1.5 / 2.0 cm
    以及 result3 的 0.1 cm 首列
  · 输出：各列的相邻网格相对变化 ⟹ 判定"满足 <0.1% 的最粗网格"

用法：python q3_grid_experiment.py
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))
import q2_core_c as base          # noqa: E402
import q3_core as q3              # noqa: E402

WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
wb = openpyxl.load_workbook(os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'),
                            data_only=True)
_sh = wb.active
_rows = [r for r in _sh.iter_rows(values_only=True)][1:]
_d = [r for r in _rows if r[0] is not None]
ts, Tv, Cv = q3.env_tables_from_att1(
    np.array([float(r[0]) for r in _d]),
    np.array([float(r[1]) for r in _d]),
    np.array([float(r[2]) for r in _d]))
wb.close()

P = base.DEF2
DT_OUT = 60.0
H_IN = 1.0 / 32.0
NSUB = int(round(DT_OUT / H_IN))
HH = DT_OUT / NSUB
R0 = P['R0']
T_CMP = 86400.0                    # 24 h

GRIDS = (25.0, 12.5, 6.25, 3.125)  # 单位 1e-5 m：0.25/0.125/0.0625/0.03125 mm
PTS = (0.0, 0.5, 1.0, 1.5, 2.0)    # cm —— 表 5 用到的位置


def run(N, dr):
    nsteps = int(round(T_CMP / DT_OUT))
    NC = N + 1
    T = np.full(NC, P['T0'])
    C = np.full(NC, P['C0'])
    for n in range(1, nsteps + 1):
        T, C, _ = q3.step_imex_fast(N, dr, HH, NSUB, R0, P['h'], P['km'],
                                    T, C, ts, Tv, Cv, (n - 1) * DT_OUT)
    return C


print('=' * 82)
print('Q3 网格裁决实验（比较时刻 %.0f h）' % (T_CMP / 3600.0))
print('=' * 82)
print('  判据：相邻网格的**相对变化 < 0.1%%**（对应 4 位小数输出的可靠性）')
print()

res = {}
for g in GRIDS:
    dr = g * 1e-5
    N = int(round(R0 / dr))
    t0 = time.time()
    C = run(N, dr)
    vals = []
    for p in PTS:
        idx = int(round(p * 1e-2 / dr))
        idx = min(idx, N)
        vals.append(C[idx])
    res[g] = (N, vals, C[0])
    print('  Δr=%-9.5f mm  N=%-4d  耗时 %5.1f s   C(0)=%.6f'
          % (g / 100.0, N, time.time() - t0, C[0]))

print()
print('  各位置的值：')
print('  %-12s %-11s %-11s %-11s %-11s %-11s'
      % ('Δr/mm', '0cm', '0.5cm', '1.0cm', '1.5cm', '2.0cm'))
for g in GRIDS:
    N, v, c0 = res[g]
    print('  %-12.5f %-11.6f %-11.6f %-11.6f %-11.6f %-11.6f'
          % (g / 100.0, v[0], v[1], v[2], v[3], v[4]))

print()
print('  相邻网格的相对变化（%，以更细者为基准）：')
hdr = ['0cm', '0.5cm', '1.0cm', '1.5cm', '2.0cm']
print('  %-24s %s' % ('网格对', '  '.join('%-9s' % h for h in hdr)))
prev = None
for g in GRIDS:
    if prev is not None:
        v = res[g][1]
        pv = res[prev][1]
        chg = [100.0 * (v[i] - pv[i]) / pv[i] for i in range(len(PTS))]
        flags = ['%.3f' % c for c in chg]
        worst = max(abs(c) for c in chg)
        print('  %-24s %s   worst=%.3f%%  %s'
              % ('%.5f vs %.5f' % (g / 100.0, prev / 100.0),
                 '  '.join('%-9s' % f for f in flags), worst,
                 'PASS' if worst < 0.1 else '未达'))
    prev = g

print()
print('  ★ 判定逻辑：从细到粗找"满足 worst<0.1% 的最粗网格"⟹ 该网格即"够用且最省"。')
print('  ⚠ 若 0.03125 mm 仍未达 0.1%，说明**均匀网格**代价过高，')
print('     应改用**表面加密的非均匀网格**（作为改进方向）。')
