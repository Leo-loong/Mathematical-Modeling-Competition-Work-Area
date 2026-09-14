# -*- coding: utf-8 -*-
"""
IN-2 | 独立实现互验轨：Crank–Nicolson ＋ Rannacher 启动（创新副本 · 只验不替）
================================================================================
独立性声明（**本脚本与 q3_core 不共享任何函数**）：
  · 空间离散：元体平衡有限体积，**自行装配**（节点中心控制体，几何权重 V_i、r_{i±1/2}）
  · 时间格式：**Crank–Nicolson（二阶）**，**Rannacher 启动**（前 2 步用后向欧拉半步）
  · 线性求解：`scipy.linalg.solve_banded`（独立于主力的 numba 手写追赶法）
  · 界面系数：仍取**沿 C 的积分平均**（口径 M6）——保证差异只来自"格式与实现"
  · 非线性：C 方程内层 Picard（ω=0.7，上限 30，tol 1e-10）

产物（带副本标记）：
  out/result3_INV2.xlsx   （60 s × 21 列，与 result3.xlsx 同构）
  logs/q3_INV2_e3.log
  out/fig_q3_INV2_e3.csv  （比对用：公共时刻的中心/表面值）

用法：
  python q3_e3_INV2_cn.py --smoke       # 冒烟：N=40、1 h 上限
  python q3_e3_INV2_cn.py               # 正式：N=80、1/32 s、事件驱动（约 8–12 min）
  python q3_e3_INV2_cn.py --hours 3     # 只跑 3 h（与 result2 比对用）
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
from scipy.linalg import solve_banded
from openpyxl import Workbook


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
WS = _find_root(HERE)
OUTDIR = os.path.join(HERE, 'out')
LOGDIR = os.path.join(HERE, 'logs')
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(LOGDIR, exist_ok=True)
ATT1 = os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx')

C_CRIT = 0.15
DT_OUT = 60.0
T_TAIL, C_TAIL = 50.00, 0.04999
R0 = 0.02
HC = 25.0
KM = 8e-7

BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


# ---------------- 物性（附录3；独立书写） ----------------
def rho_of(C):
    return 650.0 + 128.0 * C


def cp_of(C):
    return 1450.0 + 2736.0 * C / (C + 1.0)


def k_of(C):
    return 0.21 + 0.38 * C / (C + 1.0)


def D_of(C, T):
    C = np.maximum(C, 1e-12)
    return 2.4e-3 * np.exp(-0.45 / C) * np.exp(-3850.0 / (T + 273.15))


def face_integral_avg(Cl, Cr, T, kind, ns=8):
    """沿 C 的积分平均（口径 M6）：界面系数 = (1/ΔC)∫φ dC，8 点采样。"""
    Cl = np.asarray(Cl, dtype=float)
    Cr = np.asarray(Cr, dtype=float)
    T = np.asarray(T, dtype=float)
    s = (np.arange(ns) + 0.5) / ns                      # 中点采样
    Cs = Cl[:, None] + (Cr - Cl)[:, None] * s[None, :]
    if kind == 'D':
        vals = D_of(Cs, T[:, None])
    elif kind == 'k':
        vals = k_of(Cs)
    else:
        raise ValueError(kind)
    return vals.mean(axis=1)


# ---------------- 几何（节点中心控制体） ----------------
class Geo:
    def __init__(self, N, dr):
        self.N, self.dr, self.NC = N, dr, N + 1
        r = np.arange(N + 1) * dr                       # 节点
        self.r = r
        self.rf = np.append((r[:-1] + r[1:]) / 2.0, r[-1])      # 界面（含外表面 R）
        V = np.zeros(N + 1)
        V[0] = (self.rf[0] ** 2) / 2.0
        for i in range(1, N):
            V[i] = (self.rf[i] ** 2 - self.rf[i - 1] ** 2) / 2.0
        V[N] = (self.rf[N] ** 2 - self.rf[N - 1] ** 2) / 2.0
        self.V = V


def assemble_solve(geo, phi, ac, dt, u, cineq, kind, theta=0.5, pres=None):
    """组装并求解 (V φ/dt)(u^{n+1}-u^n) = θ F^{n+1} + (1-θ) F^n

    ac: (a+, a-) 数组，a+_i = coef_{i+1/2} r_{i+1/2}/dr，i=0..N-1；a-_i 同（i=1..N）
    cineq: 环境值（C∞ 或 T∞）
    kind: 'C' → 表面通量 k_m R (u_N - cineq)；'T' → 流入 h R (cineq - u_N)
    θ=0.5 → CN；θ=1 → 后向欧拉
    pres: 预组装的右端（用于 Rannacher 半步？不用）
    """
    N, V, rf, dr = geo.N, geo.V, geo.rf, geo.dr
    ap, am = ac
    n = N + 1
    diag = np.zeros(n)
    up = np.zeros(n - 1)
    lo = np.zeros(n - 1)
    rhs = np.zeros(n)

    # ---- 内部节点 1..N-1（向量化装配） ----
    idx = np.arange(1, N)
    diag[idx] = V[idx] * phi[idx] / dt + theta * (ap[idx] + am[idx])
    up[idx] = -theta * ap[idx]           # up[i] ↔ 行 i 与列 i+1 的耦合（i=0..N-1）
    lo[idx - 1] = -theta * am[idx]       # lo[i-1] ↔ 行 i 与列 i-1 的耦合
    Fn = ap[idx] * (u[idx + 1] - u[idx]) - am[idx] * (u[idx] - u[idx - 1])
    rhs[idx] = V[idx] * phi[idx] / dt * u[idx] + (1.0 - theta) * Fn

    # ---- 中心 i=0（对称；a+_0 = coef_{1/2} r_{1/2}/dr） ----
    diag[0] = V[0] * phi[0] / dt + theta * ap[0]
    up[0] = -theta * ap[0]
    Fn0 = ap[0] * (u[1] - u[0])
    rhs[0] = V[0] * phi[0] / dt * u[0] + (1.0 - theta) * Fn0

    # ---- 表面 i=N ----
    # 表面项：F_N = -am[N](u_N-u_{N-1}) + g (u_N - cineq)
    #   C：质量流出 = +k_m R (C_N - C_inf) ⟹ g = -k_m R
    #   T：流入     = +h R (T_inf - T_N)  ⟹ g = -h R
    g = -(KM if kind == 'C' else HC) * R0
    diag[N] = V[N] * phi[N] / dt + theta * (am[N] - g)
    lo[N - 1] = -theta * am[N]
    # ⚠ CN 的边界常数项：左端移项后右端须减 **g·cineq（全系数）**，
    #   否则 u_∞ 的隐式贡献 θ g u_∞ 丢失 ⟹ T 场出现 O(1 ℃) 偏差（已由单步诊断证实）
    FnN_int = -am[N] * (u[N] - u[N - 1]) + g * u[N]
    rhs[N] = V[N] * phi[N] / dt * u[N] + (1.0 - theta) * FnN_int - g * cineq

    ab = np.zeros((3, n))
    ab[0, 1:] = up
    ab[1, :] = diag
    ab[2, :-1] = lo
    return solve_banded((1, 1), ab, rhs)


def step(geo, T, C, dt, Cinf, Tinf, theta=0.5, omega=0.7, tol=1e-10, maxit=30):
    """推进一个时间步（CN 或 BE），含 C 方程内层 Picard。返回 (T, C)"""
    N = geo.N
    # ---- T（物性用旧状态；界面 k 积分平均） ----
    kf = face_integral_avg(C[:-1], C[1:], (T[:-1] + T[1:]) / 2.0, 'k')
    apT = kf * geo.rf[:N] / geo.dr
    amT_full = np.zeros(N + 1)
    amT_full[1:N] = kf[:N - 1] * geo.rf[:N - 1] / geo.dr
    amT_full[N] = kf[N - 1] * geo.rf[N - 1] / geo.dr
    phiT = rho_of(C) * cp_of(C)
    Tn = assemble_solve(geo, phiT, (apT, amT_full), dt, T, Tinf, 'T', theta=theta)

    # ---- C（Picard，界面 D 积分平均） ----
    Cit = C.copy()
    for _ in range(maxit):
        Df = face_integral_avg(Cit[:-1], Cit[1:], (T[:-1] + T[1:]) / 2.0, 'D')
        apC = Df * geo.rf[:N] / geo.dr
        amC = np.zeros(N + 1)
        amC[1:N] = Df[:N - 1] * geo.rf[:N - 1] / geo.dr
        amC[N] = Df[N - 1] * geo.rf[N - 1] / geo.dr
        phiC = np.ones(N + 1)
        Ctry = assemble_solve(geo, phiC, (apC, amC), dt, C, Cinf, 'C', theta=theta)
        Cnew = omega * Ctry + (1.0 - omega) * Cit
        den = max(1.0, float(np.max(np.abs(Cnew))))
        if float(np.max(np.abs(Cnew - Cit))) / den < tol:
            Cit = Cnew
            break
        Cit = Cnew
    return Tn, Cit


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


def env_at(t, ta, Ta, Ca):
    if t >= ta[-1]:
        return T_TAIL, C_TAIL
    return float(np.interp(t, ta, Ta)), float(np.interp(t, ta, Ca))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--hours', type=float, default=0.0, help='固定时程（h）；默认事件驱动')
    ap.add_argument('--max-hours', type=float, default=120.0)
    ap.add_argument('--N', type=int, default=80)
    ap.add_argument('--h-inner', type=float, default=1.0 / 32.0)
    ap.add_argument('--out', type=str, default='', help='结果文件（默认 out/result3_INV2.xlsx）')
    args = ap.parse_args()

    N = 20 if args.smoke else args.N
    dr = R0 / N
    geo = Geo(N, dr)
    h_inner = (1.0 / 4.0) if args.smoke else args.h_inner
    nsub = max(1, int(round(DT_OUT / h_inner)))
    hh = DT_OUT / nsub
    COLS = np.arange(0, N + 1, 4)

    ta, Ta, Ca = load_att1()

    say('=' * 84)
    say('IN-2 | 独立实现互验轨：Crank–Nicolson ＋ Rannacher（创新副本 · 只验不替）')
    say('=' * 84)
    say('[SCALE] N=%d Δr=%.4f mm 内部步=%.6f s（每输出步 %d 子步）格式=CN(θ=0.5)＋Rannacher'
        % (N, dr * 1e3, hh, nsub))
    say('        模式=%s；**与 q3_core 不共享任何函数**'
        % ('冒烟 1 h' if args.smoke else ('固定 %.1f h' % args.hours if args.hours > 0
                                        else '事件驱动（熔断 %.0f h）' % args.max_hours)))

    T = np.full(N + 1, 28.0)
    C = np.full(N + 1, 2.55)

    t = 0.0
    t_max = 3600.0 if args.smoke else (args.hours * 3600.0 if args.hours > 0
                                       else args.max_hours * 3600.0)
    rows = []
    wall0 = time.time()
    t_end = None
    n_out = 0

    while t < t_max - 1e-12:
        t_start = t
        Tp, Cp = T.copy(), C.copy()
        for s in range(nsub):
            ts = t_start + (s + 1) * hh
            Tinf, Cinf = env_at(ts, ta, Ta, Ca)
            # Rannacher 启动：前 2 个子步用后向欧拉（θ=1）且步长减半
            if t_start < 1e-9 and s < 2:
                T, C = step(geo, T, C, hh / 2.0, Cinf, Tinf, theta=1.0)
                T, C = step(geo, T, C, hh / 2.0, Cinf, Tinf, theta=1.0)
            else:
                T, C = step(geo, T, C, hh, Cinf, Tinf, theta=0.5)
        t = t_start + DT_OUT
        n_out += 1
        rows.append(C[COLS].copy())
        if float(np.max(C)) < C_CRIT:
            # 本输出步内线性回溯（用固定 hh 细分）
            lo, hi = 1, nsub
            while lo < hi:
                mid = (lo + hi) // 2
                Tm, Cm = Tp.copy(), Cp.copy()
                for s in range(mid):
                    ts = t_start + (s + 1) * hh
                    Tinf, Cinf = env_at(ts, ta, Ta, Ca)
                    Tm, Cm = step(geo, Tm, Cm, hh, Cinf, Tinf, theta=0.5)
                if float(np.max(Cm)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = t_start + lo * hh
            say('  ★ 达标：t = %.3f s = %.4f h' % (t_end, t_end / 3600.0))
            break
        if n_out % 60 == 0:
            say('  t=%7.2f h  C(0)=%.6f  C(R)=%.6f  wall=%.0fs'
                % (t / 3600.0, C[0], C[-1], time.time() - wall0))

    wall = time.time() - wall0
    say('-' * 84)
    say('  完成：%d 个输出步；墙钟 %.1f s（%.1f min）' % (n_out, wall, wall / 60))

    if not args.smoke:
        XLSX = args.out if args.out else os.path.join(OUTDIR, 'result3_INV2.xlsx')
        wb = Workbook(write_only=True)
        ws = wb.create_sheet('Sheet1')
        ws.append(['时间\\到药材中心的距离'] + ['%.1f' % (c * dr * 100) for c in COLS])
        for i, r in enumerate(rows):
            ws.append([(i + 1) * DT_OUT] + [round(float(v), 4) for v in r])
        wb.save(XLSX)
        say('  已写出：%s（%d 行 × %d 列）' % (XLSX, len(rows), len(COLS) + 1))
        arr = np.array(rows)
        dC = np.diff(arr, axis=0)
        say('  [断言] 非负=%s 中心单调=%s 不超初值=%s'
            % (bool(np.min(arr) >= 0), bool(np.all(dC[:, 0] <= 1e-9)),
               bool(np.max(arr) <= 2.55 + 1e-4)))
        with open(os.path.join(OUTDIR, 'fig_q3_INV2_e3.csv'), 'w', encoding='utf-8') as f:
            f.write('t_s,C_center,C_surface\n')
            for i, r in enumerate(rows):
                f.write('%d,%.6f,%.6f\n' % ((i + 1) * DT_OUT, r[0], r[-1]))

    with open(os.path.join(LOGDIR, 'q3_INV2_e3.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    say('  已写出日志：logs/q3_INV2_e3.log')


if __name__ == '__main__':
    main()
