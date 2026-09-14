# -*- coding: utf-8 -*-
"""核验本轮新增的 5 处 \\eqref：① tex 侧引用解析 ② PDF 侧实际呈现（含式号）③ label 键 vs 渲染号。只读。"""
import os, re, io, fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
TEX = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'sections')
PDF = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'main.pdf')

# ① tex 侧：label 列表 / 引用列表
labels, refs = set(), set()
for fn in sorted(os.listdir(TEX)):
    if fn.endswith('.tex'):
        t = io.open(os.path.join(TEX, fn), encoding='utf-8', errors='ignore').read()
        labels |= set(re.findall(r'\\label\{(eq:[^}]*)\}', t))
        for m in re.finditer(r'\\(?:eqref|ref|autoref)\{([^}]*)\}', t):
            for k in m.group(1).split(','):
                refs.add(k.strip())
eq_lab = sorted(x for x in labels if x.startswith('eq:'))
eq_ref = sorted(x for x in refs if x.startswith('eq:'))
print('① tex 侧：eq label %d ｜ 被引用 %d ｜ 未引用 %d' % (len(eq_lab), len(eq_ref), len(eq_lab) - len(eq_ref)))
print('   已引用（键名）:', ' '.join(x.replace('eq:', '') for x in eq_ref))
print('   未引用（键名）:', ' '.join(x.replace('eq:', '') for x in eq_lab if x not in eq_ref))

# ② PDF 侧：每处改动前后文（用"改动后的新词"定位）
d = fitz.open(PDF)
probe = ['定解条件为', '积分可闭式求得', '等价性可写成', '总代价因此为', '积分平均（式']
for a in probe:
    hits = []
    for i, p in enumerate(d):
        t = p.get_text()
        for m in re.finditer(re.escape(a), t):
            hits.append((i + 1, re.sub(r'\s+', ' ', t[m.start():m.start() + 76])))
    print()
    print('② [%s] 命中 %d 处' % (a, len(hits)))
    for pno, ctx in hits:
        print('     p%-4d %s' % (pno, ctx))
