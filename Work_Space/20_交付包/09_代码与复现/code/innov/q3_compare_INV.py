# -*- coding: utf-8 -*-
"""
双轨比对器（创新副本专用 · 只读，不写任何正式产物）
================================================================================
用途：把"创新轨产物"与"正式基线产物"逐值比对，回答"该轨能否采信"。

设计要点（**重要方法学**）：
  · `t_end` 是**高条件数泛函**——后段 dC/dt ≈ 1.1e-3 /h，C 的 3e-5 差异即可放大为 0.03 h
    ⟹ **不得**用"t_end 之差"直接判等价；应比对 **C 剖面**（低条件数量），
       并把 t_end 差 **换算为等效 C 差**： δC_eq ≈ |Δt_end| × (dC/dt)|_late。
  · 比对口径：公共时间网格（60 s）× 21 列。

用法：
  python q3_compare_INV.py --a out/result3_INV1.xlsx --b ../../results/result3.xlsx --tag IN1
"""
import os
import sys
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import numpy as np
import openpyxl


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
WS = _find_root(HERE)
Q3DIR = os.path.dirname(HERE)
BASE = os.path.join(WS, '20_交付包', '09_代码与复现', 'results', 'result3.xlsx')


def load(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True)]
    t = np.array([float(r[0]) for r in rows[1:]])
    d = np.array([[float(x) for x in r[1:]] for r in rows[1:]])
    wb.close()
    return t, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--a', required=True, help='创新轨结果（相对本目录或绝对路径）')
    ap.add_argument('--b', default=BASE, help='基线结果（默认 交付包 result3.xlsx）')
    ap.add_argument('--tag', default='INV')
    args = ap.parse_args()

    pa = args.a if os.path.isabs(args.a) else os.path.join(HERE, args.a)
    pb = args.b if os.path.isabs(args.b) else os.path.join(HERE, args.b)

    ta, da = load(pa)
    tb, db = load(pb)
    n = min(len(ta), len(tb))

    print('=' * 88)
    print('双轨比对 [%s]' % args.tag)
    print('=' * 88)
    print('  A（创新轨）: %s' % os.path.basename(pa))
    print('     行数 %d，末行时刻 %.1f s = %.4f h' % (len(ta), ta[-1], ta[-1] / 3600.0))
    print('  B（基线）  : %s' % os.path.basename(pb))
    print('     行数 %d，末行时刻 %.1f s = %.4f h' % (len(tb), tb[-1], tb[-1] / 3600.0))
    print('  公共比对行数：%d（前 %.1f h）' % (n, ta[n - 1] / 3600.0))

    if da.shape[1] != db.shape[1]:
        print('  ⚠ 列数不一致：A=%d B=%d —— 只比对公共列' % (da.shape[1], db.shape[1]))
    m = min(da.shape[1], db.shape[1])
    dif = np.abs(da[:n, :m] - db[:n, :m])
    rel = dif / np.maximum(1e-12, np.abs(db[:n, :m]))

    print('-' * 88)
    print('  【C 剖面差异】max|ΔC| = %.4e ；沿时程的最大值位置：第 %d 行（t=%.2f h），第 %d 列'
          % (dif.max(), int(np.argmax(dif.max(axis=1))) + 1,
             ta[int(np.argmax(dif.max(axis=1)))] / 3600.0, int(np.argmax(dif.max(axis=0))) + 1))
    print('  相对差（分母 max(1e-12,|C_B|)）最大值 = %.4e' % rel.max())
    print('  末行（公共段）逐列 |ΔC|：' + ' '.join('%.2e' % v for v in dif[n - 1, :min(m, 21)]))
    print('  列 0（中心）|ΔC| 的最大值 = %.4e ；列 %d（表面）|ΔC| 的最大值 = %.4e'
          % (dif[:, 0].max(), m - 1, dif[:, m - 1].max()) if m >= 2 else '')

    # 高条件数换算
    tA, tB = ta[-1], tb[-1]
    dt_h = (tA - tB) / 3600.0
    # 后段 dC/dt（用基线最后 6 h 的中心列估）
    k = min(len(tb) - 1, int(6 * 3600 / 60))
    if k > 0:
        dcdt = (db[-1, 0] - db[-1 - k, 0]) / ((tb[-1] - tb[-1 - k]) / 3600.0)
    else:
        dcdt = float('nan')
    dC_eq = abs(dt_h) * abs(dcdt)
    print('-' * 88)
    print('  【t_end 与等效 C 差】Δt_end = %+.4f h ；后段 dC/dt（中心）≈ %.3e /h' % (dt_h, dcdt))
    print('    ⟹ **等效 C 差** δC_eq ≈ |Δt_end|·|dC/dt| = %.3e' % dC_eq)
    print('    ⟹ 判读：若 δC_eq 与 max|ΔC| **同量级**，则 t_end 之差可全部由 C 的数值差解释，')
    print('       两轨**数值等价**（t_end 之高条件数放大所致），**不构成方法差异**。')
    print('=' * 88)


if __name__ == '__main__':
    main()
