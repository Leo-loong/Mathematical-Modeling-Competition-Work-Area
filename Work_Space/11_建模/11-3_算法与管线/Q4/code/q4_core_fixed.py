# -*- coding: utf-8 -*-
"""
A 题 Q4 求解核：物料坐标 ξ=r/R(t) 守恒形式（MB-11 + L3-09）
================================================================================
离散方案（元体平衡，全部推导见《A_Q4求解思路与工作流》v2 §2.1）：
  质量方程（×R² 前的守恒形式）:  ξ ∂tC̃ = (1/R²) ∂ξ(ξ D ∂ξC̃)
      内部:  ξ_jΔξ dC_j/dt = (1/R²)[ξ_{j+1/2}D_{j+1/2}ΔC − ξ_{j−1/2}D_{j−1/2}ΔC]/Δξ
      中心:  dC_0/dt = 4 D_{1/2} (C_1−C_0) / (R²Δξ²)
      表面:  V_N^ξ dC_N/dt = −(1/R²)ξ_{N−1/2}D_{N−1/2}ΔC/Δξ − (k_m/R)(C_N−C∞)
  能量方程（守恒形式）:  ξ ∂t[ρc_p T R²] = ∂ξ(k ξ ∂ξT)
      内部:  ξ_jΔξ[(ρc_pT)^{n+1}R_{n+1}² − (ρc_pT)^n R_n²]/h = [kξΔT 差]/Δξ
      中心:  [(ρc_pT)^{n+1}R_{n+1}² − (ρc_pT)^n R_n²]/h = 4k_{1/2}(T_1−T_0)/Δξ²
             （行已除以 R_{n+1}²，避免大数标度）
      表面:  V_N^ξ[...] /h = −kξ_{N−1/2}ΔT/Δξ + h R_{n+1}(T∞−T_N)
  固定域极限（R≡R0, Δξ=Δr/R0）下逐项退化为 Q1/Q2 格式（E3-g-② 复用检验的依据）。

时间推进：IMEX 交替（物性逐内部子步更新）；D6 取层口径由 t_corr 开关控制：
  t_corr=0 ：纯滞后（ρc_p 用 C^n）——Q2 同款
  t_corr=1 ：预估–校正（C 解出后用 ρc_p(C^{n+1}) 重解一次 T）——交付解 ρc_p 取 n+1 层
R(t) 取当前子步两端时刻的线性插值值（附件2，端点钳位＝H7 末段常值外推）。

性能：全部热路径 njit（fastmath=False 保持可复现）；一个输出步的全部子步
一次 njit 调用完成（q3_core 的"子步下沉"范式）。
"""
import sys, os, time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

try:
    from numba import njit
    _HAS_NUMBA = True
except Exception:
    _HAS_NUMBA = False
    def njit(*a, **k):
        if len(a) == 1 and callable(a[0]):
            return a[0]
        def deco(f):
            return f
        return deco

DEF4 = dict(R0=0.02, h=25.0, km=8.0e-7, T0=28.0, C0=2.55)
D_FAC = 1.0            # D0 灵敏度缩放因子（OAT 用）
CM = 273.15            # ℃ -> K


# ==================================================================
# 物性（附录4；T 内部用 ℃，D 公式内转 K）。app3=True 时切换附录3（复用检验用）
# ==================================================================
@njit(cache=True, fastmath=False)
def _rho_nb(C, app3):
    if app3:
        return 650.0 + 128.0 * C
    return 760.0 + 90.0 * C


@njit(cache=True, fastmath=False)
def _cp_nb(C, app3):
    if app3:
        return 1450.0 + 2736.0 * C / (C + 1.0)
    return 1850.0 + 2150.0 * C / (C + 1.0)


@njit(cache=True, fastmath=False)
def _k_nb(C, app3):
    if app3:
        return 0.21 + 0.38 * C / (C + 1.0)
    return 0.12 + 0.20 * C / (C + 1.0)


@njit(cache=True, fastmath=False)
def _D_nb(C, Tc, d_fac, app3):
    c = C
    if c < 1e-9:
        c = 1e-9
    if app3:
        return d_fac * 2.4e-3 * np.exp(-0.45 / c) * np.exp(-3850.0 / (Tc + CM))
    return d_fac * 4.2e-4 * np.exp(-0.30 / c) * np.exp(-3850.0 / (Tc + CM))


