# -*- coding: utf-8 -*-
"""
A 题 Q3 变步长（非均匀网格）求解核 ＋ 可选"低 C 端 D 冻结"
================================================================================
**定位**：本模块是 Q3 复检与优化（P1／P2／F-C）的**专用求解核**，
          **不改动** 已交付的 `q2_core_c.py` 与 `q3_core.py` 一行。

三项能力（彼此独立）：
  ① **非均匀网格**：把等距有限体积离散推广为**非等距**——
     元体体积 V_i = (f_{i+1}² - f_i²)/2（f 为元体界面半径），
     界面通量 = (界面半径)·(界面系数)·(节点差)/(节点间距)；
     界面系数仍用**距离加权调和平均**（界面取中点 ⟹ 两侧半距相等 ⟹ 调和平均即精确）。
  ② **可选低 C 端 D 冻结**（P2 外推对照）：D 的计算中令 c ← max(c, c_frz)。
     `c_frz=0` 时**退化为原式**，与 `q2_core_c._D_nb` 语义一致。
  ③ **等距网格上逐点复现基线**（由 `q3_verify_nu.py` 验证 ≤1e-11）。

⚠ 数学口径（与本问基线**完全一致**，仅空间离散的"等距→非等距"推广）：
  · 物性 N7–N10（附录3，T 用 K）；h、k_m 沿用附录2；
  · IMEX 交替推进；物性**逐内部子步**更新；T 全隐式；C 用 Picard ＋ 欠松弛 ω=0.7；
  · 收敛判据 max|ΔC|/max(1,max|C|) < tol（默认 1e-10）；maxit=30；
  · 中心为对称面（f_0=0）；表面为 Robin（面积 R0）；
  · `fastmath=False` — 保持逐位可核（禁止浮点重排）。

按项目约定：本文件不引用、不记载资料中的日期。
"""
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
_Q2CODE = os.path.join(os.path.dirname(HERE), 'Q2', 'code')
if _Q2CODE not in sys.path:
    sys.path.insert(0, _Q2CODE)

from q2_core_c import (njit, _HAS_NUMBA, DEF2, D_FAC,                    # noqa: E402
                       _rho_nb, _cp_nb, _k_nb, _iface_nb, _thomas_nb,
                       _faceD_nb, _facek_nb)
import q3_core as _q3                                                     # noqa: E402

MODE_MAP = {'coupled': 0, 'frozen': 1, 'decoupled': 2}


# ==================================================================
# 几何：非均匀网格描述（Python 侧预计算，njit 内只按数组取用）
# ==================================================================
def make_geom(r, R0):
    """由**节点半径数组** r（r[0]=0、r[-1]=R0）构造元体几何。

    返回 dict：
      V[i]      ：元体体积（单位轴向长度），V_i = (ft_i² - fb_i²)/2
      areaP[i]  ：节点 i 与 i+1 之间的**界面半径**（i=0..N-1）
      dP[i]     ：节点 i 与 i+1 之间的距离（i=0..N-1）
      fL[i]     ：元体左界面半径（i=1..N，fL[0]=0 不使用）
    """
    r = np.ascontiguousarray(np.asarray(r, dtype=np.float64))
    N = r.shape[0] - 1
    fb = np.empty(N + 1)
    ft = np.empty(N + 1)
    for i in range(N + 1):
        fb[i] = 0.0 if i == 0 else 0.5 * (r[i - 1] + r[i])
        ft[i] = float(R0) if i == N else 0.5 * (r[i] + r[i + 1])
    V = 0.5 * (ft ** 2 - fb ** 2)
    areaP = np.ascontiguousarray(ft[:N].copy())
    dP = np.ascontiguousarray((r[1:] - r[:-1]).copy())
    return dict(r=r, N=N, R0=float(R0), NC=N + 1,
                V=np.ascontiguousarray(V), areaP=areaP, dP=dP,
                fb=np.ascontiguousarray(fb), ft=np.ascontiguousarray(ft))


