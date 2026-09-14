# -*- coding: utf-8 -*-
"""
IN-6 Sobol 方差分解（6 维含 C_fr，补齐 A3 的 Sobol 缺口）
================================================================================
[SCALE] Saltelli N=16 ⟹ 16×(6+2)=128 代理求解（N=40, n_sub=8，低保真，与 IN-3 同轨）
  ＋Pool(5) 并行；预计墙钟 12-20 min；写 logs/q4_INV6_sobol.txt + out/fig_q4_INV6_sobol.csv。
  授权：用户指令"可以装SALib，然后在后台重跑"（SALib 已装）。
参数域与 IN-3 完全一致：d_fac[0.8,1.2] h[20,30] km[6.4e-7,9.6e-7] dT[-1,1]
  dC[-0.2,0.2] c_fr[0.15,1.0]（U[0.15,1.0] 主观先验，声明）。
输出：一阶 S1、总阶 ST 及 95% 置信区间；排序与 IN-3 Morris/PRCC 对照。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-6 Sobol: Saltelli N=16 -> 128 surrogate runs (N=40/n_sub=8), Pool(5)')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import multiprocessing as mp
import numpy as np
from SALib.sample import sobol as sobol_sample
from SALib.analyze import sobol as sobol_analyze

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PROBLEM = {
    'num_vars': 6,
    'names': ['d_fac', 'h', 'km', 'Tinf', 'Cinf', 'C_fr'],
    'bounds': [[0.8, 1.2], [20.0, 30.0], [6.4e-7, 9.6e-7],
               [-1.0, 1.0], [-0.2, 0.2], [0.15, 1.0]],
}


def _worker(args):
    from q4_INV_lib import solve_to_dry, load_data
    tag, x = args
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(40, 8, t_corr=1, breaker_h=150.0,
                     d_fac=float(x[0]), hcv=float(x[1]), kmv=float(x[2]),
                     dT=float(x[3]), dC=float(x[4]), c_fr=float(x[5]),
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv)
    return (tag, r['t_dry'])


def main():
    t0w = time.perf_counter()
    X = sobol_sample.sample(PROBLEM, 16, calc_second_order=True, seed=42)
    jobs = [('s%04d' % i, list(map(float, X[i]))) for i in range(X.shape[0])]
    rep = ['=' * 70]
    rep.append('IN-6 Sobol variance decomposition (6-dim incl C_fr; surrogate N=40/n_sub=8)')
    rep.append('Saltelli N=16 -> %d runs (calc_second_order=True); prior C_fr~U[0.15,1.0] subjective' % len(jobs))

    with mp.Pool(5) as pool:
        out = dict()
        chunk = 32
        for i in range(0, len(jobs), chunk):
            part = pool.map(_worker, jobs[i:i + chunk])
            out.update(part)
    Y = np.array([out['s%04d' % i] for i in range(len(jobs))]) / 3600.0   # 单位：h
    rep.append('Y range: %.3f - %.3f h (surrogate t_dry)' % (Y.min(), Y.max()))

    Si = sobol_analyze.analyze(PROBLEM, Y, calc_second_order=True, seed=42)
    rep.append('--- Sobol indices (t_dry output; 95% CI) ---')
    rows = []
    for i, n in enumerate(PROBLEM['names']):
        s1, s1c = Si['S1'][i], Si['S1_conf'][i]
        st, stc = Si['ST'][i], Si['ST_conf'][i]
        rows.append((n, s1, s1c, st, stc))
        rep.append('%-6s S1=%+.4f ± %.4f   ST=%.4f ± %.4f   ST-S1=%.4f'
                   % (n, s1, s1c, st, stc, st - s1))
    st_sum = sum(r[3] for r in rows)
    s1_sum = sum(r[1] for r in rows)
    rep.append('sum S1=%.3f ; sum ST=%.3f（与 1 的偏差＝高阶交互与采样误差）' % (s1_sum, st_sum))
    rep.append('NOTE: 代理保真度与 IN-3 相同（N=40/n_sub=8）；C_fr 先验 U[0.15,1.0] 主观（声明）')
    rep.append('NOTE: 二阶交互（S2）已计算、未在日志展开，完整矩阵见 CSV')
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    with open(os.path.join(HERE, 'out', 'fig_q4_INV6_sobol.csv'), 'w',
              encoding='utf-8') as f:
        f.write('param,S1,S1_conf,ST,ST_conf\n')
        for (n, s1, s1c, st, stc) in rows:
            f.write('%s,%+.5f,%.5f,%.5f,%.5f\n' % (n, s1, abs(s1c), st, abs(stc)))
    # 二阶矩阵
    s2 = Si['S2']
    with open(os.path.join(HERE, 'out', 'fig_q4_INV6_sobol_S2.csv'), 'w',
              encoding='utf-8') as f:
        f.write(','.join(PROBLEM['names']) + '\n')
        for i in range(6):
            f.write(','.join('%.5f' % (s2[i][j] if s2[i][j] == s2[i][j] else 0.0)
                             for j in range(6)) + '\n')
    with open(os.path.join(HERE, 'logs', 'q4_INV6_sobol.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('INV6 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
