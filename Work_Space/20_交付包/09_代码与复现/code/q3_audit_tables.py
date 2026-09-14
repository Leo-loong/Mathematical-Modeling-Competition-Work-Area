# -*- coding: utf-8 -*-
"""
第三问全量复查 · 表格数据逐值核对（T0 只读）
================================================================================
核对目标：表 5 的数据在 4 处文档中是否**逐值一致**
  ① 基线 `11_建模/大白话讲模型/A_第三问求解复盘.md`
  ② `20_交付包/01_模型叙述/A_Q3结果与分析.md`
  ③ `20_交付包/05_数值口径总表/A_数值口径总表.md` §10.2
  ④ `11_建模/11-3_算法与管线/Q3/A_Q3求解记录.md` §3.3
并以 result3.xlsx 的**实际数据**为最终真值源。
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import openpyxl
import numpy as np

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
R3 = os.path.join(WS, '20_交付包', '09_代码与复现', 'results', 'result3.xlsx')

DOCS = {
    '复盘(基线)': r'11_建模\大白话讲模型\A_第三问求解复盘.md',
    '结果与分析': r'20_交付包\01_模型叙述\A_Q3结果与分析.md',
    '口径表§10.2': r'20_交付包\05_数值口径总表\A_数值口径总表.md',
    '求解记录': r'11_建模\11-3_算法与管线\Q3\A_Q3求解记录.md',
}

# 表 5 的 5 个代表时刻（h）与其 5 列值（由 result3.xlsx 复算得到的真值）
# ★口径修正后：表 5 为 6/12/18/24/30/36/42/48/54 h 九行 ＋ 末行（旧版曾为 6–84 h）
HOURS = [6, 12, 18, 24, 30, 36, 42, 48, 54]

print('=' * 92)
print('第三问复查 · 表 5 数据逐值核对')
print('=' * 92)


def load_truth():
    """由 result3.xlsx 复算表 5 真值（每 6 h，列 r=0,0.5,1.0,1.5,2.0 cm）"""
    wb = openpyxl.load_workbook(R3, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True)]
    hdr = [c for c in rows[0] if c is not None]
    data = np.array([[float(x) for x in r[1:len(hdr)]] for r in rows[1:]])
    tcol = np.array([float(r[0]) for r in rows[1:]])
    wb.close()
    # 表头为 0.0,0.1,...,2.0 -> 取 0,0.5,1.0,1.5,2.0 cm 对应列号
    want = [0.0, 0.5, 1.0, 1.5, 2.0]
    idx = [i for i, c in enumerate(hdr[1:]) if round(float(c), 1) in want]
    truth = {}
    for h in HOURS:
        t_tar = h * 3600.0
        j = int(np.argmin(np.abs(tcol - t_tar)))
        truth[h] = data[j][idx]
    return truth, tcol[-1], data[-1][idx]


truth, t_final, last = load_truth()
print('  真值源：result3.xlsx，末行时刻 = %.3f h' % (t_final / 3600.0))
print('  末行（达标行）5 列 = ' + '  '.join('%.4f' % v for v in last))
print()

# 逐文档核对
print('【逐文档核对】（以 result3.xlsx 为真值，容差 1e-4 —— 因文档均 4 位小数）')
print()
for name, rel in DOCS.items():
    p = os.path.join(WS, rel)
    if not os.path.exists(p):
        print('  [缺失] %s' % rel)
        continue
    t = io.open(p, encoding='utf-8').read()
    print('  ── %s ──' % name)
    # 对每个代表时刻，检查该行 5 个数值是否都在文档中出现
    allok = True
    for h in HOURS:
        vals = truth[h]
        hit = [('%.4f' % v) in t for v in vals]
        if not all(hit):
            miss = ['%.4f' % v for v, ok in zip(vals, hit) if not ok]
            print('     h=%-3d  缺失值: %s' % (h, ' '.join(miss)))
            allok = False
    # 末行（57.5314）
    hit_last = [('%.4f' % v) in t for v in last]
    if not all(hit_last):
        miss = ['%.4f' % v for v, ok in zip(last, hit_last) if not ok]
        print('     末行(达标) 缺失值: %s' % ' '.join(miss))
        allok = False
    print('     ⟹ %s' % ('✅ 表 5 全部代表值一致' if allok else '⚠ 存在不一致，见上'))
    print()

# 关键标量核对
print('【关键标量跨文档一致性】')
SCALARS = {
    't_end=57.5314': [r'57\.5314'],
    '207113 s': [r'207[\\\,]{0,2}113'],
    '判据0.15': [r'0\.15'],
    '下界25.8': [r'25\.8'],
    '上界97.7': [r'97\.7'],
    '守恒2.394e-3': [r'2\.394'],
    'km-0.148': [r'0\.148'],
    '积分平均(M6)': [r'积分平均'],
    '旧口径87.49(应仅在说明处)': [r'87\.4933'],
    '干壳阻滞(应仅在证伪说明处)': [r'干壳阻滞'],
}
hdr = '%-16s' % '标量'
for nm in DOCS:
    hdr += '%-12s' % nm[:10]
print(hdr)
print('-' * len(hdr))
for sname, pats in SCALARS.items():
    line = '%-16s' % sname
    for nm, rel in DOCS.items():
        p = os.path.join(WS, rel)
        if not os.path.exists(p):
            line += '%-12s' % 'N/A'
            continue
        t = io.open(p, encoding='utf-8').read()
        n = sum(len(re.findall(pt, t)) for pt in pats)
        line += '%-12s' % (n if n else '·')
    print(line)
print()
print('  （数字=命中次数；·=未提及。**未提及不等于矛盾**，但基线未提及的项应按需补齐）')
