# -*- coding: utf-8 -*-
"""Word(.docx) -> Markdown 转换核心模块。

设计原则：
1. 文本内容一字不差（仅做 Markdown 必需的转义，如表格单元格中的竖线）。
2. 结构合理化：标题 / 列表 / 分隔线 / 表格按语义重建。
3. 严格按文档 XML 顺序遍历，覆盖表格、文本框、SDT 等容器，确保不丢内容。
"""
import re

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SEP_CHARS = "\u2500\u2501\u2014\u2013-=_\uff3f\uff0a\u00b7\u2022\u25cf\u25cb\u25aa\u25a0\u25a1\u3010\u3011\u3007"
RE_SEP = re.compile(r"^[\s%s]{4,}$" % re.escape(SEP_CHARS))
RE_LIST = re.compile(r"^(\s*)([\u2022\u00b7\u25cf\u25cb\u25aa\u25a0\u25a1\u2219\u30fb\u2027\u221a\u2714])\s*(.*)$")
RE_BRACKET_HEAD = re.compile(r"^[【\[][^【】\[\]]{1,40}[】\]][:：]?\s*$")
RE_STEP_HEAD = re.compile(
    r"^(?:第[0-9\uff10-\uff19]{1,3}[步章节部分篇模块]"
    r"|(?:模式|阶段|环节|步骤|阶段)[一二三四五六七八九十0-9]{1,3}"
    r")[:：]\s*\S")
RE_CN_HEAD = re.compile(r"^[一二三四五六七八九十]{1,3}[、]\s*\S")
RE_NUM_HEAD = re.compile(r"^(?:[0-9]{1,2}|[一二三四五六七八九十]{1,3})[、\.]\s*\S")


# ---------------------------------------------------------------- 富文本提取

def _flag(rPr, tag):
    """读取 rPr 中的布尔开关，考虑 w:val=false 形式。"""
    if rPr is None:
        return False
    e = rPr.find(tag)
    if e is None:
        return False
    v = e.get(W + "val")
    return v not in ("false", "0", "off")


def _walk_runs(el, out):
    """递归遍历产生 [ [text, style] , ... ]，style 为 () / ('B',) / ('I',) / ('B','I')。"""
    for ch in el:
        t = ch.tag
        if t in (W + "drawing", W + "pict", W + "object"):
            # 图形内含文本框时，其中的段落由主块遍历单独渲染，避免重复
            continue
        if t == W + "t":
            out.append([ch.text or "", ()])
        elif t == W + "tab":
            out.append(["\t", ()])
        elif t in (W + "br", W + "cr"):
            out.append([" ", ()])
        elif t == W + "sym":
            out.append([ch.get(W + "char") or "", ()])
        elif t == W + "r":
            rPr = ch.find(W + "rPr")
            st = []
            if _flag(rPr, W + "b"):
                st.append("B")
            if _flag(rPr, W + "i") or _flag(rPr, W + "iCs"):
                st.append("I")
            before = len(out)
            _walk_runs(ch, out)
            for item in out[before:]:
                item[1] = tuple(st)
        else:
            _walk_runs(ch, out)


def para_runs(p_el):
    out = []
    _walk_runs(p_el, out)
    return out


def runs_plain(pieces):
    return "".join(p[0] for p in pieces)


def runs_md(pieces):
    """渲染为带行内标记的 Markdown 文本（合并相邻同样式片段）。"""
    buf = []
    for txt, st in pieces:
        if not txt:
            continue
        if buf and buf[-1][1] == st:
            buf[-1][0] += txt
        else:
            buf.append([txt, st])
    res = ""
    for txt, st in buf:
        if not st:
            res += txt
            continue
        bold = "B" in st
        ital = "I" in st
        res += ("**" if bold else "") + ("*" if ital else "") + txt \
               + ("*" if ital else "") + ("**" if bold else "")
    return res


# ---------------------------------------------------------------- 块级遍历

def iter_blocks(el):
    """按文档顺序产出 ('p', el) / ('tbl', el)。"""
    for child in el.iterchildren():
        t = child.tag
        if t == W + "p":
            yield ("p", child)
        elif t == W + "tbl":
            yield ("tbl", child)
        else:
            for blk in iter_blocks(child):
                yield blk


# ---------------------------------------------------------------- 表格

def _pairs(row):
    if not row:
        return []
    if len(row) == 1:
        return [(row[0], "")]
    return [(row[0], " / ".join(x for x in row[1:] if x))]


def render_cell_value(tc_el):
    """单元格 -> 单行文本（多段落用 <br> 连接）。"""
    parts = []
    for child in tc_el.iterchildren():
        t = child.tag
        if t == W + "p":
            txt = runs_md(para_runs(child))
            if txt.strip():
                parts.append(txt.strip())
        elif t == W + "tbl":
            for r in collect_grid(child):
                for a, b in _pairs(r):
                    parts.append(("%s：%s" % (a.strip(), b.strip())) if b.strip() else a.strip())
        else:
            for kind, sub in iter_blocks(child):
                if kind == "p":
                    txt = runs_md(para_runs(sub))
                    if txt.strip():
                        parts.append(txt.strip())
                else:
                    for r in collect_grid(sub):
                        for a, b in _pairs(r):
                            parts.append(("%s：%s" % (a.strip(), b.strip())) if b.strip() else a.strip())
    return "<br>".join(parts)


