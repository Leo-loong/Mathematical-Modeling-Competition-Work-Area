# -*- coding: utf-8 -*-
"""diag: frozen+fixR+t_corr=1 T blow-up, pure numpy replica."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import q4_core as qc
N = 160
dxi = 1.0 / N
NSUB = 32
hsub = 1.0 / 32
R0 = 0.02; hc = 25.0; km = 8e-7
TSE = np.array([0.0, 1.0]); TVv = np.array([50.0, 50.0]); CVv = np.array([0.04999, 0.04999])
NC = N + 1
xih = (np.arange(N) + 0.5) * dxi
VN = dxi * (1.0 - dxi / 4.0) / 2.0
T = np.full(NC, 28.0); C = np.full(NC, 2.55)
def facek(C):
    return qc._facek4_nb(C, False)
for step in range(1, 12):
    for s in range(NSUB):
        t1s = (step - 1) + (s + 1) * hsub
        tinf = 50.0; cinf = 0.04999
        R1 = R0; R0m = R0; R1sq = R1 * R1
        rho = np.full(NC, qc._rho_nb(2.55, False))
        cp = np.full(NC, qc._cp_nb(2.55, False))
        kf = facek(C)
        Told = T.copy(); rho_o = rho.copy(); cp_o = cp.copy()
        drp = R1 * dxi
        aT = np.zeros(NC); bT = np.zeros(NC); cT = np.zeros(NC); dT = np.zeros(NC)
        for j in range(1, N):
            rl = (j - 0.5) * drp; rr2 = (j + 0.5) * drp
            rj1 = j * drp; rj0 = rj1 * (R0m / R1)
            aT[j] = -kf[j - 1] * rl / (drp * drp)
            cT[j] = -kf[j] * rr2 / (drp * drp)
            bT[j] = rho[j] * cp[j] * rj1 / hsub + (kf[j] * rr2 + kf[j - 1] * rl) / (drp * drp)
            dT[j] = rho[j] * cp[j] * T[j] * rj0 / hsub
        bT[0] = rho[0] * cp[0] / hsub + 4.0 * kf[0] / (R1sq * dxi * dxi)
        cT[0] = -4.0 * kf[0] / (R1sq * dxi * dxi)
        dT[0] = rho[0] * cp[0] * T[0] * R0m * R0m / (R1sq * hsub)
        bT[N] = VN * rho[N] * cp[N] * R1sq / hsub + kf[N - 1] * xih[N - 1] / dxi + hc * R1
        aT[N] = -kf[N - 1] * xih[N - 1] / dxi
        dT[N] = VN * rho[N] * cp[N] * T[N] * R0m * R0m / hsub + hc * R1 * tinf
        T1st = qc._thomas_nb(aT, bT, cT, dT)
        C = C  # frozen Picard below
        dCw = np.zeros(NC)
        dCw[0] = C[0] / hsub
        for j in range(1, N):
            dCw[j] = j * drp * C[j] / hsub
        dCw[N] = VN * R1sq * C[N] / hsub + km * R1 * cinf
        bse = dCw.copy(); Cit = C.copy()
        Dfv = qc._D_nb(2.55, 28.0, 1.0, False)
        for it in range(30):
            aC = np.zeros(NC); bC = np.zeros(NC); cC = np.zeros(NC)
            bC[0] = 1.0 / hsub + 4.0 * Dfv / (R1sq * dxi * dxi)
            cC[0] = -4.0 * Dfv / (R1sq * dxi * dxi)
            for j in range(1, N):
                aC[j] = -Dfv * (j - 0.5) * drp / (drp * drp)
                cC[j] = -Dfv * (j + 0.5) * drp / (drp * drp)
                bC[j] = j * drp / hsub + Dfv * ((j + 0.5) + (j - 0.5)) / drp
            bC[N] = VN * R1sq / hsub + Dfv * xih[N - 1] / dxi + km * R1
            aC[N] = -Dfv * xih[N - 1] / dxi
            Ctry = qc._thomas_nb(aC, bC, cC, bse)
            Cnew = 0.7 * Ctry + 0.3 * Cit
            rrn = np.max(np.abs(Cnew - Cit)) / max(1.0, np.max(np.abs(Cnew)))
            Cit = Cnew
            if rrn < 1e-10: break
        C = Cit
        rho = np.array([qc._rho_nb(c, False) for c in C])
        cp = np.array([qc._cp_nb(c, False) for c in C])
        kf = facek(C)
        for j in range(1, N):
            rl = (j - 0.5) * drp; rr2 = (j + 0.5) * drp
            rj1 = j * drp; rj0 = rj1 * (R0m / R1)
            aT[j] = -kf[j - 1] * rl / (drp * drp)
            cT[j] = -kf[j] * rr2 / (drp * drp)
            bT[j] = rho[j] * cp[j] * rj1 / hsub + (kf[j] * rr2 + kf[j - 1] * rl) / (drp * drp)
            dT[j] = rho_o[j] * cp_o[j] * Told[j] * rj0 / hsub
        bT[0] = rho[0] * cp[0] / hsub + 4.0 * kf[0] / (R1sq * dxi * dxi)
        cT[0] = -4.0 * kf[0] / (R1sq * dxi * dxi)
        dT[0] = rho_o[0] * cp_o[0] * Told[0] * R0m * R0m / (R1sq * hsub)
        bT[N] = VN * rho[N] * cp[N] * R1sq / hsub + kf[N - 1] * xih[N - 1] / dxi + hc * R1
        aT[N] = -kf[N - 1] * xih[N - 1] / dxi
        dT[N] = VN * rho_o[N] * cp_o[N] * Told[N] * R0m * R0m / hsub + hc * R1 * tinf
        T2st = qc._thomas_nb(aT, bT, cT, dT)
        T = T2st
        if T.max() > 50.0:
            j = int(np.argmax(T))
            print('step %d sub %d: T.max=%.3f at node %d (T[N]=%.3f T[N-1]=%.3f)' %
                  (step, s, T.max(), j, T[N], T[N - 1]))
            print('kf[N-1]=%.4f kf[N-2]=%.4f kf[0]=%.4f kfmin=%.4f kfmax=%.4f' %
                  (kf[N - 1], kf[N - 2], kf[0], kf.min(), kf.max()))
            print('C range: %.4f..%.4f ; bT[N]=%.4e aT[N]=%.4e dT[N]=%.4e' %
                  (C.min(), C.max(), bT[N], aT[N], dT[N]))
            print('first-solve T1st.max=%.3f ; Told.max=%.3f' % (T1st.max(), Told.max()))
            sys.exit(0)
print('no blow-up in 11 steps?! T.max=%.3f' % T.max())
