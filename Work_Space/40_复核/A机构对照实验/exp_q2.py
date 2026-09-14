# -*- coding: utf-8 -*-
"""
Q2（0–3 h 变物性双向耦合）分歧点裁决实验
==========================================
对照：机构《高质量成品论文》（显式 FV，Δr=1 mm=20 等分，Δt=1 s，算术平均，准稳态 Robin）
      机构《GT05 老哥》（有限体积 N=200=0.1 mm，隐式后向欧拉，算术平均，指数拟合边界）
      机构《GT02 MATLAB》（N=20=1 mm，隐式，调和平均，Picard 仅 3 次 + 松弛 0.85）
      我方（元体平衡 + IMEX 全隐式 + 半格表面，Δr=0.25 mm，内部步长 1/32 s，调和平均，线性插值）
输出：exp_q2_report.txt
"""
import io
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import (explicit_fv, bdf_mol, make_env, T1, TAIR, CAIR, find_root)

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
import q2_core as our_q2                     # noqa: E402

OUT = os.path.join(HERE, 'exp_q2_report.txt')
LINES = []


def say(s=''):
    print(s, flush=True)
    LINES.append(str(s))


SNAP_H = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
SNAP = tuple(int(h * 3600) for h in SNAP_H)

INS_T = np.array([
    [32.3096, 32.5050, 33.0962, 34.1040, 35.5751],
    [40.5415, 40.7127, 41.2167, 42.0294, 43.1480],
    [45.9580, 46.0444, 46.2979, 46.7024, 47.2240],
    [48.5096, 48.5464, 48.6536, 48.8238, 49.0467],
    [49.4931, 49.5047, 49.5371, 49.5854, 49.6864],
    [49.8600, 49.8659, 49.8852, 49.9204, 49.9771]])
INS_C = np.array([
    [2.5498, 2.5481, 2.5181, 2.2929, 1.5902],
    [2.5201, 2.4856, 2.3384, 1.9917, 1.4371],
    [2.3701, 2.3076, 2.1117, 1.7755, 1.3202],
    [2.1499, 2.0869, 1.9005, 1.6014, 1.2050],
    [1.9345, 1.8782, 1.7130, 1.4479, 1.0902],
    [1.7439, 1.6941, 1.5473, 1.3092, 0.9811]])
GT05_T = np.array([
    [32.1752, 32.3720, 32.9676, 33.9774, 35.4316],
    [40.3794, 40.5498, 41.0545, 41.8739, 42.9827],
    [45.8235, 45.9126, 46.1740, 46.5919, 47.1450],
    [48.4317, 48.4687, 48.5767, 48.7485, 48.9740],
    [49.4773, 49.4906, 49.5295, 49.5911, 49.6718],
    [49.8481, 49.8524, 49.8650, 49.8850, 49.9112]])
GT05_C = np.array([
    [2.5499, 2.5489, 2.5256, 2.3258, 1.6489],
    [2.5257, 2.4947, 2.3578, 2.0231, 1.4711],
    [2.3861, 2.3258, 2.1346, 1.8021, 1.3474],
    [2.1711, 2.1087, 1.9238, 1.6260, 1.2309],
    [1.9568, 1.9007, 1.7361, 1.4720, 1.1168],
    [1.7663, 1.7166, 1.5703, 1.3333, 1.0080]])
MINE = dict(
    T=np.array([[32.1893, None, None, None, 35.4131],
                [40.3816, None, None, None, 42.9977],
                [45.8467, None, None, None, 47.1401],
                [48.4502, None, None, None, 49.0033],
                [49.4670, None, None, None, 49.6609],
                [49.8495, None, None, None, 49.9664]]),
    C=np.array([[2.549932, None, None, None, 1.648607],
                [2.525686, None, None, None, 1.471056],
                [2.386030, None, None, None, 1.347541],
                [2.170851, None, None, None, 1.231073],
                [1.956656, None, None, None, 1.116631],
                [1.766196, None, None, None, 1.008111]]))


def table(res, dt_out, key='C'):
    idx = [int(round(x / res['dr'])) for x in (0.0, 0.005, 0.01, 0.015, 0.02)]
    arr = res[key]
    return np.array([arr[int(round(s / dt_out))][idx] for s in SNAP])


def show(name, tab, ref=None):
    say(f'--- {name} ---')
    say('  t/h   ' + '  '.join(f'{k:>9s}' for k in ['0 cm', '0.5', '1.0', '1.5', '2.0']))
    for i, h in enumerate(SNAP_H):
        extra = ''
        if ref is not None:
            extra = f'   max|Δ|={np.abs(tab[i]-ref[i]).max():.4f}'
        say(f'{h:6.1f}  ' + '  '.join(f'{v:9.4f}' for v in tab[i]) + extra)
    say('')


