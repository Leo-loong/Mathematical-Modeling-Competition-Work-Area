# -*- coding: utf-8 -*-
"""列出每个编号式的：label、公式本体（截断）、紧邻前文（用于判断可否加 \\eqref）。只读。"""
import os, re, io

TEX = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space\50_论文\04_交排版成图方\交付排版方论文\sections'


def rd(p):
    return io.open(p, encoding='utf-8', errors='ignore').read()


for fn in sorted(os.listdir(TEX)):
    if not fn.endswith('.tex'):
        continue
    t = rd(os.path.join(TEX, fn))
    if '\\begin{equation}' not in t:
        continue
    print('#' * 8, fn)
    for m in re.finditer(r'\\begin\{equation\}(.*?)\\end\{equation\}', t, re.S):
        body = m.group(1)
        lab = re.search(r'\\label\{([^}]*)\}', body)
        if not lab:
            continue
        eq = re.sub(r'\\label\{[^}]*\}', '', body)
        eq = re.sub(r'\s+', ' ', eq).strip()
        before = t[max(0, m.start() - 120):m.start()]
        before = re.sub(r'\s+', ' ', before).strip()
        print('  [%s]' % lab.group(1))
        print('     前文: …%s' % before[-96:])
        print('     公式: %s' % eq[:120])
