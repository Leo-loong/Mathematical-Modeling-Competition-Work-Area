# -*- coding: utf-8 -*-
"""P5 报告生成：
  kb/index/MOC.md        全库文件地图（md/doc 逐篇；代码按目录汇总）
  kb/index/覆盖与缺口.md  方法覆盖统计 + 已识别缺口复核 + 转换↔原始源映射质检
路径全部由脚本位置动态推导（kb 可整体移动）。语料 path 相对工作区根。
"""
import os
import json
import sqlite3
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
SOURCE_ROOT = os.path.join(KB, "source")
DATA = os.path.join(HERE, "data")
import sys  # noqa: E402
sys.path.insert(0, HERE)
from p3_meta import ALIAS  # noqa: E402

GAP_CHECKS = {
    "薄膜干涉/光程差": ["薄膜干涉", "光程差", "等厚干涉", "双光束干涉"],
    "多光束干涉(Fabry-Pérot)": ["Fabry-Perot", "Fabry-Pérot", "多光束干涉", "Airy"],
    "折射率色散模型": ["Sellmeier", "Cauchy公式", "色散模型", "柯西"],
    "红外干涉测厚": ["红外测厚", "外延层厚度", "膜厚测量"],
    "国奖/优秀论文范例": ["优秀论文", "国奖论文", "获奖论文"],
    "碳化硅外延(SiC)": ["碳化硅", "SiC", "外延层"],
}


