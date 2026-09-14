# -*- coding: utf-8 -*-
"""Q1 创新化路径 · 公共库（只放工具函数，不改变任何求解口径）

· 路径推导：自动定位工作区根（含 10_赛题 的目录）
· 复用：直接 import 主力求解核 `q1_core`（位于 ../code），**只读调用，不改其文件**
· 约定：本文件不引用、不记载任何资料中的日期。
"""
import io
import os
import sys
import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, '..', 'code'))
if CODE not in sys.path:
    sys.path.insert(0, CODE)

LOGDIR = os.path.join(HERE, 'logs')


def _find_root(p, marker='10_赛题', _max=6):
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
RESULTS = os.path.join(ROOT, '20_交付包', '09_代码与复现', 'results')
RESULT1 = os.path.join(RESULTS, 'result1.xlsx')
FIGDATA = os.path.join(ROOT, '20_交付包', '04_图表包', 'data')


class Rec(object):
    """极简日志记录器：print + 落盘（logs/<name>.log）"""

    def __init__(self, name):
        self.name = name
        self.lines = []

    def __call__(self, s=''):
        s = str(s)
        self.lines.append(s)
        print(s)

    def save(self):
        os.makedirs(LOGDIR, exist_ok=True)
        path = os.path.join(LOGDIR, self.name)
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.lines) + '\n')
        return path


def load_att1():
    wb = load_workbook(ATT1, data_only=True, read_only=True)
    ws = wb[wb.sheetnames[0]]
    data = list(ws.iter_rows(values_only=True))[1:]
    return (np.array([float(r[0]) for r in data]),
            np.array([float(r[1]) for r in data]),
            np.array([float(r[2]) for r in data]))


def env_fns():
    """返回 (t, Tinf, Cinf, Tenv, Cenv)，边界一律线性插值（口径 L3-06）"""
    t, Tinf, Cinf = load_att1()
    return (t, Tinf, Cinf,
            lambda s: float(np.interp(s, t, Tinf)),
            lambda s: float(np.interp(s, t, Cinf)))


def load_result1():
    """读交付文件 result1.xlsx → (time[n], dist[m], T[n,m], C[n,m])"""
    wb = load_workbook(RESULT1, data_only=True, read_only=True)
    out = []
    for sn in ('温度', '水分浓度'):
        ws = wb[sn]
        rows = list(ws.iter_rows(values_only=True))
        dist = np.array([float(x) for x in rows[0][1:]])
        arr = np.array([[float(x) for x in r[1:]] for r in rows[1:]])
        out.append(arr)
    rows = list(load_workbook(RESULT1, data_only=True, read_only=True)['温度'].iter_rows(values_only=True))
    time = np.array([int(r[0]) for r in rows[1:]])
    return time, dist, out[0], out[1]


def seminf_robin(T0, Tinf, h, D, t):
    """半无限介质（x>0）Robin 对流边界的短时解析解。

    控制：∂u/∂t = D ∂²u/∂x²，u(x,0)=T0，-D ∂u/∂x(0,t)=h[u(0,t)-Tinf]
    表面解：u(0,t) = Tinf + (T0-Tinf)·exp(β²)·erfc(β)，β = h√(t/D)
    """
    from scipy.special import erfc
    t = np.asarray(t, dtype=float)
    b = h * np.sqrt(t / D)
    return Tinf + (T0 - Tinf) * np.exp(b * b) * erfc(b)


def col_weights(dist_m):
    """给定 r 节点列（m），返回体积加权（∫C·r dr 用）的梯形权重（π、长度已约）。"""
    r = np.asarray(dist_m, dtype=float)
    w = np.zeros_like(r)
    w[0] = 0.5 * (r[1] - r[0])
    w[-1] = 0.5 * (r[-1] - r[-2])
    for i in range(1, len(r) - 1):
        w[i] = 0.5 * (r[i + 1] - r[i - 1])
    return w * r


def richardson(f1, f2, f3, ratio=2.0):
    """三点 Richardson：返回 (观测阶 p, 外推值 f_ext)。f1 最粗、f3 最细。"""
    e21 = f2 - f1
    e32 = f3 - f2
    if abs(e32) < 1e-300:
        return float('nan'), float(f3)
    p = np.log(abs(e21 / e32)) / np.log(ratio)
    f_ext = f3 + e32 / (ratio ** p - 1.0)
    return float(p), float(f_ext)
