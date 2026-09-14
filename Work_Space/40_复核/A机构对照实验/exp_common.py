# -*- coding: utf-8 -*-
"""
A 题 · 机构材料 vs 我方结果 · 复核实验公共模块（只读我方文件，不改动任何求解文件）
=================================================================================
用途：为"机构材料第一手内容"与"我方求解结果"的分歧点提供可复现的实验判据。

本模块只做两件事：
  1) 读附件（题目原始数据）；
  2) 提供若干**独立实现**的求解器内核，用于交叉验证：
       - explicit_fv  : 复刻机构《高质量成品论文》的显式有限差分/有限体积格式
                        （空间一阶边界节点 + 准稳态 Robin；界面系数可选算术/调和/积分平均）
       - implicit_fv  : 我方口径的元体平衡 + 全隐式 + 半格表面控制体
                        （与 q1_core / q2_core 结构一致，但**另写一份**用于对照）
       - bdf_mol      : 第三方路径——method-of-lines + scipy BDF 变步长隐式积分
                        （与以上两者算法完全不同，作高精度参考解）
  3) 提供半无限介质 Robin 解析解（erfc 公式）作早期时刻的解析基准。

约定：本目录只写本目录下的文件；不触碰 11_建模 / 20_交付包 中的任何求解文件。
"""
import os
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.special import erfc

HERE = os.path.dirname(os.path.abspath(__file__))


def find_root(p=None, marker='10_赛题', _max=8):
    cur = p or HERE
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
        par = os.path.dirname(cur)
        if par == cur:
            break
        cur = par
    raise RuntimeError('未找到工作区根')


ROOT = find_root()
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx')
ATT2 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件2.xlsx')


# ---------------------------------------------------------------- 附件读取
def load_att1():
    import openpyxl
    wb = openpyxl.load_workbook(ATT1, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    rows = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in rows])
    T = np.array([float(r[1]) for r in rows])
    C = np.array([float(r[2]) for r in rows])
    return t, T, C


def load_att2():
    import openpyxl
    wb = openpyxl.load_workbook(ATT2, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    rows = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in rows])
    R = np.array([float(r[1]) for r in rows])
    return t, R


T1, TAIR, CAIR = load_att1()


# ---------------------------------------------------------------- 边界插值方式
def make_env(kind='linear', t_ext=14400.0, T_ext=50.00, C_ext=0.04999):
    """返回 (Tenv, Cenv) 两个函数。

    kind='linear' : 我方口径（L3-06）：np.interp，节点严格复现原值
    kind='pchip'  : 机构《高质量成品论文》《A题代码》《GT02》口径：分段三次 Hermite
    kind='expfit' : 机构《GT05》口径：约束拉伸指数模型（参数取自其源码）
    """
    if kind == 'linear':
        def Te(t):
            return float(np.interp(t, T1, TAIR)) if t <= t_ext else T_ext

        def Ce(t):
            return float(np.interp(t, T1, CAIR)) if t <= t_ext else C_ext
        return Te, Ce

    if kind == 'pchip':
        pT = PchipInterpolator(T1, TAIR)
        pC = PchipInterpolator(T1, CAIR)

        def Te(t):
            return float(pT(t)) if t <= t_ext else T_ext

        def Ce(t):
            return float(pC(t)) if t <= t_ext else C_ext
        return Te, Ce

    if kind == 'expfit':
        # GT05 源码给出的参数（y∞, y0, tau, beta）
        pT = (50.0164, 28.0, 1884.0, 1.150)
        pC = (0.05009, 0.01963, 2703.0, 1.271)

        def _f(p, t):
            y_inf, y0, tau, beta = p
            return y_inf - (y_inf - y0) * np.exp(-(np.asarray(t, float) / tau) ** beta)

        def Te(t):
            return float(_f(pT, t)) if t <= t_ext else T_ext

        def Ce(t):
            return float(_f(pC, t)) if t <= t_ext else C_ext
        return Te, Ce

    raise ValueError(kind)


# ---------------------------------------------------------------- 物性
def props_q1(C):
    C = np.maximum(np.asarray(C, float), 1e-12)
    rho = np.full_like(C, 820.0)
    cp = np.full_like(C, 2600.0)
    k = np.full_like(C, 0.36)
    D = 7e-9 * np.exp(-0.89 / C)
    return rho, cp, k, D


