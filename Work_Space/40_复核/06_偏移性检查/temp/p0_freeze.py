# -*- coding: utf-8 -*-
"""P0 冻结检查基准：为锚点与交付件生成 SHA-256 指纹清单（**只读**，只写 temp/）。"""
import hashlib, os, csv
from collections import Counter

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
SUP = os.path.join(ROOT, '50_论文', '04_交排版成图方', '支撑材料')
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')
BASE = os.path.join(ROOT, '50_论文', '02_章节稿', '基线')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')
os.makedirs(TEMP, exist_ok=True)

rows = []


def add(path, tag):
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        st = os.stat(path)
        rows.append((tag, os.path.relpath(path, ROOT), st.st_size, int(st.st_mtime), h))


def add_dir(d, tag, exts=None):
    if not os.path.isdir(d):
        return
    for dirpath, _, files in os.walk(d):
        for fn in sorted(files):
            if exts is None or os.path.splitext(fn)[1].lower() in exts:
                add(os.path.join(dirpath, fn), tag)


add_dir(DELIV, '交付件·论文', {'.tex', '.pdf'})
add_dir(os.path.join(DELIV, 'frontmatter'), '交付件·前置', {'.tex'})
add(os.path.join(SUP, 'AI工具使用详情.pdf'), '交付件·支撑')
add_dir(BODY, '成文', {'.md'})
add_dir(BASE, '基线', {'.md'})
for p, tag in [
    (os.path.join(ROOT, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md'), '锚·数值口径'),
    (os.path.join(ROOT, '20_交付包', '03_假设清单', 'A_假设清单.md'), '锚·假设'),
    (os.path.join(ROOT, '11_建模', '11-1_题目分析', 'A_语义基线.md'), '锚·语义'),
    (os.path.join(ROOT, '50_论文', '01_写作计划', 'A_写作口径与用语约定.md'), '锚·写作契约'),
    (os.path.join(ROOT, '50_论文', '02_章节稿', '基线', '00_全文写作基线.md'), '锚·写作契约'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_数值溯源对照.md'), '锚·溯源'),
    (os.path.join(ROOT, '50_论文', '03_对照与索引', 'A_图表定稿口径表.md'), '锚·图表口径'),
]:
    add(p, tag)
add_dir(os.path.join(ROOT, '20_交付包', '09_代码与复现', 'code'), '代码', {'.py'})
add_dir(os.path.join(ROOT, '20_交付包', '09_代码与复现', 'results'), '结果', None)

out = os.path.join(TEMP, '_基准指纹.csv')
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['tag', 'path', 'bytes', 'mtime', 'sha256'])
    w.writerows(rows)

print('★ 指纹清单 →', out)
print('★ 合计 %d 件' % len(rows))
for k, v in sorted(Counter(r[0] for r in rows).items()):
    print('   %-12s %4d 件' % (k, v))
