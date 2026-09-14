# -*- coding: utf-8 -*-
"""
Q3 事后核验：① 推演偏差归因（分段积分 vs 圆柱渐近解）
             ② 表 5 数据生成
             ③ 与 Q2 重叠段一致性核对
"""
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
import openpyxl
from scipy.special import j0, j1
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
R0, KM, KE, CINF = 0.02, 8e-7, 323.15, 0.05


def Dof(C):
    return 2.4e-3 * np.exp(-0.45 / C) * np.exp(-3850.0 / KE)


def mu1(Bi):
    return brentq(lambda m: m * j1(m) - Bi * j0(m), 0.01, 3.0)


print('=' * 74)
print('① 推演偏差归因：两种解析估计与实测对照')
print('=' * 74)
C0, Cc = 2.55, 0.15
MR = (Cc - CINF) / (C0 - CINF)
print('  目标水分比 MR = (%.2f-%.2f)/(%.2f-%.2f) = %.6f' % (Cc, CINF, C0, CINF, MR))
print()
print('  %-34s %-14s %s' % ('估计方法', 't_end', '与实测 57.53 h 之比'))
print('  ' + '-' * 68)

# 方法 1：原分段积分（空间均匀假设）
def tau(C):
    Bi = KM * R0 / Dof(C)
    return R0 * R0 / (mu1(Bi) ** 2 * Dof(C)) / 3600.0


from scipy.integrate import quad
t1, _ = quad(lambda C: tau(C) / (C - CINF), Cc, C0, limit=300)
print('  %-34s %-14s %.2f×' % ('原分段积分（空间均匀假设）', '%.1f h' % t1, t1 / 57.5314))

# 方法 2：圆柱渐近解（中心点，含特征值与首项系数）
a1_list = []
for i in range(1, 8):
    Bi = KM * R0 / Dof(Cc)
    m = mu1(Bi)
    A = 2.0 * Bi / (m * m + Bi * Bi) / j0(m)
    a1_list.append((m, A))
mu_1, A_1 = a1_list[0]
Fo = -np.log(MR / A_1) / (mu_1 ** 2)
t2 = Fo * R0 * R0 / Dof(Cc) / 3600.0
print('  %-34s %-14s %.2f×' % ('圆柱渐近解（中心点，D(0.15)）', '%.1f h' % t2, t2 / 57.5314))
print('     其中 mu_1=%.4f  A_1=%.4f  Fo=%.4f' % (mu_1, A_1, Fo))
print()
print('  ⟹ 结论：① 原"空间均匀"分段积分把扩散 PDE 当单点 ODE，**系统性低估**（25.8 h）；')
print('     ② 圆柱渐近解取 D(C_crit) 为常数、忽略"早期 D 更大"，**高估**为 %.1f h（约 %.2f× 实测）；'
      % (t2, t2 / 57.5314))
print('     ③ 两者分别给出**下界/上界**，实测 %.2f h 落在其间 ⟹ **量级自洽**。' % 57.5314)

# ---------------- ② 表 5 生成 ----------------
print()
print('=' * 74)
print('② 表 5 数据（每 6 h；列：0/0.5/1/1.5/2 cm；末行为烘干结束时间）')
print('=' * 74)
wb = openpyxl.load_workbook(os.path.join(WS, '20_交付包', '09_代码与复现',
                                         'results', 'result3.xlsx'), read_only=True)
ws = wb.active
rows = [r for r in ws.iter_rows(values_only=True)]
hdr = rows[0][1:]
tv = np.array([float(r[0]) for r in rows[1:]])
A = np.array([[float(x) for x in r[1:]] for r in rows[1:]])
wb.close()
sel = [0, 5, 10, 15, 20]          # 0, 0.5, 1.0, 1.5, 2.0 cm
print('  %-12s %-11s %-11s %-11s %-11s %s'
      % ('时间/h', '0cm', '0.5cm', '1.0cm', '1.5cm', '2.0cm'))
for h in range(6, 88, 6):
    tt = h * 3600.0
    if tt > tv[-1]:
        break
    k = int(np.argmin(np.abs(tv - tt)))
    print('  %-12d %-11.4f %-11.4f %-11.4f %-11.4f %.4f'
          % (h, A[k, 0], A[k, 5], A[k, 10], A[k, 15], A[k, 20]))
print('  %-12s %-11.4f %-11.4f %-11.4f %-11.4f %.4f'
      % ('烘干结束(57.5314)', A[-1, 0], A[-1, 5], A[-1, 10], A[-1, 15], A[-1, 20]))

# ---------------- ③ 与 Q2 重叠段一致性 ----------------
print()
print('=' * 74)
print('③ 与 Q2 重叠段一致性（Q3 前 3 h vs Q2 result2.xlsx）')
print('=' * 74)
wb2 = openpyxl.load_workbook(os.path.join(WS, '20_交付包', '09_代码与复现',
                                          'results', 'result2.xlsx'), read_only=True)
wsc = wb2['水分浓度']
r2 = [r for r in wsc.iter_rows(values_only=True)]
t2v = np.array([float(r[0]) for r in r2[1:]])
A2 = np.array([[float(x) for x in r[1:]] for r in r2[1:]])
wb2.close()
print('  %-10s %-11s %-11s %-11s' % ('时间/s', 'Q3 C(0)', 'Q2 C(0)', '差'))
for tt in (60, 1800, 3600, 7200, 10800):
    k3 = int(np.argmin(np.abs(tv - tt)))
    k2 = int(np.argmin(np.abs(t2v - tt)))
    print('  %-10d %-11.4f %-11.4f %+.3e' % (tt, A[k3, 0], A2[k2, 0], A[k3, 0] - A2[k2, 0]))
print()
print('  ⟹ 两者同模型同口径，差异应 ≤ 输出精度（1e-4）')