def props_q2(C, Tc):
    C = np.maximum(np.asarray(C, float), 1e-12)
    Tk = np.asarray(Tc, float) + 273.15
    rho = 650.0 + 128.0 * C
    cp = 1450.0 + 2736.0 * C / (C + 1.0)
    k = 0.21 + 0.38 * C / (C + 1.0)
    D = 2.4e-3 * np.exp(-0.45 / C) * np.exp(-3850.0 / Tk)
    return rho, cp, k, D


def props_q4(C, Tc):
    C = np.maximum(np.asarray(C, float), 1e-12)
    Tk = np.asarray(Tc, float) + 273.15
    rho = 760.0 + 90.0 * C
    cp = 1850.0 + 2150.0 * C / (C + 1.0)
    k = 0.12 + 0.20 * C / (C + 1.0)
    D = 4.2e-4 * np.exp(-0.30 / C) * np.exp(-3850.0 / Tk)
    return rho, cp, k, D


def iface(coef, mode='arith', bD=None, D0=None, Carr=None, nsamp=8):
    """界面系数：'arith' 算术平均｜'harm' 调和平均｜'integral' 沿 C 的积分平均"""
    a, b = coef[:-1], coef[1:]
    if mode == 'arith':
        return 0.5 * (a + b)
    if mode == 'harm':
        return 2.0 * a * b / np.maximum(a + b, 1e-300)
    if mode == 'integral':
        C = np.asarray(Carr, float)
        lo = np.minimum(C[:-1], C[1:])
        hi = np.maximum(C[:-1], C[1:])
        xs = lo[:, None] + (hi - lo)[:, None] * (np.arange(nsamp) + 0.5)[None, :] / nsamp
        xs = np.maximum(xs, 1e-12)
        fv = np.exp(-bD / xs).mean(axis=1)
        flat = (hi - lo) < 1e-14
        if flat.any():
            fv[flat] = np.exp(-bD / np.maximum(lo[flat], 1e-12))
        return D0 * fv
    raise ValueError(mode)


