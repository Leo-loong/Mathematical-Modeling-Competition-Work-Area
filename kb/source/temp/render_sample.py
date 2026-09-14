# -*- coding: utf-8 -*-
"""渲染指定 PDF 的指定页，供人工/模型精读核对 OCR 质量。"""
import os
import sys
import pymupdf

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
OUT = os.path.join(BASE, "temp", "qc_sample")


def main():
    dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ("老哥讲义！2026数学建模国赛冲奖要点全解析！.pdf", [20, 61]),
        ("2026数学建模国赛60个核心获奖要点！.pdf", [12]),
    ]
    for name, pages in jobs:
        d = pymupdf.open(os.path.join(SRC, name))
        for p in pages:
            if p - 1 >= d.page_count:
                continue
            fn = "%s_p%d.png" % (name[:8], p)
            d[p - 1].get_pixmap(dpi=dpi).save(os.path.join(OUT, fn))
            print("saved " + fn)
        d.close()


if __name__ == "__main__":
    main()
