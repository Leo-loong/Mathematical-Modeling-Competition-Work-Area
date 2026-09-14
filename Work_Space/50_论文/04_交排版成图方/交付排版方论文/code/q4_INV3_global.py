# -*- coding: utf-8 -*-
"""
IN-3（A3）全局灵敏度（Morris 筛选 ＋ LHS-PRCC；6 维含 C_fr）· v2
================================================================================
[SCALE] Morris 10 轨 ×7 点 = 70 代理求解（N=40, n_sub=8，低保真）＋ LHS 48 点代理
  ＋ 严格轨抽查 2 点（N=160, n_sub=16）；Pool(5)，预计墙钟 15-25 min；
  写 logs/q4_INV3_global.txt + out/fig_q4_INV3_{morris,lhs,samples}.csv。
  授权：候选清单 §五 裁定（6 维含 C_fr；保真度自定）。
v2 修复：①LHS 每列独立分层置换（v1 各列同序导致 Spearman 退化 -1，结果作废）；
  ②Morris 改标准 OAT 轨迹（每坐标恰扰动一次，越界反弹）；③去除 c_fr 错误守卫。
参数域：d_fac[0.8,1.2] h[20,30] km[6.4e-7,9.6e-7] dT[-1,1] dC[-0.2,0.2]
        c_fr[0.15,1.0]（U[0.15,1.0] 主观先验，声明）。
诚实边界：Sobol 完整方差分解未做（需 SALib，登记为可补做项）；Morris/PRCC 为手写
  基础统计（有限差分＋秩相关，scipy.stats.spearmanr），非关键数值库替代。
"""
import sys, os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

print('[SCALE] IN-3 global sensitivity v2: Morris 70 + LHS 48 (surrogate) + 2 strict, Pool(5)')
if '--go' not in sys.argv:
    print('[SCALE] --go not given -> exit (gate closed)')
    sys.exit(0)

import time
import multiprocessing as mp
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PNAMES = ['d_fac', 'h', 'km', 'Tinf', 'Cinf', 'C_fr']
LO = np.array([0.8, 20.0, 6.4e-7, -1.0, -0.2, 0.15])
HI = np.array([1.2, 30.0, 9.6e-7, 1.0, 0.2, 1.0])


def phys(x):
    return LO + np.asarray(x, dtype=float) * (HI - LO)


def _surrogate_worker(args):
    from q4_INV_lib import solve_to_dry, load_data
    tag, x = args
    p = phys(x)
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(40, 8, t_corr=1, breaker_h=150.0,
                     d_fac=float(p[0]), hcv=float(p[1]), kmv=float(p[2]),
                     dT=float(p[3]), dC=float(p[4]), c_fr=float(p[5]),
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv)
    return (tag, r['t_dry'])


def _strict_worker(args):
    from q4_INV_lib import solve_to_dry, load_data
    tag, x = args
    p = phys(x)
    ts_env, Tv, Cv, ts_R, Rv = load_data()
    r = solve_to_dry(160, 16, t_corr=1, breaker_h=150.0,
                     d_fac=float(p[0]), hcv=float(p[1]), kmv=float(p[2]),
                     dT=float(p[3]), dC=float(p[4]), c_fr=float(p[5]),
                     ts_env=ts_env, Tv=Tv, Cv=Cv, ts_R=ts_R, Rv=Rv)
    return (tag, r['t_dry'])


def oat_trajectories(k=6, r=10, delta=2.0 / 3.0, seed=42):
    """标准 OAT 轨迹：每条轨迹 k+1 个点，每坐标恰扰动一次（越界反弹）。"""
    rng = np.random.default_rng(seed)
    trajs = []
    for _ in range(r):
        x = rng.random(k)
        path = [x.copy()]
        for m in rng.permutation(k):
            x2 = x.copy()
            d = delta if rng.random() < 0.5 else -delta
            if not (0.0 <= x2[m] + d <= 1.0):
                d = -d
            x2[m] = x2[m] + d
            path.append(x2.copy())
            x = x2
        trajs.append(np.array(path))
    return trajs


