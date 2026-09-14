# -*- coding: utf-8 -*-
"""P2b 数值对账（**归一化** ＋ 正文侧限定）：剔除"格式差异"与"附录代码常量"两类假偏移。

归一化：`52%` ↔ `0.52`；尾零（`1.00` ↔ `1`）；有效位（`1.7662` ↔ `1.766193` 不做跨位匹配，
只做**同值不同写法**）；科学计数（`3.678e1` ↔ `36.78`）。
"""
import os, re, io, csv, fitz

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')
REG_FILES = [
    (os.path.join(ROOT, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md'), '口径总表'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_数值溯源对照.md'), '溯源对照'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_图表定稿口径表.md'), '图表口径'),
    (os.path.join(ROOT, '20_交付包', '03_假设清单', 'A_假设清单.md'), '假设清单'),
]
DEC = re.compile(r'(?<![\d.])(\d{1,4}\.\d{2,6})(?![\d])')
PCT = re.compile(r'(?<![\d.])(\d{1,3}(?:\.\d{1,4})?)\s*%')
SCI = re.compile(r'(?<![\d.])(\d{1,3}\.\d{1,4})[eE]([−\-+]?\d{1,2})')


def canon(tok):
    s = {tok}
    t, pct = tok, False
    if t.endswith('%'):
        pct, t = True, t[:-1]
    try:
        v = float(t)
    except ValueError:
        return s
    for f in ('{:.6g}', '{:.5f}', '{:.4f}', '{:.3f}', '{:.2f}', '{:.1f}', '{:.0f}'):
        s.add(f.format(v))
    if pct:
        w = v / 100.0
        for f in ('{:.6g}', '{:.5f}', '{:.4f}', '{:.3f}', '{:.2f}', '{:.1f}'):
            s.add(f.format(w))
        s.add('%g' % v)
    return s


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def toks(text):
    out = set(DEC.findall(text)) | set(m + '%' for m in PCT.findall(text))
    for m, e in SCI.findall(text):
        try:
            out.add('%.6g' % (float(m) * (10 ** float(e.replace('−', '-')))))
        except Exception:
            pass
    return out


reg_canon = {}
for path, tag in REG_FILES:
    if os.path.isfile(path):
        for t in toks(read(path)):
            for c in canon(t):
                reg_canon.setdefault(c, set()).add(tag)

doc = fitz.open(os.path.join(DELIV, 'main.pdf'))


def scan(lo, hi):
    d = {}
    for pno in range(lo, min(hi, doc.page_count) + 1):
        for line in doc[pno - 1].get_text().split('\n'):
            st = line.strip()
            if not st:
                continue
            for t in toks(st):
                d.setdefault(t, []).append((pno, st[:88]))
    return d


body = scan(1, 31)          # 摘要 ＋ 正文
appx = scan(32, doc.page_count)   # 附录（含 B.1–B.12 代码 与 表 A-1 / C）

print('=== P2b 归一化对账 ===')
print('登记侧范式 token = %d ｜ 正文侧数据型 token = %d ｜ 附录侧 = %d'
      % (len(reg_canon), len(body), len(appx)))

for name, d in (('正文＋摘要（p1–31）', body), ('附录（p32+）', appx)):
    un = [t for t in d if not (canon(t) & set(reg_canon))]
    print('★ %s：未登记 %d / %d（%.1f%%）' % (name, len(un), len(d), 100.0 * len(un) / max(1, len(d))))

rows = []
for t, locs in sorted(body.items(), key=lambda kv: -len(kv[1])):
    ok = bool(canon(t) & set(reg_canon))
    rows.append([t, len(locs), ','.join(str(p) for p, _ in locs[:10]), '登记' if ok else '**未登记**', locs[0][1]])
with open(os.path.join(TEMP, '_数值对账_正文侧.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['值', '出现次数', '页号', '判定', '例句'])
    w.writerows(rows)

print()
print('--- 正文＋摘要侧 **未登记** 明细（按次数降序，全部列出）---')
un = sorted([t for t in body if not (canon(t) & set(reg_canon))], key=lambda x: -len(body[x]))
for t in un:
    pgs = sorted(set(p for p, _ in body[t]))
    print('   %-12s ×%-3d p%-14s %s' % (t, len(body[t]), ','.join(map(str, pgs[:6])), body[t][0][1][:66]))
print()
print('（附录侧未登记 %d 个中，p46–190 为附录 B **代码常量**，按设计**不纳入**口径登记）'
      % len([t for t in appx if not (canon(t) & set(reg_canon))]))
