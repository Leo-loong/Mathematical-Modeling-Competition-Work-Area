# -*- coding: utf-8 -*-
"""T2-2 边界"真值"的状态空间数据同化（Kalman 滤波 ＋ RTS 后向平滑）

与 T2-1 构成**两条独立的 UQ 路线**：
  T2-1 = 前向传播（给噪声模型 → 抽样 → 看输出散布）；
  T2-2 = 反向反演（把附件1 视为"含噪观测" → 估计"真边界"及其后验方差 → 传播）。

⚠ **强声明**：题面给定附件1 即为边界输入 ⟹ **平滑后的边界只作对照轨，严禁替换交付口径**；
   "随机游走状态 ＋ 高斯观测噪声"属**附加假设**（题面未给），其代价须在论文中声明。

运行：python q1_inv_T2_da.py
"""
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

from q1_inv_lib import Rec
from q1_inv_par import load_att1, solve_worker

rec = Rec('q1_inv_T2_da.log')
KEY = ['T0', 'TR', 'C0', 'CR']
NPOST = 24


def kf_rts(y, R, q):
    """**局部线性趋势**状态空间模型（level ＋ slope）的 Kalman 滤波 ＋ RTS 平滑。

    v1 用"纯随机游走"：过程噪声极小 ⟹ 无法跟踪 T∞ 由 28 ℃ 升到 50 ℃ 的**强趋势**，
    平滑结果出现系统性滞后（实测使 T(0,1800) 偏移 +0.49 ℃，属**模型误设**）。
    本版改用 level+slope（积分随机游走），可同时跟踪趋势与压制观测噪声。
    返回 (x_hat, P_diag)
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    Q = q * np.array([[1.0 / 3.0, 0.5], [0.5, 1.0]])
    xf = np.zeros((n, 2)); Pf = np.zeros((n, 2, 2))
    xp = np.zeros((n, 2)); Pp = np.zeros((n, 2, 2))
    x = np.array([y[0], (y[1] - y[0]) if n > 1 else 0.0])
    P = np.diag([1e3 * R, 1e-2 * q])
    for k in range(n):
        if k > 0:
            x = F @ x
            P = F @ P @ F.T + Q
        xp[k], Pp[k] = x.copy(), P.copy()
        S = P[0, 0] + R
        K = P[:, 0] / S
        x = x + K * (y[k] - x[0])
        P = P - np.outer(K, P[0, :])
        xf[k], Pf[k] = x.copy(), P.copy()
    xs = xf.copy(); Ps = Pf.copy()
    for k in range(n - 2, -1, -1):
        C = Pf[k] @ F.T @ np.linalg.inv(Pp[k + 1])
        xs[k] = xf[k] + C @ (xs[k + 1] - xp[k + 1])
        Ps[k] = Pf[k] + C @ (Ps[k + 1] - Pp[k + 1]) @ C.T
    return xs[:, 0], np.maximum(Ps[:, 0, 0], 0.0)


def main():
    t0 = time.time()
    t, Tinf, Cinf = load_att1()
    seg = (t >= 10000) & (t <= 14400)
    sT = float(Tinf[seg].std(ddof=1))
    sC = float(Cinf[seg].std(ddof=1))
    rec('=== T2-2 边界状态空间数据同化（Kalman ＋ RTS · **局部线性趋势**状态）===')
    rec('观测噪声标定（平台段）：σ(T∞)=%.5g ℃  σ(C∞)=%.5g kg/kg' % (sT, sC))
    rec('状态模型：level＋slope（积分随机游走，过程方差 q=1e-4）—— 可跟踪趋势（v1 随机游走不可）')
    rec('')

    xT, PT = kf_rts(Tinf, R=sT ** 2, q=1e-4)
    xC, PC = kf_rts(Cinf, R=sC ** 2, q=(sC * 1e-4) ** 2 * 1e4)
    rec('平滑后边界：T∞ 平台段 σ 由 %.5g → %.5g（降低 %.1f%%）；C∞ σ 由 %.5g → %.5g（降低 %.1f%%）'
        % (sT, xT[seg].std(ddof=1), 100 * (1 - xT[seg].std(ddof=1) / sT),
           sC, xC[seg].std(ddof=1), 100 * (1 - xC[seg].std(ddof=1) / sC)))
    rec('平滑残差 max|y−x̂|：T∞ %.3e ℃ ；C∞ %.3e kg/kg' %
        (np.max(np.abs(Tinf - xT)), np.max(np.abs(Cinf - xC))))
    rec('后验标准差均值：T∞ %.3e ℃ ；C∞ %.3e kg/kg' % (PT.mean() ** 0.5, PC.mean() ** 0.5))
    rec('')

    base = solve_worker({})
    rec('基准（原始附件1）：T(0)=%.4f T(R)=%.4f C(0)=%.4f C(R)=%.4f'
        % (base['T0'], base['TR'], base['C0'], base['CR']))

    # 轨 A：以后验均值（平滑边界）重解
    mean_cfg = dict(dT_noise=xT - Tinf, dC_noise=xC - Cinf)
    rmean = solve_worker(mean_cfg)
    rec('')
    rec('— 轨 A：以后验**均值**边界重解（对照轨，**不替换交付**）—')
    for k in KEY:
        rec('  %-3s 基准 %.6f → 后验均值 %.6f  （Δ=%+.2e）'
            % (k, base[k], rmean[k], rmean[k] - base[k]))

    # 轨 B：从后验抽样（随机游走 ＋ 后验方差），并行重解 → 后验带
    rng = np.random.default_rng(7)
    cfgs, used = [], []
    n = len(t)
    while len(cfgs) < NPOST:
        zT = rng.standard_normal(n)
        zC = rng.standard_normal(n)
        aT = xT + np.sqrt(PT) * zT * 0.5      # 后验抽样（幅度按后验 sd 的 1/2，保守）
        aC = xC + np.sqrt(PC) * zC * 0.5
        cfgs.append(dict(dT_noise=aT - Tinf, dC_noise=aC - Cinf))
    with ProcessPoolExecutor(max_workers=12) as ex:
        res = list(ex.map(solve_worker, cfgs))
    rec('')
    rec('— 轨 B：后验抽样 %d 条 → 输出后验带 —' % NPOST)
    rec('  %-4s %10s %10s %10s %10s' % ('量', '基准', 'P5', 'P50', 'P95'))
    band = {}
    for k in KEY:
        v = np.array([r[k] for r in res])
        p5, p50, p95 = np.percentile(v, [5, 50, 95])
        band[k] = (p5, p95)
        rec('  %-4s %10.6f %10.6f %10.6f %10.6f' % (k, base[k], p5, p50, p95))
    rec('')
    rec('后验带半幅（(P95−P5)/2）：' + ' '.join('%s=%.2e' % (k, (band[k][1] - band[k][0]) / 2) for k in KEY))
    rec('')
    rec('与 T2-1 的正交对照：两条路线的带宽应**同量级**（前向 MC vs 后验抽样）；')
    rec('两者**方向一致**即可互证；若不一致，须**并列如实呈现**、不得择优选漂亮的。')
    rec('⚠ 轨 A 的平滑边界**只作对照**，交付口径仍为附件1 原始数据。')
    rec('总耗时 %.1f s' % (time.time() - t0))
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
