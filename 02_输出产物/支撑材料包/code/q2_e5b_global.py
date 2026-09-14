# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验 E5-b：全局灵敏度（Morris 筛选 ＋ Sobol 定量）· O7
======================================================
【为什么需要】E5 用的是 **OAT（单因素局部扰动）**——它只能反映"基准点附近"的敏感性，
              无法刻画**参数同时变化**时的**交互作用**与**非线性**。

【方法】
  · **Morris 筛选法**：沿每个参数的"轨迹"做一次基本增量，得到
      μ*（平均绝对影响，稳健版）与 σ（影响的标准差，反映非线性/交互）。
      ⟹ 用于**快速筛选**：σ/μ* 大者说明存在交互或强非线性。
  · **Sobol 方差分解**：用 Saltelli 采样估计
      一阶指数 S_i（该参数单独贡献的方差占比）与
      总效应指数 S_Ti（含与其他参数交互的贡献）。
      ⟹ 用于**定量排序**：S_Ti − S_i 即该参数的**交互作用占比**。

【设置】为控制计算量，用时程 1 h（与 E5 同口径）＋ 内部步长 1/16 s；
        参数 5 个（h、k_m、D_0、T∞、C∞），取值范围为基准的 ±20%（边界项取绝对量）。
        所有算例**多进程并行**。

【说明】本项属"加分项"，结论用于论文"灵敏度分析"节的补充（**不改变任何主力结果**）。

运行：python q2_e5b_global.py
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                              # noqa: E402
from concurrent.futures import ProcessPoolExecutor              # noqa: E402
from scipy.stats import qmc                                     # noqa: E402
from q2_core import DEF2, run_q2                                # noqa: E402

LOG = os.path.join(HERE, 'q2_e5b_log.txt')
BUF = []

NSTEP, N_SUB = 3600, 16          # 1 h 时程、内部步长 1/16 s（与 E5 同口径）
T_EXT, C_EXT = 50.00, 0.04999
PNAMES = ['h', 'km', 'D0', 'Tinf', 'Cinf']
NBASE = [DEF2['h'], DEF2['km'], 1.0, T_EXT, C_EXT]
# 扰动半幅（相对量；边界项按其绝对量级折算）
PHALF = [0.20, 0.20, 0.20, 0.5 / T_EXT, 0.0005 / C_EXT]
H_BASE, KM_BASE = DEF2['h'], DEF2['km']
C0_BASE = DEF2['C0']
NCPU = os.cpu_count() or 4
WORKERS = max(1, min(16, NCPU - 1))


_FH = None


def say(s=''):
    """实时输出并**即时落盘**（避免长时间运行被中断时丢日志）"""
    global _FH
    print(s, flush=True)
    BUF.append(s)
    if _FH is None:
        _FH = open(LOG, 'w', encoding='utf-8')
    _FH.write(s + '\n')
    _FH.flush()


def flush_log():
    if _FH is not None:
        _FH.flush()


def _solve_one(x):
    """x = [h, km, D0, Tinf, Cinf]（物理值）→ 输出 [T(0), T(R), C(0), C(R)]"""
    import q2_core as qc
    qc.DEF2['h'] = float(x[0])
    qc.DEF2['km'] = float(x[1])
    qc.D_FAC = float(x[2])
    tinf, cinf = float(x[3]), float(x[4])
    res, _, _ = qc.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=NSTEP, n_sub=N_SUB,
                          Tenv_fn=lambda _t: tinf, Cenv_fn=lambda _t: cinf,
                          mode='coupled')
    T, C = res['T_end'], res['C_end']
    return [float(T[0]), float(T[-1]), float(C[0]), float(C[-1])]


def _worker(chunk):
    return [_solve_one(x) for x in chunk]


def run_batch(X, tag=''):
    """并行求解样本矩阵 X（每行一个样本）；**逐块提交并打印进度**（避免长时间无输出）"""
    n = len(X)
    k = max(1, min(WORKERS, n))
    chunks = [X[i::k] for i in range(k)]
    out = [None] * n
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(max_workers=k) as ex:
        futs = {ex.submit(_worker, ch): i for i, ch in enumerate(chunks)}
        for fut in __import__('concurrent.futures').futures.as_completed(futs):
            i = futs[fut]
            part = fut.result()
            for j, v in zip(range(i, n, k), part):
                out[j] = v
            done += len(part)
            el = time.time() - t0
            say(f'    [{tag}] {done}/{n} 已用 {el:.0f}s  预计剩余 '
                f'{el/max(1,done)*(n-done):.0f}s')
    return np.array(out)


def to_phys(u):
    """单位立方体 [0,1]^5 → 物理值"""
    u = np.atleast_2d(u)
    x = np.empty_like(u)
    for j in range(5):
        x[:, j] = NBASE[j] + (2.0 * u[:, j] - 1.0) * PHALF[j] * NBASE[j]
    return x


