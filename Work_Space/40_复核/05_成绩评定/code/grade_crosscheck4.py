# -*- coding: utf-8 -*-
"""第四轮 · **待核查项交叉核查**（把"待核"变成"已实测"）。

关闭以下项：
  D-6  灵敏度分析覆盖的参数个数（判据 ≥5 个；P-A 工作量 #7）
  D-7  误差评价指标个数（判据 ≥4 个；P-A 工作量 #8）
  D-10 正文内的"流程图类"图件数（判据：每小问 1 张）
  D-17 是否给出「±10%／±20% 扰动 → 核心结果偏移／结论不变」的判定句
  D-20 是否有"工程/工艺启示"段
  D-15 选型是否含"为何不用其他方法"的排除式论证
  15.1 抄题自查（论文 ↔ 题面 的**最长公共片段**，替代不可自测的"查重率"）
只读；不写任何交付物。
"""
import io
import os
import re
import sys
from collections import defaultdict

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PAPER = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
SEC = os.path.join(PAPER, 'sections')
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
OUT = []


def p(s=''):
    OUT.append(s)
    print(s)


def read(f):
    return io.open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''


ALL = ''
for f in sorted(os.listdir(SEC)):
    if f.endswith('.tex'):
        ALL += read(os.path.join(SEC, f)) + '\n'
FRONT = read(os.path.join(PAPER, 'frontmatter', '00_摘要页.tex'))
A10 = read(os.path.join(BODY, 'A_10_模型检验.md'))
A11 = read(os.path.join(BODY, 'A_11_模型评价与改进.md'))
A08 = read(os.path.join(BODY, 'A_08_模型建立与求解.md'))
A09 = read(os.path.join(BODY, 'A_09_结果分析.md'))
A02 = read(os.path.join(BODY, 'A_02_摘要.md'))

p('=' * 92)
p('第四轮 · 待核查项交叉核查（实测）')
p('=' * 92)

# ── D-6 灵敏度参数个数
p('\n## D-6 灵敏度覆盖的参数个数')
PARAMS = ['D', 'k', 'rho', '\\rho', 'cp', 'c_p', 'h', 'k_m', 'km', 'E_a', 'R_0', 'C_t', 'T_inf',
          'rho_b', 'phi', 'alpha', '导热', '密度', '比热', '换热', '传质', '扩散', '潜热', '收缩']
hits = []
for q in ['图 11', '龙卷风', '灵敏度']:
    for m in re.finditer(re.escape(q), ALL):
        seg = ALL[max(0, m.start() - 200):m.start() + 400]
        hits.append(seg)
blob = '\n'.join(hits) + A10
found = sorted({q for q in PARAMS if q in blob})
p('  灵敏度段/检验章内出现的候选参数记号：%s' % ('、'.join(found) if found else '(未命中)'))
m = re.findall(r'对\s*[^\n，。]{0,40}?参数', A10)
p('  A_10 中"…参数"表述样例：%s' % ('；'.join(m[:6]) if m else '(无)'))
n = len(re.findall(r'±\s*(?:1|2)?\d+%', A10 + ALL))
p('  文中出现"±n%%"扰动幅度的次数 = %d' % n)
p('  ⟹ 判定：%s（判据 ≥5 个参数 × ±10%%/±20%%）'
  % ('需按上列候选逐项点数确认' if len(found) < 5 else '候选 ≥5，待确认是否逐项做了扰动'))

# ── D-7 误差评价指标
p('\n## D-7 误差评价指标个数')
METRICS = ['误差带', 'GCI', 'Richardson', '观测阶', '收敛阶', '残差', '守恒残差', '偏差',
           'RMSE', 'MAE', 'MAPE', '相对误差', '不确定度', '置信', '覆盖']
cnt = {k: ALL.count(k) for k in METRICS if ALL.count(k)}
p('  命中：%s' % '、'.join('%s×%d' % (k, v) for k, v in cnt.items()))
p('  ⟹ 量化指标类别数 = %d（判据 ≥4）' % len(cnt))

