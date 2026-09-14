# -*- coding: utf-8 -*-
"""P1 统一扫描建档：全源清单 + 文本哈希重复分组 + 质量标签。
只读扫描，不修改任何源文件。
⚠ 约束：本引擎任何脚本禁止用 os.remove / shutil.rmtree 删除语料或索引文件
  （会触发环境安全删除保护导致进程异常）；需要清理时一律移动到 source/temp 隔离目录。
输出到 kb/engine/data/：
  p1_inventory.csv   全量清单
  p1_dup_groups.csv  重复组（文本级归并）
  p1_summary.txt     统计摘要（UTF-8）
"""
import os
import csv
import re
import sys
import hashlib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
WORKSPACE = os.path.dirname(KB)  # 所有路径由此动态推导，kb 可整体移动
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)
from p3_meta import discover_areas, DOC_EXTS  # noqa: E402  语料区发现与 doc 类型口径统一

EXCLUDE_DIR_NAMES = {"_无效内容"}
TEXT_EXTS = {".md", ".m", ".M", ".py", ".c", ".h", ".cpp", ".txt", ".html",
             ".csv", ".json", ".cls", ".bst", ".bib", ".dat", ".sas", ".sty"}
CODE_EXTS = {".m", ".M", ".py", ".c", ".h", ".cpp"}
MD_EXTS = {".md"}
PAGE_MARK = re.compile(r"<!--\s*第\s*\d+\s*页\s*-->")
WS_RE = re.compile(r"\s+")
HEAD_RE = re.compile(r"^#{1,6}\s+", re.M)


def read_text_best(path):
    """按 utf-8 -> gbk 顺序尝试读取，返回 (text, encoding)。"""
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "replace"


def raw_hash(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def md_norm_hash(text):
    """md 文本级哈希：去页码注释 + 去空白，识别'内容相同'的重复。"""
    t = PAGE_MARK.sub("", text)
    t = WS_RE.sub("", t)
    return hashlib.sha1(t.encode("utf-8")).hexdigest() if t else ""


def md_title(text):
    m = re.search(r"^#{1,4}\s+(.+)$", text, re.M)
    if m:
        return m.group(1).strip()[:120]
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s[:120]
    return ""


def main():
    os.makedirs(DATA, exist_ok=True)
    rows = []
    n_files = 0
    for area, base in discover_areas():
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIR_NAMES]
            for fn in filenames:
                n_files += 1
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, WORKSPACE).replace("\\", "/")
                ext = os.path.splitext(fn)[1].lower()
                try:
                    size = os.path.getsize(full)
                except OSError:
                    size = -1
                kind, text_sha1, nchars = "asset", "", ""
                title, n_head, enc = "", "", ""
                if ext in TEXT_EXTS:
                    kind = "md" if ext in MD_EXTS else ("code" if ext in CODE_EXTS else "text")
                    try:
                        text, enc = read_text_best(full)
                        nchars = len(text)
                        if kind == "md":
                            title = md_title(text)
                            n_head = len(HEAD_RE.findall(text))
                            text_sha1 = md_norm_hash(text)
                        elif size <= 2 * 1024 * 1024:
                            text_sha1 = "raw:" + raw_hash(full)
                    except Exception as e:
                        kind, enc = "asset", "ERR:%s" % type(e).__name__
                elif ext in DOC_EXTS:
                    kind = "doc"  # 二进制文献：文件名级注册，与 p3 口径一致
                    title = fn
                rows.append({
                    "relpath": rel, "area": area, "ext": ext, "kind": kind,
                    "size": size, "nchars": nchars, "enc": enc,
                    "n_headings": n_head, "title": title, "hash": text_sha1,
                    "dup_group": "",
                })
        print("scanned area: %s (total %d files)" % (area, n_files))

    # 重复分组
    by_hash = defaultdict(list)
    for i, r in enumerate(rows):
        if r["hash"]:
            by_hash[r["hash"]].append(i)
    gid = 0
    for h, idxs in by_hash.items():
        if len(idxs) > 1:
            gid += 1
            for i in idxs:
                rows[i]["dup_group"] = "G%04d" % gid

    inv_csv = os.path.join(DATA, "p1_inventory.csv")
    with open(inv_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    dup_csv = os.path.join(DATA, "p1_dup_groups.csv")
    with open(dup_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["group", "n_members", "members"])
        for h, idxs in sorted(by_hash.items(), key=lambda kv: -len(kv[1])):
            if len(idxs) > 1:
                w.writerow([rows[idxs[0]]["dup_group"], len(idxs),
                            " || ".join(rows[i]["relpath"] for i in idxs)])

    # 摘要
    kind_count, ext_count, md_quality = defaultdict(int), defaultdict(int), defaultdict(int)
    dup_members = 0
    for r in rows:
        kind_count[r["kind"]] += 1
        ext_count[r["ext"]] += 1
        if r["dup_group"]:
            dup_members += 1
        if r["kind"] == "md":
            try:
                nc = int(r["nchars"])
            except (TypeError, ValueError):
                nc = 0
            tag = "C_lowinfo" if nc < 500 else ("B_short" if nc < 2000 else "A_full")
            md_quality[tag] += 1
    rep = ["# P1 扫描摘要\n",
           "- 扫描文件总数: %d" % n_files,
           "- 按类型: " + ", ".join("%s=%d" % kv for kv in sorted(kind_count.items())),
           "- md 质量分布(按字符数): " + ", ".join("%s=%d" % kv for kv in sorted(md_quality.items())),
           "- 重复组数: %d，涉及成员文件: %d" % (gid, dup_members),
           "- Top 扩展名: " + ", ".join("%s=%d" % kv for kv in
                                        sorted(ext_count.items(), key=lambda kv: -kv[1])[:15]),
           "- 清单: %s" % inv_csv,
           "- 重复组: %s" % dup_csv]
    with open(os.path.join(DATA, "p1_summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("P1 done. inventory=%d rows, dup_groups=%d" % (len(rows), gid))


if __name__ == "__main__":
    main()
