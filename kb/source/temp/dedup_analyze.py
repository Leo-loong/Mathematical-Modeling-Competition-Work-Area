# -*- coding: utf-8 -*-
"""查重分析：第二批 vs 第一批（跨批次）+ 第二批内部。

判定口径：
  - MD5 相同  => 字节完全一致（确定重复）
  - SHA1 相同 => 去空白后文本内容一致（内容重复，可能格式/元数据不同）
输出报告: temp/查重报告.txt  +  temp/重复清单.csv
"""
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

IDX_B1 = os.path.join(TMP, "idx_b1.csv")
IDX_B2 = [os.path.join(TMP, n) for n in
          ("idx_b2_doc.csv", "idx_b2_code.csv", "idx_b2_pdf.csv")]
REPORT = os.path.join(TMP, "查重报告.txt")
DUP_CSV = os.path.join(TMP, "重复清单.csv")


MIN_CHARS = 100  # 低于此长度的文本不参与内容指纹比对（空文本哈希会误聚）


def usable_sha(r):
    """只有成功提取到足够文本的文件，其内容指纹才可信。"""
    try:
        if not r.get("sha1") or r["sha1"] == "ERR":
            return None
        if int(r.get("chars") or 0) < MIN_CHARS:
            return None
        if r.get("note") in ("NO_TEXT_LAYER", "DOC_LEGACY", "UNSUPPORTED", "MD5_ONLY"):
            return None
        if str(r.get("note") or "").startswith("SCAN_ERR"):
            return None
        return r["sha1"]
    except Exception:
        return None


def load(path, root):
    out = []
    if not os.path.exists(path):
        return out
    with io.open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["full"] = os.path.join(root, row["path"])
            out.append(row)
    return out


def md5_only(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    b1 = load(IDX_B1, B1)
    b2 = []
    for p in IDX_B2:
        b2 += load(p, B2)

    # 覆盖第二批剩余类型的文件（仅 MD5）
    seen = set(r["full"] for r in b2)
    extra = []
    for dp, _dn, fn in os.walk(B2):
        for f in fn:
            if f.startswith("~$"):
                continue
            p = os.path.join(dp, f)
            if p in seen:
                continue
            try:
                extra.append(dict(path=os.path.relpath(p, B2), ext=os.path.splitext(f)[1].lower(),
                                  size=os.path.getsize(p), md5=md5_only(p),
                                  sha1="", chars=0, note="MD5_ONLY", full=p))
            except Exception:
                pass
    b2 += extra

    # 扩展名分布
    ext_cnt = defaultdict(int)
    for r in b2:
        ext_cnt[r["ext"]] += 1

    # 索引
    b1_md5 = defaultdict(list)
    b1_sha = defaultdict(list)
    b1_name = defaultdict(list)
    for r in b1:
        b1_md5[r["md5"]].append(r)
        s = usable_sha(r)
        if s:
            b1_sha[s].append(r)
        b1_name[os.path.basename(r["path"])].append(r)

    cross_md5, cross_sha, inner_md5, inner_sha, same_name_diff = [], [], [], [], []
    b2_md5 = defaultdict(list)
    b2_sha = defaultdict(list)
    for r in b2:
        b2_md5[r["md5"]].append(r)
        s = usable_sha(r)
        if s:
            b2_sha[s].append(r)

    for r in b2:
        if r["md5"] in b1_md5:
            cross_md5.append((r, b1_md5[r["md5"]][0]))
            continue
        s = usable_sha(r)
        if s and s in b1_sha:
            cross_sha.append((r, b1_sha[s][0]))
        name = os.path.basename(r["path"])
        if name in b1_name:
            same = [x for x in b1_name[name]
                    if x["md5"] == r["md5"] or (s and usable_sha(x) == s)]
            if not same:
                same_name_diff.append((r, b1_name[name][0]))

    for md5, lst in b2_md5.items():
        if len(lst) > 1:
            inner_md5.append(lst)
    for sha, lst in b2_sha.items():
        # md5 不同但文本内容一致：说明是"换了包装"的同一份内容
        if len(lst) > 1 and len(set(x["md5"] for x in lst)) > 1:
            inner_sha.append(lst)

    # 报告
    out = []
    out.append("# 第二批查重报告")
    out.append("")
    out.append("第二批文件总数: %d" % len(b2))
    out.append("第一批文件总数: %d" % len(b1))
    out.append("")
    out.append("## 第二批扩展名分布（前20）")
    for ext, c in sorted(ext_cnt.items(), key=lambda kv: -kv[1])[:20]:
        out.append("  %-8s %d" % (ext or "(无扩展名)", c))
    out.append("")
    out.append("## 一、跨批次重复（第二批 == 第一批）")
    out.append("  字节完全一致(MD5): %d 个" % len(cross_md5))
    out.append("  内容一致(MD5不同但去空白文本相同): %d 个" % len(cross_sha))
    out.append("")
    out.append("## 二、第二批内部重复")
    out.append("  字节完全一致分组: %d 组，涉及 %d 个文件" % (
        len(inner_md5), sum(len(g) for g in inner_md5)))
    out.append("  内容一致(字节不同)分组: %d 组，涉及 %d 个文件" % (
        len(inner_sha), sum(len(g) for g in inner_sha)))
    out.append("")
    out.append("## 三、与第一批次同名但内容不同")
    out.append("  共 %d 个" % len(same_name_diff))
    for r, o in same_name_diff[:40]:
        out.append("  - %s  (第一批: %s)" % (r["path"], o["path"]))
    out.append("")
    out.append("## 三·补充：第二批内部「字节不同但文本内容一致」的分组明细")
    for i, lst in enumerate(inner_sha, 1):
        out.append("  组%d（%d 个文件，chars=%s）:" % (i, len(lst), lst[0].get("chars")))
        for r in lst[:12]:
            out.append("      %s" % r["path"])
        if len(lst) > 12:
            out.append("      ...（另 %d 个）" % (len(lst) - 12))
    out.append("")
    out.append("## 四、跨批次重复明细（前60条）")
    for r, o in (cross_md5 + cross_sha)[:60]:
        kind = "MD5" if (r, o) in [(a, b) for a, b in cross_md5] else "TEXT"
        out.append("  [%s] %s" % (kind, r["path"]))
        out.append("        == 第一批: %s" % o["path"])
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(out))

    # 重复清单（用于清理）
    with io.open(DUP_CSV, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["group", "kind", "keep", "path", "dup_with"])
        gid = 0
        for r, o in cross_md5 + cross_sha:
            gid += 0
            w.writerow(["CROSS", "CROSS", "b1", r["path"], o["path"]])
        for lst in inner_md5 + inner_sha:
            gid += 1
            keep = sorted(lst, key=lambda x: (len(x["path"].split(os.sep)), x["path"]))[0]
            for r in lst:
                w.writerow([gid, "INNER", "keep" if r is keep else "dup",
                            r["path"], keep["path"]])
    print("CROSS=%d INNER_GROUPS=%d SAME_NAME_DIFF=%d TOTAL_B2=%d" % (
        len(cross_md5) + len(cross_sha), len(inner_md5) + len(inner_sha),
        len(same_name_diff), len(b2)))


if __name__ == "__main__":
    main()