def main():
    with open(os.path.join(DATA, "files.json"), encoding="utf-8") as f:
        records = json.load(f)
    con = sqlite3.connect(os.path.join(DATA, "catalog.db"))
    cur = con.cursor()

    # ---------- MOC ----------
    md_recs = [r for r in records if r["kind"] == "md"]
    code_recs = [r for r in records if r["kind"] == "code"]
    doc_recs = [r for r in records if r["kind"] == "doc"]
    groups = defaultdict(list)
    for r in md_recs:
        groups[r["area"]].append(r)
    lines = ["# MOC — 全库文件地图", "",
             "> 由 kb/engine/p5_report.py 自动生成，检索请用 kb/engine/p5_search.py。",
             "> 路径相对工作区根。语料区动态发现：kb/source 下所有子目录（temp 除外）。",
             ""]
    lines.append("| 区域 | md 篇数 | 代码文件数 | 文献原件(文件名级) |")
    lines.append("|---|---|---|---|")
    area_stats = defaultdict(lambda: [0, 0, 0])
    for r in records:
        idx = {"md": 0, "code": 1, "doc": 2}.get(r["kind"])
        if idx is not None:
            area_stats[r["area"]][idx] += 1
    for area, (n_md, n_code, n_doc) in sorted(area_stats.items()):
        lines.append("| %s | %d | %d | %d |" % (area, n_md, n_code, n_doc))
    lines.append("")
    for top in sorted(groups):
        recs = sorted(groups[top], key=lambda r: r["path"])
        lines.append("## %s（%d 篇）" % (top, len(recs)))
        lines.append("")
        lines.append("| 标题 | 摘要 | 路径 |")
        lines.append("|---|---|---|")
        for r in recs:
            title = (r["title"] or os.path.basename(r["path"])).replace("|", "\\|")[:60]
            summary = (r["summary"] or "").replace("|", "\\|")[:80]
            lines.append("| %s | %s | %s |" % (title, summary, r["path"]))
        lines.append("")
    lines.append("## 文献原件索引（%d 个 PDF/DOC 等，文件名级可检索，转 md 后升级全文）" % len(doc_recs))
    lines.append("")
    lines.append("| 文件名 | 路径 |")
    lines.append("|---|---|")
    for r in sorted(doc_recs, key=lambda r: r["path"]):
        lines.append("| %s | %s |" % (r["title"].replace("|", "\\|"), r["path"]))
    lines.append("")
    code_dirs = defaultdict(int)
    for r in code_recs:
        code_dirs[os.path.dirname(r["path"])] += 1
    lines.append("## 代码资产目录索引（%d 个代码文件，按目录汇总）" % len(code_recs))
    lines.append("")
    lines.append("| 目录 | 代码文件数 |")
    lines.append("|---|---|")
    for d, n in sorted(code_dirs.items(), key=lambda kv: -kv[1]):
        lines.append("| %s | %d |" % (d.replace("\\", "/"), n))
    os.makedirs(os.path.join(KB, "index"), exist_ok=True)
    with open(os.path.join(KB, "index", "MOC.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # ---------- 覆盖与缺口 ----------
    rep = ["# 覆盖度与缺口报告", "",
           "> 自动生成（p5_report.py）。缺口判定基于 files 表 title/summary/keywords 命中数。", ""]
    rep.append("## 一、方法覆盖面（受控词表在库内的文件命中数 Top30）")
    rep.append("")
    rep.append("| 方法 | 库内命中文件数 |")
    rep.append("|---|---|")
    scores = []
    for std, aliases in ALIAS.items():
        pat = " OR ".join(["keywords LIKE '%%%s%%'" % a.replace("'", "''") for a in [std] + aliases])
        n = cur.execute("SELECT COUNT(*) FROM files WHERE " + pat).fetchone()[0]
        scores.append((std, n))
    for std, n in sorted(scores, key=lambda kv: -kv[1])[:30]:
        rep.append("| %s | %d |" % (std, n))
    rep.append("")
    rep.append("## 二、已识别缺口复核（结合资料充足性结论）")
    rep.append("")
    rep.append("| 主题 | 库内命中 | 判定 |")
    rep.append("|---|---|---|")
    for topic, kws in GAP_CHECKS.items():
        total = 0
        for kw in kws:
            total += cur.execute(
                "SELECT COUNT(*) FROM files WHERE title LIKE ? OR keywords LIKE ? OR summary LIKE ?",
                ("%%%s%%" % kw, "%%%s%%" % kw, "%%%s%%" % kw)).fetchone()[0]
        verdict = "有覆盖" if total >= 5 else ("薄弱" if total > 0 else "**缺口：库内无支撑**")
        rep.append("| %s | %d | %s |" % (topic, total, verdict))
    rep.append("")
    rep.append("## 三、转换↔原始源映射质检（第一批）")
    rep.append("")
    matched, missing = 0, []
    for r in md_recs:
        # 路径形如 kb/source/第一批提取后/...
        parts = r["path"].split("/")
        if len(parts) < 3 or parts[2] != "第一批提取后":
            continue
        name = os.path.basename(r["path"])
        rel_inside = "/".join(parts[3:-1]) if len(parts) > 4 else ""
        orig_base = os.path.join(SOURCE_ROOT, "第一批", rel_inside)
        stem = os.path.splitext(name)[0]
        cand = [os.path.join(orig_base, stem + e) for e in (".docx", ".pdf", ".doc")]
        if any(os.path.exists(c) for c in cand):
            matched += 1
        else:
            missing.append(name)
    rep.append("- 第一批提取后 md 总数: %d；可回溯原始文件: %d；未匹配: %d"
               % (matched + len(missing), matched, len(missing)))
    for m in missing[:20]:
        rep.append("  - 未匹配: %s" % m)
    rep.append("")
    rep.append("## 四、网盘选择性下载建议（按缺口优先级）")
    rep.append("")
    rep.append("1. 薄膜光学/物理光学教材相关章节（薄膜干涉、多光束干涉、Airy 公式）")
    rep.append("2. 折射率色散模型（Cauchy/Sellmeier/Drude）资料")
    rep.append("3. 红外干涉测厚方法文献（FFT 波数域变换、极值法、包络法）")
    rep.append("4. 近 3 年国奖论文 3–5 篇（现有范例命中偏少）")
    with open(os.path.join(KB, "index", "覆盖与缺口.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("P5 reports done. MOC=%d lines, gap report written." % len(lines))


if __name__ == "__main__":
    main()
