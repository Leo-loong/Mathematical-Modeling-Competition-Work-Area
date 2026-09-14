# -*- coding: utf-8 -*-
"""
IN-REG 回归验证：innov 核（c_fr<=0, if_mode=0）与正式核 q4_core 逐位一致
================================================================================
[SCALE] 三个 60 s 求解（N=80, n_sub=32）：正式核、innov 核、innov 核(c_fr=0.3)；
  墙钟 <1 min；只写 logs/q4_INV0_regression.txt。
  判据：①innov(c_fr=-1) vs 正式核 max|dT|=max|dC|=0（逐位）；
        ②c_fr=0.3 与基线出现实质差异（钳位生效证据）。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] regression: three 60 s solves (N=80, n_sub=32), wall <1 min')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'code'))

from q4_w6_lib import load_data
import q4_core as formal
import q4_core_INV as inv

ts_env, Tv, Cv, ts_R, Rv = load_data()
N, NSUB, T_END = 80, 32, 60


def run(core, **kw):
    T = np.full(N + 1, core.DEF4['T0'])
    C = np.full(N + 1, core.DEF4['C0'])
    for k in range(T_END):
        T, C, _ = core.step_imex4(N, 1.0 / N, 1.0 / NSUB, NSUB, core.DEF4['R0'],
                                  core.DEF4['h'], core.DEF4['km'], T, C,
                                  float(k), ts_env, Tv, Cv, ts_R, Rv,
                                  t_corr=1, **kw)
    return T, C


rep = ['=' * 70]
Tf, Cf = run(formal)
Ti, Ci = run(inv, c_fr=-1.0, if_mode=0)
dT0 = float(np.max(np.abs(Ti - Tf)))
dC0 = float(np.max(np.abs(Ci - Cf)))
rep.append('BITWISE  innov(c_fr=-1,if_mode=0) vs formal: max|dT|=%.3e max|dC|=%.3e -> %s'
           % (dT0, dC0, 'PASS' if (dT0 == 0.0 and dC0 == 0.0) else 'FAIL'))
T3, C3 = run(inv, c_fr=2.0, if_mode=0)
rep.append('c_fr=2.0 effect probe (60 s 内 C<2 区域存在，钳位应生效): max|dT|=%.3e max|dC|=%.3e'
           % (float(np.max(np.abs(T3 - Tf))), float(np.max(np.abs(C3 - Cf)))))
rep.append('c_fr=2.0 differs from base: %s'
           % ('YES (clamp active)' if float(np.max(np.abs(C3 - Cf))) > 1e-6 else 'CHECK'))

with open(os.path.join(HERE, 'logs', 'q4_INV0_regression.txt'), 'w',
          encoding='utf-8') as f:
    f.write('\n'.join(rep))
print('REG DONE')
