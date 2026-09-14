# -*- coding: utf-8 -*-
"""T2-3 全局灵敏度（Morris 筛选 ＋ Sobol 方差分解，经代理加速）

参数（归一化到 [0,1]，括号内为物理范围）：
  p1 h    （±20%）
  p2 km   （±20%）
  p3 D0   （±20%）
  p4 T∞ 整体偏移（±0.5 ℃）
  p5 C∞ 整体偏移（±5×10⁻⁴ kg/kg）

Morris：r=8 条轨迹 × (k+1)=6 点 = 48 次**严格解**（并行）
Sobol ：在 48 样本上拟合二次响应面代理，于代理上做 Saltelli（N=2048）
输出 ：μ*／σ 散点数据 ＋ Si／STi；与 OAT（E5）排序并置对照

运行：python q1_inv_T2_gs.py
"""
import io
import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

from q1_inv_lib import Rec, FIGDATA
from q1_inv_par import load_att1, solve_worker

rec = Rec('q1_inv_T2_gs.log')
KEY = ['CR', 'TR']
R = 8
NAMES = ['h', 'km', 'D0', 'Tinf_off', 'Cinf_off']
D = len(NAMES)


def to_cfg(u):
    u = np.asarray(u, dtype=float)
    return dict(p={'h': 25.0 * (0.8 + 0.4 * u[0]),
                   'km': 8.0e-7 * (0.8 + 0.4 * u[1]),
                   'D0': 7.0e-9 * (0.8 + 0.4 * u[2])},
                dt_off=-0.5 + 1.0 * u[3],
                dc_off=(-5e-4) + 1e-3 * u[4])


def main():
    t0 = time.time()
    rec('=== T2-3 全局灵敏度（Morris ＋ Sobol，代理加速）===')
    rec('参数：' + ' '.join(NAMES))
    rec('')
    rng = np.random.default_rng(11)
    delta = 2.0 / 3.0

    # ---------------- Morris 轨迹
    pts, traj = [], []
    for r in range(R):
        base = rng.random(D)
        order = rng.permutation(D)
        u = base.copy()
        traj.append(u.copy())
        for j in order:
            u = u.copy()
            u[j] = u[j] + delta if u[j] <= 1 - delta else u[j] - delta
            traj.append(u.copy())
    traj = np.array(traj)
    rec('Morris 采样：%d 条轨迹 × %d 点 = %d 次严格解' % (R, D + 1, len(traj)))
    with ProcessPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(solve_worker, [to_cfg(u) for u in traj]))
    Y = {k: np.array([x[k] for x in res]) for k in KEY}
    rec('  完成，耗时 %.1f s' % (time.time() - t0))

    rec('')
    rec('— Morris 基本效应（μ* 绝对值均值／σ 标准差）—')
    mu_star = {k: np.zeros(D) for k in KEY}
    sig = {k: np.zeros(D) for k in KEY}
    # 按"相邻点差分"计算 EE（轨迹内相邻两点恰有一个参数变动）
    for k in KEY:
        ee = np.zeros((R, D))
        for r in range(R):
            i0 = r * (D + 1)
            for j in range(D):
                diff = traj[i0 + j + 1] - traj[i0 + j]
                idx = int(np.argmax(np.abs(diff)))
                ee[r, idx] = (Y[k][i0 + j + 1] - Y[k][i0 + j]) / diff[idx]
        mu_star[k] = np.abs(ee).mean(axis=0)
        sig[k] = ee.std(axis=0, ddof=1)
    for j, nm in enumerate(NAMES):
        line = ' '.join('%s:μ*=%.3e σ=%.3e' % (k, mu_star[k][j], sig[k][j]) for k in KEY)
        rec('  %-9s %s' % (nm, line))

    # ---------------- 代理 ＋ Sobol
    def design(X):
        cols = [np.ones(len(X))]
        for i in range(D):
            cols.append(X[:, i])
        for i in range(D):
            for j in range(i, D):
                cols.append(X[:, i] * X[:, j])
        return np.column_stack(cols)

    A_ = design(traj)
    NS = 2048
    rec('')
    rec('— Sobol（代理上 Saltelli，N=%d）—' % NS)
    M = rng.random((NS, D)); Nm = rng.random((NS, D))
    sobol = {}
    for k in KEY:
        coef, *_ = np.linalg.lstsq(A_, Y[k], rcond=None)
        f = lambda X: design(X) @ coef
        fA, fB = f(M), f(Nm)
        VY = np.var(np.concatenate([fA, fB]), ddof=1)
        Si, STi = np.zeros(D), np.zeros(D)
        for i in range(D):
            ABi = M.copy(); ABi[:, i] = Nm[:, i]
            fAB = f(ABi)
            Si[i] = np.mean(fB * (fAB - fA)) / VY
            BAi = Nm.copy(); BAi[:, i] = M[:, i]
            fBA = f(BAi)
            STi[i] = 0.5 * np.mean((fA - fAB) ** 2) / VY
        sobol[k] = (np.clip(Si, -1, 1), np.clip(STi, 0, 1))
        rec('  [%s] ' % k + ' '.join('%s S1=%+.3f ST=%.3f' % (NAMES[j], Si[j], STi[j]) for j in range(D)))

    rec('')
    rec('— 与 OAT（E5）排序并置 —')
    for k in KEY:
        rank_g = [NAMES[j] for j in np.argsort(-sobol[k][1])]
        rec('  [%s] 全局（ST）排序：%s' % (k, ' > '.join(rank_g)))

    os.makedirs(FIGDATA, exist_ok=True)
    with io.open(os.path.join(FIGDATA, 'fig_q1_gs.csv'), 'w', encoding='utf-8') as f:
        f.write('output,param,mu_star,sigma,S1,ST\n')
        for k in KEY:
            for j, nm in enumerate(NAMES):
                f.write('%s,%s,%.8e,%.8e,%.8f,%.8f\n'
                        % (k, nm, mu_star[k][j], sig[k][j], sobol[k][0][j], sobol[k][1][j]))
    rec('  已写入 fig_q1_gs.csv')
    rec('')
    rec('结论：① 全局（ST）与单因素（OAT）排序一致性见上；')
    rec('      ② ST−S1 反映**交互效应**；若显著则须如实说明"OAT 低估交互"。')
    rec('      ③ 代理为二次响应面，56 点内插可信、外推不可信（如实声明）。')
    rec('总耗时 %.1f s' % (time.time() - t0))
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