@njit(cache=True, fastmath=False)
def _iface_nb(f):
    """界面值：距离加权调和平均（与 q2_core_c.iface 同式）。

    ⚠ 旧口径（仅保留作 S2 旧口径对照与新口径对照实验），主力已改用
    _facek4_nb／_faceD4_nb（沿 C 的积分平均，2026-09-11 口径纠偏后）。
    """
    n = f.shape[0]
    out = np.empty(n - 1)
    for i in range(n - 1):
        l = f[i]
        r = f[i + 1]
        s = l + r
        if s > 0.0:
            out[i] = 2.0 * l * r / s
        else:
            out[i] = 0.0
    return out


@njit(cache=True, fastmath=False)
def _facek4_nb(Carr, app3):
    """★修正口径（Q4 版）：界面导热系数取【沿 C 的积分平均】（解析式）。

        ⟨k⟩ = k0 + k1·Δ(C − ln(1+C))/ΔC ，(k0,k1) = 附录4 (0.12,0.20)／附录3 (0.21,0.38)

    依据：单元内稳态通量 J=(1/Δr)∫k dC ⟹ 界面系数=沿 C 积分平均。
    调和平均只对"界面处系数间断"成立；Q4 尾部单胞内 D/k 为连续急变（同 Q3）。
    模板：q2_core_c._facek_nb（只读复制，系数换附录4）。|ΔC|≈0 退化为节点值。
    """
    n = Carr.shape[0] - 1
    out = np.empty(n)
    for i in range(n):
        a = Carr[i]
        b = Carr[i + 1]
        if abs(b - a) < 1e-14:
            c = a
            if app3:
                out[i] = 0.21 + 0.38 * c / (1.0 + c)
            else:
                out[i] = 0.12 + 0.20 * c / (1.0 + c)
        else:
            ga = a - np.log(1.0 + a)
            gb = b - np.log(1.0 + b)
            if app3:
                out[i] = 0.21 + 0.38 * (gb - ga) / (b - a)
            else:
                out[i] = 0.12 + 0.20 * (gb - ga) / (b - a)
    return out


