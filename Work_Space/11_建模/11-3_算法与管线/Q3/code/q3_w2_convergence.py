# -*- coding: utf-8 -*-
"""
Q3 · W2 长时程收敛性重验
================================================================================
动机：Q2 的 Δr=0.25 mm 与内部步 1/32 s 是在 **10800 s** 内验证的；
     Q3 时程约 **57.53 h（207 113 s）**，为 Q2 的 **19 倍**，
     误差随时程累积 ⟹ **必须在 Q3 的真实工况上重验**（依计划 §2.2）。

做法（控制变量）：
  · 空间收敛：固定内部步 1/32 s，比较 Δr = 1.0 / 0.5 / 0.25 mm
  · 时间收敛：固定 Δr = 0.25 mm，比较内部步 1/16 / 1/32 / 1/64 s
  · 比较基准：**推进到固定时刻 T_CMP = 24 h（86400 s）** 的全场 C
    （24 h 时系统已深入降速段，对离散误差敏感；且耗时仅为全程的 27%）
  · 判据（L3-07）：关键量相对变化 < 5e-5（保证第 4 位小数有效）

⚠ 注意：N=80 时 Δr=0.25 mm 对应"输出点与节点重合"（0.1 cm = 4 层）；
   N=40（0.5 mm）时 0.1 cm = 2 层，仍重合；N=20（1.0 mm）时 0.1 cm = 1 层，仍重合。
   ⟹ 比较点可直接取节点，无需插值。

用法：python q3_w2_convergence.py
"""
import sys
import os
import time

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
ts, Tv, Cv = q3.env_tables_from_att1(
    np.array([float(r[0]) for r in _d]),
    np.array([float(r[1]) for r in _d]),
    np.array([float(r[2]) for r in _d]))
wb.close()

P = base.DEF2
T_CMP = 86400.0                 # 比较时刻：24 h
DT_OUT = 60.0                   # 输出步（固定）
C_CRIT = 0.15


def run_to(N, dr, h_inner, t_cmp=T_CMP, report=""):
    """从初值推进到 t_cmp，返回 (T场, C场, 墙钟)。固定 Δr 与内部步，逐子步推进。"""
    nsub = int(round(DT_OUT / h_inner))
    hh = DT_OUT / nsub
    nsteps = int(round(t_cmp / DT_OUT))
    NC = N + 1
    T = np.full(NC, P['T0'])
    C = np.full(NC, P['C0'])
    t0 = time.time()
    for n in range(1, nsteps + 1):
        T, C, _ = q3.step_imex_fast(N, dr, hh, nsub, P['R0'], P['h'], P['km'],
                                    T, C, ts, Tv, Cv, (n - 1) * DT_OUT)
    return T, C, time.time() - t0


print('=' * 76)
print('Q3 · W2 长时程收敛性重验（比较时刻 %.0f h）' % (T_CMP / 3600.0))
print('=' * 76)
print('  核：q3_core（A/B 优化）  判据：相对变化 < 5e-5')

# ---------- ① 空间收敛 ----------
# ⚠ 收敛性验证的**正确做法**：以**最细网格为基准**，比较相邻网格的差异
#   （只比更粗的网格只能说明"粗网格不够"，无法证明所选中网格已足够）
print()
print('① 空间收敛（固定内部步 1/32 s，比较时刻 24 h）')
print('  %-10s %-6s %-12s %-12s %-22s %s'
      % ('Δr/mm', 'N', 'C(0)', 'C(R)', '相邻网格相对变化', '耗时'))
res_s = {}
for dmm in (1.0, 0.5, 0.25, 0.125):
    N = int(round(P['R0'] / (dmm * 1e-3)))
    T, C, w = run_to(N, dmm * 1e-3, 1.0 / 32.0)
    res_s[dmm] = (N, C[0], C[-1], w)
    print('  %-10.3f %-6d %-12.6f %-12.6f %-22s %.1fs'
          % (dmm, N, C[0], C[-1], '—' if dmm == 1.0 else '', w))

print()
print('  相邻网格相对变化（以更细者为基准）：')
prev = None
for dmm in (1.0, 0.5, 0.25, 0.125):
    N, c0, cR, w = res_s[dmm]
    if prev is not None:
        p0, pR, pd = prev
        r0 = abs(c0 - p0) / abs(p0)
        rR = abs(cR - pR) / abs(pR)
        print('    %.3f vs %.3f mm：|ΔC(0)|/C(0)=%.3e   |ΔC(R)|/C(R)=%.3e   %s'
              % (dmm, pd, r0, rR, 'PASS(<5e-5)' if max(r0, rR) < 5e-5 else '未达判据'))
    prev = (c0, cR, dmm)
print()
print('  ★ 判定：0.25 mm 是否足够，取决于「0.25 vs 0.125」的变化是否 < 5e-5。')
print('     （0.25 与 0.5 差异较大是**预期**的——说明 0.5 mm 不足，不能反推 0.25 不足）')

# ---------- ② 时间收敛 ----------
print()
print('② 时间收敛（固定 Δr=0.25 mm）')
print('  %-12s %-12s %-12s %-14s %s'
      % ('内部步/s', 'C(0)', 'C(R)', '相对变化', '耗时'))
res_t = {}
for hin in (1.0 / 16.0, 1.0 / 32.0, 1.0 / 64.0):
    T, C, w = run_to(80, 2.5e-4, hin)
    res_t[hin] = (C[0], C[-1], w)
    print('  %-12.6f %-12.6f %-12.6f %-14s %.1fs'
          % (hin, C[0], C[-1], '—' if abs(hin - 1 / 32.0) < 1e-12 else '', w))

reft = res_t[1.0 / 32.0]
print()
print('  以内部步 1/32 s 为基准的相对变化：')
for hin in (1.0 / 16.0, 1.0 / 64.0):
    c0, cR, w = res_t[hin]
    r0 = abs(c0 - reft[0]) / abs(reft[0])
    rR = abs(cR - reft[1]) / abs(reft[1])
    print('    h=1/%-5.0f s：|ΔC(0)|/C(0)=%.3e   |ΔC(R)|/C(R)=%.3e   %s'
          % (1 / hin, r0, rR, 'PASS' if max(r0, rR) < 5e-5 else '*** FAIL ***'))

print()
print('  说明：时间一阶格式的误差应近似随 h 线性递减；')
print('        若 1/16 相对变化显著、而 1/64 更小 ⟹ 一致。')
