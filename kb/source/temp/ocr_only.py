# -*- coding: utf-8 -*-
"""ocr_only.py -- 扫描版 PDF 的 OCR 独立一轮（Windows 内置 OCR，zh-Hans-CN）。

输入：temp/b2_ocr_pending.txt（相对「第二批」的路径清单）
流程：并行渲染 PNG -> 多分片 winocr.ps1 -> 组装 Markdown 写入「第二批提取后」
用法：
  python ocr_only.py            # 默认 8 分片、150 DPI
  python ocr_only.py 8 150
"""
import os
import io
import sys
import json
import time
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

TMP = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(TMP)
SRC = os.path.join(SOURCE, "第二批")
DST = os.path.join(SOURCE, "第二批提取后")
# 必须用 winocr.ps1 的自定位默认目录（ocr_png / ocr_tsv）：
# PowerShell 的 -File 传参在中文路径下会乱码，实测传 -PngDir/-TsvDir 后一片 TSV 都出不来。
PNG = os.path.join(TMP, "ocr_png")
TSV = os.path.join(TMP, "ocr_tsv")
PENDING = os.path.join(TMP, "b2_ocr_pending.txt")
PROGRESS = os.path.join(TMP, "ocr_progress.txt")
REPORT = os.path.join(TMP, "第二批OCR报告.txt")

SHARDS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 150
CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008

log = []
_lock = __import__("threading").Lock()


def say(m):
    with _lock:
        log.append("[%s] %s" % (time.strftime("%H:%M:%S"), m))
        print(m)
        try:
            with io.open(PROGRESS, "w", encoding="utf-8") as f:
                f.write("\n".join(log[-60:]))
        except Exception:
            pass


def render_one(args):
    i, rel, dpi = args
    import pymupdf
    p = os.path.join(SRC, rel)
    try:
        d = pymupdf.open(p)
        n = d.page_count
        for pno in range(n):
            out = os.path.join(PNG, "%04d_%04d.png" % (i, pno))
            if os.path.exists(out):
                continue
            try:
                d[pno].get_pixmap(dpi=dpi).save(out)
            except Exception:
                pass
        d.close()
        return (i, rel, n)
    except Exception:
        return (i, rel, 0)


def read_tsv(path):
    rows = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 5:
                rows.append(parts[4])
    return rows


def main():
    t0 = time.time()
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(TSV, exist_ok=True)
    if not os.path.exists(PENDING):
        say("无待 OCR 清单 %s" % PENDING)
        return
    rels = [l.strip() for l in io.open(PENDING, encoding="utf-8") if l.strip()]
    say("待 OCR：%d 个 PDF，DPI=%d，分片=%d" % (len(rels), DPI, SHARDS))

    # 1) 渲染
    meta = []
    with ProcessPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(render_one, (i, rel, DPI)) for i, rel in enumerate(rels)]
        done = 0
        for fu in as_completed(futs):
            i, rel, n = fu.result()
            meta.append((i, rel, n))
            done += 1
            if done % 20 == 0 or done == len(rels):
                say("渲染 %d/%d（累计 %d 页）" % (done, len(rels), sum(m[2] for m in meta)))
    meta.sort()
    total_pages = sum(m[2] for m in meta)
    say("渲染完成：%d 页，耗时 %.1f 分钟，开始 OCR" % (total_pages, (time.time() - t0) / 60.0))
    with io.open(os.path.join(TMP, "ocr2_map.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps([[i, rel, n] for i, rel, n in meta], ensure_ascii=False))

    # 2) OCR 多分片（只加 CREATE_NO_WINDOW：加 DETACHED_PROCESS 会让 PowerShell 起不来）
    procs = []
    for s in range(SHARDS):
        procs.append(subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", os.path.join(TMP, "winocr.ps1"),
             "-Shard", str(s), "-Shards", str(SHARDS)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW))
    for pr in procs:
        pr.wait()
    n_tsv = len([x for x in os.listdir(TSV) if x.endswith(".tsv")]) if os.path.isdir(TSV) else 0
    say("TSV 产出：%d / %d 页" % (n_tsv, total_pages))
    if n_tsv == 0:
        say("!! OCR 无产出，中止组装（检查 powershell 是否被调用）")
        with io.open(REPORT, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
        return
    say("OCR 完成，开始组装（耗时 %.1f 分钟）" % ((time.time() - t0) / 60.0))

    # 3) 组装
    ok = fail = 0
    for i, rel, n in meta:
        lines = []
        for pno in range(n):
            t = os.path.join(TSV, "%04d_%04d.tsv" % (i, pno))
            if os.path.exists(t):
                lines.extend(x for x in read_tsv(t) if x.strip())
        body = "\n".join(lines).strip() + "\n"
        dst = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        if len(body.strip()) < 20:
            fail += 1
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with io.open(dst, "w", encoding="utf-8") as f:
            f.write(body)
        ok += 1
        if ok % 20 == 0:
            say("组装 %d/%d" % (ok, len(meta)))

    say("")
    say("OCR 组装完成：成功 %d，失败 %d，总耗时 %.1f 分钟"
        % (ok, fail, (time.time() - t0) / 60.0))
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("OCR_ONLY DONE ok=%d fail=%d pages=%d" % (ok, fail, total_pages))


if __name__ == "__main__":
    main()
