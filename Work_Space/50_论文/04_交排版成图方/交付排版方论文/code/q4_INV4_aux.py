# -*- coding: utf-8 -*-
"""
IN-4（A4/A7/B4/B7）辅助档：判据敏感度 ＋ fixR 效应分解 ＋ 潜热中段曲线 ＋ 取法×网格 2×2
================================================================================
[SCALE] 8 个全量事件求解（n_sub=16 为主，潜热档 n_sub=32），Pool(5)；
  预计墙钟 15-25 min；写 logs/q4_INV4_aux.txt + out/fig_q4_INV4_*.csv。
  授权：候选清单 §五 裁定。
注意：B7 调和平均对照轨为"对照实验失败臂"，其数值不得作为任何结果呈现（Q3 同款纪律）。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-4 aux: 8 full event solves, Pool(5), wall 15-25 min')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import multiprocessing as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _worker(args):
    from q4_INV_lib import solve_to_dry, load_data
    tag, cfg = args
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(cfg.get('N', 160), cfg.get('n_sub', 16), t_corr=1,
                     breaker_h=cfg.get('breaker_h', 150.0),
                     hist_every=cfg.get('hist_every', 0),
                     C_crit=cfg.get('C_crit', 0.15),
                     fixR=cfg.get('fixR', False),
                     L=cfg.get('L', 0.0),
                     if_mode=cfg.get('if_mode', 0),
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv,
                     verbose=cfg.get('verbose', False), tag=tag)
    return (tag, r)


def main():
    t0w = time.perf_counter()
    jobs = [
        ('crit018', dict(C_crit=0.18)),
        ('crit013', dict(C_crit=0.13)),
        ('fixR', dict(fixR=True)),
        ('latent_hist', dict(L=2.26e6, n_sub=32, hist_every=60, breaker_h=240.0,
                             verbose=True)),
        ('ifc_h40', dict(N=40, if_mode=1, breaker_h=150.0)),
        ('ifc_h80', dict(N=80, if_mode=1, breaker_h=150.0, verbose=True)),
        ('ifc_i40', dict(N=40, if_mode=0)),
        ('ifc_i80', dict(N=80, if_mode=0)),
    ]
    with mp.Pool(5) as pool:
        out = pool.map(_worker, jobs)
    d = dict((o[0], o[1]) for o in out)

    t_base = 182348.109        # 主力（n_sub=32）现行口径，仅作对照参照
    rep = ['=' * 70]
    rep.append('IN-4 aux batch (n_sub=16 unless noted; breaker as configured)')

    rep.append('--- A4 criterion sensitivity (vs main 0.15 -> 50.6523 h) ---')
    for tag, cc in (('crit018', 0.18), ('crit013', 0.13)):
        td = d[tag]['t_dry']
        rep.append('C_crit=%.2f : t_dry=%.4f h  dt=%+.2f%% vs C_crit=0.15'
                   % (cc, td / 3600.0, 100.0 * (td - t_base) / t_base))

    rep.append('--- A7 shrinkage vs property decomposition (appendix-4 both) ---')
    rep.append('contracted R(t)  : t_dry=%.4f h (main)' % (t_base / 3600.0))
    rep.append('fixed R=R0       : t_dry=%.4f h  (收缩加速贡献 = fixR - main = %+.3f h, %+.2f%%)'
               % (d['fixR']['t_dry'] / 3600.0,
                  (d['fixR']['t_dry'] - t_base) / 3600.0,
                  100.0 * (d['fixR']['t_dry'] - t_base) / t_base))
    rep.append('(vs Q3 fixed-R appendix-3 57.53 h：跨口径差异见口径表，不直接相减)')

    rep.append('--- B7 interface-selection x mesh 2x2 (对照失败臂，不得作结果呈现) ---')
    for tag in ('ifc_i40', 'ifc_i80', 'ifc_h40', 'ifc_h80'):
        td = d[tag]['t_dry']
        rep.append('%-8s : %s' % (tag, 'UNREACHED within breaker' if td is None
                                  else 't_dry=%.4f h' % (td / 3600.0)))

    rep.append('--- B4 latent-heat mid-horizon curve (L=2.26e6, n_sub=32, hist) ---')
    h = d['latent_hist']['hist']
    t = np.array([x[0] for x in h]); Rk = np.array([x[1] for x in h])
    TR_lat = np.array([x[5] for x in h])
    base = np.genfromtxt(os.path.join(HERE, '..', 'logs', 'q4_e7_hist.csv'),
                         delimiter=',', names=True)
    TR_base = np.interp(t, base['t_s'], base['T_R'])
    dT = TR_lat - TR_base
    rep.append('max|dT(t)| = %.4f K at t=%.2f h ; dT(6h)=%+.4f K ; dT(24h)=%+.4f K'
               % (np.max(np.abs(dT)), t[int(np.argmax(np.abs(dT)))] / 3600.0,
                  float(dT[360]), float(dT[1440])))
    rep.append('t_dry(latent)=%.4f h' % (d['latent_hist']['t_dry'] / 3600.0))
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    with open(os.path.join(HERE, 'out', 'fig_q4_INV4_latent_dT.csv'), 'w',
              encoding='utf-8') as f:
        f.write('t_h,dT_K\n')
        for i in range(len(t)):
            f.write('%.4f,%+.6f\n' % (t[i] / 3600.0, dT[i]))
    with open(os.path.join(HERE, 'out', 'fig_q4_INV4_iface_grid.csv'), 'w',
              encoding='utf-8') as f:
        f.write('iface,N,t_dry_h\n')
        for tag, iface, N in (('ifc_i40', 'integral', 40), ('ifc_i80', 'integral', 80),
                              ('ifc_h40', 'harmonic', 40), ('ifc_h80', 'harmonic', 80)):
            td = d[tag]['t_dry']
            f.write('%s,%d,%s\n' % (iface, N, 'NA' if td is None else '%.4f' % (td / 3600.0)))
    with open(os.path.join(HERE, 'logs', 'q4_INV4_aux.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('INV4 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
