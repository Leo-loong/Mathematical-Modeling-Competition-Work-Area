# -*- coding: utf-8 -*-
"""聚合 ai_files.txt：按目录分组统计 + 输出可读报告。"""
import io, os
from collections import Counter

BASE = r'c:/Users/wang-/Desktop/2026数学建模/2025国赛真题/B题/Work_Space/kb/source'
IN = os.path.join(BASE, 'temp', 'ai_files.txt')
OUT = os.path.join(BASE, 'temp', 'ai_report.txt')

sec = None
name_rows, meta_rows = [], []
for line in io.open(IN, encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('### A'):
        sec = 'A'
        continue
    if line.startswith('### B'):
        sec = 'B'
        continue
    if not line.strip():
        continue
    (meta_rows if sec == 'B' else name_rows).append(line.split('\t'))

def top_dirs(rows, depth=2):
    c = Counter()
    for r in rows:
        parts = r[2].split('/')
        c['/'.join(parts[:depth])] += 1
    return c

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write('A 文件名命中 %d 个\n' % len(name_rows))
    for d, n in top_dirs(name_rows).most_common():
        f.write('  %4d  %s\n' % (n, d))
    f.write('\nB 仅标题/关键词命中 %d 个\n' % len(meta_rows))
    for d, n in top_dirs(meta_rows).most_common():
        f.write('  %4d  %s\n' % (n, d))
    # kind 分布
    f.write('\nA kind 分布: %s\n' % Counter(r[0] for r in name_rows))
    f.write('B kind 分布: %s\n' % Counter(r[0] for r in meta_rows))
    # B 部分逐条列出（文件名不含 AI 但内容是 AI 主题——重点核查对象）
    f.write('\nB 逐条清单：\n')
    for r in sorted(meta_rows, key=lambda x: x[2]):
        f.write('  [%s|%s] %s\n' % (r[0], r[1], r[2]))
print('report written')
