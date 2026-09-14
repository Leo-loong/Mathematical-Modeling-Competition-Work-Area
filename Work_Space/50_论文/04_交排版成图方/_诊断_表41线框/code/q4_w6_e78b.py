# -*- coding: utf-8 -*-
"""
E7 守恒核算（修正口径）＋ E8 潜热对照（潜热缺陷修复后）
================================================================================
[SCALE] 两次全量求解（N=160, n_sub=32, t_corr=1, 熔断 240 h）＋核算后处理；
  预计墙钟 ≈17-20 min（参照 E7/E8 旧跑 501 s/491 s/471 s）；无交付物改动，
  只写 logs/q4_w6_e78b.txt 与 logs/q4_e7_hist.csv。
  授权：用户指令"完成第四问未完成的建模"（W6 检验批次）。
用法：python q4_w6_e78b.py          -> 只打印 [SCALE] 并退出
      python q4_w6_e78b.py --go    -> 实际执行
================================================================================
修正点（相对旧 q4_w6_e78.py）：
  F1 E8 缺陷修复：q4_core 校正步此前漏加潜热源项（t_corr=1 下潜热被抹除，
     旧日志 max|dT|=2e-9 无效）；本次在 q4_core._step_all_nb 步④补回。
  F2 E7 核算口径修正（旧脚本两处错误）：
     (a) 通量用常值 (T∞=50, C∞=0.04999)——附件1 前 4 h 为时变（T∞ 28→50 ℃、
         C∞ 0.0196→0.04999），改用逐时刻插值；
     (b) 质量衡算对象错配：W=R²∫C̃ξdξ 的增量被直接与 −∫2Rkm(C_R−C∞)dt 对比，
         既丢几何项 2RR'∫C̃ξdξ，又多乘 2R。本问锁定 PDE（物料坐标、无几何项）
         的精确守恒量是 M=∫C̃ξdξ，其平衡为 dM/dt=−(km/R)(C_R−C∞)；
         能量 U=R²∫ρcpTξdξ 的平衡为 dU/dt=hR(T∞−T_R)。两者均改按此核算。
     交叉核对：另报 W 的物理收支 ΔW vs ∫(2RR'M − Rkm(C_R−C∞))dt（R' 由数值微分）。
  F3 t_dry 版本偏移排查：旧 E7/E8 日志 t_dry=182816.7 s vs 主力 182817.5 s，
     归因于旧跑先于 q4_core 末次修订（r 空间行标定）；本次以现行核重跑，
     预期 t_dry 与主力一致（±1e-3 s）。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] E7b+E8b: two full solves (N=160, n_sub=32, t_corr=1, breaker 240 h)')
print('[SCALE] wall est 17-20 min; outputs: logs/q4_w6_e78b.txt + logs/q4_e7_hist.csv')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q4_w6_lib import load_data, solve_to_dry, N0

HERE = os.path.dirname(os.path.abspath(__file__))
LOGD = os.path.join(HERE, '..', 'logs')
os.makedirs(LOGD, exist_ok=True)

KM = 8.0e-7
HC = 25.0

rep = ['=' * 70]
t0w = time.perf_counter()

ts_env, Tv, Cv, ts_R, Rv = load_data()

# ---------------- 基线全量求解（兼作 E7 数据源与 E8 基线） ----------------
rep.append('E7b conservation (corrected accounting) + E8b latent (fixed core)')
rep.append('baseline solve: N=%d, n_sub=32, t_corr=1, breaker 240 h' % N0)
res = solve_to_dry(N0, 32, t_corr=1, breaker_h=240.0, hist_every=60,
                   ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv,
                   verbose=True, tag='e7b')
rep.append('baseline t_dry=%.3f s (%.4f h) wall=%.0f s'
           % (res['t_dry'], res['t_dry'] / 3600.0, res['wall']))

h = res['hist']
t = np.array([x[0] for x in h])
Rk = np.array([x[1] for x in h])
W = np.array([x[2] for x in h])
U = np.array([x[3] for x in h])
CR = np.array([x[4] for x in h])
TR = np.array([x[5] for x in h])

# 前插 t=0 解析行（均匀初态）
R0 = float(Rk[0])  # t=60 s 的 R，与 R(0) 差 <1e-6；t=0 用附件2 精确值
R0 = float(np.interp(0.0, ts_R, Rv))
rho_cp0 = (760.0 + 90.0 * 2.55) * (1850.0 + 2150.0 * 2.55 / 3.55)
M0 = 2.55 * 0.5
U0 = R0 * R0 * rho_cp0 * 28.0 * 0.5
t = np.concatenate([[0.0], t])
Rk = np.concatenate([[R0], Rk])
M = np.concatenate([[M0], W / Rk[1:] ** 2])
U = np.concatenate([[U0], U])
CR = np.concatenate([[2.55], CR])
TR = np.concatenate([[28.0], TR])
W = np.concatenate([[M0 * R0 * R0], W])

cinf_t = np.interp(t, ts_env, Cv)
tinf_t = np.interp(t, ts_env, Tv)

# ---- E7b：PDE 层面守恒核算 ----
dM = M[-1] - M[0]
Fmass = float(np.trapezoid(KM / Rk * (CR - cinf_t), t))
res_m = abs(dM + Fmass) / abs(dM)

dU = U[-1] - U[0]
Eflux = float(np.trapezoid(HC * Rk * (tinf_t - TR), t))
res_e = abs(dU - Eflux) / abs(dU)

# ---- 交叉核对：物理含水量 W=R²M 的收支（含几何项） ----
Rp = np.gradient(Rk, t)
dW = W[-1] - W[0]
Wflux = float(np.trapezoid(2.0 * Rk * Rp * M - Rk * KM * (CR - cinf_t), t))
res_w = abs(dW - Wflux) / abs(dW)

rep.append('--- E7b (PDE-level: M=int C.xi dxi, U=int rho_cp*T*R^2*xi dxi) ---')
rep.append('mass  : dM=%+.6e  -int(km/R*(CR-Cinf))dt=%+.6e  rel residual=%.3e'
           % (dM, -Fmass, res_m))
rep.append('energy: dU=%+.6e  int(h*R*(Tinf-TR))dt=%+.6e  rel residual=%.3e'
           % (dU, Eflux, res_e))
rep.append('cross W-form: dW=%+.6e  int(2RR\'M - R*km*(CR-Cinf))dt=%+.6e  rel=%.3e'
           % (dW, Wflux, res_w))
rep.append('residual sources (honest): 60 s trapezoid in time, O(dxi^2) spatial')
rep.append('trapezoid + center-cell O(dxi) telescoping defect (L Hospital row doubling)')
rep.append('criterion: mass/energy ~1e-3 order (Q2/Q3 same)')

# hist 落盘（可复核）
import csv
with open(os.path.join(LOGD, 'q4_e7_hist.csv'), 'w', newline='',
          encoding='utf-8') as f:
    wtr = csv.writer(f)
    wtr.writerow(['t_s', 'R_m', 'M_intCxi', 'U_intRhoCpT', 'C_R', 'T_R',
                  'Cinf', 'Tinf'])
    for i in range(len(t)):
        wtr.writerow(['%.3f' % t[i], '%.8f' % Rk[i], '%.10e' % M[i],
                      '%.10e' % U[i], '%.8f' % CR[i], '%.6f' % TR[i],
                      '%.8f' % cinf_t[i], '%.6f' % tinf_t[i]])

# ---------------- E8b：潜热对照（修复后核） ----------------
rl = solve_to_dry(N0, 32, t_corr=1, breaker_h=240.0, L=2.26e6, ts_env=ts_env,
                  Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv, verbose=True, tag='e8b')
dT = np.max(np.abs(rl['Tend'] - res['Tend']))
dC = np.max(np.abs(rl['Cend'] - res['Cend']))
dt_h = (rl['t_dry'] - res['t_dry']) / 3600.0
rep.append('--- E8b (latent L=2.26e6 J/kg, core fixed) ---')
rep.append('latent  : t_dry=%.4f h (wall %.0f s)' % (rl['t_dry'] / 3600.0, rl['wall']))
rep.append('end-field: max|dT|=%.3e K ; max|dC|=%.3e' % (dT, dC))
rep.append('t_dry shift = %+.4f h (%+.3f%%)'
           % (dt_h, 100.0 * dt_h / (res['t_dry'] / 3600.0)))
rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

with open(os.path.join(LOGD, 'q4_w6_e78b.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep))
print('E78B DONE')
