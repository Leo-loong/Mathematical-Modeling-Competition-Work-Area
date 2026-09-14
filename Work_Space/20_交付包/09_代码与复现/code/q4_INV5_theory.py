# -*- coding: utf-8 -*-
"""
IN-5（A5/A6）理论档：解析两界夹逼 ＋ 压缩温升机理分析（零 PDE 求解）
================================================================================
[SCALE] 仅 ODE 积分与后处理（基线 hist 数据 + 附件2），墙钟 <10 s；
  写 logs/q4_INV5_theory.txt + out/fig_q4_INV5_compression.csv。
A5：下界 = 表面控制集总极限（均匀浓度，严格快于任何真实剖面）；
    上界 = 数值严格上界（fixR 档，R≡R0 ≥ R(t) ⟹ 更慢，来自 IN-4）＋渐近量级校验。
A6：绝热包络 T_ad(t)（峰值处严格：T>T∞ 时净散热 ⟹ T ≤ T_ad）＋准稳态超温估计。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-5 theory: ODE + postprocess only, wall <10 s')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from q4_INV_lib import load_data

KM = 8.0e-7
ts_env, Tv, Cv, ts_R, Rv = load_data()
rep = ['=' * 70]

# ---------------- A5 下界：均匀浓度（表面控制）ODE ----------------
def cinf(t):
    return float(np.interp(t, ts_env, Cv))

def Rof(t):
    return float(np.interp(t, ts_R, Rv))

dt = 0.5
M, t = 2.55 * 0.5, 0.0        # M = int C.xi dxi；均匀 C -> C_R = 2M
t_lower = None
while t < 240.0 * 3600:
    k1 = -KM / Rof(t) * (2.0 * M - cinf(t))
    k2 = -KM / Rof(t + dt / 2) * (2.0 * (M + dt / 2 * k1) - cinf(t + dt / 2))
    k3 = -KM / Rof(t + dt / 2) * (2.0 * (M + dt / 2 * k2) - cinf(t + dt / 2))
    k4 = -KM / Rof(t + dt) * (2.0 * (M + dt * k3) - cinf(t + dt))
    M += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    t += dt
    if 2.0 * M < 0.15:
        t_lower = t
        break
rep.append('A5 lower bound (uniform-C / surface-controlled lump limit):')
rep.append('  t_dry >= %.4f h   (严格：真实剖面 C_R < 平均 C ⟹ 通量更小、更慢)'
           % ((t_lower or float('nan')) / 3600.0))

# ---------------- A5 上界：数值严格上界（fixR，来自 IN-4）＋渐近量级 ----------------
# fixR 档数值由 q4_INV4_aux 产出；此处登记占位，报告中由汇总文档引用。
rep.append('A5 upper bound (rigorous numeric): t_dry(fixR, appendix-4) —— 见 IN-4 fixR 档')
# 渐近量级校验：固定 R0、特征 D*=D(C=0.15, T=50C)、BiC 对应的一阶渐近
T_K = 323.15
Dstar = 4.2e-4 * np.exp(-0.30 / 0.15) * np.exp(-3850.0 / T_K)
BiC = KM * 0.02 / Dstar
tau_asym = 0.02 ** 2 / Dstar          # 扩散时标
rep.append('  asymptotic scale check: D*=D(C=0.15,T=50C)=%.3e m2/s, BiC(km R0/D*)=%.1f,'
           % (Dstar, BiC))
rep.append('  R0^2/D* = %.3e s = %.1f h（长时程渐近时标量级；非严格界）' % (tau_asym, tau_asym / 3600.0))

# ---------------- A6 压缩温升机理 ----------------
base = np.genfromtxt(os.path.join(HERE, '..', 'logs', 'q4_e7_hist.csv'),
                     delimiter=',', names=True)
t = base['t_s']; Rk = base['R_m']; TR = base['T_R']
U = base['U_intRhoCpT']              # 每弧度积分（不含 2pi）
U_tot = 2.0 * np.pi * U
tinf = np.interp(t, ts_env, Tv)
Rp = np.gradient(Rk, t)
theta_meas = TR - tinf

# 准稳态超温估计：theta_qs = P_comp/(h*2*pi*R), P_comp = -2(R'/R) U_tot
P_comp = -2.0 * (Rp / Rk) * U_tot
theta_qs = P_comp / (25.0 * 2.0 * np.pi * Rk)

# 绝热包络（峰值处严格）：T_ad = T0 * rho_cp0 * R0^2 / (rho_cp(0.15) * R(t)^2)
rho_cp0 = (760 + 90 * 2.55) * (1850 + 2150 * 2.55 / 3.55)
rho_cp_end = (760 + 90 * 0.15) * (1850 + 2150 * 0.15 / 1.15)
T_ad = 28.0 * rho_cp0 * 0.02 ** 2 / (rho_cp_end * Rk ** 2)

i_above = theta_meas > 0
rep.append('A6 compression heating mechanism (from baseline hist):')
rep.append('  measured: max excess T_R - T_inf = %+.3f K at t=%.2f h ; steps above env: %d/%d'
           % (np.max(theta_meas), t[int(np.argmax(theta_meas))] / 3600.0,
              int(np.sum(i_above)), len(t)))
rep.append('  quasi-steady estimate theta_qs: max %+.3f K at t=%.2f h（量级/时相一致）'
           % (np.max(theta_qs), t[int(np.argmax(theta_qs))] / 3600.0))
rep.append('  adiabatic envelope T_ad(t) = T0*rho_cp0*R0^2/(rho_cp(C_end)*R^2):')
rep.append('    at peak-excess time: T_ad=%.1f C vs measured T_R=%.1f C -> T <= T_ad %s'
           % (T_ad[int(np.argmax(theta_meas))], TR[int(np.argmax(theta_meas))],
              'PASS' if TR[int(np.argmax(theta_meas))] <= T_ad[int(np.argmax(theta_meas))] else 'FAIL'))
rep.append('    global check: max(T_R - T_ad) = %.3f K over steps with T_R > T_inf %s'
           % (float(np.max(TR[i_above] - T_ad[i_above])),
              'PASS' if np.max(TR[i_above] - T_ad[i_above]) <= 0 else 'FAIL'))
rep.append('  interpretation: 超温峰值出现在 R 收缩最快时段（附件2 前段），')
rep.append('  准稳态估计给出量级与相位；严格包络由绝热迹线承担（T>T∞ 时净散热 ⟹ T ≤ T_ad）。')

os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
with open(os.path.join(HERE, 'out', 'fig_q4_INV5_compression.csv'), 'w',
          encoding='utf-8') as f:
    f.write('t_h,TR,T_inf,theta_meas,theta_qs,T_ad\n')
    for i in range(len(t)):
        f.write('%.4f,%.4f,%.4f,%+.5f,%+.5f,%.2f\n'
                % (t[i] / 3600.0, TR[i], tinf[i], theta_meas[i], theta_qs[i], T_ad[i]))
with open(os.path.join(HERE, 'logs', 'q4_INV5_theory.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(rep))
print('INV5 DONE')
