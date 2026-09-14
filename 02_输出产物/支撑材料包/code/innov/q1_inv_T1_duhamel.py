# -*- coding: utf-8 -*-
"""T1-1 Duhamel／Green 半解析解（真实**连续时变**边界）· 独立参照轨

目的：把解析对拍从"常边界／分段常边界"扩展到**真实连续时变边界**（附件1 分段线性），
      并**单独量化** E2b 阶梯近似本身的偏差。

构造（T 方程为线性常系数，可严格叠加；T∞(0)=T0=28 ℃ ⟹ dT∞ 在 t=0 无跳跃原子）：
  单位阶跃响应（零初值、T∞≡1）：ψ(r,t) = 1 - Σ_n a_n J0(μ_n ρ) e^{-μ_n² Fo}
      a_n = 2J1(μ_n) / [μ_n (J0²+J1²)],  μ_n J1(μ_n) = Bi_T J0(μ_n),  Fo = α t / R0²
  则 T(r,t) = T0[1-ψ(r,t)] + ∫_0^t ψ(r,t-s) dT∞(s)
  边界分段线性（Δt_knot = 60 s）⟹ 积分为有限项求和：
      ∫ = Σ_k m_k [Ψ(r, t-t_k) - Ψ(r, t-t_{k+1}^*)]
      Ψ(r,τ) = ∫_0^τ ψ du = τ - (R0²/α) Σ_n a_n J0(μ_n ρ) (1-e^{-μ_n² S}) / μ_n² ,  S = α τ / R0²
      m_k = ΔT∞_k / Δt_knot

对照：① 与主力数值解（后向欧拉 1/32 s）逐点比；② 与"阶梯近似"（E2b 口径）比。

运行：python q1_inv_T1_duhamel.py
"""
import numpy as np
from scipy.special import j0, j1
from scipy.optimize import brentq

from q1_inv_lib import Rec, env_fns, load_result1   # 先导入 lib（其内部把 ../code 加入 sys.path）
import q1_core as core                              # noqa: E402
from q1_core import DEF                             # noqa: E402

rec = Rec('q1_inv_T1_duhamel.log')
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
RHO = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
NKNOT = 60.0


def find_roots(Bi, nmax=200, hi=1200.0, nscan=240001):
    xs = np.linspace(1e-8, hi, nscan)
    fs = xs * j1(xs) - Bi * j0(xs)
    idx = np.where(np.sign(fs[:-1]) != np.sign(fs[1:]))[0]
    roots = []
    for i in idx:
        a, b = xs[i], xs[i + 1]
        try:
            r = brentq(lambda m: m * j1(m) - Bi * j0(m), a, b, xtol=1e-14, rtol=8.9e-16)
        except Exception:
            continue
        roots.append(float(r))
        if len(roots) >= nmax:
            break
    return np.array(roots)


def series_coeffs(Bi, nmax=200):
    mu = find_roots(Bi, nmax)
    J0, J1 = j0(mu), j1(mu)
    return mu, 2.0 * J1 / (mu * (J0 ** 2 + J1 ** 2))


def psi_and_int(mu, A, rho, tau_s, alpha, R0, tau_max):
    """一次算出 τ 落在 [0, tau_max] 上多个点的 (ψ, Ψ)。"""
    tau = np.atleast_1d(np.asarray(tau_s, dtype=float))
    S = alpha * tau / R0 ** 2
    th = np.zeros_like(tau)
    intth = np.zeros_like(tau)
    for n in range(len(mu)):
        c = A[n] * j0(mu[n] * rho)
        e = np.exp(-mu[n] ** 2 * S)
        th += c * e
        intth += c * (1.0 - e) / mu[n] ** 2
    return 1.0 - th, tau - (R0 ** 2 / alpha) * intth


