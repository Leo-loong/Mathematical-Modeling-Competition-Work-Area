# -*- coding: utf-8 -*-
"""把 Windows 内置 OCR 输出的行文本（tsv）组装为 Markdown。

无坐标信息，故用「行序 + 行宽」启发式重建段落：
  - 满行（接近本页最大行宽）视为续行，与上一行同属一段；
  - 短行视为段落结尾，之后分段；
  - 编号/篇/章/项目符号等模式识别为标题或列表。
"""
import os
import re
import io
import sys
import json

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
SRC = os.path.join(BASE, "第一批")
DST = os.path.join(BASE, "第一批提取后")
TMP = os.path.join(BASE, "temp")
TSV = os.path.join(TMP, "ocr_tsv")

RE_PREF = re.compile(r"^第\s*[0-9一二三四五六七八九十]{1,3}\s*[篇章节部]")
RE_NUMSEC = re.compile(r"^\s*(\d+(?:[.．]\d+)*)\s*[、\.．]?\s*\S")
RE_PAREN = re.compile(r"^\s*[（(]\s*[0-9一二三四五六七八九十]{1,3}\s*[）)]\s*\S")
RE_BRACKET = re.compile(r"^\s*【[^】]{1,40}】\s*[:：]?\s*$")
RE_BULLET = re.compile(r"^\s*[.．·•\-—※*]\s*(.*)$")
RE_PAGE_NO = re.compile(r"^\s*[-–—]?\s*\d{1,4}\s*[-–—]?\s*$")


_ASCII_LETTER = re.compile(r"[A-Za-z]")


def collapse(s):
    """去掉 OCR 在汉字/全角标点/数字之间插入的多余空格。
    仅当空格两侧至少有一个是 ASCII 字母时（西文单词边界）才保留空格。"""
    out = []
    for i, ch in enumerate(s):
        if ch == " ":
            prev = out[-1] if out else ""
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if not (_ASCII_LETTER.match(prev or " ") or _ASCII_LETTER.match(nxt or " ")):
                continue
        out.append(ch)
    return "".join(out).strip()


def read_tsv(path):
    rows = []
    with io.open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            text = parts[4] if len(parts) >= 5 else line
            rows.append(collapse(text))
    return [r for r in rows if r]


def classify(line, full_width):
    """返回 (kind, payload)。"""
    s = line.strip()
    if not s:
        return ("blank", "")
    if RE_PAGE_NO.match(s) and len(s) <= 6:
        return ("skip", "")
    if RE_BULLET.match(s):
        body = RE_BULLET.match(s).group(1).strip()
        if body:
            return ("list", body)
    if RE_BRACKET.match(s):
        return ("h3", s)
    if len(s) <= 45 and RE_PREF.match(s):
        return ("h2", s)
    if len(s) <= 45 and RE_NUMSEC.match(s):
        dots = len(re.findall(r"[.．]", RE_NUMSEC.match(s).group(1)))
        return ("h2" if dots == 0 else ("h3" if dots == 1 else "h4"), s)
    if len(s) <= 40 and RE_PAREN.match(s):
        return ("h4", s)
    if full_width:
        return ("plain", s)
    # 短行：可能是小标题或段落末行
    if len(s) <= 30 and not s.endswith(("。", "！", "？", "：", "；", "，", "、", ":", "”")):
        return ("h3", s)
    return ("plain", s)


def page_to_lines(rows):
    if not rows:
        return []
    widths = sorted(len(r) for r in rows)
    W = widths[-1] if len(widths) < 3 else widths[int(len(widths) * 0.9)]
    out = []
    prev_blank = True
    for r in rows:
        # 只有明显短于版心宽度（<70%）的行才视作段落结尾，避免段内被切断
        full = len(r) >= max(12, W * 0.70)
        kind, payload = classify(r, full)
        if kind == "skip":
            continue
        if kind == "blank":
            continue
        if kind == "list":
            out.append("- " + payload)
            prev_blank = False
            continue
        if kind in ("h2", "h3", "h4"):
            lvl = {"h2": 2, "h3": 3, "h4": 4}[kind]
            out.append("")
            out.append("#" * lvl + " " + payload)
            out.append("")
            prev_blank = True
            continue
        if not full and not prev_blank:
            out.append("")
        out.append(payload)
        prev_blank = False
    return out


def main():
    meta = json.load(io.open(os.path.join(TMP, "ocr_map.json"), encoding="utf-8"))
    names = meta["files"]
    counts = meta["counts"]
    total = 0
    for i, rel in enumerate(names):
        lines = []
        missing = 0
        for pno in range(counts[i]):
            tsv = os.path.join(TSV, "%02d_%04d.tsv" % (i, pno))
            if not os.path.exists(tsv):
                missing += 1
                continue
            lines.append("<!-- 第 %d 页 -->" % (pno + 1))
            lines.extend(page_to_lines(read_tsv(tsv)))
            lines.append("")
        body = "\n".join(lines).rstrip() + "\n"
        while "\n\n\n" in body:
            body = body.replace("\n\n\n", "\n\n")
        dst = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with io.open(dst, "w", encoding="utf-8") as f:
            f.write(body)
        total += len(body)
        print("WRITE %s chars=%d missing_pages=%d" % (os.path.basename(rel), len(body), missing))
    print("TOTAL chars", total)


if __name__ == "__main__":
    main()
