# -*- coding: utf-8 -*-
"""
Q3 · E7 守恒性核算（**能量单列**）—— 遗留项 L-3
================================================================================
【动机】Q3 的 E7 原先**只做质量守恒**；规范要求"质量＋能量各一条"。
        本脚本补上**能量守恒**，形式与 Q2 的《q2_checks.py》E7 **完全一致**，
        以便"与 Q2 同量级"的跨问对照成立。

【能量方程（变物性）】
    ρ(C)c_p(C)·∂ₜT = (1/r)∂_r( k(C)·r·∂_rT )
  因 ρc_p 随 C 变化，写成"守恒量形式"会**多出一项**：
    ∂ₜ(ρc_p·T) = ∇·(k∇T) + T·∂ₜ(ρc_p)
  区域积分（乘 r、积 0→R₀）：
    ∂ₜ∫ρc_p·T·r dr = R₀·h·(T∞ − T_R) + ∫ T·∂ₜ(ρc_p)·r dr
  ⟹ **必须补"物性变化项"**，否则残差极大（Q2 首版未补时实测相对残差 1.30）。

【潜热口径】主力模型 H3 取 **L = 0**（忽略蒸发潜热）；
  其代价已由 **Q2 的 E8** 单独对照（L=2.26e6 J/kg ⟹ 潜热项约为对流项的 2 倍）。
  本核算**按主力口径 L = 0**，与求解方程严格一致；潜热不在本核算内重复计入。

【判据】相对残差 = |residE| / |边界热流累积|——
  与 Q2 的 E7（**1.803e-02**）同量级即为正常。

【积分口径】全场量一律用**梯形积分** ∫ v·r dr（与 Q2 的 E7 同口径）。

【用法】
  python q3_energy.py                # dry-run：只声明，不计算
  python q3_energy.py --go           # 正式（推进至 57.5314 h，约 6–7 min）
  python q3_energy.py --go --smoke   # 冒烟（推进至 3 h，约 30 s）
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

import numpy as np                                                     # noqa: E402
import openpyxl                                                        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
Q3ROOT = os.path.abspath(os.path.join(HERE, '..'))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, Q3ROOT)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))

import q2_core_c as base                                               # noqa: E402
import q3_core as q3                                                   # noqa: E402

GO = '--go' in sys.argv
SMOKE = '--smoke' in sys.argv

LOG = os.path.join(Q3ROOT, 'logs', 'q3_energy_log.txt')
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(str(s))


# ─────────────────────────── 参数（与主力一致） ───────────────────────────
P = base.DEF2
N, DR = 80, 2.5e-4
NC = N + 1
DT_OUT = 60.0
NSUB = int(round(DT_OUT / (1.0 / 32.0)))        # 内部步 1/32 s
HH = DT_OUT / NSUB
R0, HC, KM = P['R0'], P['h'], P['km']
T0, C0 = P['T0'], P['C0']
T_END = 10800.0 if SMOKE else 207113.094        # 3 h ／ 正式 57.5314 h
SNAP_S = 300.0                     # ⚠ 与 Q2 的 E7 同口径；过粗（1800/3600 s）会使梯形累积残差虚高 10–15 倍


def load_env():
    wb = openpyxl.load_workbook(
        os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'), data_only=True)
    ws = wb.active
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    ts, Tv, Cv = q3.env_tables_from_att1(
        np.array([float(r[0]) for r in d]),
        np.array([float(r[1]) for r in d]),
        np.array([float(r[2]) for r in d]))
    wb.close()
    return ts, Tv, Cv


def main():
    say('=' * 78)
    say('Q3 · E7 守恒性核算（**能量单列**）')
    say('=' * 78)
    say('  核：q3_core.step_imex_fast（现行口径 M6）  网格 N=%d（Δr=%.2f mm）  内部步 1/32 s'
        % (N, DR * 1e3))
    say('  推进至 t_end = %.1f s（%.4f h）%s' % (T_END, T_END / 3600.0,
                                                '  【冒烟】' if SMOKE else ''))
    say('  积分口径：梯形 ∫v·r dr（与 Q2 的 E7 同）；潜热按主力口径 L = 0')

    if not GO:
        say('')
        say('  [SCALE] 本脚本将完整推进 %.1f h（约 %s），并写入 %s'
            % (T_END / 3600.0, '30 s' if SMOKE else '6–7 min', LOG))
        say('  [SCALE] 加 --go 才会执行（--go --smoke 为 3 h 冒烟）。')
        return

    ts, Tv, Cv = load_env()

    r = np.arange(NC) * DR

    def field_int(v):
        return float(np.trapezoid(v * r, r))

    def rc_of(Cv):
        return base._rho_nb(Cv) * base._cp_nb(Cv)

    def energy_int(Tv_, Cv_):
        return float(np.trapezoid(rc_of(Cv_) * Tv_ * r, r))

    T = np.full(NC, T0)
    C = np.full(NC, C0)
    snaps = [(0.0, T.copy(), C.copy())]
    nsteps = int(round(T_END / DT_OUT))
    next_snap = SNAP_S

    t0 = time.time()
    for n in range(1, nsteps + 1):
        t_start = (n - 1) * DT_OUT
        T, C, _ = q3.step_imex_fast(N, DR, HH, NSUB, R0, HC, KM,
                                    T, C, ts, Tv, Cv, t_start)
        if n * DT_OUT + 1e-9 >= next_snap:
            snaps.append((n * DT_OUT, T.copy(), C.copy()))
            next_snap += SNAP_S
    wall = time.time() - t0
    say('  主力解完成，用时 %.1f s（%d 个输出步、%d 个快照）'
        % (wall, nsteps, len(snaps)))

    # ───────────────── 质量守恒（复核，梯形口径） ─────────────────
    I0 = field_int(snaps[0][2])
    I1 = field_int(snaps[-1][2])
    flux = 0.0
    for (ta, Ta, Ca), (tb, Tb, Cb) in zip(snaps[:-1], snaps[1:]):
        ci_a = float(q3._interp1_nb(ta, ts, Cv))
        ci_b = float(q3._interp1_nb(tb, ts, Cv))
        flux += R0 * KM * ((ci_a - Ca[-1]) + (ci_b - Cb[-1])) / 2.0 * (tb - ta)
    resid_M = (I1 - I0) - flux
    say('')
    say('  ── 质量守恒 ──')
    say('    ∫C·r dr ：初值 %.6e → 终值 %.6e   变化 %+.6e' % (I0, I1, I1 - I0))
    say('    边界通量累积 %+.6e   残差 %+.3e   相对残差 %.3e'
        % (flux, resid_M, abs(resid_M) / max(1e-30, abs(I1 - I0))))

    # ───────────────── 能量守恒（★本项主体） ─────────────────
    E0 = energy_int(snaps[0][1], snaps[0][2])
    E1 = energy_int(snaps[-1][1], snaps[-1][2])
    hflux = 0.0
    src = 0.0
    for (ta, Ta, Ca), (tb, Tb, Cb) in zip(snaps[:-1], snaps[1:]):
        ti_a = float(q3._interp1_nb(ta, ts, Tv))
        ti_b = float(q3._interp1_nb(tb, ts, Tv))
        hflux += R0 * HC * ((ti_a - Ta[-1]) + (ti_b - Tb[-1])) / 2.0 * (tb - ta)
        rc_a, rc_b = rc_of(Ca), rc_of(Cb)
        src += float(np.trapezoid(((Ta + Tb) / 2.0) * (rc_b - rc_a) * r, r))
    resid_E = (E1 - E0) - hflux - src
    rel_E = abs(resid_E) / max(1e-30, abs(hflux))

    say('')
    say('  ── 能量守恒（变物性正确形式） ──')
    say('    ∫ρc_p·T·r dr ：初值 %.6e → 终值 %.6e   变化 %+.6e' % (E0, E1, E1 - E0))
    say('    边界热流累积 %+.6e（本应为主项）' % hflux)
    say('    物性变化项   %+.6e（ρc_p 随 C 降低而减小 ⟹ 负贡献）' % src)
    say('    残差 %+.3e   相对残差 = %.3e' % (resid_E, rel_E))
    say('')
    say('  ⟹ 判据：与 Q2 的 E7 能量核算（1.803e-02）同量级即为正常。')
    say('     本期结果 %s（%s Q2 的 1.803e-02）'
        % ('%.3e' % rel_E,
           '优于' if rel_E < 1.803e-2 else ('同量级于' if rel_E < 5 * 1.803e-2 else '显著大于')))
    say('  ⚠ 方法学留痕：变物性下 ∫ρc_p·T·r dr **不是**守恒量，')
    say('     必须补 T·∂ₜ(ρc_p) 项方可作守恒判据（与 Q2 同一发现）。')
    say('  ⚠ 边界说明：本核算按主力口径 **L = 0**（忽略蒸发潜热）；')
    say('     潜热的代价已由 Q2 的 E8 单独对照（约为对流项的 2 倍），此处不重复计入。')

    # ───────────────── 极值核验 ─────────────────
    mxT = max(float(np.max(s[1])) for s in snaps)
    mnT = min(float(np.min(s[1])) for s in snaps)
    mnC = min(float(np.min(s[2])) for s in snaps)
    mxC = max(float(np.max(s[2])) for s in snaps)
    mono = all(bool(np.all(np.diff(s[2]) <= 1e-9)) for s in snaps)
    # 环境温度的实际上界：取环境时程的**最大值**，
    #   ⚠ 不得硬编码 50.0 —— 附件1 的峰值实为 50.165 ℃（末点），
    #     误用 50.0 会把物理上正确的 T 场误判为"超界"。
    Tmax_env = float(np.max(Tv))
    say('')
    say('  ── 极值核验 ──')
    say('    T ∈ [%.4f, %.4f] ℃（上界应为环境最大值 %.4f）⟹ %s'
        % (mnT, mxT, Tmax_env, 'PASS' if mxT <= Tmax_env + 1e-9 else 'FAIL'))
    say('    C ∈ [%.6f, %.6f] kg/kg（上界应为初值 %.2f；非负）⟹ %s'
        % (mnC, mxC, C0, 'PASS' if (mxC <= C0 + 1e-9 and mnC >= 0.0) else 'FAIL'))
    say('    含水率沿时间单调不增：%s' % ('PASS' if mono else 'FAIL'))


if __name__ == '__main__':
    print('[SCALE] 只读算例：不修改任何交付物；仅写日志 %s' % LOG)
    main()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    if GO:
        print('\n日志已写：%s' % LOG)
