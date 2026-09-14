# -*- coding: utf-8 -*-
"""P1（结构编号）＋P5（证据链）机械检查：label／ref／cite 双向表、图表环境计数、引用句配对。只读。"""
import os, re, io, csv
from collections import Counter

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
TEX = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'sections')
FRONT = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'frontmatter')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


files = [os.path.join(TEX, fn) for fn in sorted(os.listdir(TEX)) if fn.endswith('.tex')]
if os.path.isdir(FRONT):
    files += [os.path.join(FRONT, fn) for fn in sorted(os.listdir(FRONT)) if fn.endswith('.tex')]

labels, refs, cites, bib = {}, {}, {}, set()
envs, ig, caps = Counter(), 0, 0
for p in files:
    name = os.path.relpath(p, os.path.dirname(TEX))
    t = re.sub(r'(?m)(?<!\\)%.*$', '', read(p))
    for m in re.finditer(r'\\label\{([^}]*)\}', t):
        labels.setdefault(m.group(1), name)
    for m in re.finditer(r'\\(?:ref|eqref|autoref|pageref)\{([^}]*)\}', t):
        for k in m.group(1).split(','):
            refs.setdefault(k.strip(), []).append(name)
    for m in re.finditer(r'\\cite\{([^}]*)\}', t):
        for k in m.group(1).split(','):
            cites.setdefault(k.strip(), []).append(name)
    for m in re.finditer(r'\\bibitem\{([^}]*)\}', t):
        bib.add(m.group(1))
    for m in re.finditer(r'\\begin\{(figure|table|longtable|wrapfigure)\}', t):
        envs[m.group(1)] += 1
    ig += len(re.findall(r'\\includegraphics', t))
    caps += len(re.findall(r'\\caption', t))

dangling = [k for k in refs if k not in labels and not k.startswith('sec')]
unused = [k for k in labels if k not in refs]
missing_bib = [k for k in cites if k not in bib]
unused_bib = sorted(bib - set(cites))

print('=== P1 结构完整性（交付 tex ＋ frontmatter）===')
print('label = %d ｜ \\ref 目标 = %d ｜ \\cite 键 = %d ｜ bibitem = %d' % (len(labels), len(refs), len(cites), len(bib)))
print('环境计数：figure %d ｜ wrapfigure %d ｜ longtable %d ｜ table %d ｜ includegraphics %d ｜ caption %d'
      % (envs['figure'], envs['wrapfigure'], envs['longtable'], envs['table'], ig, caps))
print()
print('★ 悬空引用（ref 无 label）= %d %s' % (len(dangling), dangling[:20]))
print('★ 未被引用的 label = %d %s' % (len(unused), unused[:20]))
print('★ 引用但无 bibitem（缺文献）= %d %s' % (len(missing_bib), missing_bib[:10]))
print('★ bibitem 但正文未引用 = %d %s' % (len(unused_bib), unused_bib[:10]))
print()
fig_refs = sum(len(v) for k, v in refs.items() if k.startswith('fig:'))
tab_refs = sum(len(v) for k, v in refs.items() if k.startswith('tab:'))
eq_refs = sum(len(v) for k, v in refs.items() if k.startswith('eq:'))
sec_refs = sum(len(v) for k, v in refs.items() if k.startswith('sec:'))
print('引用计数：图 %d ｜ 表 %d ｜ 式 %d ｜ 节 %d ｜ 其他 %d'
      % (fig_refs, tab_refs, eq_refs, sec_refs,
         sum(len(v) for k, v in refs.items() if not re.match(r'^(fig|tab|eq|sec):', k))))

with open(os.path.join(TEMP, '_结构引用检查.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['项', '数量', '明细'])
    w.writerow(['悬空引用', len(dangling), ';'.join(dangling[:40])])
    w.writerow(['未被引用 label', len(unused), ';'.join(unused[:40])])
    w.writerow(['缺 bibitem', len(missing_bib), ';'.join(missing_bib[:40])])
    w.writerow(['未引用 bibitem', len(unused_bib), ';'.join(unused_bib[:40])])
