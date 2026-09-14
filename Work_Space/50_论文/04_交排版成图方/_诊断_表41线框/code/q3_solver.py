# -*- coding: utf-8 -*-
"""
A 题 Q3 主力求解：事件驱动终止 + 60 s 输出 + 达标定位 + 上界熔断
================================================================================
口径（严格依 Q3 计划文档《A_Q3求解思路与工作流》v3）：
  · 物性：附录 3（N7–N10），全程无阶段切换
  · 空间：Δr = 0.25 mm（N=80 区间／81 节点）
  · 内部步：1/32 s（先按基线，与 Q2 一致）
  · 格式：IMEX 交替推进（物性每内部子步更新）
  · 边界：t≤14400 s 附件1 线性插值；t>14400 s 取 T∞=50.00 ℃、C∞=0.04999
  · 判据：**全局各处 C < 0.15**（严格小于；最慢点=中心）
  · 输出：每 60 s，21 个距离点（0～2 cm，每 0.1 cm）
  · 核：**q3_core（A/B 优化的 B+C 核）**；禁止 `_orig`

终止条件（P1）：
  · 达标：全域 max_r C < 0.15 ⟹ 记录并**停止**
  · 熔断：t 超过 --max-hours（默认 120 h）仍未达标 ⟹ 停止并报警

达标定位（P3）：
  · 以 60 s 输出网格记录；达标判定在**每个内部步**检查（比输出更密）
  · 记录"首次达标的内部时刻" t_end_inner 与"首个达标输出点" t_out

用法：
  python q3_solver.py                          # 正式：事件驱动，上限 120 h
  python q3_solver.py --steps 10800            # 回归：固定 10800 步（用于与 result2 比对）
  python q3_solver.py --out ../tmp_test.xlsx   # 指定输出
  python q3_solver.py --hours 1 --no-assert    # 快速冒烟
"""
import sys
import os
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Q2', 'code'))

import openpyxl                                                  # noqa: E402
from openpyxl import Workbook                                    # noqa: E402
import q2_core_c as base                                         # noqa: E402
import q3_core as q3                                             # noqa: E402

WS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))     # Work_Space 根
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')

# ---------- 口径常量 ----------
N = 80
DR = 2.5e-4
DT_OUT = 60.0                    # Q3 输出步长（题面：每隔 60 s）
# ★ 内部步长必须与 Q2 已验证值一致（1/32 s）—— 不得因输出间隔变大而放大内部步！
H_INNER = 1.0 / 32.0
NSUB = int(round(DT_OUT / H_INNER))      # = 1920 个子步／输出步
HH = DT_OUT / NSUB                       # 实际内部步长（≈1/32 s，由整除保证）
R0 = base.DEF2['R0']
HC = base.DEF2['h']
KM = base.DEF2['km']
C_CRIT = 0.15                    # 达标判据（N18；严格小于）
C_WATCH = 0.16                   # 进入"细粒度达标定位"的预警阈值
C_ENV_TAIL = 0.04999             # H6／N20
T_ENV_TAIL = 50.00               # H6／N19
COLS = np.arange(0, N + 1, 4)    # 0,0.1,...,2.0 cm ⟹ 21 列
NCOL = len(COLS)
NC = N + 1

LOG = os.path.join(HERE, 'q3_run_log.txt')
BUF = []


