# -*- coding: utf-8 -*-
r"""
Q3 诊断 ①｜常数 D ＋ Robin 圆柱：本格式 vs **Carslaw-Jaeger 解析级数**
================================================================================
**目的**：判别"表面薄层 $\delta=D/k_m\ll\Delta r$ 未被分辨"是否使本有限体积格式失准（候选 m1）。

**构造式隔离**：取常数 $D$（$C$、$T$ 冻结）＋ 可调 $k_m$ ⟹ 可任意设定
$\mathrm{Bi}=k_mR_0/D$；该问题**有解析解**：
$$u=\frac{C-C_\infty}{C_0-C_\infty},\qquad
  u(x,\mathrm{Fo})=\sum_{n\ge1}\frac{2\,\mathrm{Bi}}{(\mu_n^2+\mathrm{Bi}^2)J_0(\mu_n)}J_0(\mu_n x)e^{-\mu_n^2\mathrm{Fo}}$$
$\mu_n$ 为 $\mu J_1(\mu)=\mathrm{Bi}\,J_0(\mu)$ 的第 $n$ 个正根；$\mathrm{Fo}=Dt/R_0^2$、$x=r/R_0$。
比较量：$u(0)$、$u(1)$（**表面值**）、无量纲总质量 $M=2\!\int_0^1u\,x\,dx$。

**两步**：
  **第 1 步（代码体检）**：`q3_core` 的 `frozen` 分支用的是**模块全局 `D_FAC`**（njit 内会按编译期常量冻结），
  而**不是**入参 `d_fac` ⟹ 构造对照实验：同进程内先取 `D_FAC=1`、再取 `D_FAC=3`，看结果是否变化。
  **第 2 步（格式判别）**：改用 `q3_core_nu`（其 frozen 分支用**入参 `d_fac`**，无全局歧义），
  设定 $D=10^{-8}$，扫描 $\mathrm{Bi}$ 与网格，与解析解对拍。

用法：
  python q3_diag_mech.py            # 规模声明
  python q3_diag_mech.py --go       # 执行（或 ALLOW_RUN=1）
"""
import sys
import os
import time
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
from scipy.special import j0, j1
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))

import q3_core as q3                                                # noqa: E402
import q3_core_nu as nu                                             # noqa: E402
from q2_core_c import DEF2                                          # noqa: E402

LOG = os.path.join(HERE, 'q3_diag_mech_log.txt')
R0 = DEF2['R0']
C0 = DEF2['C0']
T0 = DEF2['T0']
CINF = 0.05
HH, NSUB = 1.0 / 32.0, 1920
D_BASE = 2.4e-3 * np.exp(-0.45 / C0) * np.exp(-3850.0 / (T0 + 273.15))   # d_fac=1 时的常数 D
D_TGT = 1.0e-8
FO_LIST = (0.02, 0.05, 0.10, 0.20, 0.40)
BUF = []


def say(s=''):
    print(s)
    BUF.append(s)


def mu_roots(Bi, nmax=200):
    mus = []
    for k in range(nmax):
        a = 1e-10 if k == 0 else k * np.pi + 1e-10
        b = (k + 1) * np.pi - 1e-10
        if (a * j1(a) - Bi * j0(a)) * (b * j1(b) - Bi * j0(b)) > 0:
            continue
        mus.append(brentq(lambda m: m * j1(m) - Bi * j0(m), a, b))
    return np.array(mus)


def exact(Bi, Fo, mus):
    A = 2.0 * Bi / (mus ** 2 + Bi ** 2)
    e = np.exp(-mus ** 2 * Fo)
    return (float(np.sum(A / j0(mus) * e)), float(np.sum(A * e)),
            float(np.sum(4.0 * Bi ** 2 / (mus ** 2 * (mus ** 2 + Bi ** 2)) * e)))


def env_const(cinf):
    return np.array([0.0, 1e18]), np.array([T0, T0]), np.array([cinf, cinf])


def probe_global():
    """第 1 步：q3_core 的 frozen 分支是否随模块全局 D_FAC 变化？（同进程内）"""
    say('第 1 步｜代码体检：q3_core frozen 分支对模块全局 D_FAC 的响应')
    N, nst = 80, 20
    ts, Tv, Cv = env_const(CINF)
    out = []
    for fac in (1.0, 3.0):
        q3.D_FAC = fac
        T = np.full(N + 1, T0)
        C = np.full(N + 1, C0)
        for n in range(1, nst + 1):
            T, C, _ = q3.step_imex_fast(N, R0 / N, HH, NSUB, R0, 10.0, 8e-7,
                                        T, C, ts, Tv, Cv, (n - 1) * 60.0, mode='frozen')
        out.append(float(C[-1]))
    q3.D_FAC = 1.0
    say('   D_FAC=1.0 → C(R)=%.10f ；D_FAC=3.0 → C(R)=%.10f ；相对变化 %.3e'
        % (out[0], out[1], abs(out[1] - out[0]) / out[0]))
    say('   ⟹ %s' % ('**frozen 分支忽略入参、按编译期常量取 D_FAC（=首次编译时的全局值）**'
                     if abs(out[1] - out[0]) < 1e-12 else 'frozen 分支随全局 D_FAC 变化（正常）'))
    return out


