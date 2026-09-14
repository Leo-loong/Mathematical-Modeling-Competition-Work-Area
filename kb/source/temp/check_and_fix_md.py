# -*- coding: utf-8 -*-
"""两批次提取后 Markdown 的联合体检 + 自动修复。

检查项（均可能造成 Agent 读取阻塞/浪费上下文）：
  1. 编码非 UTF-8 / 带 BOM / 含替换字符 U+FFFD
  2. 空文件、过短文件
  3. 超长行（单行无换行，读取会爆上下文）
  4. 超大文件
  5. 重复行占比异常（OCR 死循环）
  6. 控制字符 / 二进制残留
  7. Markdown 结构：未闭合代码块、表格分隔符异常
  8. 乱码率（非常用字符比例）

可自动修复的：编码统一 UTF-8 无 BOM、去控制字符、闭合代码块、
超长行按标点软换行、空文件与低质量文件加头部警示、超大文件生成摘要版。
"""
import os
import io
import re
import sys
import hashlib
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B1 = os.path.join(BASE, "第一批提取后")
B2 = os.path.join(BASE, "第二批提取后")
REPORT = os.path.join(BASE, "temp", "提取内容联合检查报告.txt")
FIXLOG = os.path.join(BASE, "temp", "修复明细.txt")

MAX_LINE = 2000          # 单行超过此长度做软换行
BIG_FILE = 400 * 1024    # 超过 400KB 视为超大文件
MIN_USEFUL = 50          # 少于此字符数视为无效内容
CJK = re.compile(r"[\u4e00-\u9fa5]")
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
REPEAT_WINDOW = 30

fixlog = []
stat = Counter()


def read_raw(path):
    with open(path, "rb") as f:
        return f.read()


def decode_fix(raw):
    """尽量正确解码，返回 (text, 编码名, 是否有替换字符)"""
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
        enc = "utf-8-bom"
    else:
        enc = "?"
    for e in ("utf-8", "gb18030"):
        try:
            t = raw.decode(e)
            if e != "utf-8":
                enc = e
            elif enc == "?":
                enc = "utf-8"
            return t, enc, ("\ufffd" in t)
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8/replace", True


def longest_line(text):
    return max((len(l) for l in text.split("\n")), default=0)


def repeat_ratio(lines):
    if len(lines) < REPEAT_WINDOW:
        return 0.0
    cnt = Counter(l.strip() for l in lines if l.strip())
    if not cnt:
        return 0.0
    top = cnt.most_common(1)[0][1]
    return top / float(len(lines))


def garble_rate(text):
    """非常用字符（私用区/替换符/不可见）比例。"""
    if not text:
        return 0.0
    bad = sum(1 for ch in text
              if ch == "\ufffd" or 0xe000 <= ord(ch) <= 0xf8ff)
    return bad / float(len(text))


def soft_wrap(line, width=MAX_LINE):
    """按中文标点断行，避免超长行。"""
    if len(line) <= width:
        return [line]
    PUNCT = "。；！？，、：；,.;!?"
    out, buf = [], ""
    for ch in line:
        buf += ch
        if len(buf) >= width and ch in PUNCT:
            out.append(buf)
            buf = ""
        elif len(buf) > width:
            # 已超宽且未遇标点：按宽度硬切，保证行宽严格受控
            out.append(buf[:width])
            buf = buf[width:]
    # 无标点可断（长代码/长数字串/长 URL）时强制按宽度切，保证行宽可控
    while len(buf) > width:
        out.append(buf[:width])
        buf = buf[width:]
    if buf:
        out.append(buf)
    return out


def fix_code_fences(text):
    n = text.count("```")
    if n % 2 == 1:
        return text.rstrip() + "\n```\n"
    return text


def summarize(text, keep=8000):
    """超大文件：保留开头 keep 字符 + 结尾 2000 字符，并说明已截断。"""
    head = text[:keep]
    tail = text[-2000:] if len(text) > keep + 2000 else ""
    return (head
            + "\n\n<!-- 本文件过大，已生成摘要版本；完整内容请读取同名原始文件 -->\n\n"
            + tail)


