# -*- coding: utf-8 -*-
"""收尾清理：删除第二批内的空目录，并检查是否还有未解压的压缩包。"""
import os
import io
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B2 = os.path.join(BASE, "第二批")
TMP = os.path.join(BASE, "temp")
REPORT = os.path.join(TMP, "目录清理报告.txt")
ARCH_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".iso"}

log = []


def remove_empty_dirs(root):
    """单次自底向上遍历即可：子目录先判定，父目录后判定（此时已可能变空）。"""
    removed = 0
    for dp, _dn, _fn in os.walk(root, topdown=False):
        if dp == root:
            continue
        try:
            if not os.listdir(dp):
                os.rmdir(dp)
                removed += 1
        except Exception:
            pass
    return removed


def find_archives(root):
    res = []
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            if os.path.splitext(f)[1].lower() in ARCH_EXT:
                res.append(os.path.relpath(os.path.join(dp, f), root))
    return sorted(res)


def main():
    do_delete = "--run" in sys.argv
    before_dirs = sum(len(d) for _d, d, _f in os.walk(B2))
    empty = []
    for dp, dn, fn in os.walk(B2):
        if dp != B2 and not dn and not fn:
            empty.append(os.path.relpath(dp, B2))
    log.append("第二批中空目录: %d 个" % len(empty))
    for e in empty[:20]:
        log.append("  " + e)
    if len(empty) > 20:
        log.append("  ...（共 %d 个）" % len(empty))

    if do_delete:
        n = remove_empty_dirs(B2)
        log.append("已删除空目录: %d 个" % n)

    after_dirs = sum(len(d) for _d, d, _f in os.walk(B2))
    log.append("目录数: %d -> %d" % (before_dirs, after_dirs))

    arch = find_archives(B2)
    log.append("")
    log.append("第二批中剩余压缩包: %d 个" % len(arch))
    for a in arch:
        log.append("  " + a)

    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("EMPTY=%d REMAIN_ARCH=%d" % (len(empty), len(arch)))


if __name__ == "__main__":
    main()
