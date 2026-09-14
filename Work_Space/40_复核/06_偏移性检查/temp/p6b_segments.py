# -*- coding: utf-8 -*-
"""P6b 原味候选段抽取：按"元话语／模板腔／四字格密度"排序，给人读用。只读。"""
import os, re, io

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

META = ['值得注意的是', '需要说明的是', '需要指出的是', '需要强调的是', '本文认为', '本文取',
        '在本文口径下', '不构成新的', '本文不宣称', '需要声明', '须在引用时声明', '定位说明']
IDIOM = re.compile(r'(?<=[\u4e00-\u9fff])[\u4e00-\u9fff]{4}(?=[，。、；：）]|$)')


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def exported(md):
    t = read(md)
    m = re.search(r'<!--\s*LATEX-EXPORT:BEGIN\s*-->(.*?)<!--\s*LATEX-EXPORT:END\s*-->', t, re.S)
    return m.group(1) if m else t


rows = []
for fn in sorted(os.listdir(BODY)):
    if not fn.endswith('.md'):
        continue
    for para in re.split(r'\n\s*\n', exported(os.path.join(BODY, fn))):
        p = re.sub(r'\s+', ' ', para).strip()
        if len(p) < 60 or p.startswith('#') or p.startswith('|'):
            continue
        score = sum(p.count(w) for w in META) * 2 + len(IDIOM.findall(p))
        rows.append((score, len(IDIOM.findall(p)), fn, p[:300]))

rows.sort(key=lambda r: -r[0])
out = ['### P6b 原味候选段（按 元话语×2 ＋ 四字格 计分降序，取前 12 段）', '']
for s, n, fn, p in rows[:12]:
    out.append('**[%s] 计分 %d（四字格 %d）**\n   %s\n' % (fn, s, n, p))
with io.open(os.path.join(TEMP, '_原味候选段.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('★ 原味候选段 → temp/_原味候选段.txt（前 12 段）')
print()
for s, n, fn, p in rows[:12]:
    print('   [%s] 计分 %d ｜ 四字格 %d ｜ %s' % (fn, s, n, p[:96]))