def process(path, root):
    rel = os.path.relpath(path, root)
    raw = read_raw(path)
    text, enc, has_fffd = decode_fix(raw)
    info = dict(rel=rel, enc=enc, size=len(raw))
    changed = False

    # 1) 控制字符清理
    if CTRL.search(text):
        text = CTRL.sub("", text)
        changed = True
        stat["清理控制字符"] += 1
        fixlog.append("[控制字符] " + rel)

    # 1b) 清理替换字符 / 私用区乱码字符（无意义，且会让 Agent 读取困惑）
    if "\ufffd" in text or any(0xe000 <= ord(c) <= 0xf8ff for c in text):
        text = re.sub(r"[\ue000-\uf8ff\ufffd]", "", text)
        changed = True
        stat["清理乱码字符"] += 1
        fixlog.append("[乱码字符] " + rel)

    # 2) 超长行软换行
    ll = longest_line(text)
    if ll > MAX_LINE:
        new = []
        for l in text.split("\n"):
            new.extend(soft_wrap(l))
        text = "\n".join(new)
        changed = True
        stat["超长行换行"] += 1
        fixlog.append("[超长行 %d] %s" % (ll, rel))

    # 3) 代码块闭合
    t2 = fix_code_fences(text)
    if t2 != text:
        text = t2
        changed = True
        stat["闭合代码块"] += 1
        fixlog.append("[代码块未闭合] " + rel)

    # 4) 质量判定
    lines = text.split("\n")
    rr = repeat_ratio(lines)
    gr = garble_rate(text)
    cjk = len(CJK.findall(text))
    useful = len(text.strip())
    info.update(lines=len(lines), cjk=cjk, repeat=round(rr, 3),
                garble=round(gr, 4), chars=useful, maxline=ll)

    flags = []
    if useful < MIN_USEFUL:
        flags.append("内容过少/空文件")
        stat["空或过少"] += 1
    if rr > 0.5:
        flags.append("重复行占比过高")
        stat["重复行异常"] += 1
    if gr > 0.02:
        flags.append("乱码率过高")
        stat["乱码"] += 1
    if has_fffd:
        flags.append("含替换字符")
        stat["替换字符"] += 1
    if len(raw) > BIG_FILE:
        flags.append("超大文件")
        stat["超大文件"] += 1

    # 5) 超大文件 -> 生成摘要版（原始 .md 改名保留）
    if len(raw) > BIG_FILE:
        base, ext = os.path.splitext(path)
        full = base + ".full" + ext
        if not os.path.exists(full):
            with io.open(full, "w", encoding="utf-8") as f:
                f.write(text)
        text = summarize(text)
        changed = True
        fixlog.append("[超大文件摘要化] " + rel)

    # 6) 有问题的文件加头部警示（便于 Agent 判断是否值得读）
    if flags:
        warn = ("> [自动质检] " + "；".join(flags)
                + "（字符 %d / 行 %d / 中文 %d）\n\n" % (useful, len(lines), cjk))
        if not text.startswith("> [自动质检]"):
            text = warn + text
            changed = True
        fixlog.append("[标记] %s -> %s" % (rel, "、".join(flags)))

    # 7) 统一写回 UTF-8 无 BOM
    if changed or enc != "utf-8" or has_fffd:
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(text)
        stat["写回"] += 1
    return info


def main():
    rows = []
    for root in (B1, B2):
        if not os.path.isdir(root):
            continue
        for dp, _dn, fn in os.walk(root):
            # 跳过隔离子目录，避免对完整版/数据文件重复处理（会递归生成 .full.full.md）
            if any(k in dp for k in ("_数据文件", "_无效内容", "_完整版")):
                continue
            for f in sorted(fn):
                if not f.lower().endswith(".md"):
                    continue
                p = os.path.join(dp, f)
                try:
                    rows.append(process(p, root))
                except Exception as e:
                    fixlog.append("[处理异常] %s %r" % (p, e))
                    stat["异常"] += 1
    rows.sort(key=lambda r: -r.get("chars", 0))

    out = ["# 两批次提取内容联合检查报告", ""]
    out.append("检查文件数: %d" % len(rows))
    out.append("")
    out.append("## 一、总体统计")
    total = sum(r.get("chars", 0) for r in rows)
    out.append("总字符数: %d" % total)
    out.append("总中文字符: %d" % sum(r.get("cjk", 0) for r in rows))
    out.append("")
    out.append("## 二、问题分布")
    for k, v in stat.most_common():
        out.append("  %-16s %d" % (k, v))
    out.append("")
    out.append("## 三、需要关注的文件（按字符数降序前 60）")
    out.append("%-10s %-8s %-8s %-8s %s" % ("字符", "行", "重复率", "乱码", "文件"))
    for r in rows[:60]:
        out.append("%-10d %-8d %-8s %-8s %s" % (
            r.get("chars", 0), r.get("lines", 0), r.get("repeat", 0),
            r.get("garble", 0), r.get("rel", "")[:80]))
    out.append("")
    out.append("## 四、问题文件清单（内容过少/重复/乱码）")
    for r in rows:
        if r.get("chars", 0) < MIN_USEFUL or r.get("repeat", 0) > 0.5 \
                or r.get("garble", 0) > 0.02:
            out.append("  %s  (字符 %d, 行 %d, 重复 %s, 乱码 %s)" % (
                r.get("rel", ""), r.get("chars", 0), r.get("lines", 0),
                r.get("repeat", 0), r.get("garble", 0)))
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))
    with io.open(FIXLOG, "w", encoding="utf-8") as fp:
        fp.write("\n".join(fixlog))
    print("CHECKED=%d ISSUES=%s" % (len(rows), dict(stat)))


if __name__ == "__main__":
    main()
