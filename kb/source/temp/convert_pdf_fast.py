# -*- coding: utf-8 -*-
"""convert_pdf_fast.py -- 第二批 PDF -> Markdown（文本层并发快通道，OCR 留到单独一轮）。

用法：
  python convert_pdf_fast.py            # 只做文本层，扫描件清单写入 b2_ocr_pending.txt
"""
import os
import io
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TMP = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(TMP)
SRC = os.path.join(SOURCE, "第二批")
DST = os.path.join(SOURCE, "第二批提取后")
PROGRESS = os.path.join(TMP, "pdf_fast_progress.txt")
REPORT = os.path.join(TMP, "第二批PDF转换报告.txt")
PENDING = os.path.join(TMP, "b2_ocr_pending.txt")

sys.path.insert(0, TMP)
import pdf_core as pc  # noqa: E402

WORKERS = 8
MIN_TEXT_PER_PAGE = 100
SKIP_EXISTING = "--force" not in sys.argv


def do_one(p):
    """（模块级，供进程池 pickle）单个 PDF -> md。"""
    dst = os.path.join(DST, os.path.splitext(os.path.relpath(p, SRC))[0] + ".md")
    if SKIP_EXISTING and os.path.exists(dst) and os.path.getsize(dst) > 0:
        return (True, p, "")
    try:
        body = pc.pdf_text_to_md(p)
        if not body.strip():
            return (False, p, "空文本")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with io.open(dst, "w", encoding="utf-8") as f:
            f.write(body)
        return (True, p, "")
    except Exception as e:
        return (False, p, repr(e)[:100])

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


def out_path(src):
    rel = os.path.relpath(src, SRC)
    return os.path.join(DST, os.path.splitext(rel)[0] + ".md")


def main():
    t0 = time.time()
    os.makedirs(DST, exist_ok=True)
    import pymupdf
    pdfs = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(dp, f))
    pdfs.sort()
    say("PDF 共 %d 个，开始分类" % len(pdfs))

    text_list, ocr_list, ocr_pages = [], [], 0
    for p in pdfs:
        try:
            d = pymupdf.open(p)
            total = sum(len((pg.get_text("text") or "").strip()) for pg in d)
            n = d.page_count
            d.close()
        except Exception:
            n, total = 0, 0
        if n and total >= MIN_TEXT_PER_PAGE * n:
            text_list.append(p)
        else:
            ocr_list.append(p)
            ocr_pages += n
    say("分类完成：文本层 %d，需 OCR %d（共 %d 页）" % (len(text_list), len(ocr_list), ocr_pages))
    with io.open(PENDING, "w", encoding="utf-8") as f:
        f.write("\n".join(os.path.relpath(p, SRC) for p in ocr_list))

    ok = fail = 0
    failed = []

    # pymupdf 取文本是 CPU 密集且不释放 GIL -> 用进程池才能真正并行
    from concurrent.futures import ProcessPoolExecutor

    n = len(text_list)
    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(do_one, p) for p in text_list]
        done = 0
        for fu in as_completed(futs):
            good, p, err = fu.result()
            done += 1
            if good:
                ok += 1
            else:
                fail += 1
                failed.append((os.path.relpath(p, SRC), err))
            if done % 100 == 0 or done == n:
                say("PDF 文本层进度 %d/%d" % (done, n))

    say("")
    say("PDF 文本层完成：成功 %d 失败 %d，耗时 %.1f 分钟" % (ok, fail, (time.time() - t0) / 60.0))
    say("需 OCR：%d 个 / %d 页（清单 %s）" % (len(ocr_list), ocr_pages, PENDING))
    say("--- 失败清单（前 40）---")
    for rel, err in failed[:40]:
        say("  %s  << %s" % (rel, err))
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("PDF_FAST DONE ok=%d fail=%d ocr=%d" % (ok, fail, len(ocr_list)))


if __name__ == "__main__":
    main()
