# -*- coding: utf-8 -*-
"""重复判定审计：重点排查「版本差异」风险。

分组口径与清理时一致，然后分类：
  A 类 = MD5 完全一致（字节级相同，绝对安全）
  B 类 = MD5 不同但去空白文本 SHA1 相同（疑似同内容不同格式/版本，需关注）
  C 类 = 文件名相同但大小不同，且未被判为重复（版本差异，需人工确认）

输出: temp/重复判定审计报告.txt
"""
import os
import io
import re
import sys
import hashlib
from collections import defaultdict

TMP = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TMP)
B2 = os.path.join(BASE, "第二批")
QUAR = os.path.join(BASE, "第二批_重复隔离")
PROGRESS = os.path.join(TMP, "audit_progress.txt")
REPORT = os.path.join(TMP, "重复判定审计报告.txt")
MIN_CHARS = 100

sys.path.insert(0, TMP)
import scan_index as si  # noqa: E402

log = []


def say(m):
    log.append(m)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as fp:
            fp.write("\n".join(log[-20:]))
    except Exception:
        pass


def usable(r):
    if not r["sha1"]:
        return None
    if r["chars"] < MIN_CHARS:
        return None
    if r["note"] in ("NO_TEXT_LAYER", "DOC_LEGACY", "UNSUPPORTED", "MD5_ONLY"):
        return None
    return r["sha1"]


def scan_root(root, tag):
    rows = []
    n = 0
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            if f.startswith("~$"):
                continue
            p = os.path.join(dp, f)
            try:
                md5 = si.file_md5(p)
                size = os.path.getsize(p)
            except Exception:
                continue
            rows.append(dict(tag=tag, rel=os.path.relpath(p, root), md5=md5,
                             sha1="", chars=0, note="", size=size,
                             name=os.path.basename(f)))
            n += 1
            if n % 5000 == 0:
                say("扫描 %s: %d" % (tag, n))
    say("扫描完成 %s: %d" % (tag, n))
    return rows


def main():
    rows = scan_root(B2, "b2") + scan_root(QUAR, "quar")
    say("纳入文件: %d" % len(rows))

    # 同一 md5 只提取一次文本
    by_md5 = defaultdict(list)
    for r in rows:
        by_md5[r["md5"]].append(r)
    say("唯一 md5: %d" % len(by_md5))
    for i, (_md5, lst) in enumerate(by_md5.items(), 1):
        # 只为「文本类且有可能是 B 类」提取内容：全部提取（保证与清理时一致）
        rep = lst[0]
        root = B2 if rep["tag"] == "b2" else QUAR
        p = os.path.join(root, rep["rel"])
        ext = os.path.splitext(p)[1].lower()
        try:
            text, note = si.extract(p, ext)
            norm = re.sub(r"\s+", "", text)
            sha1 = hashlib.sha1(norm.encode("utf-8", "ignore")).hexdigest()
            chars = len(text)
        except Exception as e:
            sha1, chars, note = "", 0, "ERR %s" % e
        for r in lst:
            r["sha1"] = sha1
            r["chars"] = chars
            r["note"] = note
        if i % 3000 == 0:
            say("文本提取 %d/%d" % (i, len(by_md5)))

    # A 类：md5 组（>1）
    a_groups = [g for g in by_md5.values() if len(g) > 1]
    # B 类：sha1 相同但 md5 不同
    by_sha = defaultdict(list)
    for g in a_groups:
        s = usable(g[0])
        if s:
            by_sha[s].append(g)
    b_groups = []
    for s, glist in by_sha.items():
        flat = [r for g in glist for r in g]
        if len(set(r["md5"] for r in flat)) > 1:
            b_groups.append(flat)
    # 也考虑单 md5 组内成员（md5 相同不可能是 B）；B 只来自跨 md5

    say("A 类（MD5 一致）组数: %d" % len(a_groups))
    say("B 类（文本一致但字节不同）组数: %d" % len(b_groups))

    # C 类：同名不同大小
    by_name = defaultdict(list)
    for r in rows:
        by_name[r["name"]].append(r)
    c_list = []
    for name, lst in by_name.items():
        sizes = set(r["size"] for r in lst)
        if len(sizes) > 1:
            c_list.append((name, lst))

    out = []
    out.append("# 重复判定审计报告")
    out.append("")
    out.append("第二批文件: %d，隔离区文件: %d，纳入审计: %d" % (
        sum(1 for r in rows if r["tag"] == "b2"),
        sum(1 for r in rows if r["tag"] == "quar"), len(rows)))
    out.append("")
    out.append("## 一、A 类：MD5 完全一致（字节级相同，判定绝对可靠）")
    out.append("  组数 %d" % len(a_groups))
    out.append("  说明：同一 MD5 意味着文件二进制内容完全相同，不存在版本差异。")
    out.append("")
    out.append("## 二、B 类：文本一致但字节不同（★ 需重点核查版本差异 ★）")
    out.append("  组数 %d" % len(b_groups))
    out.append("  说明：去空白后文本完全相同，但文件大小/二进制不同，")
    out.append("        可能来自不同格式导出（docx/版本另存），也可能存在细微修订差异。")
    out.append("")
    for i, g in enumerate(b_groups[:200], 1):
        keep = [r for r in g if r["tag"] == "b2"]
        dups = [r for r in g if r["tag"] == "quar"]
        if not keep:
            out.append("  [组%d] 无保留项（异常）" % i)
            continue
        k = keep[0]
        sizes = sorted(set(r["size"] for r in g))
        out.append("  [组%d] %s" % (i, os.path.basename(k["rel"])))
        out.append("        保留: %s  (%d bytes)" % (k["rel"], k["size"]))
        for d in dups[:4]:
            out.append("        移走: %s  (%d bytes)" % (d["rel"], d["size"]))
        out.append("        大小集合: %s  差异: %d bytes" % (
            sizes, (sizes[-1] - sizes[0]) if len(sizes) > 1 else 0))
    if len(b_groups) > 200:
        out.append("  ...（仅列出前 200 组，共 %d 组）" % len(b_groups))
    out.append("")
    out.append("## 三、C 类：文件名相同但大小不同（未被判为重复，疑似版本差异）")
    out.append("  共 %d 组" % len(c_list))
    for name, lst in c_list[:150]:
        out.append("  %s" % name)
        for r in sorted(lst, key=lambda x: x["size"])[:5]:
            out.append("      %8d  [%s] %s" % (r["size"], r["tag"], r["rel"]))
    if len(c_list) > 150:
        out.append("  ...（共 %d 组）" % len(c_list))

    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log + [""] + out))
    print("AUDIT DONE A=%d B=%d C=%d" % (len(a_groups), len(b_groups), len(c_list)))


if __name__ == "__main__":
    main()
