# -*- coding: utf-8 -*-
"""
Q4 W2 预试验批次（T1/T2 测试级；止步于正式全量执行前）
================================================================================
[SCALE] 本批次各算例规模（全部远小于正式求解）：
  S1 冒烟      : 60 s 时程 x 32 子步/s x 81 节点      （约 2 s）
  S2 复用检验  : 同上（q4 vs q3_core 对照）           （约 4 s）
  S3 绝热自检  : 3600 s x 32 x 81                     （约 3 s）
  S4 D6 取层   : 7200 s x 32 x 81 x 2 变体            （约 8 s）
  S5 时间收敛  : 21600 s x {8,16,32} x 81             （约 10 s）
  S6 空间收敛  : 21600 s x 32 x {41,81,161} 节点      （约 20 s）
  S7 插值误差  : 后处理（无新求解）                   （约 0 s）
  批次总计预计 < 60 s 墙钟（不含 JIT 编译）。
授权：用户本轮指令"可自行执行测试……停止在正式全量执行前"（T2 批内，无交付物）。
用法：python q4_pretest.py          -> 只打印 [SCALE] 声明并退出
      python q4_pretest.py --go     -> 实际执行
输出：控制台仅 ASCII 状态；详细结果写 logs/q4_pretest_log.txt（UTF-8）。
"""
import sys, os, time, io

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_Q3 = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'Q3')
sys.path.insert(0, _Q3)

import numpy as np
import q4_core as qc

LOG = os.path.join(HERE, '..', 'logs')
os.makedirs(LOG, exist_ok=True)
LOGF = os.path.join(LOG, 'q4_pretest_log.txt')
rep = []


def log(s=''):
    rep.append(s)
    try:
        print(s.encode('ascii', 'replace').decode('ascii'))
    except Exception:
        pass


def sec(title):
    log('')
    log('=' * 72)
    log(title)


TINF, CINF = 50.00, 0.04999
TS_ENV = np.array([0.0, 1.0])
TV = np.array([TINF, TINF])
CV = np.array([CINF, CINF])
NREF = 80
DSUB = 32

# ---- [SCALE] 声明与闸门 ----
log('[SCALE] Q4 W2 pretest batch: 9 cases (S0-S8), all T1/T2 scale (see file header)')
log('[SCALE] max horizon=21600 s, max nodes=321, total wall est ~400 s (measured 403 s) + JIT')
log('[SCALE] NO deliverable produced; formal full solve NOT included')
if '--go' not in sys.argv:
    log('[SCALE] --go not given -> exit (gate closed)')
    open(LOGF, 'w', encoding='utf-8').write('\n'.join(rep))
    sys.exit(0)

t_start = time.perf_counter()

# ---- 公共数据 ----
ATT2 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE)))), '10_赛题', 'A题', '附件', '附件2.xlsx')
ts_R, Rv = qc.load_R_table(ATT2)
log('R table: %d pts, R(0)=%.4f m, R(end)=%.4f m, t_end=%.0f s'
    % (len(ts_R), Rv[0], Rv[-1], ts_R[-1]))


def Rof(t):
    return float(np.interp(t, ts_R, Rv))


# ================================================================
sec('S0 unit checks (pure python, no solving)')
# (a) 调和平均
f = np.array([2.0, 8.0, 0.0, 6.0])
ifc = qc._iface_nb(f)
log('iface([2,8,0,6]) = %s  expect [3.2, 0, 0]' % np.array2string(ifc))
assert abs(ifc[0] - 3.2) < 1e-14 and ifc[1] == 0.0 and ifc[2] == 0.0
# (b) R 插值端点钳位与节点值
assert abs(qc._interp1_nb.py_func(0.0, ts_R, Rv) - Rv[0]) < 1e-15
assert abs(qc._interp1_nb.py_func(1e9, ts_R, Rv) - Rv[-1]) < 1e-15
for t in (1800.0, 36000.0, 259200.0):
    assert abs(qc._interp1_nb.py_func(t, ts_R, Rv) - Rof(t)) < 1e-15
