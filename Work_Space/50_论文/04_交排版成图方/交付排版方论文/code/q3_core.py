# -*- coding: utf-8 -*-
"""
A 题 Q3 求解核：在 Q2 优化核（q2_core_c）之上实施 **A/B 优化**
================================================================================
设计原则（**零数值风险**）：
  · **复用** `q2_core_c` 的全部物性／界面／装配／右端／追赶法实现（一行不改）；
  · 仅在**驱动层**做两项工程优化：
      **B｜环境边界改"预插值查表"**：把 Python lambda 调用改为 njit 内的
            线性插值查表（附件1 仅 241 点，二分查找 + 线性插值）；
      **A｜"子步循环下沉 JIT"**：把 `for s in range(n_sub)` 整段循环下沉为
            单个 njit 函数，使 Python 层调用次数由 O(n_sub) 降为 O(1)。
  · **数学表达式、迭代流程、tol/maxit/omega、物性公式、离散格式全部不变**；
  · `fastmath=False` 保持不变（保证与 B/C 版**逐位一致**）。

验证方式：`q3_verify_opt.py` —— 同输入下与 `q2_core_c.step_imex` 逐位比对。

⚠ 本文件仅新增"组装层"，不改变任何物理或离散口径。
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_Q2CODE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Q2', 'code')
sys.path.insert(0, _Q2CODE)

import q2_core_c as base                      # noqa: E402  （B+C 优化核，逐字复用）
from q2_core_c import (DEF2, D_FAC, njit, _HAS_NUMBA,   # noqa: E402
                       _rho_nb, _cp_nb, _k_nb, _D_nb, _iface_nb,
                       _faceD_nb, _facek_nb,
                       _assemble_T_nb, _rhs_T_nb, _assemble_C_nb, _rhs_C_nb,
                       _thomas_nb)

MODE_MAP = {'coupled': 0, 'frozen': 1, 'decoupled': 2}


# ==================================================================
# B｜环境边界的 njit 线性插值查表（替代 Python lambda 调用）
# ==================================================================
@njit(cache=True, fastmath=False)
def _interp1_nb(t, ts, vs):
    """分段线性插值（njit）：t<=ts[0] 取 vs[0]；t>=ts[-1] 取 vs[-1]。

    与原 Python 版 `np.interp` / lambda 的语义一致；
    端点外推取常值，对应"恒温段延拓"口径（H6／N19／N20）。
    """
    n = ts.shape[0]
    if t <= ts[0]:
        return vs[0]
    if t >= ts[n - 1]:
        return vs[n - 1]
    lo = 0
    hi = n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if ts[mid] <= t:
            lo = mid
        else:
            hi = mid
    w = (t - ts[lo]) / (ts[hi] - ts[lo])
    return vs[lo] + w * (vs[hi] - vs[lo])


# ==================================================================
# A｜子步循环下沉：一个输出步的全部内部子步 + Picard 迭代，一次 njit 调用完成
#     （数学流程与 q2_core_c.step_imex **逐行等价**）
# ==================================================================
@njit(cache=True, fastmath=False)
def _step_all_nb(N, dr, h, n_sub, R0, hc, km, T, C, t0,
                 ts_env, Tenv_v, Cenv_v, d_fac, C0f, T0f,
                 omega, tol, maxit, mode_flag):
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
        tinf = _interp1_nb(ts, ts_env, Tenv_v)      # ← B 优化
        cinf = _interp1_nb(ts, ts_env, Cenv_v)      # ← B 优化

        # ① 物性（逐子步按局部状态更新；frozen 模式用 C0 常值）
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
        _assemble_T_nb(N, dr, h, R0, hc, rho, cp, kk, aT, bT, cT, kf)
        _rhs_T_nb(N, dr, h, R0, hc, rho, cp, Tcur, tinf, dT)
        Tcur = _thomas_nb(aT, bT, cT, dT)

        # ③④ C（Picard 线性化；D 随迭代中的 C 更新，T 固定）
        #    界面 D 取**沿 C 的积分平均**（修正口径；原调和平均仅对系数间断成立）
        #    ⚠ base 在 numpy 版是**新数组**（不复用缓冲）⟹ 此处同样 copy
        _rhs_C_nb(N, dr, h, R0, km, Ccur, cinf, dC)
        bse = dC.copy()
        Cit = Ccur.copy()
        for it in range(1, maxit + 1):
            if mode_flag == 1:
                Df = np.full(N, d_fac * 2.4e-3 * np.exp(-0.45 / C0f)
                             * np.exp(-3850.0 / (T0f + 273.15)))
            elif mode_flag == 2:
                Df = _faceD_nb(Cit, Tcur, 1.0, False, 8)
            else:
                Df = _faceD_nb(Cit, Tcur, d_fac, True, 8)
            _assemble_C_nb(N, dr, h, Df, R0, km, aC, bC, cC)
            Ctry = _thomas_nb(aC, bC, cC, bse)
            Cnew = np.empty(NC)
            for i in range(NC):
                Cnew[i] = omega * Ctry[i] + (1.0 - omega) * Cit[i]

            # 残差：与原式 max|Cnew-Cit| / max(1, max|Cnew|) 等价
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


def env_tables_from_att1(t_arr, T_arr, C_arr,
                         t_tail=14400.0, T_tail=50.00, C_tail=0.04999):
    """把附件1 时序转为 njit 可用的等长数组，并实现**恒温段常值延拓**。

    ⚠ **延拓口径（H6／N19／N20，必须严格遵守）**：
        t ≤ 14400 s ：附件1 原数据（线性插值）
        t >  14400 s：**常值** T∞=50.00 ℃、C∞=0.04999

    实现：把 (t_tail, T_tail) 与 (t_tail+1, T_tail) 两点**追加在末尾**，
    使 t>t_tail 时插值恒为常值 T_tail（`_interp1_nb` 对 t>=ts[-1] 返回末值）。

    ⚠ 注意：附件1 末点本身是 (14400, 50.165)。本函数**不改动**该点，
       故 t=14400 处取 50.165、t>14400 处取 50.00——与 Q2 主力口径
       （`np.interp(t, ...) if t <= t_arr[-1] else 50.00`）**完全一致**。
    """
    # ⚠ 追加点的时间必须**严格大于** t_arr[-1]，否则产生重复节点，
    #    二分插值会出现 0/0。取 +1e-6 s 的微小偏移：对物理量无影响
    #    （内部步长 1/32 s，远大于 1e-6 s）。
    t0 = t_arr[-1]
    ts = np.ascontiguousarray(
        np.concatenate([t_arr, [t0 + 1e-6, t0 + 1.0]]), dtype=np.float64)
    Tv = np.ascontiguousarray(
        np.concatenate([T_arr, [T_tail, T_tail]]), dtype=np.float64)
    Cv = np.ascontiguousarray(
        np.concatenate([C_arr, [C_tail, C_tail]]), dtype=np.float64)
    return ts, Tv, Cv


def step_imex_fast(N, dr, h, n_sub, R0, hc, km, T, C,
                   ts_env, Tenv_v, Cenv_v, t0,
                   omega=0.7, tol=1e-10, maxit=30, mode='coupled'):
    """A/B 优化版的一输出步推进（接口与 q2_core_c.step_imex 兼容，
    但环境边界以**查表数组**传入而非 lambda）。返回 (T, C, info)。"""
    mf = MODE_MAP[mode]
    Tk, Ck, inner_tot, res_max = _step_all_nb(
        N, dr, h, n_sub, R0, hc, km,
        np.ascontiguousarray(T, dtype=np.float64),
        np.ascontiguousarray(C, dtype=np.float64),
        float(t0), ts_env, Tenv_v, Cenv_v, float(D_FAC),
        float(DEF2['C0']), float(DEF2['T0']),
        float(omega), float(tol), int(maxit), int(mf))
    return Tk, Ck, dict(inner_tot=inner_tot, nsub=n_sub, res_max=res_max,
                        outer_it=1, res_T=None, res_C=None, flag='ok', res_hist=[])
