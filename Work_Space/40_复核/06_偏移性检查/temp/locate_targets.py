# -*- coding: utf-8 -*-
"""把"渲染号（图 5-2 等）"映射到 tex 源码位置：以**题注文字**为匹配键（PDF ↔ tex）。只读。"""
import os, re, io, fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

TARGETS = ['表1-1', '表2-1', '表4-1', '表5-4',
           '图5-2', '图5-3', '图5-4', '图5-6', '图5-7', '图5-8', '图5-10', '图5-11',
           '图6-1', '图6-3', '图6-4', '图6-5']

d = fitz.open(os.path.join(DELIV, 'main.pdf'))
caps = []
for pno in range(1, d.page_count + 1):
    for line in d[pno - 1].get_text().split('\n'):
        s = line.strip()
        m = re.match(r'^(图|表)\s*(\d+-\d+)\s*(.*)$', s)
        if m:
            caps.append([m.group(1) + m.group(2), pno, m.group(3).strip()])

print('=== PDF 中的图表题注（前 40 条）===')
for num, pno, cap in caps[:40]:
    print('   %-8s p%-3d %s' % (num, pno, cap[:56]))

# tex 侧：全部 tex 文本
tex = {}
for fn in sorted(os.listdir(os.path.join(DELIV, 'sections'))):
    if fn.endswith('.tex'):
        tex[fn] = io.open(os.path.join(DELIV, 'sections', fn), encoding='utf-8', errors='ignore').read()

out = ['### 渲染号 → tex 定位（以题注文字为键）', '']
print()
print('=== 目标项定位 ===')
for t in TARGETS:
    hit = [c for c in caps if c[0] == t]
    if not hit:
        print('   %-8s ✗ PDF 中未找到该题注' % t)
        out.append('%s: PDF 未找到' % t)
        continue
    num, pno, cap = hit[0]
    key = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '', cap)[:12]
    loc = []
    for fn, txt in tex.items():
        for m in re.finditer(re.escape(key) if key else r'(?!x)x', txt):
            ln = txt[:m.start()].count('\n') + 1
            loc.append((fn, ln))
    # 另按 \includegraphics / caption 附近找
    print('   %-8s p%-3d ｜题注「%s」｜tex 命中: %s' % (t, pno, cap[:34],
          ', '.join('%s:%d' % (f, l) for f, l in loc[:3]) or '（需按题注全文再找）'))
    out.append('--- %s （PDF p%d）题注：%s' % (t, pno, cap))
    for f, l in loc[:2]:
        lines = tex[f].split('\n')
        for i in range(max(0, l - 9), min(len(lines), l + 4)):
            out.append('   %s:%d  %s' % (f, i + 1, lines[i].strip()[:120]))
        out.append('')
    if not loc:
        out.append('   （未命中，需人工看 tex）\n')

io.open(os.path.join(TEMP, '_精修定位.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print()
print('★ 详细定位（含上下文）→ temp/_精修定位.txt（%d 行）' % len(out))
