# -*- coding: utf-8 -*-
"""
A 题 Q2 · W2 预试验（**前台版 · 并行**）
======================================================
格式：IMEX 交替推进（物性每内部子步更新，**不损失精度**）
任务：
  A. 空间收敛：Δr = 1.0 / 0.5 / 0.25 mm（固定内部步长 1/32 s）
  B. 时间收敛：内部步长 = 1/2 … 1/64 s（固定 Δr = 0.25 mm）
判定：关键量相对变化 < 5e-5（L3-07，保证第 4 位小数有效）

【性能优化 · 2026-09-11】**仅改执行编排，不改任何数值设置与求解逻辑**
  · 9 个算例彼此独立 ⟹ `ProcessPoolExecutor` 并行（max_workers = min(9, 物理核数-1)）
  · 日志 IO：`say()` 只入内存缓冲，收尾一次性落盘（原为每行 open/append/close）
  · 环境变量：BLAS/OMP 线程数置 1（小规模三对角求解无需多线程，避免线程切换开销）
  · ⚠ `one()`／`run_q2()` 内部逻辑、n_sub、T_END、tol、maxit、omega **均未改动**

运行：在本目录下 `python q2_w2_foreground.py`
输出：控制台进度 ＋ 同目录 `w2_foreground_log.txt`（供后续分析）
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# ---- 线程环境变量必须早于 numpy 导入（子进程由 spawn 重建模块，同样生效）----
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np                                   # noqa: E402
from concurrent.futures import ProcessPoolExecutor   # noqa: E402
from q2_core import run_q2                           # noqa: E402

T_END = 1800.0
TINF, CINF = 50.00, 0.04999
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w2_foreground_log.txt')
BUF = []
NCPU = os.cpu_count() or 4
MAX_WORKERS = max(1, min(9, NCPU - 1))


def say(s=''):
    """仅追加到内存缓冲；由 `flush_log()` 一次性落盘（优化前为每行写盘一次）"""
    print(s, flush=True)
    BUF.append(s)


def flush_log():
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')


def bar(i, n, t0, width=28):
    f = int(width * i / n)
    el = time.time() - t0
    eta = el / i * (n - i) if i else 0.0
    return ('[' + '#' * f + '.' * (width - f) + f'] {i:>2}/{n}  '
            f'已用 {el:5.1f}s  预计剩余 {eta:5.1f}s')


def one(N, dr, n_sub, tag, kind):
    """单个算例（**与优化前逐行等价**，仅增加 kind 字段用于分组与并行）"""
    t0 = time.time()
    res, _, _ = run_q2(N=N, dr=dr, dt_out=1.0, nsteps=int(T_END),
                       Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                       n_sub=n_sub, mode='coupled')
    T, C = res['T_end'], res['C_end']
    return dict(kind=kind, tag=tag, N=N, dr=dr, n_sub=n_sub, h=1.0 / n_sub,
                Tc=float(T[0]), Ts=float(T[-1]),
                Cc=float(C[0]), Cs=float(C[-1]), Cmax=float(np.max(C)),
                inner_avg=res['stats']['inner_tot'] / max(1, res['stats']['nsub']),
                wall=time.time() - t0)


def _worker(task):
    """模块级 worker（可 pickle）：参数只有标量，函数在子进程内构造"""
    kind, N, dr, ns, tag = task
    return one(N, dr, ns, tag, kind)


def main():
    say('=' * 78)
    say(f'Q2 · W2 预试验（IMEX 格式）  时程 {T_END:.0f}s  恒定边界 '
        f'({TINF} ℃, {CINF} kg/kg)')
    say(f'并行：{MAX_WORKERS} 进程（CPU {NCPU} 核），BLAS/OMP 线程数=1')
    say('=' * 78)

    tasks = []
    for dr, N in ((1.0e-3, 20), (5.0e-4, 40), (2.5e-4, 80)):
        tasks.append(('space', N, dr, 32, f'空间 dr={dr*1e3:.2f}mm'))
    for ns in (2, 4, 8, 16, 32, 64):
        tasks.append(('time', 80, 2.5e-4, ns, f'时间 h=1/{ns}s'))

    rows = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
        for i, r in enumerate(ex.map(_worker, tasks), 1):
            say(bar(i, len(tasks), t0))
            say(f"  ▶ {r['tag']}")
            say(f"    {r['tag']:<22s} T0={r['Tc']:10.6f} TR={r['Ts']:10.6f} "
                f"C0={r['Cc']:.8f} CR={r['Cs']:.8f}  "
                f"内层×{r['inner_avg']:.1f}/步  {r['wall']:5.1f}s")
            rows.append((r['kind'], r))
    say(bar(len(tasks), len(tasks), t0))
    say(f'\n【总墙钟】{time.time()-t0:.1f}s（9 个算例，串行耗时约 '
        f'{sum(r["wall"] for _, r in rows):.0f}s）')

    # ---------- 判定 ----------
    def judge(kind, key, name):
        rs = [r for k, r in rows if k == kind]
        ref = rs[-1][key]
        say(f"\n【{name}】基准＝最后一组（{rs[-1]['tag']}），{key}={ref:.8f}")
        ok = True
        for r in rs:
            e = abs(r[key] - ref) / max(1e-30, abs(ref))
            flag = '✅' if e < 5e-5 else '⚠'
            if e >= 5e-5:
                ok = False
            say(f"    {r['tag']:<22s} {key}={r[key]:.8f}  相对变化={e:.3e}  {flag}")
        say(f"    ⟹ {'通过（<5e-5）' if ok else '未全通过，需更细步长'}")
        return rs

    say('\n' + '=' * 78)
    judge('space', 'Ts', '空间收敛（Δr）')
    judge('time', 'Ts', '时间收敛 · 温度（内部步长）')
    judge('time', 'Cs', '时间收敛 · 含水率（内部步长）')
    say('=' * 78)
    say(f'\n完成。日志：{LOG}')
    flush_log()

    try:
        input('\n按 Enter 键退出...')
    except Exception:
        pass


if __name__ == '__main__':
    main()
