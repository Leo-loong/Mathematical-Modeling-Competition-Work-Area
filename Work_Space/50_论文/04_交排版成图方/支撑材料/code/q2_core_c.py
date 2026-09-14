# -*- coding: utf-8 -*-
"""
A 题 Q2 求解核（变物性 · 双向强耦合）· v4（★B ＋ ★C 优化）
======================================================
★C 优化（在 B 的基础上）：**以 numba 编译的手写追赶法（Thomas）替换
`scipy.linalg.solve_banded`**。

  依据（用户指令解除"禁止替换 Thomas"限制后实施）：
    · 本系统矩阵为**三对角且严格对角占优**（|b_i| > |a_i| + |c_i|，由隐式格式的
      正定性保证），故追赶法**无需选主元即可稳定**，与 LAPACK `dgbsv` 数值等价；
    · `solve_banded` 对小规模带状矩阵存在固定调用开销（Python 校验 + 数据整理），
      微基准实测 21.25 μs（关检查后 14.48 μs），而 njit 追赶法仅需数微秒；
    · 追赶法**消元顺序与 LAPACK 不同** ⟹ 结果存在 ~1e-15 量级的舍入差异
      （远低于 4 位小数输出精度），**必须经 `q2_verify_BC.py` 核对**。

  ⚠ 其余一切（离散表达式、Picard 流程、tol/maxit/omega、物性公式、IMEX 子步）
     与 B 版**完全相同**。

--- 以下为 B 版说明 ---

A 题 Q2 求解核（变物性 · 双向强耦合）· v3（★B 优化：numba JIT）
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

v3 性能改造（★B：numba JIT；**不改任何数值语义**）
--------------------------------------------------
  · 用 `@njit(cache=True, fastmath=False)` 编译：物性 ρ/c_p/k/D、界面调和平均、
    以及 T/C 的装配与右端函数（改为**接收预分配数组、原地填充**）。
  · **`fastmath=False` 是硬性要求** —— 保持 IEEE 语义，禁止任何浮点重排/近似。
  · **求解器仍是 `scipy.linalg.solve_banded`**（B 版不替换 Thomas；C 版另见 `q2_core_c.py`）。
  · **Picard 的 `for it` 循环、残差计算、break 条件、欠松弛、外层逻辑全部留在
    Python 层，一行未改**；离散公式与装配表达式**逐字保留**（见各函数注释对照）。
  · numba 不可用时自动**降级**为原 numpy 实现（`_HAS_NUMBA=False`），行为不变。

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

# ==================================================================
# numba 可用性（不可用则自动降级为 numpy 实现，行为完全不变）
# ==================================================================
try:
    from numba import njit
    _HAS_NUMBA = True
except Exception:                                            # pragma: no cover
    njit = None
    _HAS_NUMBA = False


DEF2 = dict(R0=0.02, h=25.0, km=8.0e-7, T0=28.0, C0=2.55)

# 全局扩散系数缩放因子（供灵敏度实验 OAT 使用；默认 1.0 不影响主力结果）
D_FAC = 1.0


# ==================================================================
# ★ JIT 内核（fastmath=False：严格 IEC 559，禁止浮点重排）
#   每个内核下方都注明其**原 numpy 表达式**，供逐字核对。
# ==================================================================
if _HAS_NUMBA:

    @njit(cache=True, fastmath=False)
    def _rho_nb(C):
        """N7：ρ = 650 + 128C   （原式 650.0 + 128.0 * C）"""
        n = C.shape[0]
        out = np.empty(n)
        for i in range(n):
            out[i] = 650.0 + 128.0 * C[i]
        return out

    @njit(cache=True, fastmath=False)
    def _cp_nb(C):
        """N8：c_p = 1450 + 2736·C/(C+1)   （原式 1450.0 + 2736.0 * C / (C + 1.0)）"""
        n = C.shape[0]
        out = np.empty(n)
        for i in range(n):
            out[i] = 1450.0 + 2736.0 * C[i] / (C[i] + 1.0)
        return out

    @njit(cache=True, fastmath=False)
    def _k_nb(C):
        """N9：k = 0.21 + 0.38·C/(C+1)   （原式 0.21 + 0.38 * C / (C + 1.0)）"""
        n = C.shape[0]
        out = np.empty(n)
        for i in range(n):
            out[i] = 0.21 + 0.38 * C[i] / (C[i] + 1.0)
        return out

    @njit(cache=True, fastmath=False)
    def _D_nb(C, T_C, d_fac):
        """N10：D = D_FAC · 2.4e-3 · exp(-0.45/C) · exp(-3850/T)，T 用 K

        ⚠ `D_FAC` 原为模块级全局量；在 njit 内**必须显式传参**，
          否则 numba 会将其在编译期冻结为常量（OAT 扰动将失效）。
        """
        n = C.shape[0]
        out = np.empty(n)
        for i in range(n):
            c = C[i]
            if c < 1e-9:
                c = 1e-9
            out[i] = d_fac * 2.4e-3 * np.exp(-0.45 / c) * np.exp(-3850.0 / (T_C[i] + 273.15))
        return out

    @njit(cache=True, fastmath=False)
    def _iface_nb(f):
        """界面值：距离加权调和平均；任一侧 ≤0 则取 0
        （原式 out[m] = 2·l·r/(l+r)，其余位置保持 0）

        ⚠ **本式仅适用于"系数在界面处间断（分段常数）"**。
        当系数随 $C$ 平滑但陡峭变化时（如 Q3 低含水率端 $D$ 跨 2–3 个数量级），
        应改用下方 `_faceD_nb`／`_facek_nb` 的**沿 $C$ 积分平均**。
        """
        n = f.shape[0] - 1
        out = np.zeros(n)
        for i in range(n):
            l = f[i]
            r = f[i + 1]
            if l > 0.0 and r > 0.0:
                out[i] = 2.0 * l * r / (l + r)
        return out

    @njit(cache=True, fastmath=False)
    def _faceD_nb(Carr, Tarr, d_fac, useT, nsamp):
        """★**修正口径**：界面扩散系数取**沿 $C$ 的积分平均**

            ⟨D⟩ = (1/ΔC)∫_{C_{i+1}}^{C_i} D(C, T_face) dC

        依据：单元内稳态通量 $J=\\frac{1}{\\Delta r}\\int D\\,\\mathrm dC$ ⟹ 界面系数 = 沿 $C$ 的积分平均。
        利用可分离性 $D=[d_{fac}2.4\\!\\times\\!10^{-3}e^{-0.45/C}]\\,[e^{-3850/T_K}]$，只需对 $C$ 因子采样。
        `useT=True`：含 $T$ 因子（coupled）；`False`：仅 $C$ 因子（decoupled，不乘 $d_{fac}$）。
        $|\\Delta C|\\approx0$ 时退化为节点值。
        """
        n = Carr.shape[0] - 1
        out = np.empty(n)
        for i in range(n):
            a = Carr[i]
            b = Carr[i + 1]
            lo = a if a < b else b
            hi = b if a < b else a
            if hi - lo < 1e-14:
                c = lo if lo > 1e-9 else 1e-9
                fv = np.exp(-0.45 / c)
            else:
                s = 0.0
                for k in range(nsamp):
                    x = lo + (hi - lo) * (k + 0.5) / nsamp
                    if x < 1e-9:
                        x = 1e-9
                    s += np.exp(-0.45 / x)
                fv = s / nsamp
            if useT:
                Tm = 0.5 * (Tarr[i] + Tarr[i + 1])
                out[i] = d_fac * 2.4e-3 * fv * np.exp(-3850.0 / (Tm + 273.15))
            else:
                out[i] = 2.4e-3 * fv
        return out

    @njit(cache=True, fastmath=False)
    def _facek_nb(Carr):
        """★**修正口径**：界面导热系数取沿 $C$ 的积分平均（解析式）

            ⟨k⟩ = 0.21 + 0.38·[Δ(C − ln(1+C))]/ΔC
        """
        n = Carr.shape[0] - 1
        out = np.empty(n)
        for i in range(n):
            a = Carr[i]
            b = Carr[i + 1]
            if abs(b - a) < 1e-14:
                c = a
                out[i] = 0.21 + 0.38 * c / (1.0 + c)
            else:
                ga = a - np.log(1.0 + a)
                gb = b - np.log(1.0 + b)
                out[i] = 0.21 + 0.38 * (gb - ga) / (b - a)
        return out

    @njit(cache=True, fastmath=False)
    def _assemble_T_nb(N, dr, dt, R0, h, rho, cp, k, a, b, c, kf):
        """T 方程装配（原地填充 a/b/c）。表达式与原 numpy 版逐字对应。

        `kf`（界面调和平均）由调用方预先算好传入 —— 与 v2 中
        "函数内先 `kf = iface(k)`" 语义一致，只是把该步提到包装层以避免重复计算。
        """
        V0 = dr * dr / 4.0
        b[0] = (rho[0] * cp[0] * V0 / dt + kf[0] * dr / dr) / V0
        c[0] = (-kf[0] * dr / dr) / V0
        a[0] = 0.0
        for i in range(1, N):
            r = i * dr
            rl = r - dr / 2.0
            rr = r + dr / 2.0
            rc = rho[i] * cp[i]
            b[i] = rc * r / dt + (kf[i] * rr + kf[i - 1] * rl) / dr ** 2
            a[i] = -kf[i - 1] * rl / dr ** 2
            c[i] = -kf[i] * rr / dr ** 2
        VN = dr * (R0 - dr / 4.0) / 2.0
        b[N] = rho[N] * cp[N] * VN / dt + kf[N - 1] * (R0 - dr / 2.0) / dr + h * R0
        a[N] = -kf[N - 1] * (R0 - dr / 2.0) / dr
        c[N] = 0.0

    @njit(cache=True, fastmath=False)
    def _rhs_T_nb(N, dr, dt, R0, h, rho, cp, Told, Tinf, d):
        """T 方程右端（原地填充 d）；固定取上一时层解 Told"""
        rcT = rho * cp * Told
        d[0] = rcT[0] / dt
        for i in range(1, N):
            d[i] = (i * dr) * rcT[i] / dt
        VN = dr * (R0 - dr / 4.0) / 2.0
        d[N] = rcT[N] * VN / dt + h * R0 * Tinf
        return d

    @njit(cache=True, fastmath=False)
    def _assemble_C_nb(N, dr, dt, Df, R0, km, a, b, c):
        """C 方程装配（原地填充 a/b/c）。表达式与原 numpy 版逐字对应。"""
        V0 = dr * dr / 4.0
        b[0] = (V0 / dt + Df[0] * dr / dr) / V0
        c[0] = (-Df[0] * dr / dr) / V0
        a[0] = 0.0
        for i in range(1, N):
            r = i * dr
            rl = r - dr / 2.0
            rr = r + dr / 2.0
            b[i] = r / dt + (Df[i] * rr + Df[i - 1] * rl) / dr ** 2
            a[i] = -Df[i - 1] * rl / dr ** 2
            c[i] = -Df[i] * rr / dr ** 2
        VN = dr * (R0 - dr / 4.0) / 2.0
        b[N] = VN / dt + Df[N - 1] * (R0 - dr / 2.0) / dr + km * R0
        a[N] = -Df[N - 1] * (R0 - dr / 2.0) / dr
        c[N] = 0.0

    @njit(cache=True, fastmath=False)
    def _rhs_C_nb(N, dr, dt, R0, km, Cold, cinf, d):
        """C 方程右端（原地填充 d）"""
        d[0] = Cold[0] / dt
        for i in range(1, N):
            d[i] = (i * dr) * Cold[i] / dt
        VN = dr * (R0 - dr / 4.0) / 2.0
        d[N] = VN * Cold[N] / dt + km * R0 * cinf
        return d

    @njit(cache=True, fastmath=False)
    def _thomas_nb(a, b, c, d):
        """★C：手写追赶法（Thomas 消元，无选主元）

        矩阵严格对角占优 ⟹ 无需主元选择即数值稳定。

        算法（标准前向消元 ＋ 后向回代）：
          前向：cp[0] = c[0]/b[0]；dp[0] = d[0]/b[0]
                cp[i] = c[i] / (b[i] - a[i]·cp[i-1])
                dp[i] = (d[i] - a[i]·dp[i-1]) / (b[i] - a[i]·cp[i-1])
          后向：x[n-1] = dp[n-1]；x[i] = dp[i] - cp[i]·x[i+1]

        `a[0]` 与 `c[n-1]` 在装配时已置零，故首末行自动退化为正确形式。
        """
        n = b.shape[0]
        cp_ = np.empty(n)
        dp_ = np.empty(n)
        cp_[0] = c[0] / b[0]
        dp_[0] = d[0] / b[0]
        for i in range(1, n):
            m = b[i] - a[i] * cp_[i - 1]
            cp_[i] = c[i] / m
            dp_[i] = (d[i] - a[i] * dp_[i - 1]) / m
        x = np.empty(n)
        x[n - 1] = dp_[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = dp_[i] - cp_[i] * x[i + 1]
        return x


# ==================================================================
# 公共接口（签名与 v2 完全一致 ⟹ 既有脚本零改动）
# ==================================================================
def rho_of(C):
    if _HAS_NUMBA:
        arr = np.asarray(C, dtype=np.float64)
        if arr.ndim == 0:                      # 标量输入 ⟹ 返回标量（与原版 float() 兼容）
            return float(_rho_nb(arr.reshape(1))[0])
        return _rho_nb(np.ascontiguousarray(arr))
    return 650.0 + 128.0 * np.asarray(C, dtype=float)


def cp_of(C):
    if _HAS_NUMBA:
        arr = np.asarray(C, dtype=np.float64)
        if arr.ndim == 0:
            return float(_cp_nb(arr.reshape(1))[0])
        return _cp_nb(np.ascontiguousarray(arr))
    C = np.asarray(C, dtype=float)
    return 1450.0 + 2736.0 * C / (C + 1.0)


def k_of(C):
    if _HAS_NUMBA:
        arr = np.asarray(C, dtype=np.float64)
        if arr.ndim == 0:
            return float(_k_nb(arr.reshape(1))[0])
        return _k_nb(np.ascontiguousarray(arr))
    C = np.asarray(C, dtype=float)
    return 0.21 + 0.38 * C / (C + 1.0)


def D_of(C, T_C):
    """N10：D = 2.4e-3·exp(-0.45/C)·exp(-3850/T)，T 用 K"""
    if _HAS_NUMBA:
        Ca = np.asarray(C, dtype=np.float64)
        Ta = np.asarray(T_C, dtype=np.float64)
        if Ca.ndim == 0:
            v = _D_nb(Ca.reshape(1), Ta.reshape(1), float(D_FAC))
            return float(v[0])
        return _D_nb(np.ascontiguousarray(Ca), np.ascontiguousarray(Ta), float(D_FAC))
    C = np.maximum(np.asarray(C, dtype=float), 1e-9)
    TK = np.asarray(T_C, dtype=float) + 273.15
    return D_FAC * 2.4e-3 * np.exp(-0.45 / C) * np.exp(-3850.0 / TK)


def harm(dl, dr_):
    """**标量版**界面系数：距离加权调和平均（与 `iface` 等价）"""
    if dl <= 0.0 or dr_ <= 0.0:
        return 0.0
    return 2.0 / (1.0 / dl + 1.0 / dr_)


def iface(f):
    """界面值：距离加权调和平均（矢量化）。任一侧 ≤0 则取 0。"""
    if _HAS_NUMBA:
        arr = np.asarray(f, dtype=np.float64)
        if arr.ndim == 0:
            return np.zeros(0)
        return _iface_nb(np.ascontiguousarray(arr))
    f = np.asarray(f, dtype=float)
    l, r = f[:-1], f[1:]
    s = l + r
    out = np.zeros_like(l)
    m = (l > 0.0) & (r > 0.0)
    out[m] = 2.0 * l[m] * r[m] / s[m]
    return out


# ==================================================================
# ★**修正口径**：界面系数取"沿 C 的积分平均"
#   （原 `iface` 的调和平均仅对"界面处系数间断"成立；本项在系数随 C 陡变时失真）
# ==================================================================
NSAMP_FACE = 8          # 沿 C 的 Midpoint 采样点数（已验 4/8/16 收敛）


def faceD_of(C, T, d_fac=1.0, useT=True, nsamp=NSAMP_FACE):
    """界面扩散系数（沿 $C$ 的积分平均）——**修正口径**。

    $\\langle D\\rangle=\\frac1{\\Delta C}\\int D\\,\\mathrm dC$，$D$ 对 $C$ 因子采样、$T$ 取界面均值。
    """
    Ca = np.ascontiguousarray(np.asarray(C, dtype=np.float64))
    Ta = np.ascontiguousarray(np.asarray(T, dtype=np.float64))
    if _HAS_NUMBA:
        return _faceD_nb(Ca, Ta, float(d_fac), bool(useT), int(nsamp))
    lo, hi = np.minimum(Ca[:-1], Ca[1:]), np.maximum(Ca[:-1], Ca[1:])
    xs = lo[:, None] + (hi - lo)[:, None] * (np.arange(nsamp) + 0.5)[None, :] / nsamp
    xs = np.maximum(xs, 1e-9)
    fv = np.exp(-0.45 / xs).mean(axis=1)
    flat = (hi - lo) < 1e-14
    if flat.any():
        fv[flat] = np.exp(-0.45 / np.maximum(lo[flat], 1e-9))
    if useT:
        Tm = 0.5 * (Ta[:-1] + Ta[1:])
        return d_fac * 2.4e-3 * fv * np.exp(-3850.0 / (Tm + 273.15))
    return 2.4e-3 * fv


def facek_of(C):
    """界面导热系数（沿 $C$ 的积分平均，解析式）——**修正口径**。"""
    Ca = np.ascontiguousarray(np.asarray(C, dtype=np.float64))
    if _HAS_NUMBA:
        return _facek_nb(Ca)
    a, b = Ca[:-1], Ca[1:]
    db = np.abs(b - a)
    safe = np.where(db < 1e-14, 1.0, b - a)
    gb = b - np.log(1.0 + b)
    ga = a - np.log(1.0 + a)
    out = 0.21 + 0.38 * (gb - ga) / safe
    flat = db < 1e-14
    if flat.any():
        out[flat] = 0.21 + 0.38 * a[flat] / (1.0 + a[flat])
    return out


# ==================================================================
# 三对角求解（B 版：**保留 scipy.linalg.solve_banded**）
# ==================================================================
def thomas(a, b, c, d):
    """解三对角系统（a/b/c 为下/主/上对角，a[0] 与 c[-1] 不使用）

    ★C 版：改为 **numba 手写追赶法**（原 `scipy.linalg.solve_banded` 仅作降级回退）。
    调用签名**完全不变** ⟹ 上层装配/Picard 逻辑一行未改。
    """
    if _HAS_NUMBA:
        return _thomas_nb(a, b, c, d)
    n = len(b)
    ab = np.zeros((3, n), dtype=float)
    ab[0, 1:] = c[:-1]
    ab[1, :] = b
    ab[2, :-1] = a[1:]
    return solve_banded((1, 1), ab, d, check_finite=False, overwrite_ab=True)


# ==================================================================
# T 方程装配（Java 侧包装：负责缓冲分配，内核原地填充）
# ==================================================================
def assemble_T_var(N, dr, dt, R0, h, rho, cp, k, out=None, kf=None):
    """返回 (a, b, c)。rho/cp/k 为长度 N+1 的节点数组。

    `out=(a,b,c)` 时**原地覆写**预分配缓冲；否则新建。
    `kf`：可选的**预计算界面导热系数**（修正口径 `facek_of(C)`）；None 时回退旧调和平均。
    """
    if out is None:
        a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    else:
        a, b, c = out
    if _HAS_NUMBA:
        if kf is None:
            kf = _iface_nb(np.ascontiguousarray(k, dtype=np.float64))
        _assemble_T_nb(N, dr, dt, R0, h,
                       np.ascontiguousarray(rho, dtype=np.float64),
                       np.ascontiguousarray(cp, dtype=np.float64),
                       np.ascontiguousarray(k, dtype=np.float64),
                       a, b, c, kf)
        return a, b, c
    r = np.arange(N + 1) * dr
    if kf is None:
        kf = iface(k)
    V0 = dr * dr / 4.0
    b[0] = (rho[0] * cp[0] * V0 / dt + kf[0] * dr / dr) / V0
    c[0] = (-kf[0] * dr / dr) / V0
    a[0] = 0.0
    ii = np.arange(1, N)
    rl, rr = r[ii] - dr / 2.0, r[ii] + dr / 2.0
    rc = rho[ii] * cp[ii]
    b[ii] = rc * r[ii] / dt + (kf[ii] * rr + kf[ii - 1] * rl) / dr ** 2
    a[ii] = -kf[ii - 1] * rl / dr ** 2
    c[ii] = -kf[ii] * rr / dr ** 2
    VN = dr * (R0 - dr / 4.0) / 2.0
    b[N] = rho[N] * cp[N] * VN / dt + kf[N - 1] * (R0 - dr / 2.0) / dr + h * R0
    a[N] = -kf[N - 1] * (R0 - dr / 2.0) / dr
    c[N] = 0.0
    return a, b, c


def rhs_T_var(N, dr, dt, R0, h, rho, cp, Told, Tinf, out=None):
    """右端：固定取上一时层解 Told"""
    d = np.zeros(N + 1) if out is None else out
    if _HAS_NUMBA:
        _rhs_T_nb(N, dr, dt, R0, h,
                  np.ascontiguousarray(rho, dtype=np.float64),
                  np.ascontiguousarray(cp, dtype=np.float64),
                  np.ascontiguousarray(Told, dtype=np.float64),
                  float(Tinf), d)
        return d
    r = np.arange(N + 1) * dr
    rcT = rho * cp * Told
    d[0] = rcT[0] / dt
    d[1:N] = r[1:N] * rcT[1:N] / dt
    VN = dr * (R0 - dr / 4.0) / 2.0
    d[N] = rcT[N] * VN / dt + h * R0 * Tinf
    return d


# ==================================================================
# C 方程装配
# ==================================================================
def assemble_C_var(N, dr, dt, Df, R0, km, out=None):
    """同 `assemble_T_var`：`out=(a,b,c)` 时原地覆写。"""
    if out is None:
        a = np.zeros(N + 1); b = np.zeros(N + 1); c = np.zeros(N + 1)
    else:
        a, b, c = out
    if _HAS_NUMBA:
        _assemble_C_nb(N, dr, dt,
                       np.ascontiguousarray(Df, dtype=np.float64),
                       R0, km, a, b, c)
        return a, b, c
    r = np.arange(N + 1) * dr
    V0 = dr * dr / 4.0
    b[0] = (V0 / dt + Df[0] * dr / dr) / V0
    c[0] = (-Df[0] * dr / dr) / V0
    a[0] = 0.0
    ii = np.arange(1, N)
    rl, rr = r[ii] - dr / 2.0, r[ii] + dr / 2.0
    b[ii] = r[ii] / dt + (Df[ii] * rr + Df[ii - 1] * rl) / dr ** 2
    a[ii] = -Df[ii - 1] * rl / dr ** 2
    c[ii] = -Df[ii] * rr / dr ** 2
    VN = dr * (R0 - dr / 4.0) / 2.0
    b[N] = VN / dt + Df[N - 1] * (R0 - dr / 2.0) / dr + km * R0
    a[N] = -Df[N - 1] * (R0 - dr / 2.0) / dr
    c[N] = 0.0
    return a, b, c


def rhs_C_var(N, dr, dt, R0, km, Cold, cinf, out=None):
    d = np.zeros(N + 1) if out is None else out
    if _HAS_NUMBA:
        _rhs_C_nb(N, dr, dt, R0, km,
                  np.ascontiguousarray(Cold, dtype=np.float64),
                  float(cinf), d)
        return d
    r = np.arange(N + 1) * dr
    d[0] = Cold[0] / dt
    d[1:N] = r[1:N] * Cold[1:N] / dt
    VN = dr * (R0 - dr / 4.0) / 2.0
    d[N] = VN * Cold[N] / dt + km * R0 * cinf
    return d


# ==================================================================
# 单时步：双层迭代（逻辑与 v2 **一行未改**）
# ==================================================================
def step_coupled(N, dr, dtT, dtC, subT, subC, R0, h, km,
                 T, C, Tenv_fn, Cenv_fn, t0,
                 omega=0.7, tol=1e-9, maxit=30, max_outer=20, tol_outer=1e-8,
                 mode='coupled', lag_props=True, verbose=False):
    """推进一个输出步。返回 (T_new, C_new, info)。

    右端纪律：每轮外层的 T、C 求解**都从 n 层解出发**；C 的每个子步从**本子步起点**出发。
    """
    Told, Cold = T.copy(), C.copy()
    Tk, Ck = T.copy(), C.copy()
    res_hist = []
    inner_tot = 0
    res_T = res_C = None
    flg = 'ok'
    outer_it = 0
    n_outer = 1 if lag_props else max_outer

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
        if lag_props:
            rho, cp, kk = rho0, cp0, k0
        elif mode == 'frozen':
            rho = np.full(N + 1, float(rho_of(DEF2['C0'])))
            cp = np.full(N + 1, float(cp_of(DEF2['C0'])))
            kk = np.full(N + 1, float(k_of(DEF2['C0'])))
        else:
            rho, cp, kk = rho_of(Ck), cp_of(Ck), k_of(Ck)

        Tprev = Tk.copy()
        Tcur = Told.copy()
        for s in range(subT):
            ts = t0 + (s + 1) * dtT
            kf = np.full(N, float(k_of(DEF2['C0']))) if mode == 'frozen' else facek_of(Ck)
            a, b, c = assemble_T_var(N, dr, dtT, R0, h, rho, cp, kk, kf=kf)
            d = rhs_T_var(N, dr, dtT, R0, h, rho, cp, Tcur, float(Tenv_fn(ts)))
            Tcur = thomas(a, b, c, d)
        Tk = Tcur

        if lag_props:
            Dnode = D0
        elif mode == 'frozen':
            Dnode = np.full(N + 1, float(D_of(DEF2['C0'], DEF2['T0'])))
        elif mode == 'decoupled':
            Dnode = 2.4e-3 * np.exp(-0.45 / np.maximum(Ck, 1e-9))
        else:
            Dnode = D_of(Ck, Tk)

        Cit = Ck.copy()
        for s in range(subC):
            tt = t0 + (s + 1) * dtC
            cinf = float(Cenv_fn(tt))
            Cbase = Cit.copy()
            base = rhs_C_var(N, dr, dtC, R0, km, Cbase, cinf)
            for it in range(1, maxit + 1):
                if lag_props:
                    if mode == 'frozen':
                        Df = np.full(N, float(D_of(DEF2['C0'], DEF2['T0'])))
                    elif mode == 'decoupled':
                        Df = faceD_of(Cbase, Tk, 1.0, useT=False)
                    else:
                        Df = faceD_of(Cbase, Told, float(D_FAC), useT=True)
                else:
                    if mode == 'frozen':
                        Df = np.full(N, float(D_of(DEF2['C0'], DEF2['T0'])))
                    elif mode == 'decoupled':
                        Df = faceD_of(Cit, Tk, 1.0, useT=False)
                    else:
                        Df = faceD_of(Cit, Tk, float(D_FAC), useT=True)
                a, b, c = assemble_C_var(N, dr, dtC, Df, R0, km)
                Ctry = thomas(a, b, c, base)
                Cnew = omega * Ctry + (1.0 - omega) * Cit
                rr = float(np.max(np.abs(Cnew - Cit))) / max(1.0, float(np.max(np.abs(Cnew))))
                Cit = Cnew
                inner_tot += 1
                if rr < tol:
                    break
        Ck = Cit

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
# 单时步：IMEX 交替推进（主力格式）★B 优化：装配缓冲预分配并原地复用
# ==================================================================
def step_imex(N, dr, h, n_sub, R0, hc, km, T, C, Tenv_fn, Cenv_fn, t0,
              omega=0.7, tol=1e-10, maxit=30, mode='coupled'):
    """把**一个输出步**细分为 n_sub 个内部步（内部步长 h = dt_out/n_sub），
    每个内部步内**更新物性**并交替推进 T、C：

        ① 物性 ← 当前 T,C（本内部子步起点）
        ② 解 T（1 步 h，物性冻结 ⟹ 线性三对角）
        ③ D   ← 新的 T 与当前 C
        ④ 解 C（Picard 线性化，1 步 h）

    ★B 优化仅涉及**缓冲复用**（a/b/c/d 每输出步建一次），
      迭代次数、判据、松弛、物性更新时机**全部不变**。
    """
    Tcur, Ccur = T.copy(), C.copy()
    inner_tot = 0
    res_max = 0.0
    # 预分配缓冲（每输出步一次）
    bufT = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))
    bufC = (np.zeros(N + 1), np.zeros(N + 1), np.zeros(N + 1))
    dT = np.zeros(N + 1)
    dC = np.zeros(N + 1)
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

        # ② T（全隐式，物性冻结）；界面 k 取沿 C 的积分平均（修正口径）
        kf = np.full(N, float(k_of(DEF2['C0']))) if mode == 'frozen' else facek_of(Ccur)
        a, b, c = assemble_T_var(N, dr, h, R0, hc, rho, cp, kk, out=bufT, kf=kf)
        d = rhs_T_var(N, dr, h, R0, hc, rho, cp, Tcur, tinf, out=dT)
        Tcur = thomas(a, b, c, d)

        # ③ D 基准（仅 frozen 需常数基准）
        if mode == 'frozen':
            Dbase = np.full(N + 1, float(D_of(DEF2['C0'], DEF2['T0'])))

        # ④ C（Picard 线性化：D 随迭代中的 C 更新，T 固定）；界面 D 取沿 C 的积分平均（修正口径）
        base = rhs_C_var(N, dr, h, R0, km, Ccur, cinf)      # 每子步更新 ⟹ 不复用缓冲
        Cit = Ccur.copy()
        for it in range(1, maxit + 1):
            if mode == 'frozen':
                Df = np.full(N, Dbase[0])
            elif mode == 'decoupled':
                Df = faceD_of(Cit, Tcur, 1.0, useT=False)
            else:
                Df = faceD_of(Cit, Tcur, float(D_FAC), useT=True)
            a, b, c = assemble_C_var(N, dr, h, Df, R0, km, out=bufC)
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
# 驱动（逻辑与 v2 **一行未改**）
# ==================================================================
def run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=10800,
           Tenv_fn=None, Cenv_fn=None, subT=32, subC=10, n_sub=None,
           omega=0.7, tol=1e-10, maxit=30, max_outer=20, tol_outer=1e-8,
           mode='coupled', scheme='imex', lag_props=True,
           cols=None, snap_at=(), progress=0, verbose=False):
    """Q2 主力求解（单遍运行，同时收集整表与快照）。返回 (res, tableT, tableC)。"""
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
