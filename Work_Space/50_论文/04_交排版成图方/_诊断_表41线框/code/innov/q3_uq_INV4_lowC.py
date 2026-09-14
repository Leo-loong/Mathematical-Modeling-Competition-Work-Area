# -*- coding: utf-8 -*-
"""
IN-4b | 低含水率端 D 公式外推的**不确定性量化**（创新副本 · 不改动正式产物）
================================================================================
问题：Q3 把附录3 的 D 公式推至 C≈0.053（远低于 Q1/Q2 的 C≥1.0）。
      "公式在多低的 C 以下不再可信"**是未知的** ⟹ 这是**模型外推不确定度**（区别于 IN-4a 的离散不确定度）。

建模：引入"**公式可信下限**" $C_{\rm fr}$（物理含义：C < C_fr 时不再信任公式，D 冻结为 D(C_fr)）。
      该参数**不可由题面确定** ⟹ 按**区间/概率**处理：
        (a) 确定性截断族  C_fr ∈ {0(无截断), 0.15, 0.2, …, 1.0} ⟹ 敏感性曲线
        (b) 概率先验      C_fr ~ U[0.15, 1.0]（**主观设定，须在论文中显式声明**），
                          LHS 采样 16 点 ⟹ t_end 的分位数（P5/P50/P95）

采样引擎：IN-1 自适应快轨（tol=5e-5，约 1.6 s/次）＋ 冻结能力（`q3_core_nu.step_imex_gen` 的 c_frz）

自校：C_fr = 0 必须复现"无截断"基准（≈57.5 h），否则本项作废。

产物（带副本标记）：
  logs/q3_INV4_uq.log
  out/fig_q3_INV4_uq_grid.csv     （C_fr, t_end_h）
  out/fig_q3_INV4_uq_lhs.csv      （样本 C_fr, t_end_h）

用法：
  python q3_uq_INV4_lowC.py --smoke     # 冒烟：仅 2 个 C_fr
  python q3_uq_INV4_lowC.py             # 正式（约 1 min）
"""
import os
import sys
import time
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
Q3DIR = os.path.dirname(HERE)
WS = _find_root(HERE)
LOGDIR = os.path.join(HERE, 'logs')
OUTDIR = os.path.join(HERE, 'out')
os.makedirs(LOGDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')

BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


def _adaptive_tend_frz(geom, ts, Tv, Cv, c_frz, tol=5e-5,
                       dt0=1.0 / 32.0, dt_min=1.0 / 2048.0, dt_max=60.0,
                       max_hours=120.0):
    """自适应推进（Richardson 后验误差）＋ D 冻结（c_frz）。返回 t_end（h）"""
    import q3_core_nu as nu
    R0, hc, km = 0.02, 25.0, 8e-7
    DT_OUT = 60.0
    T = np.full(81, 28.0)
    C = np.full(81, 2.55)
    t = 0.0
    dt = dt0
    t_max = max_hours * 3600.0
    while t < t_max - 1e-12:
        rem = DT_OUT - (t % DT_OUT)
        if rem <= 1e-9:
            rem = DT_OUT
        acc = False
        while not acc:
            dt_try = min(dt, rem, dt_max)
            T1, C1, _ = nu.step_imex_gen(geom, dt_try, 1, R0, hc, km, T, C,
                                         ts, Tv, Cv, t, c_frz=c_frz)[:3]
            T2, C2, _ = nu.step_imex_gen(geom, dt_try / 2.0, 2, R0, hc, km, T, C,
                                         ts, Tv, Cv, t, c_frz=c_frz)[:3]
            denC = max(1.0, float(np.max(np.abs(C2))))
            denT = max(1.0, float(np.max(np.abs(T2))))
            est = max(float(np.max(np.abs(C1 - C2))) / denC,
                      float(np.max(np.abs(T1 - T2))) / denT)
            if est <= tol or dt_try <= dt_min * 1.0000001:
                acc = True
                T, C = T2, C2
                t += dt_try
                if est > 1e-30:
                    dt = dt_try * 0.9 * np.sqrt(tol / est)
                else:
                    dt = dt_try * 2.0
                dt = min(max(dt, dt_try * 0.5), dt_try * 2.0)
                dt = min(max(dt, dt_min), dt_max)
            else:
                dt = max(dt_try * 0.5, dt_min)
        if float(np.max(C)) < 0.15:
            return t / 3600.0
    return float('nan')


def _worker(job):
    """子进程：给定 c_frz，返回 t_end（h）"""
    import os as _os
    import sys as _sys
    import numpy as _np
    import openpyxl as _xl
    idx, c_fr = job
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _q3dir = _os.path.dirname(_here)
    _ws = _find_root(_here)
    _sys.path.insert(0, _q3dir)
    _sys.path.insert(0, _os.path.join(_ws, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
    import q3_core_nu as _nu
    wb = _xl.load_workbook(_os.path.join(_ws, '10_赛题', 'A题', '附件', '附件1.xlsx'),
                           data_only=True)
    sh = wb.active
    rows = [r for r in sh.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    t = _np.array([float(r[0]) for r in d])
    T = _np.array([float(r[1]) for r in d])
    Cc = _np.array([float(r[2]) for r in d])
    wb.close()
    ts, Tv, Cv = _nu.env_tables_from_att1(t, T, Cc)
    geom = _nu.geom_uniform(80, 0.02)
    te = _adaptive_tend_frz(geom, ts, Tv, Cv, float(c_fr))
    return int(idx), float(te)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--n-lhs', type=int, default=16)
    ap.add_argument('--seed', type=int, default=20260911)
    args = ap.parse_args()

    from concurrent.futures import ProcessPoolExecutor

    say('=' * 88)
    say('IN-4b | 低 C 端 D 公式外推的不确定性量化（C_fr 截断族 ＋ 概率先验）')
    say('=' * 88)
    say('  物理含义：C_fr = "D 公式的可信下限"；C < C_fr 时 D 冻结为 D(C_fr)')
    say('  ⚠ C_fr **不可由题面确定** ⟹ 按区间/概率处理；先验为主观设定，须在论文中显式声明')

    if args.smoke:
        grid = [0.0, 0.3]
        lhs = []
        say('[SCALE] 冒烟：C_fr ∈ {0, 0.3}，2 次求解')
    else:
        grid = [0.0, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00]
        # LHS：C_fr ~ U[0.15, 1.0]
        rng = np.random.default_rng(args.seed)
        cuts = (np.arange(args.n_lhs)[:, None] + rng.random((args.n_lhs, 1))) / args.n_lhs
        lhs = (0.15 + cuts[:, 0] * (1.00 - 0.15)).tolist()
        say('[SCALE] 正式：确定性族 %d 点 ＋ LHS %d 点 = %d 次求解（快轨 ~1.6 s/次）'
            % (len(grid), len(lhs), len(grid) + len(lhs)))

    # ⚠ 索引必须**全局唯一**（否则 grid 与 LHS 的结果会互相覆盖 —— 首版即因此自校失败）
    payload = [(i, float(c)) for i, c in enumerate(grid)]
    payload += [(len(grid) + j, float(c)) for j, c in enumerate(lhs)]

    t0 = time.time()
    nw = min(8, os.cpu_count() or 4)
    res = np.full(len(payload), np.nan)
    with ProcessPoolExecutor(max_workers=nw) as ex:
        for idx, te in ex.map(_worker, payload):
            res[idx] = te
    say('  完成 %d 次求解，墙钟 %.1f s（并行度 %d）' % (len(payload), time.time() - t0, nw))

    gv = res[:len(grid)]
    lv = res[len(grid):]

    say('-' * 88)
    say('  【确定性截断族】')
    say('    %-10s %-14s' % ('C_fr', 't_end/h'))
    for c, v in zip(grid, gv):
        say('    %-10.3f %-14.4f' % (c, v))
    base = gv[0]
    if np.isfinite(base):
        say('    自校：C_fr=0（无截断）→ %.4f h（应≈57.5 h；若偏离过大则本项作废）' % base)
        say('    相对贡献：' + ' '.join('%+.1f%%' % (100 * (v - base) / base)
                                       for v in gv[1:] if np.isfinite(v)))
    if not args.smoke and np.isfinite(lv).any():
        q = np.nanpercentile(lv, [5, 25, 50, 75, 95])
        say('-' * 88)
        say('  【概率先验 C_fr ~ U[0.15, 1.0]，LHS N=%d】' % len(lhs))
        say('    t_end 分位：P5=%.4f  P25=%.4f  P50=%.4f  P75=%.4f  P95=%.4f h'
            % tuple(q))
        say('    ⟹ **模型外推不确定度**（相对无截断基准）：[-%.2f%%, +%.2f%%]'
            % (100 * (base - q[0]) / base, 100 * (q[4] - base) / base))
        say('    ⚠ 该区间**仅**反映"C_fr 未知"这一项；与 IN-4a 的**离散**不确定度**分列报告**，不得相加。')

    with open(os.path.join(LOGDIR, 'q3_INV4_uq.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    if not args.smoke:
        with open(os.path.join(OUTDIR, 'fig_q3_INV4_uq_grid.csv'), 'w', encoding='utf-8') as f:
            f.write('C_fr,t_end_h\n')
            for c, v in zip(grid, gv):
                f.write('%.3f,%.6f\n' % (c, v))
        with open(os.path.join(OUTDIR, 'fig_q3_INV4_uq_lhs.csv'), 'w', encoding='utf-8') as f:
            f.write('C_fr,t_end_h\n')
            for c, v in zip(lhs, lv):
                f.write('%.6f,%.6f\n' % (c, v))
        say('  已写出：logs/q3_INV4_uq.log 与 out/fig_q3_INV4_uq_*.csv')


if __name__ == '__main__':
    main()
