# -*- coding: utf-8 -*-
"""md_clean.py -- 转换产物的编码异常与格式混乱修复（就地改写，原文件自动备份）。

处理项：
  1. BOM / NUL / 控制字符 / U+FFFD(替换符) 清理
  2. 换行归一（CRLF、CR -> LF）、行尾空白、连续空行折叠
  3. 全角空格与零宽字符处理
  4. 结尾空行归一
  5. 质量统计：乱码嫌疑、空文件、过短文件

用法：
  python md_clean.py            # 演练，只出报告
  python md_clean.py --apply    # 实际改写（备份到 temp/md_clean_backup/）
"""
import os
import io
import re
import sys
import time
import shutil

TMP = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(TMP)
AREAS = [os.path.join(SOURCE, d) for d in ("第二批提取后", "第一批提取后", "教材_转化")]
BACKUP = os.path.join(TMP, "md_clean_backup")
EMPTY_DIR = os.path.join(TMP, "第二批_空md_20260910")
PROGRESS = os.path.join(TMP, "md_clean_progress.txt")
REPORT = os.path.join(TMP, "md清洗报告.txt")

APPLY = "--apply" in sys.argv
CTRL = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]")
ZERO = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")
MOJI = re.compile(r"[\ue000-\uf8ff\ufffd]")

log = []


def say(m):
    log.append(m)
    print(m)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as f:
            f.write("\n".join(log[-40:]))
    except Exception:
        pass


def clean(text):
    orig = text
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = CTRL.sub("", text)
    text = ZERO.sub("", text)
    text = MOJI.sub("", text)          # 替换符与私用区字符（解码失败的残渣）
    text = text.replace("\u00a0", " ")
    text = text.replace("\u3000", "  ")
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.rstrip() + "\n"
    return text, text != orig


def suspicious(text):
    """乱码嫌疑：私用区/替换符多，或可打印字符占比低。"""
    if not text.strip():
        return "空文件"
    bad = len(MOJI.findall(text))
    if bad >= 10:
        return "替换符/私用区 %d 个" % bad
    sample = text[:3000]
    good = sum(1 for c in sample
               if 0x4E00 <= ord(c) <= 0x9FFF or 32 <= ord(c) < 127
               or ord(c) in (10, 9) or 0x3000 <= ord(c) <= 0x303F)
    if good / max(len(sample), 1) < 0.55:
        return "可打印字符占比低"
    return ""


def main():
    t0 = time.time()
    n = fixed = n_fffd = n_empty = n_short = pruned = 0
    suspects = []
    for area in AREAS:
        if not os.path.isdir(area):
            continue
        for dp, _dn, fn in os.walk(area):
            for f in fn:
                if not f.lower().endswith(".md"):
                    continue
                p = os.path.join(dp, f)
                n += 1
                try:
                    raw = open(p, "rb").read()
                    text = raw.decode("utf-8", "replace")
                except OSError:
                    continue
                had_fffd = "\ufffd" in text
                if had_fffd:
                    n_fffd += 1
                new, changed = clean(text)
                why = suspicious(new)
                if why:
                    suspects.append((os.path.relpath(p, SOURCE), why))
                if len(new.strip()) < 100:
                    n_short += 1
                    if not new.strip():
                        n_empty += 1
                if not new.strip():
                    # 完全无内容的空壳 md：移出语料区（备份后移动，不用 os.remove）
                    if APPLY:
                        rel = os.path.relpath(p, SOURCE)
                        b = os.path.join(BACKUP, rel)
                        os.makedirs(os.path.dirname(b), exist_ok=True)
                        if not os.path.exists(b):
                            shutil.copy2(p, b)
                        d = os.path.join(EMPTY_DIR, rel)
                        os.makedirs(os.path.dirname(d), exist_ok=True)
                        try:
                            shutil.move(p, d)
                            pruned += 1
                        except OSError:
                            pass
                    continue
                if changed and APPLY:
                    rel = os.path.relpath(p, SOURCE)
                    b = os.path.join(BACKUP, rel)
                    os.makedirs(os.path.dirname(b), exist_ok=True)
                    if not os.path.exists(b):
                        shutil.copy2(p, b)
                    with io.open(p, "w", encoding="utf-8") as fp:
                        fp.write(new)
                    fixed += 1
                elif changed:
                    fixed += 1
                if n % 500 == 0:
                    say("扫描 %d 个（改写 %d）" % (n, fixed))

    say("")
    say("md 清洗报告  模式=%s" % ("实际改写 APPLY" if APPLY else "演练 DRY-RUN"))
    say("扫描 md      : %d" % n)
    say("需要规范化   : %d" % fixed)
    say("含替换符     : %d" % n_fffd)
    say("过短(<100字) : %d（其中空文件 %d）" % (n_short, n_empty))
    say("乱码嫌疑     : %d" % len(suspects))
    say("移出空壳 md  : %d -> %s" % (pruned, EMPTY_DIR))
    say("耗时 %.1f 分钟" % ((time.time() - t0) / 60.0))
    say("--- 乱码嫌疑清单（前 60）---")
    for rel, why in suspects[:60]:
        say("  %s  << %s" % (rel, why))
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("MD_CLEAN DONE n=%d fixed=%d suspects=%d" % (n, fixed, len(suspects)))


if __name__ == "__main__":
    main()
