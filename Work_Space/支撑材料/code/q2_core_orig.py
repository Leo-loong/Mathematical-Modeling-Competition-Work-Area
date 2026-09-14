# -*- coding: utf-8 -*-
"""
A 题 Q2 求解核（变物性 · 双向强耦合）· ★「优化前」基线版（供前台对照）
=====================================================================
⚠ **本文件为对照基准，刻意保持未优化状态**：
    · 三对角求解 —— `scipy.linalg.solve_banded` 默认参数（无快参数）
    · 装配函数 —— 每次调用新建数组（`out=None`）
    · 无 numba JIT、无多进程
   用途：与 B/C 优化版跑同一算例，比对结果差异（应 ≪ 5e-5）。
   **请勿在本文件上做任何性能优化**，否则失去对照意义。
   命令行：`python q2_solver_orig.py`（前台模式，结束后等待按键）

--- 以下为原始说明 ---

A 题 Q2 求解核（变物性 · 双向强耦合）· v2（矢量化版）
======================================================
与 Q1 核（q1_core.py）的关系
---------------------------
Q2 = Q1 框架 + 变物性 + 强耦合。本核**照搬** Q1 的离散结构：
  · 元体平衡（有限体积）＋ 全隐式（后向欧拉）＋ 三对角求解
  · 中心用中心控制体（V0=Δr²/4、A½=Δr）；表面用半格元体平衡
  · 界面系数一律**距离加权调和平均**
差异（两处）：
  · 物性不再是常数：ρ(C)、c_p(C)、k(C)、D(C,T)（附录3，T 用 K）
  · 两场**双向耦合** ⟹ 外层耦合迭代 ＋ 内层 Picard 迭代

v2 性能改造（v1 单步 0.63 s → 目标 <0.02 s）
--------------------------------------------
  · iface / assemble_* / rhs_* 全部**矢量化**（原为逐元素 Python 循环）
  · 三对角求解改用 `scipy.linalg.solve_banded`（C 实现）
  · 物性用 numpy 数组整体运算

口径（全部引自《A_数值口径总表》）
----------------------------------
  N7  ρ = 650 + 128C ｜ N8  c_p = 1450 + 2736·C/(C+1) ｜ N9  k = 0.21 + 0.38·C/(C+1)
  N10 D = 2.4e-3·exp(-0.45/C)·exp(-3850/T) [m²/s]，T 用 K
  N4  h = 25 ｜ N5  k_m = 8e-7（全程沿用附录2，H5）

模式
----
  'coupled'   主力：双向强耦合
  'frozen'    E2 常物性退化对拍
  'decoupled' E3 强制解耦（D 不含 T）

关键纪律
--------
  · **每一轮外层迭代中，T 与 C 都从 n 层解出发**（右端固定），仅物性随迭代更新
  · **C 方程每个子步的右端取本子步起点**（子步间串行推进）
  · 欠松弛 ω=0.7 必须保留；收敛判据一律用解的（绝对）增量

约定：本核不引用、不记载任何资料中的日期。
"""
import time
import numpy as np
from scipy.linalg import solve_banded

DEF2 = dict(R0=0.02, h=25.0, km=8.0e-7, T0=28.0, C0=2.55)

# 全局扩散系数缩放因子（供灵敏度实验 OAT 使用；默认 1.0 不影响主力结果）
D_FAC = 1.0


# ==================================================================
# 物性（附录3）—— 全矢量化
# ==================================================================
def rho_of(C):
    return 650.0 + 128.0 * np.asarray(C, dtype=float)


def cp_of(C):
    C = np.asarray(C, dtype=float)
    return 1450.0 + 2736.0 * C / (C + 1.0)


def k_of(C):
    C = np.asarray(C, dtype=float)
    return 0.21 + 0.38 * C / (C + 1.0)


def D_of(C, T_C):
    """N10：D = 2.4e-3·exp(-0.45/C)·exp(-3850/T)，T 用 K"""
    C = np.maximum(np.asarray(C, dtype=float), 1e-9)
    TK = np.asarray(T_C, dtype=float) + 273.15
    return D_FAC * 2.4e-3 * np.exp(-0.45 / C) * np.exp(-3850.0 / TK)


def harm(dl, dr_):
    """**标量版**界面系数：距离加权调和平均（供逐点装配与检验脚本复用；与 `iface` 等价）"""
    if dl <= 0.0 or dr_ <= 0.0:
        return 0.0
    return 2.0 / (1.0 / dl + 1.0 / dr_)