def knots_upto(ts):
    ks = [k * NKNOT for k in range(int(ts // NKNOT) + 1)]
    if ks[-1] < ts - 1e-9:
        ks.append(float(ts))
    return ks


def duhamel_continuous(mu, A, rho, ts, tgrid, Tinf, alpha, R0, T0):
    """真实分段线性边界的半解析解（无阶梯近似）"""
    ks = knots_upto(ts)
    taus = [ts - k for k in ks]                       # 与 ks 同序（递减）
    psi, Psi = psi_and_int(mu, A, rho, taus, alpha, R0, ts)
    P = {k: Psi[i] for i, k in enumerate(ks)}
    # T∞(0)=T0 ⟹ 边界的初值原子项 T∞(0)·ψ 与齐次项 T0(1−ψ) 恰好抵消：
    #   T(r,t) = T0·(1−ψ) + [T∞(0)·ψ + ∫ψ dT∞] = T0 + ∫_0^t ψ(r,t−s) dT∞(s)
    val = float(T0)
    for i, k in enumerate(ks[:-1]):
        k1 = ks[i + 1]
        mk = (float(np.interp(k1, tgrid, Tinf)) - float(np.interp(k, tgrid, Tinf))) / (k1 - k)
        val += mk * (P[k] - P[k1])
    return float(val)


def duhamel_staircase(mu, A, rho, ts, tgrid, Tinf, alpha, R0, T0):
    """阶梯近似（E2b 口径）：每 60 s 取该段常数，按增量叠加"""
    lv = [float(np.interp(i * NKNOT, tgrid, Tinf)) for i in range(int(ts // NKNOT) + 1)]
    val = T0
    for j in range(1, len(lv)):
        tj = j * NKNOT
        if tj >= ts:
            break
        d = lv[j] - lv[j - 1]
        if d == 0.0:
            continue
        psi, _ = psi_and_int(mu, A, rho, [ts - tj], alpha, R0, ts)
        val += d * psi[0]
    return float(val)


def main():
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(DEF)
    R0 = p['R0']
    alpha = p['k'] / (p['rho'] * p['cp'])
    BiT = p['h'] * R0 / p['k']
    mu, A = series_coeffs(BiT)
    rec('=== T1-1 Duhamel／Green 半解析（真实连续时变边界）===')
    rec('alpha=%.6e m^2/s   Bi_T=%.6f   特征根 %d 个（μmax=%.2f）' % (alpha, BiT, len(mu), mu[-1]))
    rec('')

    res = core.run_sim(N=80, dr=0.25e-3, dt_out=1.0, nsteps=1800, p=p,
                       Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                       center='fv', surf='fvm', solve_C=False, snap_at=set(SNAP))

    rec('%6s %7s %14s %16s %12s %12s' % ('t/s', 'r/cm', '数值(隐式)', '半解析(连续)', 'Δ连续/℃', '阶梯偏差/℃'))
    dmax_c = dmax_s = 0.0
    for ts in SNAP:
        for rho in RHO:
            i = int(round(rho * R0 / 0.25e-3))
            num = float(res['T_snap'][ts][i])
            ana = duhamel_continuous(mu, A, rho, float(ts), t, Tinf, alpha, R0, p['T0'])
            st = duhamel_staircase(mu, A, rho, float(ts), t, Tinf, alpha, R0, p['T0'])
            dmax_c = max(dmax_c, abs(num - ana))
            dmax_s = max(dmax_s, abs(ana - st))
            rec('%6d %7.2f %14.6f %16.6f %12.2e %12.2e' % (ts, rho * R0 * 100, num, ana, num - ana, ana - st))
    rec('')
    rec('全场 |数值 − 半解析(连续)| 最大 = %.3e ℃' % dmax_c)
    rec('全场 |半解析(连续) − 阶梯近似| 最大 = %.3e ℃  ⟸ E2b 阶梯近似本身带来的偏差' % dmax_s)

    _, dist, Tt, _ = load_result1()
    idxT = [int(round(rho * 20)) for rho in RHO]      # 交付表列＝0.1 cm 网格（21 列）
    bad = 0
    for ts in SNAP:
        for rho, i in zip(RHO, idxT):
            ana = duhamel_continuous(mu, A, rho, float(ts), t, Tinf, alpha, R0, p['T0'])
            if round(ana, 4) != round(float(Tt[ts - 1, i]), 4):
                bad += 1
    rec('与交付表 T（7×5 = 35 格）4 位小数不一致格数 = %d' % bad)
    rec('')
    rec('⟹ 判定：阈值 2e-4 ℃ ⟹ %s（实测 %.2e ℃）' % ('PASS' if dmax_c <= 2e-4 else 'CHECK', dmax_c))
    rec('   阶梯近似偏差已单独量化 ⟹ 可直接回答"E2b 阶梯近似本身多大"。')
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
