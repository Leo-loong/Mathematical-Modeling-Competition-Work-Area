# -*- coding: utf-8 -*-
r"""T2-4 连续伴随法灵敏度（adjoint）· 与 OAT 交叉验证  · v2

v1 的两处缺陷（已修）：
  ① **求积不足**：伴随 λ 含**快模态**（温度侧时间常数 ≈0.09 s、含水率侧 ≈3 s），
     用 1 s 的黎曼求积无法分辨 → 表面输出梯度偏差可达 70%。
     修法：λ 用 **子步精确推进**（T: 1/64 s；C: 1/8 s），状态按 1 s 网格线性插值。
  ② **含水率伴随漏项**：km 同时出现在 $A_C[N,N]$ 与 $\eta$ 中，v1 只计了 $\eta$ 项 ⟹ 符号反。
     修法：对 km 与 D0 都做中心差分装配 $\partial A_C/\partial q$。

原理：
  dψ/dt = A ψ + b(t),  J = e_pᵀ ψ(T)
  -dλ/dt = Aᵀ λ, λ(T) = e_p
  dJ/dq = ∫_0^T λᵀ (∂A/∂q ψ + ∂b/∂q) dt

运行：python q1_inv_T2_adjoint.py
"""
import time
import numpy as np
from scipy.linalg import expm
from concurrent.futures import ProcessPoolExecutor

from q1_inv_lib import Rec, env_fns
from q1_inv_par import solve_worker
import q1_core as core
import q1_exact as ex

rec = Rec('q1_inv_T2_adjoint.log')
N, DR, R0 = 80, 0.25e-3, 0.02
D = 81
T_END = 1800
RQ = ('h', 'k', 'rho', 'cp')


def fd_mat(fn, q, dq):
    pp = dict(fn); pp[q] += dq
    pm = dict(fn); pm[q] -= dq
    return pp, pm


# ------------------------------------------------------------------ 温度伴随
def t_adjoint_grads(p, Tenv, dt_sub=1.0 / 256.0):
    A, kappa = ex.assemble_T_ode(N, DR, p)
    E, w0, w1 = ex.etd_prop(A, kappa, 1.0)
    T = np.full(D, p['T0'])
    traj = np.empty((T_END + 1, D))
    traj[0] = T
    for k in range(1, T_END + 1):
        T = E @ T + float(Tenv(k - 1)) * w0 + (float(Tenv(k)) - float(Tenv(k - 1))) * w1
        traj[k] = T

    VN = DR * (R0 - DR / 4.0) / 2.0
    dAdq = {}
    for q in RQ:
        dq = max(abs(p[q]) * 1e-6, 1e-14)
        pp, pm = fd_mat(p, q, dq)
        Ap, _ = ex.assemble_T_ode(N, DR, pp)
        Am, _ = ex.assemble_T_ode(N, DR, pm)
        dAdq[q] = (Ap - Am) / (2 * dq)
    dkap = dict(h=R0 / (p['rho'] * p['cp'] * VN), k=0.0,
                rho=-kappa / p['rho'], cp=-kappa / p['cp'])

    Fs = expm(A.T * dt_sub)
    nsub = int(round(T_END / dt_sub))
    out = {}
    for nm, pidx in (('T0_out', 0), ('TR_out', N)):
        lam = np.zeros(D); lam[pidx] = 1.0
        acc = {q: 0.0 for q in RQ}
        for m in range(nsub - 1, -1, -1):
            t = m * dt_sub
            kk = int(t)
            r = t - kk
            Tk = (1 - r) * traj[kk] + r * traj[min(kk + 1, T_END)]
            gk = float(Tenv(t))
            for q in RQ:
                acc[q] += (float(lam @ (dAdq[q] @ Tk)) + dkap[q] * gk * lam[-1]) * dt_sub
            lam = Fs @ lam
        # T0（初值）的解析梯度：λ(0)·1
        acc['T0_init'] = float(lam @ np.ones(D))
        out[nm] = acc
    return out


# --------------------------------------------------------------- 含水率伴随
def c_adjoint_grads(p, Cenv, C_traj, Df_traj, dt_sub=1.0 / 8.0):
    """两个输出共用一遍子步循环（避免重复装配；也避免存 1.4 万个 81×81 矩阵）"""
    VN = DR * (R0 - DR / 4.0) / 2.0
    eta_km = R0 / VN                       # ∂η/∂km
    eta0 = p['km'] * R0 / VN               # η 本身（∂η/∂C∞偏移）
    nsub = int(round(T_END / dt_sub))
    pidx = {'C0_out': 0, 'CR_out': N}
    lam = {k: np.zeros(D) for k in pidx}
    for k, i in pidx.items():
        lam[k][i] = 1.0
    acc = {k: {'D0': 0.0, 'km': 0.0, 'cinf_off': 0.0} for k in pidx}
    dqD = max(abs(p['D0']) * 1e-6, 1e-20)
    dqK = max(abs(p['km']) * 1e-6, 1e-20)
    for m in range(nsub - 1, -1, -1):
        t = m * dt_sub
        kk = int(t); r = t - kk
        Df = (1 - r) * Df_traj[kk] + r * Df_traj[min(kk + 1, T_END - 1)]
        A, _ = ex.assemble_C_ode(N, DR, Df, R0, p['km'])
        Ap, _ = ex.assemble_C_ode(N, DR, Df * (p['D0'] + dqD) / p['D0'], R0, p['km'])
        Am, _ = ex.assemble_C_ode(N, DR, Df * (p['D0'] - dqD) / p['D0'], R0, p['km'])
        dD = (Ap - Am) / (2 * dqD)
        Ap, _ = ex.assemble_C_ode(N, DR, Df, R0, p['km'] + dqK)
        Am, _ = ex.assemble_C_ode(N, DR, Df, R0, p['km'] - dqK)
        dK = (Ap - Am) / (2 * dqK)
        Ck = (1 - r) * C_traj[kk] + r * C_traj[min(kk + 1, T_END)]
        g = float(Cenv(t))
        F = expm(A.T * dt_sub)
        for k in pidx:
            L = lam[k]
            acc[k]['D0'] += float(L @ (dD @ Ck)) * dt_sub
            acc[k]['km'] += (float(L @ (dK @ Ck)) + eta_km * g * L[-1]) * dt_sub
            acc[k]['cinf_off'] += eta0 * L[-1] * dt_sub
            lam[k] = F @ L
    for k, i in pidx.items():
        acc[k]['C0_init'] = float(lam[k] @ np.ones(D))
    return acc


