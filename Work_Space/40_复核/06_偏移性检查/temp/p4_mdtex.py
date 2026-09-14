# -*- coding: utf-8 -*-
"""范围内核心检查：**原 md ↔ LaTeX 同版性** ＋ **论文内部数值自洽** ＋ **论文自身红线**。

范围（严格）：`06_偏移性检查` 之外只读 `成文/*.md`、`基线/*.md`、`交付排版方论文/{main,preamble}.tex`、
`sections/*.tex`、`frontmatter/*.tex`。**不读**口径总表／结果文件／代码／支撑材料／过程文档／快照。
"""
import os, re, io, csv

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
BASE = os.path.join(ROOT, '50_论文', '02_章节稿', '基线')
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

MAP = {
    '01_问题重述.tex': ['A_04_问题重述.md'],
    '02_问题分析.tex': ['A_05_问题分析.md'],
    '03_模型假设.tex': ['A_06_模型假设.md'],
    '04_符号说明.tex': ['A_07_符号说明.md'],
    '05_模型建立与求解.tex': ['A_08_模型建立与求解.md', 'A_09_结果分析.md'],
    '06_模型检验.tex': ['A_10_模型检验.md'],
    '07_模型评价与推广.tex': ['A_11_模型评价与改进.md'],
    '08_AI工具使用声明.tex': ['A_12_AI工具使用声明.md'],
    '09_参考文献.tex': ['A_13_参考文献.md'],
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


def clean_md(s):
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'^\s*\|.*$', ' ', s, flags=re.M)          # 表格行（tex 侧会重排，不可比）
    s = re.sub(r'(?m)^\s*>.*$', ' ', s)                    # 引用块
    s = re.sub(r'[*`_#]', ' ', s)
    s = s.replace('\\', ' ')
    return s


def clean_tex(s):
    s = re.sub(r'(?m)(?<!\\)%.*$', '', s)
    s = re.sub(r'\\begin\{(longtable|table|figure|center|tabular|wrapfigure)\}.*?\\end\{\1\}', ' ', s, flags=re.S)
    s = re.sub(r'\\(?:label|ref|eqref|cite|autoref|pageref)\{[^}]*\}', ' ', s)
    s = re.sub(r'\\[a-zA-Z]+\*?', ' ', s)
    return s.replace('{', ' ').replace('}', ' ')


def cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))


def sents(s):
    out = []
    for x in re.split(r'[。！？；]', s):
        x = re.sub(r'\s+', '', x)
        if cjk(x) >= 8:
            out.append(x)
    return out


print('=== ① 原 md ↔ LaTeX 同版性（逐章）===')
print('%-26s %-9s %-9s %-9s %-7s %s' % ('tex 文件', 'md汉字', 'tex汉字', '差异', '句覆盖', '数值集合差异'))
rows = []
all_md_nums, all_tex_nums = {}, {}
for tex, mds in MAP.items():
    tp = os.path.join(DELIV, 'sections', tex)
    if not os.path.isfile(tp):
        continue
    t = clean_tex(read(tp))
    m = ' '.join(clean_md(md_export(x)) for x in mds)
    mn, tn = set(DEC.findall(m)), set(DEC.findall(t))
    ms = sents(m)
    tc = re.sub(r'\s+', '', t)
    cov = sum(1 for s in ms if s[:10] in tc) / max(1, len(ms))
    all_md_nums[tex], all_tex_nums[tex] = mn, tn
    rows.append([tex, cjk(m), cjk(t), cjk(t) - cjk(m), round(100 * cov, 1),
                 ('仅md: ' + ','.join(sorted(mn - tn)[:8])) if mn - tn else '',
                 ('仅tex: ' + ','.join(sorted(tn - mn)[:8])) if tn - mn else ''])
    print('%-26s %-9d %-9d %-+9d %-6.1f%% %s' % (tex, cjk(m), cjk(t), cjk(t) - cjk(m), 100 * cov,
                                                ('仅md:%s' % ','.join(sorted(mn - tn)[:6])) if mn - tn else
                                                (('仅tex:%s' % ','.join(sorted(tn - mn)[:6])) if tn - mn else '一致')))

with open(os.path.join(TEMP, '_md与tex对账.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['tex', 'md汉字', 'tex汉字', '汉字差', '句覆盖%', '仅md数值', '仅tex数值'])
    w.writerows(rows)

print()
print('=== ② 论文内部数值自洽（摘要 ↔ 正文/附录）===')
ab = clean_md(md_export('A_02_摘要.md'))
abn = set(DEC.findall(ab))
rest = set()
for tex, mds in MAP.items():
    rest |= all_tex_nums.get(tex, set())
orphan = sorted(abn - rest)
print('摘要数据型数值 %d 个 ｜ 其中**正文/附录中未再现** = %d 个：%s' % (len(abn), len(orphan), orphan[:20]))

print()
print('=== ③ 论文自身红线（md＋tex 全文扫）===')
reds = {
    '内部代号 F\\d{2}': r'\bF\d{2}\b', '内部代号 INV\\d': r'\bINV\d\b',
    '日期类数字': r'(20\d{2}\s*年|[0-9]{1,2}\s*月\s*[0-9]{1,2}\s*日)',
    '自评词 创新': r'创新', '身份/学校': r'(大学|学院|学号|姓名|指导教师|参赛队号)',
    '口语/感叹': r'(非常|特别|超级|简直|！)',
}
texts = {'成文': ' '.join(clean_md(md_export(f)) for f in os.listdir(BODY) if f.endswith('.md'))}
for tex in MAP:
    p = os.path.join(DELIV, 'sections', tex)
    if os.path.isfile(p):
        texts['tex'] = texts.get('tex', '') + ' ' + clean_tex(read(p))
for k, pat in reds.items():
    tot = []
    for who, t in texts.items():
        for m in re.finditer(pat, t):
            tot.append((who, t[max(0, m.start() - 22):m.end() + 22].replace('\n', ' ')))
    print('   %-16s 命中 %-3d %s' % (k, len(tot), ('例：' + tot[0][1][:60]) if tot else ''))
