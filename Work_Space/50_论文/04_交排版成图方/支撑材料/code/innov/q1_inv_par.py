# -*- coding: utf-8 -*-
"""T2 公共并行求解器（供 UQ／数据同化／全局灵敏度／伴随 复用）

· `solve_worker(cfg)` 为一个纯函数式工作单元（可被 ProcessPoolExecutor pickle）
· cfg 支持：p（参数字典覆盖）、dt_off（T∞ 整体平移 ℃）、dc_off（C∞ 平移）、
           dT_noise / dC_noise（逐节点的边界扰动数组）、snap（快照时刻，默认 1800）
· 返回关键泛函（4 个登记量 ＋ 全场 L2）
"""
import os
import sys
import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (HERE, os.path.abspath(os.path.join(HERE, '..', 'code'))):
    if _p not in sys.path:
        sys.path.insert(0, _p)

_FIND = None


def _find_root(p, marker='10_赛题', _max=7):
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.abspath(os.path.join(p, '..', '..', '..', '..'))


ROOT = _find_root(HERE)
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx')
N, DR, R0 = 80, 0.25e-3, 0.02
DT = 1.0
NSTEP = 1800
IDX = [0, 20, 40, 60, 80]          # 0/0.5/1.0/1.5/2.0 cm（81 节点网格）


def load_att1():
    wb = load_workbook(ATT1, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    data = list(ws.iter_rows(values_only=True))[1:]
    return (np.array([float(r[0]) for r in data]),
            np.array([float(r[1]) for r in data]),
            np.array([float(r[2]) for r in data]))


def solve_worker(cfg):
    """一次完整求解（Q1 交付口径：T 精确推进 ＋ C 后向欧拉 M6）"""
    t, Tinf0, Cinf0 = load_att1()
    import q1_core as core
    p = dict(core.DEF)
    p.update(cfg.get('p', {}) or {})

    Tarr = Tinf0 + float(cfg.get('dt_off', 0.0))
    Carr = Cinf0 + float(cfg.get('dc_off', 0.0))
    if cfg.get('dT_noise') is not None:
        Tarr = Tarr + np.asarray(cfg['dT_noise'], dtype=float)
    if cfg.get('dC_noise') is not None:
        Carr = Carr + np.asarray(cfg['dC_noise'], dtype=float)

    Tf = lambda s: float(np.interp(s, t, Tarr))
    Cf = lambda s: float(np.interp(s, t, Carr))
    snap = cfg.get('snap', (1800,))
    res, _, _ = core.run_sim_collect(
        N=N, dr=DR, dt_out=DT, nsteps=NSTEP, p=p, Tenv_fn=Tf, Cenv_fn=Cf,
        sub=cfg.get('sub', 10), subT=1, cols=np.arange(0, N + 1, 4),
        snap_at=set(snap), tmethod='expm')
    Te, Ce = res['T_end'], res['C_end']
    return dict(T0=float(Te[0]), TR=float(Te[-1]),
                C0=float(Ce[0]), CR=float(Ce[-1]),
                T2=float(np.sqrt(np.mean(Te[IDX] ** 2))),
                C2=float(np.sqrt(np.mean(Ce[IDX] ** 2))))
