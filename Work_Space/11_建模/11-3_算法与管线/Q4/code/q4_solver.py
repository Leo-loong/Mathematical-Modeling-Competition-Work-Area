# -*- coding: utf-8 -*-
"""
A 题 Q4 主力求解（事件驱动 + 子步级二分 + 熔断）
================================================================================
[SCALE] 正式求解（T3）：时程 0 -> t_dry（事件终止，熔断 240 h）；
  N=160（Δξ=1/160）、n_sub=32（内部步 1/32 s）、t_corr=1（D6 方案 b）、
  IMEX + Picard(ω=0.7, tol=1e-10, maxit=30)；预计墙钟 30-70 min。
  授权：用户指令（2026-09-11）"不再有明确的正式放行门禁，可以直接跑主求解程序"；
  申请单见《A_Q4求解思路与工作流》§5.6（已按本轮指令更新为已批准）。
用法：python q4_solver.py          -> 只打印 [SCALE] 并退出
      python q4_solver.py --go     -> 实际执行
输出：results/result4.xlsx + results/result4_data.csv；日志 logs/q4_solve_log.txt；
  进度 logs/q4_solve_progress.txt（供后台轮询）。
口径：判据 max_r C < 0.15（严格）；result4 = 60 s x (0..1.9 cm + 药材表面)，
  r>R(t) 留空（O4）；t_dry 非 60 s 整数倍时追加精确行（MB-21/O10）。
"""
import sys, os, time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))

import numpy as np
import openpyxl
import q4_core as qc

RES = os.path.join(HERE, '..', 'results')
LOG = os.path.join(HERE, '..', 'logs')
os.makedirs(RES, exist_ok=True)
os.makedirs(LOG, exist_ok=True)
LOGF = os.path.join(LOG, 'q4_solve_log.txt')
PROG = os.path.join(LOG, 'q4_solve_progress.txt')

N = 160
NSUB = 32
DT_OUT = 1.0
CC = 0.15                 # 判据（严格小于）
BREAK_H = 240.0           # 熔断（h）
R_TOL = 1e-12

rep = []


def log(s=''):
    rep.append(s)
    try:
        print(s.encode('ascii', 'replace').decode('ascii'))
    except Exception:
        pass


def flush():
    open(LOGF, 'w', encoding='utf-8').write('\n'.join(rep))


def prog(s):
    open(PROG, 'w', encoding='utf-8').write(s)


log('[SCALE] Q4 formal solve (T3): horizon 0->t_dry (event, breaker %.0f h)' % BREAK_H)
log('[SCALE] N=%d, n_sub=%d, t_corr=1, IMEX+Picard(0.7,1e-10,30)' % (N, NSUB))
log('[SCALE] est wall 30-70 min; output result4.xlsx (60s x 21col+surface)')
if '--go' not in sys.argv:
    log('[SCALE] --go not given -> exit (gate closed)')
    flush()
    sys.exit(0)

t_start = time.perf_counter()
prog('running: init')

# ---- 数据装载 ----
ts_env, Tv, Cv = None, None, None
att1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')
wb = openpyxl.load_workbook(att1, read_only=True, data_only=True)
ws = wb[wb.sheetnames[0]]
# ★修复：isinstance 过滤已剔除表头，原 [1:] 误删 t=0 行（首分钟环境钳位偏移）
rr = [(float(a), float(b), float(c)) for a, b, c in ws.iter_rows(values_only=True)
      if a is not None and not isinstance(a, str)]
t1 = np.array([x[0] for x in rr])
T1v = np.array([x[1] for x in rr])
C1v = np.array([x[2] for x in rr])
ts_env, Tv, Cv = qc.env_tables_from_att1(t1, T1v, C1v)
log('att1: %d pts, T %.3f-%.3f C, Cinf %.5f-%.5f' %
    (len(t1), T1v.min(), T1v.max(), C1v.min(), C1v.max()))
TENVM = float(T1v.max())

ts_R, Rv = qc.load_R_table(os.path.join(WS, '10_赛题', 'A题', '附件', '附件2.xlsx'))


def Rof(t):
    return float(np.interp(t, ts_R, Rv))


