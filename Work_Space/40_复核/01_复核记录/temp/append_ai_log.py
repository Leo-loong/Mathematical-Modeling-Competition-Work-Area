# -*- coding: utf-8 -*-
"""AI 工具使用登记 · 简化增量追加（实际执行版留痕）
用户指示（本阶段起）：AI 登记从简——仅向处置登记表（末表）追加一行；幂等可重跑。
"""
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

P = r"C:\Users\wang-\Desktop\2026数学建模\Work_Space\20_交付包\12_AI工具使用详情\A_AI工具使用登记.json"
d = json.load(open(P, encoding="utf-8"))
t = [b for b in d["blocks"] if b.get("type") == "table"][-1]  # 处置登记表（末表）
row = ["92", "论文内容基线全面复核（PR-01…PR-38）",
       "「报告与台账可以直接写…现在正式开始执行」＋「后续简化AI工具使用登记」",
       "六阶段复核：机检＋表1–6逐格211/211＋覆盖度＋kb对标＋取舍；登记报告与台账；未改章节稿/数值/交付物",
       "40_复核/01_复核记录/0913_论文内容基线全面复核.md；02_差异台账 §十八；temp 脚本",
       "paper_lint ❌0；build_indexes 四表一致；PR 系列待用户批复"]
if not any(str(r[0]).strip("*") == "92" for r in t["rows"]):
    t["rows"].append(row)
json.dump(d, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("已登记（幂等）：", t["rows"][-1][0])
