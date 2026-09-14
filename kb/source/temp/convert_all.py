# -*- coding: utf-8 -*-
"""一次性总转换：第一批 -> 第一批提取后（保留目录结构与文件名，扩展名改 .md）。

策略（按速度从快到慢）：
  1. .docx           ：python-docx 直读XML（秒级）
  2. .doc            ：Word COM 另存为 docx 后同上
  3. .pdf 有文本层   ：PyMuPDF 按版式重排（秒级）
  4. .pdf 纯扫描图片 ：渲染后离线 OCR（多进程并行）

终端只输出 ASCII；详细中文日志写入 report.txt。
"""
import os
import io
import re
import sys
import json
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
DST = os.path.join(BASE, "第一批提取后")
TMP = os.path.join(BASE, "temp")
DOCX_CACHE = os.path.join(TMP, "docx_cache")
REPORT = os.path.join(TMP, "final_report.txt")
sys.path.insert(0, TMP)

import docx_core as dc  # noqa: E402

_LOG = []


def log(s):
    _LOG.append(s)


def scan(ext):
    res = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.startswith("~$"):
                continue
            if f.lower().endswith(ext):
                res.append(os.path.join(dp, f))
    res.sort()
    return res


def out_path(src, rel_root=None, ext=".md"):
    rel = os.path.relpath(src, rel_root or SRC)
    return os.path.join(DST, os.path.splitext(rel)[0] + ext)


def write_md(dst, body):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8") as f:
        f.write(body)


# ---------------------------------------------------------------- Word / doc

def doc_to_docx(files):
    """Word COM 把 .doc 另存为 .docx，返回 [(原始doc, 临时docx)]。"""
    out = []
    if not files:
        return out
    os.makedirs(DOCX_CACHE, exist_ok=True)
    import win32com.client as win32
    import pythoncom
    pythoncom.CoInitialize()
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        for i, src in enumerate(files):
            rel = os.path.splitext(os.path.relpath(src, SRC))[0]
            safe = re.sub(r'[\\/:*?"<>|]', "_", rel)
            dst = os.path.join(DOCX_CACHE, "%03d_%s.docx" % (i, safe[:60]))
            try:
                d = word.Documents.Open(src, False, True)
                d.SaveAs2(dst, 16)  # wdFormatDocumentDefault
                d.Close(0)
                out.append((src, dst))
                print("COM-OK %d" % i)
            except Exception as e:
                log("COM FAIL %s : %r" % (rel, e))
                print("COM-ERR %d" % i)
    finally:
        word.Quit()
        pythoncom.CoUninitialize()
    return out


def do_docx(pairs):
    """pairs: [(源相对路径名, 实际docx路径)]"""
    ok = 0
    for label, real in pairs:
        try:
            body = dc.docx_to_md(real)
            write_md(os.path.join(DST, os.path.splitext(label)[0] + ".md"), body)
            ok += 1
            log("[DOCX] OK %s (%d chars)" % (label, len(body)))
        except Exception:
            log("[DOCX] ERR %s\n%s" % (label, traceback.format_exc()))
    print("DOCX done %d/%d" % (ok, len(pairs)))
    return ok


# ---------------------------------------------------------------- PDF

def pdf_has_text(path, threshold=100):
    import pymupdf
    d = pymupdf.open(path)
    total = 0
    for page in d:
        total += len((page.get_text("text") or "").strip())
    n = d.page_count
    d.close()
    return total >= threshold * n, total, n


def do_pdf_text(files):
    import pdf_core as pc
    ok = 0
    for src in files:
        try:
            body = pc.pdf_text_to_md(src)
            write_md(out_path(src), body)
            ok += 1
            log("[PDF-TEXT] OK %s (%d chars)" % (os.path.basename(src), len(body)))
        except Exception:
            log("[PDF-TEXT] ERR %s\n%s" % (os.path.basename(src), traceback.format_exc()))
    print("PDFTEXT done %d/%d" % (ok, len(files)))
    return ok


def _ocr_worker(args):
    src, dst = args
    sys.path.insert(0, TMP)
    import pdf_core as pc
    body = pc.pdf_ocr_to_md(src, dpi=180)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8") as f:
        f.write(body)
    return os.path.basename(src), len(body)


def do_pdf_ocr(files, workers=4):
    tasks = [(f, out_path(f)) for f in files]
    ok = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_ocr_worker, t): t for t in tasks}
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                name, n = fu.result()
                log("[PDF-OCR] OK %s (%d chars)" % (name, n))
                ok += 1
                print("OCR %d/%d %s chars=%d" % (i, len(tasks), name, n))
            except Exception:
                name = os.path.basename(futs[fu][0])
                log("[PDF-OCR] ERR %s\n%s" % (name, traceback.format_exc()))
                print("OCR-ERR %s" % name)
    return ok


# ---------------------------------------------------------------- main

def main():
    t0 = time.time()
    os.makedirs(DST, exist_ok=True)

    docxs = scan(".docx")
    docs = scan(".doc")
    pdfs = scan(".pdf")
    print("scan: docx=%d doc=%d pdf=%d" % (len(docxs), len(docs), len(pdfs)))

    pairs = [(os.path.relpath(f, SRC), f) for f in docxs]
    if docs:
        pairs += [(os.path.relpath(s, SRC), d) for s, d in doc_to_docx(docs)]
    do_docx(pairs)

    pdf_text, pdf_ocr = [], []
    for p in pdfs:
        has, total, n = pdf_has_text(p)
        log("[SCAN] %s text=%d pages=%d -> %s" % (
            os.path.basename(p), total, n, "TEXT" if has else "OCR"))
        (pdf_text if has else pdf_ocr).append(p)
    print("pdf: text=%d ocr=%d" % (len(pdf_text), len(pdf_ocr)))

    do_pdf_text(pdf_text)
    if pdf_ocr:
        do_pdf_ocr(pdf_ocr, workers=min(6, max(2, os.cpu_count() - 2)))

    log("ELAPSED %.1f s" % (time.time() - t0))
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(_LOG))
    print("ALL DONE %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
