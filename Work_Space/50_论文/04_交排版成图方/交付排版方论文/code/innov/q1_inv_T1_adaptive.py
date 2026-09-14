# -*- coding: utf-8 -*-
"""T1-2 误差驱动步长（Richardson 半步后验误差）· 替代"凭经验的 1/32 s"

背景：原口径把温度内部子步定为 1/32 s，是**由 E1-b 试出来的**（1 s 误差 1.2e-3 ℃ 不可接受）。
本项把"步长"换成**误差判据**：以半步 Richardson 构造局部误差估计 est = ||T_h − T_{h/2}||∞，
用 PI 控制器调整步长使 est ≤ tol（相对全场 ≤5e-5）。

被积格式：**后向欧拉**（对照轨；交付轨已是"时间精确推进"，与步长无关，故本项的意义是
          证明"若沿用一阶格式，也可由误差判据自动定步长"，并给出步长轨迹图数据）。

参照：精确推进解（`q1_exact.run_T_expm`，时间误差归零）。

运行：python q1_inv_T1_adaptive.py
"""
import io
import os
import numpy as np

from q1_inv_lib import Rec, env_fns, FIGDATA
import q1_core as core
import q1_exact as ex

rec = Rec('q1_inv_T1_adaptive.log')
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
RHO = [0.0, 0.25, 0.5, 0.75, 1.0]
N, DR, R0 = 80, 0.25e-3, 0.02
IDX = [int(round(r * R0 / DR)) for r in RHO]
TOL = 5e-5


def be_step(A, kappa, T, ga, gb, h):
    """后向欧拉一步（T∞ 在步内线性 ⟹ 右端取 gb 即为一阶格式的标准写法）"""
    n = len(T)
    b = np.zeros(n)
    b[-1] = kappa * gb
    M = np.eye(n) - h * A
    return np.linalg.solve(M, T + h * b)


def adapt(Tenv, p, t_end=1800.0, tol=TOL, h0=1.0, hmin=1e-4, hmax=8.0, maxsteps=400000):
    """tol 为**全局**误差预算（℃）；每步允许的局部误差按 h/t_end **按比例分配**
    （即"局部误差预算 = tol·h/t_end"，使 Σ局部 ≤ tol）。"""
    A, kappa = ex.assemble_T_ode(N, DR, p)
    T = np.full(N + 1, p['T0'])
    ts, hs, ests = 0.0, h0, []
    trace = [(0.0, h0)]
    k = 0
    while ts < t_end - 1e-12 and k < maxsteps:
        h = min(hs, hmax, t_end - ts)
        ga, gb = float(Tenv(ts)), float(Tenv(ts + h))
        gm = float(Tenv(ts + h / 2))
        T2 = be_step(A, kappa, be_step(A, kappa, T, ga, gm, h / 2), gm, gb, h / 2)
        T1 = be_step(A, kappa, T, ga, gb, h)
        est_abs = float(np.max(np.abs(T2 - T1)))            # 绝对局部误差（℃）
        budget = tol * h / t_end                            # 本步预算
        fac = 0.9 * (budget / max(est_abs, 1e-300)) ** 0.5  # 一阶 ⟹ 指数 0.5
        fac = min(2.0, max(0.4, fac))
        T = T2
        ts += h
        k += 1
        ests.append(est_abs)
        hs = max(hmin, min(hmax, h * fac))
        trace.append((ts, hs))
    return T, np.array(trace), np.array(ests)


def main():
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(core.DEF)
    rec('=== T1-2 误差驱动步长（Richardson 半步后验误差）===')
    rec('判据 tol=%.1e（相对全场）；后向欧拉 ＋ PI 控制器（p=1）' % TOL)
    rec('')

    tex = ex.run_T_expm(N, DR, p, Tenv, 1800.0, hstep=1.0, t_snaps=SNAP)
    rec('— 参照：时间精确推进（时间误差 0）')

    bad = 0
    for tol, tag in ((TOL, 'tol=5e-5'), (1e-4, 'tol=1e-4')):
        T, trace, ests = adapt(Tenv, p, tol=tol)
        d_end = float(np.max(np.abs(T - tex['T_end'])))
        hs = np.diff(trace[:, 0])
        rec('')
        rec('— %s：总步数 %d（平均 h=%.4f s，min=%.4g／max=%.4g）; 相对固定口径 %d 步'
            % (tag, len(trace) - 1, hs.mean(), hs.min(), hs.max(), 1800 * 32))
        rec('   T(0,1800)=%.6f  T(R,1800)=%.6f  |  与精确推进差 max=%.3e ℃'
            % (T[0], T[-1], d_end))
        rec('   ⟹ %s' % ('PASS（≤5e-5）' if d_end <= 5e-5 else 'CHECK'))
        if tag.startswith('tol=5e-5'):
            bad += 0 if d_end <= 5e-5 else 1
            os.makedirs(FIGDATA, exist_ok=True)
            with io.open(os.path.join(FIGDATA, 'fig_q1_stepsize.csv'), 'w', encoding='utf-8') as f:
                f.write('t_s,h_next_s\n')
                for a, b in trace:
                    f.write('%.6f,%.6f\n' % (a, b))
            rec('   步长轨迹已写入 fig_q1_stepsize.csv（%d 点）' % len(trace))
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
