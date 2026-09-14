# -*- coding: utf-8 -*-
"""T2 查询完整性（召回率）验证。
A 账实核对：源目录可索引文本文件 与 files 表 双向差集。
B 召回探针：随机抽样文件，从正文单行内抽取特征片段作查询词（deep 模式），
  验证该文件能否被召回；未命中归类（低信息量/全局高频截断等）。
C 边界场景：2 字短词(LIKE 兜底)、代码标识符、大小写、OCR 错字(预期未命中)。
输出：data/t2_recall_report.txt
"""
import os
import re
import json
import random
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = HERE
ROOT = os.path.dirname(os.path.dirname(HERE))  # 工作区根（kb 的上级）
DATA = os.path.join(ENGINE, "data")
TEXT_EXTS = {".md", ".m", ".M", ".py", ".c", ".h", ".cpp", ".txt", ".html",
             ".csv", ".json", ".cls", ".bst", ".bib", ".dat", ".sty"}
sys_path = __import__("sys"); sys_path.path.insert(0, ENGINE)
from p5_search import search  # noqa: E402
from p3_meta import discover_areas  # noqa: E402  语料区口径与 p3 保持一致


def read_text_best(path):
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def walk_texts():
    out = []
    for area, base in discover_areas():
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in {"_无效内容"}]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() in TEXT_EXTS:
                    out.append(os.path.join(dirpath, fn))
    return out


def pick_probes(text, kind, k=2):
    """从单行内抽取特征查询片段。"""
    probes = []
    if kind == "code":
        ids = re.findall(r"\b[A-Za-z_][A-Za-z_0-9]{5,}\b", text)
        random.shuffle(ids)
        probes = ids[:k]
    else:
        cands = []
        for ln in text.split("\n"):
            s = ln.strip()
            if len(s) >= 24 and "<!--" not in s and not s.startswith("```"):
                cands.append(s)
        random.shuffle(cands)
        for s in cands[:k * 3]:
            seg = re.search(r"[\u4e00-\u9fff][\u4e00-\u9fffA-Za-z0-9，、：()]{5,18}", s)
            if seg:
                probes.append(seg.group(0)[:10])
            if len(probes) >= k:
                break
    return probes


def global_chunk_freq(term):
    con = sqlite3.connect(os.path.join(DATA, "catalog.db"))
    n = con.execute("SELECT COUNT(*) FROM chunks WHERE body LIKE ?",
                    ("%" + term + "%",)).fetchone()[0]
    con.close()
    return n


def main():
    rep = ["# T2 查询完整性验证\n"]
    # ---------- A 账实核对 ----------
    src_files = {os.path.relpath(p, ROOT).replace("\\", "/") for p in walk_texts()}
    with open(os.path.join(DATA, "files.json"), encoding="utf-8") as f:
        recs = json.load(f)
    db_files = {r["path"].replace("\\", "/") for r in recs}
    only_src = sorted(src_files - db_files)
    only_db = sorted(db_files - src_files)
    rep.append("## A 账实核对")
    rep.append("")
    rep.append("- 源可索引文本文件: %d；库内记录: %d" % (len(src_files), len(db_files)))
    rep.append("- 在源不在库(漏建): %d %s" % (len(only_src), only_src[:5] if only_src else ""))
    rep.append("- 在库不在源(悬空): %d %s" % (len(only_db), only_db[:5] if only_db else ""))

    # ---------- B 召回探针 ----------
    rep.append("")
    rep.append("## B 召回探针（正文特征片段 -> deep 查询应召回原文件）")
    rep.append("")
    by_kind = {"md": [], "code": [], "text": []}
    for r in recs:
        if r["kind"] in by_kind and r["nchars"] > 1000:
            by_kind[r["kind"]].append(r)
    random.seed(42)
    plan = [("md", 30), ("code", 20), ("text", 10)]
    total, hit, misses = 0, 0, []
    for kind, n in plan:
        sample = random.sample(by_kind[kind], min(n, len(by_kind[kind])))
        for r in sample:
            full = os.path.join(ROOT, r["path"])
            try:
                text = read_text_best(full)
            except OSError:
                continue
            for term in pick_probes(text, kind):
                if not term or len(term) < 2:
                    continue
                total += 1
                res, extra, _, _ = search(term, deep=True, limit=20)
                hit_paths = {x["path"] for x in res} | {x["path"] for x in extra}
                rel = r["path"].replace("\\", "/")
                if rel in hit_paths:
                    hit += 1
                else:
                    freq = global_chunk_freq(term)
                    misses.append((kind, os.path.basename(r["path"])[:40], term,
                                   "全局含该片段的块数=%d" % freq))
    rep.append("- 探针总数: %d；召回: %d；未命中: %d；**召回率 %.1f%%**"
               % (total, hit, len(misses), 100.0 * hit / max(total, 1)))
    for m in misses[:15]:
        rep.append("  - 未命中 [%s] %s :: %s (%s)" % m)

    # ---------- C 边界场景 ----------
    rep.append("")
    rep.append("## C 边界场景")
    rep.append("")
    cases = [
        ("2字短词(反演)", "反演", True),
        ("2字短词(拟合)", "拟合", True),
        ("英文大小写(MonteCarlo)", "MonteCarlo", True),
        ("纯英文小写(particle swarm)", "particle", True),
        ("OCR错字(蒙特卡罗写法)", "蒙特卡罗", True),
        ("无意义串(预期未命中)", "阿西莫夫三定律", False),
    ]
    for name, q, expect_hit in cases:
        res, extra, _, _ = search(q, deep=True, limit=10)
        got = len(res) + len(extra) > 0
        verdict = "命中%d条" % (len(res) + len(extra)) if got else "未命中"
        status = "OK" if got == expect_hit else "注意"
        rep.append("- %-24s 查询=%-18s -> %s [%s]" % (name, q, verdict, status))
    rep.append("")
    rep.append("## 已知查不出的内容（设计边界，非缺陷）")
    rep.append("1. 扫描件 PDF/CAJ/PPT/VSS：仅文件名与目录可检索（正文是图片/二进制）")
    rep.append("2. OCR 形近字错字：按原文错字存储，需用错字或别名才能命中（词表可补）")
    rep.append("3. 语义改述（正文不含查询用词）：词法引擎不召回，需扩充别名词表")
    rep.append("4. <3 字符的英文词：trigram 下限，已由 LIKE 兜底，但代码海量短词时排序变弱")
    with open(os.path.join(ENGINE, "data", "t2_recall_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("T2 done. probes=%d recall=%.1f%%" % (total, 100.0 * hit / max(total, 1)))


if __name__ == "__main__":
    main()