# ---------------------------------------------------------------- 显式格式（复刻机构成品论文）
def explicit_fv(N, R0, dt, nsteps, dt_out, Te, Ce, prop='q1',
                surf='quasi', ifmode='arith', quasi_use_new=True,
                snap=None, cols_idx=None, store_all=False):
    """显式（前向欧拉）有限体积，复刻机构《2026国赛A题高质量成品论文！》的离散：

    内部节点 i=1..N-1：
        T_i^{n+1} = T_i^n + (dt/(rho cp r_i dr^2)) * [ r_{i+1/2} k_{i+1/2}(T_{i+1}-T_i)
                                                        - r_{i-1/2} k_{i-1/2}(T_i-T_{i-1}) ]
        C_i^{n+1} = C_i^n + (dt/(r_i dr^2)) * [ r_{i+1/2} D_{i+1/2}(C_{i+1}-C_i)
                                                 - r_{i-1/2} D_{i-1/2}(C_i-C_{i-1}) ]
    中心 i=0： T_0^{n+1} = T_0^n + (4 k dt/(rho cp dr^2))(T_1-T_0)   ; C 同理用 D_0
    表面 i=N： surf='quasi'  —— 准稳态 Robin 代数式（机构原文式(14)(15)）
                    T_N = (k_N T_{N-1} + h dr T_air)/(k_N + h dr)
                    C_N = (D_N C_{N-1} + km dr C_air)/(D_N + km dr)
                surf='halfcell' —— 我方口径的半格元体平衡（含表面控制体储能）
    返回 dict
    """
    r = np.arange(N + 1) * (R0 / N)
    dr = R0 / N
    rl = r[:-1] + dr / 2.0            # 内部界面 r_{i+1/2}，长度 N
    h, km = 25.0, 8.0e-7

    T = np.full(N + 1, 28.0)
    C = np.full(N + 1, 2.55)
    out_t, out_T, out_C = [0.0], [T.copy()], [C.copy()]
    sub = max(1, int(round(dt_out / dt)))
    hist = [] if store_all else None

    for n in range(1, nsteps + 1):
        t_prev = (n - 1) * dt_out
        for s in range(sub):
            ts = t_prev + (s + 1) * dt
            Ta = float(Te(ts))
            Ca = float(Ce(ts))
            if prop == 'q1':
                rho, cp, kk, DD = props_q1(C)
            elif prop == 'q2':
                rho, cp, kk, DD = props_q2(C, T)
            else:
                rho, cp, kk, DD = props_q4(C, T)

            # ---------------- 温度 ----------------
            # k 在 Q1 为常数（任何平均等价）；Q2/Q4 下 k(C) 变化，'integral' 分支退回调和平均
            kf = iface(kk, 'harm' if ifmode == 'integral' else ifmode)
            Tn = T.copy()
            # 内部
            Tn[1:N] = T[1:N] + (dt / (rho[1:N] * cp[1:N] * r[1:N] * dr ** 2)) * (
                rl[1:] * kf[1:] * (T[2:] - T[1:N]) - rl[:-1] * kf[:-1] * (T[1:N] - T[0:N - 1]))
            # 中心
            Tn[0] = T[0] + (4.0 * kk[0] * dt / (rho[0] * cp[0] * dr ** 2)) * (T[1] - T[0])
            # 表面
            if surf == 'quasi':
                src = Tn[N - 1] if quasi_use_new else T[N - 1]
                Tn[N] = (kk[N] * src + h * dr * Ta) / (kk[N] + h * dr)
            else:
                VN = dr * (R0 - dr / 4.0) / 2.0
                cn = kf[N - 1] * rl[N - 1] / dr
                Tn[N] = (rho[N] * cp[N] * VN / dt * T[N] + cn * T[N - 1] + h * R0 * Ta) / (
                    rho[N] * cp[N] * VN / dt + cn + h * R0)

            # ---------------- 水分 ----------------
            Df = iface(DD, ifmode, bD=0.89, D0=7e-9, Carr=C) if (ifmode == 'integral') else iface(DD, ifmode)
            Cn = C.copy()
            Cn[1:N] = C[1:N] + (dt / (r[1:N] * dr ** 2)) * (
                rl[1:] * Df[1:] * (C[2:] - C[1:N]) - rl[:-1] * Df[:-1] * (C[1:N] - C[0:N - 1]))
            Cn[0] = C[0] + (4.0 * DD[0] * dt / dr ** 2) * (C[1] - C[0])
            if surf == 'quasi':
                src = Cn[N - 1] if quasi_use_new else C[N - 1]
                Cn[N] = (DD[N] * src + km * dr * Ca) / (DD[N] + km * dr)
            else:
                VN = dr * (R0 - dr / 4.0) / 2.0
                cn = Df[N - 1] * rl[N - 1] / dr
                Cn[N] = (VN / dt * C[N] + cn * C[N - 1] + km * R0 * Ca) / (VN / dt + cn + km * R0)

            T, C = Tn, np.maximum(Cn, 0.0)
            if store_all:
                hist.append((ts, T.copy(), C.copy()))
        out_t.append(n * dt_out)
        out_T.append(T.copy())
        out_C.append(C.copy())

    res = dict(N=N, dr=dr, dt=dt, r=r, t=np.array(out_t),
               T=np.array(out_T), C=np.array(out_C), hist=hist)
    if snap:
        res['snap'] = {k: dict(T=out_T[int(round(k / dt_out))], C=out_C[int(round(k / dt_out))])
                       for k in snap}
    if cols_idx is not None:
        res['tabT'] = np.array(out_T)[:, cols_idx]
        res['tabC'] = np.array(out_C)[:, cols_idx]
    return res


