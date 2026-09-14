# -*- coding: utf-8 -*-
"""
E1 网格与时间收敛（GCI）
========================
按 Math_2 的 M-1 修订执行（并修正首版的两处方法问题）：
 · **空间收敛**：固定内部时间步（T: Δt_T = 1 s；C: Δt_int = 0.25 s），
   Δr = 1 / 0.5 / 0.25 mm
 · **时间（T）**：固定 Δr = 0.25 mm，Δt_T = 1 / 0.5 / 0.25 / 0.125 s。
   **注（本版）**：温度已改为「时间方向精确推进」⟹ Δt_T 不再影响结果，
   本项由"收敛阶"改为 **步长无关性**核验（四档极差应为机器精度量级）。
 · **时间（C）**：固定 Δr = 0.25 mm，Δt_int = 1 / 0.5 / 0.25 / 0.125 s（仍为一阶后向欧拉）。
解泛函（**统一在 21 个公共输出点上取值**，保证不同网格可比；首版在各自全网格上
取 RMS 导致点集不同、观测阶失真，本版修正）：
   T(0)、T(R)、T 的 RMS；C(0)、C(R)、C 的 RMS

产出：q1_e1_log.txt；30_图表/03_图数据准备/fig_gci_data.csv
约定：本文件不引用、不记载任何资料中的日期。
"""
import os
import io
import sys
import time
import numpy as np
from openpyxl import load_workbook

import q1_core as core
from q1_core import DEF

HERE = os.path.dirname(os.path.abspath(__file__))
# 自适应定位工作区根：向上查找含 10_赛题 的目录
# （兼容两种目录深度：工作区 11_建模/11-3_算法与管线/Q1/code/ 与交付包 09 的 code/）
def _find_root(p, _marker='10_赛题', _max=6):
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, _marker)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.abspath(os.path.join(p, '..', '..', '..'))


ROOT = _find_root(HERE)
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx')
LOG = os.path.join(HERE, 'q1_e1_log.txt')
CSVDIR = os.path.join(ROOT, '30_图表', '03_图数据准备')
CSV = os.path.join(CSVDIR, 'fig_gci_data.csv')
FS = 1.25
NSTEP = 1800
DT = 1.0
L = []


def say(s):
    L.append(str(s))
    print(s)