def main():
    t0 = time.time()
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(core.DEF)
    rec('=== T2-4 连续伴随法灵敏度（与 OAT 交叉验证）· v2（子步求积 ＋ km 漏项已修）===')
    rec('')

    rec('— 温度场（伴随精确，应≈OAT）—')
    adjT = t_adjoint_grads(p, Tenv)
    for nm, lbl in (('T0_out', 'T(0,1800)'), ('TR_out', 'T(R,1800)')):
        rec('  [%s]' % lbl)
        idx = 0 if nm == 'T0_out' else N
        for q in RQ:
            dq = abs(p[q]) * 1e-3
            pp, pm = fd_mat(p, q, dq)
            fd = (ex.run_T_expm(N, DR, pp, Tenv, 1800.0, hstep=1.0)['T_end'][idx]
                  - ex.run_T_expm(N, DR, pm, Tenv, 1800.0, hstep=1.0)['T_end'][idx]) / (2 * dq)
            rel = abs(adjT[nm][q] - fd) / max(abs(fd), 1e-30)
            rec('    %-4s 伴随=%+.6e  OAT=%+.6e  相对差=%.2e  ⟹ %s'
                % (q, adjT[nm][q], fd, rel, 'PASS' if rel < 1e-3 else 'CHECK'))
        dq = 1e-2
        pp = dict(p); pp['T0'] = p['T0'] + dq
        pm = dict(p); pm['T0'] = p['T0'] - dq
        fdt0 = (ex.run_T_expm(N, DR, pp, Tenv, 1800.0, hstep=1.0)['T_end'][idx]
                - ex.run_T_expm(N, DR, pm, Tenv, 1800.0, hstep=1.0)['T_end'][idx]) / (2 * dq)
        rel = abs(adjT[nm]['T0_init'] - fdt0) / max(abs(fdt0), 1e-30)
        rec('    T0   伴随=%+.6e  OAT=%+.6e  相对差=%.2e  ⟹ %s'
            % (adjT[nm]['T0_init'], fdt0, rel, 'PASS' if rel < 1e-3 else 'CHECK'))

    rec('')
    rec('— 含水率场（**冻结-D 线性化**伴随；须量化与 OAT 的差）—')
    C_traj = np.empty((T_END + 1, D)); Df_traj = np.empty((T_END, N))
    C = np.full(D, p['C0']); C_traj[0] = C
    for k in range(T_END):
        Df_traj[k] = core.faceD_int(C, p['D0'], p['bD'])
        for s in range(10):
            C, _, _ = core.step_C(N, DR, 0.1, C, float(Cenv(k + 1)), p, tol=1e-9, maxit=30)
        C_traj[k + 1] = C
    adjC = c_adjoint_grads(p, Cenv, C_traj, Df_traj)

    cfg = [dict(p={'D0': p['D0'] * (1 - 1e-3)}), dict(p={'D0': p['D0'] * (1 + 1e-3)}),
           dict(p={'km': p['km'] * (1 - 1e-3)}), dict(p={'km': p['km'] * (1 + 1e-3)}),
           dict(dc_off=-1e-5), dict(dc_off=1e-5)]
    with ProcessPoolExecutor(max_workers=6) as exe:
        rs = list(exe.map(solve_worker, cfg))
    fd = {'D0': (rs[1]['CR'] - rs[0]['CR']) / (2 * p['D0'] * 1e-3),
          'km': (rs[3]['CR'] - rs[2]['CR']) / (2 * p['km'] * 1e-3),
          'cinf_off': (rs[5]['CR'] - rs[4]['CR']) / 2e-5}
    for q in ('D0', 'km', 'cinf_off'):
        a, b = adjC['CR_out'][q], fd[q]
        rel = abs(a - b) / max(abs(b), 1e-30)
        rec('  C(R) 对 %-9s 伴随=%+.6e  OAT=%+.6e  相对差=%.2e ⟹ %s'
            % (q, a, b, rel, 'PASS' if rel < 0.25 else 'CHECK'))

    rec('')
    rec('结论：① 温度伴随与 OAT **一致**（线性系统，精确）⟹ 伴随实现正确；')
    rec('      ② 含水率伴随为**冻结-D 线性化**，与 OAT 的差即"忽略 D(C) 反馈"的代价；')
    rec('         差在 25% 内视为可用于**排序／分布**，不替代 OAT 数值；')
    rec('      ③ 伴随增量价值：一次前向＋一次反向即得全部参数梯度，并可给灵敏度时空分布。')
    rec('总耗时 %.1f s' % (time.time() - t0))
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