def geom_uniform(N, R0):
    """等距网格（与基线 Δr=R0/N 完全相同的节点位置）。"""
    dr = float(R0) / N
    r = np.arange(N + 1) * dr
    return make_geom(r, R0)


def refined_sizes(region, M, s1):
    """外层 `region` 长度内、M 个**几何递减**单元：s_j = s1·q^{-(j-1)}（j=1..M，j=1 靠内）。

    约束 Σ s_j = region ⟹ 解 q；返回 (q, sizes)。
    """
    from scipy.optimize import brentq

    def f(q):
        return s1 * (1.0 - q ** (-M)) / (1.0 - 1.0 / q) - region

    q = brentq(f, 1.0 + 1e-12, 20.0)
    sizes = s1 * q ** (-np.arange(M))
    return q, sizes


def geom_refined_surface(R0, dr0=2.5e-4, region=1.0e-3, M=26):
    """**表面加密**网格：内区 [0, R0-region] 等距 dr0；外层 region 内 M 个几何递减单元。

    · 内区等距 ⟹ 输出点（每 0.1 cm＝1 mm）**严格落在节点上**；
    · 外层最后一个单元最小（贴近表面），用于分辨低 C 端的薄扩散边界层。
    返回 (geom, meta)，meta 含 q、外层最小/最大单元、外层节点索引区间。
    """
    n_in = int(round((R0 - region) / dr0))
    r_in = np.arange(n_in + 1) * dr0                 # 0 .. R0-region（含）
    q, sizes = refined_sizes(region, M, dr0)         # s1 = dr0 ⟹ 与内区平滑衔接
    edges = r_in[-1] + np.concatenate([[0.0], np.cumsum(sizes)])
    r = np.concatenate([r_in, edges[1:]])
    r[-1] = R0                                       # 保证末节点恰为表面
    g = make_geom(r, R0)
    meta = dict(n_in=n_in, M=M, q=float(q),
                s_min=float(sizes[-1]), s_max=float(sizes[0]),
                idx_inner_end=n_in)
    return g, meta


