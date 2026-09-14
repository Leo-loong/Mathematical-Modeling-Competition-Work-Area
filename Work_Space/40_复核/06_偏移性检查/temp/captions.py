# -*- coding: utf-8 -*-
"""提取每个 图/表 渲染号对应的**题注原文**与页码（图：题注在编号的下一行；表：题注同行）。只读。"""
import os, re, fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')

d = fitz.open(os.path.join(DELIV, 'main.pdf'))
res = {}
for pno in range(1, d.page_count + 1):
    lines = [l.strip() for l in d[pno - 1].get_text().split('\n')]
    for i, l in enumerate(lines):
        m = re.fullmatch(r'(图|表)\s*(\d+-\d+)', l)
        if m:
            k = m.group(1) + m.group(2)
            nxt = ''
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j]:
                    nxt = lines[j]
                    break
            res.setdefault(k, (pno, nxt[:56]))
        else:
            m2 = re.match(r'^(表)\s*(\d+-\d+)\s+(.{4,})$', l)
            if m2:
                k = m2.group(1) + m2.group(2)
                res.setdefault(k, (pno, m2.group(3)[:56]))

def key(k):
    a, b = k[1:].split('-')
    return (k[0], int(a), int(b))

print('=== 图：渲染号 → 页码 → 题注 ===')
for k in sorted([x for x in res if x.startswith('图')], key=key):
    print('   %-7s p%-3d %s' % (k, res[k][0], res[k][1]))
print()
print('=== 表：渲染号 → 页码 → 题注 ===')
for k in sorted([x for x in res if x.startswith('表')], key=key):
    print('   %-7s p%-3d %s' % (k, res[k][0], res[k][1]))
