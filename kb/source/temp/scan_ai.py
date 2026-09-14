# -*- coding: utf-8 -*-
"""扫描检索库中所有 AI 主题文件（修正版）：
A = 文件名(basename)命中 AI 词族；B = 仅标题/关键词命中（供人工甄别）。"""
import sqlite3, io, os
from collections import Counter

BASE = r'c:/Users/wang-/Desktop/2026数学建模/2025国赛真题/B题/Work_Space/kb'
DB = os.path.join(BASE, 'engine', 'data', 'catalog.db')
OUT = os.path.join(BASE, 'source', 'temp', 'ai_files.txt')

NAME_WORDS = ['AI', 'Ai', '提示词', 'prompt', 'Prompt', '大模型', 'GPT', 'gpt',
              'DeepSeek', 'deepseek', '智能体', 'AIGC', 'aigc', 'LLM', 'llm',
              'Claude', 'claude', 'Kimi', 'kimi', 'Copilot', 'copilot', '人工智能']
META_WORDS = ['AI', '人工智能', '提示词', '大模型', '智能体', 'AIGC']

con = sqlite3.connect(DB)
cur = con.cursor()
name_hits, meta_hits = set(), set()
for w in NAME_WORDS:
    pat = '%{}%'.format(w)
    for r in cur.execute('SELECT path,kind,nchars FROM files LIMIT 200000'):
        base = r[0].replace('\\', '/').split('/')[-1]
        if w in base:
            name_hits.add(r)
for w in META_WORDS:
    pat = '%{}%'.format(w)
    for r in cur.execute('SELECT path,kind,nchars FROM files WHERE title LIKE ? OR keywords LIKE ? LIMIT 5000', (pat, pat)):
        meta_hits.add(r)

only_meta = sorted(m for m in meta_hits if m not in name_hits)
name_sorted = sorted(name_hits)
con.close()

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write('### A. 文件名命中（%d）\n' % len(name_sorted))
    for path, kind, n in name_sorted:
        f.write('%s\t%s\t%s\n' % (kind, n, path))
    f.write('\n### B. 仅标题/关键词命中（文件名不含 AI 词，%d）\n' % len(only_meta))
    for r in sorted(only_meta, key=lambda x: x[0]):
        f.write('%s\t%s\t%s\n' % (r[1], r[2], r[0]))

ka = Counter(r[1] for r in name_hits)
kb = Counter(r[1] for r in only_meta)
print('A name hits:', len(name_sorted), dict(ka))
print('B meta-only:', len(only_meta), dict(kb))
