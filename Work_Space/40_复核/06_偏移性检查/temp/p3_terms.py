# -*- coding: utf-8 -*-
"""P3（机理保真）＋P4（结论强度）＋P6（原味指纹）文本侧扫描。

对象：`成文/A_*.md` 的 LaTeX-EXPORT 区块（去元信息）与 `sections/*.tex`（去注释）。
只读；产物写入 temp/。
"""
import os, re, io, csv
from collections import Counter

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
TEX = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文', 'sections')
BASE = os.path.join(ROOT, '50_论文', '02_章节稿', '基线')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

MECH_POS = ['元体平衡', '有限体积', '单元中心', '严格守恒', 'M 矩阵', 'M矩阵', '对角占优', '极值原理',
            '矩阵指数', '杜哈梅尔', '追赶法', '三对角', '子步级二分', '交替推进', '仿射收缩', '物料坐标',
            '第三类边界', '积分平均', '洛必达', '半格', '次随机', '广义理查森', '网格收敛指数', '数据同化']
MECH_NEG = ['有限差分', '差分格式', '显式欧拉', '前向欧拉', '隐式欧拉', '纯解析解', '高斯消元',
            '集总参数', '有限元', '多模型融合', '数据驱动模型', '神经网络', '机器学习']
STRENGTH = ['证明', '必然', '完全', '唯一', '显著', '首次', '最优', '彻底', '毫无疑问', '毋庸置疑', '精确无误', '充分说明']
AI_TRACE = ['赋能', '助力', '显著提升', '极大', '完美', '一体化', '深度融合', '全方位', '彰显', '打造', '抓手', '痛点', '闭环']
TEMPLATE = ['值得注意的是', '综上所述', '不难看出', '众所周知', '为了更好地', '由此可见', '总而言之', '需要指出']
SELF = ['本文认为', '在本文口径下', '本文判据', '笔者认为', '本文选择', '本文不采用', '本文取', '本文不宣称', '本文限定']


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def exported(md):
    t = read(md)
    m = re.search(r'<!--\s*LATEX-EXPORT:BEGIN\s*-->(.*?)<!--\s*LATEX-EXPORT:END\s*-->', t, re.S)
    return m.group(1) if m else t


def detex(tex):
    return re.sub(r'(?m)(?<!\\)%.*$', '', read(tex))


docs = []
for fn in sorted(os.listdir(BODY)):
    if fn.endswith('.md'):
        docs.append(('成文/' + fn, exported(os.path.join(BODY, fn)), 'md'))
for fn in sorted(os.listdir(TEX)):
    if fn.endswith('.tex'):
        docs.append(('tex/' + fn, detex(os.path.join(TEX, fn)), 'tex'))
base_docs = []
if os.path.isdir(BASE):
    for fn in sorted(os.listdir(BASE)):
        if fn.endswith('.md'):
            base_docs.append(('基线/' + fn, exported(os.path.join(BASE, fn)), 'md'))

LATEX_CMD = re.compile(r'\\[a-zA-Z]+\*?|[{}$\\]|\\begin\{[^}]*\}|\\end\{[^}]*\}')


def clean(s, kind):
    if kind == 'tex':
        s = LATEX_CMD.sub(' ', s)
    return s


# ---------- P3/P4/P6 词表扫描 ----------
def scan(docs, words):
    hits = {}
    for name, txt, kind in docs:
        t = clean(txt, kind)
        for w in words:
            n = t.count(w)
            if n:
                hits.setdefault(w, []).append((name, n))
    return hits


SCAN_ROWS = []


def report(title, words, docs):
    print('=== %s ===' % title)
    h = scan(docs, words)
    for w in words:
        row = sorted(h.get(w, []), key=lambda x: -x[1])
        tot = sum(n for _, n in row)
        SCAN_ROWS.append([title, w, tot, '；'.join('%s×%d' % (n, c) for n, c in row)])
        if tot:
            print('   %-10s 合计 %-4d' % (w, tot))
        else:
            print('   %-10s 合计 0' % w)
    print()
    return h


print('### 扫描对象：成文 %d 件 ＋ tex %d 件（基线 %d 件供对照）'
      % (sum(1 for _, _, _ in docs), sum(1 for n, _, k in docs if k == 'tex'), len(base_docs)))
print()
report('P3-正：机理学名（应存在）', MECH_POS, docs)
report('P3-反：误称／被否定的模型形态（应为 0）', MECH_NEG, docs)
report('P4：结论强度词（需逐条回查证据）', STRENGTH, docs)
report('P6-a：AI 痕迹词（密度不应高于基线）', AI_TRACE, docs)
report('P6-b：模板腔词（密度不应高于基线）', TEMPLATE, docs)
report('P6-c：第一人称判断句（原味指标，应存在）', SELF, docs)

print('--- 对照：基线侧同表 ---')
report('基线 · AI 痕迹词', AI_TRACE, base_docs)
report('基线 · 模板腔词', TEMPLATE, base_docs)
report('基线 · 第一人称判断句', SELF, base_docs)

# ---------- P6 风格指纹（句长/短句率/标点密度） ----------
SENT = re.compile(r'[^。！？；]+[。！？；]')


def fingerprint(docs):
    rows = []
    for name, txt, kind in docs:
        t = clean(txt, kind)
        t = re.sub(r'\s+', '', t)
        if len(t) < 200:
            continue
        sents = [s for s in SENT.findall(t) if len(s.strip()) > 3]
        if not sents:
            continue
        L = [len(s) for s in sents]
        L.sort()
        med = L[len(L) // 2]
        short = sum(1 for x in L if x <= 15) / len(L)
        four = len(re.findall(r'(?<=[\u4e00-\u9fff])[\u4e00-\u9fff]{4}(?=[，。、；：）]|$)', t))
        rows.append([name, len(t), len(sents), round(sum(L) / len(L), 1), med,
                     round(100 * short, 1), round(100 * four / len(sents), 2),
                     round(100 * t.count('——') / len(sents), 2),
                     round(100 * (t.count('（') + t.count('(')) / len(sents), 2)])
    return rows


with open(os.path.join(TEMP, '_词表扫描.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['组', '词', '合计', '分布'])
    w.writerows(SCAN_ROWS)

print()
print('=== P6 风格指纹：文件 ｜ 汉字数 ｜ 句数 ｜ 平均句长 ｜ 中位句长 ｜ 短句率% ｜ 四字格/百句 ｜ 破折号/百句 ｜ 括号/百句 ===')
fp = fingerprint(docs) + fingerprint(base_docs)
with open(os.path.join(TEMP, '_风格指纹对照.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['文件', '字符数', '句数', '平均句长', '中位句长', '短句率%', '四字格每百句', '破折号每百句', '括号每百句'])
    w.writerows(fp)
for r in fp:
    print('   %-34s %6d %5d %6.1f %6d %7.1f %10.2f %11.2f %10.2f' % tuple(r))
