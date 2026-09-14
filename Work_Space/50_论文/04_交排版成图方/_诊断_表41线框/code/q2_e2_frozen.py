# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验 E2：**常物性退化对拍**
======================================================
为什么需要它
------------
Q2 的物性随 C、T 变化 ⟹ 方程非线性 ⟹ **解析解不存在**，Q1 的"级数解对拍"手段失效。
对策：把变物性代码**退化为常物性**（物性全部冻结为 C0 处的常数），
此时问题回到线性抛物型 ⟹ 可与**圆柱非稳态导热级数解**逐点对拍。

它证明什么 / 不证明什么
----------------------
· 证明：**变物性框架下的离散与实现是正确的**（同样的装配、同样的追赶法、同样的耦合循环）；
· 不证明：变物性本身的物理正确性——那由题面给定的附录3 公式保证（H4／H10）。
（此边界须在论文"模型检验"节如实写出。）

对照设置
--------
· 边界：**恒定** T∞=50 ℃（级数解要求常边界）
· 物性：冻结为 C0 处常数 ρ=976.4、c_p=3415.3、k=0.4830、D=5.6417e-9
· 空间：Δr=0.25 mm（N=80）；时间：Δt_T=1/32 s（与主力同）
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 线程环境变量须早于 numpy 导入（小规模三对角求解无需多线程）
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
from scipy.special import j0, j1
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q2_core import run_q2, rho_of, cp_of, k_of, D_of, DEF2   # noqa: E402

R0, H = DEF2['R0'], DEF2['h']
T0, C0 = DEF2['T0'], DEF2['C0']
TINF = 50.0
T_END = 1800.0


# ------------------------------------------------------------------
# 圆柱非稳态导热级数解（第一类边界为 Robin；常物性）
#   θ = (T-∞)/(T0-∞) = Σ 2Bi/[(μn²+Bi²)J0(μn)] · J0(μn·r/R) · exp(-μn²·Fo)
#   特征根：μ·J1(μ) = Bi·J0(μ)
# ------------------------------------------------------------------
def char_roots(Bi, nmax=200, mumax=400.0, dx=0.02):
    """求 μJ1(μ)=Bi·J0(μ) 的前 nmax 个正根（扫描 + brentq 精化）"""
    f = lambda m: m * j1(m) - Bi * j0(m)
    out = []
    x = dx
    prev = f(1e-8)
    while len(out) < nmax and x < mumax:
        cur = f(x)
        if (prev < 0.0) != (cur < 0.0):
            try:
                r = brentq(f, x - dx, x, xtol=1e-13, rtol=1e-15)
                if r > 1e-6:
                    out.append(r)
            except ValueError:
                pass
        prev = cur
        x += dx
    return np.array(out)


def series_theta(r_over_R, Fo, Bi, mus):
    """级数解（返回 θ；r_over_R 可为标量或数组）"""
    c = 2.0 * Bi / ((mus ** 2 + Bi ** 2) * j0(mus))
    x = np.asarray(r_over_R, dtype=float)
    J = j0(np.outer(x, mus).reshape(x.shape + mus.shape)) if x.ndim else j0(x * mus)
    decay = np.exp(-mus ** 2 * Fo)
    if x.ndim == 0:
        return float(np.sum(c * j0(x * mus) * decay))
    return np.sum(J * (c * decay)[None, :], axis=-1)


def main():
    rho = float(rho_of(C0)); cp = float(cp_of(C0)); kk = float(k_of(C0))
    Dd = float(D_of(C0, T0))
    alpha = kk / (rho * cp)
    Bi = H * R0 / kk
    print("=" * 74)
    print("Q2 检验 E2：常物性退化对拍")
    print(f"  冻结物性：rho={rho:.4f}  cp={cp:.4f}  k={kk:.6f}  D={Dd:.6e}")
    print(f"  alpha={alpha:.6e} m²/s   Bi=hR0/k={Bi:.6f}   边界：恒定 {TINF} ℃")
    mus = char_roots(Bi)
    print(f"  特征根数：{len(mus)}（μ1={mus[0]:.6f}）")
    # 级数解自检：Fo→0 时 θ→1
    s0 = series_theta(0.0, 1e-12, Bi, mus)
    print(f"  [自检] Fo→0 时 θ(0)={s0:.10f}（应≈1）")

    # ---- 数值解（mode='frozen'）----
    # 【性能优化】原版此处**用完全相同设置连跑两次**（先跑一次只为打印迭代轮数，
    # 再跑一次带 snap_at 做对拍）⟹ 纯冗余。现合并为**单次运行**（带 snap_at），
    # 迭代轮数从同一结果读取；数值设置（N/dr/dt_out/nsteps/subT/subC/mode）一字未改。
    nsteps = int(T_END)
    snaps = (100, 300, 600, 900, 1200, 1500, 1800)
    t0 = time.time()
    res2, _, _ = run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=nsteps,
                        Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: 0.04999,
                        subT=32, subC=10, mode='frozen', snap_at=snaps)
    print(f"  [数值] 外层迭代均 {res2['stats']['outer_tot']/max(1,res2['stats']['nsub']):.2f} 轮"
          f"（frozen 应≈1）  总耗时 {time.time()-t0:.1f}s（单次运行）")

    # ---- 对拍（利用 snap 取整数时刻）----
    print("\n  t(s)     r=0 数值 / 解析 / 偏差(℃)        r=R 数值 / 解析 / 偏差(℃)")
    dmax0 = dmaxR = 0.0
    for n in snaps:
        t = float(n)
        Fo = alpha * t / R0 ** 2
        a0 = TINF + (T0 - TINF) * series_theta(0.0, Fo, Bi, mus)
        aR = TINF + (T0 - TINF) * series_theta(1.0, Fo, Bi, mus)
        Tn = res2['T_snap'][n]
        n0, nR = float(Tn[0]), float(Tn[-1])
        e0, eR = n0 - a0, nR - aR
        dmax0 = max(dmax0, abs(e0)); dmaxR = max(dmaxR, abs(eR))
        print(f"  {t:6.0f}   {n0:10.6f} / {a0:10.6f} / {e0:+.2e}      "
              f"{nR:10.6f} / {aR:10.6f} / {eR:+.2e}")
    print(f"\n  最大偏差：中心 {dmax0:.3e} ℃  表面 {dmaxR:.3e} ℃")
    print("  判定：与 Q1 的同型对拍（10⁻³ 量级，由时间离散主导）可比即为通过；")
    print("        细化 Δt_T 后应降至 10⁻⁵ 量级。")


if __name__ == '__main__':
    main()
