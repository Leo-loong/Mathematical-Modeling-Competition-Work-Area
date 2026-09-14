# -*- coding: utf-8 -*-
"""为目录下的文档建立「内容指纹索引」，用于跨批次查重。

用法:
  python scan_index.py <根目录> <扩展名逗号分隔> <输出csv>

输出字段: path, ext, size, md5(字节级), sha1(去空白后的文本内容), chars, note
- md5 相同  => 文件字节完全一致
- sha1 相同 => 文本内容一致（可能格式/元数据不同，或去空白后一致）
"""
import os
import re
import io
import csv
import sys
import hashlib

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TEXT_EXT = {".txt", ".md", ".py", ".m", ".csv", ".json", ".jsonl", ".rst",
            ".yml", ".yaml", ".xml", ".html", ".htm", ".tex", ".bib", ".c",
            ".cpp", ".h", ".java", ".js", ".ts", ".sh", ".bat", ".ps1", ".sql",
            ".r", ".jl", ".ini", ".cfg", ".log"}


def file_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_auto(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return ""


def docx_text(path):
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import docx_core as dc
        from docx import Document
        doc = Document(path)
        buf = []
        for kind, el in dc.iter_blocks(doc.element.body):
            if kind == "p":
                t = dc.runs_plain(dc.para_runs(el))
                if t.strip():
                    buf.append(t)
            else:
                for row in dc.collect_grid(el):
                    buf.append(" ".join(c for c in row if c))
        return "\n".join(buf)
    except Exception as e:
        return "[[DOCX_ERR %s]]" % (e,)


def pdf_text(path):
    try:
        import pymupdf
        d = pymupdf.open(path)
        parts = []
        for page in d:
            parts.append(page.get_text("text") or "")
        n = d.page_count
        d.close()
        return "\n".join(parts), n
    except Exception as e:
        return "[[PDF_ERR %s]]" % (e,), 0


def extract(path, ext):
    note = ""
    if ext == ".docx":
        return docx_text(path), note
    if ext == ".pdf":
        t, n = pdf_text(path)
        if len(t.strip()) < 60 * max(1, n):
            note = "NO_TEXT_LAYER" if n else note
        return t, note
    if ext == ".doc":
        return "", "DOC_LEGACY"
    if ext in TEXT_EXT:
        return read_text_auto(path), note
    return "", "UNSUPPORTED"


def main():
    root = sys.argv[1]
    exts = set("." + e.lower().lstrip(".") for e in sys.argv[2].split(","))
    out_csv = sys.argv[3]
    rows = []
    n = 0
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            if f.startswith("~$"):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext not in exts:
                continue
            p = os.path.join(dp, f)
            try:
                size = os.path.getsize(p)
                text, note = extract(p, ext)
                norm = re.sub(r"\s+", "", text)
                rows.append(dict(
                    path=os.path.relpath(p, root),
                    ext=ext, size=size,
                    md5=file_md5(p),
                    sha1=hashlib.sha1(norm.encode("utf-8", "ignore")).hexdigest(),
                    chars=len(text), note=note))
                n += 1
                if n % 100 == 0:
                    print("scanned %d" % n)
            except Exception as e:
                rows.append(dict(path=os.path.relpath(p, root), ext=ext,
                                 size=-1, md5="ERR", sha1="ERR",
                                 chars=0, note="SCAN_ERR %s" % (e,)))
    with io.open(out_csv, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=["path", "ext", "size", "md5", "sha1", "chars", "note"])
        w.writeheader()
        w.writerows(rows)
    print("WROTE %s rows=%d" % (out_csv, len(rows)))


if __name__ == "__main__":
    main()
