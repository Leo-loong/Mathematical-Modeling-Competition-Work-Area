# -*- coding: utf-8 -*-
"""打通三方编号：① 成品图文件名（图NN-…） ② tex 中的 figure 块 ③ PDF 渲染号＋题注＋页码。只读。"""
import os, re, io, fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

# ---------- PDF 侧：所有 图/表 号 + 紧随文字 ----------
d = fitz.open(os.path.join(DELIV, 'main.pdf'))
print('=== PDF 侧：全部渲染号（去重，含页码与紧随文字）===')
seen = {}
for pno in range(1, d.page_count + 1):
    t = re.sub(r'\s+', ' ', d[pno - 1].get_text())
    for m in re.finditer(r'(图|表)\s*(\d+-\d+)\s*([^。；]{0,40})', t):
        k = m.group(1) + m.group(2)
        if k not in seen:
            seen[k] = (pno, m.group(3).strip()[:40])
figs = sorted([k for k in seen if k.startswith('图')], key=lambda x: (int(x[1:].split('-')[0]), int(x[1:].split('-')[1])))
tabs = sorted([k for k in seen if k.startswith('表')], key=lambda x: (int(x[1:].split('-')[0]), int(x[1:].split('-')[1])))
for k in figs:
    print('   %-8s p%-3d %s' % (k, seen[k][0], seen[k][1]))
for k in tabs:
    print('   %-8s p%-3d %s' % (k, seen[k][0], seen[k][1]))

# ---------- tex 侧：figure 块（含 includegraphics 名、caption、注释里的编号） ----------
print()
print('=== tex 侧：figure 块清单（05_模型建立与求解.tex / 06_模型检验.tex）===')
out = []
for fn in ('05_模型建立与求解.tex', '06_模型检验.tex'):
    txt = io.open(os.path.join(DELIV, 'sections', fn), encoding='utf-8', errors='ignore').read()
    lines = txt.split('\n')
    for i, l in enumerate(lines):
        if '\\begin{figure}' in l or '\\begin{wrapfigure}' in l:
            blk = '\n'.join(lines[i:i + 14])
            ig = re.search(r'\\includegraphics[^{]*\{([^}]*)\}', blk)
            cap = re.search(r'\\caption\{([^}]*)\}', blk)
            # 往前找注释里的编号（如 % 图5-11 / 登记 5-11）
            ctx = '\n'.join(lines[max(0, i - 4):i])
            num = re.findall(r'(\d+-\d+)', ctx) + re.findall(r'(\d+-\d+)', blk)
            print('   %s:%-4d %-13s 图件=%-34s 编号提示=%-10s 题注=%s' % (
                fn, i + 1, 'wrapfigure' if 'wrapfigure' in l else 'figure',
                (os.path.basename(ig.group(1)) if ig else '—')[:33],
                ','.join(dict.fromkeys(num))[:9] or '—',
                (cap.group(1)[:26] if cap else '—')))
            out.append('%s:%d' % (fn, i + 1))

io.open(os.path.join(TEMP, '_图表清单.txt'), 'w', encoding='utf-8').write(
    '\n'.join('%s p%d %s' % (k, seen[k][0], seen[k][1]) for k in figs + tabs))
print()
print('★ PDF 侧清单 → temp/_图表清单.txt')
