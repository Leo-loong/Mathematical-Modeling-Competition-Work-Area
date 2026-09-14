# -*- coding: utf-8 -*-
"""OCR 质量自动质检（L1 健康度 + L2 同源文本层对照）。

思路：
  L1 无需参考答案：空页/碎片行/低频可疑字/符号异常/数字密度。
  L2 利用本批资料的特点——同一份讲义往往同时存在"扫描版(无文本层)"和
     "文本版(有文本层)"，以后者为参考答案，用字符 n-gram 的
     「覆盖率(漏字?) / 精确率(错字?)」估计识别质量。
"""
import os
import re
import io
import sys
import json
import random

BASE = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source"
DST = os.path.join(BASE, "第一批提取后")
TMP = os.path.join(BASE, "temp")
REPORT = os.path.join(TMP, "OCR质检报告.txt")
sys.path.insert(0, TMP)
from convert_all import scan, pdf_has_text  # noqa: E402

# ---------- 文本归一化：只保留"内容字符"，去掉 Markdown 装饰 ----------
RE_COMMENT = re.compile(r"<!--.*?-->")
RE_TAG = re.compile(r"<[^>]{1,10}>")
RE_MD = re.compile(r"^[\s>#*\-|]+", re.M)
RE_PIPE = re.compile(r"\|")
RE_WS = re.compile(r"[\s\u3000]+")


def norm(md):
    s = RE_COMMENT.sub("", md)
    s = RE_TAG.sub("", s)
    s = RE_PIPE.sub("", s)
    s = RE_MD.sub("", s)
    s = RE_WS.sub("", s)
    return s


def strip_markup_pure(s):
    return s


# ---------- L1 指标 ----------
CJK = re.compile(r"[\u4e00-\u9fa5]")
DIGIT = re.compile(r"\d+(?:\.\d+)?")
NOISE_CHARS = set("'\"``\u2018\u2019\u201c\u201d\uFFFD\uFFFE\uFFEF")
# 常见 OCR 形近误识的繁体/异体字（本资料为简体）
TRAD_HINT = set("個國學數題問實際處於與產業務動機結構優點為這樣點無實現體關係複雜")


