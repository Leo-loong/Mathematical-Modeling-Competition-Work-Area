# -*- coding: utf-8 -*-
"""把需要 OCR 的 PDF 渲染为 PNG（供 Windows 内置 OCR 使用）。

用法: python render_pages.py <dpi> [最大页数]
输出: temp/ocr_png/<idx>_<page>.png  以及 temp/ocr_map.json
"""
import os
import io
import sys
import json

import pymupdf

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
TMP = os.path.join(BASE, "temp")
PNG = os.path.join(TMP, "ocr_png")
sys.path.insert(0, TMP)
from convert_all import scan, pdf_has_text  # noqa: E402


def main():
    dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    os.makedirs(PNG, exist_ok=True)
    targets = [f for f in scan(".pdf") if not pdf_has_text(f)[0]]
    mapping = []
    total = 0
    for i, f in enumerate(targets):
        d = pymupdf.open(f)
        n = d.page_count if not limit else min(d.page_count, limit)
        for pno in range(n):
            pix = d[pno].get_pixmap(dpi=dpi)
            name = "%02d_%04d.png" % (i, pno)
            pix.save(os.path.join(PNG, name))
            total += 1
        d.close()
        print("rendered %s (%d pages)" % (os.path.basename(f), n))
    meta = dict(dpi=dpi,
                files=[os.path.relpath(f, SRC) for f in targets],
                counts=[])
    for i, f in enumerate(targets):
        d = pymupdf.open(f)
        meta["counts"].append(d.page_count)
        d.close()
    with io.open(os.path.join(TMP, "ocr_map.json"), "w", encoding="utf-8") as fp:
        fp.write(json.dumps(meta, ensure_ascii=False, indent=1))
    print("TOTAL PNG %d" % total)


if __name__ == "__main__":
    main()