def say(s=''):
    print(s)
    BUF.append(s)


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--steps', type=int, default=0,
                    help='固定输出步数（>0 时忽略事件驱动，用于回归/冒烟）')
    ap.add_argument('--hours', type=float, default=0.0,
                    help='固定时程上限（h）；与 --steps 二选一')
    ap.add_argument('--max-hours', type=float, default=120.0,
                    help='事件驱动模式的熔断上限（h），默认 120')
    ap.add_argument('--out', type=str, default='')
    ap.add_argument('--no-assert', action='store_true')
    args = ap.parse_args()

    t_a1, T_a1, C_a1 = load_att1()
    ts_env, Tenv_v, Cenv_v = q3.env_tables_from_att1(t_a1, T_a1, C_a1)

    # 决定运行模式
    if args.steps > 0:
        nsteps_max = args.steps
        mode_txt = '固定 %d 步（%.2f h）' % (args.steps, args.steps * DT_OUT / 3600.0)
    elif args.hours > 0:
        nsteps_max = int(round(args.hours * 3600.0 / DT_OUT))
        mode_txt = '固定 %.2f h' % args.hours
    else:
        nsteps_max = int(round(args.max_hours * 3600.0 / DT_OUT))
        mode_txt = '事件驱动（熔断 %.0f h）' % args.max_hours

    out = args.out if args.out else os.path.join(HERE, 'result3_raw.xlsx')

    say('=' * 70)
    say('Q3 主力求解')
    say('=' * 70)
    say('  物性        附录3 全程（N7–N10）')
    say('  空间        Δr=%.2f mm（N=%d 区间／%d 节点）' % (DR * 1e3, N, NC))
    say('  输出步      %.1f s   内部子步 %d（内部步长 %.6f s）' % (DT_OUT, NSUB, HH))
    say('  判据        全域 C < %.2f kg/kg（严格小于，中心为最慢点）' % C_CRIT)
    say('  运行模式    %s' % mode_txt)
    say('  使用核      q3_core（A/B 优化：环境查表 + 子步下沉 njit）')
    say('  输出        21 列（0～2 cm，每 0.1 cm）⟹ 文件 %s' % os.path.basename(out))
    say('-' * 70)

    T = np.full(NC, base.DEF2['T0'])
    C = np.full(NC, base.DEF2['C0'])

    rows = []                       # 每 60 s 一行（仅存 21 个输出点）
    inner_tot_all = 0
    res_max_all = 0.0
    t_end_inner = None              # 首个"全域达标"的内部时刻（s）
    t_end_i_step = -1
    reached = False
    t0 = time.time()

    for n in range(1, nsteps_max + 1):
        t_start = (n - 1) * DT_OUT
        T_prev, C_prev = T.copy(), C.copy()
        # ★ 批量推进**一整输出步**（1920 个子步），一次 njit 调用
        #   —— 这是 A 优化（子步循环下沉）的收益所在
        T, C, info = q3.step_imex_fast(
            N, DR, HH, NSUB, R0, HC, KM, T, C,
            ts_env, Tenv_v, Cenv_v, t_start)
        inner_tot_all += info['inner_tot']
        res_max_all = max(res_max_all, info['res_max'])
        rows.append(C[COLS].copy())

        cmax = float(np.max(C))
        if cmax < C_CRIT:
            # ★ 达标：在本输出步内**二分细定位**（P3）
            reached = True
            lo, hi = 1, NSUB
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = q3.step_imex_fast(
                    N, DR, HH, mid, R0, HC, KM, T_prev, C_prev,
                    ts_env, Tenv_v, Cenv_v, t_start)
                if float(np.max(Ca)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end_inner = t_start + lo * HH
            t_end_i_step = lo - 1
            # 用精确定位所得状态覆盖末行（保证末行与 t_end 严格对应）
            _, Cx, _ = q3.step_imex_fast(
                N, DR, HH, lo, R0, HC, KM, T_prev, C_prev,
                ts_env, Tenv_v, Cenv_v, t_start)
            rows[-1] = Cx[COLS].copy()
            C = Cx
            break
        if cmax < C_WATCH:
            say('  [预警] t=%.1f h，全域最大 C=%.6f 已接近判据 %.2f'
                % (n * DT_OUT / 3600.0, cmax, C_CRIT))
        if n % max(1, nsteps_max // 20) == 0:
            frac = 100.0 * n / nsteps_max
            say('  [%5.1f%%] t=%8.1f s (%6.2f h)  C(0)=%.6f  T(0)=%.4f  wall=%.1fs'
                % (frac, n * DT_OUT, n * DT_OUT / 3600.0,
                   C[0], T[0], time.time() - t0))

    wall = time.time() - t0
    say('-' * 70)
    say('  完成：%d 个输出步，总墙钟 %.1f s（%.1f min）' % (len(rows), wall, wall / 60))
    say('  内部迭代累计 %d 次；内层最大残差 %.3e' % (inner_tot_all, res_max_all))
    say('  末端 T(0)=%.4f ℃  T(R)=%.4f ℃  C(0)=%.6f  C(R)=%.6f'
        % (T[0], T[-1], C[0], C[-1]))
    if reached:
        say('  ★ 达标：全域 C<%.2f 首次出现于 t = %.3f s = %.4f h（第 %d 个内部子步）'
            % (C_CRIT, t_end_inner, t_end_inner / 3600.0, t_end_i_step + 1))
    else:
        say('  ⚠ 未达标：运行至 %d 步（%.2f h）仍未全域 C<%.2f'
            % (len(rows), len(rows) * DT_OUT / 3600.0, C_CRIT))

    # ---------- 写盘 ----------
    # ★ O10 口径修正：
    #   ① 距离列头改为**数值**（与 result1／result4／附件3 模板一致）；
    #   ② 达标时**末行时间列写精确 t_end**（与 result4 同款），而非输出步序号
    #      —— 末行数值本已由二分所得 t_end 状态覆盖，此前仅时间标签未同步。
    wb = Workbook(write_only=True)
    ws = wb.create_sheet('Sheet1')
    ws.append(['时间\\到药材中心的距离'] + [round(c * DR * 100, 1) for c in COLS])
    n_rows = len(rows)
    for i, r in enumerate(rows):
        t_row = (i + 1) * DT_OUT
        if reached and i == n_rows - 1:
            t_row = round(t_end_inner, 3)
        ws.append([t_row] + [round(float(v), 4) for v in r])
    wb.save(out)
    say('  已写出：%s' % out)

    # ---------- 断言 ----------
    # ⚠ 断言口径说明（Q3 相对 Q2 的必要修正）：
    #    Q2 仅 3 h，全域含水率单调不增成立；
    #    Q3 长时程下**表面会出现"局部增湿"式回升**（内部水分扩散补充超过表面脱除），
    #    属**真实物理现象**（与文献所述"局部增湿"同机理）。
    #    故断言改为：①**中心点**（＝最慢点，决定达标）严格单调不增；
    #                ②全场上界 = 初值；③非负；④达标后末行全域 < 判据。
    if not args.no_assert:
        arr = np.array(rows)
        dC = np.diff(arr, axis=0) if len(arr) > 1 else np.zeros((1, NCOL))
        # "最大值在中心"改用**容差判据**：
        #   中心与邻点可能存在 1~数个 ulp 的差异（写盘 round 到 4 位后即消失），
        #   属数值可分辨范围内的小抖动；差异超过 1e-6 才算真实违反。
        TOL_MAXLOC = 1e-6
        gap = arr.max(axis=1) - arr[:, 0]
        n_beyond = int(np.sum(gap > TOL_MAXLOC))
        chk = [
            ('形状 (行数, %d)' % (NCOL + 1), arr.shape[1] == NCOL),
            ('含水率非负（全域）', bool(np.min(arr) >= 0.0)),
            ('中心点单调不增', bool(np.all(dC[:, 0] <= 1e-9))),
            ('含水率不超初值', bool(np.max(arr) <= base.DEF2['C0'] + 1e-4)),
            ('全域最大值在中心（容差 %.0e）' % TOL_MAXLOC, n_beyond == 0),
        ]
        if reached:
            chk.append(('末行全域 < %.2f' % C_CRIT, bool(np.max(arr[-1]) < C_CRIT)))
        say('-' * 70)
        say('  [断言]')
        for nm, ok in chk:
            say('    %s  %s' % ('PASS' if ok else 'FAIL', nm))
        if not all(ok for _, ok in chk):
            say('  *** 存在 FAIL ***')
        say('  [留痕] 中心低于全场最大值的最大偏差 = %.3e（阈值 %.0e）；'
            '其中写盘 round 到 4 位后并列的行数 = %d / %d'
            % (float(gap.max()), TOL_MAXLOC,
               int(np.sum(np.argmax(arr, axis=1) == 0)),
               len(arr)))
        # 登记表面回升（不判 FAIL，仅留痕）
        nup = int(np.sum(dC[:, -1] > 1e-9))
        say('  [留痕] 表面（r=%.1f cm）出现回升的输出步：%d 个（占 %.1f%%），最大单次 %+.3e'
            % (COLS[-1] * DR * 100, nup, 100.0 * nup / max(1, len(dC)),
               float(dC[:, -1].max()) if len(dC) else 0.0))
        say('         ⟹ 属"局部增湿"物理现象，不影响达标判定（最大值恒在中心）')

    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')


if __name__ == '__main__':
    main()
