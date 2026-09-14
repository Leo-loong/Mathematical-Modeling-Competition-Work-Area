# -*- coding: utf-8 -*-
"""
Q2 · 优化前后严格 A/B 基准（回答"CPU 占用率为何不变"）
=====================================================
本脚本用**同一台机器、同一进程、同一输入**，直接对比两条执行路径：
  · OLD：完全复刻优化前 —— `thomas` 用 scipy 默认参数（含有限性全量扫描），
         装配每次新建数组（out=None）
  · NEW：当前代码路径 —— `check_finite=False + overwrite_ab`，装配复用预分配缓冲

说明：CPU 占用率不因本类优化而改变 —— 优化减少的是**每次迭代的耗时**
（少做内部拷贝与检查），而不是**并行度**。两者是不同维度，故任务管理器的
占用率看起来"一样"，但墙钟时间会缩短。
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
import numpy as np                                              # noqa: E402
from scipy.linalg import solve_banded                           # noqa: E402
import q2_core as qc                                            # noqa: E402
from q2_core import (rho_of, cp_of, k_of, D_of, iface, thomas,
                     assemble_C_var, rhs_C_var, DEF2)           # noqa: E402


def thomas_old(a, b, c, d):
    """优化前的实现（scipy 默认参数：check_finite=True，必然拷贝 ab/b）"""
    n = len(b)
    ab = np.zeros((3, n), dtype=float)
    ab[0, 1:] = c[:-1]
    ab[1, :] = b
    ab[2, :-1] = a[1:]
    return solve_banded((1, 1), ab, d)


def main():
    N, dr, h = 80, 2.5e-4, 1.0 / 32
    R0, hc, km = DEF2['R0'], DEF2['h'], DEF2['km']
    C = np.linspace(2.55, 1.0, N + 1)
    T = np.linspace(28.0, 49.9, N + 1)
    base = rhs_C_var(N, dr, h, R0, km, C, 0.04999)
    buf = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))

    def it_old():
        Dn = D_of(C, T)
        a, b, c = assemble_C_var(N, dr, h, iface(Dn), R0, km)      # 无预分配
        return thomas_old(a, b, c, base)                            # scipy 默认参数

    def it_new():
        Dn = D_of(C, T)
        a, b, c = assemble_C_var(N, dr, h, iface(Dn), R0, km, out=buf)
        return thomas(a, b, c, base)                                # 快参数

    def meas(f, n=4000):
        f()
        t0 = time.perf_counter()
        for _ in range(n):
            f()
        return (time.perf_counter() - t0) / n * 1e6

    t_o, t_n = meas(it_old), meas(it_new)
    print('=' * 70)
    print('单次完整 Picard 迭代耗时（同一进程内交替测量，n=4000）')
    print('=' * 70)
    print(f'  优化前路径  {t_o:7.2f} us/迭代')
    print(f'  当前路径    {t_n:7.2f} us/迭代')
    print(f'  ⟹ 单迭代加速 {t_o/t_n:.2f}×   （纯 CPU 串行，单线程）')
    print()
    print('  推算主力（10800 步 × 32 子步 × 平均 ~16 次迭代）：')
    iters = 10800 * 32 * 16
    print(f'     优化前 ≈ {iters*t_o/1e6:6.0f} s')
    print(f'     当前   ≈ {iters*t_n/1e6:6.0f} s')
    print()
    print('  说明：两者均为**单线程**，任务管理器中的 CPU 占用率**不会变化**；')
    print('        变化的是墙钟时间。想提高占用率 ⟹ 必须引入多进程（见 W2/E6），')
    print('        但主力求解的时间步**严格串行依赖**，无法并行。')
    print('=' * 70)


if __name__ == '__main__':
    main()