def main():
    t0 = time.time()
    say('=' * 104)
    say('A 题 Q2（0–3 h 变物性双向耦合）分歧点裁决实验')
    say('=' * 104)
    Tex, Cex = make_env('pchip')
    Tle, Cle = make_env('linear')
    Tef, Cef = make_env('expfit')
    T_EXT, C_EXT = 50.00, 0.04999
    say(f'附件1 环境：1800 s={np.interp(1800,T1,TAIR):.4f}℃ / 3600 s={np.interp(3600,T1,TAIR):.4f}℃ / '
        f'10800 s={np.interp(10800,T1,TAIR):.4f}℃（原始值）；'
        f'GT05 指数拟合 10800 s={float(Tef(10800)):.4f}℃ ⟹ 与原始数据差 '
        f'{float(Tef(10800))-np.interp(10800,T1,TAIR):+.4f} ℃')
    say('')

    # ================================================= A 复刻机构显式格式
    say('#' * 104)
    say('# 实验 A：复刻机构《高质量成品论文》Q2 显式格式（N=20，Δr=1 mm，Δt=1 s，算术平均，准稳态 Robin）')
    say('#' * 104)
    rA = explicit_fv(20, 0.02, 1.0, 10800, 1.0, Tex, Cex, prop='q2',
                     surf='quasi', ifmode='arith', quasi_use_new=True)
    show('A1 机构格式 表3 温度', table(rA, 1.0, 'T'), INS_T)
    show('A1 机构格式 表4 水分浓度', table(rA, 1.0, 'C'), INS_C)

    # ================================================= B 网格细分
    say('#' * 104)
    say('# 实验 B：保持机构口径不变，仅加密网格（Δt 按显式稳定限同比缩小）')
    say('#' * 104)
    say(f'{"N":>5} {"Δr/mm":>8} {"Δt/s":>7} {"C(0)":>9} {"C(1.0)":>9} {"C(R)":>9} {"T(0)":>9} {"T(R)":>9}')
    for N, dt in [(20, 1.0), (40, 0.25), (80, 0.05), (160, 0.02)]:
        r = explicit_fv(N, 0.02, dt, 10800, 1.0, Tex, Cex, prop='q2',
                        surf='quasi', ifmode='arith', quasi_use_new=True)
        i10 = int(round(0.01 / r['dr']))
        say(f'{N:5d} {0.02/N*1e3:8.4f} {dt:7.4f} {r["C"][-1][0]:9.4f} {r["C"][-1][i10]:9.4f} '
            f'{r["C"][-1][-1]:9.4f} {r["T"][-1][0]:9.4f} {r["T"][-1][-1]:9.4f}')
    say('')

    # ================================================= C 逐项隔离（N=20）
    say('#' * 104)
    say('# 实验 C：在 N=20（机构同一网格）下逐项替换离散口径（3 h 值）')
    say('#' * 104)
    cases = [
        ('机构原样 准稳态Robin+算术平均+PCHIP', dict(surf='quasi', ifmode='arith'), Tex, Cex),
        ('仅改表面 → 半格元体(含储能)', dict(surf='halfcell', ifmode='arith'), Tex, Cex),
        ('仅改界面 → 调和平均', dict(surf='quasi', ifmode='harm'), Tex, Cex),
        ('半格+调和平均+线性', dict(surf='halfcell', ifmode='harm'), Tle, Cle),
        ('半格+调和平均+指数拟合边界', dict(surf='halfcell', ifmode='harm'), Tef, Cef),
    ]
    say(f'{"口径":<38s} {"C(0)":>8} {"C(1.0)":>8} {"C(R)":>8} {"T(0)":>9} {"T(R)":>9}')
    for name, kw, Te, Ce in cases:
        r = explicit_fv(20, 0.02, 1.0, 10800, 1.0, Te, Ce, prop='q2', **kw)
        i10 = 10
        say(f'{name:<38s} {r["C"][-1][0]:8.4f} {r["C"][-1][i10]:8.4f} {r["C"][-1][20]:8.4f} '
            f'{r["T"][-1][0]:9.4f} {r["T"][-1][20]:9.4f}')
    say('')

    # ================================================= D 我方核（只读调用）
    say('#' * 104)
    say('# 实验 D：只读调用我方 Q2 求解核 q2_core')
    say('#' * 104)

    def Tenv(t):
        return float(np.interp(t, T1, TAIR)) if t <= T1[-1] else T_EXT

    def Cenv(t):
        return float(np.interp(t, T1, CAIR)) if t <= T1[-1] else C_EXT

    for N, dr, nsub in [(20, 1e-3, 32), (80, 2.5e-4, 32)]:
        t1 = time.time()
        res, tT, tC = our_q2.run_q2(N=N, dr=dr, dt_out=1.0, nsteps=10800,
                                   Tenv_fn=Tenv, Cenv_fn=Cenv, n_sub=nsub,
                                   mode='coupled', cols=np.arange(0, N + 1, N // 20),
                                   snap_at=set(SNAP))
        i10 = int(round(0.01 / dr))
        say(f'q2_core N={N:4d} Δr={dr*1e3:.4f} mm  耗时 {time.time()-t1:6.1f}s  '
            f'C(0)={res["C_end"][0]:.6f} C(1.0)={res["C_end"][i10]:.6f} C(R)={res["C_end"][-1]:.6f}  '
            f'T(0)={res["T_end"][0]:.4f} T(R)={res["T_end"][-1]:.4f}')
        if N == 80:
            idd = [0, 20, 40, 60, 80]
            tabT = np.array([[res['T_snap'][s][i] for i in idd] for s in SNAP])
            tabC = np.array([[res['C_snap'][s][i] for i in idd] for s in SNAP])
            show('q2_core N=80 表3 温度（复核我方已发布值）', tabT)
            show('q2_core N=80 表4 水分浓度（复核我方已发布值）', tabC)
    say('')

    # ================================================= E 第三方 BDF 参考
    say('#' * 104)
    say('# 实验 E：第三方路径参考解（MOL + scipy BDF，调和平均，线性插值）')
    say('#' * 104)
    for N in (80,):
        t1 = time.time()
        r = bdf_mol(N, 0.02, 10800.0, Tle, Cle, prop='q2', ifmode='harm',
                    dt_samp=60.0, rtol=1e-8, atol=1e-10)
        i10 = int(round(0.01 / r['dr']))
        say(f'BDF N={N:4d} Δr={0.02/N*1e3:.4f} mm nfev={r["nfev"]:6d} 耗时 {time.time()-t1:6.1f}s '
            f'C(0)={r["C"][-1][0]:.6f} C(1.0)={r["C"][-1][i10]:.6f} C(R)={r["C"][-1][-1]:.6f}  '
            f'T(0)={r["T"][-1][0]:.4f} T(R)={r["T"][-1][-1]:.4f}')
        show('BDF 参考 N=80 表4 水分浓度（与机构论文逐格比对）', table(r, 60.0, 'C'), INS_C)
        show('BDF 参考 N=80 表3 温度', table(r, 60.0, 'T'), INS_T)
    say('')

    # ================================================= F 欠收敛 Picard（GT02 口径风险）
    say('#' * 104)
    say('# 实验 F：内层非线性迭代"跑不满"的后果（对照机构《GT02》Picard=3 次 + 松弛 0.85）')
    say('#' * 104)
    say(f'{"设置":<44s} {"C(0)@3h":>11} {"C(R)@3h":>11} {"T(0)@3h":>10} {"T(R)@3h":>10}')
    ref = None
    for tag, nsub, maxit, om in [('参考：32 子步 / maxit=30 / ω=0.7', 32, 30, 0.7),
                                 ('GT02 型：1 子步(整步) / maxit=3 / ω=0.85', 1, 3, 0.85),
                                 ('32 子步 / maxit=3 / ω=0.85', 32, 3, 0.85)]:
        res, _, _ = our_q2.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=10800,
                                  Tenv_fn=Tenv, Cenv_fn=Cenv, n_sub=nsub,
                                  omega=om, maxit=maxit, mode='coupled')
        v = (res['C_end'][0], res['C_end'][-1], res['T_end'][0], res['T_end'][-1])
        if ref is None:
            ref = v
        d = f'   (ΔC0={v[0]-ref[0]:+.5f}, ΔCR={v[1]-ref[1]:+.5f})' if ref is not v else ''
        say(f'{tag:<44s} {v[0]:11.6f} {v[1]:11.6f} {v[2]:10.4f} {v[3]:10.4f}{d}')
    say('')

    # ================================================= G 边界平滑影响
    say('#' * 104)
    say('# 实验 G：边界数据"平滑/拟合"对 Q2 结果的影响（我方网格 N=80）')
    say('#' * 104)
    say(f'{"边界口径":<30s} {"C(0)@3h":>11} {"C(R)@3h":>11} {"T(0)@3h":>10} {"T(R)@3h":>10}')
    for tag, Te, Ce in [('原始数据线性插值（我方）', Tle, Cle),
                        ('PCHIP（机构论文）', Tex, Cex),
                        ('指数饱和拟合（GT05）', Tef, Cef)]:
        res, _, _ = our_q2.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=10800,
                                  Tenv_fn=Te, Cenv_fn=Ce, n_sub=32, mode='coupled')
        say(f'{tag:<30s} {res["C_end"][0]:11.6f} {res["C_end"][-1]:11.6f} '
            f'{res["T_end"][0]:10.4f} {res["T_end"][-1]:10.4f}')
    say('')

    say(f'总耗时 {time.time()-t0:.1f} s')
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINES) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
