# -*- coding: utf-8 -*-
"""dedup_md.py -- 「第二批提取后」内部 md 去重（**只在同目录内**去重，不拆散资料组）。

策略（沿用 踩坑指南 §4.5）：
  - 按「去空白后文本 SHA1」分组，仅在同一目录内比较；
  - 保留评分最高的一份（无 (1)/(2)/副本/复件/copy 痕迹 > 文件名更长 > 路径更短）；
  - 其余移入 temp\\第二批_重复md_20260910\\（备份式移动，不用 os.remove）。
跨目录的重复（A/B/C 三套内容近似）**不动**——引擎在检索层按重复组折叠，且拆散资料组代价更大。

用法：
  python dedup_md.py            # 演练
  python dedup_md.py --apply    # 实际移动
"""
import os
import io
import re
import sys
import hashlib
import shutil
from collections import defaultdict

TMP = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(TMP)
AREA = os.path.join(SOURCE, "第二批提取后")
OUT = os.path.join(TMP, "第二批_重复md_20260910")
REPORT = os.path.join(TMP, "第二批md去重报告.txt")

APPLY = "--apply" in sys.argv
BAD_NAME = re.compile(r"\(\d+\)|副本|复件|copy|新建|\(\d\)", re.I)
PAGE_MARK = re.compile(r"<!--\s*第\s*\d+\s*页\s*-->")


def norm_hash(path):
    try:
        raw = open(path, "rb").read()
        t = raw.decode("utf-8", "replace")
    except OSError:
        return None
    t = PAGE_MARK.sub("", t)
    t = re.sub(r"\s+", "", t)
    if not t:
        return None
    return hashlib.sha1(t.encode("utf-8")).hexdigest()


def score(path):
    fn = os.path.basename(path)
    s = 0
    if not BAD_NAME.search(fn):
        s += 100
    s += min(len(fn), 80) // 4
    s -= min(len(path), 300) // 60
    return s


def main():
    groups = defaultdict(list)
    n = 0
    for dp, _dn, fn in os.walk(AREA):
        mds = [os.path.join(dp, f) for f in fn if f.lower().endswith(".md")]
        if not mds:
            continue
        for p in mds:
            n += 1
            h = norm_hash(p)
            if h:
                groups[(dp, h)].append(p)

    moved = 0
    freed = 0
    detail = []
    for (dp, _h), paths in groups.items():
        if len(paths) < 2:
            continue
        paths.sort(key=score, reverse=True)
        keep = paths[0]
        for p in paths[1:]:
            freed += os.path.getsize(p)
            if APPLY:
                rel = os.path.relpath(p, AREA)
                d = os.path.join(OUT, rel)
                os.makedirs(os.path.dirname(d), exist_ok=True)
                try:
                    shutil.move(p, d)
                    moved += 1
                except OSError:
                    continue
            else:
                moved += 1
            detail.append((os.path.relpath(keep, AREA), os.path.relpath(p, AREA)))

    lines = []
    lines.append("第二批提取后 md 去重报告  模式=%s" % ("实际移动 APPLY" if APPLY else "演练 DRY-RUN"))
    lines.append("扫描 md        : %d" % n)
    lines.append("同目录重复组   : %d" % sum(1 for k, v in groups.items() if len(v) > 1))
    lines.append("可精简副本     : %d" % moved)
    lines.append("释放空间       : %.1f MB" % (freed / 1048576.0))
    lines.append("隔离目录       : %s" % OUT)
    lines.append("")
    lines.append("--- 明细（保留 <- 移走）前 80 条 ---")
    for keep, gone in detail[:80]:
        lines.append("  KEEP %s" % keep)
        lines.append("       <- %s" % gone)
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("DEDUP DONE n=%d dup=%d freed=%.1fMB" % (n, moved, freed / 1048576.0))


if __name__ == "__main__":
    main()
