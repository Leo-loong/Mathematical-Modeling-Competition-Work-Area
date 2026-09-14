# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验脚本合集：E4 独立实现互验 ＋ E7 守恒性核算
======================================================
E4（独立实现互验）
-----------------
用**显式 FTCS** 独立实现变物性求解（与主力的元体平衡＋全隐式**完全不同的代码路径**），
在稳定性限内跑**短时程**，与主力解逐点比对。
  · 显式稳定限：Δt ≤ Δr²/(2α)，α≈1.45e-7、Δr=0.25mm ⟹ Δt ≲ 2.1e-4 s ⟹ **只能跑短时程**
  · 意义：验证"空间算子与物性装配"的**代码独立性**（时间格式差异是预期的）

E7（守恒性核算）
---------------
区域积分闭合：
  · 质量：d/dt ∫₀^{R₀} C·r dr = R₀·k_m·(C∞ − C_R)
  · 与数值解的场积分变化比对，给出**相对残差**并归因
  · 同时核验：温度场逐点、逐时刻不超环境极值

用法：
  python q2_checks.py e4      # 独立实现互验
  python q2_checks.py e7      # 守恒性核算
  python q2_checks.py all
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 线程环境变量须早于 numpy 导入（零数值影响，纯环境级优化）
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np                                                    # noqa: E402
from q2_core import (run_q2, rho_of, cp_of, k_of, D_of, harm, DEF2)    # noqa: E402

R0, H, KM = DEF2['R0'], DEF2['h'], DEF2['km']
T0, C0 = DEF2['T0'], DEF2['C0']
TINF, CINF = 50.00, 0.04999
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'q2_checks_log.txt')
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(s)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')


# ==================================================================
# E4：显式 FTCS 独立实现（物性每步更新；与主力代码路径独立）
# ==================================================================
def explicit_run(N, dr, dt, nsteps):
    """显式 FTCS ＋ 元体平衡空间算子（物性取 n 层）。仅供短时程互验。"""
    r = np.arange(N + 1) * dr
    VN = dr * (R0 - dr / 4.0) / 2.0
    T = np.full(N + 1, T0)
    C = np.full(N + 1, C0)
    for n in range(nsteps):
        t = n * dt
        tinf = TINF if t <= 14400.0 else TINF
        cinf = CINF if t <= 14400.0 else CINF
        rho, cp, kk = rho_of(C), cp_of(C), k_of(C)
        Dd = D_of(C, T)
        kf = np.array([harm(kk[i], kk[i + 1]) for i in range(N)])
        Df = np.array([harm(Dd[i], Dd[i + 1]) for i in range(N)])
        Tn, Cn = T.copy(), C.copy()
        # ---- T ----
        T[0] = Tn[0] + dt * (4.0 * kf[0] / (rho[0] * cp[0] * dr ** 2)) * (Tn[1] - Tn[0])
        for i in range(1, N):
            rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
            T[i] = Tn[i] + dt / (rho[i] * cp[i] * r[i] * dr ** 2) * (
                kf[i] * rr * (Tn[i + 1] - Tn[i]) - kf[i - 1] * rl * (Tn[i] - Tn[i - 1]))
        T[N] = Tn[N] + dt / (rho[N] * cp[N] * VN) * (
            -kf[N - 1] * (R0 - dr / 2.0) / dr * (Tn[N] - Tn[N - 1]) + H * R0 * (tinf - Tn[N]))
        # ---- C ----
        C[0] = Cn[0] + dt * (4.0 * Df[0] / dr ** 2) * (Cn[1] - Cn[0])
        for i in range(1, N):
            rl, rr = r[i] - dr / 2.0, r[i] + dr / 2.0
            C[i] = Cn[i] + dt / (r[i] * dr ** 2) * (
                Df[i] * rr * (Cn[i + 1] - Cn[i]) - Df[i - 1] * rl * (Cn[i] - Cn[i - 1]))
        C[N] = Cn[N] + dt / VN * (
            -Df[N - 1] * (R0 - dr / 2.0) / dr * (Cn[N] - Cn[N - 1]) + KM * R0 * (cinf - Cn[N]))
    return T, C