# ── D-10 正文流程图类图件
p('\n## D-10 正文内"流程图／示意图"类图件')
figs = re.findall(r'\\includegraphics\[[^\]]*\]\{([^}]*)\}', ALL)
for f in figs:
    name = f.split('/')[-1].replace('\\_', '_')
    p('    · %s' % name)
flow = [f for f in figs if any(k in f for k in ('流程', '示意', '框架', '关系图', '变换'))]
p('  判定：正文图件 %d 张，其中"流程图／示意／框架"类 **%d 张**（判据：每小问 1 张）'
  % (len(figs), len(flow)))

# ── D-17 ±20% 扰动判定句
p('\n## D-17 「±20% 扰动 → 结论不变」判定句')
pat = re.compile(r'(±\s*20%|±20\\%|20%[^\n]{0,30}(扰动|偏移)|扰动[^\n]{0,30}(结论|排序|稳定|不变))')
mm = pat.findall(ALL)
p('  命中条数 = %d' % len(mm))
for s in re.findall(r'[^\n。]{0,60}(?:±\s*20%|±20\\%)[^\n。]{0,80}', ALL)[:5]:
    p('    · %s' % s.strip()[:130])

# ── D-20 工程/工艺启示段
p('\n## D-20 「工程／工艺启示」段')
for k in ['启示', '工艺', '实际意义', '指导意义', '工程意义', '生产', '建议']:
    p('   %-6s ×%d' % (k, ALL.count(k) + A09.count(k) + A11.count(k)))

# ── D-15 选型"排除式"论证
p('\n## D-15 选型"为何不用其他方法"的排除式论证')
for k in ['不采用', '不选', '而不', '相比之下', '故不', '未采用', '不予']:
    p('   %-6s ×%d（全文 tex）｜A_08 ×%d' % (k, ALL.count(k), A08.count(k)))

# ── 15.1 抄题自查（论文 ↔ 题面）
p('\n## 15.1 抄题自查：论文 ↔ 题面 的最长公共片段')
qp = os.path.join(ROOT, '10_赛题', 'A题', 'A题.pdf')
qtext = ''
if os.path.exists(qp):
    doc = fitz.open(qp)
    qtext = '\n'.join(pg.get_text() for pg in doc)
    doc.close()
    p('  题面 PDF 抽取字符数 = %d' % len(qtext))
else:
    p('  !! 未找到题面 PDF：%s' % qp)


def norm(s):
    """去空白/标点/数学记号，只留汉字与字母数字。"""
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    return re.sub(r'[^0-9A-Za-z\u4e00-\u9fff]', '', s)


PAPER_TXT = norm(re.sub(r'%.*', '', ALL + FRONT + A08 + A09 + A10 + A11))
Q_TXT = norm(qtext)
p('  论文（归一化）字符数 = %d ｜ 题面（归一化）= %d' % (len(PAPER_TXT), len(Q_TXT)))
import difflib
sm = difflib.SequenceMatcher(None, PAPER_TXT, Q_TXT, autojunk=False)
blocks = sorted([b for b in sm.get_matching_blocks() if b.size >= 20],
                key=lambda b: -b.size)[:8]
if blocks:
    for b in blocks:
        p('    · 公共片段长 %d：%s' % (b.size, PAPER_TXT[b.a:b.a + b.size][:110]))
    p('  ⟹ 最长公共片段 = **%d 字**（判据：全文无"大段复制原题"；单句级术语重复属正常）'
      % blocks[0].size)
else:
    p('  ⟹ **未发现长度 ≥20 的公共片段 ⟹ 无复制原题迹象** ✅')

io.open(os.path.join(ROOT, '40_复核', '05_成绩评定', 'temp', '_crosscheck4.txt'),
        'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('\n[留证] 40_复核/05_成绩评定/temp/_crosscheck4.txt')
