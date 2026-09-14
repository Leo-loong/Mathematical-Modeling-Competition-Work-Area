# -*- coding: utf-8 -*-
"""P2 数值三向对账：**PDF 纸面** ↔ 口径总表/溯源对照（登记侧） ↔ 结果文件（真值侧）。

只读；只写 temp/。输出：
  1) 控制台摘要（登记侧 token 数、纸面 token 数、未登记 token 清单）
  2) temp/_数值对账明细.csv
  3) temp/_口径总表_显现值补登记.txt（§十三 原文，供逐条目视）
"""
import os, re, csv, io, sys
import fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')
os.makedirs(TEMP, exist_ok=True)

REG_FILES = [
    (os.path.join(ROOT, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md'), '口径总表'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_数值溯源对照.md'), '溯源对照'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_图表定稿口径表.md'), '图表口径'),
    (os.path.join(ROOT, '20_交付包', '03_假设清单', 'A_假设清单.md'), '假设清单'),
]

# 数据型 token：≥2 位小数（避免把章节号 5.1 / 图号 5-8 误当数据）
DEC = re.compile(r'(?<![\d.])(\d{1,4}\.\d{2,6})(?![\d])')
PCT = re.compile(r'(?<![\d.])(\d{1,3}(?:\.\d{1,4})?)\s*%')


def toks(text):
    s = set(DEC.findall(text))
    s |= set(m + '%' for m in PCT.findall(text))
    return s


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


# ---------- 1) 登记侧 ----------
reg = {}
for path, tag in REG_FILES:
    if os.path.isfile(path):
        for t in toks(read(path)):
            reg.setdefault(t, set()).add(tag)
    else:
        print('⚠ 登记侧缺件：', path)

# ---------- 2) 纸面侧（PDF） ----------
pdf = os.path.join(DELIV, 'main.pdf')
doc = fitz.open(pdf)
paper = {}
noise = re.compile(r'(图|表|式|节|附录|第|参考文献|页)\s*$')
for pno in range(1, doc.page_count + 1):
    txt = doc[pno - 1].get_text()
    for line in txt.split('\n'):
        st = line.strip()
        if not st:
            continue
        for t in toks(st):
            paper.setdefault(t, []).append((pno, st[:90]))

# ---------- 3) 对账 ----------
hit, miss = {}, {}
for t, locs in paper.items():
    (hit if t in reg else miss)[t] = locs

rows = []
for t in sorted(paper, key=lambda x: -len(paper[x])):
    locs = paper[t]
    pages = sorted(set(p for p, _ in locs))
    rows.append(['%s' % t, len(locs), len(pages), ','.join(map(str, pages[:12])),
                 '登记' if t in reg else '未登记', sorted(reg.get(t, [])) and '|'.join(sorted(reg.get(t, []))) or '',
                 locs[0][1]])

with open(os.path.join(TEMP, '_数值对账明细.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['值', '纸面出现次数', '涉及页数', '页号(前12)', '判定', '登记于', '例句'])
    w.writerows(rows)

print('=== P2 数值三向对账（纸面 ↔ 登记侧）===')
print('登记侧 token（不重复）= %d ｜ 纸面数据型 token（不重复）= %d' % (len(reg), len(paper)))
print('★ 纸面 token 命中登记侧 = %d（%.1f%%）｜ **未登记 = %d**'
      % (len(hit), 100.0 * len(hit) / max(1, len(paper)), len(miss)))
print()
print('--- 未登记 token（按出现次数降序，最多 40 条）---')
for t in sorted(miss, key=lambda x: -len(miss[x]))[:40]:
    pgs = sorted(set(p for p, _ in miss[t]))
    print('   %-12s 出现%3d 次  p%s  ｜ %s' % (t, len(miss[t]), ','.join(map(str, pgs[:8])), miss[t][0][1][:64]))

# ---------- 4) §十三 显现值补登记原文 ----------
qs = os.path.join(ROOT, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md')
if os.path.isfile(qs):
    lines = read(qs).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('## 十三')]
    if idx:
        seg = '\n'.join(lines[idx[0]:idx[0] + 60])
        with io.open(os.path.join(TEMP, '_口径总表_显现值补登记.txt'), 'w', encoding='utf-8') as f:
            f.write(seg)
        print()
        print('--- §十三 论文显现值补登记（前 12 行，完整见 temp/_口径总表_显现值补登记.txt）---')
        for l in seg.split('\n')[:12]:
            print('   ' + l[:110])
