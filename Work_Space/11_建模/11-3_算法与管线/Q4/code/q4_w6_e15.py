# -*- coding: utf-8 -*-
"""E1 GCI at 24 h (N=80/160/320) + E5 OAT sensitivity (11 cases, parallel)."""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q4_w6_lib import load_data, solve_to_dry, N0

which = sys.argv[1]
rep = ['=' * 70]

if which == 'e1':
    import q4_core as qc
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    tC = 86400.0
    out = {}
    for N in (80, 160, 320):
        dxi = 1.0 / N
        T = np.full(N + 1, 28.0); C = np.full(N + 1, 2.55)
        t0w = time.perf_counter()
        for k in range(int(tC)):
            T, C, _ = qc.step_imex4(N, dxi, 1 / 32, 32, 0.02, 25.0, 8e-7,
                                    T, C, float(k), ts_env, Tv, Cv, ts_R, Rv,
                                    t_corr=1)
        wall = time.perf_counter() - t0w
        out[N] = (T.copy(), C.copy(), wall)
        rep.append('N=%3d wall=%6.0f s  C(0)=%.9f C(R)=%.9f T(0)=%.6f' %
                   (N, wall, C[0], C[-1], T[0]))
    r1 = abs(out[160][1][0] - out[80][1][0]); r2 = abs(out[320][1][0] - out[160][1][0])
    p = np.log(r1 / r2) / np.log(2.0) if r2 > 0 else float('inf')
    rep.append('C(0): d80-160=%.3e d160-320=%.3e obs p=%.2f' % (r1, r2, p))
    rep.append('err(N=160) ~ (C320-C160)/3 = %.3e' % (abs(out[320][1][0] - out[160][1][0]) / 3.0))
    r1s = abs(out[160][1][-1] - out[80][1][-1]); r2s = abs(out[320][1][-1] - out[160][1][-1])
    ps = np.log(r1s / r2s) / np.log(2.0) if r2s > 0 else float('inf')
    rep.append('C(R): d80-160=%.3e d160-320=%.3e obs p=%.2f' % (r1s, r2s, ps))

elif which == 'e5':
    import multiprocessing as mp

    def _case_worker(args):
        from q4_w6_lib import solve_to_dry as _s2d
        name, cfg, breaker = args
        ts_env, Tv, Cv, ts_R, Rv = load_data()
        r = _s2d(N0, 16, t_corr=1, breaker_h=breaker, hist_every=0,
                 ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv, **cfg)
        return (name, r['t_dry'], r['wall'], r['it'])

    jobs = [('base', {}), ('Tinf-1', dict(dT=-1.0)), ('Tinf+1', dict(dT=1.0)),
            ('Cinf-20', dict(dC=-0.20)), ('Cinf+20', dict(dC=0.20)),
            ('h-20', dict(hcv=20.0)), ('h+20', dict(hcv=30.0)),
            ('km-20', dict(kmv=6.4e-7)), ('km+20', dict(kmv=9.6e-7)),
            ('D0-20', dict(d_fac=0.8)), ('D0+20', dict(d_fac=1.2))]
    jobs = [(n, c, 150.0) for n, c in jobs]
    with mp.Pool(5) as pool:
        out = pool.map(_case_worker, jobs)
    base = dict((o[0], o[1]) for o in out)['base']
    tb = base / 3600.0
    wl = dict((o[0], o[2]) for o in out)
    rep.append('base t_dry (n_sub=16) = %.4f h (wall %.0f s)' % (tb, wl['base']))
    dp = dict(Tinf_scan=0)
    dp = {'Tinf-1': -0.02, 'Tinf+1': 0.02, 'Cinf-20': -0.20, 'Cinf+20': 0.20,
          'h-20': -0.20, 'h+20': 0.20, 'km-20': -0.20, 'km+20': 0.20,
          'D0-20': -0.20, 'D0+20': 0.20}
    for (name, td, w, it) in out:
        if name == 'base':
            continue
        if td is None:
            rep.append('%-8s UNREACHED within 150 h breaker' % name)
            continue
        th = td / 3600.0
        S = ((th - tb) / tb) / dp[name]
        rep.append('%-8s t_dry=%.4f h  dt=%+.4f h  S=%+.3f' % (name, th, th - tb, S))
    rep.append('note: n_sub=16 justified by S5 (16->32 rel change 3.4e-6)')

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs',
                  'q4_w6_%s.txt' % which), 'w', encoding='utf-8').write('\n'.join(rep))
print('%s DONE' % which.upper())