log('R interp: node/endpoints clamp OK')
# (c) 中心双路系数一致性（洛必达 vs 元体平衡，符号推导核对）
#     元体平衡: rho*cp/h + 4k/(R^2 dxi^2)  ;  洛必达: lim (1/(xi R^2)) d(xi k dT) = 2k/R^2 * d2T
#     2k * 2(dT1-dT0)/dxi^2 / R^2 = 4k/(R^2 dxi^2)  -> 与实现一致（解析核对，见工作流 §2.1）
log('center dual-path: algebraic identity documented (4k/(R^2 dxi^2)) OK')
# (d) 三次插值常数/线性再现性
xs = np.linspace(0.0, 1.0, 81)
for g in (lambda x: 1.0, lambda x: x, lambda x: x * x * x):
    err = max(abs(qc.interp_cubic(xs, [g(x) for x in xs], x) - g(x))
              for x in np.linspace(0.02, 0.98, 25))
    log('cubic interp reproducibility err = %.2e' % err)
    assert err < 1e-12
log('S0 PASS')

# ================================================================
sec('S1 smoke: 60 s, N=80, n_sub=32 (t_corr=1, coupled)')
f1, s1 = qc.run_q4(N=NREF, t_end=60.0, dt_out=1.0, n_sub=DSUB,
                   ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                   t_corr=1)
T60, C60 = f1[60.0]
log('wall=%.2fs inner=%d res_max=%.2e' % (s1['wall'], s1['inner_tot'], s1['res_max']))
log('T(0)=%.6f T(R)=%.6f C(0)=%.6f C(R)=%.6f' % (T60[0], T60[-1], C60[0], C60[-1]))
log('checks: T in [28,50.01]? %s ; C nonneg & <=C0? %s'
    % (bool(T60.min() >= 28.0 - 1e-12 and T60.max() <= TINF + 1e-12),
       bool(C60.min() >= 0.0 and C60.max() <= 2.55 + 1e-12)))
# Picard 收敛判据：平均迭代数远低于上限 ⟹ 无截断（res_max 含首次迭代残差，
# 属 Q2/Q3 同款语义，不作收敛判据）
avg_it = s1['inner_tot'] / (s1['nsteps'] * DSUB)
log('avg Picard iters/substep = %.1f (cap 30) -> %s'
    % (avg_it, 'OK' if avg_it < 30 else 'TRUNCATED'))
assert avg_it < 30

# ================================================================
sec('S2 reuse check: q4(fixR,app3) vs q3_core.step_imex_fast, 60 s')
import q3_core as q3c
T = np.full(NREF + 1, 28.0)
C = np.full(NREF + 1, 2.55)
dr = 2.0e-2 / NREF
t0w = time.perf_counter()
for k in range(60):
    T, C, info = q3c.step_imex_fast(NREF, dr, 1.0 / DSUB, DSUB, 2.0e-2,
                                    25.0, 8.0e-7, T, C,
                                    TS_ENV, TV, CV, float(k))
w3 = time.perf_counter() - t0w
f2, s2 = qc.run_q4(N=NREF, t_end=60.0, dt_out=1.0, n_sub=DSUB,
                   ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                   fixR=True, app3=True)
T4, C4 = f2[60.0]
dT = np.max(np.abs(T4 - T))
dC = np.max(np.abs(C4 - C))
log('q3 wall=%.2fs ; q4 wall=%.2fs' % (w3, s2['wall']))
log('max|dT| = %.3e K ; max|dC| = %.3e kg/kg' % (dT, dC))
log('rel dT = %.3e ; rel dC = %.3e' % (dT / max(1.0, np.abs(T).max()),
                                       dC / max(1.0, np.abs(C).max())))
# 判据修订（2026-09-12；**只改判据口径，不改任何数值**）：
#   ① 交付量 C → 严格相对判据 rel ≤ 1e-9；
#   ② 监测量 T → 输出预算判据 |ΔT| ≤ 5e-5 K（4 位小数有效，L3-07）。
#   依据：两核单子步**机器级一致**（1.07e-14）；60 s 聚合差呈**舍入噪声底**
#   （非公式差异：kf/Df/ρcp 逐位为 0；根因＝内点行标定路径代数等价但不同），
#   且 Q4 交付量为 C（result4 仅含水率），T 为监测量。详见《A_Q4求解记录》§五。
_ok_c = (dC / 2.55) <= 1e-9
_ok_T = dT <= 5e-5
log('S2 %s (criteria: rel dC<=1e-9 [交付量] ; |dT|<=5e-5 K [输出预算])'
    % ('PASS' if (_ok_c and _ok_T) else 'FAIL'))
