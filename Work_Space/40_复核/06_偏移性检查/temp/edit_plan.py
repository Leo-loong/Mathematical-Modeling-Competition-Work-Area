# -*- coding: utf-8 -*-
"""为 16 项精修取"当前位置 + 现有参数"（含图宽、表列宽、包络环境）。只读。"""
import os, re, io

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
SEC = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'sections')

CAPS = {
    '表1-1': '建模对象与给定数据', '表2-1': '四问要素对照', '表4-1': '主要符号一览',
    '表5-4': '网格加密序列', '图5-2': '问题一求解原理示意图', '图5-3': '问题一温度场时空分布',
    '图5-4': '问题一水分浓度场时空分布', '图5-6': '交替推进', '图5-7': '重叠段差异归因',
    '图5-8': '问题三求解流程图', '图5-10': '物质坐标变换示意', '图5-11': '压缩温升机理',
    '图6-1': '网格与时间收敛性', '图6-3': '解析级数解对拍', '图6-4': '守恒性总账瀑布图',
    '图6-5': '低含水率端外推不确定度',
}

files = {}
for fn in sorted(os.listdir(SEC)):
    if fn.endswith('.tex'):
        files[fn] = io.open(os.path.join(SEC, fn), encoding='utf-8', errors='ignore').read().split('\n')

print('=== 16 项目标：位置与现有参数 ===')
for tag, key in CAPS.items():
    found = None
    for fn, lines in files.items():
        for i, l in enumerate(lines):
            if key in l:
                found = (fn, i)
                break
        if found:
            break
    if not found:
        print('   %-7s ✗ 未找到（键：%s）' % (tag, key))
        continue
    fn, i = found
    lines = files[fn]
    # 找包络环境起止
    lo = max(0, i - 12)
    hi = min(len(lines), i + 16)
    blk = lines[lo:hi]
    env = next((x.strip() for x in blk if '\\begin{figure}' in x or '\\begin{wrapfigure}' in x or '\\begin{longtable}' in x or '\\begin{table}' in x), '?')
    igs = [x.strip()[:110] for x in blk if '\\includegraphics' in x]
    colspec = [x.strip()[:150] for x in blk if '\\begin{longtable}' in x or '\\begin{tabular}' in x]
    print('   %-7s %s:%d  环境=%s' % (tag, fn, i + 1, env[:44]))
    for c in colspec[:1]:
        print('           列宽定义: %s' % c)
    for g in igs[:4]:
        print('           图宽: %s' % g)