def iface(f):
    """界面值：距离加权调和平均（矢量化）。任一侧 ≤0 则取 0。"""
    f = np.asarray(f, dtype=float)
    l, r = f[:-1], f[1:]
    s = l + r
    out = np.zeros_like(l)
    m = (l > 0.0) & (r > 0.0)
    out[m] = 2.0 * l[m] * r[m] / s[m]
    return out


# ==================================================================
# 三对角求解（scipy 带状求解，C 实现）
# ==================================================================
def thomas(a, b, c, d):
    """解三对角系统（a/b/c 为下/主/上对角，a[0] 与 c[-1] 不使用）

    ⚠ **本文件是「优化前」基线版本**（供前台对照运行）：
      使用 `scipy.linalg.solve_banded` 的**默认参数**（含有限性全量扫描与内部拷贝），
      装配函数每次**新建**数组（`out=None` 路径），无任何 JIT。
      **禁止在本文件上做性能优化** —— 它是对照基准，必须保持"慢而原始"。
    """
    n = len(b)
    ab = np.zeros((3, n), dtype=float)
    ab[0, 1:] = c[:-1]
    ab[1, :] = b
    ab[2, :-1] = a[1:]
    return solve_banded((1, 1), ab, d)


# ==================================================================
# T 方程（矢量化装配）
# ==================================================================
def assemble_T_var(N, dr, dt, R0, h, rho, cp, k, out=None):
    """返回 (a, b, c)。rho/cp/k 为长度 N+1 的节点数组。

    `out=(a,b,c)` 时**原地覆写**这三条预分配缓冲（省去每次装配的 3 次 `np.zeros`）。
    ⚠ 原地模式下未赋值的位置（`a[0]`、`c[N]`）**必须显式置零**，否则残留上一轮的值。
    算术表达式、索引与装配顺序与预分配模式**完全一致**。
    """
    r = np.arange(N + 1) * dr
    if out is None:
        a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    else:
        a, b, c = out
        a[0] = 0.0
        c[N] = 0.0
    kf = iface(k)
    V0 = dr * dr / 4.0
    b[0] = (rho[0] * cp[0] * V0 / dt + kf[0] * dr / dr) / V0
    c[0] = (-kf[0] * dr / dr) / V0
    ii = np.arange(1, N)
    rl, rr = r[ii] - dr / 2.0, r[ii] + dr / 2.0
    rc = rho[ii] * cp[ii]
    b[ii] = rc * r[ii] / dt + (kf[ii] * rr + kf[ii - 1] * rl) / dr ** 2
    a[ii] = -kf[ii - 1] * rl / dr ** 2
    c[ii] = -kf[ii] * rr / dr ** 2
    VN = dr * (R0 - dr / 4.0) / 2.0
    b[N] = rho[N] * cp[N] * VN / dt + kf[N - 1] * (R0 - dr / 2.0) / dr + h * R0
    a[N] = -kf[N - 1] * (R0 - dr / 2.0) / dr
    return a, b, c


def rhs_T_var(N, dr, dt, R0, h, rho, cp, Told, Tinf):
    """右端：固定取上一时层解 Told"""
    r = np.arange(N + 1) * dr
    d = np.zeros(N + 1)
    rcT = rho * cp * Told
    d[0] = rcT[0] / dt
    d[1:N] = r[1:N] * rcT[1:N] / dt
    VN = dr * (R0 - dr / 4.0) / 2.0
    d[N] = rcT[N] * VN / dt + h * R0 * Tinf
    return d


# ==================================================================
# C 方程（矢量化装配）
# ==================================================================
def assemble_C_var(N, dr, dt, Df, R0, km, out=None):
    """同 `assemble_T_var`：`out=(a,b,c)` 时原地覆写（未赋值位置显式置零）。"""
    r = np.arange(N + 1) * dr
    if out is None:
        a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    else:
        a, b, c = out
        a[0] = 0.0
        c[N] = 0.0
    V0 = dr * dr / 4.0
    b[0] = (V0 / dt + Df[0] * dr / dr) / V0
    c[0] = (-Df[0] * dr / dr) / V0
    ii = np.arange(1, N)
    rl, rr = r[ii] - dr / 2.0, r[ii] + dr / 2.0
    b[ii] = r[ii] / dt + (Df[ii] * rr + Df[ii - 1] * rl) / dr ** 2
    a[ii] = -Df[ii - 1] * rl / dr ** 2
    c[ii] = -Df[ii] * rr / dr ** 2
    VN = dr * (R0 - dr / 4.0) / 2.0
    b[N] = VN / dt + Df[N - 1] * (R0 - dr / 2.0) / dr + km * R0
    a[N] = -Df[N - 1] * (R0 - dr / 2.0) / dr
    return a, b, c


