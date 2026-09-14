# -*- coding: utf-8 -*-
"""范围内核心检查（改进版）：md ↔ tex 同版性。

两把尺子：
  ① **汉字二元组 Jaccard**（对标记语言不敏感，>0.9 视为同版）
  ② **数值集合差异**（清洗双侧对称：表格内容**两侧都保留**，只去标记）
"""
import os, re, io, csv

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

MAP = {
    '01_问题重述.tex': ['A_04_问题重述.md'], '02_问题分析.tex': ['A_05_问题分析.md'],
    '03_模型假设.tex': ['A_06_模型假设.md'], '04_符号说明.tex': ['A_07_符号说明.md'],
    '05_模型建立与求解.tex': ['A_08_模型建立与求解.md', 'A_09_结果分析.md'],
    '06_模型检验.tex': ['A_10_模型检验.md'], '07_模型评价与推广.tex': ['A_11_模型评价与改进.md'],
    '08_AI工具使用声明.tex': ['A_12_AI工具使用声明.md'], '09_参考文献.tex': ['A_13_参考文献.md'],
    '10_附录.tex': ['A_14_附录.md'],
}
DEC = re.compile(r'(?<![\d.])(\d{1,4}\.\d{2,6})(?![\d])')


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def md_export(fn):
    t = read(os.path.join(BODY, fn))
    m = re.search(r'<!--\s*LATEX-EXPORT:BEGIN\s*-->(.*?)<!--\s*LATEX-EXPORT:END\s*-->', t, re.S)
    return m.group(1) if m else t


def norm(s):
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'\\[a-zA-Z]+\*?', ' ', s)          # LaTeX 命令名（双侧对称）
    s = re.sub(r'\\begin\{[^}]*\}|\\end\{[^}]*\}', ' ', s)
    s = re.sub(r'\\(?:label|ref|eqref|cite|autoref|pageref)\{[^}]*\}', ' ', s)
    s = re.sub(r'[*`_#&|~^\\{}\[\]$]', ' ', s)     # 标记字符一律去（双侧对称）
    s = re.sub(r'\s+', '', s)
    return s


def bigrams(s):
    c = re.findall(r'[\u4e00-\u9fff]', s)
    j = [c[i] + c[i + 1] for i in range(len(c) - 1)]
    return set(j)


print('=== ① md ↔ tex：二元组 Jaccard ｜ 数值集合差异（对称清洗）===')
rows = []
for tex, mds in MAP.items():
    tp = os.path.join(DELIV, 'sections', tex)
    if not os.path.isfile(tp):
        continue
    t, m = norm(read(tp)), norm(' '.join(md_export(x) for x in mds))
    A, B = bigrams(m), bigrams(t)
    jac = len(A & B) / max(1, len(A | B))
    mn, tn = set(DEC.findall(m)), set(DEC.findall(t))
    verdict = '同版' if jac >= 0.90 and not (mn - tn) else '**须核**'
    rows.append([tex, round(jac, 3), len(mn), len(tn), ','.join(sorted(mn - tn)[:10]),
                 ','.join(sorted(tn - mn)[:10]), verdict])
    print('%-24s Jaccard %.3f ｜ md 数值 %3d / tex %3d ｜ %s' % (tex, jac, len(mn), len(tn), verdict))
    if mn - tn:
        print('      仅 md 有：' + ','.join(sorted(mn - tn)[:12]))
    if tn - mn:
        print('      仅 tex 有：' + ','.join(sorted(tn - mn)[:12]))

with open(os.path.join(TEMP, '_md与tex同版性.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['tex', 'Jaccard', 'md数值数', 'tex数值数', '仅md数值', '仅tex数值', '判定'])
    w.writerows(rows)

print()
print('=== ③ 红线上下文（"身份/学校"的 12 处逐条）===')
texts = []
for f in sorted(os.listdir(BODY)):
    if f.endswith('.md'):
        texts.append((f, re.sub(r'\s+', ' ', md_export(f))))
for name, t in texts:
    for m in re.finditer(r'(大学|学院|学号|姓名|指导教师|参赛队号)', t):
        s = max(0, m.start() - 34)
        print('   [%s] …%s…' % (name.replace('A_', '').replace('.md', ''), t[s:m.end() + 34]))
