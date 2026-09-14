# -*- coding: utf-8 -*-
"""E7 conservation + E8 latent (full solves with history)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q4_w6_lib import load_data, solve_to_dry, N0

which = sys.argv[1]
ts_env, Tv, Cv, ts_R, Rv = load_data()
rep = ['=' * 70]

if which == 'e7':
    rep.append('E7 conservation (full solve, hist every 60 s)')
    res = solve_to_dry(N0, 32, t_corr=1, breaker_h=240.0, hist_every=60,
                       ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv,
                       verbose=True, tag='e7')
    h = res['hist']
    t = np.array([x[0] for x in h]); Rk = np.array([x[1] for x in h])
    W = np.array([x[2] for x in h]); U = np.array([x[3] for x in h])
    CR = np.array([x[4] for x in h]); TR = np.array([x[5] for x in h])
    flux = 2.0 * Rk * 8e-7 * (CR - 0.04999)
    Fint = float(np.trapezoid(flux, t)); dW = W[-1] - W[0]
    res_m = abs(dW + Fint) / abs(dW)
    eint = float(np.trapezoid(25.0 * Rk * (50.0 - TR), t)); dU = U[-1] - U[0]
    res_e = abs(dU - eint) / abs(dU)
    rep.append('mass  : dW=%.6e  flux_out=%.6e  rel residual=%.3e' % (dW, Fint, res_m))
    rep.append('energy: dU=%.6e  net_in=%.6e  rel residual=%.3e' % (dU, eint, res_e))
    rep.append('criterion: mass ~1e-3 order (Q2/Q3 same); energy residual includes')
    rep.append('60 s trapezoid truncation + endpoint sampling; attribute honestly')
    rep.append('t_dry=%.3f s (%.4f h) wall=%.0f s' % (res['t_dry'], res['t_dry'] / 3600.0, res['wall']))
elif which == 'e8':
    rep.append('E8 latent heat (L=2.26e6 J/kg) vs baseline')
    rb = solve_to_dry(N0, 32, t_corr=1, breaker_h=240.0, ts_env=ts_env, Tv=Tv,
                      Cv=Cv, ts_R=ts_R, Rv=Rv, verbose=True, tag='e8base')
    rl = solve_to_dry(N0, 32, t_corr=1, breaker_h=240.0, L=2.26e6, ts_env=ts_env,
                      Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv, verbose=True, tag='e8lat')
    dT = np.max(np.abs(rl['Tend'] - rb['Tend'])); dC = np.max(np.abs(rl['Cend'] - rb['Cend']))
    dt_h = (rl['t_dry'] - rb['t_dry']) / 3600.0
    rep.append('baseline: t_dry=%.4f h (wall %.0f s)' % (rb['t_dry'] / 3600.0, rb['wall']))
    rep.append('latent  : t_dry=%.4f h (wall %.0f s)' % (rl['t_dry'] / 3600.0, rl['wall']))
    rep.append('end-field: max|dT|=%.3e K ; max|dC|=%.3e' % (dT, dC))
    rep.append('t_dry shift = %+.4f h (%+.3f%%)' % (dt_h, 100.0 * dt_h / (rb['t_dry'] / 3600.0)))

_LOGD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(_LOGD, exist_ok=True)
open(os.path.join(_LOGD, 'q4_w6_%s.txt' % which), 'w', encoding='utf-8').write('\n'.join(rep))
print('%s DONE' % which.upper())