def load_att1():
    wb = load_workbook(ATT1, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    data = list(ws.iter_rows(values_only=True))[1:]
    return (np.array([float(r[0]) for r in data]),
            np.array([float(r[1]) for r in data]),
            np.array([float(r[2]) for r in data]))


def one_case(N, dr, sub, subT, t, Tinf, Cinf, p, need_T=True, need_C=True):
    """在给定 (dr, dt) 下求解，并把泛函统一取在 21 个公共输出点上"""
    cols = np.arange(0, N + 1, max(1, N // 20))
    res, _, _ = core.run_sim_collect(
        N=N, dr=dr, dt_out=DT, nsteps=NSTEP, p=p,
        Tenv_fn=lambda s: float(np.interp(s, t, Tinf)),
        Cenv_fn=lambda s: float(np.interp(s, t, Cinf)),
        sub=sub, subT=subT, center='fv', surf='fvm', cols=cols,
        solve_T=need_T, solve_C=need_C)
    out = {}
    if need_T:
        Tp = res['T_end'][cols]
        out.update(Tc=float(Tp[0]), Ts=float(Tp[-1]),
                   Trms=float(np.sqrt(np.mean(Tp ** 2))))
    if need_C:
        Cp = res['C_end'][cols]
        out.update(Cc=float(Cp[0]), Cs=float(Cp[-1]),
                   Crms=float(np.sqrt(np.mean(Cp ** 2))))
    return out, res['stats']


def richardson(f1, f2, f3, r, Fs=FS):
    """f1 最细、f3 最粗（r 为均匀加密比）。返回 p、外推值、相对差、GCI%"""
    e21, e32 = f2 - f1, f3 - f2
    if e21 == 0 or e32 == 0:
        return None
    p = abs(np.log(abs(e32 / e21))) / np.log(r)
    f_ext = f1 + (f1 - f2) / (r ** p - 1.0)
    rel = abs((f1 - f2) / f1)
    gci = Fs * rel / (r ** p - 1.0)
    return dict(p=p, ext=f_ext, rel=rel, gci=gci * 100.0, e21=e21, e32=e32)


def order_seq(v):
    """相邻三档观测阶 p = log2((v粗2-v粗1)/(v粗3-v粗2))，v 从粗到细"""
    ps = []
    for i in range(len(v) - 2):
        e1 = v[i] - v[i + 1]
        e2 = v[i + 1] - v[i + 2]
        ps.append(np.log(abs(e2 / e1)) / np.log(2.0) if (e1 and e2) else float('nan'))
    return ps


def main():
    t0 = time.time()
    t, Tinf, Cinf = load_att1()
    p = dict(DEF)
    rows = []

    # ------------------------------------------------------------ 空间收敛
    say('=== E1-a 空间收敛（固定 dtT=1 s, dt_int=0.25 s；dr = 1 / 0.5 / 0.25 mm）===')
    spatial = []
    for (N, dr) in [(20, 1.0e-3), (40, 0.5e-3), (80, 0.25e-3)]:
        f, st = one_case(N, dr, 4, 1, t, Tinf, Cinf, p)
        spatial.append((N, dr, f))
        say('N=%3d  dr=%.2f mm   T(0)=%.8f  T(R)=%.8f  Trms=%.8f | C(R)=%.8f  Crms=%.8f (avg_it=%.2f)'
            % (N, dr * 1e3, f['Tc'], f['Ts'], f['Trms'], f['Cs'], f['Crms'], st['avg_it']))
        rows.append(('spatial', 'dr=%.2f mm' % (dr * 1e3), N, dr * 1e3, f))

    say('')
    for k in ['Tc', 'Ts', 'Trms', 'Cs', 'Crms']:
        f1, f2, f3 = spatial[2][2][k], spatial[1][2][k], spatial[0][2][k]
        g = richardson(f1, f2, f3, 2.0)
        if g:
            say('  [%-4s] p=%.3f  f_ext=%.8f  |e21|/f1=%.3e  GCI=%.4f%%  渐近比值|e32/e21|=%.3f'
                % (k, g['p'], g['ext'], g['rel'], g['gci'], abs(g['e32'] / g['e21'])))

    # ------------------------------------------------- 时间收敛（T 与 C 分开）
    say('')
    say('=== E1-b 时间步**独立性** · T 方程（固定 dr=0.25 mm；dtT = 1/0.5/0.25/0.125 s）===')
    say('  （温度已改为「时间方向精确推进」⟹ dtT = 输出步长，本条由"收敛阶"改为"步长无关性"核验）')
    seqT = []
    for subT in (1, 2, 4, 8):
        f, st = one_case(80, 0.25e-3, 4, subT, t, Tinf, Cinf, p, need_C=False)
        seqT.append((subT, f))
        say('dtT=%.3f s   T(0)=%.10f  T(R)=%.10f  Trms=%.10f' % (DT / subT, f['Tc'], f['Ts'], f['Trms']))
    for k in ['Tc', 'Ts', 'Trms']:
        v = [d[1][k] for d in seqT]
        say('  [%-4s] 四档极差 = %.3e  ⟹ %s'
            % (k, max(v) - min(v), '与步长无关（PASS）' if (max(v) - min(v)) <= 1e-9 else '存在步长依赖（CHECK）'))

    say('')
    say('=== E1-c 时间收敛 · C 方程（固定 dr=0.25 mm, dtT=1 s；dt_int = 1/0.5/0.25/0.125 s）===')
    seqC = []
    for sub in (1, 2, 4, 8):
        f, st = one_case(80, 0.25e-3, sub, 1, t, Tinf, Cinf, p, need_T=False)
        seqC.append((sub, f))
        say('dt_int=%.3f s   C(0)=%.10f  C(R)=%.10f  Crms=%.10f  (avg_it=%.2f)'
            % (DT / sub, f['Cc'], f['Cs'], f['Crms'], st['avg_it']))
    for k in ['Cc', 'Cs', 'Crms']:
        v = [d[1][k] for d in seqC][::-1]
        say('  [%-4s] 观测阶序列(粗→细) = %s' % (k, ' '.join('%.3f' % x for x in order_seq(v))))

    # ------------------------------------------------------------ CSV
    os.makedirs(CSVDIR, exist_ok=True)
    keys = ['Tc', 'Ts', 'Trms', 'Cc', 'Cs', 'Crms']
    with io.open(CSV, 'w', encoding='utf-8') as f:
        f.write('group,case,idx,delta,' + ','.join(keys) + '\n')
        for grp, lbl, idx, delta, f_ in rows:
            f.write('%s,%s,%d,%.6g,%s\n' % (grp, lbl, idx, delta,
                                            ','.join('%.8f' % f_.get(k, float('nan')) for k in keys)))
        for subT, f_ in seqT:
            f.write('temporal_T,dtT_s,%d,%.6g,%s\n' % (subT, DT / subT,
                                                       ','.join('%.8f' % f_.get(k, float('nan')) for k in keys)))
        for sub, f_ in seqC:
            f.write('temporal_C,dtint_s,%d,%.6g,%s\n' % (sub, DT / sub,
                                                         ','.join('%.8f' % f_.get(k, float('nan')) for k in keys)))
    say('')
    say('CSV written: %s' % CSV)
    say('E1 elapsed=%.1fs' % (time.time() - t0))
    with io.open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
