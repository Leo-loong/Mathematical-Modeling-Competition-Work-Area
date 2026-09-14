# -*- coding: utf-8 -*-
"""
A 题 Q1 求解核（配置化）—— 主力求解与全部检验实验共用
======================================================
统一口径
--------
· 空间    ：元体平衡（有限体积）＋ 三对角追赶法
· 时间    ：**温度＝时间方向精确推进**（矩阵指数＋分段线性 Duhamel，见 `q1_exact.py`；
            本核经 `tmethod='expm'` 调用，**无时间离散误差**）
            其余（Q1 含水率、Q2–Q4 全部场量）＝全隐式（后向欧拉）
· 中心    ：两条**真正独立**的装配路径，经同一尺度归一化后逐系数比对
            center='fv' —— 用中心控制体体积 V0=Δr²/4 与界面面积 A12=Δr 显式装配
            center='lh' —— 洛必达极限 (1/r)∂r(r∂rT) → 2∂r²T 的差分离散
· 表面    ：surf='fvm'   —— 元体平衡半格（主力）
            surf='ghost' —— **一阶近似口径**（体积取 R0·Δr/2、导热界面取 R0）；
                            **仅**用于边界口径对照实验。⚠ 命名沿用历史，
                            **其实现并非"虚拟节点＋中心差分"**（原虚拟节点装配符号有误、已改）
· 非线性  ：D(C) 单因子；Picard 迭代＋欠松弛；时间导数右端**固定取上一时层解**
· 解耦    ：先全程解 T，再全程解 C（T 方程不含 C，D 不含 T）
退化与灵敏度
------------
· kfac / Dfac：物性缩放因子（0.0 → 退化自检；1±0.2 → 灵敏度 OAT）
· 环境条件以函数传入（常数环境用于 E2 解析对拍与退化自检）

约定：本核不引用、不记载任何资料中的日期。
"""
import time
import numpy as np

DEF = dict(R0=0.02, rho=820.0, cp=2600.0, k=0.36, h=25.0, km=8.0e-7,
           D0=7.0e-9, bD=0.89, T0=28.0, C0=2.55)

V0_OF = staticmethod(lambda dr: dr * dr / 4.0)          # 中心控制体体积（π 已约去）
VN_OF = staticmethod(lambda dr, R0: dr * (R0 - dr / 4.0) / 2.0)  # 表面控制体体积


