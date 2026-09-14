# -*- coding: utf-8 -*-
"""
Q1（0–1800 s 预热平衡阶段）分歧点裁决实验
==========================================
对照：机构《2026国赛A题高质量成品论文！》（显式有限差分/FV，Δr=1 mm=20 等分，Δt=1 s）
      机构《GT05 老哥》（有限体积 N=200=Δr 0.1 mm，隐式，指数拟合边界）
      我方（元体平衡 + 全隐式 + 半格表面控制体，Δr=0.25 mm，内部步长 1/32 s）
      第三方参考（MOL + scipy BDF 自适应步长）
输出：exp_q1_report.txt
"""
import io
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import (explicit_fv, implicit_fv, bdf_mol, make_env,
                        semi_infinite_C, T1, TAIR, CAIR, find_root)

# 只读导入我方 Q1 求解核（不修改任何文件）
ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
import q1_core as our_core          # noqa: E402

OUT = os.path.join(HERE, 'exp_q1_report.txt')
LINES = []


def say(s=''):
    print(s, flush=True)
    LINES.append(str(s))


SNAP = (100, 300, 600, 900, 1200, 1500, 1800)

INS_PAPER_T = np.array([
    [28.0001, 28.0004, 28.0047, 28.0373, 28.2027],
    [28.0453, 28.0698, 28.1638, 28.3922, 28.8987],
    [28.4783, 28.5637, 28.8397, 29.3651, 30.2325],
    [29.3717, 29.5084, 29.9334, 30.6853, 31.8117],
    [30.6090, 30.7781, 31.2970, 32.1975, 33.5268],
    [32.0775, 32.2703, 32.8546, 33.8415, 35.2178],
    [33.6669, 33.8643, 34.4589, 35.4619, 36.8923]])
INS_PAPER_C = np.array([
    [2.5500, 2.5500, 2.5500, 2.5500, 2.0483],
    [2.5500, 2.5500, 2.5500, 2.5465, 1.8857],
    [2.5500, 2.5500, 2.5499, 2.5236, 1.7307],
    [2.5500, 2.5500, 2.5491, 2.4844, 1.6189],
    [2.5500, 2.5500, 2.5465, 2.4377, 1.5299],
    [2.5500, 2.5498, 2.5413, 2.3887, 1.4552],
    [2.5500, 2.5494, 2.5332, 2.3398, 1.3907]])
GT05_C = np.array([
    [2.55, 2.55, 2.55, 2.55, 2.2477],
    [2.55, 2.55, 2.55, 2.5492, 2.0511],
    [2.55, 2.55, 2.55, 2.5352, 1.8771],
    [2.55, 2.55, 2.5497, 2.5045, 1.7548],
    [2.55, 2.55, 2.5482, 2.4645, 1.6586],
    [2.55, 2.5499, 2.5445, 2.4206, 1.5788],
    [2.55, 2.5497, 2.5383, 2.3755, 1.5104]])
MINE_T = np.array([
    [28.0001, 28.0004, 28.0041, 28.0327, 28.1800],
    [28.0408, 28.0635, 28.1514, 28.3681, 28.8488],
    [28.4534, 28.5361, 28.8040, 29.3159, 30.1652],
    [29.3244, 29.4583, 29.8755, 30.6162, 31.7304],
    [30.5428, 30.7098, 31.2224, 32.1126, 33.4276],
    [31.9958, 32.1868, 32.7661, 33.7463, 35.1203],
    [33.5754, 33.7720, 34.3642, 35.3621, 36.7856]])
MINE_C = np.array([
    [2.5500, 2.5500, 2.5500, 2.5500, 2.2490],
    [2.5500, 2.5500, 2.5500, 2.5492, 2.0517],
    [2.5500, 2.5500, 2.5500, 2.5352, 1.8774],
    [2.5500, 2.5500, 2.5497, 2.5045, 1.7550],
    [2.5500, 2.5500, 2.5482, 2.4646, 1.6588],
    [2.5500, 2.5499, 2.5445, 2.4207, 1.5789],
    [2.5500, 2.5497, 2.5383, 2.3755, 1.5103]])


