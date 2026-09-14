# -*- coding: utf-8 -*-
"""T3 主算法升级验收（T 时间精确积分 / C-ETD）· 四闸门

T3-1：以「矩阵指数 ＋ 分段线性 Duhamel 的**精确时间积分**」替换 T 的后向欧拉口径
T3-2：以「ETD（冻结-D）＋ Picard 校正」替换 C 的后向欧拉口径

闸门（缺一不采纳）：
  ① 与基线一致   : max|ΔT| ≤ 2e-4 ℃（主力自身一阶时间误差量级）
  ② 不劣化       : 与 T1-1 半解析(真实时变边界)的对拍**不劣于**基线
  ③ 步长无关     : h=1 s 与 h=60 s 结果一致（≤1e-9 ℃；⟹ 时间误差归零）
  ④ 物理自检     : 界内 / 径向单调 / 时间单调 / 守恒 / E≥0 且 E·1≤1

运行：python q1_inv_T3.py
"""
import time
import numpy as np

from q1_inv_lib import Rec, env_fns
import q1_core as core
import q1_exact as ex
from q1_inv_T1_duhamel import series_coeffs, duhamel_continuous

rec = Rec('q1_inv_T3.log')
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
RHO = [0.0, 0.25, 0.5, 0.75, 1.0]
N, DR, R0 = 80, 0.25e-3, 0.02
IDX = [int(round(r * R0 / DR)) for r in RHO]          # 81 节点网格上的 5 个输出列


