# -*- coding: utf-8 -*-
"""
IN-1（A1）t_dry 离散误差带（GCI）：空间 N=80/160/320 三档 ＋ 时间 n_sub=16/32/64 三档
================================================================================
[SCALE] 5 个全量事件求解（N=160 档含 320/64 两个 ~17 min 大档）＋GCI 后处理；
  Pool(4) 并行，预计墙钟 25-35 min；写 logs/q4_INV1_gci_tend.txt + out/fig_q4_INV1_gci.csv。
  授权：候选清单 §五 裁定（全量采纳）。复用 Q3 IN-4a 模板。
判据：空间/时间不确定度分别给出；合成口径 = 两者取大（Q3 同款，写入文档时声明）。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-1 GCI on t_dry: 5 full event solves, Pool(4), wall 25-35 min')
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
    tag, N, n_sub = args
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(N, n_sub, t_corr=1, breaker_h=240.0,
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv,
                     verbose=(N == 320 or n_sub == 64), tag=tag)
    return (tag, N, n_sub, r['t_dry'], r['wall'])


def main():
    t0w = time.perf_counter()
    jobs = [('spN80', 80, 32), ('spN160', 160, 32), ('spN320', 320, 32),
            ('tsub16', 160, 16), ('tsub64', 160, 64)]
    with mp.Pool(4) as pool:
        out = pool.map(_worker, jobs)
    res = dict((o[0], o[3]) for o in out)

    rep = ['=' * 70]
    rep.append('IN-1 GCI on t_dry (all: N/ n_sub event solves, breaker 240 h)')
    for (tag, N, ns, td, wall) in out:
        rep.append('%-7s N=%3d n_sub=%2d : t_dry=%.3f s = %.4f h (wall %.0f s)'
                   % (tag, N, ns, td, td / 3600.0, wall))

    # 空间三档
    t80, t160, t320 = res['spN80'], res['spN160'], res['spN320']
    d1, d2 = abs(t160 - t80), abs(t320 - t160)
    p_sp = np.log(d1 / d2) / np.log(2.0) if d2 > 0 else float('nan')
    err_sp = d2 / (2.0 ** p_sp - 1.0) if d2 > 0 else float('nan')
    gci_sp = 1.25 * abs(err_sp) / abs(t160)
    rep.append('SPACE: d80-160=%.3f s d160-320=%.3f s  obs p=%.2f  err(N=160)=%.3f s'
               % (d1, d2, p_sp, err_sp))
    rep.append('SPACE: GCI(N=160) = %.3e (%.4f%%) = %.5f h'
               % (gci_sp, 100 * gci_sp, 1.25 * abs(err_sp) / 3600.0))

    # 时间三档
    t16, t32, t64 = res['tsub16'], res['spN160'], res['tsub64']
    d1t, d2t = abs(t32 - t16), abs(t64 - t32)
    mono = (d1t >= d2t > 0)
    if d2t > 0 and d1t > 0:
        p_t = np.log(d1t / d2t) / np.log(2.0)
        err_t = d2t / (2.0 ** p_t - 1.0)
    else:
        p_t, err_t = float('nan'), abs(d1t) if abs(d1t) > abs(d2t) else abs(d2t)
    # 时间非单调 ⟹ 保守上界 = max|相邻差|（Q3 IN-4a 同款口径）
    bound_t_s = max(d1t, d2t) if not mono else (1.25 * abs(err_t) if err_t == err_t else d2t)
    rep.append('TIME: d16-32=%.3f s d32-64=%.3f s  obs p=%.2f  monotonic=%s'
               % (d1t, d2t, p_t, mono))
    rep.append('TIME: conservative bound = %.3f s = %.5f h (%.4f%%)'
               % (bound_t_s, bound_t_s / 3600.0, 100 * bound_t_s / t32))
    bound_s = max(1.25 * abs(err_sp) if err_sp == err_sp else 0.0, bound_t_s)
    rep.append('COMBINED (max rule): t_dry = %.4f h +/- %.5f h (%.4f%%)'
               % (t32 / 3600.0, bound_s / 3600.0, 100 * bound_s / t32))
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    with open(os.path.join(HERE, 'out', 'fig_q4_INV1_gci.csv'), 'w',
              encoding='utf-8') as f:
        f.write('kind,key,N,n_sub,t_dry_s\n')
        for (tag, N, ns, td, wall) in out:
            f.write('%s,%s,%d,%d,%.3f\n' % ('space' if tag.startswith('sp') else 'time',
                                            tag, N, ns, td))
    with open(os.path.join(HERE, 'logs', 'q4_INV1_gci_tend.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('INV1 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
