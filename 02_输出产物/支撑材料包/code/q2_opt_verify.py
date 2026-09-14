# -*- coding: utf-8 -*-
"""
Q2 性能优化 · 数值等价性校验（必过门槛：偏差 ≪ 5e-5）
=====================================================
三项独立校验
-----------
  V1 组件级：`assemble_*` 的 `out=None`（原路径）与 `out=(a,b,c)`（预分配路径）
             输出必须**逐位完全相同**（bitwise）。
  V2 组件级：`thomas` 优化版（check_finite=False + overwrite_ab）与
             **朴素参照实现**（scipy 默认参数）结果逐位一致。
  V3 端到端：以**优化前** W2 预试验已落盘的结果为基准（Δr=0.25 mm、h=1/32 s、
             1800 s、恒定边界），重跑同一算例，偏差必须 ≪ 5e-5。

用法：python q2_opt_verify.py
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np                                              # noqa: E402
from scipy.linalg import solve_banded                           # noqa: E402
from q2_core import (run_q2, assemble_T_var, assemble_C_var, thomas,
                     rho_of, cp_of, k_of, D_of, iface, DEF2)     # noqa: E402

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q2_opt_verify_log.txt')
BUF = []
FAIL = []


def say(s=''):
    print(s, flush=True)
    BUF.append(s)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')


def chk(name, ok, extra=''):
    say(f'   {"PASS" if ok else "**FAIL**"}  {name}{("  " + extra) if extra else ""}')
    if not ok:
        FAIL.append(name)


def v1_assemble():
    say('\n[V1] assemble_* 预分配路径 vs 原路径（逐位）')
    N, dr, dt = 80, 2.5e-4, 1.0 / 32
    R0, h, km = DEF2['R0'], DEF2['h'], DEF2['km']
    C = np.linspace(2.55, 1.0, N + 1)
    T = np.linspace(28.0, 49.9, N + 1)
    rho, cp, kk = rho_of(C), cp_of(C), k_of(C)
    Df = iface(D_of(C, T))

    a1, b1, c1 = assemble_T_var(N, dr, dt, R0, h, rho, cp, kk)
    buf = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))
    a2, b2, c2 = assemble_T_var(N, dr, dt, R0, h, rho, cp, kk, out=buf)
    chk('T 装配 a 逐位相同', np.array_equal(a1, a2))
    chk('T 装配 b 逐位相同', np.array_equal(b1, b2))
    chk('T 装配 c 逐位相同', np.array_equal(c1, c2))

    a1, b1, c1 = assemble_C_var(N, dr, dt, Df, R0, km)
    a2, b2, c2 = assemble_C_var(N, dr, dt, Df, R0, km, out=buf)
    chk('C 装配 a 逐位相同', np.array_equal(a1, a2))
    chk('C 装配 b 逐位相同', np.array_equal(b1, b2))
    chk('C 装配 c 逐位相同', np.array_equal(c1, c2))

    # 复用同一 buf 第二轮（检验"残留值"陷阱是否已被显式置零消除）
    a3, b3, c3 = assemble_C_var(N, dr, dt, Df, R0, km, out=buf)
    chk('C 装配 复用缓冲第二轮仍逐位相同',
        np.array_equal(a1, a3) and np.array_equal(b1, b3) and np.array_equal(c1, c3))


def v2_thomas():
    say('\n[V2] thomas 优化版 vs scipy 默认参数参照实现')
    rng = np.random.default_rng(20260911)
    N = 80
    a = rng.normal(size=N + 1)
    b = 10.0 + rng.random(N + 1) * 5.0
    c = rng.normal(size=N + 1)
    d = rng.normal(size=N + 1)
    a[0] = c[N] = 0.0

    ref = solve_banded((1, 1),
                       np.vstack([np.r_[0.0, c[:-1]], b, np.r_[a[1:], 0.0]]), d)
    got = thomas(a, b, c, d)
    chk('解逐位相同', np.array_equal(ref, got),
        f'max|Δ|={np.max(np.abs(ref - got)):.3e}')

    # 复现真实调用方式：d 在同一循环中被反复使用 ⟹ 必须未被覆写
    d_before = d.copy()
    for _ in range(3):
        thomas(a, b, c, d)
    chk('d 未被就地覆写（可安全复用）', np.array_equal(d, d_before))


def v3_end2end():
    say('\n[V3] 端到端回归：与**优化前**已落盘的 W2 基准值对比')
    # 基准值取自优化前 W2 运行（w2_foreground_log.txt，Δr=0.25mm / h=1/32s）
    TS_REF, CS_REF = 44.30366337, 1.75240165
    TOL = 5e-5
    t0 = time.time()
    res, _, _ = run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=1800, n_sub=32,
                       Tenv_fn=lambda _t: 50.00, Cenv_fn=lambda _t: 0.04999,
                       mode='coupled')
    wall = time.time() - t0
    Ts, Cs = float(res['T_end'][-1]), float(res['C_end'][-1])
    eT = abs(Ts - TS_REF) / abs(TS_REF)
    eC = abs(Cs - CS_REF) / abs(CS_REF)
    say(f'   Ts = {Ts:.8f}  (基准 {TS_REF:.8f})  相对偏差 {eT:.3e}')
    say(f'   Cs = {Cs:.8f}  (基准 {CS_REF:.8f})  相对偏差 {eC:.3e}')
    chk('温度端到端偏差 < 5e-5', eT < TOL)
    chk('含水率端到端偏差 < 5e-5', eC < TOL)
    return wall


def bench():
    say('\n[BENCH] 单次完整 Picard 迭代耗时（优化后）')
    N, dr, h = 80, 2.5e-4, 1.0 / 32
    R0, hc, km = DEF2['R0'], DEF2['h'], DEF2['km']
    C = np.linspace(2.55, 1.0, 81)
    T = np.linspace(28.0, 49.9, 81)
    d = np.zeros(81)
    buf = (np.zeros(81), np.zeros(81), np.zeros(81))

    def one_it_old():
        Dn = D_of(C, T)
        aa, bb, cc = assemble_C_var(N, dr, h, iface(Dn), R0, km)
        return thomas(aa, bb, cc, d)

    def one_it_new():
        Dn = D_of(C, T)
        aa, bb, cc = assemble_C_var(N, dr, h, iface(Dn), R0, km, out=buf)
        return thomas(aa, bb, cc, d)

    def meas(f, n=3000):
        f()
        t0 = time.perf_counter()
        for _ in range(n):
            f()
        return (time.perf_counter() - t0) / n * 1e6

    t_new = meas(one_it_new)
    t_old = meas(one_it_old)
    say(f'   原路径（out=None）      {t_old:7.2f} us/迭代')
    say(f'   优化路径（预分配+快参数） {t_new:7.2f} us/迭代')
    say(f'   ⟹ 单迭代加速 {t_old/t_new:.2f}×')


if __name__ == '__main__':
    open(LOG, 'w', encoding='utf-8').close()
    say('=' * 78)
    say('Q2 性能优化 · 数值等价性校验')
    say('=' * 78)
    v1_assemble()
    v2_thomas()
    wall = v3_end2end()
    bench()
    say('\n' + '=' * 78)
    if FAIL:
        say(f'❌ 未通过项 {len(FAIL)}：{FAIL}')
        say('   ⟹ **禁止使用**优化后的核；须回退。')
    else:
        say(f'✅ 全部校验通过（V3 端到端耗时 {wall:.1f}s）')
    say('=' * 78)
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
