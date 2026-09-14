# -*- coding: utf-8 -*-
"""
Q1 补充实验：几何降维（圆柱 vs 球体）与边界条件情景对机构《GT04/GS05》公布值的检验
==================================================================================
机构《GS05》《GT04》按**球坐标**建模；其余文档按圆柱（1/r）。
本实验用同一套元体平衡 + 全隐式 + 半格表面格式，只切换几何指数 p
（柱：p=1；球：p=2）与边界情景（附件1 时变 / 恒定 50 ℃），给出 1800 s 结果。
优化：Q1 温度方程是线性的（ρ、c_p、k 为常数），T 单独一次线性解；只对 C 做 Picard。
"""
import io
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import make_env, T1, TAIR, CAIR

OUT = os.path.join(HERE, 'exp_geom_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(s)


def thomas(a, b, c, d):
    n = len(b)
    cp_ = np.empty(n - 1); dp_ = np.empty(n)
    cp_[0] = c[0] / b[0]; dp_[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp_[i - 1]
        dp_[i] = (d[i] - a[i] * dp_[i - 1]) / m
        if i < n - 1:
            cp_[i] = c[i] / m
    x = np.empty(n); x[-1] = dp_[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp_[i] - cp_[i] * x[i + 1]
    return x


def solve(pg, N=80, R0=0.02, dtT=1 / 8, dtC=1 / 32, nsteps=1800, dt_out=1.0,
          Tenv=None, Cenv=None, picard=25, tol=1e-10, omega=0.7):
    dr = R0 / N
    r = np.arange(N + 1) * dr
    h, km = 25.0, 8.0e-7
    V0 = (dr / 2) ** (pg + 1) / (pg + 1.0)
    A12 = (dr / 2) ** pg
    VN = (R0 ** (pg + 1) - (R0 - dr / 2) ** (pg + 1)) / (pg + 1.0)
    Am = (R0 - dr / 2) ** pg
    Vi = np.empty(N + 1)
    Au = np.empty(N + 1); Al = np.empty(N + 1)
    Vi[0] = V0; Vi[N] = VN
    Au[0] = A12; Al[0] = 0.0
    Au[N] = 0.0; Al[N] = Am
    for i in range(1, N):
        Vi[i] = ((r[i] + dr / 2) ** (pg + 1) - (r[i] - dr / 2) ** (pg + 1)) / (pg + 1)
        Au[i] = (r[i] + dr / 2) ** pg
        Al[i] = (r[i] - dr / 2) ** pg

    # ---------- T（线性，一次解）----------
    rhocp = 820.0 * 2600.0
    nT = int(round(dt_out / dtT))
    T = np.full(N + 1, 28.0)
    a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1); d = np.zeros(N + 1)
    b[0] = rhocp * Vi[0] / dtT + 0.36 * A12 / dr
    c[0] = -0.36 * A12 / dr
    for i in range(1, N):
        b[i] = rhocp * Vi[i] / dtT + 0.36 * (Au[i] + Al[i]) / dr
        a[i] = -0.36 * Al[i] / dr
        c[i] = -0.36 * Au[i] / dr
    b[N] = rhocp * VN / dtT + 0.36 * Am / dr + h * R0 ** pg
    a[N] = -0.36 * Am / dr
    for n in range(1, nsteps + 1):
        for s in range(nT):
            ts = (n - 1) * dt_out + (s + 1) * dtT
            d[0] = rhocp * Vi[0] / dtT * T[0]
            for i in range(1, N):
                d[i] = rhocp * Vi[i] / dtT * T[i]
            d[N] = rhocp * VN / dtT * T[N] + h * R0 ** pg * float(Tenv(ts))
            T = thomas(a, b, c, d.copy())

    # ---------- C（非线性 Picard）----------
    nC = int(round(dt_out / dtC))
    C = np.full(N + 1, 2.55)
    for n in range(1, nsteps + 1):
        for s in range(nC):
            ts = (n - 1) * dt_out + (s + 1) * dtC
            Ca_ = float(Cenv(ts))
            Cold = C.copy(); Ci = C.copy()
            for _ in range(picard):
                Dd = 7e-9 * np.exp(-0.89 / np.maximum(Ci, 1e-12))
                Df = 2 * Dd[:-1] * Dd[1:] / np.maximum(Dd[:-1] + Dd[1:], 1e-300)
                A2 = np.zeros(N + 1); B2 = np.zeros(N + 1)
                C2 = np.zeros(N + 1); D2 = np.zeros(N + 1)
                B2[0] = Vi[0] / dtC + Df[0] * A12 / dr
                C2[0] = -Df[0] * A12 / dr
                D2[0] = Vi[0] / dtC * Cold[0]
                for i in range(1, N):
                    B2[i] = Vi[i] / dtC + (Df[i] * Au[i] + Df[i - 1] * Al[i]) / dr
                    A2[i] = -Df[i - 1] * Al[i] / dr
                    C2[i] = -Df[i] * Au[i] / dr
                    D2[i] = Vi[i] / dtC * Cold[i]
                B2[N] = VN / dtC + Df[N - 1] * Am / dr + km * R0 ** pg
                A2[N] = -Df[N - 1] * Am / dr
                D2[N] = VN / dtC * Cold[N] + km * R0 ** pg * Ca_
                Cn = np.maximum(omega * thomas(A2, B2, C2, D2) + (1 - omega) * Ci, 1e-12)
                res = np.max(np.abs(Cn - Ci))
                Ci = Cn
                if res < tol:
                    break
            C = Ci
    return T, C, r


def main():
    t0 = time.time()
    Tle, Cle = make_env('linear')
    T50 = lambda s: 50.0
    C50 = lambda s: 0.01963
    Tle2 = lambda s: float(np.interp(s, T1, TAIR))
    say('=' * 100)
    say('Q1 补充实验：几何（圆柱 p=1 / 球体 p=2）× 边界情景（附件1 时变 / 恒定 50 ℃）')
    say('=' * 100)
    say(f'1800 s 附件1 烘房温度 = {np.interp(1800,T1,TAIR):.4f} ℃ ；全时段最大 = {TAIR.max():.4f} ℃')
    say('')
    say(f'{"几何":<10s} {"边界":<26s} {"T(0)":>9} {"T(R)":>9} {"C(0)":>9} {"C(1.5)":>9} {"C(R)":>9}')
    cases = [('圆柱 p=1', '附件1 时变（本题正解口径）', 1, Tle2, Cle),
             ('球体 p=2', '附件1 时变', 2, Tle2, Cle),
             ('圆柱 p=1', '恒定 50 ℃（GS05/GT04 写法）', 1, T50, C50),
             ('球体 p=2', '恒定 50 ℃', 2, T50, C50)]
    for gname, bname, pg, Te, Ce in cases:
        T, C, r = solve(pg, Tenv=Te, Cenv=Ce)
        i15 = int(round(0.015 / (0.02 / 80)))
        say(f'{gname:<10s} {bname:<26s} {T[0]:9.4f} {T[-1]:9.4f} {C[0]:9.4f} {C[i15]:9.4f} {C[-1]:9.4f}')
    say('')
    say('机构《GT04：A题解题步骤》表1 1800 s 公布值：中心 47.3203 ℃、表面 48.5448 ℃（表2：中心 2.5464、表面 1.7900）')
    say('结论：上表四种情景（含"球体＋恒定 50 ℃"这一最激进组合）均复现不出 47.3203/48.5448；')
    say('      且 1800 s 烘房温度仅 41.5130 ℃，第三类边界 + 无内热源下药材温度不可能超过它。')
    say(f'总耗时 {time.time()-t0:.1f} s')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
