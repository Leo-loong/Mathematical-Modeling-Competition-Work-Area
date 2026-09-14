# -*- coding: utf-8 -*-
"""
外部核验（XCHK-1）：**内部步长 / 网格** 对 Q3 烘干时长的影响
================================================================================
对照对象：机构 GT02（MATLAB）——Q1/Q2 用 dt=1 s，**Q3 突变为 dt=30 s**（放大 30 倍）；
          网格 N=20（Δr=1 mm）。机构结果 t_dry ≈ 55.1–55.8 h。
我方主力：N=80（Δr=0.25 mm）、内部步长 1/32 s，t_end = 57.5314 h。

本实验：固定界面口径（沿 C 积分平均，即我方现行 M6），**只变时间步与网格**，
        判定"机构与我方 4% 差异"是否可由**离散分辨率**解释。

纪律：不改动任何既有文件（只读 `q3_core`）；产物写入 `innov/out/`。
用法：python q3_xchk_dt.py [--smoke]
"""
import os
import sys
import time
import argparse
import json

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
sys.path.insert(0, Q3DIR)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
OUTDIR = os.path.join(HERE, 'out')
LOGDIR = os.path.join(HERE, 'logs')
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(LOGDIR, exist_ok=True)

import openpyxl                                              # noqa: E402
import q3_core as q3                                         # noqa: E402

R0, HC, KM = 0.02, 25.0, 8e-7
OUTDT = 60.0                    # 输出/判据步长（题面规定 60 s）
TMAX_H = 400.0                  # 熔断（小时）

BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


def load_env():
    wb = openpyxl.load_workbook(
        os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'), data_only=True)
    sh = wb.active
    rows = [r for r in sh.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    ta = np.array([float(r[0]) for r in d])
    Ta = np.array([float(r[1]) for r in d])
    Ca = np.array([float(r[2]) for r in d])
    wb.close()
    return q3.env_tables_from_att1(ta, Ta, Ca)


def run_case(N, dt_sub, ts, Tv, Cv, tag=''):
    """固定内部步长推进至 max(C)<0.15；返回 (t_end_h, 总子步, C_center_end, 墙钟)"""
    dr = R0 / N
    n_sub = max(1, int(round(OUTDT / dt_sub)))
    dt_act = OUTDT / n_sub
    T = np.full(N + 1, 28.0)
    C = np.full(N + 1, 2.55)
    t = 0.0
    subs = 0
    t0 = time.time()
    while t < TMAX_H * 3600.0:
        T, C, _ = q3.step_imex_fast(N, dr, dt_act, n_sub, R0, HC, KM,
                                    T, C, ts, Tv, Cv, t)[:3]
        t += OUTDT
        subs += n_sub
        if float(np.max(C)) < 0.15:
            break
    return t / 3600.0, subs, float(C[0]), time.time() - t0, dt_act


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    args = ap.parse_args()

    ts, Tv, Cv = load_env()

    say('=' * 92)
    say('XCHK-1 | 内部步长 / 网格 对 Q3 烘干时长的影响（界面口径固定＝沿 C 积分平均）')
    say('=' * 92)
    say('  基准：N=80、内部步长 1/32 s ⟹ 我方主力 t_end = 57.5314 h')
    say('  对照：机构 GT02 Q3 用 dt=30 s、N=20 ⟹ t_dry ≈ 55.1–55.8 h')

    # ── 实验 A：内部步长扫描（固定 N=80，我方主力网格）──
    if args.smoke:
        dt_list = [30.0, 1.0]
    else:
        dt_list = [30.0, 15.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.25,
                   1 / 8, 1 / 16, 1 / 32]
    say('')
    say('─' * 92)
    say('  【实验 A】内部步长扫描（N=80，Δr=0.25 mm）')
    say('  %-12s %-10s %-14s %-14s %-12s %-10s' %
        ('设定步长/s', '实际/s', 't_end/h', '相对1/32', '中心C(末)', '墙钟/s'))
    recA = []
    base = None
    for dt in dt_list:
        te, subs, cmax, wall, dta = run_case(80, dt, ts, Tv, Cv)
        if abs(dt - 1 / 32) < 1e-12:
            base = te
        recA.append(dict(dt_set=dt, dt_act=dta, t_end=te, subs=subs, wall=wall))
        say('  %-12.6g %-10.6g %-14.4f %-14s %-12.4f %-10.1f' %
            (dt, dta, te, '—' if base is None else '%+.3f%%' % (100 * (te - base) / base),
             cmax, wall))

    # ── 实验 B：网格扫描（在 dt=30 s 与 dt=1/32 s 两个步长下）──
    say('')
    say('─' * 92)
    say('  【实验 B】网格扫描（两组步长，检验"粗网格+大步长"的组合效应）')
    say('  %-8s %-10s %-12s %-14s %-12s %-10s' %
        ('N', 'Δr/mm', '步长/s', 't_end/h', '中心C(末)', '墙钟/s'))
    recB = []
    if args.smoke:
        grid = [(20, 30.0), (80, 30.0)]
    else:
        grid = [(20, 30.0), (20, 1.0), (40, 30.0), (40, 1.0),
                (80, 30.0), (80, 1.0), (80, 1 / 32), (160, 1 / 32)]
    for N, dt in grid:
        te, subs, cmax, wall, _ = run_case(N, dt, ts, Tv, Cv)
        recB.append(dict(N=N, dt=dt, t_end=te, wall=wall))
        say('  %-8d %-10.4f %-12.6g %-14.4f %-12.4f %-10.1f' %
            (N, R0 / N * 1000, dt, te, cmax, wall))

    # ── 判读 ──
    say('')
    say('─' * 92)
    say('  【判读】')
    a30 = [r for r in recA if abs(r['dt_set'] - 30.0) < 1e-9]
    a_b = [r for r in recA if abs(r['dt_set'] - 1 / 32) < 1e-12]
    if a30 and a_b:
        d = 100 * (a30[0]['t_end'] - a_b[0]['t_end']) / a_b[0]['t_end']
        say('   · N=80 时，把内部步长由 1/32 s 放大到 30 s ⟹ t_end 变化 %+.2f%%（%.4f → %.4f h）'
            % (d, a_b[0]['t_end'], a30[0]['t_end']))
        say('   · 若该变化量为负且量级与机构差异（约 -4%）相当 ⟹ **机构差异可由时间步解释**')
    say('   · 机构自报 t_dry ≈ 55.1–55.8 h；对比上表可直接定位其配置来源')

    with open(os.path.join(LOGDIR, 'q3_xchk_dt.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    if not args.smoke:
        with open(os.path.join(OUTDIR, 'fig_q3_xchk_dt.csv'), 'w', encoding='utf-8') as f:
            f.write('kind,N,dt_sub,t_end_h\n')
            for r in recA:
                f.write('A,80,%.8f,%.6f\n' % (r['dt_act'], r['t_end']))
            for r in recB:
                f.write('B,%d,%.8f,%.6f\n' % (r['N'], r['dt'], r['t_end']))
    say('')
    say('  已写出 logs/q3_xchk_dt.log 与 out/fig_q3_xchk_dt.csv')


if __name__ == '__main__':
    main()
