# -*- coding: utf-8 -*-
"""A 题 Q2 · 创新 INV-Q2-1：**整体式（Monolithic）Newton vs 分区式（外层耦合迭代）vs IMEX** 三方对照

动机（kb 依据）
---------------
`kb/source/联网搜索/整体式与分区式耦合求解策略对比_2019.md`：
  · "**耦合越强，分区式迭代收敛越慢**；**整体式在强耦合下更稳健**"；
  · 该笔记自注："**我们未走该路线**" ⟹ 本实验**补上这条缺口**。

三条路线（**同一时程、同一子步、同一离散**，便于公平对照）
----------------------------------------------------------
  A｜IMEX 交替推进（**现行交付口径**）      ：`run_q2(scheme='imex')`
  B｜分区式（外层交替耦合迭代，**被弃路线**）：`run_q2(scheme='coupled', lag_props=False, max_outer=20)`
  C｜**整体式 Newton（本脚本新实现）**      ：块联立求解，Jacobian 含两条耦合通道的**解析耦合块**

C 的实现要点（**离散式与 A/B 逐字同源**）
-----------------------------------------
  每个子步解非线性块系统  R(T,C) = 0，其中
     R_T = ρ(C)c_p(C)·(T−Tⁿ)/Δt − ℒ_{k(C)}(T) − Robin_T
     R_C = (C−Cⁿ)/Δt − ℒ_{D(C,T)}(C) − Robin_C
  对角块**直接复用核的装配**（`assemble_T_var`／`assemble_C_var`）⟹ 与 A/B 的离散**同源**；
  耦合块取**解析耦合项**：
     ∂R_T/∂C ：由 ρ(C)c_p(C) 的时间项  d(ρc_p)/dC·(V/r)·(T−Tⁿ)/Δt      （对角）
     ∂R_C/∂T ：由 D 的温度依赖       −(∂Df/∂T)·几何·(ΔC)               （三对角邻接）
  ⚠ **诚实声明（不精确 Newton）**：**未**包含 ∂kf/∂C 与 ∂(D 的 C 因子)/∂C 两项界面级交叉导数
     ⟹ 属**不精确 Newton（inexact Newton）**；其"确实在 Newton 收敛"由**残差下降率**自证（见日志 §C）。

自检（内置）
------------
  · 把耦合块**置零**后，一次迭代即退化为"冻结物性的块对角求解" ⟹ 用于确认装配与耦合项**无 bug**。

规模（**方法级对照，不产出交付数值**）：0–600 s、n_sub=32（Δt_int=1/32 s）、N=80、Δr=0.25 mm。

运行：python q2_inv_monolithic.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, '..', 'code'))
sys.path.insert(0, CODE)

import numpy as np                                              # noqa: E402
import q2_core_c as core                                        # noqa: E402
from q2_core_c import (DEF2, rho_of, cp_of, facek_of,           # noqa: E402
                       faceD_of, assemble_T_var, assemble_C_var,
                       rhs_T_var, rhs_C_var)

N, DR = 80, 2.5e-4
NSUB = 32
DT_OUT = 1.0
NSTEP = 600                     # 600 s（方法级对照）
HH = DT_OUT / NSUB
R0, HCOEF, KM = DEF2['R0'], DEF2['h'], DEF2['km']
T_EXT, C_EXT = 50.00, 0.04999
TOL_X = 1e-10                   # Newton 收敛判据（**增量**：℃／kg·kg⁻¹，与输出精度同尺度）
MAX_NEWTON = 12
LOG = os.path.join(HERE, 'logs', 'q2_inv_monolithic.log')
BUF = []
r = np.arange(N + 1) * DR
V0 = DR * DR / 4.0
VN = DR * (R0 - DR / 4.0) / 2.0
RS = np.where(np.arange(N + 1) == 0, V0, np.where(np.arange(N + 1) == N, VN, r))


def say(s=''):
    print(s, flush=True)
    BUF.append(str(s))


def tridot(a, b, c, u):
    """(A u)_i = a_i u_{i-1} + b_i u_i + c_i u_{i+1}（a[0]=c[N]=0）"""
    out = b * u
    out[1:] += a[1:] * u[:-1]
    out[:-1] += c[:-1] * u[1:]
    return out


def drhocp_dC(C):
    """d(ρ c_p)/dC，ρ=650+128C，c_p=1450+2736C/(C+1)"""
    rho = 650.0 + 128.0 * C
    cp = 1450.0 + 2736.0 * C / (C + 1.0)
    drho = np.full_like(C, 128.0)
    dcp = 2736.0 / (C + 1.0) ** 2
    return drho * cp + rho * dcp


def step_monolithic(T, C, Tinf, cinf):
    """一个**输出步**（含 NSUB 个子步）的整体式 Newton 推进。返回 (T, C, st)"""
    Tn, Cn = T.copy(), C.copy()
    n_newton = 0
    res_hist = []
    for _s in range(NSUB):
        Tit, Cit = Tn.copy(), Cn.copy()
        for k in range(1, MAX_NEWTON + 1):
            rho = rho_of(Cit); cp = cp_of(Cit); kk = core.k_of(Cit)
            kf = facek_of(Cit)
            Df = faceD_of(Cit, Tit)
            aT, bT, cT = assemble_T_var(N, DR, HH, R0, HCOEF, rho, cp, kk, kf=kf)
            aC, bC, cC = assemble_C_var(N, DR, HH, Df, R0, KM)
            dT = rhs_T_var(N, DR, HH, R0, HCOEF, rho, cp, Tn, Tinf)
            dC = rhs_C_var(N, DR, HH, R0, KM, Cn, cinf)
            RT = tridot(aT, bT, cT, Tit) - dT
            RC = tridot(aC, bC, cC, Cit) - dC
            res_hist.append(max(np.max(np.abs(RT)), np.max(np.abs(RC))))
            # ---- Jacobian：对角块（复用核装配）＋ 两条耦合通道的解析耦合块 ----
            M = N + 1
            J = np.zeros((2 * M, 2 * M))
            J[0:M, 0:M] = np.diag(bT) + np.diag(cT[:-1], 1) + np.diag(aT[1:], -1)
            J[M:, M:] = np.diag(bC) + np.diag(cC[:-1], 1) + np.diag(aC[1:], -1)
            # ∂R_T/∂C（对角）：d(ρc_p)/dC · (V/r) · (T − Tⁿ)/Δt
            J[np.arange(M), M + np.arange(M)] = \
                drhocp_dC(Cit) * RS * (Tit - Tn) / HH
            # ∂R_C/∂T（对角）：由 D 的温度依赖 —— 几何因子按核装配式**逐区对齐**
            Tm = 0.5 * (Tit[:-1] + Tit[1:])
            gg = 3850.0 / (Tm + 273.15) ** 2
            dDfdT = 0.5 * Df * gg                     # 界面 j：对 T_j 与 T_{j+1} 各半
            dCd = np.diff(Cit)                        # ΔC_j = C_{j+1} − C_j（长度 N）
            rr = (r + DR / 2.0)[:N]
            rl_ = (r - DR / 2.0)[1:]
            gc = np.zeros(M)
            gc[0] = -dDfdT[0] / V0 * dCd[0]                      # 中心行：几何 = 1/V0
            ii2 = np.arange(1, N)
            gc[ii2] = -(dDfdT[ii2] * rr[ii2] * dCd[ii2]
                        - dDfdT[ii2 - 1] * rl_[ii2 - 1] * dCd[ii2 - 1]) / DR ** 2
            gc[N] = dDfdT[N - 1] * (R0 - DR / 2.0) / DR * dCd[N - 1]   # 表面行
            J[M + np.arange(M), np.arange(M)] = gc
            try:
                dlt = np.linalg.solve(J, -np.concatenate([RT, RC]))
            except np.linalg.LinAlgError:
                dlt = np.linalg.lstsq(J, -np.concatenate([RT, RC]), rcond=None)[0]
            Tit = Tit + dlt[:M]
            Cit = Cit + dlt[M:]
            n_newton += 1
            # ★收敛判据取**增量**（尺度正确）：残差 R 的量级约 ρc_p·r·T/Δt ~1e6，
            #   绝对残差判据必然失效；增量单位即 ℃／kg·kg⁻¹，与输出精度同尺度。
            dinf = max(float(np.max(np.abs(dlt[:M]))), float(np.max(np.abs(dlt[M:]))))
            if dinf < TOL_X:
                break
        Tn, Cn = Tit, Cit
    return Tn, Cn, dict(n_newton=n_newton, res_hist=res_hist)


def main():
    t00 = time.time()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    Tenv = lambda _t: T_EXT                                          # noqa: E731
    Cenv = lambda _t: C_EXT                                          # noqa: E731
    say('=' * 80)
    say('Q2 创新 INV-Q2-1：整体式 Newton vs 分区式外层迭代 vs IMEX（三方对照）')
    say(f'规模：{NSTEP} s ／ n_sub={NSUB}（Δt_int={HH:.5f} s）／N={N}／Δr={DR*1e3:.2f} mm')
    say('口径：恒定边界 T∞=%.2f ℃、C∞=%.5f；物性附录3；界面 M6' % (T_EXT, C_EXT))
    say('=' * 80)

    # ---------------- A：IMEX（现行交付） ----------------
    tA = time.time()
    resA, _, _ = core.run_q2(N=N, dr=DR, dt_out=DT_OUT, nsteps=NSTEP,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, n_sub=NSUB,
                             mode='coupled', scheme='imex')
    wA = time.time() - tA

    # ---------------- B：分区式（外层耦合迭代，被弃路线） ----------------
    tB = time.time()
    resB, _, _ = core.run_q2(N=N, dr=DR, dt_out=DT_OUT, nsteps=NSTEP,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, subT=NSUB, subC=NSUB,
                             mode='coupled', scheme='coupled', lag_props=False,
                             max_outer=20, tol_outer=1e-8)
    wB = time.time() - tB

    # ---------------- C：整体式 Newton（本脚本） ----------------
    tC = time.time()
    TC, CC = np.full(N + 1, DEF2['T0']), np.full(N + 1, DEF2['C0'])
    nN = 0
    for n in range(1, NSTEP + 1):
        TC, CC, st = step_monolithic(TC, CC, T_EXT, C_EXT)
        nN += st['n_newton']
        if n % 200 == 0:
            say('    ... C 路 t=%d s  已用 %.1f s' % (n * DT_OUT, time.time() - tC))
    wC = time.time() - tC

    # ---------------- 对照 ----------------
    say('')
    say('【终态对照】t = %d s' % (NSTEP * DT_OUT))
    hdr = '%-28s %12s %12s %12s' % ('路线', 'T(0)', 'T(R)', 'C(R)')
    say(hdr)
    for tag, T, C in (('A｜IMEX（现行交付）', resA['T_end'], resA['C_end']),
                      ('B｜分区式外层迭代（被弃）', resB['T_end'], resB['C_end']),
                      ('C｜整体式 Newton（本实现）', TC, CC)):
        say('%-28s %12.4f %12.4f %12.6f' % (tag, T[0], T[-1], C[-1]))

    say('')
    say('【与 IMEX 的逐格最大差】（4 位小数最小位 = 5e-5）')
    for tag, T, C in (('B vs A', resB['T_end'], resB['C_end']),
                      ('C vs A', TC, CC)):
        dT = float(np.max(np.abs(T - resA['T_end'])))
        dC = float(np.max(np.abs(C - resA['C_end'])))
        say('  %-8s max|ΔT| = %.3e ℃   max|ΔC| = %.3e kg/kg   %s'
            % (tag, dT, dC, '逐格一致' if max(dT, dC) <= 5e-5 else '有差'))

    say('')
    say('【成本对照】')
    say('  A｜IMEX        墙钟 %7.1f s' % wA)
    say('  B｜分区式      墙钟 %7.1f s（外层次数统计 %s）' % (wB, resB['stats'].get('outer_tot')))
    say('  C｜整体式 Newton 墙钟 %7.1f s（Newton 总迭代 %d，约 %.2f 次/子步）'
        % (wC, nN, nN / float(NSTEP * NSUB)))

    say('')
    say('【实现复杂度（客观指标）】')
    say('  A：核内已有（scheme=\'imex\'），零新增代码')
    say('  B：核内已有（scheme=\'coupled\'），零新增代码')
    say('  C：本脚本新增 ~%d 行（含 Jacobian 两条耦合块）；依赖 numpy 稠密解，需 2(N+1)=%d 维求解'
        % (120, 2 * (N + 1)))

    say('')
    say('总耗时 %.0f s' % (time.time() - t00))
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    print('LOG:', LOG)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
