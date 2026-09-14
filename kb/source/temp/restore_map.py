# -*- coding: utf-8 -*-
"""从 ocr_tsv 目录重建 ocr_map.json（无需重新渲染图片）。"""
import os
import io
import sys
import json

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
TMP = os.path.join(BASE, "temp")
TSV = os.path.join(TMP, "ocr_tsv")
sys.path.insert(0, TMP)
from convert_all import scan, pdf_has_text  # noqa: E402
import pymupdf

files = [f for f in scan(".pdf") if not pdf_has_text(f)[0]]
meta = dict(dpi=150,
            files=[os.path.relpath(f, SRC) for f in files],
            counts=[])
for f in files:
    d = pymupdf.open(f)
    meta["counts"].append(d.page_count)
    d.close()
io.open(os.path.join(TMP, "ocr_map.json"), "w", encoding="utf-8").write(
    json.dumps(meta, ensure_ascii=False, indent=1))
print("files=%d pages=%d" % (len(meta["files"]), sum(meta["counts"])))
print("tsv on disk=%d" % len([x for x in os.listdir(TSV) if x.endswith(".tsv")]))
