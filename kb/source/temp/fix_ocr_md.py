# -*- coding: utf-8 -*-
"""OCR 结果修复：页脚过滤 / 形近字修正 / 表格区重建。

仅作用于「无文本层、经 OCR 得到」的 Markdown，文本层文件不受影响。
原则：只调整结构与明确的形近字，不删除、不改写任何未经确认的内容。
"""
import os
import re
import io
import sys
from collections import Counter

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
DST = os.path.join(BASE, "第一批提取后")
TMP = os.path.join(BASE, "temp")
REPORT = os.path.join(TMP, "OCR修复报告.txt")
sys.path.insert(0, TMP)
from convert_all import scan, pdf_has_text  # noqa: E402

RE_PAGE_TAG = re.compile(r"^<!--\s*第\s*\d+\s*页\s*-->\s*$")
RE_PAGE_FOOT = re.compile(r"^第\s*\d+\s*页\s*[/／]\s*共\s*\d+\s*页$")
RE_HEADING = re.compile(r"^(#{2,4})\s+(.*)$")

# ---- 形近字修正表：(正则, 替换, 说明) ----
# 全部带上下文约束，避免误伤正常文本
FIX_RULES = [
    (re.compile(r"弟(?=[0-9一二三四五六七八九十]{1,2}\s*[步天章节页项])"), "第", "弟->第(弟X步/弟X天)"),
    (re.compile(r"佛(?=[0-9一二三四五六七八九十]{1,2}\s*[天步])"), "第", "佛->第(佛X天)"),
    (re.compile(r"第(?=[0-9一二三四五六七八九十]{1,2}\s*[步天章节页项])"), "第", "规范第"),
    (re.compile(r"间题"), "问题", "间题->问题"),
    (re.compile(r"王笔为王"), "主笔为主", "王笔为王->主笔为主"),
    (re.compile(r"主笔为王"), "主笔为主", "主笔为王->主笔为主"),
    (re.compile(r"王笔"), "主笔", "王笔->主笔"),
    (re.compile(r"(\d)[．・](\d)(?=\s*(?:条|个|步|小时|天|次|项|人))"),
     r"\1-\2", "数字范围号 . -> -"),
    (re.compile(r"纟且"), "组", "纟且->组"),
    (re.compile(r"分纟且"), "分组", "分纟且->分组"),
    (re.compile(r"題"), "题", "題->题(繁转简)"),
    (re.compile(r"間"), "间", "間->间(繁转简)"),
    (re.compile(r"〔(?=[^〕]{1,20})"), "（", "〔->（"),
    (re.compile(r"〕"), "）", "〕->）"),
]

NOTE_LINE = "> 说明：本文件由扫描件 OCR 生成，经形近字与结构修复；" \
            "表格为按 OCR 行序重建，列划分可能有偏差，关键数字与公式请回查原件。"


def apply_char_fixes(line, counter):
    for pat, rep, desc in FIX_RULES:
        new = pat.sub(rep, line)
        if new != line:
            counter[desc] += 1
            line = new
    return line


def split_pages(lines):
    """按 <!-- 第 N 页 --> 切页，返回 [(pageno, [lines])]。"""
    pages = []
    cur_no = 0
    cur = []
    for ln in lines:
        m = RE_PAGE_TAG.match(ln)
        if m:
            if cur:
                pages.append((cur_no, cur))
            cur_no = int(re.search(r"\d+", m.group(0)).group(0))
            cur = []
        else:
            cur.append(ln)
    if cur:
        pages.append((cur_no, cur))
    return pages


def find_boilerplate(pages):
    """页眉/页脚识别：把数字归一化为 # 后统计重复行模板。

    这样 "第12页/共63页" 与 "第13页/共63页" 会归并为同一模板。
    """
    cnt = Counter()
    n = 0
    for _no, body in pages:
        n += 1
        seen = set()
        for ln in body:
            s = ln.strip()
            if not s:
                continue
            key = re.sub(r"\d+", "#", s)
            if key in seen:
                continue
            seen.add(key)
            cnt[key] += 1
    n_page = max(1, n)
    return set(s for s, c in cnt.items()
               if c >= n_page * 0.6 and c > 3
               and re.search(r"[#\d]|页|共|篇", s))


def is_page_footer(s):
    key = re.sub(r"\d+", "#", s)
    return bool(RE_PAGE_FOOT.match(s) or re.match(r"^第#+页", key)
                or re.match(r"^第#+页\s*[/／]\s*共#+页$", key))


def matches_boiler(s, boiler):
    return s in boiler or re.sub(r"\d+", "#", s) in boiler


def looks_like_cell(s):
    return bool(s) and len(s) <= 26


