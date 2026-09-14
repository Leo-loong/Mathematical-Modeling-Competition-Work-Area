# -*- coding: utf-8 -*-
"""全量复查：Work_Space 下（kb 除外）所有 md 的路径引用检查。
找出：绝对路径、旧目录硬编码（B题/2025国赛真题/2026数学建模）、失效的相对引用。"""
import os, io, re

ROOT = r'c:/Users/wang-/Desktop/2026数学建模/2025国赛真题/B题/Work_Space'
SKIP_DIRS = {'kb', 'temp', 'data', 'figures', 'figures_reference', '_old_db', 'p2_backup'}
BAD_PATTERNS = [
    (r'2025国赛真题', '旧目录:2025国赛真题'),
    (r'B题', '旧目录:B题'),
    (r'2026数学建模(?!国赛)', '旧目录:2026数学建模'),
    (r'[cC]:[/\\]Users', '绝对路径'),
    (r'wang-', '用户名'),
    (r'Desktop', '桌面路径'),
]
issues = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if not f.endswith(('.md', '.py', '.ps1', '.txt')):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT)
        try:
            text = io.open(p, encoding='utf-8').read()
        except Exception:
            text = io.open(p, encoding='utf-8', errors='ignore').read()
        for i, line in enumerate(text.split('\n'), 1):
            for pat, tag in BAD_PATTERNS:
                if re.search(pat, line):
                    issues.append('%s | %s:%d | %s | %s' % (tag, rel, i, f, line.strip()[:110]))

out = os.path.join(ROOT, 'kb', 'source', 'temp', 'path_issues.txt')
io.open(out, 'w', encoding='utf-8').write('\n'.join(issues))
print('issues:', len(issues))
