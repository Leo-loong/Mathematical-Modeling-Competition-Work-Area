# -*- coding: utf-8 -*-
"""
Q2 诊断：内层 Picard 迭代的收敛性与其对结果的实际影响（T1 级小规模诊断）
=====================================================================
背景
----
主力求解日志显示「内层均 256.0 次/步」= 32 子步 × **8 次上限跑满**，
且「内层最大残差 1.39e-04」远大于判据 tol=1e-10 ⟹ 内层迭代**从未收敛**。

本诊断回答一个问题：**这会不会影响结果**？

方法（A/B 对照，同一时程、同一设置，只改内层迭代上限与判据）
--------------------------------------------------------
  A) 当前设置：maxit=8,   tol=1e-10
  B) 高精度参考：maxit=400, tol=1e-14

比较两者**末端场**的 max|ΔT|、max|ΔC|：
  · 差异 < 1e-6  ⟹ 内层上限不构成实质影响（当前结果可信），仅需修正日志表述；
  · 差异 ≥ 1e-4  ⟹ 第 3–4 位小数不可靠，**必须修复后重跑主力**。

用法：python q2_diag_picard.py
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import numpy as np                                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from q2_core import run_q2                                       # noqa: E402

LOG = os.path.join(HERE, 'q2_diag_picard_log.txt')
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(s)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')


def main():
    open(LOG, 'w', encoding='utf-8').close()
    N, DR = 80, 2.5e-4
    NSUB = 32
    TINF, CINF = 50.00, 0.04999

    # 取 600 s 时程：此时 C 已显著下降（内有非线性最强段），耗时约 15 s（T1 级）
    NSTEP = 600

    say('=' * 78)
    say('Q2 诊断：内层 Picard 收敛性对结果的影响（A/B 对照）')
    say('=' * 78)
    say(f'  时程 {NSTEP} s   Δr={DR*1e3:.2f} mm   N={N}   子步={NSUB}   恒定边界({TINF} ℃, {CINF})')

    out = {}
    for tag, maxit, tol in (('A 当前 maxit=8, tol=1e-10', 8, 1e-10),
                            ('B 高精 maxit=120, tol=1e-13', 120, 1e-13)):
        t0 = time.time()
        res, _, _ = run_q2(N=N, dr=DR, dt_out=1.0, nsteps=NSTEP, n_sub=NSUB,
                           Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                           mode='coupled', maxit=maxit, tol=tol)
        st = res['stats']
        it_per_sub = st['inner_tot'] / max(1, NSTEP * NSUB)
        say(f'\n  [{tag}]  耗时 {time.time()-t0:.1f}s')
        say(f'     内层迭代 {st["inner_tot"]} 次  ⟹  平均 {it_per_sub:.3f} 次/子步'
            f'（上限 {maxit} ⟹ {"跑满上限" if abs(it_per_sub-maxit) < 0.01 else "未跑满"}）')
        say(f'     内层残差 max = {st["resC_max"]:.3e}')
        # 本轮未做"逐步收敛曲线"采集（不修改求解核），上述统计已足以判定
        out[tag] = res

    a, b = list(out.values())
    dT = float(np.max(np.abs(a['T_end'] - b['T_end'])))
    dC = float(np.max(np.abs(a['C_end'] - b['C_end'])))
    rT = dT / max(1e-30, float(np.max(np.abs(b['T_end']))))
    rC = dC / max(1e-30, float(np.max(np.abs(b['C_end']))))

    say('\n' + '=' * 78)
    say('【A/B 差异】（末端场的逐点最大差）')
    say(f'   max|ΔT| = {dT:.3e} ℃      相对 {rT:.3e}')
    say(f'   max|ΔC| = {dC:.3e} kg/kg  相对 {rC:.3e}')
    say('')
    if max(rT, rC) < 1e-6:
        say('  判定：**无实质影响** —— 当前内力迭代上限不改变结果（差异远小于输出精度）。')
        say('        处置：修正日志/文档表述即可，主力结果**可采信**。')
    elif max(rT, rC) < 1e-4:
        say('  判定：**边界情形** —— 差异接近输出精度（1e-4），第 4 位小数存疑。')
        say('        处置：建议提高内层迭代上限后重跑主力。')
    else:
        say('  判定：**有实质影响** —— 须修复内层迭代后重跑主力，并同步全部数值文档。')
    say('=' * 78)


if __name__ == '__main__':
    main()
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
