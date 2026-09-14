# -*- coding: utf-8 -*-
"""P3-反／P4 上下文判读：把"命中词"落回原句，判"否定式使用"还是"误称／强度通胀"。只读。"""
import os, re, io

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
TEX = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'sections')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

WORDS = {
    '集总参数': 12, '有限元': 6, '多模型融合': 8, '数据驱动模型': 6,
    '证明': 6, '唯一': 4, '首次': 6, '必然': 8, '显著': 10, '值得注意的是': 4,
}


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def exported(md):
    t = read(md)
    m = re.search(r'<!--\s*LATEX-EXPORT:BEGIN\s*-->(.*?)<!--\s*LATEX-EXPORT:END\s*-->', t, re.S)
    return m.group(1) if m else t


def detex(tex):
    return re.sub(r'(?m)(?<!\\)%.*$', '', read(tex))


docs = [('成文/' + fn, exported(os.path.join(BODY, fn))) for fn in sorted(os.listdir(BODY)) if fn.endswith('.md')]
docs += [('tex/' + fn, detex(os.path.join(TEX, fn))) for fn in sorted(os.listdir(TEX)) if fn.endswith('.tex')]

out = []
print('=== 命中词上下文判读（同一处会同时出现在 成文 与 tex，属同一句的两次计数）===')
for w, cap in WORDS.items():
    occ = []
    for name, txt in docs:
        t = re.sub(r'\s+', ' ', re.sub(r'\\[a-zA-Z]+\*?|[{}$\\]', ' ', txt))
        for m in re.finditer(re.escape(w), t):
            s = max(0, m.start() - 46)
            occ.append((name, t[s:m.end() + 46]))
    out.append('### %s（共 %d 处，含 md/tex 重复）' % (w, len(occ)))
    for name, ctx in occ:
        out.append('   [%s] …%s…' % (name, ctx))
    print('   %-8s 命中 %-3d 处 ｜ 首例 [%s] …%s…' % (w, len(occ), occ[0][0] if occ else '-', occ[0][1][:78] if occ else ''))
    out.append('')

with io.open(os.path.join(TEMP, '_上下文判读.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print()
print('★ 全部上下文 → temp/_上下文判读.txt（共 %d 行）' % len(out))