def l1_metrics(md):
    pages = re.split(r"<!--\s*第\s*\d+\s*页\s*-->", md)
    pages = [p for p in pages if p.strip()]
    n_page = len(pages)
    empty_pages = sum(1 for p in pages if len(CJK.findall(p)) < 10)
    body = [l.strip() for l in md.split("\n")
            if l.strip() and not l.strip().startswith("<!--")]
    lines = [l for l in body if not l.startswith("#")]
    if lines:
        lens = sorted(len(l) for l in lines)
        med_len = lens[len(lens) // 2]
        short = sum(1 for x in lens if x <= 3) / float(len(lines))
    else:
        med_len, short = 0, 0.0
    text = norm(md)
    cjk = CJK.findall(text)
    # 低频可疑字：仅出现 1~2 次的汉字占比（错字往往孤立出现）
    from collections import Counter
    cnt = Counter(cjk)
    rare = sum(1 for ch, c in cnt.items() if c <= 2)
    rare_rate = rare / float(len(cnt)) if cnt else 0.0
    noise = sum(1 for ch in text if ch in NOISE_CHARS)
    trad = sum(1 for ch in cjk if ch in TRAD_HINT)
    digits = DIGIT.findall(text)
    return dict(
        pages=n_page,
        empty_pages=empty_pages,
        empty_rate=round(empty_pages / n_page, 3) if n_page else 0,
        lines=len(lines),
        median_line_len=med_len,
        short_line_rate=round(short, 3),
        cjk_chars=len(cjk),
        rare_char_rate=round(rare_rate, 3),
        noise_char_rate=round(noise / max(1, len(text)), 4),
        trad_char_rate=round(trad / max(1, len(cjk)), 4),
        digit_tokens=len(digits),
    )


# ---------- L2 对照 ----------
def ngrams(s, n=4):
    return set(s[i:i + n] for i in range(0, max(0, len(s) - n + 1)))


def sample_grams(s, n=4, k=4000):
    g = [s[i:i + n] for i in range(0, max(0, len(s) - n + 1))]
    if len(g) <= k:
        return g
    step = len(g) / float(k)
    return [g[int(i * step)] for i in range(k)]


def compare(ref, ocr, n=4):
    """ref=文本层(参考答案), ocr=OCR结果。
    覆盖率 = ref 的 n-gram 在 ocr 中出现比例（低 => 漏内容）
    精确率 = ocr 的 n-gram 在 ref 中出现比例（低 => 错字多）"""
    ref_set = ngrams(ref, n)
    ocr_set = ngrams(ocr, n)
    if not ref_set or not ocr_set:
        return 0.0, 0.0
    probe = sample_grams(ref, n, 4000)
    coverage = sum(1 for g in probe if g in ocr_set) / float(len(probe))
    probe2 = sample_grams(ocr, n, 4000)
    precision = sum(1 for g in probe2 if g in ref_set) / float(len(probe2))
    return coverage, precision


def digit_recall(ref, ocr):
    from collections import Counter
    rc = Counter(DIGIT.findall(ref))
    oc = Counter(DIGIT.findall(ocr))
    if not rc:
        return 0.0
    hit = tot = 0
    for d, c in rc.most_common(300):
        tot += min(c, 3)
        hit += min(oc.get(d, 0), 3)
    return hit / float(tot)


def main():
    random.seed(7)
    ocr_files, text_files = [], []
    for f in scan(".pdf"):
        has, _t, _n = pdf_has_text(f)
        rel = os.path.relpath(f, os.path.join(BASE, "第一批"))
        md = os.path.join(DST, os.path.splitext(rel)[0] + ".md")
        if not os.path.exists(md):
            continue
        (text_files if has else ocr_files).append((os.path.basename(f), md))

    out = ["# OCR 质量质检报告", ""]
    out.append("## 一、L1 健康度（无需参考答案）")
    out.append("")
    out.append("%-46s %5s %6s %6s %6s %7s %7s" % (
        "文件", "页数", "空页率", "中位行长", "短行率", "低频字率", "繁体率"))
    store = {}
    for name, md in ocr_files + text_files:
        body = io.open(md, encoding="utf-8").read()
        m = l1_metrics(body)
        store[name] = (norm(body), m)
        tag = "OCR" if (name, md) in ocr_files else "TEXT"
        out.append("[%s] %-42s %5d %6.3f %6d %6.3f %7.3f %7.4f" % (
            tag, name[:42], m["pages"], m["empty_rate"],
            m["median_line_len"], m["short_line_rate"],
            m["rare_char_rate"], m["trad_char_rate"]))

    out.append("")
    out.append("## 二、L2 同源对照（以文本层文件为参考答案）")
    out.append("")
    out.append("%-40s %-30s %8s %8s %8s" % (
        "OCR 文件", "最佳匹配(文本层)", "覆盖率", "精确率", "数字召回"))
    for name, md in ocr_files:
        ocr_text, _m = store[name]
        best = None
        for tname, tmd in text_files:
            ref_text, _tm = store[tname]
            cov, pre = compare(ref_text, ocr_text)
            if best is None or (cov + pre) > (best[1] + best[2]):
                best = (tname, cov, pre, ref_text)
        if best is None:
            continue
        tname, cov, pre, ref_text = best
        dr = digit_recall(ref_text, ocr_text)
        out.append("%-40s %-30s %8.3f %8.3f %8.3f" % (
            name[:40], tname[:30], cov, pre, dr))
    out.append("")
    out.append("指标读法：覆盖率<0.9 说明有内容缺失；精确率<0.85 说明错字偏多；")
    out.append("数字召回<0.9 说明年份/参数等数字识别不可靠（对建模资料风险最高）。")
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(out))
    print("\n".join(out[-14:]))


if __name__ == "__main__":
    main()