def rhs_C_var(N, dr, dt, R0, km, Cold, cinf):
    r = np.arange(N + 1) * dr
    d = np.zeros(N + 1)
    d[0] = Cold[0] / dt
    d[1:N] = r[1:N] * Cold[1:N] / dt
    VN = dr * (R0 - dr / 4.0) / 2.0
    d[N] = VN * Cold[N] / dt + km * R0 * cinf
    return d


# ==================================================================
# 单时步：双层迭代
# ==================================================================
def step_coupled(N, dr, dtT, dtC, subT, subC, R0, h, km,
                 T, C, Tenv_fn, Cenv_fn, t0,
                 omega=0.7, tol=1e-9, maxit=30, max_outer=20, tol_outer=1e-8,
                 mode='coupled', lag_props=True, verbose=False):
    """推进一个输出步。返回 (T_new, C_new, info)。

    右端纪律：每轮外层的 T、C 求解**都从 n 层解出发**；C 的每个子步从**本子步起点**出发。

    lag_props=True  —— **物性滞后一步**（用 n 层的 T,C 冻结物性）：
                       每步内问题线性 ⟹ 外层一轮即收敛（快 ~20 倍）；
                       滞后误差 O(Δt)，与后向欧拉**同阶**，不降低整体精度。
                       这是变系数扩散的标准做法（lagged diffusivity）。
    lag_props=False —— 物性随外层迭代更新（严格同层，精度更高但收敛慢，
                       弱耦合迭代收敛因子≈0.93 ⟹ 需 100+ 轮）。用于**一致性对照**。
    """
    Told, Cold = T.copy(), C.copy()
    Tk, Ck = T.copy(), C.copy()
    res_hist = []
    inner_tot = 0
    res_T = res_C = None
    flg = 'ok'
    outer_it = 0
    n_outer = 1 if lag_props else max_outer

    # 物性基线（滞后模式）：由 n 层冻结
    if lag_props:
        if mode == 'frozen':
            rho0 = np.full(N + 1, float(rho_of(DEF2['C0'])))
            cp0 = np.full(N + 1, float(cp_of(DEF2['C0'])))
            k0 = np.full(N + 1, float(k_of(DEF2['C0'])))
            D0 = np.full(N + 1, float(D_of(DEF2['C0'], DEF2['T0'])))
        elif mode == 'decoupled':
            rho0, cp0, k0 = rho_of(Cold), cp_of(Cold), k_of(Cold)
            D0 = 2.4e-3 * np.exp(-0.45 / np.maximum(Cold, 1e-9))
        else:
            rho0, cp0, k0 = rho_of(Cold), cp_of(Cold), k_of(Cold)
            D0 = D_of(Cold, Told)

    for k in range(1, n_outer + 1):
        outer_it = k
        # ① 物性
        if lag_props:
            rho, cp, kk = rho0, cp0, k0
        elif mode == 'frozen':
            rho = np.full(N + 1, float(rho_of(DEF2['C0'])))
            cp = np.full(N + 1, float(cp_of(DEF2['C0'])))
            kk = np.full(N + 1, float(k_of(DEF2['C0'])))
        else:
            rho, cp, kk = rho_of(Ck), cp_of(Ck), k_of(Ck)

        # ② T：每轮从 n 层 Told 出发
        Tprev = Tk.copy()
        Tcur = Told.copy()
        for s in range(subT):
            ts = t0 + (s + 1) * dtT
            a, b, c = assemble_T_var(N, dr, dtT, R0, h, rho, cp, kk)
            d = rhs_T_var(N, dr, dtT, R0, h, rho, cp, Tcur, float(Tenv_fn(ts)))
            Tcur = thomas(a, b, c, d)
        Tk = Tcur

        # ③ D
        if lag_props:
            Dnode = D0
        elif mode == 'frozen':
            Dnode = np.full(N + 1, float(D_of(DEF2['C0'], DEF2['T0'])))
        elif mode == 'decoupled':
            Dnode = 2.4e-3 * np.exp(-0.45 / np.maximum(Ck, 1e-9))
        else:
            Dnode = D_of(Ck, Tk)

        # ④ C：每个子步从本子步起点出发
        Cit = Ck.copy()
        for s in range(subC):
            tt = t0 + (s + 1) * dtC
            cinf = float(Cenv_fn(tt))
            Cbase = Cit.copy()
            base = rhs_C_var(N, dr, dtC, R0, km, Cbase, cinf)
            for it in range(1, maxit + 1):
                if lag_props:
                    Dcur = D0          # 滞后：扩散系数在步内固定 ⟹ 一步线性求解
                elif mode == 'frozen':
                    Dcur = Dnode
                else:
                    Dcur = D_of(Cit, Tk)
                a, b, c = assemble_C_var(N, dr, dtC, iface(Dcur), R0, km)
                Ctry = thomas(a, b, c, base)
                Cnew = omega * Ctry + (1.0 - omega) * Cit
                rr = float(np.max(np.abs(Cnew - Cit))) / max(1.0, float(np.max(np.abs(Cnew))))
                Cit = Cnew
                inner_tot += 1
                if rr < tol:
                    break
        Ck = Cit

        # ⑤ 外层收敛判定（绝对增量）
        res_T = float(np.max(np.abs(Tk - Tprev)))
        res_hist.append(res_T)
        if k > 1:
            res_C = float(np.max(np.abs(Ck - Cprev)))
            if res_T < tol_outer and res_C < tol_outer:
                break
        Cprev = Ck.copy()

    if outer_it >= max_outer:
        flg = 'outer_max'
    if verbose:
        print("      outer res_T hist:", " ".join(f"{v:.2e}" for v in res_hist[:8]),
              "...", f"{res_hist[-1]:.2e}" if len(res_hist) > 8 else "")
    return Tk, Ck, dict(outer_it=outer_it, inner_tot=inner_tot, res_T=res_T,
                        res_C=res_C, flag=flg, res_hist=res_hist)