def collect_grid(tbl_el):
    """表格 -> 二维文本网格，已处理 gridSpan（横向合并）与 vMerge（纵向合并）。"""
    grid = []
    prev = None
    for tr in tbl_el.findall(W + "tr"):
        row = []
        for tc in tr.findall(W + "tc"):
            tcPr = tc.find(W + "tcPr")
            gs = 1
            vmerge = None
            if tcPr is not None:
                g = tcPr.find(W + "gridSpan")
                if g is not None:
                    try:
                        gs = int(g.get(W + "val"))
                    except Exception:
                        gs = 1
                vm = tcPr.find(W + "vMerge")
                if vm is not None:
                    val = vm.get(W + "val")
                    vmerge = val if val == "restart" else "continue"
            txt = render_cell_value(tc)
            if vmerge == "continue" and prev is not None and len(row) < len(prev) and not txt:
                txt = prev[len(row)]
            row.append(txt)
            for _i in range(gs - 1):
                row.append("")
        grid.append(row)
        prev = row
    return grid


def esc_cell(s):
    return s.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def md_table(grid):
    """二维网格 -> Markdown 表格行列表。"""
    if not grid:
        return []
    width = max(len(r) for r in grid)
    def pad(r):
        r = list(r) + [""] * (width - len(r))
        return "| " + " | ".join(esc_cell(c) for c in r) + " |"
    lines = [pad(grid[0]), "| " + " | ".join(["---"] * width) + " |"]
    for r in grid[1:]:
        lines.append(pad(r))
    return lines


# ---------------------------------------------------------------- 段落结构判定

def classify(text, is_first_doc_para, is_second_doc_para):
    """返回 (kind, payload)；kind ∈ heading1/heading2/heading3/sep/list/plain。"""
    t = text.rstrip()
    s = t.strip()
    if not s:
        return ("blank", "")
    if RE_SEP.match(s):
        return ("sep", "")
    if RE_LIST.match(t):
        m = RE_LIST.match(t)
        indent = len(m.group(1).expandtabs(2))
        return ("list", (min(indent // 2, 4), m.group(3)))
    if is_first_doc_para:
        return ("heading1", s)
    if is_second_doc_para and s.startswith(("\uff08", "(")) and len(s) <= 60:
        return ("heading2", s)
    if RE_BRACKET_HEAD.match(s):
        return ("heading3", s)
    if len(s) <= 45 and (RE_STEP_HEAD.match(s) or RE_CN_HEAD.match(s)):
        return ("heading2", s)
    if len(s) <= 45 and RE_NUM_HEAD.match(s) and not s.endswith(("。", "；", "：", ":", "，", ",")):
        return ("heading3", s)
    return ("plain", t.rstrip())


def _strip_wrap(s):
    """去掉整段统一包裹的粗体/斜体标记（用于标题行，避免 **标题** 这种冗余）。"""
    while len(s) > 4 and ((s.startswith("**") and s.endswith("**"))
                          or (s.startswith("*") and s.endswith("*") and not s.startswith("**"))):
        s = s[2:-2] if s.startswith("**") else s[1:-1]
    return s


def render_paragraph(kind, payload, plain, rich):
    """kind 来自「纯文本」判定，渲染时使用「富文本」版本保证内容不丢。"""
    if kind == "blank":
        return ""
    if kind == "sep":
        return "---"
    if kind == "heading1":
        return "# " + _strip_wrap(rich)
    if kind == "heading2":
        return "## " + _strip_wrap(rich)
    if kind == "heading3":
        return "### " + _strip_wrap(rich)
    if kind == "list":
        level, body = payload
        return "  " * level + "- " + _strip_wrap(body)
    return rich.rstrip()


# ---------------------------------------------------------------- 主入口

def docx_to_md(path, doc_title=None):
    from docx import Document

    doc = Document(path)
    out = []
    first = True
    second = False
    last_blank = False

    def emit(line):
        nonlocal last_blank
        if line == "":
            if not last_blank:
                out.append("")
            last_blank = True
        else:
            out.append(line)
            last_blank = False

    for kind, el in iter_blocks(doc.element.body):
        if kind == "p":
            pieces = para_runs(el)
            rich = runs_md(pieces)
            plain = runs_plain(pieces)
            s = plain.strip()
            if not s:
                emit("")
                continue
            k, payload = classify(plain, first, second)
            if k == "list":
                # 列表正文需按原始缩进映射到富文本上（用纯文本定位前缀长度）
                m = RE_LIST.match(plain.rstrip())
                body_plain = m.group(3) if m else s
                idx = rich.find(body_plain)
                body_rich = rich[idx:] if idx >= 0 else rich.lstrip()
                payload = (payload[0], body_rich)
            if first:
                first = False
                second = True
            elif second:
                second = False
            emit(render_paragraph(k, payload, plain, rich))
        else:
            grid = collect_grid(el)
            lines = md_table(grid)
            if lines:
                emit("")
                for ln in lines:
                    emit(ln)
                emit("")

    while out and not out[0].strip():
        out.pop(0)
    lines = []
    for ln in out:
        if ln == "" and lines and lines[-1] == "":
            continue
        lines.append(ln)
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"