def thomas(a, b, c, d):
    """三对角追赶法（a/b/c 为下/主/上对角，a[0] 与 c[-1] 不使用）"""
    n = len(b)
    cp_ = np.empty(n - 1, dtype=float)
    dp_ = np.empty(n, dtype=float)
    cp_[0] = c[0] / b[0]
    dp_[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp_[i - 1]
        dp_[i] = (d[i] - a[i] * dp_[i - 1]) / m
        if i < n - 1:
            cp_[i] = c[i] / m
    x = np.empty(n, dtype=float)
    x[-1] = dp_[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp_[i] - cp_[i] * x[i + 1]
    return x


def thomas_prep(a, b, c):
    """常数系数三对角矩阵的预消元（前向消元结果与 d 无关，可复用）"""
    n = len(b)
    cp_ = np.empty(n - 1, dtype=float)
    inv = np.empty(n, dtype=float)
    cp_[0] = c[0] / b[0]
    inv[0] = 1.0 / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp_[i - 1]
        inv[i] = 1.0 / m
        if i < n - 1:
            cp_[i] = c[i] / m
    return cp_, inv


def thomas_solve_prep(a, cp_, inv, d):
    """配合 thomas_prep 使用的快速求解（与 thomas 同式，仅省去重复除法）"""
    n = len(d)
    dp_ = np.empty(n, dtype=float)
    dp_[0] = d[0] * inv[0]
    for i in range(1, n):
        dp_[i] = (d[i] - a[i] * dp_[i - 1]) * inv[i]
    x = np.empty(n, dtype=float)
    x[-1] = dp_[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp_[i] - cp_[i] * x[i + 1]
    return x


def D_of(C, D0=DEF['D0'], bD=DEF['bD']):
    """有效水分扩散系数 D(C) = D0·exp(-bD/C)"""
    return D0 * np.exp(-bD / np.maximum(np.asarray(C, dtype=float), 1e-9))


def harm(dl, dr_):
    """界面系数：距离加权调和平均（D≡0 时退化为 0，避免除零）。

    ⚠ **本函数已不用于生产路径**：C 方程的界面扩散系数改由 `faceD_int`
      （**沿 $C$ 的积分平均**，口径 **M6**）生成；本函数**仅保留作旧口径对照**。
    """
    if dl <= 0.0 or dr_ <= 0.0:
        return 0.0
    return 2.0 / (1.0 / dl + 1.0 / dr_)


# ----------------------------------------------------------------- T 方程
def assemble_T(N, dr, dt, p, center='fv', surf='fvm'):
    """装配后向欧拉 T 方程系数 (a, b, c, meta)；右端另由 rhs_T 生成"""
    rho, cp = p['rho'], p['cp']
    k = p['k'] * p.get('kfac', 1.0)
    h, R0 = p['h'], p['R0']
    r = np.arange(N + 1) * dr
    a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    meta = {}

    # --- 中心节点：两条独立路径，均归一化到"单位体积"以便逐系数比对 ---
    if center == 'fv':
        V0 = dr * dr / 4.0
        A12 = dr
        b[0] = (rho * cp * V0 / dt + k * A12 / dr) / V0
        c[0] = (-k * A12 / dr) / V0
        meta['center_scale'] = V0
    elif center == 'lh':
        d2 = 2.0 / dr ** 2
        b[0] = rho * cp / dt + 2.0 * k * d2
        c[0] = -2.0 * k * d2
        meta['center_scale'] = 1.0
    else:
        raise ValueError(center)
    meta['center_row'] = (float(b[0]), float(c[0]))

    # --- 内部节点：标准元体平衡（含 r_{i±1/2} 几何权重） ---
    for i in range(1, N):
        rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
        b[i] = rho * cp * r[i] / dt + k * (rr + rl) / dr ** 2
        a[i] = -k * rl / dr ** 2
        c[i] = -k * rr / dr ** 2

    # --- 表面节点 ---
    if surf == 'fvm':
        VN = dr * (R0 - dr / 4.0) / 2.0
        b[N] = rho * cp * VN / dt + k * (R0 - dr / 2.0) / dr + h * R0
        a[N] = -k * (R0 - dr / 2.0) / dr
        meta['surf'] = 'fvm'
    elif surf == 'ghost':
        # 对照口径（**仅用于边界离散敏感性对照**）：
        # 表面控制体体积取一阶近似 R0·Δr/2（忽略曲率），导热界面半径取 R0
        VNa = R0 * dr / 2.0
        b[N] = rho * cp * VNa / dt + k * R0 / dr + h * R0
        a[N] = -k * R0 / dr
        meta['surf'] = 'approx'
    else:
        raise ValueError(surf)
    return a, b, c, meta


def rhs_T(N, dr, dt, p, Told, Tinf, surf='fvm'):
    """生成 T 方程右端向量 d"""
    rho, cp = p['rho'], p['cp']
    h, R0 = p['h'], p['R0']
    r = np.arange(N + 1) * dr
    d = np.zeros(N + 1)
    d[0] = rho * cp * Told[0] / dt
    for i in range(1, N):
        d[i] = rho * cp * r[i] * Told[i] / dt
    if surf == 'fvm':
        VN = dr * (R0 - dr / 4.0) / 2.0
        d[N] = rho * cp * VN * Told[N] / dt + h * R0 * Tinf
    else:
        VNa = R0 * dr / 2.0
        d[N] = rho * cp * VNa * Told[N] / dt + h * R0 * Tinf
    return d


# ----------------------------------------------------------------- C 方程
def assemble_C(N, dr, dt, Df, R0, km):
    """装配 C 方程系数 (a, b, c, VN)；Df 为界面扩散系数（长度 N，**沿 $C$ 的积分平均**，由 `faceD_int` 生成）"""
    r = np.arange(N + 1) * dr
    a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    V0 = dr * dr / 4.0
    A12 = dr
    b[0] = (V0 / dt + Df[0] * A12 / dr) / V0
    c[0] = (-Df[0] * A12 / dr) / V0
    for i in range(1, N):
        rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
        b[i] = r[i] / dt + (Df[i] * rr + Df[i - 1] * rl) / dr ** 2
        a[i] = -Df[i - 1] * rl / dr ** 2
        c[i] = -Df[i] * rr / dr ** 2
    VN = dr * (R0 - dr / 4.0) / 2.0
    b[N] = VN / dt + Df[N - 1] * (R0 - dr / 2.0) / dr + km * R0
    a[N] = -Df[N - 1] * (R0 - dr / 2.0) / dr
    return a, b, c, VN


def rhs_C(N, dr, dt, Cold, cinf, R0, km):
    """生成 C 方程右端向量 d（**固定取上一时层解 Cold**）"""
    r = np.arange(N + 1) * dr
    d = np.zeros(N + 1)
    d[0] = Cold[0] / dt
    for i in range(1, N):
        d[i] = r[i] * Cold[i] / dt
    VN = dr * (R0 - dr / 4.0) / 2.0
    d[N] = VN * Cold[N] / dt + km * R0 * cinf
    return d


def faceD_int(Carr, D0, bD, Dfac=1.0, nsamp=8):
    """★修正口径：界面扩散系数取**沿 C 的积分平均** ⟨D⟩=(1/ΔC)∫D dC。

    （原 `harm` 的调和平均仅对"界面处系数间断"成立；系数随 C 陡变时显著失真。）
    """
    C = np.asarray(Carr, dtype=float)
    lo = np.minimum(C[:-1], C[1:])
    hi = np.maximum(C[:-1], C[1:])
    xs = lo[:, None] + (hi - lo)[:, None] * (np.arange(nsamp) + 0.5)[None, :] / nsamp
    xs = np.maximum(xs, 1e-9)
    fv = np.exp(-bD / xs).mean(axis=1)
    flat = (hi - lo) < 1e-14
    if flat.any():
        fv[flat] = np.exp(-bD / np.maximum(lo[flat], 1e-9))
    return D0 * Dfac * fv


def step_C(N, dr, dt, C, cinf, p, omega=0.7, tol=1e-9, maxit=30, Dfac=1.0,
           dmode='func'):
    """推进一个 C 子步：Picard 迭代＋欠松弛。返回 (C_new, iters, res)

    dmode='func' ：D = D(C) 单因子非线性（主力）
    dmode='const'：D ≡ D(C0)（用于 E2 解析对拍；此时单次迭代即收敛）
    """
    Cold = C.copy()
    Cit = C.copy()
    res = None
    it = 0
    Dconst = p['D0'] * np.exp(-p['bD'] / p['C0']) * Dfac
    for it in range(1, maxit + 1):
        if dmode == 'const':
            Df = np.full(N, Dconst)
        else:
            Df = faceD_int(Cit, p['D0'], p['bD'], Dfac)
        a, b, c, _ = assemble_C(N, dr, dt, Df, p['R0'], p['km'])
        d = rhs_C(N, dr, dt, Cold, cinf, p['R0'], p['km'])
        Ctry = thomas(a, b, c, d)
        Cnew = omega * Ctry + (1.0 - omega) * Cit
        res = float(np.max(np.abs(Cnew - Cit))) / max(1.0, float(np.max(np.abs(Cnew))))
        Cit = Cnew
        if res < tol:
            break
    return Cit, it, res


# ----------------------------------------------------------------- 驱动
def run_sim(N, dr, dt_out, nsteps, p, Tenv_fn, Cenv_fn, sub=10, subT=1,
            center='fv', surf='fvm', kfac=1.0, Dfac=1.0, dmode='func',
            tol=1e-9, omega=0.7, maxit=30, snap_at=(), out_idx=None,
            solve_T=True, solve_C=True, tmethod='expm'):
    """统一求解驱动。

    参数
    ----
    N, dr      : 空间区间数与步长（节点数 N+1）
    dt_out     : 输出时间步长（s）
    nsteps     : 输出步数（总时长 = nsteps·dt_out）
    p          : 物性/几何参数字典（见 DEF）
    Tenv_fn    : T∞(t) 函数；Cenv_fn: C∞(t) 函数
    sub        : C 方程内部子步数（内部步长 = dt_out/sub）
    subT       : T 方程内部子步数（内部步长 = dt_out/subT，用于时间收敛实验）
    out_idx    : 需要收集的列索引（None → 不收集整表）
    返回 dict
    """
    p = dict(p)
    p['kfac'] = kfac
    R0 = p['R0']
    r = np.arange(N + 1) * dr
    dt_int = dt_out / float(sub)
    dtT = dt_out / float(subT)

    res = dict(N=N, dr=dr, dt_out=dt_out, dt_int=dt_int, sub=sub,
               center=center, surf=surf, kfac=kfac, Dfac=Dfac)

    # ---------------- T ----------------
    Tend = None
    Tsnap = {}
    res['tmethod'] = tmethod
    if solve_T:
        a, b, c, meta = assemble_T(N, dr, dtT, p, center, surf)
        res['center_row'] = meta['center_row']
        t0 = time.time()
        if tmethod == 'expm':
            # 时间方向**精确推进**（交付口径）：矩阵指数 ＋ 分段线性 Duhamel
            import q1_exact as _ex
            rT = _ex.run_T_expm(N, dr, p, Tenv_fn, nsteps * dt_out,
                                hstep=dt_out, center=center, surf=surf,
                                t_snaps=[n * dt_out for n in snap_at])
            Tsnap[0] = np.full(N + 1, p['T0'])
            for n in snap_at:
                Tsnap[n] = rT['T_snap'][round(float(n * dt_out), 9)].copy()
            T = rT['T_end']
        else:
            cp_, inv = thomas_prep(a, b, c)
            T = np.full(N + 1, p['T0'])
            Tsnap[0] = T.copy()
            for n in range(1, nsteps + 1):
                for s in range(subT):
                    ts = (n - 1) * dt_out + (s + 1) * dtT
                    d = rhs_T(N, dr, dtT, p, T, float(Tenv_fn(ts)), surf)
                    T = thomas_solve_prep(a, cp_, inv, d)
                if n in snap_at:
                    Tsnap[n] = T.copy()
        res['T_time'] = time.time() - t0
        Tend = T.copy()
    res['T_end'] = Tend
    res['T_snap'] = Tsnap

    # ---------------- C ----------------
    Cend = None
    Csnap = {}
    stats = dict(total_it=0, avg_it=0.0, max_it=0, max_res=0.0, nsub=0)
    if solve_C:
        C = np.full(N + 1, p['C0'])
        Csnap[0] = C.copy()
        tot, mx, mxr, nsub = 0, 0, 0.0, 0
        t0 = time.time()
        for n in range(1, nsteps + 1):
            for s in range(sub):
                tt = (n - 1) * dt_out + (s + 1) * dt_int
                cinf = float(Cenv_fn(tt))
                C, it, rr = step_C(N, dr, dt_int, C, cinf, p, omega, tol, maxit, Dfac, dmode)
                tot += it; mx = max(mx, it); mxr = max(mxr, rr); nsub += 1
            if n in snap_at:
                Csnap[n] = C.copy()
        res['C_time'] = time.time() - t0
        Cend = C.copy()
        stats.update(total_it=tot, avg_it=tot / max(1, nsub), max_it=mx,
                     max_res=mxr, nsub=nsub)
    res['C_end'] = Cend
    res['C_snap'] = Csnap
    res['stats'] = stats
    return res


def run_sim_collect(N, dr, dt_out, nsteps, p, Tenv_fn, Cenv_fn, sub=10, subT=1,
                    center='fv', surf='fvm', kfac=1.0, Dfac=1.0, dmode='func',
                    tol=1e-9, omega=0.7, maxit=30, cols=None,
                    snap_at=(), solve_T=True, solve_C=True, tmethod='expm'):
    """单遍运行并**同时**收集整表输出与快照（替代"两遍计算"）。

    cols: 需要写出的列索引（如 np.arange(0, N+1, 4)），None 表示不收集
    返回 (res, tableT, tableC)；tableT/C 形状为 (nsteps, len(cols))
    """
    p = dict(p)
    p['kfac'] = kfac
    R0 = p['R0']
    r = np.arange(N + 1) * dr
    dt_int = dt_out / float(sub)
    dtT = dt_out / float(subT)
    ncol = 0 if cols is None else len(cols)

    tableT = np.zeros((nsteps, ncol)) if (cols is not None and solve_T) else None
    tableC = np.zeros((nsteps, ncol)) if (cols is not None and solve_C) else None
    Tsnap, Csnap = {}, {}
    res = dict(N=N, dr=dr, dt_out=dt_out, dt_int=dt_int, sub=sub,
               center=center, surf=surf, kfac=kfac, Dfac=Dfac)

    Tprep = None
    res['tmethod'] = tmethod
    use_expm_T = bool(solve_T and tmethod == 'expm')
    if solve_T:
        aT, bT, cT, meta = assemble_T(N, dr, dtT, p, center, surf)
        res['center_row'] = meta['center_row']
        if use_expm_T:
            import q1_exact as _ex
            rT = _ex.run_T_expm(N, dr, p, Tenv_fn, nsteps * dt_out, hstep=dt_out,
                                center=center, surf=surf,
                                t_snaps=[n * dt_out for n in snap_at],
                                cols=cols, dt_out=dt_out)
            tableT = rT['table']
            T = rT['T_end']
            Tsnap[0] = np.full(N + 1, p['T0'])
            for n in snap_at:
                Tsnap[n] = rT['T_snap'][round(float(n * dt_out), 9)].copy()
            tT = 0.0
        else:
            cpT, invT = thomas_prep(aT, bT, cT)
            Tprep = (aT, cpT, invT)
            T = np.full(N + 1, p['T0'])
            Tsnap[0] = T.copy()

    C = np.full(N + 1, p['C0']) if solve_C else None
    Csnap[0] = C.copy() if C is not None else None

    tot, mx, mxr, nsub = 0, 0, 0.0, 0
    tT = tC = 0.0
    for n in range(1, nsteps + 1):
        if solve_T and not use_expm_T:
            t0 = time.time()
            a, cp_, inv = Tprep
            for s in range(subT):
                ts = (n - 1) * dt_out + (s + 1) * dtT
                d = rhs_T(N, dr, dtT, p, T, float(Tenv_fn(ts)), surf)
                T = thomas_solve_prep(a, cp_, inv, d)
            tT += time.time() - t0
            if n in snap_at:
                Tsnap[n] = T.copy()
            if cols is not None:
                tableT[n - 1, :] = T[cols]
        if solve_C:
            t0 = time.time()
            for s in range(sub):
                tt = (n - 1) * dt_out + (s + 1) * dt_int
                C, it, rr = step_C(N, dr, dt_int, C, float(Cenv_fn(tt)), p,
                                   omega, tol, maxit, Dfac, dmode)
                tot += it; mx = max(mx, it); mxr = max(mxr, rr); nsub += 1
            tC += time.time() - t0
            if n in snap_at:
                Csnap[n] = C.copy()
            if cols is not None:
                tableC[n - 1, :] = C[cols]

    res['T_end'] = T.copy() if solve_T else None
    res['C_end'] = C.copy() if solve_C else None
    res['T_snap'] = Tsnap
    res['C_snap'] = Csnap
    res['T_time'] = tT
    res['C_time'] = tC
    res['stats'] = dict(total_it=tot, avg_it=tot / max(1, nsub), max_it=mx,
                        max_res=mxr, nsub=nsub)
    return res, tableT, tableC
