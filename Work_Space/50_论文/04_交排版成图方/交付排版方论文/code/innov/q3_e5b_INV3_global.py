# -*- coding: utf-8 -*-
"""
IN-3 | 全局灵敏度双轨：Morris 筛选 ＋ Sobol 分解（经代理加速）（创新副本）
================================================================================
动机：现有 E5 为 **OAT（局部、单参数）**，在**强非线性＋参数交互**下信息不足。
      本项增加**全局轨**，与 OAT 轨互证（"双轨融合"的检验侧应用）。

成本控制（**关键设计**）：
  · 采样引擎 = **IN-1 的自适应快轨**（Richardson 后验误差 tol=5e-5，约 1.6 s/次）
    —— 相比严格轨（248 s/次）快约 150×；
  · Sobol **不在真求解器上直接采样**，而是在**代理模型**上做 Saltelli 估计（秒级）；
  · **严格轨抽查** N_spot 个样本点（1/32 s）验证代理可用性（相对误差 ≤1%，否则降级）。

产出（带副本标记）：
  logs/q3_INV3_global.log
  out/fig_q3_INV3_morris.csv   （参数, mu_star, sigma）
  out/fig_q3_INV3_sobol.csv    （参数, S1, ST）
  out/fig_q3_INV3_samples.csv  （全部样本点与 t_end）

用法：
  python q3_e5b_INV3_global.py            # 正式（约 5–10 min）
  python q3_e5b_INV3_global.py --r 4      # 冒烟：轨迹数 4
"""
import os
import sys
import time
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
Q3DIR = os.path.dirname(HERE)
WS = _find_root(HERE)
LOGDIR = os.path.join(HERE, 'logs')
OUTDIR = os.path.join(HERE, 'out')
os.makedirs(LOGDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')

PARAMS = ['T_inf', 'C_inf', 'h', 'k_m', 'D0']
# 各参数的"**相对**半幅"（T_inf 为 ±2% 即 ±1 ℃；其余 ±20%）
HALF = np.array([0.02, 0.20, 0.20, 0.20, 0.20])
P_BASE = np.array([50.0, 0.04999, 25.0, 8e-7, 1.0])   # 参数基准值（归一化用）

BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


# ============================ 采样引擎（自适应快轨） ============================
def _adaptive_tend(ts, Tv, Cv, hc, km, d_fac, tol=5e-5,
                   dt0=1.0 / 32.0, dt_min=1.0 / 2048.0, dt_max=60.0,
                   max_hours=120.0):
    """IN-1 自适应推进（Richardson 后验误差）——快轨采样引擎。返回 t_end（h）"""
    sys.path.insert(0, Q3DIR)
    sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
    import q3_core as q3
    N, DR = 80, 2.5e-4
    NC = N + 1
    R0 = 0.02
    DT_OUT = 60.0
    orig = q3.D_FAC
    q3.D_FAC = d_fac
    try:
        T = np.full(NC, 28.0)
        C = np.full(NC, 2.55)
        t = 0.0
        dt = dt0
        t_max = max_hours * 3600.0
        while t < t_max - 1e-12:
            rem = DT_OUT - (t % DT_OUT)
            if rem <= 1e-9:
                rem = DT_OUT
            dt_try = min(dt, rem, dt_max)
            acc = False
            while not acc:
                dt_try = min(dt, rem, dt_max)
                T1, C1 = q3.step_imex_fast(N, DR, dt_try, 1, R0, hc, km, T, C,
                                           ts, Tv, Cv, t)[:2]
                T2, C2 = q3.step_imex_fast(N, DR, dt_try / 2.0, 2, R0, hc, km, T, C,
                                           ts, Tv, Cv, t)[:2]
                denC = max(1.0, float(np.max(np.abs(C2))))
                denT = max(1.0, float(np.max(np.abs(T2))))
                est = max(float(np.max(np.abs(C1 - C2))) / denC,
                          float(np.max(np.abs(T1 - T2))) / denT)
                if est <= tol or dt_try <= dt_min * 1.0000001:
                    acc = True
                    T, C = T2, C2
                    t += dt_try
                    if est > 1e-30:
                        dt = dt_try * 0.9 * np.sqrt(tol / est)
                    else:
                        dt = dt_try * 2.0
                    dt = min(max(dt, dt_try * 0.5), dt_try * 2.0)
                    dt = min(max(dt, dt_min), dt_max)
                else:
                    dt = max(dt_try * 0.5, dt_min)
            if float(np.max(C)) < 0.15:
                return t / 3600.0
        return float('nan')
    finally:
        q3.D_FAC = orig


def _worker(job):
    """子进程：给定归一化点 x∈[0,1]^5，返回 t_end（h）"""
    import os as _os
    import sys as _sys
    import numpy as _np
    import openpyxl as _xl
    idx, x = job
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _q3dir = _os.path.dirname(_here)
    _ws = _find_root(_here)
    _sys.path.insert(0, _q3dir)
    _sys.path.insert(0, _os.path.join(_ws, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
    import q2_core_c as _base
    import q3_core as _q3

    x = _np.asarray(x, dtype=float)
    dr = (2.0 * x - 1.0) * HALF                     # **相对**扰动量
    dT = P_BASE[0] * dr[0]                          # ℃
    dC, dh, dk, dD = dr[1], dr[2], dr[3], dr[4]
    P = _base.DEF2
    _wb = _xl.load_workbook(_os.path.join(_ws, '10_赛题', 'A题', '附件', '附件1.xlsx'),
                            data_only=True)
    _sh = _wb.active
    _rows = [r for r in _sh.iter_rows(values_only=True)][1:]
    _dd = [r for r in _rows if r[0] is not None]
    _t = _np.array([float(r[0]) for r in _dd])
    _T = _np.array([float(r[1]) for r in _dd])
    _Cc = _np.array([float(r[2]) for r in _dd])
    _wb.close()
    ts, Tv, Cv = _q3.env_tables_from_att1(_t, _T, _Cc,
                                          T_tail=50.00 + dT,
                                          C_tail=0.04999 * (1.0 + dC))
    te = _adaptive_tend(ts, Tv, Cv, P['h'] * (1.0 + dh), P['km'] * (1.0 + dk),
                        1.0 + dD)
    return int(idx), float(te)


# ============================ Morris 采样 ============================
def morris_sample(k, r, levels, seed=20260911):
    rng = np.random.default_rng(seed)
    delta = levels / (2.0 * (levels - 1.0))
    trajs = []
    for _ in range(r):
        x = rng.uniform(0.0, 1.0 - delta, size=k)
        perm = rng.permutation(k)
        signs = rng.choice([-1.0, 1.0], size=k)
        cur = x.copy()
        traj = [cur.copy()]
        for i in perm:
            cur = cur.copy()
            cur[i] = np.clip(cur[i] + signs[i] * delta, 0.0, 1.0)
            traj.append(cur.copy())
        trajs.append((traj, perm, signs, delta))
    return trajs


def morris_stats(trajs, ydict, k):
    """初等效应 EE → (mu_star, sigma)"""
    ee = {p: [] for p in range(k)}
    for ti, (traj, perm, signs, delta) in enumerate(trajs):
        ys = [ydict[(ti, j)] for j in range(len(traj))]
        for j, i in enumerate(perm):
            dy = ys[j + 1] - ys[j]
            dxi = traj[j + 1][i] - traj[j][i]
            if abs(dxi) > 1e-12:
                ee[i].append(dy / dxi)
    mu = np.array([np.mean(np.abs(ee[i])) if ee[i] else np.nan for i in range(k)])
    sg = np.array([np.std(ee[i]) if ee[i] else np.nan for i in range(k)])
    return mu, sg, ee


# ============================ 代理与 Sobol ============================
def poly2_features(X):
    n, k = X.shape
    cols = [np.ones(n)]
    for i in range(k):
        cols.append(X[:, i])
    for i in range(k):
        cols.append(X[:, i] ** 2)
    for i in range(k):
        for j in range(i + 1, k):
            cols.append(X[:, i] * X[:, j])
    return np.column_stack(cols)


def fit_poly2(X, y):
    A = poly2_features(X)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ coef
    r2 = 1.0 - np.sum((y - pred) ** 2) / max(1e-30, np.sum((y - y.mean()) ** 2))
    return coef, r2


def eval_poly2(coef, X):
    return poly2_features(X) @ coef


def sobol_saltelli(f, k, n_base, seed=7):
    """在代理 f 上做 Saltelli 估计 → (S1, ST)"""
    rng = np.random.default_rng(seed)
    A = rng.random((n_base, k))
    B = rng.random((n_base, k))
    yA = f(A)
    yB = f(B)
    var = np.var(np.concatenate([yA, yB]))
    S1 = np.zeros(k)
    ST = np.zeros(k)
    for i in range(k):
        AB = A.copy()
        AB[:, i] = B[:, i]
        BA = B.copy()
        BA[:, i] = A[:, i]
        yAB = f(AB)
        yBA = f(BA)
        # Jansen 估计
        ST[i] = np.mean((yA - yAB) ** 2) / (2.0 * var)
        S1[i] = (np.mean(yB * (yAB - yA))) / var
    return S1, ST


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--r', type=int, default=8, help='Morris 轨迹数')
    ap.add_argument('--levels', type=int, default=4)
    ap.add_argument('--n-base', type=int, default=2048, help='Saltelli 基样本数')
    ap.add_argument('--n-spot', type=int, default=2, help='严格轨抽查点数（1/32 s，每次约 4 min）')
    args = ap.parse_args()

    from concurrent.futures import ProcessPoolExecutor
    k = len(PARAMS)
    say('=' * 88)
    say('IN-3 | 全局灵敏度双轨：Morris 筛选 ＋ Sobol 分解（代理加速）')
    say('=' * 88)
    say('  参数：%s（半幅 %s）' % (', '.join(PARAMS), HALF.tolist()))
    say('  采样：Morris 轨迹 r=%d、levels=%d ⟹ %d 个点；引擎＝IN-1 自适应快轨（tol=5e-5）'
        % (args.r, args.levels, args.r * (k + 1)))
    say('[SCALE] 求解次数 = %d（快轨 ~1.6 s/次）＋ 严格轨抽查 %d 次（1/32 s）'
        % (args.r * (k + 1), args.n_spot))

    trajs = morris_sample(k, args.r, args.levels)
    jobs = []
    ydict = {}
    n = 0
    for ti, (traj, _, _, _) in enumerate(trajs):
        for j, x in enumerate(traj):
            jobs.append((n, x.tolist()))
            ydict[(ti, j)] = n
            n += 1
    X = np.array([j[1] for j in jobs])

    t0 = time.time()
    nw = min(8, os.cpu_count() or 4)
    ys = np.full(len(jobs), np.nan)
    with ProcessPoolExecutor(max_workers=nw) as ex:
        for idx, te in ex.map(_worker, jobs):
            ys[idx] = te
    say('  采样完成：%d 点，墙钟 %.1f s（并行度 %d）' % (len(jobs), time.time() - t0, nw))
    ok = np.isfinite(ys)
    say('  达标点 %d / %d（未达标记为 NaN）' % (int(ok.sum()), len(ys)))

    ymap = {j: ys[i] for i, j in enumerate(range(len(jobs)))}
    mu, sg, ee = morris_stats(trajs, {kk: ys[v] for kk, v in ydict.items()}, k)

    # ★ 归一化为"相对灵敏度"：S = (Δy/y) / (Δp/p)，与 OAT 的 S 同口径可对照
    delta = args.levels / (2.0 * (args.levels - 1.0))
    base_t = float(np.nanmedian(ys[ok])) if ok.any() else float('nan')
    S_norm = mu / (2.0 * delta * HALF) / base_t

    say('-' * 88)
    say('  【Morris 初等效应】（μ* = 平均绝对效应；σ 大 ⟹ 非线性/交互强）')
    say('    %-8s %-12s %-12s %-14s' % ('参数', 'μ*', 'σ', 'S_norm(=相对灵敏度)'))
    for i, p in enumerate(PARAMS):
        say('    %-8s %-12.4f %-12.4f %-14.4f' % (p, mu[i], sg[i], S_norm[i]))

    # ---- 代理 ----
    xu = X[ok]
    yu = ys[ok]
    coef, r2 = fit_poly2(xu, yu)
    say('-' * 88)
    say('  【代理模型】二次多项式（21 项）：R² = %.4f（样本 %d）' % (r2, len(xu)))
    f = lambda Z: eval_poly2(coef, np.atleast_2d(Z))       # noqa: E731
    S1, ST = sobol_saltelli(f, k, args.n_base)
    say('  【Sobol 方差分解】（在代理上、Saltelli N=%d）' % args.n_base)
    say('    %-8s %-12s %-12s %-12s' % ('参数', 'S1', 'ST', 'ST-S1(交互)'))
    for i, p in enumerate(PARAMS):
        say('    %-8s %-12.4f %-12.4f %-12.4f' % (p, S1[i], ST[i], ST[i] - S1[i]))

    # ---- 严格轨抽查 ----
    say('-' * 88)
    say('  【严格轨抽查】（1/32 s 固定步长；验证快轨/代理可用性）')
    spot_idx = np.linspace(0, len(xu) - 1, num=min(args.n_spot, len(xu))).astype(int)
    spot = []
    for si in spot_idx:
        x = xu[si]
        dr = (2.0 * x - 1.0) * HALF
        d = np.array([P_BASE[0] * dr[0], dr[1], dr[2], dr[3], dr[4]])
        import openpyxl as _xl
        wb = _xl.load_workbook(ATT1, data_only=True)
        sh = wb.active
        rows = [r for r in sh.iter_rows(values_only=True)][1:]
        dd = [r for r in rows if r[0] is not None]
        t = np.array([float(r[0]) for r in dd])
        T = np.array([float(r[1]) for r in dd])
        Cc = np.array([float(r[2]) for r in dd])
        wb.close()
        sys.path.insert(0, Q3DIR)
        sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
        import q3_core as q3
        import q2_core_c as base
        ts, Tv, Cv = q3.env_tables_from_att1(t, T, Cc, T_tail=50.00 + d[0],
                                             C_tail=0.04999 * (1.0 + d[1]))
        N, DR, R0 = 80, 2.5e-4, 0.02
        nsub = 1920
        hh = 60.0 / nsub
        orig = q3.D_FAC
        q3.D_FAC = 1.0 + d[4]
        try:
            Ts = np.full(N + 1, 28.0)
            Cs = np.full(N + 1, 2.55)
            te = float('nan')
            for m in range(1, int(120 * 3600 / 60) + 1):
                Ts, Cs, _ = q3.step_imex_fast(N, DR, hh, nsub, R0,
                                              base.DEF2['h'] * (1.0 + d[2]),
                                              base.DEF2['km'] * (1.0 + d[3]),
                                              Ts, Cs, ts, Tv, Cv, (m - 1) * 60.0)
                if float(np.max(Cs)) < 0.15:
                    te = m * 60.0 / 3600.0
                    break
        finally:
            q3.D_FAC = orig
        emb = float(f(x)[0])
        rel = abs(emb - te) / max(1e-12, abs(te))
        spot.append((x, te, emb, rel))
        say('    点 %d：严格轨 %.4f h ；代理 %.4f h ；相对差 %.3e %s'
            % (si, te, emb, rel, 'OK' if rel <= 0.01 else '⚠ 超 1%'))

    with open(os.path.join(LOGDIR, 'q3_INV3_global.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    with open(os.path.join(OUTDIR, 'fig_q3_INV3_morris.csv'), 'w', encoding='utf-8') as f:
        f.write('param,mu_star,sigma\n')
        for i, p in enumerate(PARAMS):
            f.write('%s,%.6f,%.6f\n' % (p, mu[i], sg[i]))
    with open(os.path.join(OUTDIR, 'fig_q3_INV3_sobol.csv'), 'w', encoding='utf-8') as f:
        f.write('param,S1,ST\n')
        for i, p in enumerate(PARAMS):
            f.write('%s,%.6f,%.6f\n' % (p, S1[i], ST[i]))
    with open(os.path.join(OUTDIR, 'fig_q3_INV3_samples.csv'), 'w', encoding='utf-8') as f:
        f.write('idx,' + ','.join(PARAMS) + ',t_end_h\n')
        for i in range(len(X)):
            f.write('%d,%s,%.6f\n' % (i, ','.join('%.6f' % v for v in X[i]), ys[i]))
    say('  已写出：logs/q3_INV3_global.log 与 out/fig_q3_INV3_*.csv')


if __name__ == '__main__':
    main()
