# -*- coding: utf-8 -*-
"""为 `02_章节稿/成文/A_*.md` 的**正文**加脚本可识别标记（幂等）。

标记（HTML 注释，Markdown 渲染时不可见）：
    <!-- LATEX-EXPORT:BEGIN -->
    …正文…
    <!-- LATEX-EXPORT:END -->

职责边界：标记**只圈定正文** —— 文首的「元信息块 / 占位清单 / 自查 / 撰写说明」与文末的
「元信息（定稿交排版前整块删除）」及其后续小节**一律在标记之外**，故下游生成器无需再判断
哪些内容不进论文。每份稿的正文起止以**显式签名**给出（见 SPEC），运行时逐条校验命中数，
命中 ≠ 1 即报错并终止（不猜、不近似）。

用法：
    python 50_论文/02_章节稿/mark_body.py            # 校验/预演（不改文件）
    python 50_论文/02_章节稿/mark_body.py --apply    # 落盘
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BODY_DIR = os.path.join(HERE, "成文")
APPLY = "--apply" in sys.argv
BEGIN = "<!-- LATEX-EXPORT:BEGIN -->"
END = "<!-- LATEX-EXPORT:END -->"

# 每份稿：正文**首行签名** + 正文**终止签名**（终止行本身不进正文）
SPEC = {
    # A_01 的正文**只有题名一行**：题名之后紧跟的元信息块与各内部小节**一律不进正文**，
    # 故终止签名取「元信息块首行」而非「占位清单」（否则元信息块会被圈进正文）。
    "A_01_题目.md":         ("# 药材的烘干问题",           "> **【以下为章节稿元信息"),
    "A_02_摘要.md":         ("## 摘要（成文正文）",         "## 成文修正（相对基线）"),
    "A_03_关键词.md":       ("## 一、选择理由",             "## 二、独立核验"),
    "A_04_问题重述.md":     ("## 一、问题重述",             "## 成文修正（相对基线）"),
    "A_05_问题分析.md":     ("## 一、总体判断",             "## 成文修正（相对基线）"),
    "A_06_模型假设.md":     ("## 一、模型假设",             "## 成文修正（相对基线）"),
    "A_07_符号说明.md":     ("## 一、符号说明",             "## 成文修正（相对基线）"),
    "A_08_模型建立与求解.md": ("# 五、模型建立与求解",       "## 元信息（定稿交排版前整块删除）"),
    "A_09_结果分析.md":     ("# 5.5 四问结果",             "## 元信息（定稿交排版前整块删除）"),
    "A_10_模型检验.md":     ("# 六、模型检验",             "## 元信息（定稿交排版前整块删除）"),
    "A_11_模型评价与改进.md": ("# 七、模型评价与推广",       "## 元信息（定稿交排版前整块删除）"),
    "A_12_AI工具使用声明.md": ("# AI 工具使用声明",          "## 元信息（定稿交排版前整块删除）"),
    "A_13_参考文献.md":     ("# 参考文献",                 "## 元信息（定稿交排版前整块删除）"),
    "A_14_附录.md":         ("# 附录",                     "## 元信息（定稿交排版前整块删除）"),
}

ok = bad = skip = 0
print("正文标记（%s）" % ("落盘" if APPLY else "预演"))
for fn in sorted(SPEC):
    path = os.path.join(BODY_DIR, fn)
    if not os.path.isfile(path):
        print("  ✗ 缺文件：%s" % fn)
        bad += 1
        continue
    lines = io.open(path, encoding="utf-8").read().split("\n")
    b_sig, t_sig = SPEC[fn]

    if BEGIN in lines and END in lines:                    # 幂等
        bi, ei = lines.index(BEGIN), lines.index(END)
        print("  ✅ 已有标记  %-24s 正文 %d 行 ｜ 首「%s」｜ 末「%s」"
              % (fn, ei - bi - 1, lines[bi + 1][:18],
                 lines[ei - 1][:18] if ei > bi + 1 else ""))
        skip += 1
        continue

    hit_b = [i for i, l in enumerate(lines) if l.startswith(b_sig)]
    hit_t = [i for i, l in enumerate(lines) if l.startswith(t_sig)]
    if len(hit_b) != 1 or len(hit_t) != 1 or hit_t[0] <= hit_b[0]:
        print("  ✗ 签名不唯一/顺序异常  %s ｜ 首行命中 %d ｜ 终止命中 %d"
              % (fn, len(hit_b), len(hit_t)))
        bad += 1
        continue

    bi, ti = hit_b[0], hit_t[0]
    # 末端回退：丢弃正文末的**空行与分隔线（`---`）**，让 END 紧贴正文最后一行实内容
    while ti - 1 > bi and lines[ti - 1].strip() in ("", "---"):
        ti -= 1
    new = lines[:bi] + [BEGIN] + lines[bi:ti] + [END] + lines[ti:]
    body = [l for l in lines[bi:ti] if l.strip()]
    print("  ➕ 插标记    %-24s 正文 %d 行（含空行 %d 行）｜ 首「%s」｜ 末「%s」"
          % (fn, len(body), ti - bi, body[0][:18], body[-1][:18]))
    if APPLY:
        io.open(path, "w", encoding="utf-8", newline="").write("\n".join(new))
    ok += 1

print("\n合计：新插 %d ｜ 已有 %d ｜ 失败 %d ⟹ %s"
      % (ok, skip, bad, "全部就绪 ✅" if not bad else "须处理 ✗"))
sys.exit(1 if bad else 0)