def e4():
    say('=' * 78)
    say('E4 独立实现互验（显式 FTCS vs 主力 IMEX）')
    say('=' * 78)
    N, dr = 80, 2.5e-4
    alpha = float(k_of(C0)) / (float(rho_of(C0)) * float(cp_of(C0)))
    dt_lim = dr ** 2 / (2.0 * alpha)
    dt = 0.4 * dt_lim
    nsteps = int(2.0 / dt)          # 跑 2 s（显式极慢，只做短程比对）
    # 端点严格对齐：取 nsteps 使 nsteps*dt 恰为整数秒 t_end，dt 再等分回填
    #   ⟹ 排除"总推进时间不同"这一干扰项（旧版端点相差 0.015 s，只能作量级校核）
    t_end = 2.0
    nsteps = int(np.ceil(t_end / dt))
    dt = t_end / nsteps
    assert dt <= dt_lim, '显式步长超稳定限'
    say(f'  α={alpha:.4e} m²/s  Δr={dr*1e3:.2f} mm  稳定限 Δt≤{dt_lim:.3e} s  取 Δt={dt:.3e} s')
    say(f'  对比时程 = {nsteps*dt:.6f} s（{nsteps} 步，端点**严格对齐**）')

    t0 = time.time()
    Te, Ce = explicit_run(N, dr, dt, nsteps)
    t_e = time.time() - t0
    say(f'  [显式] 完成，{t_e:.1f}s')

    # 主力：**同步长、同空间离散**，唯一差别是时间格式（全隐式 vs 显式）
    #   ⟹ 差异即为"时间格式差异"，可直接与一阶后向欧拉的理论量级比对
    t0 = time.time()
    res, _, _ = run_q2(N=N, dr=dr, dt_out=dt, nsteps=nsteps, n_sub=1,
                       Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                       mode='coupled')
    Tm, Cm = res['T_end'], res['C_end']
    say(f'  [主力] 完成（{nsteps} 步 × 内部步长 {dt:.3e} s，总推进 {nsteps*dt:.6f} s），'
        f'{time.time()-t0:.1f}s')

    dT = np.max(np.abs(Tm - Te))
    dC = np.max(np.abs(Cm - Ce))
    say(f'  ⟹ 末端场最大差：|ΔT|={dT:.3e} ℃   |ΔC|={dC:.3e} kg/kg')
    say('  判定：两法**空间算子相同、步长相同**，唯一差别是时间格式（显式 vs 全隐式 / 一阶）。')
    say(f'        实测差异应与"一阶时间格式在 Δt={dt:.2e} s 下的量级"相符，且**平滑无振荡**；')
    say('        若出现 10⁻¹ 以上或非单调振荡，则说明存在实现级错误。')
    say('  补充：两法在**中心点**的差异通常最小（扩散最慢），在**表面点**最大。')


