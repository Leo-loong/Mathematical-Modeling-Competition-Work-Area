# -*- coding: utf-8 -*-
"""H2 条目解析器：内容库 30 件 → entries.json（只读）"""
import re, json, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(r"C:\Users\wang-\Desktop\2026数学建模\Work_Space")
CD = ROOT / "50_论文" / "02_章节稿" / "章节内容库"
FIELDS = ["所属节", "类型", "条目", "依据", "数值口径", "关联图表", "关联文献",
          "目标篇幅", "状态", "验收判据", "风险／备注", "风险/备注", "变更痕"]

entries = []
modules = {}
for mod in range(1, 15):
    f = CD / f"A_{mod:02d}_" 
    files = list(CD.glob(f"A_{mod:02d}_*_内容条目.md"))
    if not files:
        modules[mod] = {"entries": 0, "file": None}
        continue
    p = files[0]
    text = p.read_text(encoding="utf-8")
    # 详表条目块
    blocks = re.split(r"\n(?=### \d{2}-)", text)
    n = 0
    for b in blocks:
        m = re.match(r"### (\d{2}-[\d.]+-\d{2,3})　?(.*)", b)
        if not m:
            continue
        eid, title = m.group(1), m.group(2).strip()
        body = b
        d = {"id": eid, "title": title, "module": mod, "file": p.name}
        # 逐字段：先整行匹配，再行内 ｜ 切分
        for line in body.splitlines():
            if not line.strip().startswith("- **"):
                continue
            # 拆出该行内的所有「**字段**：值」片段（同行多字段用 ｜ 分隔）
            for seg in re.split(r"\s*｜\s*", line.strip().lstrip("- ").strip()):
                sm = re.match(r"\*\*(.+?)\*\*：(.*)", seg.strip())
                if sm and sm.group(1) in FIELDS:
                    d[sm.group(1)] = sm.group(2).strip()
        entries.append(d)
        n += 1
    # 覆盖回勾节
    cov = []
    cm = re.search(r"## 三、覆盖回勾.*?(?=\n## |\Z)", text, re.S)
    if cm:
        for ln in cm.group(0).splitlines():
            if ln.strip().startswith("|") and not set(ln) <= set("|-: "):
                cov.append(ln.strip())
    modules[mod] = {"entries": n, "file": p.name, "cov_rows": len(cov)}

out = {"modules": modules, "entries": entries}
json.dump(out, open(Path(__file__).with_name("entries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
total = sum(m["entries"] for m in modules.values())
print(f"解析条目 {total} 条（模块分布：", {k: v["entries"] for k, v in modules.items()}, "）")
# 字段齐全性统计
need = ["所属节", "类型", "条目", "依据", "数值口径", "关联图表", "关联文献", "目标篇幅", "状态", "验收判据"]
missing = {}
for e in entries:
    miss = [f for f in need if f not in e or not e[f]]
    if miss:
        missing[e["id"]] = miss
print(f"字段缺失条目：{len(missing)}")
for k, v in list(missing.items())[:15]:
    print("  ", k, v)
# 状态分布
from collections import Counter
print("状态分布：", Counter(e.get("状态", "?") for e in entries))
print("类型分布：", Counter(e.get("类型", "?") for e in entries))