# 模板表头
att3 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件3', 'result4.xlsx')
wbt = openpyxl.load_workbook(att3, read_only=True)
hrow = list(wbt[wbt.sheetnames[0]].iter_rows(min_row=1, max_row=1, values_only=True))[0]
HEADER = ['时间\\到药材中心的距离'] + [round(0.1 * i, 1) for i in range(20)] + ['药材表面']
log('template header ok (last col = %r)' % (hrow[-1],))

# ---- 主循环 ----
dxi = 1.0 / N
hsub = DT_OUT / NSUB
T = np.full(N + 1, qc.DEF4['T0'])
C = np.full(N + 1, qc.DEF4['C0'])
rows60 = []                 # (t, T.copy(), C.copy())
t_dry = None
dry_field = None
prev_T, prev_C, prev_t = T.copy(), C.copy(), 0.0
max_steps = int(BREAK_H * 3600 / DT_OUT)
tot_it = 0
rm_all = 0.0
t_all = time.perf_counter()

k = 0
while k < max_steps:
    k += 1
    t0 = (k - 1) * DT_OUT
    T, C, info = qc.step_imex4(N, dxi, hsub, NSUB, qc.DEF4['R0'], qc.DEF4['h'],
                               qc.DEF4['km'], T, C, t0, ts_env, Tv, Cv,
                               ts_R, Rv, t_corr=1)
    tot_it += info['inner_tot']
    if info['res_max'] > rm_all:
        rm_all = info['res_max']
    tk = k * DT_OUT
    if k % 60 == 0:
        rows60.append((tk, T.copy(), C.copy()))
    if C.max() < CC:
        t_dry = tk
        dry_field = (T.copy(), C.copy())
        log('event: max C < 0.15 at t=%d s (step %d)' % (tk, k))
        break
    prev_T, prev_C, prev_t = T.copy(), C.copy(), tk
    if k % 600 == 0:
        el = time.perf_counter() - t_all
        msg = 'running: step %d/%d?  t=%.1f h  C(0)=%.4f  wall=%.0f s  it/step=%.1f' % (
            k, max_steps, tk / 3600.0, C[0], el, tot_it / k)
        prog(msg)
        log(msg)
        flush()

if t_dry is None:
    log('BREAKER: no drying event within %.0f h -- abort' % BREAK_H)
    flush()
    sys.exit(2)

# ---- 子步级二分精化（区间 [prev_t, t_dry]） ----
prog('running: bisection')
t_bad, T_bad, C_bad = prev_t, prev_T, prev_C
t_ok, T_ok, C_ok = float(t_dry), dry_field[0], dry_field[1]
nit = 0
while t_ok - t_bad > 1e-3:
    mid = 0.5 * (t_ok + t_bad)
    w = mid - t_bad
    ns = max(1, int(round(w * NSUB / DT_OUT)))
    Tm, Cm, info = qc.step_imex4(N, dxi, w / ns, ns, qc.DEF4['R0'], qc.DEF4['h'],
                                 qc.DEF4['km'], T_bad, C_bad, t_bad,
                                 ts_env, Tv, Cv, ts_R, Rv, t_corr=1)
    tot_it += info['inner_tot']
    if Cm.max() < CC:
        t_ok, T_ok, C_ok = mid, Tm, Cm
    else:
        t_bad, T_bad, C_bad = mid, Tm, Cm
    nit += 1
log('bisection: %d iters -> t_dry = %.3f s (%.4f h)' % (nit, t_ok, t_ok / 3600.0))

# ---- 组装 result4 行 ----
xis = np.array([j / N for j in range(N + 1)])
R60 = [Rof(r[0]) for r in rows60]
data_rows = []              # (t, [21 values or None])
for (tk, Tk, Ck) in rows60:
    Rk = Rof(tk)
    vals = []
    for ci in range(20):
        rst = 0.1 * ci / 100.0
        if rst <= Rk + R_TOL:
            vals.append(round(float(qc.interp_lagrange(xis, Ck, rst / Rk, 6)), 4))
        else:
            vals.append(None)
    vals.append(round(float(Ck[-1]), 4))
    data_rows.append((tk, vals))