def main():
    t0w = time.perf_counter()
    rng = np.random.default_rng(7)

    trajs = oat_trajectories()
    rep = ['=' * 70]
    rep.append('IN-3 global sensitivity v2 (6-dim, surrogate N=40/n_sub=8; strict spot N=160/16)')
    rep.append('params: ' + ', '.join('%s[%.3g,%.3g]' % (n, l, h)
                                      for n, l, h in zip(PNAMES, LO, HI)))
    rep.append('Morris/OAT: %d trajectories x %d points (delta=2/3, bounce at bounds)'
               % (len(trajs), 7))

    # 任务表（按 x 元组去重）
    jobs, x2tag = [], {}
    for ti, B in enumerate(trajs):
        for pi in range(B.shape[0]):
            xt = tuple(np.round(B[pi], 6))
            if xt not in x2tag:
                x2tag[xt] = 'm%d_%d' % (ti, pi)
                jobs.append((x2tag[xt], list(xt)))

    with mp.Pool(5) as pool:
        out = dict()
        chunk = 30
        for i in range(0, len(jobs), chunk):
            part = pool.map(_surrogate_worker, jobs[i:i + chunk])
            out.update(part)
        # 基点（x=0 注意 c_fr=0.15 即先验下界）
        t_base_s = pool.map(_surrogate_worker, [('m_base', [0.0] * 6)])[0][1]
    # 以 x 元组重建取值表
    val_by_x = {}
    for xt, tag in x2tag.items():
        val_by_x[xt] = out[tag]
    rep.append('unique surrogate runs: %d ; surrogate base t_dry = %.4f h'
               % (len(jobs), t_base_s / 3600.0))

    # 基本效应（EE）
    EE = {n: [] for n in PNAMES}
    for B in trajs:
        for pi in range(1, B.shape[0]):
            xp, xc = B[pi - 1], B[pi]
            j = int(np.argmax(np.abs(xc - xp) > 1e-12))
            dx = xc[j] - xp[j]
            k1 = tuple(np.round(xp, 6))
            k2 = tuple(np.round(xc, 6))
            if k1 in val_by_x and k2 in val_by_x and abs(dx) > 1e-12:
                EE[PNAMES[j]].append((val_by_x[k2] - val_by_x[k1]) / t_base_s / dx)
    rep.append('--- Morris elementary effects (normalized (dt/t)/dx) ---')
    mus, mus_star, sig = {}, {}, {}
    for n in PNAMES:
        e = np.array(EE[n], dtype=float)
        mus[n] = float(e.mean()) if e.size else float('nan')
        mus_star[n] = float(np.abs(e).mean()) if e.size else float('nan')
        sig[n] = float(e.std(ddof=1)) if e.size > 1 else float('nan')
    finite = [v for v in mus_star.values() if v == v]
    smax = max(finite) if finite else float('nan')
    for n in PNAMES:
        rep.append('%-6s mu*=%.4f (norm %.3f)  mu=%+.4f  sigma=%.4f  (r=%d)'
                   % (n, mus_star[n], mus_star[n] / smax, mus[n], sig[n], len(EE[n])))

    # LHS 48（每列独立分层置换）＋ Spearman
    u = rng.random((48, 6))
    perms = np.column_stack([rng.permutation(48) for _ in range(6)])
    strata = (perms + u) / 48.0
    lhs_x = [list(map(float, strata[i])) for i in range(48)]
    lhs_jobs = [('lhs%02d' % i, lhs_x[i]) for i in range(48)]
    with mp.Pool(5) as pool:
        lhs_out = dict(pool.map(_surrogate_worker, lhs_jobs))
    X = np.array(lhs_x)
    T = np.array([lhs_out['lhs%02d' % i] for i in range(48)]) / t_base_s - 1.0
    rep.append('--- LHS 48 + Spearman rank correlation (surrogate) ---')
    for j, n in enumerate(PNAMES):
        rho, pv = stats.spearmanr(X[:, j], T)
        rep.append('%-6s rho=%+.3f  p=%.3g' % (n, rho, pv))

    # 严格轨抽查 2 点
    picks = [lhs_x[10], lhs_x[36]]
    with mp.Pool(2) as pool:
        strict = pool.map(_strict_worker, [('s0', picks[0]), ('s1', picks[1])])
        sur = dict(pool.map(_surrogate_worker, [('c0', picks[0]), ('c1', picks[1])]))
    for (tag, ts), ck in zip(strict, ('c0', 'c1')):
        surrogate = sur[ck]
        rel = abs(ts - surrogate) / ts
        rep.append('strict spot %s: strict=%.4f h vs surrogate=%.4f h  rel=%.2e'
                   % (tag, ts / 3600.0, surrogate / 3600.0, rel))
    rep.append('NOTE: 代理保真度 N=40/n_sub=8 仅用于筛选排序；严格轨抽查给出保真度界限')
    rep.append('NOTE: Sobol 方差分解未做（需 SALib），登记为可补做项')
    rep.append('total wall=%.0f s' % (time.perf_counter() - t0w))

    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    with open(os.path.join(HERE, 'out', 'fig_q4_INV3_morris.csv'), 'w',
              encoding='utf-8') as f:
        f.write('param,mu_star,mu,sigma\n')
        for n in PNAMES:
            f.write('%s,%.5f,%+.5f,%.5f\n' % (n, mus_star[n], mus[n], sig[n]))
    with open(os.path.join(HERE, 'out', 'fig_q4_INV3_lhs.csv'), 'w',
              encoding='utf-8') as f:
        f.write(','.join(PNAMES) + ',t_rel\n')
        for i in range(48):
            f.write(','.join('%.4f' % v for v in lhs_x[i]) + ',%.5f\n' % T[i])
    with open(os.path.join(HERE, 'logs', 'q4_INV3_global.txt'), 'w',
              encoding='utf-8') as f:
        f.write('\n'.join(rep))
    print('INV3 DONE')


if __name__ == '__main__':
    mp.freeze_support()
    main()
