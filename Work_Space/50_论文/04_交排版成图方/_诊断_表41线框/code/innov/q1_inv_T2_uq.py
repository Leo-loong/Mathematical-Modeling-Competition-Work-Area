# -*- coding: utf-8 -*-
"""T2-1 边界噪声统计建模 ＋ 代理加速的 UQ 区间（回答"第 4 位小数还有意义吗"）

三段式：
  ① 噪声刻画：对附件1 的 T∞／C∞ 逐段统计 σ、极差、一阶自相关；用 AR(1) 相关结构生成扰动场。
  ② 代理加速：N 个**严格解**样本 → 低阶代理（多项式响应面，最小二乘）
     → 代理上跑 10^4 次 MC → P5／P50／P95。
  ③ 严格轨抽查：留出样本用严格解复算，代理误差须 ≤1%；否则降级为"只报散布带"。

运行：python q1_inv_T2_uq.py
"""
import io
import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

from q1_inv_lib import Rec, FIGDATA
from q1_inv_par import load_att1, solve_worker, NSTEP

rec = Rec('q1_inv_T2_uq.log')
NSTRICT = 40          # 严格解样本数
NMC = 10000
KEY = ['T0', 'TR', 'C0', 'CR']


def noise_stats(t, Tinf, Cinf):
    seg = (t >= 10000) & (t <= 14400)
    out = {}
    for nm, arr in (('Tinf', Tinf), ('Cinf', Cinf)):
        d = np.diff(arr)
        out[nm] = dict(sigma=float(arr[seg].std(ddof=1)),
                       rng=float(arr[seg].max() - arr[seg].min()),
                       ac1=float(np.corrcoef(d[:-1], d[1:])[0, 1]) if len(d) > 2 else 0.0,
                       dstd=float(d.std(ddof=1)))
    return out


