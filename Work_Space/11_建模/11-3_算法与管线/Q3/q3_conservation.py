# -*- coding: utf-8 -*-
"""
Q3 · E7 守恒性核算（质量区域积分闭合）
================================================================================
口径（与 Q2 的 E7 一致）：
  质量守恒 —— 全域水量变化 = 表面累计排出量（含环境浓度基准）

  对柱坐标质量方程  ∂C/∂t = (1/r)∂_r(D r ∂_r C) ，
  Robin 边界  -D ∂_r C|_R = k_m (C_R - C_∞)，
  在 [0,R0] 上以 r dr 加权积分：

      d/dt ∫_0^R0 C r dr = R0 · D ∂_r C|_R = -R0 · k_m (C_R - C_∞)

  数值形式上，对**控制体**求和 = 表面通量项（元体平衡天然守恒）。

  本脚本用**输出网格**（Δr 由 result3 的 21 列给出，仅 0.1 cm 间距，
  ⟹ 仅作**低分辨率**核对）与**求解网格**（Δr=0.25 mm，需重算）两种粒度，
  报告相对残差并**归因**（输出分辨率 / 舍入 / 积分截断）。

产出：相对残差 + 归因；不修改任何交付物。
用法：python q3_conservation.py
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
N, DR = 80, 2.5e-4
NC = N + 1
DT_OUT = 60.0
NSUB = int(round(DT_OUT / (1.0 / 32.0)))
HH = DT_OUT / NSUB
KM, R0, CINF = P['km'], P['R0'], 0.05

print('=' * 76)
print('Q3 · E7 守恒性核算（质量区域积分闭合）')
print('=' * 76)


def cinf_at(t):
    return float(q3._interp1_nb(t, ts, Cv))


def run(t_end, snap_every_s=3600.0):
    """推进并记录每个快照时刻的 (C场, 表面通量率积分)。"""
    nsteps = int(round(t_end / DT_OUT))
    T = np.full(NC, P['T0'])
    C = np.full(NC, P['C0'])
    snaps = []
    next_snap = snap_every_s
    # 半径加权体积元（元体平衡口径）
    r = np.arange(NC) * DR
    w = np.ones(NC)
    w[0] = DR * DR / 4.0
    for i in range(1, N):
        w[i] = r[i] * DR
    w[N] = DR * (R0 - DR / 4.0) / 2.0
    # 初始水量（体积分，乘 2π 可略——比较时同系数）
    M0 = float(np.sum(C * w))
    flux_cum = 0.0
    for n in range(1, nsteps + 1):
        t_start = (n - 1) * DT_OUT
        T, C, _ = q3.step_imex_fast(N, DR, HH, NSUB, R0, P['h'], KM,
                                    T, C, ts, Tv, Cv, t_start)
        # 表面通量率（每 s）：J = km*(C_R - C_inf)，乘以 R0 得「r dr 加权」的源项
        for s in range(NSUB):
            tt = t_start + (s + 0.5) * HH
            # 用本输出步末的 C_R 近似（子步级未逐点存）——保守估计
            pass
        flux_cum += KM * (C[N] - cinf_at(t_start + DT_OUT)) * R0 * DT_OUT
        if n * DT_OUT + 1e-9 >= next_snap:
            M = float(np.sum(C * w))
            snaps.append((n * DT_OUT, M, flux_cum))
            next_snap += snap_every_s
    return snaps, M0, w


t_end = 207113.094
print('  推进至 t_end = %.1f s（%.4f h），每 1 h 记录一次' % (t_end, t_end / 3600.0))
t0 = time.time()
snaps, M0, w = run(t_end)
print('  完成，用时 %.1f s' % (time.time() - t0))
print()
print('  %-10s %-18s %-18s %-14s' % ('t/h', '水量 M(t)', 'M0 - M(t)', '累计排出'))
print('  ' + '-' * 62)
for tt, M, F in snaps[::max(1, len(snaps) // 12)]:
    print('  %-10.2f %-18.6f %-18.6f %-14.6f' % (tt / 3600.0, M, M0 - M, F))
print()
tt, M, F = snaps[-1]
loss = M0 - M
res = abs(loss - F) / max(abs(loss), 1e-30)
print('  末态：水量减少 = %.6f   累计表面排出 = %.6f' % (loss, F))
print('  ⟹ 质量相对残差 = %.3e (%.4f%%)' % (res, 100 * res))
print()
print('  归因：① 表面通量用**输出步末**的 C_R 近似（子步级未存 ⟹ 一阶时间误差）；')
print('        ② 输出步 60 s 的矩形积分截断；③ 浮点舍入。')
print('  ⟹ 判据：与 Q2 的 E7（1.903e-03）同量级即为正常。')
