# -*- coding: utf-8 -*-
"""清理后复验：第二批是否还有跨批次重复 / 内部重复。"""
import os
import io
import csv
import sys
import hashlib
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BASE, "temp")
B1 = os.path.join(BASE, "第一批")
B2 = os.path.join(BASE, "第二批")
REPORT = os.path.join(TMP, "清理后复验报告.txt")
sys.path.insert(0, TMP)
from dedup_analyze import load, usable_sha, md5_only  # noqa: E402


def main():
    b1 = load(os.path.join(TMP, "idx_b1.csv"), B1)
    b2 = []
    for n in ("v2_doc.csv", "v2_code.csv", "v2_pdf.csv"):
        b2 += load(os.path.join(TMP, n), B2)
    seen = set(r["full"] for r in b2)
    for dp, _dn, fn in os.walk(B2):
        for f in fn:
            if f.startswith("~$"):
                continue
            p = os.path.join(dp, f)
            if p in seen:
                continue
            try:
                b2.append(dict(path=os.path.relpath(p, B2),
                               ext=os.path.splitext(f)[1].lower(),
                               size=os.path.getsize(p), md5=md5_only(p),
                               sha1="", chars=0, note="MD5_ONLY", full=p))
            except Exception:
                pass

    b1_md5 = defaultdict(list)
    b1_sha = defaultdict(list)
    for r in b1:
        b1_md5[r["md5"]].append(r)
        s = usable_sha(r)
        if s:
            b1_sha[s].append(r)

    cross, inner_md5, inner_sha = [], [], []
    g_md5 = defaultdict(list)
    g_sha = defaultdict(list)
    for r in b2:
        g_md5[r["md5"]].append(r)
        s = usable_sha(r)
        if s:
            g_sha[s].append(r)
        if r["md5"] in b1_md5:
            cross.append((r, b1_md5[r["md5"]][0]))
        elif s and s in b1_sha:
            cross.append((r, b1_sha[s][0]))
    for _k, lst in g_md5.items():
        if len(lst) > 1:
            inner_md5.append(lst)
    for _k, lst in g_sha.items():
        if len(lst) > 1 and len(set(x["md5"] for x in lst)) > 1:
            inner_sha.append(lst)

    out = ["# 清理后复验报告", "",
           "第二批剩余文件: %d" % len(b2),
           "第一批文件: %d" % len(b1), "",
           "跨批次剩余重复: %d" % len(cross),
           "第二批内部剩余重复组: %d（MD5 %d 组 / 内容 %d 组）" % (
               len(inner_md5) + len(inner_sha), len(inner_md5), len(inner_sha))]
    for r, o in cross[:30]:
        out.append("  CROSS %s" % r["path"])
    for lst in (inner_md5 + inner_sha)[:30]:
        out.append("  INNER 组:")
        for r in lst[:6]:
            out.append("      %s" % r["path"])
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(out))
    print("REMAIN_B2=%d CROSS=%d INNER=%d" % (
        len(b2), len(cross), len(inner_md5) + len(inner_sha)))


if __name__ == "__main__":
    main()
