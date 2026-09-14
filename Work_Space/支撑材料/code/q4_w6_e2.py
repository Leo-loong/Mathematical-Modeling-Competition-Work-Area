# -*- coding: utf-8 -*-
"""E2: frozen app4 + fixed R vs cylinder Robin series (57600 s)."""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q4_w6_lib import load_data, N0
import q4_core as qc
from scipy.special import j0, j1

rep = ['=' * 70, 'E2 frozen+fixR vs series (57600 s, N=%d)' % N0]
ts_env, Tv, Cv, ts_R, Rv = load_data()
N = N0
tE = 57600.0
TINF, CINF = 50.0, 0.04999
TSE = np.array([0.0, 1.0]); TVv = np.array([TINF, TINF]); CVv = np.array([CINF, CINF])
tsR2 = np.array([0.0, 1.0]); Rv2 = np.array([0.02, 0.02])
T = np.full(N + 1, 28.0); C = np.full(N + 1, 2.55)
dxi = 1.0 / N
t0w = time.perf_counter()
for k in range(int(tE)):
    T, C, _ = qc.step_imex4(N, dxi, 1 / 32, 32, 0.02, 25.0, 8e-7, T, C,
                            float(k), TSE, TVv, CVv, tsR2, Rv2,
                            mode='frozen', fixR=True, t_corr=1)
rep.append('frozen run wall=%.0f s' % (time.perf_counter() - t0w))
kf = 0.12 + 0.20 * 2.55 / 3.55
rho_f = 760.0 + 90.0 * 2.55
cp_f = 1850.0 + 2150.0 * 2.55 / 3.55
alpha = kf / (rho_f * cp_f)
Df = 4.2e-4 * np.exp(-0.30 / 2.55) * np.exp(-3850.0 / 301.15)
BiT = 25.0 * 0.02 / kf
BiC = 8e-7 * 0.02 / Df


def roots(Bi, nterm=60):
    rs = []
    f = lambda m: m * j1(m) - Bi * j0(m)
    x = 1e-6; fx = f(x)
    while len(rs) < nterm and x < 400:
        x2 = x + 0.01; fx2 = f(x2)
        if fx * fx2 < 0:
            a, b = x, x2
            for _ in range(80):
                m = 0.5 * (a + b)
                if f(a) * f(m) <= 0: b = m
                else: a = m
            rs.append(0.5 * (a + b))
        x, fx = x2, fx2
    return np.array(rs)


def series(Bi, Fo, xi, nterm=60):
    s = np.zeros_like(xi)
    for m in roots(Bi, nterm):
        Cn = 2.0 * Bi / (j0(m) * (m * m + Bi * Bi))
        s += Cn * j0(m * xi) * np.exp(-m * m * Fo)
    return s


FoT = alpha * tE / 0.04e-4 * 0.0001 * 10000.0
FoT = alpha * tE / 0.0004
FoC = Df * tE / 0.0004
rep.append('BiT=%.4f FoT=%.3f ; BiC=%.4f FoC=%.4f' % (BiT, FoT, BiC, FoC))
xi = np.arange(N + 1) / N
th0 = series(BiT, 1e-6, xi)
rep.append('series self-check theta(Fo->0): max|1-theta|=%.2e' % np.max(np.abs(1.0 - th0)))
T_ser = TINF + (28.0 - TINF) * series(BiT, FoT, xi)
C_ser = CINF + (2.55 - CINF) * series(BiC, FoC, xi)
dT = np.max(np.abs(T - T_ser)); dC = np.max(np.abs(C - C_ser))
rep.append('max|dT| = %.3e K (nodes)' % dT)
rep.append('max|dC| = %.3e kg/kg (nodes)' % dC)
rep.append('T(0): num=%.6f ser=%.6f ; T(R): num=%.6f ser=%.6f' %
           (T[0], T_ser[0], T[-1], T_ser[-1]))
rep.append('C(0): num=%.6f ser=%.6f ; C(R): num=%.6f ser=%.6f' %
           (C[0], C_ser[0], C[-1], C_ser[-1]))
rep.append('criterion: |dT|,|dC| ~ 1e-4 order (first-order time discretization)')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs',
                  'q4_w6_e2.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
print('E2 DONE dT=%.3e dC=%.3e' % (dT, dC))
