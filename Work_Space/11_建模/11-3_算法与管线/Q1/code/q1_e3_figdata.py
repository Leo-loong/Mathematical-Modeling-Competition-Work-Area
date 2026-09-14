# -*- coding: utf-8 -*-
"""
E3 图数据导出（供 F-12）
========================
从 `q1_e3_log.txt` 的"逐时刻比对"表格解析出数值解／显式解逐时刻对照值，
导出为 `30_图表/03_图数据准备/fig_e3_check.csv`。
不重跑求解（E3 为确定性计算），仅做格式转换，保证图数据与日志**同源**。

用法：python q1_e3_figdata.py
约定：本文件不引用、不记载任何资料中的日期。
"""
import io
import os
import sys

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
SRC = os.path.join(HERE, 'q1_e3_log.txt')
DST = os.path.join(ROOT, '30_图表', '03_图数据准备', 'fig_e3_check.csv')


def main():
    lines = io.open(SRC, encoding='utf-8').read().splitlines()
    rows = []
    for ln in lines:
        if '|' not in ln:
            continue
        parts = ln.split('|')
        if len(parts) != 5:
            continue
        try:
            t = int(parts[0].strip())
        except ValueError:
            continue
        try:
            a = parts[1].split()
            b = parts[2].split()
            c = parts[3].split()
            d = parts[4].split()
            rows.append((t, float(a[0]), float(a[1]), float(b[0]), float(b[1]),
                         float(c[0]), float(c[1]), float(d[0]), float(d[1])))
        except (ValueError, IndexError):
            continue
    if not rows:
        print('解析失败：未在日志中找到逐时刻比对表')
        return 1
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with io.open(DST, 'w', encoding='utf-8') as f:
        f.write('t,Tc_main,Tc_expl,Ts_main,Ts_expl,Cc_main,Cc_expl,Cs_main,Cs_expl\n')
        for r in rows:
            f.write('%d,%.6f,%.6f,%.6f,%.6f,%.7f,%.7f,%.7f,%.7f\n' % r)
    print('OK rows=%d -> %s' % (len(rows), DST))
    return 0


if __name__ == '__main__':
    sys.exit(main())
