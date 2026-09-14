# -*- coding: utf-8 -*-
"""P1b 图/表/式的引用覆盖：label 是否被正文引用（\\ref／\\eqref／\\autoref）。只读。"""
import os, re, io

TEX = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space\50_论文\04_交排版成图方\交付排版方论文\sections'


def rd(p):
    return io.open(p, encoding='utf-8', errors='ignore').read()


labels, refs = set(), set()
for fn in sorted(os.listdir(TEX)):
    if fn.endswith('.tex'):
        t = re.sub(r'(?m)(?<!\\)%.*$', '', rd(os.path.join(TEX, fn)))
        labels |= set(re.findall(r'\\label\{([^}]*)\}', t))
        for m in re.finditer(r'\\(?:ref|eqref|autoref)\{([^}]*)\}', t):
            refs |= set(k.strip() for k in m.group(1).split(','))

for pre, name in (('fig:', '图'), ('tab:', '表'), ('eq:', '式')):
    L = sorted(x for x in labels if x.startswith(pre))
    R = sorted(x for x in refs if x.startswith(pre))
    U = [x for x in L if x not in R]
    print('%s：label %d 个 ｜ 被引用 %d 个 ｜ **未被引用 %d 个**' % (name, len(L), len(R), len(U)))
    if U:
        print('   未被引用的：', ' '.join(x.replace(pre, '') for x in U))
