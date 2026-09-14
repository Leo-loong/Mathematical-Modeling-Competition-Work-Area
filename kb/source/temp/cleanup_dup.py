# -*- coding: utf-8 -*-
"""按重复清单，把第二批中的重复文件移动到隔离目录（可逆，不删除）。

- 跨批次重复：第一批已有，第二批副本移出
- 内部重复：同组保留 1 份（路径最浅者），其余移出
"""
import os
import io
import csv
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BASE, "temp")
B2 = os.path.join(BASE, "第二批")
QUARANTINE = os.path.join(BASE, "第二批_重复隔离")
CSV_IN = os.path.join(TMP, "重复清单.csv")
REPORT = os.path.join(TMP, "清理报告.txt")


def uniq_dest(dst):
    if not os.path.exists(dst):
        return dst
    root, ext = os.path.splitext(dst)
    i = 1
    while os.path.exists("%s__dup%d%s" % (root, i, ext)):
        i += 1
    return "%s__dup%d%s" % (root, i, ext)


def main():
    dry = "--dry" in sys.argv
    dups = set()
    cross, inner = 0, 0
    with io.open(CSV_IN, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["kind"] == "CROSS":
                dups.add(row["path"])
                cross += 1
            elif row["keep"] == "dup":
                dups.add(row["path"])
                inner += 1

    moved, failed, missing = 0, [], []
    for rel in sorted(dups):
        src = os.path.join(B2, rel)
        if not os.path.exists(src):
            missing.append(rel)
            continue
        dst = uniq_dest(os.path.join(QUARANTINE, rel))
        if dry:
            moved += 1
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            moved += 1
        except Exception as e:
            failed.append((rel, repr(e)))
        if moved % 200 == 0:
            print("moved %d" % moved)

    remain = sum(len(fn) for _dp, _dn, fn in os.walk(B2))
    out = ["# 第二批重复文件清理报告", "",
           "模式: %s" % ("预演(dry-run)" if dry else "实际移动"),
           "跨批次重复(与第一批一致): %d 个" % cross,
           "第二批内部重复(多余副本): %d 个" % inner,
           "实际移动: %d 个" % moved,
           "失败: %d 个" % len(failed),
           "源文件缺失: %d 个" % len(missing),
           "", "隔离目录: %s" % QUARANTINE,
           "第二批剩余文件: %d 个" % remain]
    if failed:
        out.append("")
        out.append("## 失败明细")
        for r, e in failed[:20]:
            out.append("  %s  %s" % (r, e))
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