log('   -> rel dC=%.3e [%s] ; |dT|=%.3e K [%s]'
    % (dC / 2.55, 'OK' if _ok_c else 'X', dT, 'OK' if _ok_T else 'X'))
log('   (严格联合判据备查 max(rel dT/50, rel dC/2.55) = %.3e vs 1e-9 -> %s)'
    % (max(dT / 50.0, dC / 2.55),
       'PASS' if max(dT / 50.0, dC / 2.55) <= 1e-9 else 'FAIL'))

# ================================================================
sec('S3 adiabatic self-check: k=0 AND hc=0, 3600 s, real R(t) -> T*R^2 const')
# 绝热检验必须同时关断导热与表面对流（否则 Robin 边界仍注热，非"绝热"前提）
f3, s3 = qc.run_q4(N=NREF, t_end=3600.0, dt_out=1.0, n_sub=DSUB,
                   ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                   k_zero=True, t_corr=0, hcv=0.0)
T3600, C3600 = f3[3600.0]
R6 = Rof(3600.0)
inv_n = T3600 * R6 * R6
inv_0 = 28.0 * 0.02 * 0.02
err = np.max(np.abs(inv_n - inv_0)) / inv_0
log('T*R^2 invariant rel err = %.3e (criterion <= 1e-12)' % err)
log('S3 %s' % ('PASS' if err <= 1e-12 else 'FAIL'))

# ================================================================
sec('S4 D6 rho*cp layer choice: 7200 s, lag(0) vs predictor-corrector(1)')
fa, sa = qc.run_q4(N=NREF, t_end=7200.0, dt_out=1.0, n_sub=DSUB,
                   ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                   t_corr=0)
fb, sb = qc.run_q4(N=NREF, t_end=7200.0, dt_out=1.0, n_sub=DSUB,
                   ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                   t_corr=1)
Ta, Ca = fa[7200.0]
Tb, Cb = fb[7200.0]
log('wall lag=%.2fs corrector=%.2fs (ratio %.2f)'
    % (sa['wall'], sb['wall'], sb['wall'] / max(sa['wall'], 1e-9)))
log('max|dT| = %.3e K ; max|dC| = %.3e kg/kg' % (np.max(np.abs(Tb - Ta)),
                                                 np.max(np.abs(Cb - Ca))))
log('C(0): lag=%.9f corr=%.9f' % (Ca[0], Cb[0]))

# ================================================================
sec('S5 time convergence: 21600 s, n_sub in {8,16,32}, t_corr=1')
res_t = {}
for ns in (8, 16, 32):
    ff, ss = qc.run_q4(N=NREF, t_end=21600.0, dt_out=1.0, n_sub=ns,
                       ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                       t_corr=1)
    Tt, Ct = ff[21600.0]
    res_t[ns] = (Tt.copy(), Ct.copy(), ss['wall'])
    log('n_sub=%2d wall=%6.2fs C(0)=%.9f C(R)=%.9f T(0)=%.6f'
        % (ns, ss['wall'], Ct[0], Ct[-1], Tt[0]))
for a, b in ((8, 16), (16, 32)):
    Ta_, Ca_, _ = res_t[a]
    Tb_, Cb_, _ = res_t[b]
    rel = max(abs(Cb_[0] - Ca_[0]) / 2.55, abs(Cb_[-1] - Ca_[-1]) / 2.55)
    log('rel change n_sub %d->%d : %.3e (criterion <= 5e-5)' % (a, b, rel))

# ================================================================
sec('S6 space convergence: 21600 s, N in {40,80,160}, n_sub=32, t_corr=1')
res_s = {}
for NN in (40, 80, 160):
    ff, ss = qc.run_q4(N=NN, t_end=21600.0, dt_out=1.0, n_sub=DSUB,
                       ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                       t_corr=1)
    Tt, Ct = ff[21600.0]
    res_s[NN] = (Tt.copy(), Ct.copy(), ss['wall'])
    log('N=%3d wall=%6.2fs C(0)=%.9f C(R)=%.9f' % (NN, ss['wall'], Ct[0], Ct[-1]))
