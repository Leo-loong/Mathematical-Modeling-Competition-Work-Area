# -*- coding: utf-8 -*-
"""A 题 Q1 · 时间方向**精确推进**模块（创新化路径 T3）
=========================================================
思路（Q1 独有红利：T 方程为**线性常系数**、C 方程非线性**仅**来自 D(C)）

  半离散后：  dψ/dt = A ψ + κ·g(t)·e_N ,  g(t)=环境量（附件1 分段线性）
  解析解  ：  ψ_{n+1} = E ψ_n + ∫_0^h e^{A(h-s)} b(t_n+s) ds ,  E = e^{Ah}
  b 分段线性 ⟹ 积分**闭式**：  ∫ = g_n·w0 + (g_{n+1}-g_n)·w1
              w0 = κ·G0 e_N ,  w1 = κ·G1 e_N
              G0 = A^{-1}(E-I) ,  G1 = A^{-2}(E-I-Ah)

  实现用**增广矩阵**一次算齐（避免求逆）：
      expm([[A, e_N, e_N],[0,0,0],[0,0,0]]·h) 的右上两块 ⟹ G0 e_N 与 h·G1 e_N

  ⟹ 时间方向**零离散误差**（仅剩空间离散）；h 可在数据节点步长内任意取（1 s 或 60 s）。
  性质：A 为非奇异 M 矩阵、非对角元 ≥0、A·1 = −κ e_N ≤ 0 ⟹ E ≥ 0 且 E·1 ≤ 1（次随机）
        ⟹ 当边界值非负时，解为初值与边界值的凸组合（离散极值原理在**连续时间层面**成立）。

C 方程（T3-2）：每个子步内**冻结 D**（界面仍取口径 M6「沿 C 的积分平均」），
  则该子步同为零性常系数问题，用同一机制精确推进，再做少量 Picard 校正。

约定：本文件不引用、不记载任何资料中的日期。
"""
import numpy as np
from scipy.linalg import expm

import q1_core as core


# --------------------------------------------------------------- 装配（ODE 形式）
def assemble_T_ode(N, dr, p, center='fv', surf='fvm'):
    """半离散 T 方程 dT/dt = A T + κ·T∞(t)·e_N；返回 (A, κ)。
    与 `q1_core.assemble_T` 的后向欧拉格式**同源**（同一元体平衡算子）。"""
    rho, cp = p['rho'], p['cp']
    k = p['k'] * p.get('kfac', 1.0)
    h, R0 = p['h'], p['R0']
    r = np.arange(N + 1) * dr
    A = np.zeros((N + 1, N + 1))
    # 中心：元体平衡几何式与洛必达极限式给出**同一**算子 4k/(ρc_p Δr²)
    A[0, 0] = -4.0 * k / (rho * cp * dr ** 2)
    A[0, 1] = +4.0 * k / (rho * cp * dr ** 2)
    for i in range(1, N):
        rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
        den = rho * cp * r[i] * dr ** 2
        A[i, i - 1] = k * rl / den
        A[i, i] = -k * (rl + rr) / den
        A[i, i + 1] = k * rr / den
    if surf == 'fvm':
        VN = dr * (R0 - dr / 4.0) / 2.0
        rad = R0 - dr / 2.0
    else:
        VN = R0 * dr / 2.0
        rad = R0
    A[N, N - 1] = k * rad / (rho * cp * VN * dr)
    A[N, N] = -(k * rad / dr + h * R0) / (rho * cp * VN)
    return A, h * R0 / (rho * cp * VN)