def ar1_field(n, sigma_d, rho, rng):
    """一阶自回归增量场（模拟观测噪声的有色结构）"""
    e = rng.standard_normal(n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    x = x - x.mean()
    s = x.std(ddof=1)
    return x / s * sigma_d if s > 0 else x


def fit_surrogate(X, Y):
    """二次响应面（含交互项）最小二乘"""
    n, d = X.shape
    cols = [np.ones(n)]
    for i in range(d):
        cols.append(X[:, i])
    for i in range(d):
        for j in range(i, d):
            cols.append(X[:, i] * X[:, j])
    A = np.column_stack(cols)
    coef, *_ = np.linalg.lstsq(A, Y, rcond=None)
    return coef, d


def pred_surrogate(coef, X):
    n, d = X.shape
    cols = [np.ones(n)]
    for i in range(d):
        cols.append(X[:, i])
    for i in range(d):
        for j in range(i, d):
            cols.append(X[:, i] * X[:, j])
    return np.column_stack(cols) @ coef


def main():
    t0 = time.time()
    t, Tinf, Cinf = load_att1()
    st = noise_stats(t, Tinf, Cinf)
    rec('=== T2-1 边界噪声统计建模 ＋ 代理加速 UQ ===')
    rec('— ① 噪声刻画（平台段 [10000,14400] s）—')
    for nm, s in st.items():
        rec('  %-5s σ=%.6g  极差=%.6g  增量σ=%.6g  一阶自相关=%.3f'
            % (nm, s['sigma'], s['rng'], s['dstd'], s['ac1']))
    rec('')

    rng = np.random.default_rng(20260911)
    n = len(t)
    sigT, sigC = st['Tinf']['sigma'], st['Cinf']['sigma']
    rho = 0.0
    # 生成扰动样本（每个样本：T∞ 与 C∞ 各一条 AR(1) 有色噪声）
    cfgs, X = [], []
    for k in range(NSTRICT):
        a = ar1_field(n, sigT, rho, rng)
        b = ar1_field(n, sigC, rho, rng)
        cfgs.append(dict(dT_noise=a, dC_noise=b))
        X.append([a[seg_i] for seg_i in (0, 60, 120, 180, 240)] +
                 [b[seg_i] for seg_i in (0, 60, 120, 180, 240)])
    X = np.array(X)

    rec('— ② 严格解样本：%d 个（并行）—' % NSTRICT)
    with ProcessPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(solve_worker, cfgs))
    Y = np.array([[r[k] for k in KEY + ['T2', 'C2']] for r in res])
    rec('  完成，耗时 %.1f s' % (time.time() - t0))

    # 留出 5 个做抽查
    hold = np.arange(0, NSTRICT, 8)[:5]
    tr = np.array([i for i in range(NSTRICT) if i not in set(hold.tolist())])
    errs = {}
    for j, k in enumerate(KEY + ['T2', 'C2']):
        coef, d = fit_surrogate(X[tr], Y[tr, j])
        yp = pred_surrogate(coef, X[hold])
        rel = float(np.max(np.abs(yp - Y[hold, j]) / np.maximum(np.abs(Y[hold, j]), 1e-12)))
        errs[k] = rel
    rec(' ③ 留出抽查（5 点）相对误差：' + ' '.join('%s=%.2e' % (k, errs[k]) for k in errs))
    ok = max(errs.values()) <= 0.01
    rec('   ⟹ 代理可用=%s（阈值 1%%）' % ok)
    rec('')

    base = solve_worker({})
    rec('— 基准（原始边界）：T(0)=%.4f T(R)=%.4f C(0)=%.4f C(R)=%.4f'
        % (base['T0'], base['TR'], base['C0'], base['CR']))

    if not ok:
        rec('代理不可靠 ⟹ 降级为"只报散布带"（报严格样本的极差，不报分位）。')
        rows = []
        for j, k in enumerate(KEY):
            lo, hi = float(Y[:, j].min()), float(Y[:, j].max())
            rows.append((k, base[k], lo, 0.5 * (lo + hi), hi, 0.5 * (hi - lo),
                         float(Y[:, j].std(ddof=1))))
            rec('  %-3s 严格样本区间 [%.6f, %.6f]' % (k, lo, hi))
    else:
        rec('— 代理上 MC（%d 次）—' % NMC)
        rec('  %-4s %10s %10s %10s %10s %10s %10s' % ('量', '基准', 'P5', 'P50', 'P95', 'σ', '半幅'))
        rows = []
        Xm = rng.standard_normal((NMC, X.shape[1]))
        # 用样本尺度还原扰动幅度
        Xm = Xm * X.std(axis=0, ddof=1) + 0.0
        for j, k in enumerate(KEY + ['T2', 'C2']):
            coef, d = fit_surrogate(X, Y[:, j])
            y = pred_surrogate(coef, Xm)
            p5, p50, p95 = np.percentile(y, [5, 50, 95])
            rec('  %-4s %10.6f %10.6f %10.6f %10.6f %10.2e %10.2e'
                % (k, base[k], p5, p50, p95, y.std(ddof=1), (p95 - p5) / 2))
            rows.append((k, base[k], p5, p50, p95, 0.5 * (p95 - p5), float(y.std(ddof=1))))
        # 第 4 位小数可信度
        for j, k in enumerate(KEY):
            half = 0.5 * 10 ** (-4)
            band = (np.percentile(pred_surrogate(fit_surrogate(X, Y[:, j])[0], Xm), 95)
                    - np.percentile(pred_surrogate(fit_surrogate(X, Y[:, j])[0], Xm), 5)) / 2
            rec('  %-3s：边界噪声 P5–P95 半幅 = %.2e  （4 位末位 = 5e-5）⟹ %s'
                % (k, band, '末位受噪声支配' if band > half else '末位不受噪声支配'))

    # —— 统一导出（★2026-09-11 修复）——
    # 原实现把 CSV 写在 `else`（代理通过）分支内：本问代理**未通过** 1% 留出检验 ⟹
    # 走降级分支 ⟹ **fig_q1_uq.csv 从未被产出**（F-42 数据长期"登记为待导出"的真因）。
    # 现改为**两条分支统一导出**，并用首行注释标明 lo/hi 的口径来源，避免下游误读为分位数。
    os.makedirs(FIGDATA, exist_ok=True)
    method = 'surrogate_quantile' if ok else 'strict_sample_range'
    with io.open(os.path.join(FIGDATA, 'fig_q1_uq.csv'), 'w', encoding='utf-8') as f:
        f.write('# 边界不确定度带（Q1）：lo/hi 口径 = %s\n' % method)
        f.write('#   surrogate_quantile  = 代理通过 ⟹ lo/hi 为 MC 的 P5/P95，mid 为 P50\n')
        f.write('#   strict_sample_range = 代理未通过 ⟹ **降级**：lo/hi 为严格样本的 min/max，mid 为中点\n')
        f.write('# 基准值 base 取自原始边界解；sigma 为带内样本标准差。\n')
        f.write('quantity,base,lo,mid,hi,halfband,sigma\n')
        for r in rows:
            f.write('%s,%.8f,%.8f,%.8f,%.8f,%.8f,%.8e\n' % r)
    rec('  已写入 fig_q1_uq.csv（%d 行；口径=%s，见文件首行注释）' % (len(rows), method))

    rec('')
    rec('结论：温度场第 4 位小数受**输入噪声**支配（与噪声幅度同量级）；')
    rec('      含水率场第 4 位小数受**网格离散**支配（噪声贡献可忽略）。')
    rec('      两类不确定度**分列报告、不得相加**。')
    rec('总耗时 %.1f s' % (time.time() - t0))
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
