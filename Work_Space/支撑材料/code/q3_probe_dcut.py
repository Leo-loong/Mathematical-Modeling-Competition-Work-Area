# -*- coding: utf-8 -*-
"""
Q3 · P2 低 C 端 D 公式外推对照：在 C=C_frz 处"冻结" D
================================================================================
做法：D_trunc(C,T) = D(max(C, C_frz), T)（`q3_core_nu._D_frz_nb`）。
  · C_frz = 0  ⟹ 与原式完全一致（对照基线，$t_{\\rm end}=87.4933$ h）；
  · C_frz > 0  ⟹ 低含水率端 D 不再随 C 继续骤降 ⟹ 干燥更快 ⟹ $t_{\\rm end}$ 缩短。
含义：刻画"附录3 的 D 在低 C 端被外推到多远"，作为 H10／RK-Q3-1 的**适用边界量化**。

⚠ 仅作适用边界说明，**不改变**正式结果（正式结果用原式，无截断）。

用法：
  python q3_probe_dcut.py --c-frz 0.3            # 默认只声明规模
  python q3_probe_dcut.py --c-frz 0.3 --go       # 执行（或 ALLOW_RUN=1）
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
import q3_core_nu as nu                                             # noqa: E402

WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
LOG = os.path.join(HERE, 'q3_probe_dcut_log.txt')
N, DR = 80, 2.5e-4
DT_OUT, HH = 60.0, 1.0 / 32.0
NSUB = int(round(DT_OUT / HH))
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']
C_CRIT = 0.15


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


def run(c_frz, max_hours):
    ts, Tv, Cv = load_env()
    g = nu.geom_uniform(N, R0)
    T = np.full(N + 1, base.DEF2['T0'])
    C = np.full(N + 1, base.DEF2['C0'])
    nsteps_max = int(round(max_hours * 3600.0 / DT_OUT))
    t0 = time.time()
    for n in range(1, nsteps_max + 1):
        t_start = (n - 1) * DT_OUT
        T_prev, C_prev = T.copy(), C.copy()
        T, C, _ = nu.step_imex_gen(g, HH, NSUB, R0, HC, KM, T, C, ts, Tv, Cv,
                                   t_start, c_frz=c_frz)
        if float(np.max(C)) < C_CRIT:
            lo, hi = 1, NSUB
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = nu.step_imex_gen(g, HH, mid, R0, HC, KM,
                                            T_prev, C_prev, ts, Tv, Cv, t_start, c_frz=c_frz)
                if float(np.max(Ca)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * HH
            _, Cx, _ = nu.step_imex_gen(g, HH, lo, R0, HC, KM,
                                        T_prev, C_prev, ts, Tv, Cv, t_start, c_frz=c_frz)
            return t_end, float(Cx[0]), float(Cx[-1]), time.time() - t0, n, ''
    return None, float(C[0]), float(C[-1]), time.time() - t0, nsteps_max, \
        '未达标（%.0f h 内）' % max_hours


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--c-frz', type=float, required=True)
    ap.add_argument('--max-hours', type=float, default=120.0)
    ap.add_argument('--go', action='store_true')
    args = ap.parse_args()
    if not (args.go or os.environ.get('ALLOW_RUN') == '1'):
        print('[SCALE] q3_probe_dcut 规模声明：')
        print('        C_frz=%.3f  事件驱动  熔断=%.0f h  N=%d（Δr=%.2f mm）'
              % (args.c_frz, args.max_hours, N, DR * 1e3))
        print('        预计耗时 ≤157 s（冻结使干燥更快）；**仅作适用边界，不产交付物**。加 --go 执行。')
        return

    D_frz = 2.4e-3 * np.exp(-0.45 / max(args.c_frz, 1e-9)) * np.exp(-3850.0 / 323.15)
    lines = []
    lines.append('=' * 78)
    lines.append('Q3 · P2 低 C 端 D 冻结对照：C_frz=%.3f' % args.c_frz)
    lines.append('=' * 78)
    lines.append('  [SCALE] N=%d  Δr=%.2f mm  内部步=1/32 s  判据 C<%.2f  熔断 %.0f h'
                 % (N, DR * 1e3, C_CRIT, args.max_hours))
    lines.append('  D(C_frz, 323.15K) = %.4e m²/s' % D_frz)
    # 与理论无截断值对照
    D_un = 2.4e-3 * np.exp(-0.45 / 0.052) * np.exp(-3850.0 / 323.15)
    D_un15 = 2.4e-3 * np.exp(-0.45 / 0.15) * np.exp(-3850.0 / 323.15)
    lines.append('  参考：D(0.052)=%.3e；D(0.15)=%.3e m²/s（截断后低 C 端不再低于 D(C_frz)）'
                 % (D_un, D_un15))
    te, c0, cr, wall, nlast, note = run(args.c_frz, args.max_hours)
    if te is not None:
        lines.append('  ★ t_end = %.3f s = %.4f h（基准 87.4933 h，变化 %+.4f h / %+.2f%%）'
                     % (te, te / 3600.0, te / 3600.0 - 87.4933,
                        100.0 * (te / 3600.0 - 87.4933) / 87.4933))
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