def run_fv(N, d_fac, km, fo_max):
    """用 q3_core_nu 的 frozen 模式（入参 d_fac 生效）解常数 D 问题。"""
    g = nu.geom_uniform(N, R0)
    ts, Tv, Cv = env_const(CINF)
    T = np.full(N + 1, T0)
    C = np.full(N + 1, C0)
    idx = {fo: max(1, int(round(fo * R0 * R0 / (D_TGT * 60.0)))) for fo in FO_LIST}
    idx_max = max(idx.values())
    V = g['V']
    Vsum = V.sum()
    out = {}
    for n in range(1, idx_max + 1):
        T, C, _ = nu.step_imex_gen(g, HH, NSUB, R0, 10.0, km, T, C, ts, Tv, Cv,
                                   (n - 1) * 60.0, d_fac=d_fac, mode='frozen')
        for fo, k in idx.items():
            if n == k:
                u = (C - CINF) / (C0 - CINF)
                out[fo] = (float(u[0]), float(u[-1]), float(np.sum(u * V) / Vsum))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--go', action='store_true')
    args = ap.parse_args()
    bis = (2.0, 20.0, 200.0, 2000.0, 20000.0)
    ns = (80, 160, 320)
    if not (args.go or os.environ.get('ALLOW_RUN') == '1'):
        est = sum(8.5 * (N + 1) / 81.0 for _ in bis for N in ns)
        print('[SCALE] q3_diag_mech 规模声明：')
        print('        第1步 代码体检：2 例 × 20 输出步（N=80）')
        print('        第2步 常数D对拍：Bi=%s × N=%s ⇒ %d 例，推至 Fo=0.4，内部步 1/32 s'
              % ('/'.join('%.0f' % b for b in bis), '/'.join(str(n) for n in ns), len(bis) * len(ns)))
        print('        预计 ≈%.0f s；**仅作格式判别，不产交付物**。加 --go 执行。' % (est + 10))
        return

    d_fac = D_TGT / D_BASE
    say('=' * 100)
    say('Q3 诊断①：常数 D ＋ Robin 圆柱 —— 本格式 vs Carslaw-Jaeger 解析级数')
    say('=' * 100)
    say('  d_fac = %.6f ⟹ D = d_fac·D_BASE = %.4e m²/s（常数）；C0=%.2f；C∞=%.3f；内部步 1/32 s'
        % (d_fac, D_TGT, C0, CINF))
    say()
    probe_global()
    say()
    say('第 2 步｜格式判别（q3_core_nu，D 由入参 d_fac 给定）')
    say('  %-8s %-6s %-8s %-8s | %-13s | %-13s | %-13s'
        % ('Bi', 'N', 'δ/mm', 'Fo', 'u(0) 误差', 'u(1)≈表面 误差', '总质量 误差'))
    say('  ' + '-' * 92)
    t0 = time.time()
    for Bi in bis:
        km = Bi * D_TGT / R0
        delta = D_TGT / km
        mus = mu_roots(Bi)
        for N in ns:
            fv = run_fv(N, d_fac, km, max(FO_LIST))
            for fo in FO_LIST:
                u0e, u1e, Me = exact(Bi, fo, mus)
                u0n, u1n, Mn = fv[fo]
                say('  %-8.0f %-6d %-8.4f %-8.3f | %+11.3e | %+11.3e | %+11.3e'
                    % (Bi, N, delta * 1e3, fo,
                       (u0n - u0e) / abs(u0e), (u1n - u1e) / abs(u1e), (Mn - Me) / abs(Me)))
    say()
    say('  第 2 步耗时 %.1f s' % (time.time() - t0))
    say()
    say('  ★ 判读：δ/Δr≫1（良分辨）与 δ/Δr≪1（薄层）两端的误差若都 ≲1e-3，则')
    say('     **m1（薄层未分辨使格式失准）不成立** ⟹ 52% 误差只能源自"变系数 D 的处理"。')
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    print('已写出：%s' % LOG)


if __name__ == '__main__':
    main()
