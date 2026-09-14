# -*- coding: utf-8 -*-
"""
Q3 · P3 判据敏感度探测：$t_{\\rm end}$ 对达标判据 $C_{\\rm crit}$ 的依赖
================================================================================
口径（除 $C_{\\rm crit}$ 外**全部与主力一致**）：
  · 物性附录3；Δr=0.25 mm（N=80）；内部步 1/32 s；IMEX；边界 H6／N19／N20；
  · 事件驱动：全域 max_r C < C_crit 即停；
  · **边界探测档熔断上界 160 h**（主求解为 120 h，此处放宽以区分"更慢"与"永不达标"）；
  · 达标时刻在**输出步内做二分定位**（步长 1/32 s），与主力同法。

⚠ 本脚本产出**仅作敏感度**；正式答案仍为 $C_{\\rm crit}=0.15$ 的 $t_{\\rm end}$。

用法：
  python q3_probe_crit.py --c-crit 0.18            # 默认只声明规模
  python q3_probe_crit.py --c-crit 0.18 --go       # 执行（或 ALLOW_RUN=1）
"""
import sys
import os
import time
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))

import openpyxl                                                     # noqa: E402
import q2_core_c as base                                            # noqa: E402
import q3_core as q3                                                # noqa: E402

WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
LOG = os.path.join(HERE, 'q3_probe_crit_log.txt')
N, DR = 80, 2.5e-4
DT_OUT, HH = 60.0, 1.0 / 32.0
NSUB = int(round(DT_OUT / HH))
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']


def load_env():
    wb = openpyxl.load_workbook(ATT1, data_only=True)
    ws = wb.active
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in d])
    T = np.array([float(r[1]) for r in d])
    C = np.array([float(r[2]) for r in d])
    wb.close()
    return q3.env_tables_from_att1(t, T, C)


def run(c_crit, max_hours):
    """事件驱动推进，返回 (t_end_s or None, C0_end, CR_end, wall, nsteps, note)。"""
    ts, Tv, Cv = load_env()
    T = np.full(N + 1, base.DEF2['T0'])
    C = np.full(N + 1, base.DEF2['C0'])
    nsteps_max = int(round(max_hours * 3600.0 / DT_OUT))
    t0 = time.time()
    for n in range(1, nsteps_max + 1):
        t_start = (n - 1) * DT_OUT
        T_prev, C_prev = T.copy(), C.copy()
        T, C, _ = q3.step_imex_fast(N, DR, HH, NSUB, R0, HC, KM, T, C,
                                    ts, Tv, Cv, t_start)
        if float(np.max(C)) < c_crit:
            lo, hi = 1, NSUB
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = q3.step_imex_fast(N, DR, HH, mid, R0, HC, KM,
                                             T_prev, C_prev, ts, Tv, Cv, t_start)
                if float(np.max(Ca)) < c_crit:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * HH
            _, Cx, _ = q3.step_imex_fast(N, DR, HH, lo, R0, HC, KM,
                                         T_prev, C_prev, ts, Tv, Cv, t_start)
            return t_end, float(Cx[0]), float(Cx[-1]), time.time() - t0, n, ''
    return None, float(C[0]), float(C[-1]), time.time() - t0, nsteps_max, \
        '未达标（%.0f h 内）' % max_hours


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--c-crit', type=float, required=True)
    ap.add_argument('--max-hours', type=float, default=160.0)
    ap.add_argument('--go', action='store_true')
    args = ap.parse_args()
    if not (args.go or os.environ.get('ALLOW_RUN') == '1'):
        print('[SCALE] q3_probe_crit 规模声明：')
        print('        C_crit=%.3f  时程=事件驱动  熔断=%.0f h  网格 N=%d（Δr=%.2f mm）'
              % (args.c_crit, args.max_hours, N, DR * 1e3))
        print('        预计耗时 100–240 s；**仅作敏感度，不产交付物**。加 --go 执行。')
        return

    lines = []
    lines.append('=' * 78)
    lines.append('Q3 · P3 判据敏感度：C_crit=%.3f（熔断 %.0f h）' % (args.c_crit, args.max_hours))
    lines.append('=' * 78)
    lines.append('  [SCALE] N=%d  Δr=%.2f mm  内部步=1/32 s  判据 C<%.3f（严格小于）'
                 % (N, DR * 1e3, args.c_crit))
    te, c0, cr, wall, nlast, note = run(args.c_crit, args.max_hours)
    if te is not None:
        lines.append('  ★ t_end = %.3f s = %.4f h（第 %d 个输出步内定位）' % (te, te / 3600.0, nlast))
        lines.append('  末端 C(0)=%.6f  C(R)=%.6f' % (c0, cr))
    else:
        lines.append('  ⚠ %s；末端 C(0)=%.6f  C(R)=%.6f' % (note, c0, cr))
    lines.append('  墙钟 %.1f s' % wall)
    txt = '\n'.join(lines)
    print(txt)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(txt + '\n\n')
    print('已追加：%s' % LOG)


if __name__ == '__main__':
    main()
