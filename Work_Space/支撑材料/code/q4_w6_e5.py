# -*- coding: utf-8 -*-
"""
E5 灵敏度（OAT）：11 算例（base ＋ 5 参数 × ±20%／±1 ℃），输出 t_dry 灵敏度系数 S
================================================================================
[SCALE] 11 个全量求解（N=160, n_sub=16, t_corr=1, 熔断 150 h），mp.Pool(5) 并行；
  预计墙钟 ≈13-18 min（单例 n_sub=16 约 250-320 s，3 波）；写 logs/q4_w6_e5.txt。
  授权：用户指令"完成第四问未完成的建模"（W6 检验批次）。
用法：python q4_w6_e5.py          -> 只打印 [SCALE] 并退出
      python q4_w6_e5.py --go     -> 实际执行
说明：n_sub=16 由预试验 S5 背书（16→32 相对变化 3.4e-6 ≪ 5e-5）；
  ★本脚本为 q4_w6_e15.py 的 E5 分支修正版——原脚本缺 __main__ 守卫，
  Windows spawn 下 Pool 必崩（即 E5 此前"脚本在而日志无"的根因）。
================================================================================
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] E5 OAT: 11 full solves (N=160, n_sub=16, breaker 150 h), Pool(5)')
print('[SCALE] wall est 13-18 min; output: logs/q4_w6_e5.txt')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import multiprocessing as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _case_worker(args):
    from q4_w6_lib import solve_to_dry, load_data
    name, cfg, breaker = args
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(160, 16, t_corr=1, breaker_h=breaker, hist_every=0,
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv, **cfg)
    return (name, r['t_dry'], r['wall'], r['it'])


def main():
    t0w = time.perf_counter()
    rep = ['=' * 70]
    rep.append('E5 OAT sensitivity (t_dry output; 11 cases, Pool(5), n_sub=16)')
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
    dp = {'Tinf-1': -0.02, 'Tinf+1': 0.02, 'Cinf-20': -0.20, 'Cinf+20': 0.20,
          'h-20': -0.20, 'h+20': 0.20, 'km-20': -0.20, 'km+20': 0.20,
          'D0-20': -0.20, 'D0+20': 0.20}
    S = {}
    for (name, td, w, it) in out:
        if name == 'base':
            continue
        if td is None:
            rep.append('%-8s UNREACHED within 150 h breaker' % name)
            continue
        th = td / 3600.0
        Sv = ((th - tb) / tb) / dp[name]
        S[name] = Sv
        rep.append('%-8s t_dry=%.4f h  dt=%+.4f h  S=%+.3f' % (name, th, th - tb, Sv))
    if len(S) >= 2:
        smax = max(abs(v) for v in S.values())
        rep.append('S_norm (|S|/max|S|):')
        for k in sorted(S, key=lambda k: -abs(S[k])):
            rep.append('  %-8s %.3f' % (k, abs(S[k]) / smax))
    rep.append('note: n_sub=16 justified by S5 (16->32 rel change 3.4e-6)')
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))
    with open(os.path.join(HERE, '..', 'logs', 'q4_w6_e5.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('E5 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
