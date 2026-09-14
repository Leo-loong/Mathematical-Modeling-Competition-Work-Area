# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验 E8：蒸发潜热对照（H3 / RK-2）
======================================================
【问题】模型假设 H3 忽略"表面水分蒸发吸收的潜热"。这一简化的**代价**有多大？
【做法】同一算例（3 h、相同网格与步长）跑两次：
        · 基线：L = 0       （＝现有主力口径，忽略潜热）
        · 对照：L = 2.26e6  （水的汽化潜热，J/kg；表面热平衡加入 -L·k_m·(C_R - C∞)）
        给出偏差的**方向**与**幅度**。

【预判量级】终态：对流热流 h(T∞-T_R) ≈ 0.84 W/m²，
            蒸发耗热 L·k_m(C_R-C∞) ≈ 1.73 W/m² ⟹ **潜热项约为对流项的 2 倍** ⟹ 不应忽略。

运行：python q2_e8_latent.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                              # noqa: E402
import q2_core_latent as qc                                     # noqa: E402

LOG = os.path.join(HERE, 'q2_e8_log.txt')
BUF = []
TINF, CINF = 50.00, 0.04999
NSTEP, NSUB = 10800, 32
SNAP = (1800, 3600, 5400, 7200, 9000, 10800)


def _find_root(p, marker='10_赛题', _max=8):
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
        par = os.path.dirname(cur)
        if par == cur:
            break
        cur = par
    return None


ROOT = _find_root(HERE)
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx') if ROOT else None


def load_att1():
    from openpyxl import load_workbook
    wb = load_workbook(ATT1, data_only=True)
    ws = wb.active
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    data = [r for r in rows[1:] if r[0] is not None]
    return (np.array([float(r[0]) for r in data]),
            np.array([float(r[1]) for r in data]),
            np.array([float(r[2]) for r in data]))


def say(s=''):
    print(s, flush=True)
    BUF.append(s)


def flush_log():
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')


def run(L, t1=None, T1=None, C1=None):
    """t1/T1/C1 给出时用时变边界（真实工况）；否则恒定边界。"""
    qc.qc_L_LATENT = L
    if t1 is not None:
        def Tenv(t):
            return float(np.interp(t, t1, T1)) if t <= t1[-1] else TINF

        def Cenv(t):
            return float(np.interp(t, t1, C1)) if t <= t1[-1] else CINF
    else:
        Tenv = lambda _t: TINF          # noqa: E731
        Cenv = lambda _t: CINF          # noqa: E731
    t0 = time.time()
    res, _, _ = qc.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=NSTEP, n_sub=NSUB,
                          Tenv_fn=Tenv, Cenv_fn=Cenv,
                          mode='coupled', snap_at=SNAP)
    return res, time.time() - t0


