# -*- coding: utf-8 -*-
"""
IN-4a | t_end 的 Richardson / GCI 误差带（创新副本 · 不改动任何正式产物）
================================================================================
目的：把核心答案从"单点值"升级为"**带离散误差带的值**"。
      注意 t_end = "首次达标时刻"属**非线性泛函**，其收敛阶不能沿用场量的二阶 ⟹ 须**实测观测阶**。

做法：
  · 空间 3 档：Δr = 0.25 / 0.125 / 0.0625 mm（N = 80 / 160 / 320），固定内部步 1/32 s
  · 时间 3 档：1/16 / 1/32 / 1/64 s，固定 N = 80
  · 每档事件驱动求解至全域 C < 0.15，记录 t_end 与墙钟
  · Richardson：p = log2( (t1-t2)/(t2-t3) )（由粗到细），t_ext = t3 + (t3-t2)/(2^p-1)
    GCI_fine = 1.25 * |(t3-t2)/t3| / (2^p - 1)
  · 若 (t1-t2)/(t2-t3) <= 1（非单调）⟹ **放弃 Richardson**，改报保守误差上界 |t3-t1|

产物（带副本标记）：
  innov/logs/q3_INV4_gci.log
  innov/out/fig_q3_INV4_gci.csv

用法：
  python q3_gci_INV4_tend.py --smoke     # 冒烟（小规模，仅验证流程，不出结论）
  python q3_gci_INV4_tend.py             # 正式（约 40 min，建议后台）
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
import openpyxl


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))          # .../Q3/innov
Q3DIR = os.path.dirname(HERE)                              # .../Q3
WS = _find_root(HERE)
sys.path.insert(0, Q3DIR)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))

import q3_core as q3                                       # noqa: E402
import q2_core_c as base                                   # noqa: E402

ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
C_CRIT = 0.15
DT_OUT = 60.0
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']

LOGDIR = os.path.join(HERE, 'logs')
OUTDIR = os.path.join(HERE, 'out')
os.makedirs(LOGDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)
LOG = os.path.join(LOGDIR, 'q3_INV4_gci.log')
CSV = os.path.join(OUTDIR, 'fig_q3_INV4_gci.csv')

BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


def load_att1():
    wb = openpyxl.load_workbook(ATT1, data_only=True)
    ws = wb.active
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in d])
    T = np.array([float(r[1]) for r in d])
    C = np.array([float(r[2]) for r in d])
    wb.close()
    return t, T, C


def solve_tend(N, dr, h_inner, ts, Tv, Cv, max_hours=120.0,
               tol=1e-10, maxit=30, progress=False):
    """事件驱动求解：返回 (t_end_s, C0_end, CR_end, wall_s, n_out_steps)"""
    NC = N + 1
    nsub = int(round(DT_OUT / h_inner))
    hh = DT_OUT / nsub
    T = np.full(NC, base.DEF2['T0'])
    C = np.full(NC, base.DEF2['C0'])
    nsteps_max = int(round(max_hours * 3600.0 / DT_OUT))
    t0 = time.time()
    for n in range(1, nsteps_max + 1):
        t_start = (n - 1) * DT_OUT
        Tp, Cp = T.copy(), C.copy()
        T, C, info = q3.step_imex_fast(N, dr, hh, nsub, R0, HC, KM, T, C,
                                       ts, Tv, Cv, t_start, tol=tol, maxit=maxit)
        if float(np.max(C)) < C_CRIT:
            lo, hi = 1, nsub
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = q3.step_imex_fast(N, dr, hh, mid, R0, HC, KM, Tp, Cp,
                                             ts, Tv, Cv, t_start, tol=tol, maxit=maxit)
                if float(np.max(Ca)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * hh
            if progress:
                say('      [达标] t=%.4f h（第 %d 输出步内第 %d 子步）'
                    % (t_end / 3600.0, n, lo))
            return t_end, float(C[0]), float(C[-1]), time.time() - t0, n
        if progress and n % 200 == 0:
            say('      ... t=%.2f h  C(0)=%.6f  wall=%.0fs'
                % (n * DT_OUT / 3600.0, float(C[0]), time.time() - t0))
    return float('nan'), float(C[0]), float(C[-1]), time.time() - t0, nsteps_max


def richardson(t1, t2, t3, Fs=1.25):
    """由粗到细三档：返回 (p, t_ext, gci_fine, 是否可用)"""
    d12, d23 = (t1 - t2), (t2 - t3)
    if abs(d23) < 1e-12:
        return float('nan'), t3, 0.0, False
    r = d12 / d23
    if not (r > 1.0 and np.isfinite(r)):
        return float('nan'), t3, float('nan'), False
    p = np.log2(r)
    if p <= 0 or p > 6:
        return float('nan'), t3, float('nan'), False
    t_ext = t3 + d23 / (2.0 ** p - 1.0)
    gci = Fs * abs(d23 / t3) / (2.0 ** p - 1.0)
    return float(p), float(t_ext), float(gci), True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true', help='冒烟：小规模，不出结论')
    args = ap.parse_args()

    t_a1, T_a1, C_a1 = load_att1()
    ts, Tv, Cv = q3.env_tables_from_att1(t_a1, T_a1, C_a1)

    say('=' * 92)
    say('IN-4a | t_end 的 Richardson / GCI 误差带（创新副本 · 不影响正式产物）')
    say('=' * 92)

    cases = []
    if args.smoke:
        # 冒烟：40 节点、1/16 s，只跑 1 h（不达标），仅验证流程可跑通
        cases = [('smoke', 40, 5.0e-4, 1.0 / 16.0, 1.0)]
        say('[SCALE] 冒烟：N=40、1/16 s、上限 1 h（不达标，仅流程验证）')
    else:
        for N, dr in ((80, 2.5e-4), (160, 1.25e-4), (320, 6.25e-5)):
            cases.append(('space', N, dr, 1.0 / 32.0, 120.0))
        for h in (1.0 / 16.0, 1.0 / 32.0, 1.0 / 64.0):
            cases.append(('time', 80, 2.5e-4, h, 120.0))
        say('[SCALE] 正式：空间 3 档（N=80/160/320 @1/32 s）＋ 时间 3 档（1/16,1/32,1/64 s @N=80）')
        say('        预计总墙钟 ≈ 40 min（单档 0.25–1.0 ks），事件驱动、熔断 120 h')

    rows = []
    for kind, N, dr, h_in, mh in cases:
        say('-' * 92)
        say('  算例 %-6s N=%-4d Δr=%.5f mm  内部步=%.6f s  上限=%.1f h'
            % (kind, N, dr * 1e3, h_in, mh))
        t_end, c0, cR, wall, nstep = solve_tend(N, dr, h_in, ts, Tv, Cv,
                                                max_hours=mh, progress=True)
        ok = np.isfinite(t_end)
        say('    ⟹ t_end = %s h（C(0)=%.6f C(R)=%.6f，%d 输出步，墙钟 %.1f s）'
            % (('%.4f' % (t_end / 3600.0)) if ok else '未达标',
               c0, cR, nstep, wall))
        rows.append(dict(kind=kind, N=N, dr_mm=dr * 1e3, h_in=h_in,
                         t_end_h=(t_end / 3600.0) if ok else float('nan'),
                         wall_s=wall, n_out=nstep))

    if args.smoke:
        say('-' * 92)
        say('  [冒烟结束] 仅验证流程可运行；**不出任何结论**')
        with open(LOG, 'w', encoding='utf-8') as f:
            f.write('\n'.join(BUF) + '\n')
        return

    # ---- 空间 GCI ----
    say('=' * 92)
    say('【空间维误差带】（固定内部步 1/32 s）')
    sp = [r for r in rows if r['kind'] == 'space']
    if len(sp) == 3 and all(np.isfinite(r['t_end_h']) for r in sp):
        t1, t2, t3 = (r['t_end_h'] for r in sp)
        p, t_ext, gci, ok = richardson(t1, t2, t3)
        if ok:
            say('  三档 t_end = %.4f / %.4f / %.4f h（0.25 / 0.125 / 0.0625 mm）' % (t1, t2, t3))
            say('  观测阶 p = %.3f ；外推值 t_ext = %.4f h ；GCI(细) = %.4f%% （≈ %.4f h）'
                % (p, t_ext, 100 * gci, gci * t3))
            say('  ⟹ 空间离散不确定度 ≈ ±%.4f h（约 ±%.3f%%）' % (gci * t3, 100 * gci))
        else:
            say('  三档 t_end = %.4f / %.4f / %.4f h ⟹ **非单调，放弃 Richardson**' % (t1, t2, t3))
            say('  ⟹ 改报保守误差上界 |t3-t1| = %.4f h' % abs(t3 - t1))
    else:
        say('  ⚠ 空间档未全部达标，无法计算')

    # ---- 时间维 GCI ----
    say('=' * 92)
    say('【时间维误差带】（固定 Δr = 0.25 mm）')
    tm = [r for r in rows if r['kind'] == 'time']
    if len(tm) == 3 and all(np.isfinite(r['t_end_h']) for r in tm):
        t1, t2, t3 = (r['t_end_h'] for r in tm)
        p, t_ext, gci, ok = richardson(t1, t2, t3)
        if ok:
            say('  三档 t_end = %.4f / %.4f / %.4f h（1/16 / 1/32 / 1/64 s）' % (t1, t2, t3))
            say('  观测阶 p = %.3f ；外推值 t_ext = %.4f h ；GCI(细) = %.4f%% （≈ %.4f h）'
                % (p, t_ext, 100 * gci, gci * t3))
            say('  ⟹ 时间离散不确定度 ≈ ±%.4f h' % (gci * t3))
        else:
            say('  三档 t_end = %.4f / %.4f / %.4f h ⟹ **非单调，放弃 Richardson**' % (t1, t2, t3))
            say('  ⟹ 改报保守误差上界 |t3-t1| = %.4f h' % abs(t3 - t1))
    else:
        say('  ⚠ 时间档未全部达标，无法计算')

    say('=' * 92)
    say('【总不确定度（合成）】')
    say('  ⚠ 空间与时间误差**来源不同、不可简单相加**；建议按两者中**较大者**作保守带，')
    say('    或以"基准值 ± max(空间 GCI, 时间 GCI)"报出（**口径须在论文中说明**）。')
    say('  ⚠ 本项仅给**离散不确定度**；**模型外推不确定度**（低 C 端 D）另见 IN-4b。')

    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    with open(CSV, 'w', encoding='utf-8') as f:
        f.write('kind,N,dr_mm,h_in_s,t_end_h,wall_s,n_out\n')
        for r in rows:
            f.write('%s,%d,%.5f,%.6f,%.6f,%.1f,%d\n'
                    % (r['kind'], r['N'], r['dr_mm'], r['h_in'], r['t_end_h'], r['wall_s'], r['n_out']))
    say('  已写出：%s' % LOG)
    say('  已写出：%s' % CSV)


if __name__ == '__main__':
    main()
