# -*- coding: utf-8 -*-
"""第二批查重清理一键流水线（排除正在下载的目录）。

流程: 分批扫描 -> 建指纹 -> 跨批次/内部查重 -> 重复文件移动到隔离目录
用法: python dedup_pipeline.py
进度: temp/pipeline_progress.txt   报告: temp/第二批查重清理报告.txt
"""
import os
import io
import re
import csv
import sys
import shutil
import hashlib
from collections import defaultdict

TMP = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TMP)
B1 = os.path.join(BASE, "第一批")
B2 = os.path.join(BASE, "第二批")
QUAR = os.path.join(BASE, "第二批_重复隔离")
PROGRESS = os.path.join(TMP, "pipeline_progress.txt")
REPORT = os.path.join(TMP, "第二批查重清理报告.txt")

# 需要跳过的目录关键字（逗号分隔）；环境变量为空表示全量处理
EXCLUDE = [k for k in (os.environ.get("KB_SKIP") or "").split(",") if k]
MIN_CHARS = 100
BATCHES = [
    ("文档", ("docx", "doc", "txt", "md")),
    ("PDF", ("pdf",)),
    ("代码", ("m", "py", "c", "cpp", "h", "java", "r", "jl", "mat", "ipynb")),
]

sys.path.insert(0, TMP)
import scan_index as si  # noqa: E402

log = []


def say(msg):
    log.append(msg)
    print(msg)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as fp:
            fp.write("\n".join(log[-30:]))
    except Exception:
        pass


def excluded(path):
    return any(k in path for k in EXCLUDE)


def build_index():
    rows = []
    for tag, exts in BATCHES:
        ext_set = set("." + e.lower() for e in exts)
        n = 0
        for dp, _dn, fn in os.walk(B2):
            if excluded(dp):
                continue
            for f in fn:
                if f.startswith("~$"):
                    continue
                ext = os.path.splitext(f)[1].lower()
                if ext not in ext_set:
                    continue
                p = os.path.join(dp, f)
                try:
                    text, note = si.extract(p, ext)
                    norm = re.sub(r"\s+", "", text)
                    rows.append(dict(
                        path=os.path.relpath(p, B2), ext=ext,
                        size=os.path.getsize(p), md5=si.file_md5(p),
                        sha1=hashlib.sha1(norm.encode("utf-8", "ignore")).hexdigest(),
                        chars=len(text), note=note))
                    n += 1
                except Exception as e:
                    rows.append(dict(path=os.path.relpath(p, B2), ext=ext,
                                     size=-1, md5="ERR", sha1="ERR",
                                     chars=0, note="ERR %s" % (e,)))
        say("批次[%s] 扫描完成: %d 个" % (tag, n))
    # 其余类型：仅 MD5
    seen = set(os.path.join(B2, r["path"]) for r in rows)
    extra = 0
    for dp, _dn, fn in os.walk(B2):
        if excluded(dp):
            continue
        for f in fn:
            if f.startswith("~$"):
                continue
            p = os.path.join(dp, f)
            if p in seen:
                continue
            try:
                rows.append(dict(path=os.path.relpath(p, B2),
                                 ext=os.path.splitext(f)[1].lower(),
                                 size=os.path.getsize(p), md5=si.file_md5(p),
                                 sha1="", chars=0, note="MD5_ONLY"))
                extra += 1
            except Exception:
                pass
    say("其余类型(MD5 only): %d 个" % extra)
    say("第二批纳入统计: %d 个" % len(rows))
    return rows


def load_b1():
    out = []
    p = os.path.join(TMP, "idx_b1.csv")
    if not os.path.exists(p):
        return out
    with io.open(p, encoding="utf-8-sig") as f:
        out = list(csv.DictReader(f))
    for r in out:
        r["chars"] = int(r.get("chars") or 0)
    return out


def usable(r):
    try:
        if not r.get("sha1") or r["sha1"] == "ERR":
            return None
        if int(r.get("chars") or 0) < MIN_CHARS:
            return None
        if r.get("note") in ("NO_TEXT_LAYER", "DOC_LEGACY", "UNSUPPORTED", "MD5_ONLY"):
            return None
        return r["sha1"]
    except Exception:
        return None


def uniq_dest(dst):
    if not os.path.exists(dst):
        return dst
    root, ext = os.path.splitext(dst)
    i = 1
    while os.path.exists("%s__dup%d%s" % (root, i, ext)):
        i += 1
    return "%s__dup%d%s" % (root, i, ext)


def main():
    b1 = load_b1()
    b2 = build_index()

    b1_md5 = defaultdict(list)
    b1_sha = defaultdict(list)
    for r in b1:
        b1_md5[r["md5"]].append(r)
        s = usable(r)
        if s:
            b1_sha[s].append(r)

    g_md5 = defaultdict(list)
    g_sha = defaultdict(list)
    for r in b2:
        g_md5[r["md5"]].append(r)
        s = usable(r)
        if s:
            g_sha[s].append(r)

    dups = set()
    cross = 0
    for r in b2:
        if r["md5"] in b1_md5:
            dups.add(r["path"])
            cross += 1
            continue
        s = usable(r)
        if s and s in b1_sha:
            dups.add(r["path"])
            cross += 1
    say("跨批次重复(与第一批一致): %d 个" % cross)

    inner = 0
    for _k, lst in g_md5.items():
        if len(lst) > 1:
            keep = sorted(lst, key=lambda x: (len(x["path"].split(os.sep)), x["path"]))[0]
            for r in lst:
                if r is keep:
                    continue
                if r["path"] not in dups:
                    inner += 1
                dups.add(r["path"])
    for _k, lst in g_sha.items():
        if len(lst) > 1 and len(set(x["md5"] for x in lst)) > 1:
            keep = sorted(lst, key=lambda x: (len(x["path"].split(os.sep)), x["path"]))[0]
            for r in lst:
                if r is keep:
                    continue
                if r["path"] not in dups:
                    inner += 1
                dups.add(r["path"])
    say("第二批内部重复(多余副本): %d 个" % inner)
    say("合计待移出: %d 个" % len(dups))

    moved = failed = 0
    for i, rel in enumerate(sorted(dups), 1):
        src = os.path.join(B2, rel)
        if not os.path.exists(src):
            continue
        dst = uniq_dest(os.path.join(QUAR, rel))
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            moved += 1
        except Exception:
            failed += 1
        if moved % 500 == 0:
            say("已移出 %d / %d" % (moved, len(dups)))
    say("移动完成: 成功 %d，失败 %d" % (moved, failed))

    remain = 0
    for dp, _dn, fn in os.walk(B2):
        if excluded(dp):
            continue
        remain += len(fn)
    say("第二批（排除下载中目录）剩余文件: %d" % remain)
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("PIPELINE DONE")


if __name__ == "__main__":
    main()