@njit(cache=True, fastmath=False)
def _faceD4_nb(Carr, Tarr, d_fac, useT, nsamp, app3):
    """★修正口径（Q4 版）：界面扩散系数取【沿 C 的积分平均】（nsamp 点中矩采样）。

        ⟨D⟩ = [D0·⟨e^{-β/C}⟩_C]·[e^{-3850/T_face_K}] ，
        (D0,β) = 附录4 (4.2e-4,0.30)／附录3 (2.4e-3,0.45)

    利用可分离性只需对 C 因子采样；T 取界面两侧均值的 T 因子（T 内部 ℃，转 K）。
    useT=False：仅 C 因子（decoupled，不乘 d_fac）。|ΔC|≈0 退化为节点值。
    模板：q2_core_c._faceD_nb（只读复制，系数换附录4）。
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
            if app3:
                fv = np.exp(-0.45 / c)
            else:
                fv = np.exp(-0.30 / c)
        else:
            s = 0.0
            for q in range(nsamp):
                x = lo + (hi - lo) * (q + 0.5) / nsamp
                if x < 1e-9:
                    x = 1e-9
                if app3:
                    s += np.exp(-0.45 / x)
                else:
                    s += np.exp(-0.30 / x)
            fv = s / nsamp
        if useT:
            Tm = 0.5 * (Tarr[i] + Tarr[i + 1])
            if app3:
                out[i] = d_fac * 2.4e-3 * fv * np.exp(-3850.0 / (Tm + 273.15))
            else:
                out[i] = d_fac * 4.2e-4 * fv * np.exp(-3850.0 / (Tm + 273.15))
        else:
            if app3:
                out[i] = 2.4e-3 * fv
            else:
                out[i] = 4.2e-4 * fv
    return out


@njit(cache=True, fastmath=False)
def _thomas_nb(a, b, c, d):
    n = b.shape[0]
    cp = np.empty(n)
    dp = np.empty(n)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = np.empty(n)
    x[n - 1] = dp[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


@njit(cache=True, fastmath=False)
def _interp1_nb(t, ts, vs):
    """分段线性插值，端点钳位（附件1/附件2 的常值延拓口径）。"""
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
# 一个输出步的全部子步（下沉 njit）
#   mode: 0=coupled 1=frozen(物性冻结于 C0) 2=decoupled(D 不含 T)
#   flags: k_zero(绝热自检) fixR(R≡R0) app3(附录3 物性)
#   t_corr: 0=IMEX 滞后  1=预估–校正（D6 方案 b）
# ==================================================================
@njit(cache=True, fastmath=False)
def _step_all_nb(N, dxi, hsub, n_sub, R0, hc, km, T, C, t0,
                 ts_env, Tenv_v, Cenv_v, ts_R, Rv,
                 d_fac, C0f, omega, tol, maxit,
                 mode_flag, k_zero, fixR, app3, t_corr, hcv, L):
    NC = N + 1
    Tcur = T.copy()
    Ccur = C.copy()
    if hcv >= 0.0:
        hc = hcv          # 绝热自检等场景的对流系数覆盖（0 = 完全绝热）

    aT = np.zeros(NC); bT = np.zeros(NC); cT = np.zeros(NC); dT = np.zeros(NC)
    aC = np.zeros(NC); bC = np.zeros(NC); cC = np.zeros(NC); dC = np.zeros(NC)

    xi = np.empty(NC)
    xih = np.empty(N)          # ξ_{j+1/2}, j=0..N-1
    for j in range(NC):
        xi[j] = j * dxi
    for j in range(N):
        xih[j] = (j + 0.5) * dxi
    V0 = dxi * dxi / 4.0                 # 中心控制体（ξ 域）
    VN = dxi * (1.0 - dxi / 4.0) / 2.0   # 表面控制体（ξ 域）

    inner_tot = 0
    res_max = 0.0

    for s in range(n_sub):
        t0s = t0 + s * hsub
        t1s = t0s + hsub
        tinf = _interp1_nb(t1s, ts_env, Tenv_v)
        cinf = _interp1_nb(t1s, ts_env, Cenv_v)
        if fixR:
            R1 = R0
            R0m = R0
        else:
            R1 = _interp1_nb(t1s, ts_R, Rv)
            R0m = _interp1_nb(t0s, ts_R, Rv)
        R1sq = R1 * R1

        # ---- ① 物性（子步起点状态；frozen 用 C0 常值） ----
        if mode_flag == 1:
            rho = np.empty(NC); cp = np.empty(NC); kk = np.empty(NC)
            for j in range(NC):
                rho[j] = _rho_nb(C0f, app3)
                cp[j] = _cp_nb(C0f, app3)
                kk[j] = _k_nb(C0f, app3)
        else:
            rho = np.empty(NC); cp = np.empty(NC); kk = np.empty(NC)
            for j in range(NC):
                rho[j] = _rho_nb(Ccur[j], app3)
                cp[j] = _cp_nb(Ccur[j], app3)
                kk[j] = _k_nb(Ccur[j], app3)
        if k_zero:
            for j in range(NC):
                kk[j] = 0.0

        # ---- ② T（全隐式，能量守恒形式） ----
        # ★修正口径：界面 k 取沿 C 积分平均（k 只依赖 C，直接由节点 C 求）；
        #   k_zero（绝热自检）在面系数上整体置零
        kf = _facek4_nb(Ccur, app3)
        if k_zero:
            for j in range(N - 1 + 1):
                kf[j] = 0.0
        Told = Tcur.copy()      # D6 校正步需要旧状态（防 Q2-α 重复推进）
        rho_o = rho.copy()
        cp_o = cp.copy()
        # 内部 1..N-1（★r 空间标定，q2 同款；固定域极限逐字一致）
        # ★存储项口径（E7b 能量核算 0.645 暴露、绝热判决实验证实后修正）：
        #   整行除以 R1 后，老态项必须为 ξ_j·R0m²/R1（即 rj0 = j·drp·(R0m/R1)²），
        #   否则守恒形式 d/dt[ρcp·T·R²] 的几何压缩项被系统性减半（fixR 时 R0m=R1 不可见）。
        drp = R1 * dxi              # Δr' = R1·Δξ（新时层 r 间距）
        for j in range(1, N):
            rl = (j - 0.5) * drp
            rr = (j + 0.5) * drp
            rj1 = j * drp                    # r_j^{n+1}
            rj0 = j * drp * (R0m / R1) ** 2  # ξ_j·R0m²/R1（老态体积元，含 R² 口径）
            aT[j] = -kf[j - 1] * rl / (drp * drp)
            cT[j] = -kf[j] * rr / (drp * drp)
            bT[j] = (rho[j] * cp[j] * rj1 / hsub
                     + (kf[j] * rr + kf[j - 1] * rl) / (drp * drp))
            dT[j] = rho[j] * cp[j] * Tcur[j] * rj0 / hsub
        # 中心 0（行除以 R1sq；固定域极限下 = Q1 中心行）
        bT[0] = rho[0] * cp[0] / hsub + 4.0 * kf[0] / (R1sq * dxi * dxi)
        cT[0] = -4.0 * kf[0] / (R1sq * dxi * dxi)
        dT[0] = rho[0] * cp[0] * Tcur[0] * (R0m * R0m) / (R1sq * hsub)
        aT[0] = 0.0
        # 表面 N
        bT[N] = (VN * rho[N] * cp[N] * R1sq / hsub
                 + kf[N - 1] * xih[N - 1] / dxi + hc * R1)
        aT[N] = -kf[N - 1] * xih[N - 1] / dxi
        cT[N] = 0.0
        dT[N] = (VN * rho[N] * cp[N] * Tcur[N] * R0m * R0m / hsub
                 + hc * R1 * tinf)
        if L > 0.0:
            # E8 潜热对照：表面蒸发吸热源项（显式，用子步起点 C；q2_core_latent 同式）
            dT[N] -= L * km * R1 * (Ccur[N] - cinf)
        Tcur = _thomas_nb(aT, bT, cT, dT)

        # ---- ③ C（Picard；右端固定＝存储项，Q1 P-1 纪律） ----
        # 行标定：内点 r 空间（q2 同款），中心/表面行保持守恒形式（数学等价）
        dC[0] = Ccur[0] / hsub
        for j in range(1, N):
            dC[j] = j * drp * Ccur[j] / hsub          # r_j^{n+1}·C^n/Δt
        dC[N] = VN * R1sq * Ccur[N] / hsub + km * R1 * cinf

        # 右端固定（Q1 P-1 纪律）：bse 在 Picard 中不变
        bse = dC.copy()

        Cit = Ccur.copy()
        for it in range(1, maxit + 1):
            # ★修正口径：界面 D 取沿 C 的积分平均（8 点中矩）；T 因子用界面均值 T
            if mode_flag == 1:
                # frozen：D(C0,T0) 常值（面值＝节点值，调和/积分平均同）
                Df = np.empty(N - 1 + 1)
                dv = _D_nb(C0f, 28.0, d_fac, app3)
                for j in range(N - 1 + 1):
                    Df[j] = dv
            elif mode_flag == 2:
                Df = _faceD4_nb(Cit, Tcur, 1.0, False, 8, app3)   # decoupled：仅 C 因子
            else:
                Df = _faceD4_nb(Cit, Tcur, d_fac, True, 8, app3)  # coupled
            # 中心行
            bC[0] = 1.0 / hsub + 4.0 * Df[0] / (R1sq * dxi * dxi)
            cC[0] = -4.0 * Df[0] / (R1sq * dxi * dxi)
            # 内部行补 D（r 空间标定，q2 同款）
            for j in range(1, N):
                aC[j] = -Df[j - 1] * (j - 0.5) * drp / (drp * drp)
                cC[j] = -Df[j] * (j + 0.5) * drp / (drp * drp)
                bC[j] = j * drp / hsub + (Df[j] * (j + 0.5) * drp
                                          + Df[j - 1] * (j - 0.5) * drp) / (drp * drp)
            # 表面行补 D
            bC[N] = VN * R1sq / hsub + Df[N - 1] * xih[N - 1] / dxi + km * R1
            aC[N] = -Df[N - 1] * xih[N - 1] / dxi

            Ctry = _thomas_nb(aC, bC, cC, bse)
            Cnew = np.empty(NC)
            num = 0.0
            den = 0.0
            for j in range(NC):
                v = omega * Ctry[j] + (1.0 - omega) * Cit[j]
                dv = v - Cit[j]
                if dv < 0.0:
                    dv = -dv
                if dv > num:
                    num = dv
                av = v if v >= 0.0 else -v
                if av > den:
                    den = av
                Cnew[j] = v
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

        # ---- ④ D6 方案 b：用 C^{n+1} 的 ρc_p 重解一次 T（交付解 ρc_p 取 n+1 层） ----
        # ⚠ 右端存储项必须用【旧状态】(T^n, ρc_p(C^n), R_n)——否则即 Q2-α 重复推进
        if t_corr == 1 and (not k_zero):
            for j in range(NC):
                if mode_flag == 1:
                    rho[j] = _rho_nb(C0f, app3)   # frozen：ρc_p 保持冻结常量
                    cp[j] = _cp_nb(C0f, app3)     # （b/d 两侧口径一致，防伪源项）
                else:
                    rho[j] = _rho_nb(Ccur[j], app3)
                    cp[j] = _cp_nb(Ccur[j], app3)
            kf = _facek4_nb(Ccur, app3)
            if k_zero:
                for j in range(N):
                    kf[j] = 0.0
            for j in range(1, N):
                rl = (j - 0.5) * drp
                rr = (j + 0.5) * drp
                rj1 = j * drp
                rj0 = j * drp * (R0m / R1) ** 2  # ★同预测步：ξ_j·R0m²/R1（老态体积元）
                aT[j] = -kf[j - 1] * rl / (drp * drp)
                cT[j] = -kf[j] * rr / (drp * drp)
                bT[j] = (rho[j] * cp[j] * rj1 / hsub
                         + (kf[j] * rr + kf[j - 1] * rl) / (drp * drp))
                dT[j] = rho_o[j] * cp_o[j] * Told[j] * rj0 / hsub
            bT[0] = rho[0] * cp[0] / hsub + 4.0 * kf[0] / (R1sq * dxi * dxi)
            cT[0] = -4.0 * kf[0] / (R1sq * dxi * dxi)
            dT[0] = rho_o[0] * cp_o[0] * Told[0] * (R0m * R0m) / (R1sq * hsub)
            bT[N] = (VN * rho[N] * cp[N] * R1sq / hsub
                     + kf[N - 1] * xih[N - 1] / dxi + hc * R1)
            aT[N] = -kf[N - 1] * xih[N - 1] / dxi
            dT[N] = (VN * rho_o[N] * cp_o[N] * Told[N] * R0m * R0m / hsub
                     + hc * R1 * tinf)
            if L > 0.0:
                # ★修正（E8 缺陷）：校正步必须与预测步同样计入潜热源项，
                #   否则 t_corr=1 下潜热效应被校正步整体抹除（旧日志 max|dT|~2e-9 的根因）。
                #   用 C^{n+1}（当前 Ccur）评估蒸发通量，与对流项同时层。
                dT[N] -= L * km * R1 * (Ccur[N] - cinf)
            Tcur = _thomas_nb(aT, bT, cT, dT)

    return Tcur, Ccur, inner_tot, res_max


def load_R_table(xlsx_path):
    """读附件2 → (ts_R 秒, Rv 米)。端点钳位由 _interp1_nb 承担（H7 末段常值）。"""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    data = [(float(r[0]), float(r[1])) for r in rows[1:] if r[0] is not None]
    ts = np.ascontiguousarray([d[0] for d in data], dtype=np.float64)
    Rv = np.ascontiguousarray([d[1] / 100.0 for d in data], dtype=np.float64)  # cm→m
    return ts, Rv


def env_tables_from_att1(t_arr, T_arr, C_arr,
                         t_tail=14400.0, T_tail=50.00, C_tail=0.04999):
    """附件1 → njit 查表数组（恒温段常值延拓，口径同 q3_core 同名函数）。"""
    t0 = t_arr[-1]
    ts = np.ascontiguousarray(
        np.concatenate([t_arr, [t0 + 1e-6, t0 + 1.0]]), dtype=np.float64)
    Tv = np.ascontiguousarray(
        np.concatenate([T_arr, [T_tail, T_tail]]), dtype=np.float64)
    Cv = np.ascontiguousarray(
        np.concatenate([C_arr, [C_tail, C_tail]]), dtype=np.float64)
    return ts, Tv, Cv


def step_imex4(N, dxi, hsub, n_sub, R0, hc, km, T, C, t0,
               ts_env, Tenv_v, Cenv_v, ts_R, Rv,
               omega=0.7, tol=1e-10, maxit=30, mode='coupled',
               k_zero=False, fixR=False, app3=False, t_corr=0, d_fac=1.0,
               hcv=-1.0, L=0.0):
    """推进一个输出步。返回 (T, C, info)。hcv>=0 时覆盖对流系数；L>0 为潜热源项。"""
    mf = {'coupled': 0, 'frozen': 1, 'decoupled': 2}[mode]
    Tk, Ck, it, rm = _step_all_nb(
        N, float(dxi), float(hsub), int(n_sub), float(R0), float(hc), float(km),
        np.ascontiguousarray(T, dtype=np.float64),
        np.ascontiguousarray(C, dtype=np.float64),
        float(t0), ts_env, Tenv_v, Cenv_v, ts_R, Rv,
        float(d_fac), float(DEF4['C0']), float(omega), float(tol), int(maxit),
        int(mf), 1 if k_zero else 0, 1 if fixR else 0, 1 if app3 else 0,
        int(t_corr), float(hcv), float(L))
    return Tk, Ck, dict(inner_tot=it, nsub=n_sub, res_max=rm)


def run_q4(N=80, t_end=60.0, dt_out=1.0, n_sub=32, out_every=None,
           ts_env=None, Tenv_v=None, Cenv_v=None, ts_R=None, Rv=None,
           mode='coupled', k_zero=False, fixR=False, app3=False, t_corr=0,
           collect_fields=(), verbose=False, hcv=-1.0, L=0.0):
    """驱动：从 t=0 推进到 t_end。collect_fields 给定采样时刻集合（秒），
    返回 (fields{t:(T,C)}, stats)。hcv>=0 时覆盖对流系数（绝热自检用 0）。"""
    dxi = 1.0 / N
    hsub = dt_out / n_sub
    T = np.full(N + 1, DEF4['T0'])
    C = np.full(N + 1, DEF4['C0'])
    fields = {}
    tot_it = 0
    rm_all = 0.0
    t_all = time.perf_counter()
    nsteps = int(round(t_end / dt_out))
    for k in range(1, nsteps + 1):
        t0 = (k - 1) * dt_out
        T, C, info = step_imex4(N, dxi, hsub, n_sub, DEF4['R0'], DEF4['h'],
                                DEF4['km'], T, C, t0, ts_env, Tenv_v, Cenv_v,
                                ts_R, Rv, mode=mode, k_zero=k_zero,
                                fixR=fixR, app3=app3, t_corr=t_corr, hcv=hcv,
                                L=L)
        tot_it += info['inner_tot']
        rm_all = max(rm_all, info['res_max'])
        tk = k * dt_out
        for tc in collect_fields:
            if abs(tk - tc) < 1e-9:
                fields[float(tc)] = (T.copy(), C.copy())
    # 终态必存（预试验/主力求解都需要末端场）
    fields[float(nsteps * dt_out)] = (T.copy(), C.copy())
    stats = dict(wall=time.perf_counter() - t_all, inner_tot=tot_it,
                 res_max=rm_all, nsteps=nsteps)
    return fields, stats


def interp_cubic(ksi_nodes, values, x):
    """一维四点三次插值（非均匀节点；单点）。节点须单调递增。"""
    return interp_lagrange(ksi_nodes, values, x, 4)


def interp_lagrange(ksi_nodes, values, x, npts=6):
    """n 点 Lagrange 插值（npts=4 三次 / 6 五次；窗口贴边钳位）。

    Q4 输出口径：默认 npts=6 —— S7 实测三次插值在 N=80 下误差 ~2.8e-5，
    贴 L3-07 上限；升到五次后插值分量降一个量级以上（见预试验 S7）。
    """
    n = len(ksi_nodes)
    if x <= ksi_nodes[0]:
        return values[0]
    if x >= ksi_nodes[-1]:
        return values[-1]
    hi = 1
    while hi < n - 1 and ksi_nodes[hi] < x:
        hi += 1
    lo = hi - 1
    i0 = lo - (npts // 2 - 1)
    if i0 < 0:
        i0 = 0
    if i0 + npts > n:
        i0 = n - npts
    xs = ksi_nodes[i0:i0 + npts]
    ys = values[i0:i0 + npts]
    s = 0.0
    for i in range(npts):
        term = ys[i]
        for j in range(npts):
            if j != i:
                term *= (x - xs[j]) / (xs[i] - xs[j])
        s += term
    return s