# ==================================================================
# njit 内核
# ==================================================================
if _HAS_NUMBA:

    @njit(cache=True, fastmath=False)
    def _D_frz_nb(C, T_C, d_fac, c_frz):
        """N10 的**可截断**版本：c ← max(c, c_frz)（c_frz=0 时与原式等价）。"""
        n = C.shape[0]
        out = np.empty(n)
        for i in range(n):
            c = C[i]
            if c < c_frz:
                c = c_frz
            if c < 1e-9:
                c = 1e-9
            out[i] = d_fac * 2.4e-3 * np.exp(-0.45 / c) * np.exp(-3850.0 / (T_C[i] + 273.15))
        return out

    @njit(cache=True, fastmath=False)
    def _faceD_frz_nb(Carr, Tarr, d_fac, useT, nsamp, c_frz):
        """界面扩散系数：**沿 C 的积分平均**（修正口径）＋可选低 $C$ 端冻结 $c_{\\rm fr}$。

        $D_{\\rm trunc}(C)=D(\\max(C,c_{\\rm fr}),T)$ ⟹ 先对原区间采样、再对样本取值钳位。
        """
        n = Carr.shape[0] - 1
        out = np.empty(n)
        for i in range(n):
            a = Carr[i]
            b = Carr[i + 1]
            lo = a if a < b else b
            hi = b if a < b else a
            if hi - lo < 1e-14:
                x = lo
                if x < c_frz:
                    x = c_frz
                if x < 1e-9:
                    x = 1e-9
                fv = np.exp(-0.45 / x)
            else:
                s = 0.0
                for k in range(nsamp):
                    x = lo + (hi - lo) * (k + 0.5) / nsamp
                    if x < c_frz:
                        x = c_frz
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
    def _asm_T_gen(N, dt, kf, rho, cp, V, areaP, dP, R0, h, a, b, c):
        """T 方程装配（非等距有限体积）。"""
        gp0 = areaP[0] * kf[0] / dP[0]
        b[0] = rho[0] * cp[0] * V[0] / dt + gp0
        c[0] = -gp0
        a[0] = 0.0
        for i in range(1, N):
            gp = areaP[i] * kf[i] / dP[i]
            gl = areaP[i - 1] * kf[i - 1] / dP[i - 1]
            b[i] = rho[i] * cp[i] * V[i] / dt + gp + gl
            a[i] = -gl
            c[i] = -gp
        glN = areaP[N - 1] * kf[N - 1] / dP[N - 1]
        b[N] = rho[N] * cp[N] * V[N] / dt + glN + h * R0
        a[N] = -glN
        c[N] = 0.0

    @njit(cache=True, fastmath=False)
    def _rhs_T_gen(N, dt, rho, cp, Told, Tinf, V, R0, h, d):
        for i in range(N + 1):
            d[i] = rho[i] * cp[i] * V[i] * Told[i] / dt
        d[N] = d[N] + h * R0 * Tinf
        return d

    @njit(cache=True, fastmath=False)
    def _asm_C_gen(N, dt, Df, V, areaP, dP, R0, km, a, b, c):
        """C 方程装配（非等距有限体积）。"""
        gp0 = areaP[0] * Df[0] / dP[0]
        b[0] = V[0] / dt + gp0
        c[0] = -gp0
        a[0] = 0.0
        for i in range(1, N):
            gp = areaP[i] * Df[i] / dP[i]
            gl = areaP[i - 1] * Df[i - 1] / dP[i - 1]
            b[i] = V[i] / dt + gp + gl
            a[i] = -gl
            c[i] = -gp
        glN = areaP[N - 1] * Df[N - 1] / dP[N - 1]
        b[N] = V[N] / dt + glN + km * R0
        a[N] = -glN
        c[N] = 0.0

    @njit(cache=True, fastmath=False)
    def _rhs_C_gen(N, dt, Cold, cinf, V, R0, km, d):
        for i in range(N + 1):
            d[i] = V[i] * Cold[i] / dt
        d[N] = d[N] + km * R0 * cinf
        return d

    @njit(cache=True, fastmath=False)
    def _step_all_gen_nb(N, V, areaP, dP, h, n_sub, R0, hc, km, T, C, t0,
                         ts_env, Tenv_v, Cenv_v, d_fac, c_frz, C0f, T0f,
                         omega, tol, maxit, mode_flag):
        """一个输出步的全部内部子步（与 q3_core._step_all_nb 流程逐行等价，
        仅把等距几何换成按数组取用的非等距几何＋可选 D 冻结）。"""
        NC = N + 1
        Tcur = T.copy()
        Ccur = C.copy()
        aT = np.zeros(NC); bT = np.zeros(NC); cT = np.zeros(NC)
        aC = np.zeros(NC); bC = np.zeros(NC); cC = np.zeros(NC)
        dT = np.zeros(NC)
        dC = np.zeros(NC)

        inner_tot = 0
        res_max = 0.0

        for s in range(n_sub):
            ts = t0 + (s + 1) * h
            tinf = _q3._interp1_nb(ts, ts_env, Tenv_v)
            cinf = _q3._interp1_nb(ts, ts_env, Cenv_v)

            # ① 物性（逐子步按局部状态更新）
            if mode_flag == 1:
                rho = np.full(NC, 650.0 + 128.0 * C0f)
                cp = np.full(NC, 1450.0 + 2736.0 * C0f / (C0f + 1.0))
                kk = np.full(NC, 0.21 + 0.38 * C0f / (C0f + 1.0))
            else:
                rho = _rho_nb(Ccur)
                cp = _cp_nb(Ccur)
                kk = _k_nb(Ccur)

            # ② T（全隐式，物性冻结）；界面 k 取沿 C 的积分平均（修正口径）
            if mode_flag == 1:
                kf = np.full(N, 0.21 + 0.38 * C0f / (C0f + 1.0))
            else:
                kf = _facek_nb(Ccur)
            _asm_T_gen(N, h, kf, rho, cp, V, areaP, dP, R0, hc, aT, bT, cT)
            _rhs_T_gen(N, h, rho, cp, Tcur, tinf, V, R0, hc, dT)
            Tcur = _thomas_nb(aT, bT, cT, dT)

            # ③④ C（Picard 线性化）；界面 D 取**沿 C 的积分平均**（修正口径，含可选冻结 c_frz）
            _rhs_C_gen(N, h, Ccur, cinf, V, R0, km, dC)
            bse = dC.copy()
            Cit = Ccur.copy()
            for it in range(1, maxit + 1):
                if mode_flag == 1:
                    cc = C0f if C0f > c_frz else c_frz
                    if cc < 1e-9:
                        cc = 1e-9
                    Df = np.full(N, d_fac * 2.4e-3 * np.exp(-0.45 / cc)
                                 * np.exp(-3850.0 / (T0f + 273.15)))
                elif mode_flag == 2:
                    Df = _faceD_frz_nb(Cit, Tcur, 1.0, False, 8, c_frz)
                else:
                    Df = _faceD_frz_nb(Cit, Tcur, d_fac, True, 8, c_frz)
                _asm_C_gen(N, h, Df, V, areaP, dP, R0, km, aC, bC, cC)
                Ctry = _thomas_nb(aC, bC, cC, bse)
                Cnew = np.empty(NC)
                for i in range(NC):
                    Cnew[i] = omega * Ctry[i] + (1.0 - omega) * Cit[i]

                num = 0.0
                den = 0.0
                for i in range(NC):
                    v = abs(Cnew[i] - Cit[i])
                    if v > num:
                        num = v
                    w = abs(Cnew[i])
                    if w > den:
                        den = w
                if den < 1.0:
                    den = 1.0
                rr = num / den

                Cit = Cnew
                inner_tot += 1
                if rr > res_max:
                    res_max = rr
                if rr < tol:
                    break
            Ccur = Cit

        return Tcur, Ccur, inner_tot, res_max
