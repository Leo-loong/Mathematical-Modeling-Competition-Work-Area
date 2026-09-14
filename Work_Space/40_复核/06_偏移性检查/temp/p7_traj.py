# -*- coding: utf-8 -*-
"""P7 纵向漂移：用 `推送留证/` 的 67 个时间戳快照建"版本轴"，定位每次数值变化的轮次。只读。"""
import os, re, io, csv

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
SNAP = os.path.join(ROOT, '40_复核', '03_变更报告', '推送留证')
TEMP = os.path.join(ROOT, '40_复核', '06_偏移性检查', 'temp')

TARGETS = [
    ('口径总表', ['20_交付包/05_数值口径总表/A_数值口径总表.md']),
    ('A08基线', ['50_论文/02_章节稿/基线/A_08_模型建立与求解_基线.md',
                 '50_论文/02_章节稿/A_08_模型建立与求解_基线.md']),
    ('A10基线', ['50_论文/02_章节稿/基线/A_10_模型检验_基线.md',
                 '50_论文/02_章节稿/A_10_模型检验_基线.md']),
    ('写作基线', ['50_论文/02_章节稿/基线/00_全文写作基线.md',
                  '50_论文/02_章节稿/00_全文写作基线.md']),
]
DEC = re.compile(r'(?<![\d.])(\d{1,4}\.\d{2,6})(?![\d])')
PCT = re.compile(r'(?<![\d.])(\d{1,3}(?:\.\d{1,4})?)\s*%')


def toks(text):
    return set(DEC.findall(text)) | set(m + '%' for m in PCT.findall(text))


def read(p):
    with io.open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


snaps = sorted(d for d in os.listdir(SNAP) if os.path.isdir(os.path.join(SNAP, d)))
traj, rows = {}, []
for s in snaps:
    for name, rels in TARGETS:
        for rel in rels:
            p = os.path.join(SNAP, s, rel)
            if os.path.isfile(p):
                t = read(p)
                traj.setdefault(name, []).append((s, len(t), toks(t)))
                break

print('=== P7 版本轴（快照 %d 个）===' % len(snaps))
for name, seq in traj.items():
    print('--- %s：%d 个版本点 ｜ 字符数 %d → %d ｜ token %d → %d'
          % (name, len(seq), seq[0][1], seq[-1][1], len(seq[0][2]), len(seq[-1][2])))
    prev = None
    for s, n, tk in seq:
        if prev is not None:
            add, rm = sorted(tk - prev[2]), sorted(prev[2] - tk)
            if add or rm:
                rows.append([name, prev[0], s, '%+d' % (n - prev[1]),
                             '新增: ' + (','.join(add[:24]) if add else '—'),
                             '消失: ' + (','.join(rm[:24]) if rm else '—')])
                print('   %s → %s（Δ字符 %+d）：新增 %d 个 %s ；消失 %d 个 %s'
                      % (prev[0][-6:], s[-6:], n - prev[1], len(add), add[:8], len(rm), rm[:8]))
        prev = (s, n, tk)

with open(os.path.join(TEMP, '_版本轴漂移.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['对象', '从', '到', 'Δ字符', '新增 token', '消失 token'])
    w.writerows(rows)
print()
print('★ 版本轴变化点 = %d 处 → temp/_版本轴漂移.csv' % len(rows))
