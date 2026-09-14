# -*- coding: utf-8 -*-
"""
E3-g-② 差异定位：q4 退化模式（fixR＋附录3）vs q2_core_c（result2 生产核）
================================================================================
[SCALE] 三个 1 h 短时程求解（N=80, n_sub=32）：q2 基准、q4(t_corr=0)、q4(t_corr=1)；
  墙钟 ≈1-2 min；只写 logs/q4_diag_e3g2.txt。无交付物改动。
  授权：用户指令"完成第四问未完成的建模"；《口径总表》§11.4 勘误留待办
  "6.6 K 级差异由 Q4 侧另行定位"——本脚本即该定位实验。
背景：F-Q4-6 勘误后确认 result2.xlsx 与 q2_core_c 逐位一致、q4(fixR+app3) 与
  q3_core 机器级一致（S2），但旧 E3-g-② 报告 q4 退化模式 vs result2 在 1 h 处
  dT=6.6 K／dC=0.068 —— 与上述两条互验矛盾，须定位差异来源。
================================================================================
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] E3-g-2 localization: three 1 h solves (N=80, n_sub=32), wall ~1-2 min')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'Q2', 'code'))

import q4_core as qc
import q2_core_c as q2
from q4_w6_lib import load_data

ts_env, Tv, Cv, ts_R, Rv = load_data()
N, NSUB = 80, 32
T_END = 3600.0

rep = ['=' * 70]
rep.append('E3-g-2 localization (1 h, N=%d, n_sub=%d, appendix-3 props, fixed R)' % (N, NSUB))


def q2_env_fns():
    def Tenv_fn(t):
        return float(np.interp(t, ts_env, Tv))

    def Cenv_fn(t):
        return float(np.interp(t, ts_env, Cv))
    return Tenv_fn, Cenv_fn


def run_q2_ref():
    Tenv_fn, Cenv_fn = q2_env_fns()
    T = np.full(N + 1, q2.DEF2['T0'])
    C = np.full(N + 1, q2.DEF2['C0'])
    for k in range(int(T_END)):
        T, C, _ = q2.step_imex(N, 0.02 / N, 1.0 / NSUB, NSUB, 0.02, 25.0, 8e-7,
                               T, C, Tenv_fn, Cenv_fn, float(k))
    return T, C


def run_q4(t_corr):
    T = np.full(N + 1, qc.DEF4['T0'])
    C = np.full(N + 1, qc.DEF4['C0'])
    for k in range(int(T_END)):
        T, C, _ = qc.step_imex4(N, 1.0 / N, 1.0 / NSUB, NSUB, qc.DEF4['R0'],
                                qc.DEF4['h'], qc.DEF4['km'], T, C, float(k),
                                ts_env, Tv, Cv, ts_R, Rv,
                                fixR=True, app3=True, t_corr=t_corr)
    return T, C


t0w = time.perf_counter()
T2, C2 = run_q2_ref()
rep.append('q2_core_c (result2 production path): T(0)=%.6f C(0)=%.6f C(R)=%.6f'
           % (T2[0], C2[0], C2[-1]))
for tc in (0, 1):
    T4, C4 = run_q4(tc)
    dT = np.max(np.abs(T4 - T2))
    dC = np.max(np.abs(C4 - C2))
    rep.append('q4 fixR+app3 t_corr=%d : T(0)=%.6f C(0)=%.6f C(R)=%.6f  '
               'max|dT|=%.3e max|dC|=%.3e'
               % (tc, T4[0], C4[0], C4[-1], dT, dC))
    # 逐节点定位最大差异位置
    j = int(np.argmax(np.abs(T4 - T2)))
    rep.append('   argmax dT at node j=%d (r=%.4f cm): T2=%.4f T4=%.4f'
               % (j, j * 0.02 / N * 100.0, T2[j], T4[j]))
rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

with open(os.path.join(HERE, '..', 'logs', 'q4_diag_e3g2.txt'), 'w',
          encoding='utf-8') as f:
    f.write('\n'.join(rep))
print('E3G2 DONE')