else:                                                     # pragma: no cover
    _step_all_gen_nb = None


# ==================================================================
# Python 包装（接口与 q3_core.step_imex_fast 平行）
# ==================================================================
def step_imex_gen(geom, h, n_sub, R0, hc, km, T, C, ts_env, Tenv_v, Cenv_v, t0,
                  d_fac=1.0, c_frz=0.0, omega=0.7, tol=1e-10, maxit=30,
                  mode='coupled'):
    """推进一个输出步（n_sub 个内部子步）。返回 (T, C, info)。"""
    if not _HAS_NUMBA:
        raise RuntimeError('本核依赖 numba；当前环境不可用。')
    mf = MODE_MAP[mode]
    Tk, Ck, inner_tot, res_max = _step_all_gen_nb(
        int(geom['N']), geom['V'], geom['areaP'], geom['dP'],
        float(h), int(n_sub), float(R0), float(hc), float(km),
        np.ascontiguousarray(T, dtype=np.float64),
        np.ascontiguousarray(C, dtype=np.float64),
        float(t0), ts_env, Tenv_v, Cenv_v,
        float(d_fac), float(c_frz), float(DEF2['C0']), float(DEF2['T0']),
        float(omega), float(tol), int(maxit), int(mf))
    return Tk, Ck, dict(inner_tot=inner_tot, nsub=n_sub, res_max=res_max,
                        outer_it=1, res_T=None, res_C=None, flag='ok', res_hist=[])


# 复用环境查表口径（H6／N19／N20）—— 与 q3_core 完全同一实现
env_tables_from_att1 = _q3.env_tables_from_att1