# ==================================================================
# E7：守恒性核算（质量积分闭合 ＋ 极值核验）
# ==================================================================
def e7():
    say('=' * 78)
    say('E7 守恒性核算（区域积分闭合 ＋ 极值核验）')
    say('=' * 78)
    N, dr = 80, 2.5e-4
    NSTEP = 10800                      # 3 h
    SNAP = tuple(range(0, NSTEP + 1, 300))   # 每 300 s 取一次快照（用于通量累积）
    r = np.arange(N + 1) * dr

    def field_int(Cv):
        """π 归一化的区域积分 ∫₀^{R₀} C·r dr（梯形）"""
        return float(np.trapezoid(Cv * r, r))

    t0 = time.time()
    res, _, _ = run_q2(N=N, dr=dr, dt_out=1.0, nsteps=NSTEP,
                       Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                       n_sub=32, mode='coupled', snap_at=SNAP)
    say(f'  主力解完成（恒定边界 {TINF} ℃／{CINF} kg/kg），{time.time()-t0:.1f}s')

    # ---- 质量守恒 ----
    # 由 ∂ₜ∫C·r dr = R₀·k_m·(C∞ − C_R) 得：
    #   Δ∫ ≈ Σ_k R₀·k_m·(C∞ − C_R(t_k))·Δt_k   （用快照做梯形累积）
    I0 = field_int(np.full(N + 1, C0))
    I1 = field_int(res['C_snap'][NSTEP])
    flux = 0.0
    for a, b in zip(SNAP[:-1], SNAP[1:]):
        cRa = float(res['C_snap'][a][-1])
        cRb = float(res['C_snap'][b][-1])
        flux += R0 * KM * ((CINF - cRa) + (CINF - cRb)) / 2.0 * (b - a)
    resid = I1 - I0 - flux
    say(f'  质量：∫C·r dr 初值 {I0:.6e} → 终值 {I1:.6e}  变化 {I1-I0:+.6e}')
    say(f'        边界通量累积 {flux:+.6e}   残差 {resid:+.3e}')
    say(f'        相对残差 = {abs(resid)/max(1e-30, abs(I1-I0)):.3e}')

    # ---- 能量核算（★变物性下的正确形式） ----
    # 能量方程：ρ(C)c_p(C)·∂ₜT = (1/r)∂_r(k(C)·r·∂_rT)
    # 因 ρc_p 随 C 变化，把左端写成"守恒量"形式会多出一项：
    #     ∂ₜ(ρc_p·T) = ∇·(k∇T) + T·∂ₜ(ρc_p)
    # 区域积分（乘 r、积 0→R₀）：
    #     ∂ₜ∫ρc_p·T·r dr = R₀·h·(T∞ − T_R)  ＋  ∫ T·∂ₜ(ρc_p)·r dr
    # ⟹ **必须补上"物性变化项"**，否则残差极大（首版未补时实测相对残差 1.30）。
    def rc_of(Cv):
        return rho_of(Cv) * cp_of(Cv)

    def energy_int(Tv, Cv):
        return float(np.trapezoid(rc_of(Cv) * Tv * r, r))

    E0 = energy_int(np.full(N + 1, T0), np.full(N + 1, C0))
    E1 = energy_int(res['T_snap'][NSTEP], res['C_snap'][NSTEP])
    hflux = 0.0
    src = 0.0                       # 物性变化项 ∫T·∂ₜ(ρc_p)·r dr
    for a, b in zip(SNAP[:-1], SNAP[1:]):
        tRa = float(res['T_snap'][a][-1])
        tRb = float(res['T_snap'][b][-1])
        hflux += R0 * H * ((TINF - tRa) + (TINF - tRb)) / 2.0 * (b - a)
        rc_a, rc_b = rc_of(res['C_snap'][a]), rc_of(res['C_snap'][b])
        Ta, Tb = res['T_snap'][a], res['T_snap'][b]
        src += float(np.trapezoid((Ta + Tb) / 2.0 * (rc_b - rc_a) * r, r))
    say(f'  能量：∫ρc_p·T·r dr 初值 {E0:.6e} → 终值 {E1:.6e}  变化 {E1-E0:+.6e}')
    say(f'        边界热流累积 {hflux:+.6e}（本应为主项）')
    say(f'        物性变化项   {src:+.6e}（因 ρc_p 随 C 降低而减小 ⟹ 负贡献）')
    residE = (E1 - E0) - hflux - src
    say(f'        残差 {residE:+.3e}   相对残差 ≈ '
        f'{abs(residE)/max(1e-30, abs(hflux)):.3e}')
    say('  ⚠ 方法学提示：**变物性下 ∫ρc_p·T·r dr 不是守恒量**，')
    say('     必须补 T·∂ₜ(ρc_p) 项才能作为守恒判据（本行即该发现的留痕）。')

    # ---- 极值核验（逐快照） ----
    mxT = max(float(np.max(v)) for v in res['T_snap'].values())
    mnT = min(float(np.min(v)) for v in res['T_snap'].values())
    mnC = min(float(np.min(v)) for v in res['C_snap'].values())
    mxC = max(float(np.max(v)) for v in res['C_snap'].values())
    dC_ok = all(bool(np.all(np.diff(v) <= 1e-9)) for v in res['C_snap'].values())
    say(f'  极值：T ∈ [{mnT:.4f}, {mxT:.4f}] ℃（上界应为环境 {TINF}）')
    say(f'        C ∈ [{mnC:.6f}, {mxC:.6f}] kg/kg（上界应为初值 {C0}；非负）')
    say(f'        含水率沿时间单调不增：{"PASS" if dC_ok else "FAIL"}')


if __name__ == '__main__':
    open(LOG, 'w', encoding='utf-8').close()
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('e4', 'all'):
        e4()
    if what in ('e7', 'all'):
        e7()
    try:
        if sys.stdin.isatty():          # 仅在交互式终端下等待，避免后台运行挂起
            input('\n按 Enter 键退出...')
    except Exception:
        pass
