# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验 E5：灵敏度分析（OAT ＋ 归一化灵敏度系数）· 并行版
======================================================
扰动因素（各 ±20%，边界项取绝对量）：
  · D0   —— 扩散系数前置因子（附录3 式(4) 的 2.4e-3）
  · h    —— 对流换热系数（N4）
  · km   —— 对流传质系数（N5）
  · T∞   —— 恒温段环境温度（±0.5 ℃，H6）
  · C∞   —— 恒温段环境浓度（±0.0005 kg/kg，H6）

输出量：T(0)、T(R)、C(0)、C(R)（终态，t = 1 h）
归一化灵敏度系数：S = (Δ输出/输出_基准) / (Δ参数/参数_基准)

【性能优化 · 2026-09-11】**仅改执行编排，不改任何数值设置与求解逻辑**
  · 12 个算例（1 基准 ＋ 11 扰动）彼此独立 ⟹ `ProcessPoolExecutor` 并行；
    扰动在**各子进程内**独立施加（不再需要"施加—还原"全局变量），
    彻底消除原串行版"忘记还原"的隐患。
  · n_sub、NSTEP、tol、maxit、omega、D_FAC 语义 **均未改动**；
    灵敏度系数公式与输出格式 **与原版逐字一致**。

运行：python q2_e5_sensitivity.py        （并行后约 1 分钟）
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np                                          # noqa: E402
from concurrent.futures import ProcessPoolExecutor          # noqa: E402
from q2_core import DEF2, run_q2                             # noqa: E402

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q2_e5_log.txt')
C0, T0 = DEF2['C0'], DEF2['T0']
T_EXT, C_EXT = 50.00, 0.04999
NSTEP = 3600        # 灵敏度只需 1 h 时程（12 次求解 × 3 h 过久；1 h 已足以排序）
N_SUB = 16          # 内部步长 1/16 s（灵敏度排序不受影响，见 W2 收敛余量 70 倍）
H_BASE, KM_BASE = DEF2['h'], DEF2['km']
C0_BASE = DEF2['C0']
NCPU = os.cpu_count() or 4
MAX_WORKERS = max(1, min(12, NCPU - 1))
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(s)


def flush_log():
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')


def _solve(tinf, cinf):
    res, _, _ = run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=NSTEP,
                       Tenv_fn=lambda _t: tinf, Cenv_fn=lambda _t: cinf,
                       n_sub=N_SUB, mode='coupled')
    T, C = res['T_end'], res['C_end']
    return np.array([T[0], T[-1], C[0], C[-1]])


def _worker(job):
    """子进程内独立施加扰动并求解（job = (tag, key, frac)）"""
    tag, key, frac = job
    import q2_core as qc
    tinf, cinf = T_EXT, C_EXT
    if key == 'h':
        qc.DEF2['h'] = H_BASE * (1.0 + frac)
    elif key == 'km':
        qc.DEF2['km'] = KM_BASE * (1.0 + frac)
    elif key == 'D_FAC':
        qc.D_FAC = 1.0 * (1.0 + frac)
    elif key == 'C0':                       # ★初始含水率（建模路线 §6 检验计划列出，v2 补入）
        qc.DEF2['C0'] = C0_BASE * (1.0 + frac)
    elif key == 'TINF':
        tinf = T_EXT + frac
    elif key == 'CINF':
        cinf = C_EXT + frac
    t0 = time.time()
    out = _solve(tinf, cinf)
    return tag, key, frac, out, time.time() - t0


def main():
    t00 = time.time()
    say('=' * 76)
    say('Q2 检验 E5：灵敏度分析（OAT ±20%，恒定边界 1 h）· 并行')
    say(f'并行：{MAX_WORKERS} 进程（CPU {NCPU} 核），BLAS/OMP 线程数=1')
    say('=' * 76)

    base = _solve(T_EXT, C_EXT)
    say(f'  基准：T0={base[0]:.4f} TR={base[1]:.4f} C0={base[2]:.6f} CR={base[3]:.6f}')
    labels = ['T(0)', 'T(R)', 'C(0)', 'C(R)']

    jobs = []
    for frac in (-0.2, +0.2):
        jobs.append((f'h {frac:+.0%}', 'h', frac))
        jobs.append((f'km {frac:+.0%}', 'km', frac))
        jobs.append((f'D0 {frac:+.0%}', 'D_FAC', frac))
    jobs.append(('T∞ +0.5℃', 'TINF', +0.5))
    jobs.append(('T∞ -0.5℃', 'TINF', -0.5))
    jobs.append(('C∞ +0.0005', 'CINF', +0.0005))
    jobs.append(('C∞ -0.0005', 'CINF', -0.0005))
    # ★v2 补入：初始含水率 C0（建模路线 §6 检验计划第 4 项明确要求）
    for frac in (-0.2, +0.2):
        jobs.append((f'C0 {frac:+.0%}', 'C0', frac))

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
        results = list(ex.map(_worker, jobs))

    rows = []
    for tag, key, frac, out, wall in results:
        if key == 'TINF':
            dp = abs(frac) / T_EXT
        elif key == 'CINF':
            dp = abs(frac) / C_EXT
        else:
            dp = abs(frac)
        S = (out - base) / np.maximum(np.abs(base), 1e-30) / dp
        rows.append((tag, out, S))
        say(f'  {tag:12s} T0={out[0]:9.4f} TR={out[1]:9.4f} '
            f'C0={out[2]:.6f} CR={out[3]:.6f}  ({wall:.0f}s)')

    say('\n【归一化灵敏度系数 S】（相对变化之比）')
    say(f'{"扰动":>12s} ' + ' '.join(f'{l:>9s}' for l in labels))
    for tag, _o, S in rows:
        say(f'{tag:>12s} ' + ' '.join(f'{v:+9.3f}' for v in S))

    mx = max(abs(v) for _t, _o, S in rows for v in S)
    say(f'\n  非零 |S| 最大 = {mx:.4f}')
    say(f'总耗时 {time.time()-t00:.0f}s（并行）')

    # ★v2：把结果写成 CSV，供《A_数值口径总表》与交付包直接取用
    csvp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q2_e5_S.csv')
    with open(csvp, 'w', encoding='utf-8') as f:
        f.write('扰动,T(0),T(R),C(0),C(R)\n')
        for tag, _o, S in rows:
            f.write(tag + ',' + ','.join('%.6f' % v for v in S) + '\n')
    say(f'  S 表已写出：{os.path.basename(csvp)}')
    flush_log()


if __name__ == '__main__':
    main()
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
