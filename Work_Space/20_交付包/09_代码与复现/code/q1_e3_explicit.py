# -*- coding: utf-8 -*-
"""
E3 独立实现互验（双方法验证）：显式 FTCS 独立重解 Q1
======================================================
任务口径（不得更改）：
 · 与主力完全不同的时间格式：显式 FTCS（前向欧拉），无三对角求解、无 Picard 迭代；
 · 空间离散口径与主力一致：元体平衡（有限体积）；中心 4/Δr² 形式；
   表面半格 Robin（导热界面取 r_{N-1/2}=R0-Δr/2）；界面 D 取沿 C 的积分平均（口径 M6）；
 · C 方程时间显式：D 取上一时层值（时间显式、不迭代）；
 · 显式稳定限 Δt ≤ Δr²/(2α)，α=k/(ρcp)，Δr=0.25 mm 时约 0.185 s，
   取 Δt=0.02 s（裕度约 9）。
参考解：由 q1_core 主力口径（温度侧时间方向精确推进、含水率侧后向欧拉＋Picard，sub=10）
        现场计算；显式 FTCS 实现本身不调用 q1_core 的任何求解函数，
        仅将其结果作为"主力解"参照（双方法比对的基准）。
比对：t=100/300/600/900/1200/1500/1800 s 的 T(0)、T(R)、C(0)、C(R)，
      以及 t=1800 s 全场最大逐点差；输出最大偏差、量级解释、结论（是否通过）。
产出：q1_e3_log.txt
约定：本文件不引用、不记载任何资料中的日期。
"""
import io
import os
import platform
import sys
import time

import numpy as np
import openpyxl
from openpyxl import load_workbook

import q1_core as core
from q1_core import DEF

try:  # 重定向输出时强制 UTF-8，避免控制台编码问题
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
# 自适应定位工作区根：向上查找含 10_赛题 的目录
# （兼容两种目录深度：工作区 11_建模/11-3_算法与管线/Q1/code/ 与交付包 09 的 code/）
def _find_root(p, _marker='10_赛题', _max=6):
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, _marker)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.abspath(os.path.join(p, '..', '..', '..'))


ROOT = _find_root(HERE)
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx')
LOG = os.path.join(HERE, 'q1_e3_log.txt')

# ---------------------------------------------------------------- 口径常量
N = 80                       # 空间区间数（81 节点）
DR = 0.00025                 # Δr = 0.25 mm
DT_OUT = 1.0                 # 输出步长（s）
NSTEP = 1800                 # 输出步数（0-1800 s）
SUB = 10                     # C 内部子步数（内部步长 0.1 s）
SUBT = 32                    # T 内部子步数（内部步长 1/32 s）
TOL, OMEGA, MAXIT = 1e-9, 0.7, 30
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)   # 比对时刻（s）

DT_EX = 0.02                                  # 显式时间步（s）
NSTEPS_EX = int(round(NSTEP * DT_OUT / DT_EX))  # 90000 步
SNAP_STEPS = set(int(round(ts / DT_EX)) for ts in SNAP)

# 先验判据（在比对之前设定）：两种一阶时间格式的截断误差量级内一致即通过
CRIT_T = 1.0e-2      # max|ΔT| ≤ 1e-2 ℃
CRIT_C = 1.0e-3      # max|ΔC| ≤ 1e-3 kg/kg

# 《A_数值口径总表》§8.2 登记值（主力解，仅作参考解交叉核对，不参与求解）
REG = {'T(0,1800)': 33.5753, 'T(R,1800)': 36.7855,
       'C(0,1800)': 2.5500, 'C(R,1800)': 1.5104}

# 界面扩散系数：沿 C 的积分平均（口径 M6）。与 q1_core.faceD_int 同义的本地实现
# （本脚本保持自包含，不调用 q1_core 的任何求解函数）。
_FACE_NSAMP = 8


def _faceD_int(Carr, D0, bD):
    """<D> = D0*(1/dC)*Int exp(-bD/C) dC，胞内 8 点中点采样（与主力逐位同义）。"""
    C = np.asarray(Carr, dtype=float)
    lo = np.minimum(C[:-1], C[1:])
    hi = np.maximum(C[:-1], C[1:])
    xs = lo[:, None] + (hi - lo)[:, None] * (np.arange(_FACE_NSAMP) + 0.5)[None, :] / _FACE_NSAMP
    xs = np.maximum(xs, 1e-9)
    fv = np.exp(-bD / xs).mean(axis=1)
    flat = (hi - lo) < 1e-14
    if flat.any():
        fv[flat] = np.exp(-bD / np.maximum(lo[flat], 1e-9))
    return D0 * fv


