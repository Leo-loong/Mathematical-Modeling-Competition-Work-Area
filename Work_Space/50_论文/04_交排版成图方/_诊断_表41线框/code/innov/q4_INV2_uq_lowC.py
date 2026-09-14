# -*- coding: utf-8 -*-
"""
IN-2（A2）低 C 端 D 外推 UQ（RK-1）：C_fr 截断族 ＋ LHS 分位区间
================================================================================
[SCALE] 31 个全量事件求解（n_sub=16, N=160）：基线 1 ＋ 截断族 10（c_fr=0.15..0.60）
  ＋ LHS 20（c_fr ~ U[0.15,1.0]）；Pool(5)，预计墙钟 25-35 min；
  写 logs/q4_INV2_uq_lowC.txt + out/fig_q4_INV2_uq_{family,lhs}.csv。
  授权：候选清单 §五 裁定（先验 U[0.15,1.0] 沿用 Q3）。
注意：截断族与分位区间不得替代正式答案（Q3 采纳裁定同款）。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-2 UQ: 31 full event solves (n_sub=16), Pool(5), wall 25-35 min')
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
    tag, c_fr = args
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(160, 16, t_corr=1, breaker_h=150.0, c_fr=c_fr,
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv)
    return (tag, c_fr, r['t_dry'], r['wall'])


def main():
    t0w = time.perf_counter()
    jobs = [('base', -1.0)]
    jobs += [('fam%02d' % i, round(0.15 + 0.05 * i, 2)) for i in range(10)]
    rng = np.random.default_rng(42)
    # LHS（一维分层）：20 层，每层内均匀抽样
    strata = (np.arange(20) + rng.random(20)) / 20.0
    jobs += [('lhs%02d' % i, float(0.15 + 0.85 * s)) for i, s in enumerate(strata)]
    with mp.Pool(5) as pool:
        out = pool.map(_worker, jobs)
    d = dict((o[0], o[2]) for o in out)
    t_base = d['base']

    rep = ['=' * 70]
    rep.append('IN-2 low-C D-freeze UQ (n_sub=16, N=160, breaker 150 h)')
    rep.append('baseline (c_fr -> 0): t_dry = %.4f h' % (t_base / 3600.0))

    rep.append('--- deterministic freeze family (C_fr = 0.15..0.60) ---')
    fam = []
    for i in range(10):
        tag = 'fam%02d' % i
        c_fr = round(0.15 + 0.05 * i, 2)
        td = d[tag]
        contrib = 100.0 * (t_base - td) / t_base
        fam.append((c_fr, td, contrib))
        rep.append('C_fr=%.2f : t_dry=%.4f h  外推段贡献=%.2f%%' % (c_fr, td / 3600.0, contrib))
    rep.append('family range: 贡献 %.1f%% - %.1f%%' % (min(f[2] for f in fam),
                                                     max(f[2] for f in fam)))

    lhs = sorted(d['lhs%02d' % i] for i in range(20))
    p5, p50, p95 = lhs[0], (lhs[9] + lhs[10]) / 2, lhs[-1]
    rep.append('--- LHS 20 (C_fr ~ U[0.15,1.0], prior subjective - declared) ---')
    rep.append('t_dry quantiles: P5=%.4f h  P50=%.4f h  P95=%.4f h'
               % (p5 / 3600.0, p50 / 3600.0, p95 / 3600.0))
    rep.append('NOTE: 截断族与分位区间不得替代正式答案；先验 U[0.15,1.0] 为主观设定（声明）')
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True)
    with open(os.path.join(HERE, 'out', 'fig_q4_INV2_uq_family.csv'), 'w',
              encoding='utf-8') as f:
        f.write('C_fr,t_dry_h,contrib_pct\n')
        for (c_fr, td, c) in fam:
            f.write('%.2f,%.4f,%.2f\n' % (c_fr, td / 3600.0, c))
    with open(os.path.join(HERE, 'out', 'fig_q4_INV2_uq_lhs.csv'), 'w',
              encoding='utf-8') as f:
        f.write('sample,C_fr,t_dry_h\n')
        for i in range(20):
            tag = 'lhs%02d' % i
            f.write('%d,%.4f,%.4f\n' % (i, dict((o[0], o[1]) for o in out)[tag],
                                        d[tag] / 3600.0))
    with open(os.path.join(HERE, 'logs', 'q4_INV2_uq_lowC.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('INV2 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
