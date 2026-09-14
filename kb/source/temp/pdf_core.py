# -*- coding: utf-8 -*-
"""PDF -> Markdown 转换模块，含两条通道：
1. pdf_text_to_md：PDF 自带文本层时，按行重排 + 字号判定层级 + find_tables 还原表格；
2. pdf_ocr_to_md ：PDF 为图片（无文本层）时，渲染为位图后离线 OCR 再结构化。

两条通道最终都走统一的「行 -> Markdown」渲染管线。
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import docx_core as dc  # 复用同一套中文标题/列表判定规则

import pymupdf

# Wingdings / Symbol 私有区常用项目符号 -> 统一为圆点
BULLET_MAP = {
    "\uf06c": "\u2022", "\uf0b7": "\u2022", "\uf0a7": "\u2022",
    "\uf0a5": "\u2022", "\uf0d8": "\u2022", "\uf0b2": "\u2022",
    "\u25cf": "\u2022", "\u25cb": "\u25cb", "\u25aa": "\u2022",
    "\u25a0": "\u2022", "\u30fb": "\u2022", "\u2027": "\u2022",
    "\u2219": "\u2022", "\u00b7": "\u00b7",
}
HEADING_MAXLEN = 60


def clean_text(s):
    return "".join(BULLET_MAP.get(ch, ch) for ch in s)


# ------------------------------------------------------------------ 通用渲染

class Renderer(object):
    """把「视觉行」序列渲染为 Markdown。"""

    def __init__(self):
        self.out = []
        self._last_blank = True

    def emit(self, line):
        if line == "":
            if not self._last_blank:
                self.out.append("")
            self._last_blank = True
        else:
            self.out.append(line)
            self._last_blank = False

    def blank(self):
        self.emit("")

    def table(self, md_block):
        self.blank()
        for ln in md_block.rstrip().split("\n"):
            self.emit(ln)
        self.blank()

    def line_blocks(self, rows, size_level_fn=None, level_of_row=None):
        pass

    def finish(self):
        lines = []
        for ln in self.out:
            if ln == "" and lines and lines[-1] == "":
                continue
            lines.append(ln)
        while lines and lines[-1] == "":
            lines.pop()
        while lines and lines[0] == "":
            lines.pop(0)
        return "\n".join(lines) + "\n"


def render_rows(rows, level_fn, renderer, gap_threshold):
    """rows: [(y0, y1, x0, x1, size, text)] 已按阅读顺序排好。
    level_fn(row) -> None / 1..4 标题级别。"""
    prev_bottom = None
    for row in rows:
        y0, y1, _x0, _x1, _size, text = row
        s = text.strip()
        if not s:
            continue
        if prev_bottom is not None and y0 - prev_bottom > gap_threshold:
            renderer.blank()
        prev_bottom = y1
        lvl = level_fn(row)
        if lvl:
            renderer.blank()
            renderer.emit("#" * lvl + " " + s)
            renderer.blank()
            continue
        k, payload = dc.classify(s, False, False)
        if k == "sep":
            renderer.blank()
            renderer.emit("---")
            renderer.blank()
            continue
        if k == "list":
            level, body = payload
            renderer.emit("  " * level + "- " + body)
            continue
        renderer.emit(s)


# ------------------------------------------------------------------ 文本层通道

def _center_inside(bbox, tables, margin=2.0):
    x0, y0, x1, y1 = bbox
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    for tb in tables:
        if tb[0] - margin <= cx <= tb[2] + margin and tb[1] - margin <= cy <= tb[3] + margin:
            return True
    return False


def _page_rows(page, tables):
    """提取页面非表格区域的视觉行（同一水平带内的 span 按 x 合并）。"""
    d = page.get_text("dict")
    raw = []
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        for ln in b["lines"]:
            bb = ln["bbox"]
            if tables and _center_inside(bb, tables):
                continue
            spans = ln["spans"]
            if not spans:
                continue
            txt = "".join(sp["text"] for sp in spans)
            if not txt.strip():
                continue
            size = max(sp["size"] for sp in spans)
            raw.append((bb[0], bb[1], bb[2], bb[3], size, txt))
    raw.sort(key=lambda r: (round(r[1], 1), r[0]))
    rows = []
    cur = None
    for x0, y0, x1, y1, size, txt in raw:
        if cur is None or abs(y0 - cur["top"]) > 3.5:
            if cur is not None:
                rows.append(_flush_row(cur))
            cur = dict(top=y0, bottom=y1, size=size, parts=[(x0, x1, txt, size)])
        else:
            cur["bottom"] = max(cur["bottom"], y1)
            cur["size"] = max(cur["size"], size)
            cur["parts"].append((x0, x1, txt, size))
    if cur is not None:
        rows.append(_flush_row(cur))
    return rows


def _flush_row(cur):
    parts = sorted(cur["parts"], key=lambda p: p[0])
    buf = ""
    prev_x1 = None
    for x0, x1, txt, _sz in parts:
        if prev_x1 is not None and x0 - prev_x1 > 1.2:
            buf += " "
        buf += txt
        prev_x1 = x1
    return (cur["top"], cur["bottom"], parts[0][0], max(p[1] for p in parts),
            cur["size"], clean_text(buf))


def _is_page_number(text, y0, page_h):
    t = text.strip()
    return bool(re.match(r"^[\-\u2013]?\d{1,4}[\-\u2013]?$", t)) and y0 > page_h * 0.82


# --- 结构化判定（PDF 通道专用：无字体样式，靠字号/缩进/编号模式） ---

RE_NUM_SEC = re.compile(r"^(\d+(?:\.\d+)*)[\s、]\s*\S")
RE_PAREN_SEC = re.compile(r"^[\uff08(]\s*[0-9\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]{1,3}\s*[\uff09)]\s*\S")
RE_BULLET = re.compile(r"^\s*\u2022\s*(.*)$")
RE_HEADLINE = re.compile(r"^\s*\u2022?\s*(.*)$")


def build_indent_cols(all_rows, tol=7.0):
    """按 x 坐标聚类出文档的缩进层级（PDF 无样式，靠排版位置恢复层级）。"""
    xs = []
    for rows in all_rows:
        for row in rows:
            text = row[-1]  # 行元组末位统一为文本
            if RE_BULLET.match(text):
                xs.append(row[2])
    xs.sort()
    cols = []
    for x in xs:
        if not cols or x - cols[-1][-1] > tol:
            cols.append([x])
        else:
            cols[-1].append(x)
    return [sum(c) / len(c) for c in cols]


def _indent_level(x0, cols, tol=7.0):
    best = 0
    for i, c in enumerate(cols):
        if abs(x0 - c) <= tol:
            best = i
            break
        if x0 > c:
            best = i
    return min(best, 4)


def row_to_md(row, level_map, cols):
    """单个视觉行 -> markdown 行列表 + 是否为块级标题。"""
    s = row[5].strip()
    if not s:
        return ([], True)
    m = RE_BULLET.match(s)
    if m:
        lvl = _indent_level(row[2], cols)
        body = m.group(1).strip()
        if not body:
            return ([], True)
        return (["  " * lvl + "- " + body], False)
    size_lvl = level_map.get(round(row[4], 1))
    if size_lvl and len(s) <= HEADING_MAXLEN:
        return (["#" * size_lvl + " " + s], True)
    mm = RE_NUM_SEC.match(s)
    if mm and len(s) <= HEADING_MAXLEN:
        dots = mm.group(1).count(".")
        return (["#" * min(2 + dots - 1, 4) + " " + s], True)
    if RE_PAREN_SEC.match(s) and len(s) <= 45:
        return (["#### " + s], True)
    k, pl = dc.classify(s, False, False)
    if k == "sep":
        return (["---"], True)
    if k == "list":
        lvl, body = pl
        return (["  " * lvl + "- " + body], False)
    if k in ("heading2", "heading3"):
        return (["### " + s, ""], True)
    return ([s], False)


def pdf_text_to_md(path, progress=None):
    doc = pymupdf.open(path)
    pages = []
    sizes = {}
    for i, page in enumerate(doc):
        tabs = sorted(page.find_tables().tables, key=lambda t: t.bbox[1])
        tboxes = [tuple(t.bbox) for t in tabs]
        rows = _page_rows(page, tboxes)
        rows = [r for r in rows if not _is_page_number(r[5], r[0], page.rect.height)]
        # 统计字号（按字符数加权）
        for r in rows:
            key = round(r[4], 1)
            sizes[key] = sizes.get(key, 0) + len(r[5])
        pages.append((rows, tabs))
        if progress:
            progress(i + 1, doc.page_count)
    doc.close()

    if not sizes:
        return ""
    dom = max(sizes.items(), key=lambda kv: kv[1])[0]
    big = sorted([s for s in sizes if s > dom + 0.8])
    # 大字号 -> 标题级别：最大的做一级，其余依次下探
    level_map = {}
    for idx, sz in enumerate(sorted(big, reverse=True)):
        level_map[sz] = min(1 + idx, 4)

    cols = build_indent_cols([p[0] for p in pages])
    r = Renderer()
    for pno, (rows, tabs) in enumerate(pages):
        r.emit("<!-- 第 %d 页 -->" % (pno + 1))
        heights = sorted(y1 - y0 for y0, y1, x0, x1, sz, tx in rows)
        lh = heights[len(heights) // 2] if heights else 14.0
        items = [(row[0], row[1], "row", row) for row in rows] + \
                [(t.bbox[1], t.bbox[3], "table", t) for t in tabs]
        items.sort(key=lambda it: it[0])
        prev_bottom = None
        for y0, y1, kind, payload in items:
            if kind == "table":
                r.table(payload.to_markdown())
                prev_bottom = None
                continue
            row = payload
            gap = prev_bottom is not None and (y0 - prev_bottom) > lh * 1.15
            prev_bottom = y1
            lines, is_block = row_to_md(row, level_map, cols)
            for i, ln in enumerate(lines):
                if i == 0 and (gap or is_block):
                    r.blank()
                r.emit(ln)
        r.blank()
    return r.finish()


# ------------------------------------------------------------------ OCR 通道

def _ocr_text_items(engine, page, dpi):
    pix = page.get_pixmap(dpi=dpi)
    result, _elapse = engine(pix.tobytes("png"))
    items = []
    scale = 72.0 / dpi
    if result:
        for box, text, _score in result:
            xs = [p[0] for p in box]
            ys = [p[1] for p in box]
            items.append((min(ys) * scale, max(ys) * scale,
                          min(xs) * scale, max(xs) * scale, text))
    return items


def ocr_page_rows(engine, page, dpi):
    """OCR 单页并按 y 聚类还原视觉行。"""
    items = _ocr_text_items(engine, page, dpi)
    raw = []
    for y0, y1, x0, x1, txt in items:
        t = clean_text(txt).strip()
        if not t or _is_page_number(t, y0, page.rect.height):
            continue
        raw.append((y0, y1, x0, x1, t))
    raw.sort(key=lambda it: (round(it[0], 1), it[2]))
    rows = []
    cur = None
    for y0, y1, x0, x1, txt in raw:
        if cur is None or abs(y0 - cur["top"]) > 8.0:
            if cur is not None:
                rows.append(_flush_ocr_row(cur))
            cur = dict(top=y0, bottom=y1, parts=[(x0, x1, txt)])
        else:
            cur["bottom"] = max(cur["bottom"], y1)
            cur["parts"].append((x0, x1, txt))
    if cur is not None:
        rows.append(_flush_ocr_row(cur))
    return rows


def render_ocr_pages(pages_rows, level_map=None):
    """pages_rows: [[row, ...] 每页一行列表] -> Markdown 字符串。"""
    level_map = level_map or {}
    cols = build_indent_cols(pages_rows)
    r = Renderer()
    for pno, rows in enumerate(pages_rows):
        r.emit("<!-- 第 %d 页 -->" % (pno + 1))
        heights = sorted(row[1] - row[0] for row in rows)
        lh = heights[len(heights) // 2] if heights else 14.0
        prev_bottom = None
        for row in rows:
            y0, y1 = row[0], row[1]
            gap = prev_bottom is not None and (y0 - prev_bottom) > lh * 1.15
            prev_bottom = y1
            lines, is_block = row_to_md((y0, y1, row[2], row[3], 0.0, row[-1]),
                                        level_map, cols)
            for i, ln in enumerate(lines):
                if i == 0 and (gap or is_block):
                    r.blank()
                r.emit(ln)
        r.blank()
    return r.finish()


def pdf_ocr_to_md(path, dpi=180, progress=None):
    from rapidocr_onnxruntime import RapidOCR

    engine = RapidOCR()
    doc = pymupdf.open(path)
    pages_rows = []
    for pno in range(doc.page_count):
        pages_rows.append(ocr_page_rows(engine, doc[pno], dpi))
        if progress:
            progress(pno + 1, doc.page_count)
    doc.close()
    return render_ocr_pages(pages_rows)


def _flush_ocr_row(cur):
    parts = sorted(cur["parts"], key=lambda p: p[0])
    buf = ""
    prev_x1 = None
    for x0, x1, txt in parts:
        if prev_x1 is not None and x0 - prev_x1 > 6.0:
            buf += " "
        buf += txt
        prev_x1 = x1
    return (cur["top"], cur["bottom"], parts[0][0], max(p[1] for p in parts), buf)