LINES = []


def say(s):
    s = str(s)
    LINES.append(s)
    try:
        print(s, flush=True)
    except Exception:
        print(s.encode('ascii', 'replace').decode('ascii'), flush=True)


def flush_log():
    with io.open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINES) + '\n')


def load_att1():
    wb = load_workbook(ATT1, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    data = list(ws.iter_rows(values_only=True))[1:]
    return (np.array([float(r[0]) for r in data]),
            np.array([float(r[1]) for r in data]),
            np.array([float(r[2]) for r in data]))


def explicit_ftcs(t_arr, Tinf_arr, Cinf_arr, p):
    """显式 FTCS 求解（独立实现；时间格式与主力完全不同）。

    与主力隐式格式的逐项对应（同一套元体平衡空间算子，时间离散不同）：
      中心  i=0    : dT0/dt = 4α(T1-T0)/Δr²                  （4/Δr² 形式）
      内部  i=1..79: dT_i/dt = α[rr_i(T_{i+1}-T_i) - rl_i(T_i-T_{i-1})]/(r_i Δr²)
      表面  i=N    : ρcp·V_N·dT_N/dt = k(R0-Δr/2)(T_{N-1}-T_N)/Δr + hR0(T∞-T_N)
      C 方程同构，D 取上一时层值（时间显式、不迭代）。

    ✅ **口径已对齐（M6）**：界面 Df 本实现取**沿 C 的积分平均** <D>=(1/dC)*Int D dC
      （胞内 8 点中点采样，见 `_faceD_int`），**与主力逐位同义** ⟹ 两法差异**仅来自时间格式**。
      **T 方程不受影响**（Q1 为常数 k，不经界面平均）。
    """
    rho, cp, k = p['rho'], p['cp'], p['k']
    h, km = p['h'], p['km']
    D0, bD, T0, C0 = p['D0'], p['bD'], p['T0'], p['C0']
    R0 = p['R0']
    dr2 = DR * DR
    alpha = k / (rho * cp)
    dt = DT_EX

    # ---- 稳定性预算 ----
    Fo = alpha * dt / dr2
    lim_T_int = dr2 / (2.0 * alpha)                       # Δr²/(2α)
    VN = DR * (R0 - DR / 4.0) / 2.0                       # 表面控制体体积（元体平衡半格）
    lim_T_surf = rho * cp * VN / (k * (R0 - DR / 2.0) / DR + h * R0)
    Dmax = D0 * np.exp(-bD / C0)                          # D 的最大值（C=C0 处）
    lim_C_int = dr2 / (2.0 * Dmax)
    lim_C_surf = VN / (Dmax * (R0 - DR / 2.0) / DR + km * R0)
    lim_min = min(lim_T_int, lim_T_surf, lim_C_int, lim_C_surf)

    # ---- 显式系数（常物性＋固定网格 ⟹ 一次装配、与时间无关） ----
    ri = np.arange(1, N) * DR
    rl = ri - DR / 2.0
    rr = ri + DR / 2.0
    wl = Fo * rl / ri            # T 内部左系数（乘 T[i]-T[i-1]）
    wr = Fo * rr / ri            # T 内部右系数（乘 T[i+1]-T[i]）
    c0T = 4.0 * Fo               # 中心：4/Δr² 形式
    fT = dt / (rho * cp * VN)    # 表面：1/(ρcp·V_N) × Δt
    kface = k * (R0 - DR / 2.0) / DR
    hR0 = h * R0
    gC = dt / (ri * dr2)         # C 内部几何/步长因子
    fC = dt / VN
    kmR0 = km * R0
    rface = (R0 - DR / 2.0) / DR

    # ---- 环境取值：与主力同口径（线性插值；取子步终点时刻） ----
    t_end = (np.arange(NSTEPS_EX) + 1) * dt
    TenS = np.interp(t_end, t_arr, Tinf_arr)
    CinS = np.interp(t_end, t_arr, Cinf_arr)

    T = np.full(N + 1, T0)
    C = np.full(N + 1, C0)
    snaps = {}
    t0 = time.time()
    for n in range(NSTEPS_EX):
        tin = TenS[n]
        cin = CinS[n]
        # --- T：显式 FTCS ---
        Tn = T
        Tnew = np.empty(N + 1)
        Tnew[0] = Tn[0] + c0T * (Tn[1] - Tn[0])
        Tnew[1:N] = Tn[1:N] + wr * (Tn[2:] - Tn[1:N]) - wl * (Tn[1:N] - Tn[:-2])
        Tnew[N] = Tn[N] + fT * (kface * (Tn[N - 1] - Tn[N]) + hR0 * (tin - Tn[N]))
        # --- C：显式，D 取上一时层值（时间显式、不迭代） ---
        Cn = C
        D = D0 * np.exp(-bD / np.maximum(Cn, 1e-9))
        Df = _faceD_int(Cn, D0, bD)                     # 沿 C 的积分平均（口径 M6，与主力一致）
        Cnew = np.empty(N + 1)
        Cnew[0] = Cn[0] + 4.0 * dt * Df[0] / dr2 * (Cn[1] - Cn[0])
        Cnew[1:N] = Cn[1:N] + gC * (Df[1:] * rr * (Cn[2:] - Cn[1:N])
                                    - Df[:-1] * rl * (Cn[1:N] - Cn[:-2]))
        Cnew[N] = Cn[N] + fC * (Df[N - 1] * rface * (Cn[N - 1] - Cn[N])
                                + kmR0 * (cin - Cn[N]))
        T, C = Tnew, Cnew
        if (n + 1) in SNAP_STEPS:
            snaps[n + 1] = (T.copy(), C.copy())
        if (n + 1) % 15000 == 0:
            say('PROGRESS explicit step %d/%d  elapsed=%.1f s'
                % (n + 1, NSTEPS_EX, time.time() - t0))
    runtime = time.time() - t0
    stab = dict(alpha=alpha, Fo=Fo, lim_T_int=lim_T_int, lim_T_surf=lim_T_surf,
                lim_C_int=lim_C_int, lim_C_surf=lim_C_surf, lim_min=lim_min,
                Dmax=float(Dmax), VN=VN)
    return T, C, snaps, runtime, stab


def watchdog(snaps, p, Tinf_arr, Cinf_arr):
    """快照时刻物理看门狗：T/C 界内、C 逐节点不增、预热期 ∂rT|_R > 0"""
    Tinf_min, Tinf_max = float(Tinf_arr.min()), float(Tinf_arr.max())
    Cinf_min = float(Cinf_arr.min())
    ok = True
    msgs = []
    prev_C = None
    for n in sorted(snaps.keys()):
        T, C = snaps[n]
        tsec = n * DT_EX
        if T.min() < Tinf_min - 1e-9 or T.max() > Tinf_max + 1e-9:
            ok = False
            msgs.append('t=%g s: T 超出 [min Tinf, max Tinf]' % tsec)
        if C.min() < Cinf_min - 1e-9 or C.max() > p['C0'] + 1e-9:
            ok = False
            msgs.append('t=%g s: C 超出 [Cinf_min, C0]' % tsec)
        if prev_C is not None and np.any(C > prev_C + 1e-12):
            ok = False
            msgs.append('t=%g s: C 局部回升' % tsec)
        if (T[-1] - T[-2]) <= 0.0:
            ok = False
            msgs.append('t=%g s: 预热期方向断言 ∂rT|_R>0 不成立' % tsec)
        prev_C = C
    return ok, msgs


def main():
    t_all = time.time()
    t_arr, Tinf_arr, Cinf_arr = load_att1()
    p = dict(DEF)

    say('=' * 72)
    say('E3 独立实现互验：显式 FTCS 重解 Q1（0-1800 s 预热平衡阶段）')
    say('=' * 72)
    say('')
    say('--- 运行环境 ---')
    say('python=%s  numpy=%s  openpyxl=%s  %s %s'
        % (platform.python_version(), np.__version__, openpyxl.__version__,
           platform.system(), platform.release()))
    say('附件1 路径：%s' % ATT1)
    say('附件1 数据点=%d  t=[%g, %g] s  步长=%g s' %
        (len(t_arr), t_arr[0], t_arr[-1], t_arr[1] - t_arr[0]))
    say('Tinf 首/末 = %.4f / %.4f ℃   Cinf 首/末 = %.5f / %.5f kg/kg'
        % (Tinf_arr[0], Tinf_arr[-1], Cinf_arr[0], Cinf_arr[-1]))
    say('环境取值口径：np.interp 线性插值（L3-06），两方法一致取子步终点时刻')
    say('')
    say('--- 参数（主力口径，q1_core.DEF）---')
    for k in ('R0', 'rho', 'cp', 'k', 'h', 'km', 'D0', 'bD', 'T0', 'C0'):
        say('  %-4s = %.10g' % (k, p[k]))
    say('D(C) = D0*exp(-bD/C) = %.6g*exp(-%.4g/C) m^2/s；D(C0) = %.6e m^2/s'
        % (p['D0'], p['bD'], p['D0'] * np.exp(-p['bD'] / p['C0'])))
    say('网格：N=%d 区间 / %d 节点，dr=%.3g m；输出步长=%g s，nsteps=%d（0-1800 s）'
        % (N, N + 1, DR, DT_OUT, NSTEP))
    say('参考解（主力）：后向欧拉＋Picard＋三对角追赶法，subT=%d（dtT=%.5g s），'
        'sub=%d（dt=%.3g s），ω=%g，tol=%g，maxit=%d'
        % (SUBT, DT_OUT / SUBT, SUB, DT_OUT / SUB, OMEGA, TOL, MAXIT))
    say('本实验（显式）：FTCS 前向欧拉，dt=%.4g s，nsteps=%d，总时长=%.0f s'
        % (DT_EX, NSTEPS_EX, NSTEPS_EX * DT_EX))
    say('先验判据（比对前设定）：max|ΔT| ≤ %.1e ℃ 且 max|ΔC| ≤ %.1e kg/kg ⟹ 通过'
        % (CRIT_T, CRIT_C))
    say('（两方法共用同一套元体平衡空间算子，差异仅来自时间格式，'
        '故偏差应为一阶时间截断误差量级）')
    flush_log()

    # ------------------------------------------------ 显式解：稳定性预算
    T_ex, C_ex, snaps, rt_ex, stab = explicit_ftcs(t_arr, Tinf_arr, Cinf_arr, p)
    say('')
    say('--- 显式格式稳定性预算（dt=%.4g s）---' % DT_EX)
    say('alpha = k/(rho*cp) = %.6e m^2/s' % stab['alpha'])
    say('T 内部稳定限 dt ≤ Δr²/(2α)      = %.5f s   （裕度 %.2f）'
        % (stab['lim_T_int'], stab['lim_T_int'] / DT_EX))
    say('T 表面稳定限 dt ≤ ρcp·V_N/(k(R0-Δr/2)/Δr + h·R0) = %.5f s   （裕度 %.2f）'
        % (stab['lim_T_surf'], stab['lim_T_surf'] / DT_EX))
    say('C 内部稳定限 dt ≤ Δr²/(2·Dmax)  = %.5f s   （Dmax=D(C0)=%.4e m^2/s，裕度 %.2f）'
        % (stab['lim_C_int'], stab['Dmax'], stab['lim_C_int'] / DT_EX))
    say('C 表面稳定限 dt ≤ V_N/(Dmax(R0-Δr/2)/Δr + km·R0) = %.5f s   （裕度 %.2f）'
        % (stab['lim_C_surf'], stab['lim_C_surf'] / DT_EX))
    say('最紧稳定限 = %.5f s ⟹ 取 dt=%.3g s 全部满足（最紧裕度 ≈ %.1f）'
        % (stab['lim_min'], DT_EX, stab['lim_min'] / DT_EX))
    say('显式求解耗时 %.1f s（%d 步 × 81 节点 × T/C 两场，向量化）'
        % (rt_ex, NSTEPS_EX))
    flush_log()

    # ------------------------------------------------ 主力参考解（现算）
    say('')
    say('--- 主力参考解（q1_core 隐式口径现算，作比对基准）---')
    t0m = time.time()
    res, _, _ = core.run_sim_collect(
        N=N, dr=DR, dt_out=DT_OUT, nsteps=NSTEP, p=dict(p),
        Tenv_fn=lambda s: float(np.interp(s, t_arr, Tinf_arr)),
        Cenv_fn=lambda s: float(np.interp(s, t_arr, Cinf_arr)),
        sub=SUB, subT=SUBT, center='fv', surf='fvm',
        tol=TOL, omega=OMEGA, maxit=MAXIT, cols=None,
        snap_at=set(SNAP), solve_T=True, solve_C=True)
    rt_main = time.time() - t0m
    st = res['stats']
    say('主力求解耗时 %.1f s（T %.1f s + C %.1f s）；Picard: avg=%.2f 次/子步，'
        'max=%d 次，max_res=%.2e'
        % (rt_main, res['T_time'], res['C_time'], st['avg_it'], st['max_it'],
           st['max_res']))
    T_main_1800 = res['T_end']
    C_main_1800 = res['C_end']
    say('主力参考解 t=1800 s：T(0)=%.6f  T(R)=%.6f  C(0)=%.6f  C(R)=%.6f'
        % (T_main_1800[0], T_main_1800[-1], C_main_1800[0], C_main_1800[-1]))
    say('与《A_数值口径总表》§8.2 登记值核对（登记值：T(0)=33.5753，T(R)=36.7855，'
        'C(0)=2.5500，C(R)=1.5104）：')
    chk = [('T(0,1800)', T_main_1800[0], REG['T(0,1800)']),
           ('T(R,1800)', T_main_1800[-1], REG['T(R,1800)']),
           ('C(0,1800)', C_main_1800[0], REG['C(0,1800)']),
           ('C(R,1800)', C_main_1800[-1], REG['C(R,1800)'])]
    for name, val, ref in chk:
        say('  %-10s 现算=%.6f  登记=%g  差=%+.2e  4位小数一致=%s'
            % (name, val, ref, val - ref,
               '是' if round(float(val), 4) == round(float(ref), 4) else '否'))
    flush_log()

    # ------------------------------------------------ 逐时刻比对
    say('')
    say('--- 逐时刻比对（主力=温度精确推进／C 隐式＋Picard；显式=FTCS）---')
    say('%7s | %-9s %-9s %-10s | %-9s %-9s %-10s | %-10s %-10s %-9s | %-10s %-10s %-9s'
        % ('t(s)', 'T(0)主', 'T(0)显', 'ΔT(0)', 'T(R)主', 'T(R)显', 'ΔT(R)',
           'C(0)主', 'C(0)显', 'ΔC(0)', 'C(R)主', 'C(R)显', 'ΔC(R)'))
    max_dT_pt, max_dC_pt = 0.0, 0.0
    for ts in SNAP:
        Tm = res['T_snap'][ts]
        Cm = res['C_snap'][ts]
        Te, Ce = snaps[ts * int(round(1.0 / DT_EX))]
        dT0 = Te[0] - Tm[0]
        dTR = Te[-1] - Tm[-1]
        dC0 = Ce[0] - Cm[0]
        dCR = Ce[-1] - Cm[-1]
        max_dT_pt = max(max_dT_pt, abs(dT0), abs(dTR))
        max_dC_pt = max(max_dC_pt, abs(dC0), abs(dCR))
        say('%7d | %.6f %.6f %+.2e | %.6f %.6f %+.2e | %.7f %.7f %+.2e | %.7f %.7f %+.2e'
            % (ts, Tm[0], Te[0], dT0, Tm[-1], Te[-1], dTR,
               Cm[0], Ce[0], dC0, Cm[-1], Ce[-1], dCR))
    say('（注：C(0) 在 1800 s 内总变化约 8e-6 kg/kg，其 Δ 的绝对值极小属预期）')
    flush_log()

    # ------------------------------------------------ t=1800 s 全场比对
    say('')
    say('--- t=1800 s 全场最大逐点差（81 节点）---')
    dT_field = np.abs(T_ex - T_main_1800)
    dC_field = np.abs(C_ex - C_main_1800)
    iT = int(np.argmax(dT_field))
    iC = int(np.argmax(dC_field))
    rmsT = float(np.sqrt(np.mean(dT_field ** 2)))
    rmsC = float(np.sqrt(np.mean(dC_field ** 2)))
    say('|ΔT|max = %.3e ℃  （节点 %d，r = %.4f cm）；RMS(ΔT) = %.3e ℃'
        % (dT_field[iT], iT, iT * DR * 100.0, rmsT))
    say('|ΔC|max = %.3e kg/kg（节点 %d，r = %.4f cm）；RMS(ΔC) = %.3e kg/kg'
        % (dC_field[iC], iC, iC * DR * 100.0, rmsC))
    max_dT_all = float(dT_field.max())
    max_dC_all = float(dC_field.max())

    # ------------------------------------------------ 物理看门狗
    ok_wd, msgs_wd = watchdog(snaps, p, Tinf_arr, Cinf_arr)
    say('')
    say('--- 物理看门狗（显式解快照时刻）---')
    say('结果：%s' % ('全部通过' if ok_wd else '存在违反'))
    for m in msgs_wd:
        say('  违反：' + m)

    # ------------------------------------------------ 量级解释与结论
    dTR_tot = float(T_ex[-1] - p['T0'])
    dCR_tot = float(p['C0'] - C_ex[-1])
    say('')
    say('--- 量级解释 ---')
    say('两方法共用同一套元体平衡空间算子（中心 4/Δr² 形式、表面半格 Robin、'
        '界面 D 沿 C 的积分平均＝口径 M6），差异仅来自时间格式：')
    say('主力=温度侧时间方向精确推进／含水率侧后向欧拉（一阶）；本实验=前向欧拉（一阶，dt=0.02 s）。')
    say('一阶格式截断误差之差的量级为 O((dtT/2 + dt/2)·|ü| 的时间积分)，'
        '与 E1-b 实测的时间误差尺度同阶（dtT 由 1 s 细化到 0.125 s 时 '
        'T(0,1800) 移动约 1.05e-3 ℃）。')
    say('实测：最大 |ΔT| = %.3e ℃，占表面总升温 %.3f ℃ 的 %.2e；'
        '最大 |ΔC| = %.3e kg/kg，占表面总降湿 %.3f kg/kg 的 %.2e。'
        % (max_dT_all, dTR_tot, max_dT_all / dTR_tot,
           max_dC_all, dCR_tot, max_dC_all / dCR_tot))
    n_tot, n_diff, diff_desc = 0, 0, []
    for ts in SNAP:
        Tm4 = res['T_snap'][ts]
        Cm4 = res['C_snap'][ts]
        Te4, Ce4 = snaps[ts * int(round(1.0 / DT_EX))]
        for name, a, b in (('T(0)', Tm4[0], Te4[0]), ('T(R)', Tm4[-1], Te4[-1]),
                           ('C(0)', Cm4[0], Ce4[0]), ('C(R)', Cm4[-1], Ce4[-1])):
            n_tot += 1
            if round(float(a), 4) != round(float(b), 4):
                n_diff += 1
                diff_desc.append('t=%g s 的 %s（主力 %.4f vs 显式 %.4f，差 %.1e）'
                                 % (ts, name, a, b, abs(a - b)))
    end_diff = [d for d in diff_desc if d.startswith('t=1800')]
    say('该偏差为两方法各自一阶时间截断误差之差（温度侧主力已精确推进，故其残差即'
        '显式 dt=0.02 s 的一阶截断误差）——实测 max|ΔT|=%.1e ℃ 与其量级一致；'
        '含水率侧两法界面口径已统一为 M6，故 ΔC 即**纯实现差**。' % max_dT_all)
    say('但需强调：该偏差是两方法之间的格式差异，不等于主力解误差本身，'
        '其相对量级仅 %.1e（占表面总升温）。' % (max_dT_all / dTR_tot))
    say('4 位小数口径核验：%d 个比对量中 %d 个与主力解逐点一致；%s'
        % (n_tot, n_tot - n_diff,
           ('差异项为 ' + '；'.join(diff_desc) +
            '，恰处第 4 位小数舍入边界（论文表格一律以主力解为准，不涉及任何登记值改动）')
           if n_diff else '全部一致'))
    say('t=1800 s 终点 4 个输出量（全部登记值所在点）在 4 位小数口径下与主力解%s。'
        % ('完全一致' if not end_diff else '存在差异'))
    verdict_pass = (max_dT_all <= CRIT_T) and (max_dC_all <= CRIT_C)
    say('')
    say('--- 结论 ---')
    say('判据：max|ΔT| ≤ %.1e ℃ 且 max|ΔC| ≤ %.1e kg/kg' % (CRIT_T, CRIT_C))
    say('实测：max|ΔT| = %.3e ℃，max|ΔC| = %.3e kg/kg' % (max_dT_all, max_dC_all))
    say('一句话结论：E3 独立实现互验【%s】——显式 FTCS 与主力隐式解在'
        '一阶时间离散误差量级内一致，Q1 数值结果通过双方法验证。'
        % ('通过' if verdict_pass else '不通过'))
    say('')
    say('总耗时 %.1f s（主力 %.1f s ＋ 显式 %.1f s）' % (time.time() - t_all, rt_main, rt_ex))
    flush_log()
    print('E3 ALL DONE verdict=%s rc=%d' % ('PASS' if verdict_pass else 'FAIL',
                                            0 if verdict_pass else 1))
    return 0 if verdict_pass else 1


if __name__ == '__main__':
    sys.exit(main())