def assemble_C_ode(N, dr, Df, R0, km):
    """半离散 C 方程 dC/dt = A_C C + η·C∞(t)·e_N（冻结界面系数 Df）；返回 (A, η)。"""
    r = np.arange(N + 1) * dr
    A = np.zeros((N + 1, N + 1))
    V0, A12 = dr * dr / 4.0, dr
    A[0, 0] = -(Df[0] * A12 / dr) / V0
    A[0, 1] = +(Df[0] * A12 / dr) / V0
    for i in range(1, N):
        rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
        den = r[i] * dr ** 2
        A[i, i - 1] = Df[i - 1] * rl / den
        A[i, i] = -(Df[i] * rr + Df[i - 1] * rl) / den
        A[i, i + 1] = Df[i] * rr / den
    VN = dr * (R0 - dr / 4.0) / 2.0
    rad = R0 - dr / 2.0
    A[N, N - 1] = Df[N - 1] * rad / (VN * dr)
    A[N, N] = -(Df[N - 1] * rad / dr + km * R0) / VN
    return A, km * R0 / VN


def etd_prop(A, kappa, h):
    """返回 (E, w0, w1) 使 ψ_{n+1} = E ψ_n + g_n·w0 + (g_{n+1}-g_n)·w1（b=κ·g·e_N）。

    增广矩阵须带**线性项的 Jordan 链**（右下 [[0,1],[0,0]]）：
        M = [[A, e_N, 0],[0, 0, 1],[0, 0, 0]]  （n = N+1 个节点，e_N 位于第 n-1 行）
      ⟹ expm(M·h) 的右上两块给出
        X[:n, n]   = ∫_0^h e^{A(h-s)} ds · e_N = G0 e_N
        X[:n, n+1] = ∫_0^h e^{A(h-s)} s ds · e_N = h·G1 e_N
    （若把第三列也填 e_N，则两块**都**退化为 G0 e_N ⟹ 格式不再是精确积分——已修正。）
    """
    n = A.shape[0]
    M = np.zeros((n + 2, n + 2))
    M[:n, :n] = A
    M[n - 1, n] = 1.0          # u = e_N（最后一个节点）
    M[n, n + 1] = 1.0          # Jordan 链 ⟹ 线性项
    X = expm(M * h)
    return X[:n, :n], kappa * X[:n, n], kappa * X[:n, n + 1] / h


# --------------------------------------------------------------------- T 精确推进
def run_T_expm(N, dr, p, Tenv_fn, t_end, hstep=1.0, center='fv', surf='fvm',
               t_snaps=(), knot_dt=60.0, cols=None, dt_out=None):
    """T 方程时间精确推进。T∞ 为附件1 分段线性 ⟹ **无时间离散误差**。

    **关键**：步长必须在「数据节点（knot_dt 的倍数）」与「快照时刻」处**切分**——
    否则一步跨越节点会横跨两段线性区（函数有折点）⟹ 闭式积分不再成立、h 相关性出现。
    cols 非 None 时按 dt_out 逐行收集整表（形状 (n, len(cols))）。
    返回 dict: T_snap（按 t_snaps）、table、E、hstep、nstep、nprop。
    """
    n = N + 1
    A, kappa = assemble_T_ode(N, dr, p, center, surf)
    E, w0, w1 = etd_prop(A, kappa, hstep)
    T = np.full(n, p['T0'])
    snaps = {0.0: T.copy()}
    table = None
    if cols is not None:
        dt_out = 1.0 if dt_out is None else float(dt_out)
        nrow = int(round(t_end / dt_out))
        table = np.zeros((nrow, len(cols)))
    cuts = set()
    for step in (knot_dt, hstep, dt_out):
        if not step:
            continue
        k = 0
        while k * step < t_end - 1e-12:
            cuts.add(round(k * step, 9))
            k += 1
    for x in t_snaps:
        cuts.add(round(float(x), 9))
    cuts.add(round(float(t_end), 9))
    grid = sorted(x for x in cuts if x <= t_end + 1e-12)
    snapset = set(round(float(x), 9) for x in t_snaps) | {round(float(t_end), 9)}
    # 传播子 (E, w0, w1) **依赖步长** ⟹ 按实际步长取，并对同长度步长缓存复用
    pcache = {round(hstep, 9): (E, w0, w1)}
    for a, b in zip(grid[:-1], grid[1:]):
        hh = round(b - a, 9)
        if hh not in pcache:
            pcache[hh] = etd_prop(A, kappa, hh)
        Ee, ww0, ww1 = pcache[hh]
        ga, gb = float(Tenv_fn(a)), float(Tenv_fn(b))
        T = Ee @ T + ga * ww0 + (gb - ga) * ww1
        if round(b, 9) in snapset:
            snaps[round(b, 9)] = T.copy()
        if table is not None:
            nr = int(round(b / dt_out))
            if abs(b - nr * dt_out) < 1e-9 and 1 <= nr <= table.shape[0]:
                table[nr - 1, :] = T[cols]
    return dict(T_end=T, T_snap=snaps, table=table, A=A, kappa=kappa,
                E=pcache[round(hstep, 9)][0], nstep=len(grid) - 1,
                nprop=len(pcache), hstep=hstep)


