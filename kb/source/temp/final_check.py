# -*- coding: utf-8 -*-
"""最终完整性核对：源文件 -> 目标 md 是否齐备，并输出统计报告。"""
import os
import io
import sys

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
DST = os.path.join(BASE, "第一批提取后")
TMP = os.path.join(BASE, "temp")
REPORT = os.path.join(TMP, "最终核对报告.txt")


def scan(ext):
    res = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.startswith("~$"):
                continue
            if f.lower().endswith(ext):
                res.append(os.path.join(dp, f))
    res.sort()
    return res


def main():
    srcs = scan(".docx") + scan(".doc") + scan(".pdf")
    lines = ["源文件总数: %d" % len(srcs), ""]
    miss = []
    ok = []
    for f in srcs:
        rel = os.path.relpath(f, SRC)
        md = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        if os.path.exists(md):
            ok.append((os.path.basename(md), os.path.getsize(md)))
        else:
            miss.append(rel)
    lines.append("已生成: %d" % len(ok))
    lines.append("缺失: %d" % len(miss))
    for m in miss:
        lines.append("  MISSING: " + m)
    lines.append("")
    lines.append("---- 明细（文件名 / 字节）----")
    for name, size in sorted(ok):
        lines.append("%8d  %s" % (size, name))
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(lines))
    print("TOTAL=%d OK=%d MISSING=%d" % (len(srcs), len(ok), len(miss)))


if __name__ == "__main__":
    main()