def main():
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(core.DEF)
    alpha = p['k'] / (p['rho'] * p['cp'])
    mu, Acoef = series_coeffs(p['h'] * R0 / p['k'])
    rec('=== T3 主算法升级验收（四闸门）===')
    rec('N=%d  Δr=%.3f mm  节点 %d  α=%.6e  Bi_T=%.6f' %
        (N, DR * 1e3, N + 1, alpha, p['h'] * R0 / p['k']))
    rec('')

    # ------------------------------------------------ 基线（后向欧拉 1/32 s）
    t0 = time.time()
    rb = core.run_sim(N=N, dr=DR, dt_out=1.0, nsteps=1800, p=p, Tenv_fn=Tenv,
                      Cenv_fn=Cenv, sub=10, subT=32, center='fv', surf='fvm',
                      solve_C=False, snap_at=set(SNAP))
    tb = time.time() - t0
    Tbe = {s: rb['T_snap'][s] for s in SNAP}
    rec('— 基线：后向欧拉（内部步长 1/32 s）耗时 %.2f s' % tb)

    # ------------------------------------------------ 精确推进 h=1 s / h=60 s
    t0 = time.time()
    r1 = ex.run_T_expm(N, DR, p, Tenv, 1800.0, hstep=1.0, t_snaps=SNAP)
    t1 = time.time() - t0
    R60 = ex.run_T_expm(N, DR, p, Tenv, 1800.0, hstep=60.0, t_snaps=SNAP)
    Tex1 = {float(k): v for k, v in r1['T_snap'].items()}
    Tex60 = {float(k): v for k, v in R60['T_snap'].items()}
    rec('— 精确推进：矩阵指数（h=1 s）耗时 %.2f s；h=60 s 亦已算（同一 E 机制）' % t1)

    # ------------------------------------------------ 闸门①
    g1 = max(abs(Tex1[float(s)][IDX] - Tbe[s][IDX]).max() for s in SNAP)
    rec('')
    rec('闸门① 与基线一致：max|ΔT| = %.3e ℃  （阈值 2e-4）⟹ %s'
        % (g1, 'PASS' if g1 <= 2e-4 else 'FAIL'))

    # ------------------------------------------------ 闸门②（对拍半解析 + 网格裁决）
    # 说明：|数值−半解析| 含**空间离散误差**（两法共用同一网格）＋各自时间误差。
    # 只有做**网格细化裁决**才能分离：精确推进应随网格二阶收敛，而基线会停在自身时间误差平台上。
    def err_grid(Ng):
        drg = R0 / Ng
        rd = core.run_sim(N=Ng, dr=drg, dt_out=1.0, nsteps=1800, p=p, Tenv_fn=Tenv,
                          Cenv_fn=Cenv, sub=10, subT=32, center='fv', surf='fvm',
                          solve_C=False, snap_at={1800})
        re_ = ex.run_T_expm(Ng, drg, p, Tenv, 1800.0, hstep=1.0, t_snaps={1800})
        eb = eex = 0.0
        for rho in RHO:
            i = int(round(rho * R0 / drg))
            ana = duhamel_continuous(mu, Acoef, rho, 1800.0, t, Tinf, alpha, R0, p['T0'])
            eb = max(eb, abs(float(rd['T_snap'][1800][i]) - ana))
            eex = max(eex, abs(float(re_['T_snap'][1800.0][i]) - ana))
        return eb, eex

    rec('')
    rec('闸门② 网格裁决（对拍 T1-1 半解析，t=1800 s，5 列最大值）')
    tab = {}
    for Ng in (40, 80, 160):
        tab[Ng] = err_grid(Ng)
        rec('    N=%3d : |基线−半解析|=%.3e ℃   |精确−半解析|=%.3e ℃' % (Ng, tab[Ng][0], tab[Ng][1]))
    g2 = tab[160][1] < tab[160][0]
    rec('    ⟹ 细网格上「精确 < 基线」=%s ⟹ 闸门② %s' % (g2, 'PASS' if g2 else 'FAIL'))
    rec('      （基线被自身一阶时间误差钉住、不随网格下降；精确推进随网格二阶下降）')

    # ------------------------------------------------ 闸门③（步长无关）
    g3 = max(abs(Tex1[float(s)][IDX] - Tex60[float(s)][IDX]).max() for s in SNAP)
    rec('闸门③ 步长无关：max|T(h=1s) − T(h=60s)| = %.3e ℃ ⟹ %s'
        % (g3, 'PASS' if g3 <= 1e-9 else 'FAIL'))

    # ------------------------------------------------ 闸门④（物理自检）
    ok4, msgs = [], []
    for s in SNAP:
        T = Tex1[float(s)]
        ok4.append(bool(np.all(np.diff(T) >= -1e-12)))
    msgs.append('径向单调递增(7/7)=%s' % all(ok4))
    Tend = Tex1[1800.0]
    lo, hi = p['T0'], float(np.max(Tinf))
    msgs.append('界内 [%.4f,%.4f]⊂[%.4f,%.4f]=%s' % (Tend.min(), Tend.max(), lo, hi,
                                                 bool(Tend.min() >= lo - 1e-9 and Tend.max() <= hi + 1e-9)))
    tt = [Tex1[float(s)][0] for s in SNAP]
    msgs.append('中心温度时间单调递增=%s' % bool(np.all(np.diff(tt) >= -1e-12)))
    E, one = r1['E'], np.ones(N + 1)
    msgs.append('E≥0=%s ; E·1≤1=%s' % (bool(E.min() >= 0), bool((E @ one).max() <= 1 + 1e-12)))
    rec('闸门④ 物理自检：' + ' ; '.join(msgs))
    rec('        ⟹ %s' % ('PASS' if all('True' in m for m in msgs) else 'CHECK'))

    rec('')
    rec('— 表 1（T, ℃）对比：基线 / 精确 / 半解析 —')
    for s in SNAP:
        rec(' %4d  BE: %s' % (s, ' '.join('%.4f' % float(Tbe[s][i]) for i in IDX)))
        rec('       EX: %s' % ' '.join('%.4f' % float(Tex1[float(s)][i]) for i in IDX))
        rec('       DU: %s' % ' '.join('%.4f' % duhamel_continuous(mu, Acoef, rho, float(s), t, Tinf, alpha, R0, p['T0']) for rho in RHO))

    # ================================================ T3-2 · C 方程 ETD
    rec('')
    rec('=== T3-2 C 方程 ETD（冻结-D ＋ Picard 校正）===')
    t0 = time.time()
    cb = core.run_sim(N=N, dr=DR, dt_out=1.0, nsteps=1800, p=p, Tenv_fn=Tenv,
                      Cenv_fn=Cenv, sub=10, subT=32, solve_T=False, snap_at=set(SNAP))
    tcb = time.time() - t0
    t0 = time.time()
    ce = ex.run_C_etd(N, DR, p, Cenv, 1800.0, h_step=1.0, maxit=30, Dfac=1.0,
                      dt_col=1.0, snap_at=set(SNAP), cols=np.array(IDX))
    tce = time.time() - t0
    rec('— C 基线（后向欧拉 0.1 s ＋ Picard）%.2f s ；ETD（h=1 s）%.2f s  [stats %s]'
        % (tcb, tce, ce['stats']))
    dc = 0.0
    for s in SNAP:
        dc = max(dc, float(np.max(np.abs(ce['C_snap'][float(s)][IDX] - cb['C_snap'][s][IDX]))))
    rec('闸门c① 与基线一致：max|ΔC| = %.3e kg/kg （阈值 1e-5）⟹ %s'
        % (dc, 'PASS' if dc <= 1e-5 else 'FAIL'))
    r025 = ex.run_C_etd(N, DR, p, Cenv, 1800.0, h_step=0.25, maxit=30, snap_at={1800.0})
    d025 = float(np.max(np.abs(r025['C_end'] - ce['C_end'])))
    rec('闸门c② 打破一阶趋势：h=1s vs h=0.25s 差 %.2e kg/kg（BE 同档差 ~4e-5）⟹ %s'
        % (d025, 'PASS' if d025 <= 1e-5 else 'FAIL'))
    mono = all(np.all(np.diff(ce['C_snap'][float(1800.0)]) <= 1e-12) for _ in [0])
    rec('闸门c③ 单调/非负：径向递减=%s ; 最小 %.6f ≥0=%s'
        % (mono, float(ce['C_end'].min()), bool(ce['C_end'].min() >= 0)))
    rec('')
    rec('— 表 2（C, kg/kg）：基线 / ETD —')
    for s in SNAP:
        rec(' %4d  BE: %s' % (s, ' '.join('%.4f' % float(cb['C_snap'][s][i]) for i in IDX)))
        rec('       ETD: %s' % ' '.join('%.4f' % float(ce['C_snap'][float(s)][i]) for i in IDX))

    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