def morris(r=12, levels=4):
    """Morris 轨迹法（r 条轨迹，含 d+1 个点）"""
    d = 5
    rng = np.random.default_rng(20260911)
    grid = np.linspace(0, 1, levels)
    delta = levels / (2.0 * (levels - 1))
    pts = []
    for _ in range(r):
        base_idx = rng.integers(0, levels // 2, size=d)
        u0 = grid[base_idx].copy()
        order = rng.permutation(d)
        traj = [u0.copy()]
        cur = u0.copy()
        for j in order:
            cur = cur.copy()
            cur[j] = min(cur[j] + delta, 1.0)
            traj.append(cur)
        pts.extend(traj)
    X = to_phys(np.array(pts))
    Y = run_batch(X, tag='MORRIS')
    # 提取每条轨迹的增量效应
    ee = np.zeros((r, d, 4))
    for t in range(r):
        for k in range(d):
            i0 = t * (d + 1) + k
            i1 = i0 + 1
            denom = (X[i1] - X[i0]) / (np.array(NBASE) * np.array(PHALF))
            for m in range(4):
                ee[t, k, m] = (Y[i1, m] - Y[i0, m]) / max(1e-30, np.max(np.abs(denom)))
    base = np.abs(np.array(_solve_one(NBASE)))
    return ee, base


def sobol(N=64):
    """Saltelli 采样：一阶与总效应指数"""
    d = 5
    sampler = qmc.Sobol(d=d, scramble=True, seed=20260911)
    AB = sampler.random(2 * N)
    A, B = AB[:N], AB[N:]
    X_list = [to_phys(A), to_phys(B)]
    for i in range(d):
        ABi = A.copy()
        ABi[:, i] = B[:, i]
        X_list.append(to_phys(ABi))
    X = np.vstack(X_list)
    Y = run_batch(X, tag='SOBOL')
    YA, YB = Y[:N], Y[N:2 * N]
    YAB = [Y[2 * N + i * N: 2 * N + (i + 1) * N] for i in range(d)]
    out = {}
    for m, nm in enumerate(['T(0)', 'T(R)', 'C(0)', 'C(R)']):
        fA, fB = YA[:, m], YB[:, m]
        var = np.var(np.concatenate([fA, fB]))
        S, ST = [], []
        for i in range(d):
            fAB = YAB[i][:, m]
            S.append(np.mean(fB * (fAB - fA)) / max(1e-30, var))
            ST.append(0.5 * np.mean((fA - fAB) ** 2) / max(1e-30, var))
        out[nm] = (np.array(S), np.array(ST))
    return out


def main():
    t00 = time.time()
    say('=' * 78)
    say('Q2 检验 E5-b：全局灵敏度（Morris 筛选 ＋ Sobol 定量）')
    say('=' * 78)
    say(f'  参数：{"／".join(PNAMES)}   范围：基准 ±20%（边界项按绝对量折算）')
    say(f'  时程 1 h，内部步长 1/{N_SUB} s；并行 {WORKERS} 进程')

    say('\n[MORRIS] 筛选（μ* 平均绝对影响 ／ σ 影响离散度）')
    ee, base = morris(r=8, levels=4)
    say(f'   基准输出：T(0)={base[0]:.4f}  T(R)={base[1]:.4f}  '
        f'C(0)={base[2]:.6f}  C(R)={base[3]:.6f}')
    say(f'\n   {"参数":<6} {"μ*(C(R))":>12} {"σ(C(R))":>12} {"σ/μ*":>8}   判定')
    for j in range(5):
        mu = float(np.mean(np.abs(ee[:, j, 3])))
        sd = float(np.std(ee[:, j, 3]))
        ratio = sd / max(1e-30, mu)
        judge = '强非线性/交互' if ratio > 0.5 else ('中等' if ratio > 0.2 else '近似线性')
        say(f'   {PNAMES[j]:<6} {mu:12.3e} {sd:12.3e} {ratio:8.3f}   {judge}')

    say('\n[SOBOL] 方差分解（N=32 Saltelli 采样）')
    flush_log()
    so = sobol(N=32)
    for nm in ['T(0)', 'T(R)', 'C(0)', 'C(R)']:
        S, ST = so[nm]
        say(f'\n   ── 输出 {nm}')
        say(f'   {"参数":<6} {"S_i(一阶)":>12} {"S_Ti(总效应)":>13} {"交互占比":>10}')
        for j in range(5):
            inter = ST[j] - S[j]
            say(f'   {PNAMES[j]:<6} {S[j]:12.4f} {ST[j]:13.4f} {inter:10.4f}')
        idx = int(np.argmax(ST))
        say(f'   ⟹ 总效应最大：**{PNAMES[idx]}**（S_Ti={ST[idx]:.4f}）')

    say('\n【结论（论文表述建议）】')
    say('   ① Morris 的 σ/μ* 用于识别**非线性／交互**：比值大者说明该参数的影响随取值变化剧烈，')
    say('      或与其他参数存在交互；')
    say('   ② Sobol 的 S_Ti − S_i 即**交互作用占比**：若接近 0，则 OAT 结论已足够，')
    say('      否则须在论文中说明"单因素分析会低估该参数的作用"。')
    say('   ③ 本项与 E5（OAT）**互补**，不替代；不改变任何主力结果。')

    say(f'\n总耗时 {time.time()-t00:.1f}s')
    flush_log()


if __name__ == '__main__':
    main()
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
