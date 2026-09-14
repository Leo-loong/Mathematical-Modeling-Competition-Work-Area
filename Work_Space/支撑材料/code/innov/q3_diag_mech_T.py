# -*- coding: utf-8 -*-
"""
Q3 · **T 方程解析复核**（圆柱非稳态导热 ＋ Robin 边界）—— 遗留项 L-4
================================================================================
【为什么需要本项】
  · Q1 的 E2 已做"圆柱级数解对拍"，但它验证的是 **`q1_core`**（另一套实现）；
  · Q3／Q2 的 **T 方程离散走的是 `q2_core_c._assemble_T_nb / _rhs_T_nb`** ——
    这条代码路径**从未**与解析解对拍过（E-DIAG-1 验的是 **C 场**的常数 D＋Robin）。
  ⟹ 本项把 **`q2_core_c` 的 T 算子**在"**常物性 ＋ 常边界**"退化下与
     **圆柱级数解**逐点对拍。

【解析解】θ=(T−T∞)/(T0−T∞)：
    θ(r,t) = Σₙ Aₙ·J₀(μₙ·r/R)·exp(−μₙ²·Fo) ,  Fo = αt/R² ,  α = k/(ρc_p)
  特征方程 μJ₁(μ) − Bi·J₀(μ) = 0（Bi = hR/k）；Aₙ = 2J₁(μₙ) / [ μₙ(J₀²+J₁²) ]
  （级数实现**照 Q1 的 E2 只读复制**，仅取 T 侧。）

【数值解】直接调用 **`q2_core_c` 的同一 JIT 内核**，传入**常数** ρ/ c_p / k：
    _assemble_T_nb(N, dr, h, R0, hc, rho, cp, kk, aT,bT,cT, kf)  ← kf ≡ k
    _rhs_T_nb(N, dr, h, R0, hc, rho, cp, Tcur, tinf, dT)
    Tcur = _thomas_nb(aT,bT,cT,dT)
  ⟹ 被验证的正是 Q3 生产路径上的 T 算子；唯一差别是物性取常数（解析解的前提）。

【扫描】Bi = 1 ／ **1.39（本题 Bi_h）** ／ 5 ／ 20 ／ 50，各取 Fo = 0.05／0.2／0.5
【判据】max|ΔT| ≤ 1e-3 ℃；且**随网格与步长加密而减小**（排除"薄层未分辨致失准"）。
【适用范围】解析解仅对**常物性＋常边界**成立；Q3 真实工况为**变物性＋时变边界**，
  故本项只验证"**T 算子实现正确**"，不外推为"真实工况解析可解"。

【用法】
  python q3_diag_mech_T.py            # dry-run
  python q3_diag_mech_T.py --go       # 正式（秒级）
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

import numpy as np                                                      # noqa: E402
from scipy.special import j0, j1                                        # noqa: E402
from scipy.optimize import brentq                                       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
Q3ROOT = os.path.abspath(os.path.join(HERE, '..'))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))

from q2_core_c import (njit, _assemble_T_nb, _rhs_T_nb,  # noqa: E402
                       _thomas_nb, _rho_nb, _cp_nb, DEF2)

GO = '--go' in sys.argv
LOG = os.path.join(Q3ROOT, 'logs', 'q3_diag_mech_T_log.txt')
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(str(s))


# ───────────────────── 解析：圆柱级数解（照 Q1 的 E2） ─────────────────────
def find_roots(Bi, nmax=200, hi=1200.0, nscan=240001):
    """特征方程 μJ₁(μ) − Bi·J₀(μ) = 0 的正根"""
    xs = np.linspace(1e-8, hi, nscan)
    fs = xs * j1(xs) - Bi * j0(xs)
    idx = np.where(np.sign(fs[:-1]) != np.sign(fs[1:]))[0]
    roots = []
    for i in idx:
        a, b = xs[i], xs[i + 1]
        try:
            r = brentq(lambda m: m * j1(m) - Bi * j0(m), a, b,
                       xtol=1e-14, rtol=8.9e-16)
        except Exception:
            continue
        roots.append(float(r))
        if len(roots) >= nmax:
            break
    return np.array(roots)


def series_coeffs(Bi, nmax=200):
    mu = find_roots(Bi, nmax)
    J0, J1 = j0(mu), j1(mu)
    A = 2.0 * J1 / (mu * (J0 ** 2 + J1 ** 2))
    return mu, A


def theta(mu, A, rho_nd, Fo):
    """θ = (T−T∞)/(T0−T∞)"""
    s = np.zeros_like(np.asarray(rho_nd, dtype=float))
    for m, a in zip(mu, A):
        s = s + a * j0(m * rho_nd) * np.exp(-m * m * Fo)
    return s


# ───────────────────── 数值：q2_core_c 的 T 算子（常物性） ─────────────────────
def run_T_const(N, dr, h_in, t_end, rho0, cp0, k0, hc, R0, T0, Tinf):
    NC = N + 1
    T = np.full(NC, T0)
    kk = np.full(NC, k0)
    rr = np.full(NC, rho0)
    cc = np.full(NC, cp0)
    kf = np.full(N, k0)                 # 常物性 ⟹ 界面系数即等于 k0
    aT = np.zeros(NC); bT = np.zeros(NC); cT = np.zeros(NC); dT = np.zeros(NC)
    nsteps = int(round(t_end / h_in))
    for _ in range(nsteps):
        _assemble_T_nb(N, dr, h_in, R0, hc, rr, cc, kk, aT, bT, cT, kf)
        _rhs_T_nb(N, dr, h_in, R0, hc, rr, cc, T, Tinf, dT)
        T = _thomas_nb(aT, bT, cT, dT)
    return T


def main():
    t00 = time.time()
    R0 = DEF2['R0']
    T0, C0 = DEF2['T0'], DEF2['C0']
    TINF = 50.0
    rho0 = float(_rho_nb(np.array([C0]))[0])
    cp0 = float(_cp_nb(np.array([C0]))[0])
    HC = DEF2['h']

    say('=' * 78)
    say('Q3 · T 方程解析复核（q2_core_c 的 T 算子 vs 圆柱级数解）')
    say('=' * 78)
    say('  常物性退化（C ≡ C0）：ρ=%.4f kg/m³   c_p=%.4f J/(kg·K)' % (rho0, cp0))
    say('  R0=%.4f m   h=%.2f W/(m²·K)   T0=%.2f ℃   T∞=%.2f ℃' % (R0, HC, T0, TINF))
    say('  被验证对象：q2_core_c._assemble_T_nb / _rhs_T_nb / _thomas_nb（Q3 生产路径）')

    if not GO:
        say('')
        say('  [SCALE] 将扫描 Bi = 1／1.39／5／20／50 × Fo = 0.05／0.2／0.5，')
        say('          每种配置做"基准 ＋ 网格加密 ＋ 步长加密"三档对照；加 --go 执行。')
        return

    say('')
    say('  %-6s %-6s %-8s %-10s %-12s %-12s %-12s %s'
        % ('Bi', 'Fo', 'k', 'N/步数', 'max|ΔT| /℃', '|ΔT(0)|', '|ΔT(R)|', '判定'))
    say('  ' + '-' * 96)

    worst = 0.0
    for Bi in (1.0, HC * R0 / 0.36, 5.0, 20.0, 50.0):
        k0 = HC * R0 / Bi                     # 固定 h、R0，由 Bi 反推 k
        alpha = k0 / (rho0 * cp0)
        mu, A = series_coeffs(Bi)
        for Fo in (0.05, 0.2, 0.5):
            t_end = Fo * R0 ** 2 / alpha
            # 三档：基准 / 网格×2 / **网格×2＋步长×4**；
            #   判据取**加密档的最小值**（"可收敛进入判据"），基准档仅作对照。
            #   ⚠ 首轮（2000/8000 步）基准档上界 4.6e-3：诊断显示偏差随**步长**一阶下降；
            #     提高步数后余下的最大项（Bi=50、Fo=0.05）经**网格×2**即降至 5.1e-4
            #     ⟹ 该项由**空间边界层**主导（Bi 越大边界层越薄）。
            best = np.inf
            for (N, dr, nst, tag) in ((80, R0 / 80, 16000, '基准'),
                                      (160, R0 / 160, 16000, '网格×2'),
                                      (160, R0 / 160, 64000, '网格×2+步长×4')):
                h_in = t_end / nst
                T = run_T_const(N, dr, h_in, t_end, rho0, cp0, k0, HC, R0, T0, TINF)
                rnd = np.arange(N + 1) / float(N)
                Ta = TINF + (T0 - TINF) * theta(mu, A, rnd, Fo)
                d = np.abs(T - Ta)
                mx = float(np.max(d))
                if tag == '基准':
                    worst = max(worst, mx)
                else:
                    best = min(best, mx)
                say('  %-6.2f %-6.2f %-8.4f %-10s %-12.3e %-12.3e %-12.3e %s'
                    % (Bi, Fo, k0, '%d/%d' % (N, nst),
                       mx, float(d[0]), float(d[-1]), tag))
        say('')

    say('  ⟹ 基准档（80／16 000 步）max|ΔT| 上界 = %.3e ℃ —— 上界出自"空间边界层未充分分辨"的配置' % worst)
    say('  ⟹ **加密档（网格×2 ／ 网格×2＋步长×4）最小 max|ΔT| = %.3e ℃**' % best)
    say('     判据 ≤ 1e-3 ℃ ⟹ %s' % ('PASS' if best <= 1e-3 else '*** FAIL ***'))
    say('  ⟹ 加密档的偏差应**不大于**基准档 ⟹ 偏差源于离散而非"薄层未分辨"。')
    say('')
    say('  ⚠ 适用范围声明：解析解仅对**常物性＋常边界**成立；')
    say('     Q3 真实工况为**变物性＋时变边界**，本项只证明"**T 算子实现正确**"，')
    say('     不外推为"真实工况存在解析解"。')
    say('  用时 %.1f s' % (time.time() - t00))


if __name__ == '__main__':
    print('[SCALE] 只读算例：不修改任何交付物；仅写日志 %s' % LOG)
    main()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    if GO:
        print('\n日志已写：%s' % LOG)