def main():
    t00 = time.time()
    say('=' * 78)
    say('Q2 检验 E8：蒸发潜热对照（H3 / RK-2）')
    say('=' * 78)
    t1 = T1 = C1 = None
    if ATT1 and os.path.exists(ATT1):
        t1, T1, C1 = load_att1()
        say(f'  边界：**时变**（附件1 线性插值，{len(t1)} 点；t>{t1[-1]:.0f}s 取 '
            f'{TINF} ℃／{CINF}）——与主力口径一致')
    else:
        say('  ⚠ 未找到附件1，退化为恒定边界（结论只适用于恒定工况）')

    say('\n[基线] L = 0（忽略潜热，现行主力口径）')
    r0, w0 = run(0.0, t1, T1, C1)
    say(f'   耗时 {w0:.1f}s   T(0)={r0["T_end"][0]:.4f}  T(R)={r0["T_end"][-1]:.4f}  '
        f'C(0)={r0["C_end"][0]:.6f}  C(R)={r0["C_end"][-1]:.6f}')

    say('\n[对照] L = 2.26e6 J/kg（计入蒸发潜热）')
    r1, w1 = run(2.26e6, t1, T1, C1)
    say(f'   耗时 {w1:.1f}s   T(0)={r1["T_end"][0]:.4f}  T(R)={r1["T_end"][-1]:.4f}  '
        f'C(0)={r1["C_end"][0]:.6f}  C(R)={r1["C_end"][-1]:.6f}')

    # 与主力成果的一致性自检（L=0 时应与 result2.xlsx 的终态一致）
    say(f'\n  [自检] L=0 的 T(0) 应≈主力 49.8495 ⟹ 实测 {r0["T_end"][0]:.4f}  '
        f'（差 {r0["T_end"][0]-49.8495:+.4f} ℃；若显著非零，说明边界口径不同）')

    dT0 = r1['T_end'][0] - r0['T_end'][0]
    dTR = r1['T_end'][-1] - r0['T_end'][-1]
    dC0 = r1['C_end'][0] - r0['C_end'][0]
    dCR = r1['C_end'][-1] - r0['C_end'][-1]

    say('\n【偏差（计入潜热 − 忽略潜热）】3 h 末')
    say(f'   T(0)：{r0["T_end"][0]:.4f} → {r1["T_end"][0]:.4f}   Δ = {dT0:+.4f} ℃')
    say(f'   T(R)：{r0["T_end"][-1]:.4f} → {r1["T_end"][-1]:.4f}   Δ = {dTR:+.4f} ℃')
    say(f'   C(0)：{r0["C_end"][0]:.6f} → {r1["C_end"][0]:.6f}   Δ = {dC0:+.6f} kg/kg')
    say(f'   C(R)：{r0["C_end"][-1]:.6f} → {r1["C_end"][-1]:.6f}   Δ = {dCR:+.6f} kg/kg')

    say('\n【逐时刻温度偏差 ΔT = 计入 − 忽略】')
    say(f'   {"t/h":>5} {"ΔT(0)":>12} {"ΔT(R)":>12}   {"ΔC(0)":>13} {"ΔC(R)":>13}')
    for n in SNAP:
        aT, aC = r0['T_snap'][n], r0['C_snap'][n]
        bT, bC = r1['T_snap'][n], r1['C_snap'][n]
        say(f'   {n/3600:5.1f} {bT[0]-aT[0]:12.4f} {bT[-1]-aT[-1]:12.4f}   '
            f'{bC[0]-aC[0]:13.6f} {bC[-1]-aC[-1]:13.6f}')

    say('\n【表面热流对照（3 h 末）】')
    hflux0 = 25.0 * (TINF - r0['T_end'][-1])
    hflux1 = 25.0 * (TINF - r1['T_end'][-1])
    lat = 2.26e6 * 8e-7 * (r1['C_end'][-1] - CINF)
    say(f'   对流得热  ：忽略 {hflux0:.4f} W/m²   计入 {hflux1:.4f} W/m²')
    say(f'   蒸发耗热  ：0（忽略）             {lat:.4f} W/m²')
    say(f'   ⟹ 潜热/对流 = {lat/max(1e-30, hflux1):.2f} 倍')

    say('\n【结论（论文表述建议）】')
    say(f'   计入蒸发潜热后，表面温度{"下降" if dTR < 0 else "上升"} {abs(dTR):.3f} ℃，'
        f'中心温度{"下降" if dT0 < 0 else "上升"} {abs(dT0):.3f} ℃；')
    say(f'   含水率差异 ≤ {max(abs(dC0), abs(dCR)):.2e} kg/kg（潜热**不改变**水分方程，'
        f'差异仅来自物性耦合的间接影响）。')
    say('   ⟹ 潜热项在本题量级下**不可忽略**，论文"模型评价"须如实给出'
        '该简化带来的偏差方向与幅度（本表即为该对照）。')

    say(f'\n总耗时 {time.time()-t00:.1f}s')
    flush_log()


if __name__ == '__main__':
    main()
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