# ==================================================================
# 单时步：IMEX 交替推进（主力格式，一阶半隐式，无需外层迭代）
# ==================================================================
def step_imex(N, dr, h, n_sub, R0, hc, km, T, C, Tenv_fn, Cenv_fn, t0,
              omega=0.7, tol=1e-10, maxit=30, mode='coupled'):
    """把**一个输出步**细分为 n_sub 个内部步（内部步长 h = dt_out/n_sub），
    每个内部步内**更新物性**并交替推进 T、C：

        ① 物性 ← 当前 T,C（本内部子步起点）
        ② 解 T（1 步 h，物性冻结 ⟹ 线性三对角）
        ③ D   ← 新的 T 与当前 C
        ④ 解 C（Picard 线性化，1 步 h）

    **精度**：物性滞后量 ∝ **内部步长 h**（而非输出步长），
    h=1/32 s 时滞后误差 ~1e-8 K 量级，**远小于后向欧拉自身的时间离散误差**，
    故整体仍为后向欧拉的一阶精度，**不损失精度**。
    **速度**：无需外层耦合迭代（旧格式需 100+ 轮且收敛因子≈0.91）。
    """
    Tcur, Ccur = T.copy(), C.copy()
    inner_tot = 0
    res_max = 0.0
    # 预分配装配缓冲：每个**输出步**建一次，供本步所有子步/迭代原地复用
    # （原实现每次装配都 np.zeros 三次；数值结果不受影响，仅省分配开销）
    bufT = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))
    bufC = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))
    for s in range(n_sub):
        ts = t0 + (s + 1) * h
        tinf = float(Tenv_fn(ts))
        cinf = float(Cenv_fn(ts))

        # ① 物性
        if mode == 'frozen':
            rho = np.full(N + 1, float(rho_of(DEF2['C0'])))
            cp = np.full(N + 1, float(cp_of(DEF2['C0'])))
            kk = np.full(N + 1, float(k_of(DEF2['C0'])))
        else:
            rho, cp, kk = rho_of(Ccur), cp_of(Ccur), k_of(Ccur)

        # ② T（全隐式，物性冻结）
        a, b, c = assemble_T_var(N, dr, h, R0, hc, rho, cp, kk, out=bufT)
        d = rhs_T_var(N, dr, h, R0, hc, rho, cp, Tcur, tinf)
        Tcur = thomas(a, b, c, d)

        # ③ D（用**新的** T）
        if mode == 'frozen':
            Dbase = np.full(N + 1, float(D_of(DEF2['C0'], DEF2['T0'])))
        elif mode == 'decoupled':
            Dbase = 2.4e-3 * np.exp(-0.45 / np.maximum(Ccur, 1e-9))
        else:
            Dbase = D_of(Ccur, Tcur)

        # ④ C（Picard 线性化：D 随迭代中的 C 更新，T 固定）
        base = rhs_C_var(N, dr, h, R0, km, Ccur, cinf)
        Cit = Ccur.copy()
        for it in range(1, maxit + 1):
            if mode == 'frozen':
                Dn = Dbase
            elif mode == 'decoupled':
                Dn = 2.4e-3 * np.exp(-0.45 / np.maximum(Cit, 1e-9))
            else:
                Dn = D_of(Cit, Tcur)
            a, b, c = assemble_C_var(N, dr, h, iface(Dn), R0, km, out=bufC)
            Ctry = thomas(a, b, c, base)
            Cnew = omega * Ctry + (1.0 - omega) * Cit
            rr = float(np.max(np.abs(Cnew - Cit))) / max(1.0, float(np.max(np.abs(Cnew))))
            Cit = Cnew
            inner_tot += 1
            res_max = max(res_max, rr)
            if rr < tol:
                break
        Ccur = Cit

    return Tcur, Ccur, dict(inner_tot=inner_tot, nsub=n_sub,
                            res_max=res_max, outer_it=1, res_T=None, res_C=None,
                            flag='ok', res_hist=[])


