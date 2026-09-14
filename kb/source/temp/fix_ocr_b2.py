# -*- coding: utf-8 -*-
"""补救第二批 OCR：改用 winocr.ps1 自定位的默认目录（避免中文路径传参乱码）。

步骤：1) 把已渲染的 PNG 移入 temp\ocr_png
      2) 分片并行调用 winocr.ps1（不传 PngDir/TsvDir，用脚本默认目录）
      3) 按 b2_ocr_map.json 组装 Markdown
"""
import os
import io
import sys
import json
import shutil
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "第二批")
DST = os.path.join(BASE, "第二批提取后")
TMP = os.path.join(BASE, "temp")
PNG_SRC = os.path.join(TMP, "b2_png")
PNG = os.path.join(TMP, "ocr_png")
TSV = os.path.join(TMP, "ocr_tsv")
MAP = os.path.join(TMP, "b2_ocr_map.json")
PROGRESS = os.path.join(TMP, "b2_fix_progress.txt")

log = []


def say(m):
    log.append(m)
    print(m)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as fp:
            fp.write("\n".join(log[-30:]))
    except Exception:
        pass


def main():
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(TSV, exist_ok=True)
    # 1) 迁移已渲染的 PNG 到默认目录
    n = 0
    if os.path.isdir(PNG_SRC):
        for f in os.listdir(PNG_SRC):
            s = os.path.join(PNG_SRC, f)
            d = os.path.join(PNG, f)
            if not os.path.exists(d):
                shutil.move(s, d)
                n += 1
    say("移入 PNG: %d 个（目录内共 %d）" % (n, len(os.listdir(PNG))))

    # 2) 分片 OCR
    shards = 4
    procs = []
    for s in range(shards):
        procs.append(subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", os.path.join(TMP, "winocr.ps1"),
             "-Shard", str(s), "-Shards", str(shards)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            # 只加 CREATE_NO_WINDOW；加 DETACHED_PROCESS 会让 PowerShell 起不来
            creationflags=0x08000000))
    for i, pr in enumerate(procs):
        pr.wait()
        say("OCR 分片 %d 完成" % i)
    say("TSV 数量: %d" % len([x for x in os.listdir(TSV) if x.endswith(".tsv")]))

    # 3) 组装
    meta = json.load(io.open(MAP, encoding="utf-8"))
    files, counts = meta["files"], meta["counts"]
    for i, (rel, cnt) in enumerate(zip(files, counts)):
        lines = []
        for pno in range(cnt):
            t = os.path.join(TSV, "%04d_%04d.tsv" % (i, pno))
            if not os.path.exists(t):
                continue
            with io.open(t, encoding="utf-8") as fp:
                for line in fp:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 5 and parts[4].strip():
                        lines.append(parts[4].strip())
        body = "\n".join(lines).strip() + "\n"
        out = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with io.open(out, "w", encoding="utf-8") as fp:
            fp.write(body)
        if (i + 1) % 10 == 0:
            say("组装 %d/%d" % (i + 1, len(files)))
    say("OCR 补救完成: %d 个文件" % len(files))
    with io.open(os.path.join(TMP, "第二批OCR补救报告.txt"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("FIX DONE")


if __name__ == "__main__":
    main()