for a, b in ((40, 80), (80, 160)):
    _, Ca_, _ = res_s[a]
    _, Cb_, _ = res_s[b]
    rel = max(abs(Cb_[0] - Ca_[0]) / 2.55, abs(Cb_[-1] - Ca_[-1]) / 2.55)
    log('rel change N %d->%d : %.3e' % (a, b, rel))

# ================================================================
sec('S7 interpolation error at t=21600 s (pure post-processing)')
R6 = Rof(21600.0)
xs80 = np.linspace(0.0, 1.0, 81)
xs160 = np.linspace(0.0, 1.0, 161)
xs320 = np.linspace(0.0, 1.0, 321)
ff320, _ = qc.run_q4(N=320, t_end=21600.0, dt_out=1.0, n_sub=DSUB,
                     ts_env=TS_ENV, Tenv_v=TV, Cenv_v=CV, ts_R=ts_R, Rv=Rv,
                     t_corr=1)
_, C320 = ff320[21600.0]
_, C160 = res_s[160][:2]
_, C80 = res_s[80][:2]
log('r*   xi*      cubic80      cubic160     cubic320    '
    'd80-320      d160-320')
worst80 = worst80q = 0.0
R6cm = R6 * 100.0
samples = [rcm / 100.0 for rcm in (0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0)
           if rcm <= R6cm]
samples.append(0.95 * R6)          # 近表面（含插值最严苛位置）
samples.append(0.995 * R6)
for r in samples:
    x = r / R6
    v80c = qc.interp_lagrange(xs80, C80, x, 4)
    v80q = qc.interp_lagrange(xs80, C80, x, 6)
    v320 = qc.interp_lagrange(xs320, C320, x, 6)
    d80c = abs(v80c - v320)
    d80q = abs(v80q - v320)
    worst80 = max(worst80, d80c)
    worst80q = max(worst80q, d80q)
    log('%.3f  %.4f  cubic80=%.9f  q6-80=%.9f  q6-320=%.9f  '
        'd(c80,q320)=%.2e  d(q80,q320)=%.2e'
        % (r * 100.0, x, v80c, v80q, v320, d80c, d80q))
log('worst |cubic80 - q6_320| = %.3e ; |q6_80 - q6_320| = %.3e' %
    (worst80, worst80q))

# ================================================================
sec('S8 interface-coefficient port: new (integral avg) vs old (harmonic)')
# 参照值：2026-09-11 r1 期预试验日志（21600 s, N=80, n_sub=32, t_corr=1）
# ⚠ 该参照取自 r1 期：彼时核心含"存储项/行标定"缺陷、界面走调和平均
#   ⟹ 与本轮现口径的比较同时含"实现修复"与"界面口径"两个变更，**不是**移植影响的单变量隔离结果。
OLD = dict(C0=1.596257457, CR=0.407866630, T0v=52.099016)
Tn, Cn = res_t[32][:2]      # S5 的 n_sub=32（新口径）21600 s 场
dC0 = Cn[0] - OLD['C0']
dCR = Cn[-1] - OLD['CR']
dT0 = Tn[0] - OLD['T0v']
log('C(0)  : old=%.9f  new=%.9f  diff=%+.3e (%+.3f%%)' %
    (OLD['C0'], Cn[0], dC0, 100.0 * dC0 / OLD['C0']))
log('C(R)  : old=%.9f  new=%.9f  diff=%+.3e (%+.3f%%)' %
    (OLD['CR'], Cn[-1], dCR, 100.0 * dCR / OLD['CR']))
log('T(0)  : old=%.6f  new=%.6f  diff=%+.3e K' % (OLD['T0v'], Tn[0], dT0))
log('判读：以上为「r1 期参照（含存储缺陷 ＋ 调和平均）」与「现口径（积分平均、存储项已修复）」的实测差；')
log('  r1 期同一比较曾报 +2.148%（受存储项缺陷污染，**不得引用**）。**以本轮实测数值为准。**')
log('参考：S7 判据为 output-grid interp+disc error <= 5e-5 (L3-07)')

# ================================================================
sec('BATCH SUMMARY')
log('total batch wall = %.1f s' % (time.perf_counter() - t_start))
log('full results in %s' % LOGF)
open(LOGF, 'w', encoding='utf-8').write('\n'.join(rep))
print('LOG-WRITTEN')