def short_body(s):
    """去掉 Markdown 标题前缀后的正文长度；非短行返回 None。"""
    t = s.strip()
    if not t:
        return None
    m = RE_HEADING.match(t)
    body = m.group(2) if m else t
    if not body or len(body) > 26:
        return None
    return body


def try_table(block):
    """把「按列连续输出」的短行块重组成表格，返回 (表格行, 余下未入表行)。

    OCR 常把一个单元格断成两行，故允许少量余数行（<=3）不参与分列。
    """
    m = len(block)
    if m < 6:
        return None
    best = None
    for cols in range(2, 7):
        rows = m // cols
        rem = m % cols
        # 严格要求等长：OCR 断行会让各列行数不等，此时不重建（避免错配误导）
        if rows < 2 or rows > 25 or rem != 0:
            continue
        # 每列首行应为表头样式（短、无句末标点）
        heads = [block[r * rows] for r in range(cols)]
        if any(len(h) > 12 for h in heads):
            continue
        score = abs(cols - 4)
        if best is None or score < best[0]:
            best = (score, cols, rows, rem)
    if best is None:
        return None
    _s, cols, rows, _rem = best
    used = cols * rows
    grid = [block[r * rows:(r + 1) * rows] for r in range(cols)]
    table = [list(col) for col in zip(*grid)]
    out = ["| " + " | ".join(c.replace("|", "\\|") for c in table[0]) + " |",
           "|" + "|".join(["---"] * cols) + "|"]
    for row in table[1:]:
        out.append("| " + " | ".join(c.replace("|", "\\|") for c in row) + " |")
    return out, block[used:]


def process(md_text, fname, log):
    # 幂等：先移除上一轮写入的说明行
    lines = [l for l in md_text.split("\n")
             if not l.strip().startswith("> 说明：本文件由扫描件 OCR 生成")]
    counter = Counter()
    pages = split_pages(lines)
    boiler = find_boilerplate(pages)
    log.append("  %s：识别页眉/页脚 %d 条" % (fname, len(boiler)))

    out_pages = []
    for no, body in pages:
        new_body = []
        i = 0
        while i < len(body):
            ln = body[i]
            s = ln.strip()
            if s and (matches_boiler(s, boiler) or is_page_footer(s)):
                i += 1
                continue
            if s:
                s = apply_char_fixes(s, counter)
                ln = s if not ln.startswith(" ") else ln.replace(ln.strip(), s, 1)
                s = ln.strip()
            # 连续短行块：>=6 行才认为可能是表格/分栏区
            if short_body(s) is not None:
                j = i
                block = []
                blanks = 0
                while j < len(body):
                    t = body[j].strip()
                    if not t:
                        blanks += 1
                        if blanks > 1:
                            break
                        j += 1
                        continue
                    tb = short_body(apply_char_fixes(t, counter))
                    if tb is None:
                        break
                    block.append(tb)
                    blanks = 0
                    j += 1
                if len(block) >= 6:
                    res = try_table(block)
                    new_body.append("")
                    if res:
                        tbl, leftover = res
                        new_body.append("<!-- 表格区（按 OCR 行序重建，列划分可能有偏差） -->")
                        new_body.extend(tbl)
                        if leftover:
                            new_body.append("")
                            new_body.extend(leftover)
                    else:
                        new_body.append("<!-- 原表格区：OCR 未保留列结构，以下按阅读顺序（逐列）排列 -->")
                        for b in block:
                            new_body.append(b)
                    new_body.append("")
                    i = j
                    continue
            new_body.append(ln)
            i += 1
        out_pages.append((no, new_body))

    out = [NOTE_LINE, ""]
    for no, body in out_pages:
        out.append("<!-- 第 %d 页 -->" % no)
        out.extend(body)
        out.append("")
    text = "\n".join(out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    log.append("  形近字修正：%s" % (", ".join("%s×%d" % (k, v) for k, v in counter.most_common()) or "无"))
    return text


def main():
    targets = []
    for f in scan(".pdf"):
        has, _t, _n = pdf_has_text(f)
        if has:
            continue
        rel = os.path.relpath(f, SRC)
        md = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        if os.path.exists(md):
            targets.append((os.path.basename(f), md))
    log = ["# OCR 修复报告", ""]
    for name, md in targets:
        before = io.open(md, encoding="utf-8").read()
        n_before = len(before)
        after = process(before, name, log)
        io.open(md, "w", encoding="utf-8").write(after)
        log.append("  %s: %d -> %d chars" % (name, n_before, len(after)))
        log.append("")
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(log))
    print("\n".join(log))


if __name__ == "__main__":
    main()
