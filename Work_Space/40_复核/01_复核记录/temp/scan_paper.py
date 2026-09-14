# -*- coding: utf-8 -*-
"""论文内容基线复核 · 自定义扫描（只读）
输出四类结果：图引用完整性 / 称形与用语 / 内部代号残留 / 图表占位交叉核对
临时脚本，只读工作区文件，结果打印到 stdout。
"""
import re, sys, io, os
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"C:\Users\wang-\Desktop\2026数学建模\Work_Space")
DRAFTS = ROOT / "50_论文" / "02_章节稿"
FILES = sorted(p for p in DRAFTS.glob("A_*.md"))

def body_of(text):
    """截掉文件头元信息（---之前）与占位清单/自查之后的部分，只留正文。"""
    # 去掉头部 > 引用块（至第一个 --- ）
    m = re.search(r"^---\s*$", text, re.M)
    t = text[m.end():] if m else text
    # 截到 占位清单 或 自查 标题
    for tag in ("## 占位清单", "## 自查", "# 占位清单", "# 自查", "## 六、本章图与表"):
        i = t.find(tag)
        if i != -1:
            t = t[:i]
    return t

print("=" * 30, "一、图引用完整性（正文行内引用 vs 本文件登记）", "=" * 30)
for p in FILES:
    text = p.read_text(encoding="utf-8")
    body = body_of(text)
    # 正文行内引用的 图x-y / 图 x-y（含全角空格）
    refs = set(re.findall(r"图\s*(\d+[-–]\d+)", body))
    # 本文件 §六 表或占位清单登记的 图x-y（登记列）
    reg = set(re.findall(r"\|\s*[`]?图\s*(\d+[-–]\d+)[`]?(\(\w\))?\s*\|", text))
    reg_ids = set(a for a, b in reg)
    never = sorted(reg_ids - refs, key=lambda s: (int(s.split("-")[0]), int(s.split("-")[1].replace("–","-"))))
    # 引用了但未登记
    unreg = sorted(refs - reg_ids)
    if never or unreg:
        print(f"\n[{p.name}]")
        if never:
            print(f"  登记但正文未引用: {never}")
        if unreg:
            print(f"  正文引用但未登记: {unreg}")

print()
print("=" * 30, "二、称形与用语一致性", "=" * 30)
pats = {
    "问题一(汉字)": r"问题一",
    "问题 1(阿拉伯)": r"问题 ?1(?![0-9])",
    "“创新”出现": r"创新",
    "杜邦积分": r"杜邦积分",
    "Duhamel": r"Duhamel|杜阿美尔|杜哈梅",
    "干基": r"干基",
    "kg/kg 全角": r"ｋｇ",
}
for name, pat in pats.items():
    row = []
    for p in FILES:
        body = body_of(p.read_text(encoding="utf-8"))
        n = len(re.findall(pat, body))
        if n:
            row.append(f"{p.name[2:5]}:{n}")
    print(f"  {name:12s}: " + ("  ".join(row) if row else "（0）"))

print()
print("=" * 30, "三、内部代号残留（正文区）", "=" * 30)
code_pats = [
    (r"(?<![A-Za-z0-9])E[0-9]{1,2}(?![0-9A-Za-z])", "E 检验号"),
    (r"(?<![A-Za-z0-9])M[1-9](?![0-9A-Za-z])", "M 口径"),
    (r"(?<![A-Za-z0-9(])H[0-9]{1,2}(?![0-9A-Za-z])", "H 假设号"),
    (r"(?<![A-Za-z0-9])O[0-9]{1,2}(?![0-9A-Za-z])", "O 口径"),
    (r"(?<![A-Za-z0-9])K1?[0-9](?![0-9])", "K 口径"),
    (r"MB-[0-9]+", "MB 语义"),
    (r"(?<![A-Za-z0-9])D-[0-9]+", "D 台账"),
    (r"(?<![A-Za-z0-9])RK-", "RK 复盘"),
    (r"(?<![A-Za-z0-9(])L3-[0-9]+", "L3 阶段"),
    (r"(?<![A-Za-z0-9])W-[0-9]+", "W 约束"),
    (r"(?<![A-Za-z0-9])F-[0-9]{2}", "F 规格卡"),
    (r"(?<![A-Za-z0-9])IN-[0-9]+", "IN 创新"),
    (r"(?<![A-Za-z0-9])S[0-9](-[0-9])?(?![0-9A-Za-z])", "S 项"),
    (r"T[123]-[0-9]", "T 创新项"),
    (r"(?<![A-Za-z0-9])Q[1-4]-[A-Za-z0-9]+", "Qx 内部号"),
    (r"(?<![A-Za-z0-9])N[0-9]{1,2}(?![0-9])", "N 数值口径"),
]
for p in FILES:
    body = body_of(p.read_text(encoding="utf-8"))
    hits = []
    for pat, label in code_pats:
        for m in re.finditer(pat, body):
            s = m.group(0)
            ln = body[: m.start()].count("\n") + 1
            hits.append((label, s, ln))
    if hits:
        print(f"\n[{p.name}]")
        for label, s, ln in hits[:20]:
            print(f"  L{ln}: {label} → {s}")
        if len(hits) > 20:
            print(f"  ... 共 {len(hits)} 处")

print()
print("=" * 30, "四、A_13 引用位置对照 ↔ 正文实际引用位置", "=" * 30)
t13 = (DRAFTS / "A_13_参考文献_基线.md").read_text(encoding="utf-8")
claim = {}
for m in re.finditer(r"\|\s*\[(\d+)\]\s*\|\s*([^|]+)\|", t13):
    claim[int(m.group(1))] = m.group(2).strip()
actual = {}
for p in FILES:
    if p.name.startswith("A_13"):
        continue
    body = body_of(p.read_text(encoding="utf-8"))
    for m in re.finditer(r"\[(\d{1,2})\]", body):
        ln = body[: m.start()].count("\n") + 1
        sec = ""
        for sm in re.finditer(r"^#{2,3} (.+)$", body[: m.start()], re.M):
            sec = sm.group(1)
        actual.setdefault(int(m.group(1)), []).append(f"{p.name[2:5]}·{sec[:18]}·L{ln}")
for k in sorted(claim):
    locs = actual.get(k, ["（正文未引用！）"])
    flag = "" if locs != ["（正文未引用！）"] else "  ← 列而不引"
    print(f"  [{k:>2}] 声称:{claim[k][:28]:30s} 实际:{'; '.join(locs[:3])}{flag}")

print()
print("=" * 30, "五、A_10 图A-x 占位 vs 检验章正文引用", "=" * 30)
t10 = (DRAFTS / "A_10_模型检验_基线.md").read_text(encoding="utf-8")
b10 = body_of(t10)
print("  检验章 6.1–6.10 正文内出现 图A- 引用：", re.findall(r"图A-\d+", b10) or "（0 处 — 全部未引用）")
