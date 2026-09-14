# -*- coding: utf-8 -*-
"""
IN-1 | 自适应时间步 + **后验误差控制**（创新副本 · 不改动任何正式产物）
================================================================================
动机（kb 依据）：《摘要_IMEX-BDF2 后验误差估计与自适应时间步》指出——
  "**自适应必须有误差判据，不能凭变化率拍脑袋**"；本项目 Q2 的自适应判据是工程启发式。
本实现给出**严格后验误差判据**：

  · 格式：仍用现有 IMEX 核（后向欧拉一阶，**不改离散格式**）——零格式风险；
  · 每步做 **Richardson（半步）后验误差估计**：
        u(dt)  一次推进
        u(dt/2) 两次半步推进
        est = max|u(dt) - u(dt/2)| / max(1, max|u(dt/2)|)      （相对量）
    一阶格式 ⟹ 半步解 ≈ 真解 + C1*dt/2 ⟹ est ≈ |C1|*dt/2，可作为局部误差估计；
  · **PI 式步长控制**：dt_new = dt * safety * sqrt(tol / est)，限制在 [0.5dt, 2dt]；
  · **步长上限 dt_max**；并**强制在 60 s 输出边界对齐**（保证输出网格与正式口径一致，免插值）；
  · **Rannacher 式保护**：起步用 dt0 = 1/32 s（与正式口径同起点）；
  · 事件驱动 + 步内二分定位（与主力同逻辑，定位用固定 1/32 s 细分）。

产物（带副本标记）：
  innov/out/result3_INV1.xlsx          （60 s × 21 列，格式与 result3.xlsx 一致）
  innov/logs/q3_INV1_adaptive.log
  innov/out/fig_q3_INV1_stepsize.csv   （步长轨迹：t_h, dt_s, est, n_accepted）

用法：
  python q3_solver_INV1.py --smoke        # 冒烟：上限 1 h（不达标）
  python q3_solver_INV1.py                # 正式：事件驱动至达标（预计 1–3 min）
  python q3_solver_INV1.py --tol 1e-5     # 更严容差
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
from openpyxl import Workbook


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))          # .../Q3/innov
Q3DIR = os.path.dirname(HERE)
WS = _find_root(HERE)
sys.path.insert(0, Q3DIR)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))

import q3_core as q3                                       # noqa: E402
import q2_core_c as base                                   # noqa: E402

ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
C_CRIT = 0.15
DT_OUT = 60.0
N = 80
DR = 2.5e-4
H0 = 1.0 / 32.0            # 起步步长（与正式口径一致）
DT_MIN = 1.0 / 2048.0
DT_MAX = 60.0
R0, HC, KM = base.DEF2['R0'], base.DEF2['h'], base.DEF2['km']
NC = N + 1
COLS = np.arange(0, N + 1, 4)

LOGDIR = os.path.join(HERE, 'logs')
OUTDIR = os.path.join(HERE, 'out')
os.makedirs(LOGDIR, exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)
LOG = os.path.join(LOGDIR, 'q3_INV1_adaptive.log')
CSV = os.path.join(OUTDIR, 'fig_q3_INV1_stepsize.csv')
XLSX = os.path.join(OUTDIR, 'result3_INV1.xlsx')

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


def adv(T, C, t0, dt, nsub):
    """推进 dt（分成 nsub 个子步）；返回 (T, C)"""
    return q3.step_imex_fast(N, DR, dt / nsub, nsub, R0, HC, KM, T, C,
                             ts, Tv, Cv, t0)[:2]


ts = Tv = Cv = None


def main():
    global ts, Tv, Cv, adv_prev_state
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--tol', type=float, default=5e-5, help='相对后验误差容差')
    ap.add_argument('--safety', type=float, default=0.9)
    ap.add_argument('--max-hours', type=float, default=120.0)
    ap.add_argument('--out', type=str, default='', help='结果文件（默认 out/result3_INV1.xlsx）')
    args = ap.parse_args()

    t_a1, T_a1, C_a1 = load_att1()
    ts, Tv, Cv = q3.env_tables_from_att1(t_a1, T_a1, C_a1)

    t_max = 1.0 * 3600.0 if args.smoke else args.max_hours * 3600.0
    say('=' * 84)
    say('IN-1 | 自适应时间步 + Richardson 后验误差控制（创新副本）')
    say('=' * 84)
    say('[SCALE] N=%d Δr=%.2f mm  起步 dt0=%.6f s  dt∈[%.6f, %.1f] s  容差 tol=%.1e  上限 %.1f h'
        % (N, DR * 1e3, H0, DT_MIN, DT_MAX, args.tol, t_max / 3600.0))
    say('        格式沿用 IMEX（后向欧拉）——**零格式改动**；自适应仅改"步长如何选"')

    T = np.full(NC, base.DEF2['T0'])
    C = np.full(NC, base.DEF2['C0'])
    adv_prev_state = (T.copy(), C.copy())      # 本步起点状态（达标时二分定位用）

    t = 0.0
    dt = H0
    rows = []
    trace = []                 # (t_h, dt, est, n_acc)
    n_accept = 0
    n_reject = 0
    t_wall = time.time()
    t_end = None
    last_out_t = 0.0

    while t < t_max - 1e-12:
        # 对齐 60 s 输出边界
        rem = DT_OUT - (t % DT_OUT)
        if rem <= 1e-9:
            rem = DT_OUT
        dt_try = min(dt, rem, DT_MAX)

        accepted = False
        while not accepted:
            dt_try = min(dt, rem, DT_MAX)
            T1, C1 = adv(T, C, t, dt_try, 1)
            T2, C2 = adv(T, C, t, dt_try, 2)
            denC = max(1.0, float(np.max(np.abs(C2))))
            denT = max(1.0, float(np.max(np.abs(T2))))
            estC = float(np.max(np.abs(C1 - C2))) / denC
            estT = float(np.max(np.abs(T1 - T2))) / denT
            est = max(estC, estT)
            if est <= args.tol or dt_try <= DT_MIN * 1.0000001:
                accepted = True
                T, C = T2, C2
                t_new = t + dt_try
                n_accept += 1
                if est > 1e-30:
                    dt = dt_try * args.safety * np.sqrt(args.tol / est)
                else:
                    dt = dt_try * 2.0
                dt = min(max(dt, dt_try * 0.5), dt_try * 2.0)
                dt = min(max(dt, DT_MIN), DT_MAX)
                trace.append((t_new / 3600.0, dt_try, est, n_accept))
            else:
                n_reject += 1
                dt = max(dt_try * 0.5, DT_MIN)

        # 记录 60 s 输出点
        while t_new >= last_out_t + DT_OUT - 1e-9:
            last_out_t += DT_OUT
            rows.append(C[COLS].copy())
            if last_out_t % 3600.0 == 0:
                say('  t=%6.2f h  dt=%8.5f s  est=%.2e  acc=%-6d rej=%-5d wall=%.1fs  C(0)=%.6f'
                    % (last_out_t / 3600.0, dt_try, est, n_accept, n_reject,
                       time.time() - t_wall, float(C[0])))

        t = t_new

        # 达标检测（全域）
        if float(np.max(C)) < C_CRIT:
            # 在最后一个自适应步内用固定 1/32 s 细分做二分定位
            t_start = t - dt_try
            # 重算该步起点状态
            Tb, Cb = adv_prev_state
            nsub_tot = max(1, int(round(dt_try / H0)))
            lo, hi = 1, nsub_tot
            while lo < hi:
                mid = (lo + hi) // 2
                Tc, Cc = q3.step_imex_fast(N, DR, H0, mid, R0, HC, KM, Tb, Cb,
                                           ts, Tv, Cv, t_start)[:2]
                if float(np.max(Cc)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * H0
            Tf, Cf = q3.step_imex_fast(N, DR, H0, lo, R0, HC, KM, Tb, Cb,
                                       ts, Tv, Cv, t_start)[:2]
            C = Cf
            rows[-1] = C[COLS].copy()
            say('  ★ 达标：t = %.3f s = %.4f h（自适应步内二分，精度 1/32 s）'
                % (t_end, t_end / 3600.0))
            break
        adv_prev_state = (T.copy(), C.copy())

    wall = time.time() - t_wall
    say('-' * 84)
    say('  完成：接受 %d 步、拒绝 %d 步；总墙钟 %.1f s（%.1f min）' % (n_accept, n_reject, wall, wall / 60))
    say('  步长范围：%.6f – %.4f s（放大倍率 %.1f×）'
        % (min(x[1] for x in trace), max(x[1] for x in trace),
           max(x[1] for x in trace) / H0))
    say('  最大后验误差 est_max = %.3e（容差 %.1e）' % (max(x[2] for x in trace), args.tol))

    # 写结果（仅在正式模式）
    if not args.smoke:
        xlsx = args.out if args.out else XLSX
        wb = Workbook(write_only=True)
        ws = wb.create_sheet('Sheet1')
        ws.append(['时间\\到药材中心的距离'] + ['%.1f' % (c * DR * 100) for c in COLS])
        for i, r in enumerate(rows):
            ws.append([(i + 1) * DT_OUT] + [round(float(v), 4) for v in r])
        wb.save(xlsx)
        say('  已写出：%s（%d 行 × %d 列）' % (xlsx, len(rows), len(COLS) + 1))

        with open(CSV, 'w', encoding='utf-8') as f:
            f.write('t_h,dt_s,est_rel,n_accept\n')
            for a, b, c, d in trace:
                f.write('%.6f,%.8f,%.6e,%d\n' % (a, b, c, d))
        say('  已写出：%s（%d 个接受步）' % (CSV, len(trace)))

        arr = np.array(rows)
        dC = np.diff(arr, axis=0)
        chk = [('形状 (行数, %d)' % len(COLS), arr.shape[1] == len(COLS)),
               ('含水率非负（全域）', bool(np.min(arr) >= 0.0)),
               ('中心点单调不增', bool(np.all(dC[:, 0] <= 1e-9))),
               ('含水率不超初值', bool(np.max(arr) <= base.DEF2['C0'] + 1e-4))]
        if t_end is not None:
            chk.append(('末行全域 < %.2f' % C_CRIT, bool(np.max(arr[-1]) < C_CRIT)))
        say('  [断言]')
        for nm, ok in chk:
            say('    %s  %s' % ('PASS' if ok else 'FAIL', nm))

    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    say('  已写出：%s' % LOG)


adv_prev_state = (None, None)

if __name__ == '__main__':
    main()