# 精确 t_dry 行（若非 60 s 整数倍）
Rd = Rof(t_ok)
if abs(t_ok - round(t_ok / 60.0) * 60.0) > 1e-6:
    vals = []
    for ci in range(20):
        rst = 0.1 * ci / 100.0
        if rst <= Rd + R_TOL:
            vals.append(round(float(qc.interp_lagrange(xis, C_ok, rst / Rd, 6)), 4))
        else:
            vals.append(None)
    vals.append(round(float(C_ok[-1]), 4))
    data_rows.append((round(t_ok, 3), vals))
    log('extra exact t_dry row appended (t=%.3f s)' % t_ok)
else:
    log('t_dry is multiple of 60 s -> no extra row (MB-21 dedup)')

# ---- 断言 ----
sec = lambda: None
log('--- assertions ---')
ok_all = True
n_all = len(data_rows)
a1 = n_all == len(rows60) + (1 if abs(t_ok - round(t_ok / 60.0) * 60.0) > 1e-6 else 0)
log('1 shape: %d rows (expect %d) -> %s' % (n_all, len(rows60), 'PASS' if a1 else 'FAIL'))
ok_all &= a1
allv = [v for _, vv in data_rows for v in vv if v is not None]
a2 = min(allv) >= 0.0
log('2 C nonneg (min=%.4f) -> %s' % (min(allv), 'PASS' if a2 else 'FAIL'))
ok_all &= a2
a3 = max(allv) <= qc.DEF4['C0'] + 1e-9
log('3 C <= C0 (max=%.4f) -> %s' % (max(allv), 'PASS' if a3 else 'FAIL'))
ok_all &= a3
c0s = [vv[0] for _, vv in data_rows]
a4 = all(c0s[i] >= c0s[i + 1] - 1e-9 for i in range(len(c0s) - 1))
log('4 center monotone non-increasing -> %s' % ('PASS' if a4 else 'FAIL'))
ok_all &= a4
a5 = all(max([v for v in vv if v is not None]) - vv[0] <= 1e-6 for _, vv in data_rows)
log('5 max at center (tol 1e-6) -> %s' % ('PASS' if a5 else 'FAIL'))
ok_all &= a5
last = [v for v in data_rows[-1][1] if v is not None]
a6_raw = float(dry_field[1].max()) < CC        # 原始全精度值（二分构造保证严格小于）
a6_disp = max(last) <= CC + 5e-5               # 4 位小数显示可容许 0.1500（Q3 表5 同款先例）
a6 = a6_raw and a6_disp
log('6 final row: raw max=%.8f (<0.15 strictly: %s); displayed max=%.6f -> %s'
    % (float(dry_field[1].max()), a6_raw, max(last), 'PASS' if a6 else 'FAIL'))
ok_all &= a6
# T 压缩温升报告（F-Q4-2：不作断言，如实报告）
Tmax = max(r[1].max() for r in rows60)
n_above = sum(int((r[1] > TENVM + 1e-9).sum()) for r in rows60)
log('T report: Tmax=%.4f C (env max %.3f); steps with T>env: %d (info only, F-Q4-2)'
    % (Tmax, TENVM, n_above))
log('assertions overall: %s' % ('PASS' if ok_all else 'FAIL'))

# ---- 写 result4.xlsx + CSV ----
prog('running: writing result4')
out = os.path.join(RES, 'result4.xlsx')
wb = openpyxl.Workbook()
w = wb.active
w.title = 'Sheet1'
w.append(HEADER)
for (tk, vv) in data_rows:
    w.append([tk] + vv)
wb.save(out)
csvp = os.path.join(RES, 'result4_data.csv')
with open(csvp, 'w', encoding='utf-8') as f:
    f.write(','.join(str(h) for h in HEADER) + '\n')
    for (tk, vv) in data_rows:
        f.write(str(tk) + ',' + ','.join('' if v is None else ('%.4f' % v) for v in vv) + '\n')

wall = time.perf_counter() - t_all
log('--- summary ---')
log('t_dry = %.3f s = %.4f h' % (t_ok, t_ok / 3600.0))
log('rows=%d ; wall=%.0f s ; Picard iters=%d ; res_max=%.2e'
    % (n_all, wall, tot_it, rm_all))
log('output: %s' % out)
log('R final=%.4f cm ; R(t_dry)=%.4f cm' % (Rv[-1] * 100, Rd * 100))
prog('done: t_dry=%.4f h' % (t_ok / 3600.0))
flush()
print('LOG-WRITTEN')