# ---------------------------------------------------------------- 隐式格式（我方口径的另一份实现）
def thomas(a, b, c, d):
    n = len(b)
    cp_ = np.empty(n - 1)
    dp_ = np.empty(n)
    cp_[0] = c[0] / b[0]
    dp_[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp_[i - 1]
        dp_[i] = (d[i] - a[i] * dp_[i - 1]) / m
        if i < n - 1:
            cp_[i] = c[i] / m
    x = np.empty(n)
    x[-1] = dp_[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp_[i] - cp_[i] * x[i + 1]
    return x


def implicit_fv(N, R0, dt, nsteps, dt_out, Te, Ce, prop='q1', ifmode='arith',
                snap=None, cols_idx=None, picard_maxit=40, tol=1e-10, omega=0.7):
    """元体平衡 + 全隐式（后向欧拉）+ 半格表面控制体；非线性用 Picard 欠松弛。
    结构与我方 q1_core / q2_core 一致，但为**独立另写**的实现（用于对照，不作主力）。"""
    dr = R0 / N
    r = np.arange(N + 1) * dr
    h, km = 25.0, 8.0e-7
    T = np.full(N + 1, 28.0)
    C = np.full(N + 1, 2.55)
    out_t, out_T, out_C = [0.0], [T.copy()], [C.copy()]
    sub = max(1, int(round(dt_out / dt)))

    for n in range(1, nsteps + 1):
        for s in range(sub):
            ts = (n - 1) * dt_out + (s + 1) * dt
            Ta, Ca = float(Te(ts)), float(Ce(ts))
            Told, Cold = T.copy(), C.copy()
            Ti, Ci = T.copy(), C.copy()
            for _ in range(picard_maxit):
                if prop == 'q1':
                    rho, cp, kk, DD = props_q1(Ci)
                elif prop == 'q2':
                    rho, cp, kk, DD = props_q2(Ci, Ti)
                else:
                    rho, cp, kk, DD = props_q4(Ci, Ti)

                # ---- T ----
                kf = iface(kk, ifmode if ifmode != 'integral' else 'arith', Carr=Ci)
                a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1); d = np.zeros(N + 1)
                V0 = dr * dr / 4.0
                b[0] = rho[0] * cp[0] * V0 / dt + kf[0] * dr / dr
                c[0] = -kf[0] * dr / dr
                d[0] = rho[0] * cp[0] * V0 / dt * Told[0]
                for i in range(1, N):
                    rl_, rr_ = r[i] - dr / 2, r[i] + dr / 2
                    b[i] = rho[i] * cp[i] * r[i] / dt + (kf[i] * rr_ + kf[i - 1] * rl_) / dr ** 2
                    a[i] = -kf[i - 1] * rl_ / dr ** 2
                    c[i] = -kf[i] * rr_ / dr ** 2
                    d[i] = rho[i] * cp[i] * r[i] / dt * Told[i]
                VN = dr * (R0 - dr / 4.0) / 2.0
                b[N] = rho[N] * cp[N] * VN / dt + kf[N - 1] * (R0 - dr / 2) / dr + h * R0
                a[N] = -kf[N - 1] * (R0 - dr / 2) / dr
                d[N] = rho[N] * cp[N] * VN / dt * Told[N] + h * R0 * Ta
                Ttry = thomas(a, b, c, d)
                # ---- C ----
                if ifmode == 'integral':
                    Df = iface(DD, 'integral', bD=0.89 if prop == 'q1' else None,
                               D0=7e-9 if prop == 'q1' else None, Carr=Ci)
                    if prop != 'q1':
                        Df = iface(DD, 'harm')
                else:
                    Df = iface(DD, ifmode)
                a2 = np.zeros(N + 1); b2 = np.zeros(N + 1); c2 = np.zeros(N + 1); d2 = np.zeros(N + 1)
                b2[0] = (V0 / dt + Df[0] * dr / dr) / V0
                c2[0] = (-Df[0] * dr / dr) / V0
                d2[0] = Cold[0] / dt
                for i in range(1, N):
                    rl_, rr_ = r[i] - dr / 2, r[i] + dr / 2
                    b2[i] = r[i] / dt + (Df[i] * rr_ + Df[i - 1] * rl_) / dr ** 2
                    a2[i] = -Df[i - 1] * rl_ / dr ** 2
                    c2[i] = -Df[i] * rr_ / dr ** 2
                    d2[i] = r[i] * Cold[i] / dt
                b2[N] = VN / dt + Df[N - 1] * (R0 - dr / 2) / dr + km * R0
                a2[N] = -Df[N - 1] * (R0 - dr / 2) / dr
                d2[N] = VN * Cold[N] / dt + km * R0 * Ca
                Ctry = thomas(a2, b2, c2, d2)
                Tn = omega * Ttry + (1 - omega) * Ti
                Cn = np.maximum(omega * Ctry + (1 - omega) * Ci, 1e-12)
                rT = np.max(np.abs(Tn - Ti)) / max(1.0, np.max(np.abs(Tn)))
                rC = np.max(np.abs(Cn - Ci)) / max(1.0, np.max(np.abs(Cn)))
                Ti, Ci = Tn, Cn
                if rT < tol and rC < tol:
                    break
            T, C = Ti, Ci
        out_t.append(n * dt_out)
        out_T.append(T.copy())
        out_C.append(C.copy())

    res = dict(N=N, dr=dr, r=r, t=np.array(out_t), T=np.array(out_T), C=np.array(out_C))
    if snap:
        res['snap'] = {k: dict(T=out_T[int(round(k / dt_out))], C=out_C[int(round(k / dt_out))])
                       for k in snap}
    if cols_idx is not None:
        res['tabT'] = np.array(out_T)[:, cols_idx]
        res['tabC'] = np.array(out_C)[:, cols_idx]
    return res


# ---------------------------------------------------------------- 第三方路径：MOL + scipy BDF
def bdf_mol(N, R0, t_end, Te, Ce, prop='q1', ifmode='integral', dt_samp=1.0,
            rtol=1e-10, atol=1e-12):
    """method-of-lines：空间元体平衡（半格表面）→ 常微分方程组 → scipy BDF 自适应隐式积分。
    与显式/固定步长隐式两条路径的算法完全不同，用作高精度参考解。"""
    from scipy.integrate import solve_ivp
    dr = R0 / N
    r = np.arange(N + 1) * dr
    h, km = 25.0, 8.0e-7
    V0 = dr * dr / 4.0
    VN = dr * (R0 - dr / 4.0) / 2.0

    def rhs(t, y):
        Tc = y[:N + 1]
        Cc = np.maximum(y[N + 1:], 1e-12)
        if prop == 'q1':
            rho, cp, kk, DD = props_q1(Cc)
        elif prop == 'q2':
            rho, cp, kk, DD = props_q2(Cc, Tc)
        else:
            rho, cp, kk, DD = props_q4(Cc, Tc)
        Ta, Ca = float(Te(min(t, 1e12))), float(Ce(min(t, 1e12)))
        kf = iface(kk, ifmode if ifmode != 'integral' else 'harm')
        if ifmode == 'integral' and prop == 'q1':
            Df = iface(DD, 'integral', bD=0.89, D0=7e-9, Carr=Cc)
        else:
            Df = iface(DD, 'harm' if ifmode == 'integral' else ifmode)
        rr = r[1:-1] + dr / 2
        rl = r[1:-1] - dr / 2
        A = np.zeros(N + 1); B = np.zeros(N + 1)
        # T
        B[0] = (kf[0] * dr / dr) * (Tc[1] - Tc[0]) / (rho[0] * cp[0] * V0)
        B[1:N] = ((kf[1:] * rr * (Tc[2:] - Tc[1:N]) - kf[:-1] * rl * (Tc[1:N] - Tc[:-2])) / dr
                  ) / (rho[1:N] * cp[1:N] * r[1:N] * dr)
        B[N] = (kf[N - 1] * (R0 - dr / 2) / dr * (Tc[N - 1] - Tc[N]) + h * R0 * (Ta - Tc[N])
                ) / (rho[N] * cp[N] * VN)
        # C
        A[0] = (Df[0] * dr / dr) * (Cc[1] - Cc[0]) / V0
        A[1:N] = ((Df[1:] * rr * (Cc[2:] - Cc[1:N]) - Df[:-1] * rl * (Cc[1:N] - Cc[:-2])) / dr
                  ) / (r[1:N] * dr)
        A[N] = (Df[N - 1] * (R0 - dr / 2) / dr * (Cc[N - 1] - Cc[N]) + km * R0 * (Ca - Cc[N])) / VN
        return np.concatenate([B, A])

    y0 = np.concatenate([np.full(N + 1, 28.0), np.full(N + 1, 2.55)])
    t_eval = np.arange(0.0, t_end + 0.5 * dt_samp, dt_samp)
    sol = solve_ivp(rhs, (0.0, t_end), y0, method='BDF', t_eval=t_eval,
                    rtol=rtol, atol=atol, max_step=np.inf)
    return dict(N=N, dr=dr, r=r, t=sol.t, T=sol.y[:N + 1].T, C=sol.y[N + 1:].T,
                nfev=sol.nfev, status=sol.status, message=sol.message)


# ---------------------------------------------------------------- 半无限介质 Robin 解析解
def semi_infinite_C(t, D, km, C0, Cair):
    """半无限介质、初值 C0、表面 Robin 对流传质、环境 Cair 的精确解：
        C(0,t) = Cair + (C0-Cair)·exp(km²t/D)·erfc(km·sqrt(t)/sqrt(D))
        C(x,t) = Cair + (C0-Cair)·{ erfc(x/(2√(Dt))) − exp(km x/D + km²t/D)·erfc(x/(2√(Dt)) + km√t/√D) }
    """
    t = np.asarray(t, float)
    out = np.empty_like(t)
    s = km * np.sqrt(t) / np.sqrt(D)
    out = Cair + (C0 - Cair) * np.exp(km ** 2 * t / D) * erfc(s)
    return out