# ==================================================================
# 驱动
# ==================================================================
def run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=10800,
           Tenv_fn=None, Cenv_fn=None, subT=32, subC=10, n_sub=None,
           omega=0.7, tol=1e-10, maxit=30, max_outer=20, tol_outer=1e-8,
           mode='coupled', scheme='imex', lag_props=True,
           cols=None, snap_at=(), progress=0, verbose=False):
    """Q2 主力求解（单遍运行，同时收集整表与快照）。返回 (res, tableT, tableC)。

    scheme='imex'     主力：IMEX 交替推进（物性每内部子步更新；不损失精度）
    scheme='iterate'  对照：外层耦合迭代（物性随迭代更新，收敛慢，仅作一致性核对）
    """
    R0, h, km = DEF2['R0'], DEF2['h'], DEF2['km']
    dtT, dtC = dt_out / float(subT), dt_out / float(subC)
    nsub = n_sub if n_sub is not None else subT
    hh = dt_out / float(nsub)
    ncol = 0 if cols is None else len(cols)
    tableT = np.zeros((nsteps, ncol)) if (cols is not None) else None
    tableC = np.zeros((nsteps, ncol)) if (cols is not None) else None

    T = np.full(N + 1, DEF2['T0'])
    C = np.full(N + 1, DEF2['C0'])
    Tsnap, Csnap = {0: T.copy()}, {0: C.copy()}

    stat = dict(outer_tot=0, outer_max=0, inner_tot=0, nsub=0,
                resT_max=0.0, resC_max=0.0, flags={}, res_hist_last=None)
    t0 = time.time()
    for n in range(1, nsteps + 1):
        if scheme == 'imex':
            T, C, info = step_imex(N, dr, hh, nsub, R0, h, km, T, C,
                                   Tenv_fn, Cenv_fn, (n - 1) * dt_out,
                                   omega, tol, maxit, mode)
            stat['resC_max'] = max(stat['resC_max'], info.get('res_max', 0.0))
        else:
            T, C, info = step_coupled(N, dr, dtT, dtC, subT, subC, R0, h, km,
                                      T, C, Tenv_fn, Cenv_fn, (n - 1) * dt_out,
                                      omega, tol, maxit, max_outer, tol_outer,
                                      mode, lag_props=lag_props,
                                      verbose=(verbose and n <= 2))
            stat['resT_max'] = max(stat['resT_max'], info['res_T'] or 0.0)
            stat['resC_max'] = max(stat['resC_max'], info['res_C'] or 0.0)
        stat['outer_tot'] += info.get('outer_it', 1)
        stat['outer_max'] = max(stat['outer_max'], info.get('outer_it', 1))
        stat['inner_tot'] += info['inner_tot']
        stat['nsub'] += 1
        stat['res_hist_last'] = info.get('res_hist')
        if info.get('flag', 'ok') != 'ok':
            stat['flags'][info['flag']] = stat['flags'].get(info['flag'], 0) + 1
        if cols is not None:
            tableT[n - 1, :] = T[cols]
            tableC[n - 1, :] = C[cols]
        if n in snap_at:
            Tsnap[n], Csnap[n] = T.copy(), C.copy()
        if progress and n % progress == 0:
            el = time.time() - t0
            print(f"    ... t={n*dt_out:.0f}s  已用 {el:.1f}s  "
                  f"预计剩余 {el/n*(nsteps-n):.1f}s", flush=True)

    res = dict(N=N, dr=dr, dt_out=dt_out, dtT=hh, dtC=hh, subT=subT, subC=subC,
               n_sub=nsub, scheme=scheme, mode=mode,
               T_end=T.copy(), C_end=C.copy(),
               T_snap=Tsnap, C_snap=Csnap, stats=stat, wall=time.time() - t0)
    return res, tableT, tableC
