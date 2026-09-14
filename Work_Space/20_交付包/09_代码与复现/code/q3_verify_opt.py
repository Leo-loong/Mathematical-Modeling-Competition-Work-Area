# -*- coding: utf-8 -*-
"""
Q3 · A/B 优化的**逐位验证**（零数值风险的验收）
=================================================================
验证目标：`q3_core.step_imex_fast`（A 子步下沉 + B 环境查表）
          与 `q2_core_c.step_imex`（原 Python 层 + lambda 环境）
          在**同一输入**下给出**逐位相同**的 T、C。

覆盖：
  · 三种 mode：coupled / frozen / decoupled
  · 多个 t0：含 t<14400 s（插值段）与 t>14400 s（延拓段）
  · 多输出步串联（检验累积一致性）

判据：max|ΔT| = 0 且 max|ΔC| = 0（严格逐位）
      —— 因 fastmath=False 且表达式逐字对应，理论上应为**精确 0**。

同时给出**加速比**实测（这是 A/B 优化的收益证据）。

用法：python q3_verify_opt.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))

import openpyxl                                   # noqa: E402
import q2_core_c as base                          # noqa: E402
import q3_core as q3                              # noqa: E402


def load_att1():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))),
                     '10_赛题', 'A题', '附件', '附件1.xlsx')
    wb = openpyxl.load_workbook(p, data_only=True)
    ws = wb.active
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in d])
    T = np.array([float(r[1]) for r in d])
    C = np.array([float(r[2]) for r in d])
    wb.close()
    return t, T, C


T_A1, TINF_A1, CINF_A1 = load_att1()

# ---- 原路径的环境函数（与 Q2 主力一致的写法：np.interp + 常值延拓）----
def make_lambda(tarr, varr, tail_val):
    def fn(t):
        return float(tail_val) if t > tarr[-1] else float(np.interp(t, tarr, varr))
    return fn

# ---- 优化路径的环境查表（延拓：末点后取常值，与上式一致）----
TS_ENV, TENV_V, CENV_V = q3.env_tables_from_att1(T_A1, TINF_A1, CINF_A1)

N, DR = 80, 2.5e-4
HH = 1.0 / 32.0
NSUB = 32
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']
NC = N + 1

print('=' * 68)
print('Q3 · A/B 优化逐位验证')
print('=' * 68)
print('  网格 N=%d  h=1/%d s  n_sub=%d' % (N, int(1 / HH), NSUB))

T0v, C0v = base.DEF2['T0'], base.DEF2['C0']
allpass = True

for mode in ('coupled', 'frozen', 'decoupled'):
    for t0 in (0.0, 3600.0, 10799.0, 14399.0, 20000.0):
        T = np.full(NC, T0v)
        C = np.full(NC, C0v)
        # 造一点非平凡分布（避免平凡初值掩盖问题）
        for i in range(NC):
            T[i] = T0v + 0.3 * i
            C[i] = C0v - 0.004 * i

        # --- 原路径 ---
        Tf = make_lambda(T_A1, TINF_A1, TINF_A1[-1])
        Cf = make_lambda(T_A1, CINF_A1, CINF_A1[-1])
        Ta, Ca, ia = base.step_imex(N, DR, HH, NSUB, R0, HC, KM, T, C,
                                    Tf, Cf, t0, mode=mode)

        # --- 优化路径 ---
        Tb, Cb, ib = q3.step_imex_fast(N, DR, HH, NSUB, R0, HC, KM, T, C,
                                       TS_ENV, TENV_V, CENV_V, t0, mode=mode)

        dT = float(np.max(np.abs(Ta - Tb)))
        dC = float(np.max(np.abs(Ca - Cb)))
        same_it = (ia['inner_tot'] == ib['inner_tot'])
        ok = (dT == 0.0) and (dC == 0.0) and same_it
        allpass = allpass and ok
        print('  mode=%-10s t0=%-8.0f  max|dT|=%.3e  max|dC|=%.3e  内层迭代 %d/%d  %s'
              % (mode, t0, dT, dC, ia['inner_tot'], ib['inner_tot'],
                 'PASS' if ok else '*** FAIL ***'))

# ---- 多输出步串联（累积一致性）----
print()
print('  --- 多输出步串联（20 步 × %d 子步，t0=10000 s）---' % NSUB)
T = np.full(NC, T0v + 5.0)
C = np.full(NC, 2.0)
Tf = make_lambda(T_A1, TINF_A1, TINF_A1[-1])
Cf = make_lambda(T_A1, CINF_A1, CINF_A1[-1])

Ta, Ca = T.copy(), C.copy()
t_wall_a = time.time()
for n in range(20):
    Ta, Ca, _ = base.step_imex(N, DR, HH, NSUB, R0, HC, KM, Ta, Ca,
                               Tf, Cf, 10000.0 + n * 1.0)
t_a = time.time() - t_wall_a

Tb, Cb = T.copy(), C.copy()
t_wall_b = time.time()
for n in range(20):
    Tb, Cb, _ = q3.step_imex_fast(N, DR, HH, NSUB, R0, HC, KM, Tb, Cb,
                                  TS_ENV, TENV_V, CENV_V, 10000.0 + n * 1.0)
t_b = time.time() - t_wall_b

dT = float(np.max(np.abs(Ta - Tb)))
dC = float(np.max(np.abs(Ca - Cb)))
ok = (dT == 0.0) and (dC == 0.0)
allpass = allpass and ok
print('    串联终点 max|dT|=%.3e  max|dC|=%.3e  %s' % (dT, dC, 'PASS' if ok else '*** FAIL ***'))
print('    墙钟：原路径 %.3f s  优化路径 %.3f s  加速 %.2f×'
      % (t_a, t_b, t_a / t_b if t_b > 0 else float('nan')))

print()
print('  ★ 总判定：', 'ALL PASS（逐位一致）' if allpass else '*** 存在 FAIL ***')
print('  ⚠ 说明：本验证仅比较"同一数学流程的两种 Python/JIT 组织方式"，')
print('     不涉及任何物理或离散口径的改变。')
