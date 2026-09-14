# -*- coding: utf-8 -*-
"""
我方交付物自查：论文表格（求解记录登记值）／交付文件 result1.xlsx、result2.xlsx／现码复算，
三者是否逐格一致。只读，不写入 20_交付包 任何文件。
"""
import io
import os
import sys
import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exp_common import T1, TAIR, CAIR, find_root

ROOT = find_root()
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q1', 'code'))
sys.path.insert(0, os.path.join(ROOT, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
import q1_core as C1                       # noqa: E402
import q2_core_c as C2                     # noqa: E402  ← M6 口径核（交付文件同源）

RES = os.path.join(ROOT, '20_交付包', '09_代码与复现', 'results')
OUT = os.path.join(HERE, 'exp_selfcheck_report.txt')
L = []


def say(s=''):
    print(s, flush=True)
    L.append(str(s))


def read_file(fp, sheet, rows, cols):
    wb = load_workbook(fp, read_only=True, data_only=True)
    ws = wb[sheet]
    data = list(ws.iter_rows(values_only=True))
    wb.close()
    return np.array([[float(data[r][1 + c]) for c in cols] for r in rows])


def cmp(name, a, b):
    d = np.abs(a - b)
    bad = np.argwhere(d > 1e-9)
    say(f'  {name}: 最大差 {d.max():.6f}，不一致格数 {len(bad)}/{d.size}')
    for i, j in bad:
        say(f'      第{i}行 第{j}列： {a[i, j]:.4f}  vs  {b[i, j]:.4f}')
    return len(bad)


def main():
    cols = [0, 5, 10, 15, 20]          # 交付文件里的列号：0.0/0.5/1.0/1.5/2.0 cm
    nidx = [0, 20, 40, 60, 80]         # N=80（Δr=0.25 mm）下同位置的节点号
    say('=' * 96)
    say('我方交付物自查（Q1 / Q2）')
    say('=' * 96)

    # ---------------- Q1 ----------------
    rec_t1 = [100, 300, 600, 900, 1200, 1500, 1800]
    # 《A_Q1求解记录》§4.2 表1（温度）登记值 —— 已于【C-03 门禁】更正：
    # 原表为**陈旧快照**（其值实为早期"显式 FTCS 互验"数，16 格比交付文件高 1e-4），
    # 现与 `result1.xlsx` 与《求解记录》§4.2 逐格对齐（证据：台账 05-G2）。
    MINE_T = np.array([[28.0001, 28.0003, 28.0041, 28.0327, 28.1800],
                       [28.0408, 28.0635, 28.1514, 28.3680, 28.8487],
                       [28.4534, 28.5360, 28.8039, 29.3159, 30.1652],
                       [29.3243, 29.4583, 29.8754, 30.6161, 31.7304],
                       [30.5427, 30.7098, 31.2223, 32.1125, 33.4276],
                       [31.9957, 32.1867, 32.7660, 33.7463, 35.1203],
                       [33.5753, 33.7720, 34.3642, 35.3621, 36.7855]])
    MINE_C = np.array([[2.5500, 2.5500, 2.5500, 2.5500, 2.2490],
                       [2.5500, 2.5500, 2.5500, 2.5492, 2.0517],
                       [2.5500, 2.5500, 2.5500, 2.5352, 1.8774],
                       [2.5500, 2.5500, 2.5497, 2.5045, 1.7550],
                       [2.5500, 2.5500, 2.5482, 2.4646, 1.6588],
                       [2.5500, 2.5499, 2.5445, 2.4206, 1.5789],
                       [2.5500, 2.5497, 2.5383, 2.3755, 1.5104]])
    p = dict(C1.DEF)
    Tenv = lambda s: float(np.interp(s, T1, TAIR))
    Cenv = lambda s: float(np.interp(s, T1, CAIR))
    r1 = C1.run_sim(N=80, dr=0.00025, dt_out=1.0, nsteps=1800, p=p,
                    Tenv_fn=Tenv, Cenv_fn=Cenv, sub=10, subT=32,
                    center='fv', surf='fvm', snap_at=set(rec_t1))
    new_T1 = np.array([[round(float(r1['T_snap'][s][i]), 4) for i in nidx] for s in rec_t1])
    new_C1 = np.array([[round(float(r1['C_snap'][s][i]), 4) for i in nidx] for s in rec_t1])
    file_T1 = read_file(os.path.join(RES, 'result1.xlsx'), '温度', rec_t1, cols)
    file_C1 = read_file(os.path.join(RES, 'result1.xlsx'), '水分浓度', rec_t1, cols)

    say('[Q1] 交付文件 result1.xlsx  vs  现码复算（q1_core，N=80/Δr=0.25mm，sub=10, subT=32）')
    n1 = cmp('温度', file_T1, new_T1)
    n2 = cmp('水分浓度', file_C1, new_C1)
    say('[Q1] 交付文件 result1.xlsx  vs  《A_Q1求解记录》登记表值')
    n3 = cmp('温度', file_T1, MINE_T)
    n4 = cmp('水分浓度', file_C1, MINE_C)
    say('')

    # ---------------- Q2 ----------------
    rec_t2 = [1800, 3600, 5400, 7200, 9000, 10800]
    # 《A_Q2求解记录》§五 登记的中心/表面值（原文照录，仅 T(0)/T(R)/C(0)/C(R) 四列）
    REC_T2 = np.array([[32.1893, 35.4131],
                       [40.3816, 42.9977],
                       [45.8468, 47.1401],
                       [48.4502, 49.0033],
                       [49.4670, 49.6609],
                       [49.8495, 49.9664]])
    REC_C2 = np.array([[2.5499, 1.6486],
                       [2.5257, 1.4711],
                       [2.3860, 1.3475],
                       [2.1708, 1.2311],
                       [1.9567, 1.1166],
                       [1.7662, 1.0081]])
    T_EXT, C_EXT = 50.00, 0.04999

    def Tenv2(t):
        return float(np.interp(t, T1, TAIR)) if t <= T1[-1] else T_EXT

    def Cenv2(t):
        return float(np.interp(t, T1, CAIR)) if t <= T1[-1] else C_EXT

    res2, _, _ = C2.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=10800,
                           Tenv_fn=Tenv2, Cenv_fn=Cenv2, n_sub=32,
                           mode='coupled', snap_at=set(rec_t2))
    new_T2 = np.array([[round(float(res2['T_snap'][s][i]), 4) for i in nidx] for s in rec_t2])
    new_C2 = np.array([[round(float(res2['C_snap'][s][i]), 4) for i in nidx] for s in rec_t2])
    file_T2 = read_file(os.path.join(RES, 'result2.xlsx'), '温度', rec_t2, cols)
    file_C2 = read_file(os.path.join(RES, 'result2.xlsx'), '水分浓度', rec_t2, cols)

    say('[Q2] 交付文件 result2.xlsx  vs  现码复算（q2_core，N=80，n_sub=32, maxit=30, ω=0.7）')
    n5 = cmp('温度', file_T2, new_T2)
    n6 = cmp('水分浓度', file_C2, new_C2)
    say('[Q2] 交付文件 result2.xlsx（仅 0 cm / 2.0 cm 两列）  vs  《A_Q2求解记录》§五 登记值')
    n7 = cmp('温度', file_T2[:, [0, 4]], REC_T2)
    n8 = cmp('水分浓度', file_C2[:, [0, 4]], REC_C2)
    say('')
    say(f'合计不一致格数：{n1+n2+n3+n4+n5+n6+n7+n8} / {8*35}')

    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('WROTE ' + OUT)


if __name__ == '__main__':
    main()
