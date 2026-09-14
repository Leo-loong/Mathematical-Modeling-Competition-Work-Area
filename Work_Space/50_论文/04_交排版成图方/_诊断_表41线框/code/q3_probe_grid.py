# -*- coding: utf-8 -*-
"""
Q3 · P1／F-C：表面加密非均匀网格 ＋ $t_{\\rm end}$ 的网格裁决
================================================================================
解决两件事：
  · **P1**：均匀网格下表面列 $C(R)$ 至 $N=640$ 仍不达 0.1%；改用**表面加密非均匀网格**
    （外层 1 mm 内几何加密）分辨薄扩散边界层。
  · **F-C**：直接量化 $t_{\\rm end}$ **自身**的网格敏感度（均匀 N=80/160/320 ＋ 非均匀档）。

统一口径：附录3；内部步 1/32 s；IMEX；事件驱动 C<0.15；熔断 120 h。
空间离散由等距推广为非等距（`q3_core_nu`，已验等距复现 ≤1e-11）。

用法：
  python q3_probe_grid.py --case u160            # 默认只声明规模
  python q3_probe_grid.py --case u160 --go       # 执行（或 ALLOW_RUN=1）
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
LOG = os.path.join(HERE, 'q3_grid_tend_log.txt')
DT_OUT, HH = 60.0, 1.0 / 32.0
NSUB = int(round(DT_OUT / HH))
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']
C_CRIT = 0.15
T_CMP = 86400.0            # 24 h（与既有网格裁决同比较时刻）

CASES = {
    'u80':  ('uniform', 80),
    'u160': ('uniform', 160),
    'u320': ('uniform', 320),
    'nu20': ('refined', 20),
    'nu26': ('refined', 26),
    'nu30': ('refined', 30),
}


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


def build(case):
    kind, p = CASES[case]
    if kind == 'uniform':
        geom = nu.geom_uniform(p, R0)
        meta = dict(s_min=float(R0 / p), s_max=float(R0 / p), q=1.0, M=0)
    else:
        geom, meta = nu.geom_refined_surface(R0, dr0=2.5e-4, region=1.0e-3, M=p)
    N = geom['N']
    r = geom['r']
    cols = [int(np.argmin(np.abs(r - k * 1e-3))) for k in range(20)] + [N]
    sel5 = [int(np.argmin(np.abs(r - k * 1e-3))) for k in (0, 5, 10, 15)] + [N]
    return kind, p, geom, meta, N, r, cols, sel5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', choices=list(CASES.keys()), required=True)
    ap.add_argument('--max-hours', type=float, default=120.0)
    ap.add_argument('--h-inner', type=float, default=1.0 / 32.0)
    ap.add_argument('--go', action='store_true')
    args = ap.parse_args()

    kind, p, geom, meta, N, r, cols, sel5 = build(args.case)
    dmin = float(np.min(geom['dP']))
    hh = float(args.h_inner)
    nsub = int(round(DT_OUT / hh))
    hh = DT_OUT / nsub
    if not (args.go or os.environ.get('ALLOW_RUN') == '1'):
        print('[SCALE] q3_probe_grid case=%s' % args.case)
        print('        节点=%d  表面最小 Δr=%.4e mm  事件驱动  熔断=%.0f h  内部步=%.6f s'
              % (N + 1, dmin * 1e3, args.max_hours, hh))
        print('        预计耗时 ≈%.0f s；**仅作网格裁决，不产交付物**。加 --go 执行。'
              % (156.8 * (N + 1) / 81.0 * (1.0 / 32.0) / hh))
        return

    ts, Tv, Cv = load_env()

    def advance(nsub_eff, T0v, C0v, t0v):
        if kind == 'uniform':
            return q3.step_imex_fast(p, R0 / p, hh, nsub_eff, R0, HC, KM,
                                     T0v, C0v, ts, Tv, Cv, t0v)
        return nu.step_imex_gen(geom, hh, nsub_eff, R0, HC, KM,
                                T0v, C0v, ts, Tv, Cv, t0v)

    T = np.full(N + 1, base.DEF2['T0'])
    C = np.full(N + 1, base.DEF2['C0'])
    nsteps_max = int(round(args.max_hours * 3600.0 / DT_OUT))
    n_cmp = int(round(T_CMP / DT_OUT))
    c24 = None
    t_end = None
    t0 = time.time()
    reached = False
    for n in range(1, nsteps_max + 1):
        t_start = (n - 1) * DT_OUT
        T_prev, C_prev = T.copy(), C.copy()
        T, C, _ = advance(nsub, T, C, t_start)
        if n == n_cmp:
            c24 = C.copy()
        if float(np.max(C)) < C_CRIT:
            reached = True
            lo, hi = 1, nsub
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = advance(mid, T_prev, C_prev, t_start)
                if float(np.max(Ca)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * hh
            _, C, _ = advance(lo, T_prev, C_prev, t_start)
            break
    wall = time.time() - t0

    lines = []
    lines.append('=' * 78)
    lines.append('Q3 · 网格裁决 case=%s' % args.case)
    lines.append('=' * 78)
    lines.append('  [SCALE] 节点=%d  表面最小 Δr=%.4e mm  q=%.5f  M=%d  内部步=%.6f s  熔断 %.0f h'
                 % (N + 1, dmin * 1e3, meta['q'], meta['M'], hh, args.max_hours))
    lines.append('  墙钟 %.1f s' % wall)
    if reached:
        lines.append('  ★ t_end = %.3f s = %.4f h（相对基线 87.4933 h：%+.4f h / %+.3f%%）'
                     % (t_end, t_end / 3600.0, t_end / 3600.0 - 87.4933,
                        100.0 * (t_end / 3600.0 - 87.4933) / 87.4933))
    else:
        lines.append('  ⚠ 未达标（%.0f h 内）；末端 C(0)=%.6f' % (args.max_hours, C[0]))
    lines.append('  末端 C(0)=%.6f  C(R)=%.6f' % (C[0], C[-1]))
    if c24 is not None:
        lines.append('  24 h 表 5 五列（0/0.5/1.0/1.5/2.0 cm）：'
                     + '  '.join('%.6f' % c24[i] for i in sel5))
    lines.append('  末端 表 5 五列（0/0.5/1.0/1.5/2.0 cm）：'
                 + '  '.join('%.6f' % C[i] for i in sel5))
    lines.append('  末端 21 输出列（每 0.1 cm）：' + ' '.join('%.4f' % C[i] for i in cols))
    if kind == 'refined':
        lines.append('  末端 表面附近 8 个节点（r/mm → C）：')
        for i in range(N - 7, N + 1):
            lines.append('      r=%.5f mm   Δr_local=%.3e mm   C=%.6f'
                         % (r[i] * 1e3, geom['dP'][i - 1] * 1e3, C[i]))
        d05 = 2.4e-3 * np.exp(-0.45 / max(C[-1], 1e-6)) * np.exp(-3850.0 / 323.15) / KM
        lines.append('  末端 δ(C_R)/Δr_surface = %.3e / %.3e = %.1f'
                     % (d05, dmin, d05 / dmin))
    txt = '\n'.join(lines)
    print(txt)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(txt + '\n\n')
    print('已追加：%s' % LOG)


if __name__ == '__main__':
    main()