# --------------------------------------------------------------------- C 精确推进
def run_C_etd(N, dr, p, Cenv_fn, t_end, h_step=1.0, dt_col=1.0, maxit=30,
              Dfac=1.0, tol=1e-9, snap_at=(), cols=None, T0_C=None, knot_dt=60.0):
    """C 方程 ETD：每子步冻结 D（界面口径 M6）→ 精确推进 → Picard 迭代至收敛。

    子步同样在**数据节点**与**快照时刻**处切分（保证每步内 C∞ 线性）。
    收敛判据与主力**同口径**（相对残差 < tol，上限 maxit）——但残差按**相邻两次迭代**之差计算。
    """
    n = N + 1
    C = np.full(n, p['C0'] if T0_C is None else T0_C)
    snaps = {0.0: C.copy()}
    rows = [] if cols is not None else None
    tot_it, mx_res, nsub = 0, 0.0, 0
    cuts = set()
    k = 0
    while k * knot_dt < t_end - 1e-12:
        cuts.add(round(k * knot_dt, 9)); k += 1
    k = 0
    while k * h_step < t_end - 1e-12:
        cuts.add(round(k * h_step, 9)); k += 1
    for x in snap_at:
        cuts.add(round(float(x), 9))
    grid = sorted(x for x in cuts if x <= t_end + 1e-12)
    if grid[0] != 0.0:
        grid.insert(0, 0.0)
    snapset = set(round(float(x), 9) for x in snap_at)
    for gi in range(len(grid) - 1):
        ts, nxt = grid[gi], grid[gi + 1]
        ca, cb = float(Cenv_fn(ts)), float(Cenv_fn(nxt))
        hh = nxt - ts
        Ccur = C.copy()
        for it in range(1, maxit + 1):
            Df = core.faceD_int(Ccur, p['D0'], p['bD'], Dfac)
            A, eta = assemble_C_ode(N, dr, Df, p['R0'], p['km'])
            E, w0, w1 = etd_prop(A, eta, hh)
            Cnew = E @ C + ca * w0 + (cb - ca) * w1
            # 真正的 Picard 残差：**相邻两次迭代**之差（非"本步变化量"）
            res = float(np.max(np.abs(Cnew - Ccur))) / max(1.0, float(np.max(np.abs(Cnew))))
            Ccur = Cnew
            tot_it += 1
            mx_res = max(mx_res, res)
            if res < tol:
                break
        C = Ccur
        nsub += 1
        ts = nxt
        if snap_at and any(abs(ts - s) < 1e-9 for s in snap_at):
            snaps[round(ts, 9)] = C.copy()
        if rows is not None:
            nc = int(round(ts / dt_col))
            if abs(ts - nc * dt_col) < 1e-9:
                rows.append((nc, C[cols].copy()))
    return dict(C_end=C, C_snap=snaps, rows=rows,
                stats=dict(total_it=tot_it, avg_it=tot_it / max(1, nsub),
                           max_res=mx_res, nsub=nsub))
