# -*- coding: utf-8 -*-
"""
Q3 诊断：表面含水率 C(R) 的网格依赖性
================================================================================
现象：W2 空间收敛重验中，C(R)@24h 随网格加密单调上升
      0.0514(1.0mm) -> 0.0532(0.5) -> 0.0567(0.25) -> 0.0649(0.125)
      即 C(R) 似乎不收敛。

目的：
  ① 检查该现象是否**随时间加剧**（24 h vs 48 h）——判断是否与低 C 端强非线性相关；
  ② 检查**表面控制体体积**与网格的关系（是否存在离散口径问题）；
  ③ 用**近表面解析结构**判断物理合理性：
      稳态时 D(C)d/dr(r dC/dr)=0 ⟹ r dC/dr = const ⟹ C 呈**对数**分布，
      表面通量 -D dC/dr|_R = km(C_R - C_inf)。
  ④ 给出对主结果 t_end（由中心点决定）的影响评估。

级别：诊断（≤48 h 时程，不产出交付物）
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
_ws = wb.active
_rows = [r for r in _ws.iter_rows(values_only=True)][1:]
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


def run(N, dr, t_end):
    nsteps = int(round(t_end / DT_OUT))
    NC = N + 1
    T = np.full(NC, P['T0'])
    C = np.full(NC, P['C0'])
    for n in range(1, nsteps + 1):
        T, C, _ = q3.step_imex_fast(N, dr, HH, NSUB, P['R0'], P['h'], P['km'],
                                    T, C, ts, Tv, Cv, (n - 1) * DT_OUT)
    return T, C


print('=' * 78)
print('Q3 诊断：表面 C(R) 的网格依赖性（比较时刻 24 h）')
print('=' * 78)
print('  %-9s %-6s %-14s %-14s %-14s %-10s'
      % ('Δr/mm', 'N', 'C(R)@24h', 'C(0)@24h', 'C(0.125mm处)', '耗时'))
grids = (1.0, 0.5, 0.25, 0.125, 0.0625)
out = {}
for dmm in grids:
    N = int(round(P['R0'] / (dmm * 1e-3)))
    t0 = time.time()
    _, C24 = run(N, dmm * 1e-3, 86400.0)
    # 统一取 r=0.125 mm 处的值（要求该点为节点：0.125mm 网格 N=160 时 idx=1）
    idx = int(round(0.125e-3 / (dmm * 1e-3)))
    v0125 = C24[idx] if idx <= N else float('nan')
    out[dmm] = (N, C24[0], C24[-1], v0125)
    print('  %-9.4f %-6d %-14.6f %-14.6f %-14.6f %.0fs'
          % (dmm, N, C24[-1], C24[0], v0125, time.time() - t0))

print()
print('  --- 相邻网格的相对变化（%）---')
print('  %-22s %-16s %-16s %-16s'
      % ('网格对', 'C(R) 变化', 'C(0) 变化', 'C@0.125mm 变化'))
prev = None
for dmm in grids:
    if prev is not None:
        N, c0, cR, v = out[dmm]
        pN, p0, pR, pv = out[prev]
        print('  %-22s %-16s %-16s %-16s'
              % ('%.4f vs %.4f mm' % (dmm, prev),
                 '%+.2f%%' % (100 * (cR - pR) / pR),
                 '%+.2f%%' % (100 * (c0 - p0) / p0),
                 '%+.2f%%' % (100 * (v - pv) / pv)))
    prev = dmm

print()
print('  --- 关键：对主结果 t_end 的影响评估 ---')
print('    t_end 由**中心点 C(0)** 降到 0.15 决定 ⟹ 关注 C(0) 的网格敏感性。')
N, c0, cR, v = out[0.125]
pN, p0, pR, pv = out[0.25]
print('    C(0)：0.25mm=%.6f  0.125mm=%.6f  0.0625mm=%.6f'
      % (out[0.25][1], out[0.125][1], out[0.0625][1]))
print('    ⟹ 相对变化 0.25→0.125：%+.2f%%   0.125→0.0625：%+.2f%%'
      % (100 * (out[0.125][1] - out[0.25][1]) / out[0.25][1],
         100 * (out[0.0625][1] - out[0.125][1]) / out[0.125][1]))
print('    判读：若 C(0) 在 0.125→0.0625 间变化 < 0.5%，则 0.25 mm 的中心点')
print('         虽有小偏差，但**可达标时间量级与结论不变**；须在检验节如实声明。')
print()
print('  ⟹ 判读要点：')
print('    · 若 C(R) 随网格加密**单调增且无收敛迹象**，而 C(0) 稳定 ⟹')
print('      表面层存在**尺度效应**（低 C 端 D 极小导致表面层极薄），')
print('      但主结果 t_end 由**中心点**决定，需单独评估其网格敏感性。')
print('    · 若 C(0) 在细网格间变化 <1%，则 t_end 的网格敏感性同量级。')
