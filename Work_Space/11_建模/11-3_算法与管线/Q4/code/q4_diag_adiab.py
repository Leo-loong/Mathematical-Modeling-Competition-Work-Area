# -*- coding: utf-8 -*-
"""
绝热判决实验：老态存储项修复前后的 T·R² 不变量对照（E3-g-① 重跑）
================================================================================
[SCALE] 两个 3600 s 绝热求解（N=160, n_sub=32, k=0, hc=0, 真实 R(t)）；墙钟 <2 min；
  只写 logs/q4_diag_adiab.txt。
  授权：用户指令"完成第四问未完成的建模"（E7b 能量残差 0.645 的根因判决）。
判据：绝热（k≡0）下守恒形式给出逐节点 d/dt[ρcp·T·R²]=0。以 C 冻结近似忽略
  ρcp 演化（ρcp 取子步起点值，两侧同口径），则不变量为 T·R²。
  - 修复版（rj0=(R0m/R1)²）：T·R² = const ⟹ PASS
  - bug 版（rj0=(R0m/R1)，备份 q4_core_prebug）：T·R = const、T·R² 漂移 ⟹ 暴露
================================================================================
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] adiabatic verdict: two 3600 s solves (N=160, n_sub=32), wall <2 min')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import importlib
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from q4_w6_lib import load_data

ts_env, Tv, Cv, ts_R, Rv = load_data()
N, NSUB, T_END = 160, 32, 3600.0

rep = ['=' * 70]
rep.append('adiabatic verdict (k=0, hc=0, real R(t), %d s, N=%d)' % (T_END, N))


def run(core):
    T = np.full(N + 1, core.DEF4['T0'])
    C = np.full(N + 1, core.DEF4['C0'])
    for k in range(int(T_END)):
        T, C, _ = core.step_imex4(N, 1.0 / N, 1.0 / NSUB, NSUB, core.DEF4['R0'],
                                  core.DEF4['h'], core.DEF4['km'], T, C,
                                  float(k), ts_env, Tv, Cv, ts_R, Rv,
                                  t_corr=0, k_zero=True, hcv=0.0)
    return T, C


R_end = float(np.interp(T_END, ts_R, Rv))
R0 = float(np.interp(0.0, ts_R, Rv))

for tag, mod in (('fixed(q4_core)', 'q4_core'), ('prebug(q4_core_prebug)', 'q4_core_prebug')):
    core = importlib.import_module(mod)
    t0w = time.perf_counter()
    T, C = run(core)
    inv_R2 = T * R_end ** 2 / (28.0 * R0 ** 2)      # T·R² 归一不变量（若 T·R²=const 则=1）
    inv_R1 = T * R_end / (28.0 * R0)                # T·R  归一不变量（若 T·R =const 则=1）
    rep.append('%s: wall=%.0f s' % (tag, time.perf_counter() - t0w))
    rep.append('  T(0)=%.4f ; |T·R²/T0R0² - 1| max=%.3e ; |T·R/T0R0 - 1| max=%.3e'
               % (T[0], np.max(np.abs(inv_R2 - 1.0)), np.max(np.abs(inv_R1 - 1.0))))

rep.append('expect: fixed -> T.R^2 invariant ~1e-12 ; prebug -> T.R invariant ~1e-12')

with open(os.path.join(HERE, '..', 'logs', 'q4_diag_adiab.txt'), 'w',
          encoding='utf-8') as f:
    f.write('\n'.join(rep))
print('ADIAB DONE')