def table(res, dt_out, key='C'):
    idx = [int(round(x / res['dr'])) for x in (0.0, 0.005, 0.01, 0.015, 0.02)]
    arr = res[key]
    return np.array([arr[int(round(s / dt_out))][idx] for s in SNAP])


def show(name, tab, ref=None, tag=''):
    say(f'--- {name} {tag}---')
    say('   t/s  ' + '  '.join(f'{k:>9s}' for k in ['0 cm', '0.5', '1.0', '1.5', '2.0']))
    for i, s in enumerate(SNAP):
        extra = ''
        if ref is not None:
            extra = f'   max|Δ|={np.abs(tab[i]-ref[i]).max():.4f}'
        say(f'{s:6d}  ' + '  '.join(f'{v:9.4f}' for v in tab[i]) + extra)
    say('')


def main():
    t0 = time.time()
    say('=' * 104)
    say('A 题 Q1（预热平衡 0–1800 s）分歧点裁决实验')
    say('=' * 104)
    say(f'附件1 点数={len(T1)}  时间 {T1[0]:.0f}–{T1[-1]:.0f} s；'
        f'1800 s 环境 = {np.interp(1800,T1,TAIR):.4f} ℃ / {np.interp(1800,T1,CAIR):.5f} kg/kg；'
        f'全时段环境温度最大值 = {TAIR.max():.4f} ℃')
    say('')

    Tex, Cex = make_env('pchip')
    Tle, Cle = make_env('linear')

    # ================================================= A 复刻机构显式格式
    say('#' * 104)
    say('# 实验 A：复刻机构《高质量成品论文》显式格式（N=20，Δr=1 mm，Δt=1 s，算术平均，准稳态 Robin）')
    say('#' * 104)
    resA1 = explicit_fv(20, 0.02, 1.0, 1800, 1.0, Tex, Cex, prop='q1',
                        surf='quasi', ifmode='arith', quasi_use_new=True)
    resA2 = explicit_fv(20, 0.02, 1.0, 1800, 1.0, Tex, Cex, prop='q1',
                        surf='quasi', ifmode='arith', quasi_use_new=False)
    show('A1 机构格式 表2 水分浓度', table(resA1, 1.0, 'C'), INS_PAPER_C)
    show('A1 机构格式 表1 温度', table(resA1, 1.0, 'T'), INS_PAPER_T)
    show('A2 机构格式(表面取 n 层) 表2 水分浓度', table(resA2, 1.0, 'C'), INS_PAPER_C)

    # ================================================= B 网格细分
    say('#' * 104)
    say('# 实验 B：保持机构"准稳态 Robin + 算术平均"口径不变，仅加密网格（Δt 按显式稳定限同比缩小）')
    say('#' * 104)
    say(f'{"N":>5} {"Δr/mm":>8} {"Δt/s":>7} {"C(0)":>9} {"C(1.5)":>9} {"C(R)":>9} {"T(R)":>9}')
    for N, dt in [(20, 1.0), (40, 0.25), (80, 0.05), (160, 0.02), (320, 0.005)]:
        r = explicit_fv(N, 0.02, dt, 1800, 1.0, Tex, Cex, prop='q1',
                        surf='quasi', ifmode='arith', quasi_use_new=True)
        idx15 = int(round(0.015 / r['dr']))
        say(f'{N:5d} {0.02/N*1e3:8.4f} {dt:7.4f} {r["C"][-1][0]:9.4f} {r["C"][-1][idx15]:9.4f} '
            f'{r["C"][-1][-1]:9.4f} {r["T"][-1][-1]:9.4f}')
    say('')

    # ================================================= C 逐项隔离
    say('#' * 104)
    say('# 实验 C：在 N=20（机构同一网格）下逐项替换离散口径，定位差异来源（1800 s 值）')
    say('#' * 104)
    cases = [
        ('机构原样 准稳态Robin+算术平均+PCHIP', dict(surf='quasi', ifmode='arith'), Tex, Cex),
        ('仅改表面 → 半格元体(含储能)', dict(surf='halfcell', ifmode='arith'), Tex, Cex),
        ('仅改界面 → 调和平均', dict(surf='quasi', ifmode='harm'), Tex, Cex),
        ('仅改界面 → 积分平均', dict(surf='quasi', ifmode='integral'), Tex, Cex),
        ('仅改边界插值 → 线性', dict(surf='quasi', ifmode='arith'), Tle, Cle),
        ('仅改边界插值 → 指数拟合(GT05)', dict(surf='quasi', ifmode='arith'),
         make_env('expfit')[0], make_env('expfit')[1]),
        ('半格+调和平均+线性', dict(surf='halfcell', ifmode='harm'), Tle, Cle),
        ('半格+积分平均+线性(≈我方口径)', dict(surf='halfcell', ifmode='integral'), Tle, Cle),
    ]
    say(f'{"口径":<40s} {"C(0)":>8} {"C(1.0)":>8} {"C(1.5)":>8} {"C(2.0)":>8} {"T(0)":>9} {"T(R)":>9}')
    for name, kw, Te, Ce in cases:
        r = explicit_fv(20, 0.02, 1.0, 1800, 1.0, Te, Ce, prop='q1', **kw)
        say(f'{name:<40s} {r["C"][-1][0]:8.4f} {r["C"][-1][10]:8.4f} {r["C"][-1][15]:8.4f} '
            f'{r["C"][-1][20]:8.4f} {r["T"][-1][0]:9.4f} {r["T"][-1][20]:9.4f}')
    say('')

    # ================================================= D 我方求解核（只读调用）
    say('#' * 104)
    say('# 实验 D：直接调用我方 Q1 求解核 q1_core（只读导入，不改动其文件）')
    say('#' * 104)
    p = dict(our_core.DEF)
    Tenv = lambda s: float(np.interp(s, T1, TAIR))
    Cenv = lambda s: float(np.interp(s, T1, CAIR))
    our_res = {}
    for N in (20, 40, 80, 160):
        dr = 0.02 / N
        t1 = time.time()
        r = our_core.run_sim(N=N, dr=dr, dt_out=1.0, nsteps=1800, p=p,
                             Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                             center='fv', surf='fvm', solve_C=True, solve_T=True,
                             snap_at=set(SNAP))
        our_res[N] = r
        idx15 = int(round(0.015 / dr))
        say(f'q1_core N={N:4d} Δr={dr*1e3:.4f} mm  耗时 {time.time()-t1:6.1f}s  '
            f'C(0)={r["C_end"][0]:.6f}  C(1.5)={r["C_end"][idx15]:.6f}  '
            f'C(R)={r["C_end"][-1]:.6f}  T(0)={r["T_end"][0]:.4f}  T(R)={r["T_end"][-1]:.4f}')
    idd = [0, 20, 40, 60, 80]
    tabA = np.array([[our_res[80]['C_snap'][s][i] for i in idd] for s in SNAP])
    tabT = np.array([[our_res[80]['T_snap'][s][i] for i in idd] for s in SNAP])
    show('q1_core N=80 表2 水分浓度（复核我方已发布值）', tabA, MINE_C)
    show('q1_core N=80 表1 温度（复核我方已发布值）', tabT, MINE_T)
    say('')

    # ================================================= E 第三方 BDF 参考
    say('#' * 104)
    say('# 实验 E：第三方路径参考解（MOL + scipy BDF 自适应变步长，与上面两种算法完全不同）')
    say('#' * 104)
    for N in (80, 160):
        t1 = time.time()
        r = bdf_mol(N, 0.02, 1800.0, Tle, Cle, prop='q1', ifmode='integral',
                    dt_samp=1.0, rtol=1e-10, atol=1e-12)
        idx15 = int(round(0.015 / r['dr']))
        say(f'BDF N={N:4d} Δr={0.02/N*1e3:.4f} mm  nfev={r["nfev"]:6d}  耗时 {time.time()-t1:6.1f}s  '
            f'status={r["status"]}  C(0)={r["C"][-1][0]:.6f}  C(1.5)={r["C"][-1][idx15]:.6f}  '
            f'C(R)={r["C"][-1][-1]:.6f}  T(0)={r["T"][-1][0]:.4f}  T(R)={r["T"][-1][-1]:.4f}')
        if N == 160:
            show('BDF 参考 N=160 表2 水分浓度', table(r, 1.0, 'C'), MINE_C)
            show('BDF 参考 N=160 表1 温度', table(r, 1.0, 'T'), MINE_T)
    say('')

    # ================================================= F 解析基准
    say('#' * 104)
    say('# 实验 F：早期时刻半无限介质 Robin 解析解（erfc 精确式）基准')
    say('#' * 104)
    D0 = 7e-9 * np.exp(-0.89 / 2.55)
    say(f'D(C0=2.55)={D0:.5e} m²/s；渗透深度 √(Dt) 在 100 s / 600 s / 1800 s 分别约 '
        f'{np.sqrt(D0*100)*1e3:.2f} / {np.sqrt(D0*600)*1e3:.2f} / {np.sqrt(D0*1800)*1e3:.2f} mm（半径 20 mm）')
    say('  解析估计按 ΔC 区间内的 D 平均（分段修正）计算，故与数值解应高度一致。')
    say(f'{"t/s":>6} {"C_air":>8} {"解析 C(0,t)":>12} {"我方 N=80":>10} {"机构论文":>9} {"GT05":>9}')
    for i, s in enumerate(SNAP):
        ca = float(np.interp(s, T1, CAIR))
        cs = float(semi_infinite_C(np.array([float(s)]), D0, 8e-7, 2.55, ca)[0])
        # D 修正：用解析表面值与初值的平均 C 重算 D
        Cm = 0.5 * (cs + 2.55)
        Dm = 7e-9 * np.exp(-0.89 / Cm)
        cs2 = float(semi_infinite_C(np.array([float(s)]), Dm, 8e-7, 2.55, ca)[0])
        minev = float(np.interp(0.02, np.arange(81) * 0.00025, our_res[80]['C_snap'][s]))
        say(f'{s:6d} {ca:8.5f} {cs2:12.4f} {minev:10.4f} {INS_PAPER_C[i][4]:9.4f} {GT05_C[i][4]:9.4f}')
    say('')

    # ================================================= G 物理上界
    say('#' * 104)
    say('# 实验 G：物理上界 / 守恒 / 单调性检验（对机构各文档公布值）')
    say('#' * 104)
    say(f'· 1800 s 烘房温度 = {np.interp(1800,T1,TAIR):.4f} ℃（全时段最大 {TAIR.max():.4f} ℃）⟹ 药材任意位置温度必须 ≤ 同刻烘房温度（第三类边界 + 无内热源）')
    say('· 干基含水率必须 ≤ C0 = 2.55 且沿时间逐点不增')
    say('')
    say(f'《GT04》表1 1800 s：中心 47.3203 ℃、表面 48.5448 ℃ ⟹ 超同刻烘房温度 '
        f'{47.3203-np.interp(1800,T1,TAIR):.4f} / {48.5448-np.interp(1800,T1,TAIR):.4f} ℃ ⟹ 违反极值原理')
    say('《GT04》表2：900 s 中心 2.5512、1200 s 中心 2.5606 ⟹ 超初值 2.55 ⟹ 违反质量守恒')
    say('《GT03》1800 s 表面含水率 2.5030（30 min 内仅失水 1.8%）⟹ 与传质 Biot 数 3.24 量级严重不符')
    say('')

    say(f'总耗时 {time.time()-t0:.1f} s')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINES) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
