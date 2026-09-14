# -*- coding: utf-8 -*-
"""评估基线冻结与真源漂移巡检（只读）

用途：
  ① `freeze`：对评估对象（素材侧成果）逐文件记录 相对路径|字节数|md5，产出基线指纹清单；
  ② `check` ：重取指纹并与基线比对，报告"漂移/新增/缺失"（评估期间防另一 Agent 并发改真源）。

范围（默认）：
  20_交付包/、30_图表/、11_建模/11-1~11-5 与 大白话讲模型/ 下的
  .md/.tex/.csv/.xlsx/.json/.py/.txt 文件；排除 kb/、99_过程与归档/、root_temp/、rerun_out/、
  40_复核/03_变更报告/ 与 `_*` 临时件。

纪律：只读；不修改任何被扫描文件；产物写入 40_复核/05_成绩评定/temp/。

用法：
  python freeze_baseline.py freeze      # 产出 temp/_baseline_fingerprint.csv
  python freeze_baseline.py check       # 产出 temp/_baseline_drift.txt
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))                 # .../05_成绩评定/code
PKG = os.path.dirname(HERE)                                       # .../05_成绩评定
ROOT = os.path.dirname(os.path.dirname(PKG))                      # 工作区根
TEMP = os.path.join(PKG, 'temp')
BASE_CSV = os.path.join(TEMP, '_baseline_fingerprint.csv')
DRIFT_TXT = os.path.join(TEMP, '_baseline_drift.txt')

SCAN_DIRS = ['20_交付包', '30_图表', '11_建模']
SKIP_PARTS = {'.git', '.codebuddy', '__pycache__', 'kb', '99_过程与归档', 'root_temp',
              'rerun_out', '03_变更报告', 'temp'}
EXTS = {'.md', '.tex', '.csv', '.xlsx', '.json', '.py', '.txt'}
SKIP_PREFIX = ('~$', '_')


def _md5(path, buf=1 << 20):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def iter_files():
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dp, dns, fns in os.walk(base):
            dns[:] = [x for x in dns if x not in SKIP_PARTS and not x.startswith('_')]
            for fn in fns:
                if fn.startswith(SKIP_PREFIX):
                    continue
                if os.path.splitext(fn)[1].lower() not in EXTS:
                    continue
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, ROOT).replace('\\', '/')
                yield rel, full


def freeze():
    os.makedirs(TEMP, exist_ok=True)
    rows = []
    for rel, full in sorted(iter_files()):
        try:
            rows.append((rel, os.path.getsize(full), _md5(full)))
        except OSError as e:                                    # noqa: PERF203
            rows.append((rel, -1, 'ERR:%s' % e))
    with open(BASE_CSV, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['相对路径', '字节数', 'md5'])
        w.writerows(rows)
    print('[FREEZE OK] %d files -> %s' % (len(rows), os.path.relpath(BASE_CSV, ROOT)))
    return 0


def check():
    if not os.path.exists(BASE_CSV):
        print('[CHECK FAIL] 基线不存在，请先 freeze')
        return 2
    with open(BASE_CSV, encoding='utf-8-sig', newline='') as f:
        old = {r['相对路径']: (int(r['字节数']), r['md5']) for r in csv.DictReader(f)}
    now = {}
    for rel, full in iter_files():
        try:
            now[rel] = (os.path.getsize(full), _md5(full))
        except OSError as e:                                    # noqa: PERF203
            now[rel] = (-1, 'ERR:%s' % e)

    changed, added, removed = [], [], []
    for rel, sig in now.items():
        if rel not in old:
            added.append(rel)
        elif old[rel] != sig:
            changed.append('%s  基线=%s/%s  现值=%s/%s' % (rel, old[rel][0], old[rel][1][:8],
                                                          sig[0], sig[1][:8]))
    for rel in old:
        if rel not in now:
            removed.append(rel)

    lines = ['评估基线漂移巡检（只读）',
             '基线文件：%s' % os.path.relpath(BASE_CSV, ROOT),
             '基线计数：%d ｜ 现计数：%d' % (len(old), len(now)),
             '内容变化：%d ｜ 新增：%d ｜ 缺失：%d' % (len(changed), len(added), len(removed)),
             '']
    for title, items in (('== 内容变化 ==', changed), ('== 新增 ==', added), ('== 缺失 ==', removed)):
        lines.append(title)
        lines.extend(('  ' + x) for x in items)
        lines.append('')
    os.makedirs(TEMP, exist_ok=True)
    with open(DRIFT_TXT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('[CHECK] 变化 %d ｜ 新增 %d ｜ 缺失 %d -> %s'
          % (len(changed), len(added), len(removed), os.path.relpath(DRIFT_TXT, ROOT)))
    return 0 if not (changed or added or removed) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['freeze', 'check'])
    a = ap.parse_args()
    return freeze() if a.mode == 'freeze' else check()


if __name__ == '__main__':
    sys.exit(main())
