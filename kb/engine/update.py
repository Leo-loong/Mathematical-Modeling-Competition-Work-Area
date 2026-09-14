# -*- coding: utf-8 -*-
"""一键增量更新：把新内容拖进 kb/source（任意新文件夹/散文件均可）后运行本脚本。
流程：p2 精修(可选) -> p3 元数据 -> p4 重建索引 -> p5 报告，并输出本次变更摘要。
所有路径由脚本位置动态推导；kb 文件夹整体移动到正式工作目录后无需改代码。

用法：
  python kb\\engine\\update.py                 # 完整更新
  python kb\\engine\\update.py --skip-refine   # 跳过精修（只新增不修旧件时更快）
输出：控制台摘要 + data/update_log.txt（追加）
⚠ 约束：禁止文件系统删除；清理一律移入 source/temp 隔离目录。
"""
import os
import sys
import json
import subprocess
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
WORKSPACE = os.path.dirname(KB)
DATA = os.path.join(HERE, "data")


def run(script):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                       capture_output=True, text=True, creationflags=0x08000000)
    tail = (r.stdout or "").strip().splitlines()
    tail = tail[-1] if tail else ""
    if r.returncode != 0:
        print("!! %s 失败:\n%s" % (script, (r.stderr or "")[-800:]))
        sys.exit(2)
    return tail


def db_counts():
    import sqlite3
    if not os.path.exists(os.path.join(DATA, "catalog.db")):
        return None
    con = sqlite3.connect(os.path.join(DATA, "catalog.db"))
    try:
        n_f = con.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        n_c = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    except sqlite3.OperationalError:
        return None
    finally:
        con.close()
    return n_f, n_c


def json_paths():
    p = os.path.join(DATA, "files.json")
    if not os.path.exists(p):
        return set()
    with open(p, encoding="utf-8") as f:
        return {r["path"] for r in json.load(f)}


def main():
    skip_refine = "--skip-refine" in sys.argv
    log = ["[%s] update start" % datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    before_f = db_counts()
    old_paths = json_paths()

    steps = []
    if not skip_refine:
        steps.append("p2_refine.py")
    steps += ["p3_meta.py", "p4_build_index.py", "p5_report.py"]
    for s in steps:
        tail = run(s)
        log.append("  %s -> %s" % (s, tail))
        print("  [ok] %s %s" % (s, tail))

    new_paths = json_paths()
    added = sorted(new_paths - old_paths)
    removed = sorted(old_paths - new_paths)
    after_f = db_counts()
    log.append("  新增: %d 个文件" % len(added))
    for p in added[:30]:
        log.append("    + %s" % p)
    if len(added) > 30:
        log.append("    ... 其余 %d 个见 files.json" % (len(added) - 30))
    if removed:
        log.append("  移除: %d 个文件" % len(removed))
        for p in removed[:30]:
            log.append("    - %s" % p)
    if before_f and after_f:
        log.append("  索引规模: files %d -> %d, chunks %d -> %d"
                   % (before_f[0], after_f[0], before_f[1], after_f[1]))
    log.append("  完成。检索入口: python kb/engine/p5_search.py <关键词>")
    text = "\n".join(log) + "\n"
    with open(os.path.join(DATA, "update_log.txt"), "a", encoding="utf-8") as f:
        f.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
