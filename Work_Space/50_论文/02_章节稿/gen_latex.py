# -*- coding: utf-8 -*-
"""由 `02_章节稿/成文` 的**标记正文**生成可编译 LaTeX 工程 → `04_交排版成图方/交付排版方论文/`。

设计依据（三者一致时取最严）
  ① **kb 本地引擎**（`kb/engine/p5_search.py`）：`kb/source/教材_转化/10_AI论文插图与LaTeX排版.md`
     —— **ctexart ＋ XeLaTeX**；`\\section`/`\\subsection`；**booktabs 三线表（无竖线）**；
     表题在上、图题在下；`\\label`/`\\ref`/`\\cite` 配对；长代码用 `lstlisting`；编译两遍。
  ② **官方《论文格式规范》**（`kb/source/…/全国大学生数学建模竞赛论文格式规范.md`）：
     电子版首页＝摘要专用页（含标题与关键词，≤1 页）；正文**不要目录**、≤30 页；正文之后附录（页数不限）；
     附录须含**支撑材料文件列表**与**全部可运行源程序**；参考文献按科技论文规范并在引用处标注。
  ③ **`04_交排版成图方/A_内容与排版绘图交接说明.md` §四 十条红线**：禁人为断页（章/节间）、
     表题在上图题在下、三线表、长表重复表头并标「（续）」、不写运行环境与硬件。

分节决策（"不合理分节"的合并与排除，逐条留痕于脚本注释与 README）
  · **合并**：A_01 题名 ＋ A_02 摘要 ＋ A_03 关键词 → 合成**摘要专用页**一件（A_03 仅提供选择理由，
    属内部件，**不进论文**；关键词行由 A_02 承载）；A_08 ＋ **A_09（5.5）** → 同一章
    「模型建立与求解」（A_09 本就是该章的 5.5 节）。
  · **排除**：各稿的元信息块、占位清单、自查、撰写说明、引用位置对照、字段核验留痕、变更记录
    —— 由 `mark_body.py` 的正文标记界定，本脚本只取标记内内容。
  · **不能直接写成 LaTeX 的**：Markdown 表格 → booktabs 三线表（>40 行用 longtable 自动续表头）；
    Markdown 标题 → `\\section`/`\\subsection`/`\\subsubsection`；`$$…\\tag{5-n}$$` → `equation*`＋`\\tag`；
    题录列表 → `thebibliography`＋`\\bibitem`；文内 `[n]` → `\\textsuperscript{\\cite{refn}}`。

编号纪律：图/表/式**编号已冻结**，一律**显式写号**（图 5-1、表 A-1、式 (5-9)），
  `\\thefigure`/`\\thetable` 随件改写 ⟹ 打印号与我方冻结号**逐号一致**，`\\ref` 亦可自动跟随。

用法：
    python 50_论文/02_章节稿/gen_latex.py            # 预演（只统计，不写盘）
    python 50_论文/02_章节稿/gen_latex.py --apply    # 生成工程
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BODY = os.path.join(HERE, "成文")
OUT = os.path.join(ROOT, "50_论文", "04_交排版成图方", "交付排版方论文")
CHART_MAP = os.path.join(ROOT, "50_论文", "03_对照与索引", "A_图表编号对照.md")
APPLY = "--apply" in sys.argv
BEGIN, END = "<!-- LATEX-EXPORT:BEGIN -->", "<!-- LATEX-EXPORT:END -->"
STAT = {"fig": 0, "tab": 0, "eq": 0, "sec": 0, "cite": 0}
EMBED_CODE = True         # 附录 B **嵌入代码正文**；置 False 时全篇降级为文件名清单（应急出口）。
# ★ 收录口径（v23 · 依用户批准「落盘 A-组 R2」）：
#   官方第五条字面要求「建模所用到的**全部**完整、可运行源程序」；而官方第四条明确
#   「**附录页数不限**」⟹ 扩录**不触 30 页正文红线**（上方是正文页数，附录另计）。
#   故由 v4 的"只嵌关键程序"**上调为**：**B.1–B.12 全部嵌入正文**（交付核／主流程 ＋
#   全部检验脚本），仅 **B.13**（`code/` 下其余溯源脚本，递归含 `innov/`）仍只列文件名清单
#   —— 原因：B.13 与 B.1–B.12 在功能上无重复但其量大且属过程性溯源件，其全文随支撑材料
#   提交、并在附录 A 表 A-1 逐项登记（官方第十一条）。
#   代价：附录约 **+78 页**（附录页数不限，不占正文 30 页）。
#   调整范围：改本元组即可（`src_line` 会按块是否在内决定"嵌入正文"或"只列清单"）。
KEY_BLOCKS = ("B.1", "B.2", "B.3", "B.4", "B.5", "B.6", "B.7",
              "B.8", "B.9", "B.10", "B.11", "B.12")


def src_line(fn, embed=None):
    """附录 B 的源程序行：嵌入正文（`\\srcfile`）或只列文件名（`\\texttt`）。

    `embed` 省略时取 `EMBED_CODE`；`EMBED_CODE=False` 是统一应急出口（全篇降级为清单）。
    """
    if embed is None:
        embed = EMBED_CODE
    return ("\\srcfile{%s}" % fn) if embed else "\\noindent\\texttt{%s}\\\\" % fn.replace("_", "\\_")


# ★ 代码注释里的符号（★／希腊字母／数学符号）：`\ttfamily`（lmmono）**无这些字形**
#   ⟹ 直接嵌入会在 PDF 中**留空**（`Missing character`）。已由 `preamble.tex` 的
#   `\lstmonofam`（DejaVu Sans Mono，见 `\srcfile` 宏）解决；**不采用 `literate` 映射**
#   —— 实测 XeLaTeX ＋ listings 下 `literate` 对多字节字符不生效（最小试验：仍报缺字）。


def src_list(files, per_line=3, budget=60):
    """紧凑的**文件名清单**（不嵌正文）：按**字符预算**打包每行，便于读者对准附录 A 表 A-1。

    ★ v11 修复「程序名超出页面」：旧实现**固定每行 3 个名字**，而长文件名
      （如 `innov/q3_core_nu_INVbase.py`，渲染 28 字符 × `\\small` 等宽 6.6pt ≈ 185pt）
      **三个一行必然超出 `\\textwidth`** ⟹ 实测附录 B 的 B.13 清单出现 **16 行
      `Overfull \\hbox`，单行最多超 144.5pt（≈5cm）**。
      现改为**按渲染字符数打包**：每行累计「文件名长度 ＋ 分隔符折算 2 字符」不超过
      `budget`（默认 60 字符 ≈ 60×6.6pt ≈ 396pt ＋ 分隔符，仍低于版心宽），
      故**单行恒不越版心**；`per_line` 退化为"每行至多几个"的上限。
      另在每个 `/` 与 `\\_` 之后插入 `\\allowbreak{}`，作为超长路径的二次保险。
    """
    def brk(fn):
        """把文件名转成**可断**的 `\\texttt` 内容：`_` 转义，并在 `/`、`\\_` 后加无连字符断点。"""
        s = fn.replace("_", "\\_")
        s = s.replace("/", "/\\allowbreak{}").replace("\\_", "\\_\\allowbreak{}")
        return s

    out, buf, used = [], [], 0
    for fn in files:
        add = len(fn) + (2 if buf else 0)          # 分隔符 `\quad` ＋ 空格 ≈ 2 个字符宽
        if buf and (used + add > budget or len(buf) >= per_line):
            out.append("\\noindent " + "\\quad ".join(buf))
            buf, used = [], 0
            add = len(fn)
        buf.append("\\texttt{%s}" % brk(fn))
        used += add
    if buf:
        out.append("\\noindent " + "\\quad ".join(buf))
    # ★ v11 关键修复：**整块清单必须 raggedright**。
    #   上述"每行若干名字"只是**源码**的分行；这一整块其实被 TeX 视为**同一个段落**，
    #   它会按版心**自行重排**（日志实测：Overfull 报出的行内容与源码行并不对应）——
    #   故仅"按预算打包"并不能阻止溢出。两端对齐时 TeX 还要把行拉伸到 `\hsize`，
    #   在"固定宽盒子 ＋ 无伸缩 `\quad`"的组合下既不齐又易被判 Overfull。
    #   包一层 `\raggedright\sloppy` ⟹ 行不拉伸、断行点充分，**从机制上消除溢出**。
    return (["\\begingroup\\raggedright\\sloppy"] + out + ["\\par\\endgroup"])


# ───────────────────────── 取正文 ─────────────────────────
def body_of(fn):
    t = io.open(os.path.join(BODY, fn), encoding="utf-8").read()
    if BEGIN not in t or END not in t:
        raise SystemExit("缺正文标记：%s（先跑 mark_body.py）" % fn)
    return t.split(BEGIN, 1)[1].split(END, 1)[0].strip("\n")


def inline(s, cite=True, ref=True):
    """行内 Markdown → LaTeX（数学片段与行内代码受保护）。"""
    store = []

    def keep(m):
        store.append(m.group(0))
        return "\x00%d\x00" % (len(store) - 1)

    s = re.sub(r"\$[^$\n]+\$", keep, s)                    # 行内数学（原样）
    s = re.sub(r"`[^`\n]+`", keep, s)                      # 行内代码（原样，见下）
    # ★★ **先转义、后生成 LaTeX**：`esc()` 只作用于纯文本；粗体、引用上标、图/表/式交叉引用、
    #    Unicode 上下标**必须在 esc 之后**插入。此前顺序相反，致其 `\`、`{}` 被转义 ——
    #    `3.1×10\textsuperscript{-11} ℃` 之类**原样打印**（"部分行内公式不显示"的根因）。
    s = esc(s)
    # ★★ v18（内容轮）：**中文弯引号** —— 源稿用直引号 "…" 标注术语，而中文排版规范要求弯引号
    #   （实测 `sections/*.tex` 中直引号 **82 处**、弯引号 **0 处**）。此处只对**成对**直引号生效
    #   （未配对的不动，避免误伤），且数学片段与行内代码在 `keep()` 中已被保护 ⟹ 不受影响。
    s = re.sub(r'"([^"\n]+)"', r"“\1”", s)
    s = re.sub(r"\*\*([^*\n]+)\*\*", r"\\textbf{\1}", s)   # 粗体
    if cite:                                               # 题录上标：[1] / [9][10]
        s = re.sub(r"(?:\[\d{1,2}\])+",
                   lambda m: "\\textsuperscript{\\cite{%s}}" % ",".join(
                       "ref" + x for x in re.findall(r"\d{1,2}", m.group(0))), s)
    if ref:                                                # 图/表/式 交叉引用
        s = re.sub(r"图\s*(A-\d+|\d+-\d+)", lambda m: "图~\\ref{fig:%s}" % m.group(1), s)
        # ★ v18：补充表号由 `5-1` 扩到 `5-\d+`（本章新增 表 5-3～表 5-6 的中间结果表），
        #   附录表号由 `A-1` 扩到 `A-\d+` ⟹ 正文里写"表 5-4"等一律转成 `\ref`，与印刷号自洽。
        s = re.sub(r"(?<![0-9])表\s*(A-\d+|0-1|1-1|2-1|5-\d+|[1-6])(?![\d-])",
                   lambda m: "表~\\ref{tab:%s}" % m.group(1), s)
        s = re.sub(r"式\s*\((\d+-\d+)\)", lambda m: "式~\\eqref{eq:%s}" % m.group(1), s)
    s = sup_unicode(s)                                     # Unicode 上下标 → \textsuperscript{…}
    for i, v in enumerate(store):                          # 还原受保护片段
        if v.startswith("`"):                              # 行内代码 → \texttt{逃逸后}
            v = "\\texttt{%s}" % esc(v[1:-1])
            # ★ 行内代码多为**长路径／文件名**（`code/innov/q1_inv_T1_duhamel.py`）：默认无断行点，
            #   在窄列内必然 `Overfull \hbox`（实测 附录 A 表 A-1 有 100+ 条）。在 `/` 与 `\_` 之后
            #   插入 `\allowbreak`（**无连字符的断行点**）⟹ 路径可在列内换行，版式不再溢出。
            #   ★ v11 追加：**`.` 之后也加断点** —— 无斜杠的文件名（`requirements.txt`、
            #   `q1_core.py`）原无任何断行点，在窄列（附录 A 表 A-1）内仍会 `Overfull \hbox`（实测 2.06pt）。
            v = (v.replace("/", "/\\allowbreak{}").replace("\\_", "\\_\\allowbreak{}")
                  .replace(".", ".\\allowbreak{}"))
        s = s.replace("\x00%d\x00" % i, v)
    return s


SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6",
       "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+"}


def sup_unicode(s):
    """Unicode 上下标（如 10⁻¹¹）→ `\\textsuperscript{-11}`（kb 红线：公式禁 Unicode 上下标）。"""
    def rep(m):
        return "\\textsuperscript{%s}" % "".join(SUP[c] for c in m.group(0))
    return re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+", rep, s)


ESC = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_",
       "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def esc(s):
    return "".join(ESC.get(c, c) for c in s)


# ───────────────────────── 块级：公式 / 表 / 图 ─────────────────────────
def eq_block(line):
    """`$$…$$` → **自动编号** `equation` 环境（编号由 LaTeX 计数动态生成，不写死式号）。"""
    inner = line.strip()[2:-2].strip()
    mt = re.search(r"\\tag\{([^}]+)\}", inner)                    # 式号仅作 \label 的**键**保留
    inner = re.sub(r"\\tag\{[^}]*\}", "", inner).strip()          # 打印号改由计数器生成
    STAT["eq"] += 1
    if "\\\\" in inner and "\\begin{" not in inner:
        inner = "\\begin{aligned}\n    %s\n  \\end{aligned}" % inner   # 顶层换行改用 aligned
    env = "equation" if mt else "equation*"   # ★ 只编号**被引用**的式（源侧以 `\tag{}` 标记）
    out = ["\\begin{%s}" % env, "  %s" % inner]
    if mt:
        out.append("  \\label{eq:%s}" % mt.group(1))
    out.append("\\end{%s}" % env)
    return out


TABLE_SPECS = {"A-1": "longtable"}

# ★ v11：**表编号统一**。此前题面强制表（源侧键 `tab:1`–`tab:6`）被改用独立计数器 `reqtab`
#   呈现为"表 1–表 6"，与全篇其余表的"章-序"（表 5-1、表 5-2…）**两套编号并存** ⟹ 同一节内
#   同时出现"表 1／表 2"与"表 5-1"，被判为**未进入统一编号**（用户实测指出）。
#   现统一走"章-序"，六张题面表呈现为 表 5-2…表 5-8（正文引用一律 `\ref`，自动跟随）。
#   如需恢复"题面号"呈现，把 `REQTAB_SPECIAL` 置 True 即可（`reqtab` 相关代码保留未删）。
REQTAB_SPECIAL = False

# ───────────────── 表格列宽：按各列内容**加权分配** ─────────────────
# 旧实现各列**等分**可用宽度：短列（序、大小、符号）过宽、长列（说明、作用）过窄 ⟹
# 表内断行过多、表格高度虚增。现改为：以各列内容的**视觉宽度**为权、经幂压缩与夹取后
# 归一化到 1/1000 的整数份额（合计恰为 1000 ⟹ 列宽之和 = 可用宽度，不越版心）。
_CJK_RANGES = ((0x1100, 0x115F), (0x2E80, 0xA4CF), (0xAC00, 0xD7A3), (0xF900, 0xFAFF),
               (0xFE30, 0xFE6F), (0xFF00, 0xFF60), (0xFFE0, 0xFFE6), (0x3000, 0x303F))


def _plain(s):
    """去掉行内标记（粗体／行内代码／公式定界／`\\textsuperscript`），得到参与宽度估算的纯文本。"""
    t = re.sub(r"\*\*|`|\$", "", s)
    t = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", t)
    return re.sub(r"\\[a-zA-Z]+", "", t)


def _disp(s):
    """**视觉宽度**：CJK／全角字符按 2 计、其余按 1 计（按"字数"统计会低估中文列）。"""
    return sum(2 if any(a <= ord(c) <= b for a, b in _CJK_RANGES) else 1 for c in _plain(s))


def col_units(rows, ncol, lo=0.07, hi=0.60):
    """按各列内容分配列宽份额（整数，合计恰为 1000）。

    ① 取该列**内容视觉宽度的 90 分位**（与表头取大）—— 长表里个别超长单元不致把该列拉爆；
    ② 以 **0.6 次幂**压缩 —— 长度比不线性地变成宽度比，短列不会被压到不可读；
    ③ 份额夹在 `[lo, hi]` 内后**重新归一化**，余数归末列 ⟹ 合计恒为 1000。
    """
    raw = []
    for i in range(ncol):
        cells = sorted(_disp(r[i]) for r in rows if i < len(r))
        k = max(1, int(round(0.9 * len(cells))))
        hdr = _disp(rows[0][i]) if i < len(rows[0]) else 1
        # ★ 除 90 分位外，另保 **最宽单元的 3/4**：数值列里个别长取值（如 `50.6523±0.0249`）
        #   若被分位权重忽略，该列会窄到装不下 ⟹ `Overfull \hbox`（实测正文结果表即如此）。
        raw.append(max(2.0, float(max(cells[:k]) if cells else 2),
                       0.75 * float(cells[-1]) if cells else 2.0, float(hdr)))
    w = [x ** 0.6 for x in raw]
    share = [min(max(x / sum(w), lo), hi) for x in w]
    share = [x / sum(share) for x in share]
    units = [int(round(x * 1000)) for x in share]
    units[-1] += 1000 - sum(units)
    return units


# ★ v11：**逐表列宽覆盖**（键＝表 `\label` 的键，即 `tab:` 之后那一串；未列者仍由 `col_units` 自动分配）。
#   用途：内容长度差异极大的表——自动分配经 0.6 次幂压缩后**短列会偏窄**，可在此按实测手工重分配，
#   **不牵动其它表**。份额须合计 1.000。
TAB_COL_SHARE = {
    # ★ v13（用户报"表 4-1 一直是排版重灾区"）：按实测列坐标重分配——旧 0.30/0.39/0.31 下
    #   "含义"列仅 ~155pt ⟹ 长描述**行行折行**；而"单位"列（内容多为 `cm`、`℃、kg/kg`）
    #   右侧空出 **44pt** 未用。改为 **符号 0.26／含义 0.58／单位 0.16**：
    #   含义列 ~256pt（折行由 3 行降到 2 行）、单位列 ~70pt（`cm、无量纲` 仍单行）⟹ 表体变矮。
    "0-1": (0.26, 0.58, 0.16),          # 表 4-1 主要符号一览（符号／含义／单位）
    # 表 5-3 四问核心结果对照：第 4 列须容纳 `50.6523±0.0249 h`（12pt 下 ≈93pt），
    # 自动分配略窄 ⟹ 实测该单元格 `Overfull \hbox` 3.27pt。此处把首列压到 0.09、
    # 四问列拉平到 0.2275（0.2275×0.97×455.2≈100.4pt ≥ 93pt）。
    # ★ v13（用户报"表 5-9 的排版也有严重问题"）：上版把首列压到 0.09（≈40pt）**过了头**——
    #   实测首列"物性体系"被硬折成"物性／体系"两行。改为 **0.12／0.22×4**：
    #   首列 ~53pt（"物性体系"单行 ✓）；四问列 ~97pt，仍 ≥ 单元格 `50.6523±0.0249 h` 所需 93pt ✓。
    "5-3": (0.12, 0.22, 0.22, 0.22, 0.22),
}


# ★ v13：**可整表一页容纳**的表 → 启用**浮动表**（`table` + `tabular`，题注随表整块放置）。
#   用户报"表 4-1 一直是排版重灾区"：实测该表被 `longtable` 在 p5 页底切出
#   "题注 ＋ 表头 ＋ 仅 1 行（自变量与几何）"、其余 17 行续到 p6 ⟹ **题注与表体跨页分离**。
#   浮动表由 TeX 择页整表放置 ⟹ 该症状消失。**超一页的大表（题面六表、附录分块表）仍用
#   `longtable`**：浮动表对超页内容会 `Float too large for page` ⟹ 截断（属评奖风险）。
FLOAT_TABLES = ("0-1",)               # 键＝表 \label（表 4-1 主要符号一览）


def table_block(cap, rows, notes, label, aligns=None):
    """Markdown 表 → booktabs 三线表（>40 行用 longtable 自动续表头）。"""
    STAT["tab"] += 1
    if label:                                  # 表 \label 去重（首现保持原键，其后缀 -b／-c…）
        _base, _k = label, 0
        while label in TAB_SEEN:
            _k += 1
            label = "%s-%s" % (_base, chr(96 + _k))
        TAB_SEEN.add(label)
    head, body = rows[0], rows[1:]
    ncol = len(head)
    # ★ 列宽**必须把 `\tabcolsep` 计入**（每列左右各 1 个，共 2·ncol 个）：旧写法按"列宽之和＝0.94\textwidth"
    #   分配，**漏掉列间距** ⟹ 表实际宽 = 列宽之和 ＋ 列间距 > \textwidth，**表右伸出版心 0.7–1.2cm**
    #   （实测 24 页的表/图右界达 545–557pt，而版心右界为 524.4pt；且因 longtable 不产生 Overfull 告警而长期隐蔽）。
    #   ★ v10：列宽**不再各列均分**，而按各列内容加权（`col_units`）；可用宽度＝`\settabw{2n}` 记入的
    #   `\tblw`＝0.97\textwidth − 2n·\tabcolsep，各列按月其份额取用 ⟹ 合计恰为可用宽度、不越版心。
    _u = col_units(rows, ncol)
    # ★ v11：**逐表列宽覆盖**（见表 `TAB_COL_SHARE` 说明）。
    #   表 4-1（键 `0-1`）三列内容长度差异极大：符号列常见"3–4 个符号一组"、
    #   单位列含复合单位（`kg/m³、J/(kg·K)、W/(m·K)`），自动分配给这两列偏窄
    #   ⟹ 单元格频繁换行、单位被拆行，叠加三线表（无竖线）后可读性明显下降。
    #   故按内容实测重分配为 符号 0.32／含义 0.37／单位 0.31。
    _ov = TAB_COL_SHARE.get(label or "")
    if _ov and len(_ov) == ncol:
        _u = [int(round(x * 1000)) for x in _ov]
        _u[-1] += 1000 - sum(_u)
    _hw = [_disp(rows[0][i]) if i < len(rows[0]) else 0 for i in range(ncol)]
    _mx = [max([_disp(r[i]) for r in rows if i < len(r)] or [0]) for i in range(ncol)]
    # ★ v11：**列对齐**（原 md 的对齐行为唯一真源；未指定者沿用自动启发式）＋**竖直居中**。
    #   竖直：一律 `m{}`（原用 `p{}` 是"顶对齐"，故短单元格贴在行顶、观感不齐；
    #   表 1-1 的"项"列即因此不居中）——行高由最高单元格决定，`m` 只改格内位置、不改行高。
    #   水平：`:` 在左→左对齐、在右→右对齐、两侧都有→居中；纯 `---` → 短列居中／长列左。
    _HA = {"c": "\\centering", "l": "\\raggedright", "r": "\\raggedleft"}
    _ha = []
    for i in range(ncol):
        mk = (aligns[i].strip() if aligns and i < len(aligns) else "")
        if mk.startswith(":") and mk.endswith(":"):
            _ha.append("c")
        elif mk.startswith(":"):
            _ha.append("l")
        elif mk.endswith(":"):
            _ha.append("r")
        else:
            _ha.append("c" if (_hw[i] <= 10 and _mx[i] <= 14) else "l")
    spec = "".join(
        ">{%s\\arraybackslash}m{\\dimexpr %.3f\\tblw\\relax}"
        % (_HA[_ha[i]], _u[i] / 1000.0)
        for i in range(ncol))
    # ★ **表一律用非浮动 `longtable`**（本轮机制修复，取代 `len(body) > 40` 的阈值判据）：
    #   ① 浮动态表在"内容高于一页"时触发 `Float too large for page` ⟹ **表被截断**（实测：符号表超
    #      111.13pt、第五章选型表超 73.43pt、附录 11 张表超 70–1440pt —— 其中**支撑材料清单被截断属评奖风险**）；
    #   ② 浮动态表还会被推成"浮动页"，造成"整页只有一张表"（实测正文 p12／p17 各仅 35 字）。
    #   `longtable` 就地排版、超页自动分页并重复表头标"（续）"，同时消除上述两类缺陷；
    #   表题仍在表头之首（"表题在上"不变），编号仍由 table 计数器动态生成（编号纪律不变）。
    # ★ v13：**逐表选择浮动／非浮动**（`FLOAT_TABLES` 为"可整表一页容纳"的白名单）
    long = (label or "") not in FLOAT_TABLES
    # ★ v7：**题面强制表（表 1–表 6）改用独立计数器 `reqtab`，全篇连续编号**
    #   症状：`\numberwithin{table}{section}` 使题面表 1–6 按章渲染为"表 5-2…表 5-7"（本文补充表呈 5-1），
    #         与题面模板号"表 1–表 6"不符；正文引用因 `\ref` 自洽，但评委按题面号查找会错位。
    #   处置：**仅**对 `\label{tab:1}`–`\label{tab:6}` 这六张表，在**组内**把 `\thetable` 改写为
    #         `\arabic{reqtab}`；`\stepcounter` 必须放在**组外**（组内递增会随 `\endgroup` 回退 ⟹ 六张表都显示 1）。
    #         其余表（本文补充表 表 5-1、附录表 表 A-1）沿用"章-序"，编号纪律与《A_图表编号对照.md》不变。
    reqtab = REQTAB_SPECIAL and bool(re.fullmatch(r"[1-6]", label or ""))
    head_row = "    " + " & ".join(inline(c, cite=False) for c in head) + " \\\\"
    cap = cap or ""
    L = []                                    # 表号由 LaTeX 计数器动态生成（不写死）
    if reqtab:
        L += ["\\stepcounter{reqtab}",
              "\\begingroup\\renewcommand{\\thetable}{\\arabic{reqtab}}"]
    if long:
        L += ["\\settabw{%d}" % (2 * ncol), "\\begin{longtable}{%s}" % spec]
        if cap:                               # 无题注的内嵌对照表：不设空题注行（避免空行致装配错误）
            L += ["  \\caption{%s}\\label{tab:%s}\\\\" % (inline(cap, cite=False), label)]
        L += ["  \\toprule", head_row, "  \\midrule", "  \\endfirsthead",
              # 续页表头：题注**已自带"（续）"**（附录分块表的题注以"（续）　类别…"开头）时**不再重复标记**，
              # 否则出现"（续）　（续）"两重标记（实测附录 A 各分块表均如此）。
              *( [] if cap.strip().startswith("（续）") else
                 ["  \\multicolumn{%d}{r}{\\footnotesize（续）}\\\\" % ncol] ),
              "  \\toprule", head_row, "  \\midrule", "  \\endhead",
              # ★ v11：**续页底部横线**——原实现只写 `\endlastfoot`，表一旦跨页分页，
              #   **上一页末尾没有任何规则线**（实测：表 4-1 在第 5 页末、表 5-1 同样缺线）。
              #   三线表的收口线是 `\bottomrule`，故令 `\endfoot`（除末页外每页页末）与
              #   `\endlastfoot`（末页页末）**同取 `\bottomrule`** ⟹ 分页处与末页收口一致。
              "  \\bottomrule", "  \\endfoot",
              "  \\bottomrule", "  \\endlastfoot"]
        for r in body:
            _cells = [inline(c, cite=False) for c in r]
            # ★ v11：**分组标题行跨列**——分组行只有首格有字（如"自变量与几何"），
            #   原写法令其后各格留空；三线表无竖线时，这些空格无法传达"整行分组"的语义。
            #   改用 `\multicolumn{n}{l}` 横贯表宽 ⟹ 表内层级一眼可辨（数据行不受影响）。
            #   ★ v15（用户看诊断副本后指出）：分组行须 **合并整行 ＋ 居中 ＋ 加粗 ＋ 其下细实线** ——
            #   旧写法左对齐、不加粗、无分隔线，三线表无竖线时分组与数据行混作一片。
            if ncol > 1 and _cells and _cells[0].strip() and all(not c.strip() for c in _cells[1:]):
                L.append("  \\multicolumn{%d}{c}{\\bfseries %s} \\\\" % (ncol, _cells[0]))
                L.append("  \\cmidrule(lr){1-%d}" % ncol)
            else:
                L.append("  " + " & ".join(_cells) + " \\\\")
        L.append("\\end{longtable}")
        if reqtab:                            # 关闭题面表的 `\thetable` 局部改写（编号恢复"章-序"）
            L.append("\\endgroup")
            # ★ v8：题面表的 `\caption` 会**推进全局 `table` 计数器**（实测每表 +1，六表共 +6）⟹
            #   其后的**本文补充表被整体偏移 6 号**（实测：三套物性对照呈「表 5-4」而登记为「表 5-2」；
            #   §5.5 两表呈「表 5-9／表 5-10」而登记为「表 5-3／表 5-4」），且正文「见表 5-2」与呈现号不符。
            #   根因：v7 只在**组内**改写 `\thetable`，未隔离 `table` 计数器本身。
            #   处置：每张题面表后**全局回退 1**，把计数器还原 ⟹ 补充表恢复「章-序」连续编号（＝登记号）。
            L.append("\\makeatletter\\global\\advance\\c@table by -1\\makeatother")
    else:
        L += ["\\settabw{%d}" % (2 * ncol),
              "\\begin{table}[htbp]", "  \\centering",   # 见 fig_block 注：不用 `[H]`
              ("  \\caption{%s}\\label{tab:%s}" % (inline(cap, cite=False), label)) if cap else "",
              "  \\begin{tabular}{%s}" % spec, "    \\toprule", head_row, "    \\midrule"]
        for r in body:
            _cells = [inline(c, cite=False) for c in r]
            # ★ v13：浮动表同样支持**分组标题行跨列**（与 longtable 分支保持一致）
            #   ★ v15：同上——合并整行 ＋ 居中 ＋ 加粗 ＋ 其下细实线
            if ncol > 1 and _cells and _cells[0].strip() and all(not c.strip() for c in _cells[1:]):
                L.append("    \\multicolumn{%d}{c}{\\bfseries %s} \\\\" % (ncol, _cells[0]))
                L.append("    \\cmidrule(lr){1-%d}" % ncol)
            else:
                L.append("    " + " & ".join(_cells) + " \\\\")
        L += ["    \\bottomrule", "  \\end{tabular}"]
        if notes:
            L.append("  \\par\\vspace{2pt}\\footnotesize " + inline("；".join(notes), cite=False))
        L.append("\\end{table}")
        return L
    if notes:
        L.append("\\noindent\\footnotesize " + inline("；".join(notes), cite=False))
    return L


# ───────────────── 图表编号对照表（图嵌入的唯一权威） ─────────────────
def _draft_figmap():
    """从**成文稿「占位清单」**抽取 `论文内索引号 → {F 号, 图NN, 图名}`（编译源口径）。

    占位清单行例：
      `| 图 | 图 5-6 问题一水分浓度场时空分布 | F-09 | 图07 | 5.1.4；数据 fig_q1_field_C.csv |`
    ⟹ 取「论文内索引号」「F 号」「PDF 文件索引号」三列（第 5 列为说明，不参与）。
    表行（`| 表 |`）与附录行（无 F 号）自然不匹配。
    """
    pat = re.compile(r"\|\s*图\s*\|\s*图\s*([0-9A-Za-z]+-[0-9a-z]+)\s+([^|]*?)\s*\|\s*"
                     r"(F-\d+)\s*\|\s*(图\s*\d+[a-z]?)\s*\|")
    out = {}
    if not os.path.isdir(BODY):
        return out
    for fn in sorted(os.listdir(BODY)):
        if not fn.endswith(".md"):
            continue
        for m in pat.finditer(io.open(os.path.join(BODY, fn), encoding="utf-8").read()):
            num = m.group(1)
            out[num] = {"F": m.group(3), "pdf": m.group(4).replace(" ", ""), "name": m.group(2).strip()}
    return out


def load_figmap():
    """读《A_图表编号对照.md》：论文内索引号 ←→ F 号 ←→ PDF 文件索引号。

    返回 (map, orphans)：
      map     = {"5-1": {"F": "F-01", "pdf": "图01", "name": "总体建模流程图"}, …}
      orphans = [ (F 号, 图名, PDF 号), … ]  —— 已收割但**尚无论文内索引号**（即未进论文）
    """
    # ★ **只读 JSON**（`A_图表编号对照.json`，与同名 .md 由 `build_indexes.py` **同源产出**），
    #   不再解析 Markdown 表格 —— 键与字段即为所需，杜绝解析分歧。
    import json
    figmap, orphans = {}, []
    jp = os.path.splitext(CHART_MAP)[0] + ".json"
    if not os.path.isfile(jp):
        raise SystemExit("缺 %s —— 请先运行 50_论文/01_写作计划/code/build_indexes.py" % jp)
    doc = json.loads(io.open(jp, encoding="utf-8").read())
    for it in doc.get("figures", []):
        pi = (it.get("paper_index") or "").strip()
        pdfi = (it.get("pdf_index") or "").strip()
        if pi:
            figmap[pi] = {"F": it.get("f_no", ""), "pdf": pdfi, "name": it.get("name", "")}
        else:
            orphans.append((it.get("f_no", ""), it.get("name", ""), pdfi))

    # ★★ v11 修复「正文出现图占位」（用户实测至少 3 处）★★
    #   实测：JSON 的 `paper_index` 只填了 **12/51**（`counts.paper_index_filled=12`）——
    #   正文实际在用的 图5-3／5-6／5-10／5-11／5-12／5-15／5-20 **全部缺映射**
    #   ⟹ `fig_block()` 取不到 F 号与图NN，候选链退化为「论文内索引号」（`fig-5-6`／`图5-6`），
    #   而 `05_成品图/` 里的真实文件名是 `图07-Q1水分浓度场时空分布.pdf` 这类**交付命名**
    #   ⟹ 链未命中 ⟹ 打印 `\fbox{\parbox{…}{图占位…}}`（PDF 中可见，且**不产生 LaTeX 错误**，
    #   故历次"0 错误／0 占位"检查均漏判 —— 只因占位框文本在前言宏里、不在 sections 里）。
    #   修法：**以编译源（成文稿「占位清单」）为准补全映射**，使"正文写的号"与"图文件能否找到"
    #   同源；只在**图件链接**这一条路径生效，不触碰其余三张派生对照表。JSON 仍保留作 `name` 来源。
    draft = _draft_figmap()
    diff = [(k, figmap.get(k, {}).get("pdf", ""), v["pdf"]) for k, v in draft.items()
            if k not in figmap or figmap[k].get("pdf") != v["pdf"]]
    for k, v in draft.items():          # 成文稿＝编译源 ⟹ **以成文为准覆盖**
        figmap[k] = v
    if diff:
        print("  ★ 图号映射补全（成文「占位清单」→ FIGMAP）：新增/订正 %d 个" % len(diff))
        for k, old, new in diff:
            print("      %-8s pdf: %-8s → %s" % (k, old or "(缺)", new))
    return figmap, orphans


FIGMAP, FIG_ORPHANS = load_figmap()
FIG_SEEN = set()          # 本次生成中实际落地的图号（用于缺口报告）
TAB_SEEN = set()          # 本次生成中已用过的表 \label（**去重**：附录分块表题注均含"表 A-1（续）…"，
                          # 旧写法使 11 张表共享 `tab:A-1` ⟹ `Label multiply defined` 告警与 \ref 指向漂移）

# 成品图目录（**相对路径** `50_论文/04_交排版成图方/交付排版方论文/` → `50_论文/05_成品图/`）
FIG_SRC = os.path.join(os.path.dirname(HERE), "05_成品图")
FIG_REL = "../../05_成品图/"


def scan_figfiles():
    """扫描 `50_论文/05_成品图/` 实况 ⟹ {PDF 文件索引号如 `图01`: [真实文件名, …]}。

    成品图命名为 `<PDF 文件索引号>-<图名>.pdf`（分幅图为 `图05a-…`／`图05b-…`），
    故须**按目录实况解析**并以**相对路径**引用（禁用绝对路径）；改名或替换图后重跑生成器即可。
    """
    got = {}
    if os.path.isdir(FIG_SRC):
        for f in sorted(os.listdir(FIG_SRC)):
            m = re.match(r"^(图\s*\d+[a-zA-Z]?)\s*[-_].*\.(pdf|png|jpg|jpeg)$", f, re.I)
            if m:
                key = re.sub(r"\s+", "", m.group(1))[:]
                base = re.match(r"^(图\s*\d+)", key).group(1)
                got.setdefault(base, []).append(f)
    return got


FIGFILES = scan_figfiles()

# ── 图的版面口径（**内容侧配置**：改这里即可，不必动 `sections/*.tex`） ──────────────
# ① 逐张宽度：键＝**论文内索引号**（即《A_图表编号对照.md》的"论文内索引号"，也是 `fig:5-1`
#    这类内部标签键），值＝占 `\textwidth` 的倍数。未列者取 `FIG_W_DEFAULT`。
#    口径：**框图/流程图信息密度高 ⟹ 放足整版文字宽度**，与正文同宽便于对照阅读。
FIG_WIDTH = {
    "5-1": 1.00,          # 建模总体流程图（F-01）：加宽到整版文字宽度
    # ★ 第六章（渲染号 → 论文内索引号 由 `_pgchk.aux` 实测：图6-1＝A-1／6-2＝A-10／6-3＝A-2）
    # ★ v11 修正：双联图**总宽必须 < 1.00**——取 1.00 时两幅各 0.500，加上两幅之间的
    #   空格后合计 **> \textwidth**（`\hfill` 无收缩量），TeX 只能把第二幅折到下一行
    #   ⟹ 实测"两图未并列"。取 **0.970**（每幅 0.485，与 图 5-5／5-6 的并置口径一致），
    #   `\hfill` 吸收余量 ⟹ 稳定并列且留有图间间隔。
    "A-1": 0.970,         # 图6-1 网格与时间收敛性（F-06，双联 a/b，2 幅均分 ⟹ 每幅 0.485）
    "A-10": 0.50,         # 图6-2 界面取法与网格对照（F-39）：0.660 → **0.500**（原偏大）
    "A-2": 0.50,          # 图6-3 解析级数解对拍（F-11）：0.660 → **0.500**（原偏大）
    # ★ F-6 轮（4 张流程图入正文）：**流程图类须守"高度 ≤ 9 cm"红线**（升级提示词 模块六：
    #   流程图宽度 ≤ 正文宽 65%、高度 ≤ 页面 35%（≈9 cm））。按各图**实测纵横比**定宽：
    #   图19（IMEX 流程图）h/w=1.17、图51（Q3 求解流程）h/w=1.21 —— 取 0.66 时高度达
    #   12.4／12.8 cm，**实测触发 `Overfull \vbox (301.01pt too high)`（p12）**；
    #   改 0.45 后高度分别降至 8.4／8.7 cm ✅。图48（h/w=0.87，原 0.66 → 9.2 cm）同步收至 0.48 → 6.7 cm。
    "5-11": 0.36,         # ★ v13：0.45 → **0.36**（高 6.7 cm）。缘由：用户报"图5-8／图5-9 仍占据了一整页"
                          #   ——该流程图与相邻的 图5-12 同落一页、各高约 8.5 cm ⟹ 两图合计占版心高 69%。
    "5-12": 0.60,         # ★ v22（用户第 3、4 条）：由**环绕**改回**嵌入**并把宽度 0.50 → **0.60**
                          #   （用户报"图5-7 往左下偏""第 16 页文字为它留了空位但图在上一页"——
                          #   均系 `wrapfigure{r}` 的固有表现：图不居中 ＋ 预留行数溢出到下一页）。
                          #   0.60 宽时高 7.7 cm（纵横比 0.80），仍小于原环绕宽 0.58 的观感。
    "5-15": 0.45,         # 图5-15 问题三求解流程图（F-51／图51）：0.45（8.7cm，守 ≤9cm 红线；
                          #   实测再缩到 0.40 对落位**无改善**，故不保留未生效的改动）
    "5-17": 0.56,         # ★ v22（用户第 6 条"图5-10（＝索引5-17）下面有很大的空"）：0.48 → **0.56**
                          #   （高 8.0 cm，纵横比 0.87；原 6.7 cm 偏小、留下大块空白）
    "5-10": 0.80,         # ★ v22（用户第 2 条"图5-5（＝索引5-10）上下空隙大"）：0.66 → **0.80**
                          #   （宽 12.8 cm、高 5.2 cm，纵横比 0.41 的扁图；原 10.4×4.3 cm 偏小）
    "5-20": 0.66,         # 图5-20 压缩温升机理与绝热包络：宽度由**环绕**决定（见 `WRAP_FIGS`）
    "A-20": 0.80,         # ★ v22（用户第 10 条）：0.66 → **0.80**（宽 12.8 cm、高 7.6 cm）
    "A-9": 0.80,          # ★ v22（用户第 10 条）：0.66 → **0.80**（宽 12.8 cm、高 5.9 cm）
}
FIG_W_DEFAULT = 0.66
# ② 并置成对：(a, b) 两图**同节、机制同源**时并排呈现在**同一个 figure 环境**内的两个 `minipage`，
#    各自**保留图号与 `\label`**（编号仍由计数器连续产出，正文 `\ref` 一字不改）。
#    每幅宽度取 `PAIR_W_BY`（逐图可覆盖，未列者用 `PAIR_W`），中间以 `\hfill` 分隔。
FIG_PAIRS = (("5-5", "5-6"),       # 问题一温度场 ／ 水分浓度场时空分布（原有）
             ("5-15", "5-16"),     # ★ v22（用户第 5 条）：**仍在此登记**（配对与暂挂逻辑靠它触发），
                                   #   但**摆放方式改由 `WRAP_STACK` 决定** ⟹ 由"左右并置"改为
                                   #   "**左侧竖直排列的环绕式**"（两图同宽、整体靠左、正文绕右）。
             ("A-10", "A-2"))      # 图6-2 界面取法与网格对照 ／ 图6-3 解析级数解对拍
PAIR_W = 0.455                     # 默认每幅宽度（未在 `PAIR_W_BY` 中列出者用它）
# ★ v22：**逐图宽度**（用户第 1、9 条）——"图5-3/5-4 的间隔小一点、把图放大"与
#   "图6-2/6-3 放大，且 6-2 比 6-3 多放大"。并置对的**间隔 ＝ 1 − 两幅宽之和**，故加大宽度即
#   同时缩小间隔；总宽须 < 1.00（否则第二幅被折到下一行）。实测旧值 0.455 ⟹ 间隔 1.44 cm。
PAIR_W_BY = {
    "5-5":  0.485, "5-6":  0.485,   # 温度场/水分浓度场：间隔 1.44 → **0.48 cm**，图 +6.6%
    "A-10": 0.520, "A-2":  0.440,   # 6-2 比 6-3 **多放大**（用户第 9 条）；两幅高各 ≈5.3 cm，视觉等高
}
# ★ v22（用户第 5 条）：**竖直排列的环绕式插图**——两图放进**同一个** `wrapfigure{l}`，各占
#   `\linewidth` ⟹ **宽度必然一致**，整体靠左、正文绕右。键＝(图号, 图号)，值＝环绕宽（版心占比）。
WRAP_STACK = {("5-15", "5-16"): 0.40}
# ③ ★ v14（用户指令）：**用 Word 式"环绕"代替"嵌入"**——个别图改用 `wrapfig`，令正文绕图排，
#    而不是整块独占一个浮动体（后者即使缩窄也仍"独占一块版面"）。
#    键＝论文内索引号；值＝(图宽占比, 靠边 side)。仅用于**高瘦且附近正文充足**的图；
#    环绕对"图高于剩余正文"的情形会溢出 ⟹ 只逐张启用、且编译后须核 `Overflow`／vbox。
WRAP_FIGS = {
    # ★ v22（用户第 7 条）：**图5-11（印刷号）＝论文内 图5-20** 按要求**改环绕**。
    #   ⚠ 宽度 0.58 实测与紧随其后的 **表 5-6** 相撞（表格不能绕排，p22 实测"表头压图"）
    #   ⟹ 两处处置：① 把 **表 5-6 提到该图之前**（md 顺序调整）；② 环绕宽收到 **0.50**
    #   （高 5.6 cm ≈ 11 行，§5.4.5 正文足以绕满）。
    "5-20": (0.50, "r"),
}
# ★★ v20（用户问"有没有办法自动处理环绕图表，是否必须手动调参数"）：**自动环绕判定引擎** ★★
#   事实：`wrapfig` **自身不能自动定宽**（TeX 层没有"量图再定栏宽"的机制），所以**纯 LaTeX 做不到自动**；
#   但本工程是「md → LaTeX 生成器」结构 ⟹ 生成器在生成时**能读到每张成品图的真实尺寸**，
#   于是"要不要环绕、环绕多宽"变成**可计算量**，不再需要人工试错（原先每张图的宽度都是手填常数）。
#   四条判据（全部自动、可复核）：
#     ① 图侧正文栏下限 `AW_MIN_TEXT_W` ⟹ 图宽 ≤ 1 − 0.42 ＝ **0.58 版心**（否则正文栏太窄、断句碎）；
#     ② 图高上限 `AW_MAX_FIG_H_CM` ⟹ 由该图**实测纵横比**反算图宽上限（细高的图不允许占满整页）；
#     ③ ★ **环绕不得把图缩小**：算出的宽必须 **≥ 该图的常规嵌入宽**（`FIG_WIDTH`／默认 0.66），
#        否则一律**嵌入** —— 这正是用户反馈"很多图很小"的根因：手填的 0.40–0.45 < 嵌入 0.66；
#     ④ 纵横比须落在 `[AW_MIN_ASPECT, AW_MAX_ASPECT]`（过于细高／过于扁长都不适合环绕）。
#   取同时满足①～④的**最大宽**；无解则不环绕。预演输出中**逐图打印判定依据**（含纵横比与结论）。
AUTO_WRAP = True
AW_MIN_TEXT_W = 0.42               # 图侧正文栏最小占比
AW_MAX_FIG_H_CM = 8.0              # 环绕图的最大高度（cm）
AW_MAX_ASPECT = 1.60               # 高宽比上限
AW_MIN_ASPECT = 0.30               # 高宽比下限
TEXT_CM = 16.0                     # 版心宽（A4 21cm − 左右各 2.5cm 页边距）
# ⑤ 例外名单（**必须写明理由**，否则会退化成"又靠手填"）：键＝论文内索引号。
AW_NO_WRAP = {
    "5-17": "其后紧邻 §5.4.2 的展示式 (5-24)（收缩律插值式）；环绕侧栏（0.43 版心）容不下该式，"
            "v19 实测 Overfull 98.5pt ＋ 公式压图重叠 ⟹ 该图必须嵌入（嵌入宽 0.60，图更大）。",
    "5-12": "★ v22（用户第 3、4 条）：环绕后「图往左下偏」、且**预留行数溢出到下一页**"
            "（第 16 页文字为它留了空位、而图整个在第 15 页）——这是 `wrapfigure{r}` 的固有表现"
            "（图不居中、预留行数难精确）⟹ 改回**嵌入**（嵌入宽 0.60，图反而更大）。",
}
FIG_DIR_ABS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "05_成品图")
_FIG_CM_CACHE = {}


def _fig_size_cm(fn):
    """实测成品图单页尺寸（cm）⟹ (宽, 高)；读不到返回 None。**一次读取、进程内缓存**。"""
    if fn not in _FIG_CM_CACHE:
        _v = None
        try:
            import fitz
            with fitz.open(os.path.join(FIG_DIR_ABS, fn)) as _d:
                _r = _d[0].rect
                _v = (_r.width / 72.0 * 2.54, _r.height / 72.0 * 2.54)
        except Exception:
            _v = None
        _FIG_CM_CACHE[fn] = _v
    return _FIG_CM_CACHE[fn]


def auto_wrap(num, real, w_embed):
    """自动判定该图是否环绕 ⟹ 返回 (宽, 靠边) 或 None（None＝按常规嵌入，保持大图）。"""
    if not AUTO_WRAP or len(real) != 1:
        return None
    if num in AW_NO_WRAP:
        print("      · 图%-4s 不环绕（例外名单：%s）" % (num, AW_NO_WRAP[num].split("；")[0]))
        return None
    sz = _fig_size_cm(real[0])
    if not sz or sz[0] <= 0:
        return None
    aspect = sz[1] / sz[0]
    w_by_text = 1.0 - AW_MIN_TEXT_W
    w_by_h = AW_MAX_FIG_H_CM / (TEXT_CM * aspect)
    w = min(w_by_text, w_by_h)
    why = []
    if not (AW_MIN_ASPECT <= aspect <= AW_MAX_ASPECT):
        why.append("纵横比%.2f越界" % aspect)
    if w < w_embed:
        why.append("环绕宽%.3f<嵌入宽%.3f（环绕会缩小图）" % (w, w_embed))
    if w < AW_MIN_TEXT_W * 0.95:
        why.append("环绕宽%.3f过小" % w)
    if why:
        print("      · 图%-4s 不环绕（%s）" % (num, "；".join(why)))
        return None
    print("      · 图%-4s **环绕** 宽 %.3f（纵横比 %.2f；嵌入宽 %.3f）" % (num, w, aspect, w_embed))
    return (w, "r")
                                  # ★ v16（用户指令）：**等比放大到约原来的 1.5 倍**（0.30 × 1.5 = 0.45）
                                  #   ——理由是宽度每增 1 倍、图内文字同倍放大，0.30 下实测图内仅
                                  #   **1.7–4.1pt**（不可读），0.45 下约 **2.6–6.2pt**；且正文仍全部
                                  #   排在图的**左侧**（`r` ＝图靠右、文字绕左）。
                                  #   ⚠ 代价：图高由 ~150pt 增至 **~239pt（≈19 行）**，而 §5.2.3 内在该图
                                  #   之后**连续正文约 15 行（≈189pt）** ⟹ **可能不足以绕满** ⟹ 编译后
                                  #   必须复测"全文重叠"（判据见 `_overlap` 检查），若溢出则据实回退一档。
PAIR_OF = {}                       # 图号 → 其并置伙伴（双向登记，供 `md2tex` 就近配对）
for _a, _b in FIG_PAIRS:
    PAIR_OF[_a], PAIR_OF[_b] = _b, _a


def _fig_env(note, body, cap_tex, num, env=True, width_tex=None):
    """把**图片内容行**装进 `figure` 环境（图题在下）。

    `env=False` 时只返回「注释 ＋ 内容 ＋ 题注」三段（**不套 figure 环境**），供 `fig_pair_block`
    放进 `minipage` 并置；题注与 `\\label` 始终随图，故编号与 `\\ref` 不受呈现方式影响。
    """
    core = list(body) + ["  \\caption{%s}\\label{fig:%s}" % (cap_tex, num)]
    if not env:
        return [note] + core
    return [note, "\\begin{figure}[htbp]", "  \\centering"] + core + ["\\end{figure}"]


def fig_block(num, cap, env=True, width_tex=None):
    """图注行 → figure 环境（图题在下）。

    图片路径**依《A_图表编号对照.md》**给出**候选命名链**（PDF 文件索引号 → F 号 → 论文内索引号，
    即 `\\fgphchain`），运行到任何一个即自动显示；三者皆缺时退化为占位框（**工程仍可编译**），
    框内同时列出三个候选名，便于贵方对号投放。
    """
    STAT["fig"] += 1
    FIG_SEEN.add(num)
    esc_cap = inline(cap, cite=False)
    info = FIGMAP.get(num)
    # ★ **实时动态链接**：一律用**相对路径**指向 `50_论文/05_成品图/`（本工程在 `50_论文/04_…/` 下，
    #   故相对路径为 `../../05_成品图/`）；**禁用绝对路径**。成品图改名/替换后重编译即生效。
    #   依次尝试：PDF 文件索引号（图NN）→ F 号 → 论文内索引号；同名时先查 05_成品图、再查本地 figures/。
    LIVE = FIG_REL
    # ★ **存在性判断移到生成器**（Python 侧按 `50_论文/05_成品图/` 实况核对）：
    #   命中 ⟹ 直接 `\includegraphics` 该相对路径（**必然加载成功**）；未命中 ⟹ 占位框。
    #   这样既不依赖 TeX 的 `\IfFileExists`（对中文名/后缀脆弱），也不会因缺图而中断编译。
    # 分幅图：对照表的 PDF 索引号列写作 `图05（a/b）`，须**去掉括号部分**再作查找键，
    # 否则 `图05（a/b）` 查不到实况目录里的 `图05a-…`／`图05b-…`（本轮 3 张分幅图因此走占位）。
    key_pdf = re.sub(r"[（(].*$", "", info["pdf"]).strip() if info else ""
    real = FIGFILES.get(key_pdf.replace(" ", ""), []) if info else []
    note = ("%% 图%s ＝ %s（F 号）／%s（PDF 文件索引号）／%s"
            % (num, info["F"], info["pdf"], info["name"])) if info else (
            "%% ★ 图%s 在《A_图表编号对照.md》中**无比对行**" % num)
    if real:
        # 分幅图并排：**总宽**取该图口径（默认 0.66，可在 `FIG_WIDTH` 逐张覆盖），再按幅数均分；
        # 并置成对时 `width_tex="\linewidth"`，即以所在 `minipage` 的宽为总宽。
        unit = width_tex or "\\textwidth"
        w = (1.0 if width_tex else FIG_WIDTH.get(num, FIG_W_DEFAULT)) / len(real)
        body = "  \\hfill ".join(
            "\\includegraphics[width=%.3f%s]{%s%s}" % (w, unit, LIVE, f) for f in real)
        # ★ v14：**环绕排版**（`wrapfig`）——正文绕图排，图不再独占一块版面。
        #   题注用 `\captionof{figure}`（caption 包已加载）⟹ **编号/`\label` 与计数器语义不变**，
        #   正文 `\ref` 一字不改；不用 `figure` 浮动体 ⟹ 不会被推成"整页只有一张图"。
        #   ★ v20：宽度**不再手填** —— 先查人工覆盖 `WRAP_FIGS`，否则交 `auto_wrap()` 自动判定
        #   （判据见文件头说明：**环绕不得把图缩小**，否则一律嵌入，保证图够大）。
        if width_tex:                      # 并置图：由 `fig_pair_block` 以 `\linewidth` 放进 minipage
            _wf = None                     # ⟹ **不做环绕判定**（否则日志会误报"该图将环绕"）
        elif not env or len(real) != 1:
            _wf = None
        else:
            _wf = WRAP_FIGS.get(num) or auto_wrap(num, real, FIG_WIDTH.get(num, FIG_W_DEFAULT))
        if _wf and env and not width_tex and len(real) == 1:
            _wf_w, _wf_side = _wf
            return [note,
                    "\\begin{wrapfigure}{%s}{%.3f\\textwidth}" % (_wf_side, _wf_w),
                    "  \\centering",
                    "  \\includegraphics[width=\\linewidth]{%s%s}" % (LIVE, real[0]),
                    "  \\vspace{2pt}",
                    "  \\captionof{figure}{%s}\\label{fig:%s}" % (esc_cap, num),
                    "\\end{wrapfigure}"]
        # ★ 浮动定位用 `[htbp]`（**不用 `[H]`**）：`[H]` 是"绝对就地"语义，当页内剩余空间不足时
        #   会把整页剩余空白弃用、连同后续正文一起推到下一页，实测在本文工程中造成 **9 页纯空白**
        #   （全文 63 → 54 页，内容一字未删）。官方第八条对字体字号行距"不作统一要求"，
        #   且"表题在上、图题在下"与编号纪律均不受浮动定位影响，故此处统一取标准浮动。
        return _fig_env(note, [body], esc_cap, num, env, width_tex)
    cands = [LIVE + n for n in ([info["pdf"], info["F"]] if info else []) + ["fig-%s" % num, "图%s" % num]]
    cands += ["figures/" + c for c in cands]
    note = ("%% 图%s ＝ %s（F 号）／%s（PDF 文件索引号）／%s"
            % (num, info["F"], info["pdf"], info["name"])) if info else (
            "%% ★ 图%s 在《A_图表编号对照.md》中**无比对行**（见生成末缺口报告）" % num)
    w_tex = width_tex or ("%.3f\\textwidth" % FIG_WIDTH.get(num, FIG_W_DEFAULT))
    return _fig_env(note, ["  \\fgphchain{%s}{%s}" % (w_tex, ",".join(cands))],
                    esc_cap, num, env, width_tex)


def fig_pair_block(a, capa, b, capb):
    """两图**并置成对**：同一 `figure` 环境内两个 `minipage`，**各自保留图号与 `\\label`**。

    编号仍由 `figure` 计数器连续产出（正文 `\\ref` 一字不改，`\\caption` 各归其图）；每幅宽 `PAIR_W`，
    中间以 `\\hfill` 分隔，合计 ≈ 0.97 版心宽 ⟹ 不再"两张竖排大图各占大半页"。配置见 `FIG_PAIRS`。
    """
    blocks = []
    if (a, b) in WRAP_STACK or (b, a) in WRAP_STACK:
        # ★ v22（用户第 5 条）：**竖直排列的环绕式**——两图同宽（各占 `\linewidth`）、整体**靠左**，
        #   正文从右侧绕排；两图各带自己的 `\captionof` ⟹ 编号与 `\label` 语义不变（`\ref` 一字不改）。
        _w = WRAP_STACK.get((a, b)) or WRAP_STACK.get((b, a))
        st = ["\\begin{wrapfigure}{l}{%.3f\\textwidth}" % _w, "  \\centering"]
        for num, cap in ((a, capa), (b, capb)):
            core = fig_block(num, cap, env=False, width_tex="\\linewidth")
            st += ["  " + l.strip() for l in core[1:] if l.strip()] + ["  \\vspace{4pt}"]
        st += ["\\end{wrapfigure}"]
        return st
    for num, cap in ((a, capa), (b, capb)):
        # 计数交由 `fig_block` 统一承担（此处再计数会重复）
        core = fig_block(num, cap, env=False, width_tex="\\linewidth")   # 注释行 ＋ 内容行 ＋ 题注行
        blk = [core[0],
               "  \\begin{minipage}[t]{%.3f\\textwidth}" % PAIR_W_BY.get(num, PAIR_W),
               "    \\centering"]
        blk += ["    " + l.strip() for l in core[1:] if l.strip()]
        blk += ["  \\end{minipage}"]
        blocks.append(blk)
    return (["\\begin{figure}[htbp]", "  \\centering"]
            + blocks[0] + ["  \\hfill"] + blocks[1] + ["\\end{figure}"])


def md2tex(lines, cite=True, appendix_figs=None):
    """逐行转换（公式块、表、图、普通段落、注）。

    `appendix_figs` 非空时：**附录图（图A-n）的 figure 环境不在正文落地**，而是收集到该列表、
    由附录统一呈现（编号冻结不变，正文 `\\ref` 仍指向该图）—— 这既符合"附录图"的定位，
    也避免 30 张图把**正文页数**推过 30 页红线（见 README『页数』一节）。
    """
    out, i, n = [], 0, len(lines)
    held = None          # ★ 并置成对：先出现的图暂挂于此，待伙伴出现时合并（见 `FIG_PAIRS`）
    while i < n:
        ln = lines[i]
        s = ln.strip()
        if s in ("", "---", "<!--"):
            i += 1
            continue
        # ★ **哨兵通道**：结构性 LaTeX 命令以 `@@…@@` 形式在源行里传递，**在本函数内**、
        #   经 `inline()` 处理标题文字后一次性生成 ⟹ 根除"预生成 LaTeX 又被转义"的双重处理
        #   （该缺陷曾使 267 处标题显示为 `\textbackslash{}section\{…\}`）。
        mS = re.match(r"^@@(SEC|SUB|SUB2|RAW|APPENDIX)@@(.*)$", s)
        if mS:
            kind, rest = mS.group(1), mS.group(2).strip()
            if kind == "RAW":
                out.append(rest)
            elif kind == "APPENDIX":
                out.append("\\appendix")
            else:
                out.append("\\%s{%s}" % ({"SEC": "section", "SUB": "subsection",
                                          "SUB2": "subsubsection"}[kind], inline(rest, cite=False)))
            i += 1
            continue
        if s.startswith("%"):                    # LaTeX 注释行原样保留
            out.append(s)
            i += 1
            continue
        if s.startswith("$$"):                                    # 公式块
            out += eq_block(s)
            i += 1
            continue
        if s.startswith("|"):                                     # 表块
            rows, aligns = [], None
            j = i
            while j < n and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                    # ★ v11：**记住 md 的对齐行**——`:---:` 居中 ／ `:---` 左 ／ `---:` 右；
                    #   纯 `---` 表示"不指定"，仍用自动启发式（短列居中、长列左）。
                    #   这样"列对齐"在**原 md**里就是唯一真源（改 md 即改排版），
                    #   无需在生成器里逐表硬编码。
                    aligns = cells
                else:
                    rows.append(cells)
                j += 1
            notes = []
            while j < n and lines[j].strip().startswith(">"):
                notes.append(lines[j].strip().lstrip("> ").strip())
                j += 1
            # ★ 回溯取题注行：**题注必须从正文里"取走"**（与表格自身的 `\caption` 重复印两遍属缺陷）：
            #   ① `表~\ref{tab:1}　30 分钟内药材的温度…` —— 源侧"表 1"已被 `inline()` 转成 `\ref`；
            #   ② `表 5-2　三套物性参数…` —— 源侧写法不在 `inline()` 的转换名单内，仍是原样。
            #   旧实现只在 ② 形态里 `pop`，① 形态**只取号不取走** ⟹ 题注行留在正文里、与 `\caption`
            #   重复（实测 24 处：表 1-1／2-1／0-1／5-1／表 1–表 6／表 A-1 各分块）。
            #   另两处形态须兼容：**附录 A-1 首块**为"表名行 ＋ 分块题注行"**两行连续题注**（只取最近者
            #   作题注，其余一并取走）；**附录 1.3i 块**为"题注 → 注行 → 表格"（容忍中间夹一行非题注）。
            # ★ 变量名必须避开 `j`（`j` 是"表块扫描位置"，末尾 `i = j` 依赖它；
            #   曾因改用 `j` 做回溯 ⟹ `i` 跳错行、正文成段丢失）。
            cap, lab, skipped, q = "", "", 0, len(out) - 1
            while q >= 0 and skipped <= 1:
                cur = out[q].strip()
                if cur == "":
                    q -= 1
                    continue
                m2 = re.match(r"^表~?\\ref\{tab:([^}]+)\}\s*(.*)$", cur)
                if m2:
                    new = (m2.group(1), m2.group(2).strip())
                elif re.match(r"^表\s*[A-Za-z0-9-]+[　\s]", cur):
                    mm = re.match(r"表\s*([A-Za-z0-9-]+)", cur)
                    new = (mm.group(1), cur)
                else:
                    # 非题注：**只容忍一行"纯文本"（表前的注行）**；遇到结构性行
                    # （`\end{longtable}`／`\caption…`／`\begin{figure}` 等以 `\` 开头者）**立即停止**
                    # —— 否则会把**上一张表**的题注"偷"来当本题注（实测：表 5-1 的题注被下一块窃取，
                    #   造成该块题注错位、原表 `\label` 丢失 ⟹ 15 处未定义引用）。
                    if cur.startswith("\\") or skipped >= 1:
                        break
                    skipped += 1
                    q -= 1
                    continue
                if not cap:                 # 取**最近**的一条为题注（更远者仅取走、不采用）
                    lab, cap = new
                out.pop(q)
                q -= 1
            if not cap:                       # 无题注的表（正文内嵌对照表等）：**不设题注、不占表号**
                lab = lab or ""
            cap = re.sub(r"^表\s*[A-Za-z0-9-]+[　\s]*", "", cap).strip()   # 题注去掉旧表号（号由计数器出）
            out += [""] + table_block(cap, rows, notes, lab, aligns) + [""]
            i = j
            continue
        m = re.match(r"^图\s*(A-\d+|\d+-\d+)[　\s]*(.+)$", s)      # 图注行
        if m:
            num = m.group(1).replace(" ", "")
            cap = m.group(2).strip()
            if appendix_figs is not None and num.startswith("A-"):
                appendix_figs.append((num, cap))                   # 附录图：交由附录呈现
                out.append("% " + ("图%s「%s」为附录图，figure 环境移至附录统一呈现（编号冻结）"
                                   % (num, cap)))
            elif PAIR_OF.get(num):                                 # ★ 并置成对（配置见 `FIG_PAIRS`）
                buddy = PAIR_OF[num]
                if held and held[0] == buddy:                      # 伙伴已挂起 ⟹ 此刻合并成对
                    out += [""] + fig_pair_block(buddy, held[1], num, cap) + [""]
                    held = None
                else:                                             # 尚未见伙伴 ⟹ 挂起等它（就近配对）
                    held = (num, cap)
            else:
                out += [""] + fig_block(num, cap) + [""]
            i += 1
            continue
        if s.startswith("> "):                                    # 注 / 说明
            out.append(inline(s[2:], cite=cite))
            out.append("")
            i += 1
            continue
        out.append(inline(s, cite=cite))
        # ★ **段落分隔（关键）**：源 Markdown 以"空行"分段，而这些空行会被上面的
        #   `if s in ("", "---", "<!--")` 分支**跳过丢弃**。若不在此补回空行，相邻两段在 TeX 源里
        #   只以**单个换行**相隔 ⟹ 被 TeX 当作同一段落而**合并成一大段、完全不换行**。
        #   症状：问题重述的四问、模型假设的八条"全部挤成一段"；含图表的章节因浮动体两侧自带空行，
        #   掩盖了该缺陷，故长期未被发现。
        out.append("")
        i += 1
    if held:                       # 配置了成对、但源里只出现一张 ⟹ 单独呈现（**绝不丢图**）
        out += [""] + fig_block(held[0], held[1]) + [""]
    return out


# ───────────────────────── 章装配 ─────────────────────────
GEN_VERSION = "gen_latex/v11"  # v11：**表格列竖直居中（`p`→`m`）＋ 列对齐改由**原 md 的对齐行**驱动（`:---:`/`:---`/`---:`）＋ 文件名清单按字符预算打包（修"程序名超出页面"）＋ 行内代码与文件名在 `.` 后也加断点 ＋ 附录 B 代码字号降为 `\scriptsize`（修 80 字符横幅行越界）；v10：**表格列宽按各列内容加权分配**（旧实现各列均分 ⟹ 短列过宽、长列过窄；新增 `\settabw`／`\tblw`）；v9：附录 B 代码块等宽字体改用 `\lstmonofam`（DejaVu Sans Mono，修代码注释中 ★／希腊字母／数学符号的 `Missing character` 留空）；版式接口判定改为按**转义形态**比对（旧实现永远判"版本不一致"⟹ 每次重生成都覆盖贵方版式）；v8：题面表后全局回退 `table` 计数器（消除补充表 +6 偏移 ⟹ 呈现号＝登记号；纯渲染修复）；v7：题面强制表（表 1–表 6）改用独立计数器 reqtab 全篇连续编号（其余表仍"章-序"）；v6：行距改用 ctexart 类选项（linespread=1.06）；v5：列宽计入 \tabcolsep ＋ 表 \label 去重 ＋ 图宽 0.66

PREAMBLE = r"""% ============================================================================
% A 题 · 论文 LaTeX 前言（preamble）—— 由 50_论文/02_章节稿/gen_latex.py 生成
% GEN_LATEX_VERSION: @@GENVER@@
% 设计依据：kb《AI论文插图与LaTeX排版》＋ 官方《论文格式规范》＋ 我方《内容与排版绘图交接说明》§四
% 编译：xelatex 两遍（见 README_排版交付说明.md）
% ============================================================================
% ★ 行距用 **ctexart 的类选项**指定（`linespread=<值>`），**不可用 `\linespread`**：
%   ctex 会在 \begin{document} 处按自身方案重设 \baselinestretch，故前言区的 `\linespread{}` 会被覆盖
%   （实测：`\linespread{1.12}` 与 `\linespread{1.09}` 页数完全相同，证实其为**空操作**）。
\documentclass[12pt,a4paper,linespread=1.0]{ctexart}

\usepackage{geometry}\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}  % 官方第一条

% ---- ★ v4 新增：版面调参区（属**模板接口**；贵方如需自定义，改本区块即可，或取回 preamble.tex.bak）----
% 依据：官方第八条明示"论文中的**字号、字体、行距**不作统一要求"，故以下取值均为可选优化，非官方要求。
% 目的：正文页数由"内容侧已触底"后的 32 页收进官方第四条红线（≤30 页），并消除版面松散感。
% 行距：见上方 \documentclass 的 `linespread=1.06` 类选项（前置件的 `\linespread` 会被 ctex 覆盖）。
% 浮动体密度：允许每页承载更多浮动体，避免"整页只有一张图/表"的松散页
\setcounter{topnumber}{4}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{6}
\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.90}
\renewcommand{\textfraction}{0.06}
\renewcommand{\floatpagefraction}{0.75}
% -----------------------------------------------------------------------------
\usepackage{amsmath,amssymb}
\usepackage{booktabs}          % 三线表（\toprule/\midrule/\bottomrule），全篇无竖线
\usepackage{longtable}         % 长表：自动重复表头（对应"（续）"要求）
\usepackage{array}
% 图片搜索路径：**相对路径实时链接** 50_论文/05_成品图（禁用绝对路径），并保留本地 figures/ 备选
\usepackage{graphicx}\graphicspath{{../../05_成品图/}{figures/}}
\usepackage{float}
\usepackage{wrapfig}          % ★ v14：个别图改"环绕"排版（用户指令，见 `WRAP_FIGS`）
% ★ v14：带圈数字 ①–⑳（U+2460–U+24FF）划入 CJK 字符类——否则会被送到 Times New Roman
%   （本件 `\setmainfont{Times New Roman}`）而 Times 无此字形 ⟹ 产生 `Missing character`。
\xeCJKDeclareCharClass{CJK}{"2460 -> "24FF}
\usepackage[font=small,labelsep=quad]{caption}
\usepackage{listings}
\usepackage{pifont}            % ★ v12：`\ding{51}` 供代码注释里的 ✅ 字形
% ★ v12 新字符兜底：代码注释里 DejaVu Sans Mono 缺 ⟹(U+27F9)／✅(U+2705) ⟹ PDF 留空（44 处
%   `Missing character`）。用 `newunicodechar` 映射到已有字体里的同义字形 —— **不改 code/ 字节**。
\usepackage{newunicodechar}

ewunicodechar{⟹}{\ensuremath{\Longrightarrow}}

ewunicodechar{✅}{\ding{51}}
\usepackage{xcolor}
\usepackage[hidelinks]{hyperref}
% ★ v12 图表"留白"收紧（用户反馈；官方第八条 ⟹ 可自定）。实测：收紧 `	extfloatsep`／
%   `\intextsep`／`\floatsep` 到 8–9pt **会引起长表分块 `Overfull \vbox`（254／260pt）**
%   ⟹ 已回退为**默认浮动体间距**，只收紧**题注间距**（实测 0 vbox／0 hbox）。
\setlength{\abovecaptionskip}{5pt}
\setlength{\belowcaptionskip}{0pt}

% ---- 源程序（附录 B）：文件放入 code/ 即自动嵌入，缺位时显示占位框（保证可编译）----
% 注：文件名含下划线（`q1_core.py`），故一律经 `\detokenize` 处理，避免被当作数学下标。
% ★ v9：代码改用等宽字体 `\lstmonofam` —— `\ttfamily`（lmmono）**缺 ★／希腊字母／数学符号字形**，
%   代码注释里的这些符号会在 PDF 中**留空**（`Missing character` 警告）；改用覆盖更广的 DejaVu Sans Mono，
%   字体不可用时自动退回 `\ttfamily`（不影响编译）。**仅作用于附录 B 的代码块**。
\IfFontExistsTF{DejaVu Sans Mono}{\newfontfamily\lstmonofam{DejaVu Sans Mono}}{\let\lstmonofam\ttfamily}
\newcommand{\srcfile}[1]{%
  \edef\srcpath{\detokenize{#1}}%
  % ★ v11：代码字号由 `\footnotesize`（10pt）降为 `\scriptsize`（9pt）—— 实测 `code/*.py`
  %   第 4 行的 80 字符 `=` 横幅注释在 10pt 等宽下宽 481.6pt，超版心 455.2pt 达 **26.4pt**
  %   （日志 7 处 `Overfull \hbox`，附录 B 代码块内文字越出边框）；9pt 下 80 字符仅 433.4pt，
  %   且嵌入集内最长行恰为 80 字符 ⟹ 全部收回版心。`breaklines=true` 保留作二次保险。
  \IfFileExists{code/\srcpath}{\lstinputlisting[breaklines=true,basicstyle=\lstmonofam\scriptsize]{code/\srcpath}}%
  {\fbox{\parbox[c][1.1cm][c]{0.9\textwidth}{\centering\ttfamily\footnotesize 源程序 \detokenize{#1}（放入 code/ 目录后自动嵌入）}}}}

% ---- 图片：**依《A_图表编号对照.md》的命名候选链自动解析** ----
% `\fgphchain{宽度}{候选1,候选2,候选3}`：依次尝试 `候选.pdf`／`候选.png`，命中即插入；
% 三个候选分别为 PDF 文件索引号（图NN，交付命名）／F 号／论文内索引号，皆缺则显示占位框
% （框内列出候选名，便于贵方对号投放）。**工程在任何情况下均可编译**。
\makeatletter
\newcommand{\fgphchain}[2]{%
  \def\fgfound{0}%
  \@for\fcand:=#2\do{%
    \ifnum\fgfound=0
      \IfFileExists{\fcand}{\includegraphics[width=#1]{\fcand}\def\fgfound{1}}{%
        \IfFileExists{\fcand.pdf}{\includegraphics[width=#1]{\fcand}\def\fgfound{1}}{%
          \IfFileExists{\fcand.png}{\includegraphics[width=#1]{\fcand}\def\fgfound{1}}{}}}%
    \fi}%
  \ifnum\fgfound=0
    \fbox{\parbox[c][2.6cm][c]{#1}{\centering 图占位\\\ttfamily\footnotesize #2}}%
  \fi}
\makeatother
\newcommand{\fgph}[2][0.82\textwidth]{\fgphchain{#1}{#2}}

% ---- 摘要页与关键词 ----
\newcommand{\keywords}[1]{\par\vspace{0.8em}\noindent\textbf{关键词：}#1\par}

% ---- 编号：**全部由 LaTeX 计数器在编译期动态生成**（源文件内不写死任何图/表/式号）----
%  章-序 连字符风格（式 (5-1)、图 5-1、表 5-1；附录自动成 表 A-1、图 C-1）；`\label`-`\ref` 自动跟随。
\numberwithin{equation}{section}
\numberwithin{figure}{section}
\numberwithin{table}{section}
% ---- ★ v7：题面强制表（表 1–表 6）的**独立计数器** ----
%     六张题面表由生成器在**组内**把 `\thetable` 改写为 `\arabic{reqtab}` ⟹ 全篇连续 1–6；
%     本文补充表（表 5-1）与附录表（表 A-1）仍走"章-序" ⟹ 编号纪律与《A_图表编号对照.md》不变。
\newcounter{reqtab}
\renewcommand{\theequation}{\thesection-\arabic{equation}}
\renewcommand{\thefigure}{\thesection-\arabic{figure}}
\renewcommand{\thetable}{\thesection-\arabic{table}}

% ---- 表格：列宽**按各列内容加权分配**（旧实现各列均分 ⟹ 短列过宽、长列（说明／作用）过窄）----
% 用法：每张表前 `\settabw{2n}`（n ＝ 列数）先记下可用宽度，各列 p{} 再按月其**份额**取用。
\newlength{\tblw}
\newcommand{\settabw}[1]{\setlength{\tblw}{\dimexpr0.97\textwidth-#1\tabcolsep\relax}}

% ---- 列表（源程序语言高亮）----
\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,frame=single,
        numbers=left,numberstyle=\tiny,columns=fullflexible,keepspaces=true}

% ---- 标题层级：章/节/子节（不加人为断页；表题在上、图题在下由生成器保证）----
\ctexset{section={format=\Large\bfseries,aftername=\quad},
         subsection={format=\large\bfseries,aftername=\quad},
         subsubsection={format=\normalsize\bfseries,aftername=\quad}}
"""

MAIN = r"""% ============================================================================
% A 题 · 论文主文件（由 gen_latex.py 生成；本文件只做 \input 装配，内容在各分节文件）
% GEN_LATEX_VERSION: @@GENVER@@
% 结构：摘要专用页 → 正文（第一章…第七章）→ AI 工具使用声明 → 参考文献 → 附录
%       —— 顺序依官方规范与《AI 工具使用规定》第 3 条（AI 声明在参考文献之前）
% ============================================================================
\input{preamble}

\begin{document}

\input{frontmatter/00_摘要页}          % 官方第三条：摘要专用页（含标题与关键词，≤1 页）

\input{sections/01_问题重述}
\input{sections/02_问题分析}
\input{sections/03_模型假设}
\input{sections/04_符号说明}
\input{sections/05_模型建立与求解}      % 含 5.5（原 A_09 结果分析，已并入本章）
\input{sections/06_模型检验}
\input{sections/07_模型评价与推广}
\input{sections/08_AI工具使用声明}      % 不编号；位置在参考文献之前
\input{sections/09_参考文献}
\input{sections/10_附录}

\end{document}
"""


def strip_head(txt):
    """标题去序号：`## 5.1.3 离散格式…` → `离散格式…`；`## 一、模型优点` → `模型优点`。"""
    txt = re.sub(r"^#+\s*", "", txt.strip())
    txt = re.sub(r"^附录\s*[A-Z]\s*[　\s]*", "", txt)
    txt = re.sub(r"^\d+(\.\d+)*[　\s]*", "", txt)
    txt = re.sub(r"^[一二三四五六七八九十]+、\s*", "", txt)
    return txt.replace("*", "").strip()


def build():
    files = {}
    for key, fn in [("01", "A_01_题目.md"), ("02", "A_02_摘要.md"), ("04", "A_04_问题重述.md"),
                    ("05", "A_05_问题分析.md"), ("06", "A_06_模型假设.md"), ("07", "A_07_符号说明.md"),
                    ("08", "A_08_模型建立与求解.md"), ("09", "A_09_结果分析.md"),
                    ("10", "A_10_模型检验.md"), ("11", "A_11_模型评价与改进.md"),
                    ("12", "A_12_AI工具使用声明.md"), ("13", "A_13_参考文献.md"),
                    ("14", "A_14_附录.md")]:
        files[key] = body_of(fn).split("\n")

    W = {}

    # ── frontmatter/00_摘要页（A_01 题名 ＋ A_02 摘要与关键词）──
    title = strip_head(files["01"][0])
    paras = [l.strip() for l in files["02"][1:] if l.strip() and not l.strip().startswith("#")]
    kw = [p for p in paras if p.startswith("关键词")]
    abs_paras = [p for p in paras if p not in kw]
    # ★ v13：**摘要页格式按 kb 口径**（《2025国赛备战最强资料》§6.2）——题目 **16 号**加粗居中／
    #   摘要标题 **14 号**加粗居中（独立成行）／摘要内容 12 号、**行距 1.25**（用户指令：本页可宽、
    #   正文仍单倍）／关键词 12 号加粗居左。官方第三条只规定"摘要专用页、含标题与关键词、≤1 页"。
    # ★ v14：**题目换行点**（用户报"标题换行不合理"）——实测原断行落在 **"达标时／间"**：
    #   **断在词中间**，且两行 448pt ／ 160pt **极不平衡**（版心 453pt）。
    #   此处给**显式换行**（改下表一行即可移动换行位置）：断在"耦合模型的建立"之前 ⟹
    #   上行「药材的烘干问题：圆柱非稳态传热传质」(18 字 ≈288pt)、下行「耦合模型的建立、达标时间反演与收缩效应分析」(21 字 ≈336pt)，
    #   两行均衡、且均不出现"行首标点"与"断词"。
    TITLE_BREAK_BEFORE = "建立、达标时间反演与收缩效应分析"
    if TITLE_BREAK_BEFORE in title:
        title = title.replace(TITLE_BREAK_BEFORE, "\\\\" + TITLE_BREAK_BEFORE, 1)
    L = ["% 摘要专用页（官方第三条：含标题与关键词，不超过一页；电子版论文第一页即本页）",
         "\\thispagestyle{plain}", "{\\linespread{1.25}\\selectfont",
         "\\begin{center}", "  {\\zihao{3}\\bfseries %s}" % title,
         "\\end{center}", "", "\\vspace{0.4em}",
         "\\begin{center}\\zihao{4}\\bfseries 摘要\\end{center}", "", "\\vspace{0.2em}", ""]
    for p in abs_paras:
        L += [inline(p), ""]
    if kw:
        L.append("\\keywords{%s}" % inline(kw[0].split("：", 1)[-1], cite=False))
    L += ["}", "% ← 关闭「摘要内容行距 1.25」分组（正文仍 1.0 单倍）", "",
          "% 摘要页边界：官方要求摘要单独一页（属**前置件边界**，非「章/节间人为断页」）",
          "\\clearpage"]
    W["frontmatter/00_摘要页.tex"] = L

    # ── 正文各章（标题映射：见文件头"分节决策"）──
    APPX_FIGS = []

    def section_chapter(key, sec_title, sub_of_h2=True, h3="subsubsection", prelude=None):
        src = files[key]
        out = ["@@SEC@@" + sec_title]
        if prelude:
            out += prelude
        top_seen = False
        for ln in src:
            if ln.startswith("#"):
                lvl = len(ln.split(" ")[0])
                head = strip_head(ln)
                if not top_seen and lvl <= 2 and head:
                    top_seen = True
                    if head != sec_title and not sub_of_h2:
                        out.append("@@SUB@@" + head)
                    continue
                out.append(("@@SUB@@" if lvl == 2 else "@@SUB2@@") + head)
            else:
                out.append(ln)
        # ★ **不再把附录图路由到附录**：30 张图原样落在各自的 6.x 节（"哪里引用、哪里出现"），
        #   否则它们会连续堆在文末，形成"大量图集中在结尾"（本轮取证：附录内 30 张图行号 363–566，7 行一张）。
        body = md2tex(out)
        SRCNAME = {"04": "A_04_问题重述.md", "05": "A_05_问题分析.md", "06": "A_06_模型假设.md",
                   "07": "A_07_符号说明.md", "10": "A_10_模型检验.md", "11": "A_11_模型评价与改进.md"}
        return ["% 来源：成文/" + SRCNAME.get(key, "")] + body

    W["sections/01_问题重述.tex"] = section_chapter("04", "问题重述")
    W["sections/02_问题分析.tex"] = section_chapter("05", "问题分析", sub_of_h2=True)
    W["sections/03_模型假设.tex"] = section_chapter("06", "模型假设")
    W["sections/04_符号说明.tex"] = section_chapter("07", "符号说明")

    # ── 第五章：A_08（5.0–5.4）＋ A_09（5.5）合并 ──
    src08, src09 = files["08"], files["09"]
    merged = []
    for ln in src08:
        if ln.startswith("# ") and "模型建立与求解" in ln:
            continue
        merged.append(ln)
    for ln in src09:
        if ln.startswith("# ") and "5.5" in ln:
            merged.append("## 5.5 四问结果的横向对照与讨论")
            continue
        merged.append(ln)
    seq = ["@@SEC@@模型建立与求解",
           r"% 本章子节编号自 5.0 起（计数器置 -1：首个子节即 5.0）—— 属**计数器机制**，非写死编号",
           "@@RAW@@\\setcounter{subsection}{-1}"]
    for ln in merged:
        if ln.startswith("## "):
            seq.append("@@SUB@@" + strip_head(ln))
        elif ln.startswith("### "):
            seq.append("@@SUB2@@" + strip_head(ln))
        elif ln.startswith("#"):
            continue
        else:
            seq.append(ln)
    W["sections/05_模型建立与求解.tex"] = (
        ["% 来源：成文/A_08_模型建立与求解.md ＋ 成文/A_09_结果分析.md（原 5.5，并入本章）"] + md2tex(seq))

    W["sections/06_模型检验.tex"] = section_chapter("10", "模型检验")
    W["sections/07_模型评价与推广.tex"] = section_chapter("11", "模型评价与推广")

    # ── AI 工具使用声明（不编号，置参考文献之前）──
    ai = files["12"]
    ai_txt = [l for l in ai if l.strip() and not l.startswith("#")]
    W["sections/08_AI工具使用声明.tex"] = [
        "% 官方《人工智能工具使用规定》第 3 条：置于**参考文献之前**，措辞逐字采用第（2）式",
        "\\section*{AI 工具使用声明}", "\\addcontentsline{toc}{section}{AI 工具使用声明}"] + md2tex(ai_txt)

    # ── 参考文献（thebibliography ＋ \bibitem）──
    refs = [l.strip() for l in files["13"][1:] if re.match(r"^\[\d+\]", l.strip())]
    biblio = ["% 官方第七条：按科技论文规范列出；正文引用处以 \\cite 上标标注（GB/T 7714）",
              "\\begin{thebibliography}{99}"]
    for r in refs:
        m = re.match(r"^\[(\d+)\]\s*(.+)$", r)
        STAT["cite"] += 1
        biblio.append("\\bibitem{ref%s} %s" % (m.group(1), inline(m.group(2), cite=False, ref=False)))
    biblio.append("\\end{thebibliography}")
    W["sections/09_参考文献.tex"] = biblio

    # ── 附录（A–C；附录 B 依《附录B_代码块对应源文件.md》补源程序嵌入位）──
    apx = ["% 官方第四、五、十一条：附录页数不限；含支撑材料文件列表与全部可运行源程序",
           "@@APPENDIX@@"]
    cur = None
    for ln in files["14"][1:]:
        if ln.startswith("# "):
            continue
        if ln.startswith("## "):
            cur = strip_head(ln)
            apx.append("@@SEC@@" + cur)
            continue
        apx.append(ln)
    W["sections/10_附录.tex"] = md2tex(apx)
    if APPX_FIGS:                       # 附录补充图：正文只引用，图环境在附录统一呈现
        W["sections/10_附录.tex"] += [
            "", "% ---- 附录补充图（正文以 图A-n 引用；图环境在此呈现，编号冻结）----",
            "\\section{附录补充图}",
            "\\noindent 共 %d 张（正文以 \\ref 引用；编号由计数器动态生成，与附录 A–C 同属自动编号体系）。"
            % len(APPX_FIGS)]
        for num, cap in sorted(APPX_FIGS, key=lambda x: int(x[0].split("-")[1])):
            W["sections/10_附录.tex"] += [""] + fig_block(num, cap)
    # 附录 B：源程序（官方第五条：**全部完整、可运行的源程序**）
    #   ★ 收录口径（v4 · 用户裁定）：**只嵌入关键程序正文**（`KEY_BLOCKS` ＝ B.1–B.7：公共模块
    #     ＋ 四问求解的交付核与主流程）；其余块与 B.13 **只列文件名清单**（不全量收录），
    #     非关键部分的全文随支撑材料提交并在附录 A 表 A-1 逐项登记（官方第十一条）。
    #   ① B.1–B.12 按《附录B_代码块对应源文件.md》的块序处理；
    #   ② B.13 ＝ `code/` 目录下**其余全部源程序**（**递归含 `innov/`**）的**文件名清单**（不嵌正文），
    #      确保"完整收录"义务不留缺口（与块内文件不重复）。
    #   ★ 结构口径（本轮修复）：块清单**并入「附录 B」之内**，**不再另立 \section** ——
    #     原实现会额外生成一个与附录 B 同名的第 4 节（「源程序（代码块 B.1--B.13）」），
    #     使附录出现两个"源程序"节、且排在附录 C 之后，属结构重复。
    apx_tail = ["", "% ---- 附录 B 源程序块清单：按《附录B_代码块对应源文件.md》块序列出（并入附录 B）----", "\\small"]
    if EMBED_CODE:      # ★ 代码注释里的 ℃／①-④ 不属 xeCJK 默认 CJK 区间、等宽字体亦无字形
        apx_tail += ["% ---- ℃／①-④ 交 xeCJK 的 CJK 字体渲染（等宽字体无此字形，代码注释会留空）----",
                     '\\xeCJKDeclareCharClass{CJK}{"2103 -> "2103, "2460 -> "24FF}']
    shown = set()
    mp = os.path.join(ROOT, "50_论文", "04_交排版成图方", "附录B_代码块对应源文件.md")
    if os.path.isfile(mp):
        for ln in io.open(mp, encoding="utf-8").read().split("\n"):
            m = re.match(r"^\|\s*\*\*(B\.\d+)\*\*\s*\|([^|]*)\|([^|]*)\|", ln)
            if not m:
                continue
            blk = m.group(1)
            names = []
            for x in re.findall(r"`([^`]+)`", m.group(3)):
                fn = re.sub(r"^code/", "", x.strip()).strip()   # 去掉映射表里的 `code/` 前缀
                if fn and fn not in names and not fn.endswith("_"):
                    names.append(fn)
            apx_tail += ["", "\\noindent\\textbf{%s\\quad %s}" % (blk, inline(m.group(2).strip(), cite=False))]
            if blk in KEY_BLOCKS:       # ★ 关键程序：正文逐块嵌入
                for fn in names:
                    apx_tail.append(src_line(fn))
            else:                       # 其余块：只列文件名清单（不嵌正文）
                apx_tail += ["\\noindent\\footnotesize 本块为检验脚本，正文不随附录印出；"
                             "源文件全文随支撑材料提交，文件名与附录 A 表 A-1 逐项对应："] + src_list(names)
            shown.update(names)
    CODE_DIR = os.path.join(OUT, "code")
    rest = sorted(os.path.relpath(os.path.join(dp, f), CODE_DIR).replace(os.sep, "/")
                  for dp, _, fs in os.walk(CODE_DIR) for f in fs
                  if f.endswith((".py", ".ps1"))
                  and os.path.relpath(os.path.join(dp, f), CODE_DIR).replace(os.sep, "/") not in shown
                  ) if os.path.isdir(CODE_DIR) else []      # ★ 递归（含 `innov/`），不再只扫顶层
    if rest:
        apx_tail += ["", "\\noindent\\textbf{B.13\\quad 其余源程序（清单，正文不嵌入）}",
                     "\\noindent\\footnotesize 下列 %d 个文件与 B.1–B.12 不重复（含改进链脚本 "
                     "innov/）；全部源程序随支撑材料提交，并在附录 A 表 A-1 逐项登记；"
                     "检验日志与结果数据同属支撑材料。" % len(rest)] + src_list(rest)
    if not EMBED_CODE:          # ★ 统一出口：关闭代码嵌入时，把**所有** `\srcfile{…}` 降级为文件名
        apx_tail = [re.sub(r"\\srcfile\{([^}]+)\}",
                           lambda m: "\\noindent\\texttt{%s}\\\\" % m.group(1).replace("_", "\\_"), l)
                   for l in apx_tail]
    # ★ 结构修复：把源程序块清单**插入「附录 B」节内**（紧接表 B-1 之后），
    #   使其归属正确、不再生成重复的「源程序」第 4 节；锚点缺失时回退为追加（保证可编译）。
    ANCHOR = "\\section{关键中间结果与图示说明}"
    tex10 = W["sections/10_附录.tex"]
    if ANCHOR in tex10:
        i = tex10.index(ANCHOR)
        W["sections/10_附录.tex"] = tex10[:i] + apx_tail + [""] + tex10[i:]
    else:
        W["sections/10_附录.tex"] = tex10 + apx_tail
    # ★ 自检（"自检而非我以为"）：报告附录 B 的嵌入／清单规模，并**逐个核对**嵌入文件在 code/ 就位
    #   —— 嵌入文件缺失时，`\srcfile` 只会画占位框、代码不出现（编译仍"成功"），必须显式报出。
    _emb = [f for l in apx_tail for f in re.findall(r"\\srcfile\{([^}]+)\}", l)]
    _lst = [f for l in apx_tail for f in re.findall(r"\\texttt\{([^}]+)\}", l)]
    _miss = [f for f in _emb
             if not os.path.isfile(os.path.join(CODE_DIR, f.replace("/", os.sep)))]
    print("  ⤓ 附录 B：正文嵌入关键程序 %d 项 ｜ 文件名清单 %d 项 ｜ 嵌入文件缺失 %d%s"
          % (len(_emb), len(_lst), len(_miss), ("（" + "、".join(_miss) + "）") if _miss else ""))
    return W


def sync_code():
    """把**交付源程序**（`20_交付包/09_代码与复现/code/`）**递归镜像**到 `交付排版方论文/code/`。

    口径（v4 修复，对应三处缺口）：
      ① **递归复制 `.py`／`.ps1`，保留 `innov/` 子目录** —— 原实现用 `os.listdir` 只取顶层，
         `code/innov/` 下 45 个改进链脚本**全部漏投**（其中 34 个既不进工程、也不进 B.13）
         ⟹《附录B_代码块对应源文件.md》中 `code/innov/…` 的路径无从解析；
      ② **镜像清理** —— 目标目录内不在本次同步集的 `.py`／`.ps1`（含旧布局残留的顶层副本）
         一律删除，杜绝"同一文件两份"；旧口径投下的日志／结果数据一并清除；
      ③ 只投**源程序** —— 检验日志与结果数据属支撑材料，不进本目录。
    这样附录 B 的 `\\srcfile` 才有实体可嵌；同时写入投放说明，便于贵方核对与替换。
    """
    src = os.path.join(ROOT, "20_交付包", "09_代码与复现", "code")
    dst = os.path.join(OUT, "code")
    if not os.path.isdir(src):
        print("  ✗ 未找到交付代码目录，跳过：%s" % src)
        return 0, []
    rels = sorted(os.path.relpath(os.path.join(dp, f), src).replace(os.sep, "/")
                  for dp, _, fs in os.walk(src) for f in fs if f.endswith((".py", ".ps1")))
    n_innov = len([r for r in rels if r.startswith("innov/")])
    if not APPLY:                       # ★ 预演**不写盘**：镜像同步会删旧件，不得在预演中发生
        print("  ⤓ （预演）应镜像源程序 %d 个（含 innov/ %d 个）→ code/；未落盘" % (len(rels), n_innov))
        return len(rels), rels
    os.makedirs(dst, exist_ok=True)
    for rel in rels:
        p = os.path.join(dst, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, "w", encoding="utf-8", newline="").write(
            io.open(os.path.join(src, rel.replace("/", os.sep)), encoding="utf-8",
                    errors="replace").read())
    keep, pruned = set(rels), []
    for dp, _, fs in os.walk(dst):
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), dst).replace(os.sep, "/")
            if rel == "README_源程序投放说明.md":
                continue
            if f.endswith((".py", ".ps1")) and rel not in keep:
                os.remove(os.path.join(dp, f))          # 旧布局残留（如顶层副本）
                pruned.append(rel)
            elif not f.endswith((".py", ".ps1")) and os.path.isfile(os.path.join(src, f)):
                os.remove(os.path.join(dp, f))          # 旧口径投下的日志／结果数据
                pruned.append(rel)
    io.open(os.path.join(dst, "README_源程序投放说明.md"), "w", encoding="utf-8", newline="\n").write(
        "# 源程序（附录 B 用）\n\n"
        "> 本目录由 `50_论文/02_章节稿/gen_latex.py` 从 `20_交付包/09_代码与复现/code/` **递归镜像**而来"
        "（保留 `innov/` 子目录）。\n\n"
        "- 源程序 **%d** 个（`.py`／`.ps1`，其中 `innov/` **%d** 个，含改进链脚本）；检验日志与结果数据属支撑材料，**不在本目录**。\n"
        "- 附录 B **只嵌入关键程序正文**（B.1–B.7：公共模块 ＋ 四问求解）；其余（B.8–B.12 检验脚本、"
        "B.13 其余脚本）**只列文件名清单**，全文随支撑材料提交。块序见 `04_交排版成图方/附录B_代码块对应源文件.md`。\n"
        "- **替换/新增源程序**：请改 `20_交付包/09_代码与复现/code/` 后重跑生成器（本目录**镜像同步**："
        "源目录没有的 `.py`／`.ps1` 会被删除）。\n"
        % (len(rels), n_innov))
    tail = ("（%s%s）" % ("、".join(pruned[:6]), "…" if len(pruned) > 6 else "")) if pruned else ""
    print("  ⤓ 随包镜像源程序：%d 个（含 innov/ %d 个）→ code/；清理旧件 %d 个%s"
          % (len(rels), n_innov, len(pruned), tail))
    return len(rels), rels


def write(W):
    # ★ `main.tex`／`preamble.tex` 属**排版方版式件**：只在缺失时生成，已存在则**保留不覆盖**
    #   —— 使贵方的字号/行距/宏包改动在后续重新生成时**不被冲掉**（稳定工作流）。
    KEEP = {"main.tex", "preamble.tex"}
    for rel, lines in sorted(W.items()):
        p = os.path.join(OUT, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if rel in KEEP and os.path.isfile(p):
            cur = io.open(p, encoding="utf-8", errors="replace").read()
            # ★ 版式接口版本判定：写盘时 `_` 会被转义（`gen\_latex/v8`），故须按**转义形态**比对，
            #   否则永远判为"版本不一致"⟹ 每次重生成都覆盖贵方的版式改动（旧实现的实际行为）。
            if GEN_VERSION in cur or GEN_VERSION.replace("_", "\\_") in cur:
                print("  ♻ 保留（已存在，未覆盖）%-30s" % rel)
                continue
            io.open(p + ".bak", "w", encoding="utf-8", newline="\n").write(cur)
            print("  ⬆ 版式接口升级（已备份 %s）%-24s" % (os.path.basename(p) + ".bak", rel))
        if p.endswith(".tex"):     # ★ 全局兜底：数学环境之外的 `_`／`^` 一律转义（根治 Missing $ 一类错误）
            fixed, envc = [], 0
            for l in lines:
                if re.search(r"\\begin\{(equation|align|gather|multline|eqnarray|aligned|cases)", l):
                    envc += 1
                if envc > 0 or re.search(r"\\end\{(equation|align|gather|multline|eqnarray|aligned|cases)", l):
                    fixed.append(l)
                    if re.search(r"\\end\{(equation|align|gather|multline|eqnarray|aligned|cases)", l):
                        envc -= 1
                    continue
                o, inm, i2 = [], False, 0
                while i2 < len(l):
                    c = l[i2]
                    if l.startswith("\\srcfile{", i2):      # ★ 源程序路径**不转义** `_`：
                        j = l.find("}", i2)                 #   `\srcfile{q1\_core.py}` 会被 `\detokenize`
                        o.append(l[i2:j + 1])               #   还原成 `q1\_core.py` ⟹ `\IfFileExists`
                        i2 = j + 1                          #   判为不存在（只显占位框，代码不嵌入）
                        continue
                    if c == "\\" and i2 + 1 < len(l):
                        o.append(l[i2:i2 + 2]); i2 += 2; continue
                    if c == "$":
                        inm = not inm; o.append(c); i2 += 1; continue
                    if c in "_^" and not inm:
                        o.append("\\" + c); i2 += 1; continue
                    o.append(c); i2 += 1
                fixed.append("".join(o))
            lines = fixed
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines).rstrip() + "\n")
        print("  ✍ %-42s %d 行" % (rel, len(lines)))


sync_code()          # 先随包源程序（附录 B 的"其余源程序"清单依赖 code/ 实体）
W = build()
W["preamble.tex"] = PREAMBLE.replace("@@GENVER@@", GEN_VERSION).split("\n")
W["main.tex"] = MAIN.replace("@@GENVER@@", GEN_VERSION).split("\n")

# ── 图表编号对照（**以最新 `A_图表编号对照.md` 为准**）随包清单 ──
FIG_HINT = ["# 图片投放说明（figures/）—— 依《A_图表编号对照.md》",
            "",
            "每张图给出**三个候选文件名**（按此顺序解析，`.pdf` 优先，其次 `.png`）：",
            "",
            "1. `图NN.pdf` —— **PDF 文件索引号**（交付命名，首选）；",
            "2. `F-xx.pdf` —— F 号（规格卡命名）；",
            "3. `fig-<论文内索引号>.pdf` —— 本工程原名。",
            "",
            "三者任一放入即可自动显示；**皆缺时正文显示「图占位」框（框内列出候选名），工程仍可编译**。",
            "",
            "| 论文内索引号 | F 号 | PDF 文件索引号 | 图名 | 候选命名（依次尝试） |",
            "|---|---|---|---|---|"]
for _k in sorted(FIGMAP, key=lambda x: (x[:1], len(x), x)):
    _v = FIGMAP[_k]
    FIG_HINT.append("| 图%s | %s | %s | %s | `figures/%s` → `figures/%s` → `figures/fig-%s` |"
                    % (_k, _v["F"], _v["pdf"], _v["name"], _v["pdf"], _v["F"], _k))
if FIG_ORPHANS:
    FIG_HINT += ["", "> **已收割但尚未进论文**（《对照表》中「论文内索引号」为空，本工程不引用）："
                 + "；".join("%s %s（%s）" % (f, n, p) for f, n, p in FIG_ORPHANS)]
W["figures/README_图片投放说明.md"] = FIG_HINT

README = r"""# 交付排版方论文 · LaTeX 工程说明（我方 → 排版成图方）

> **来源**：本工程由 `50_论文/02_章节稿/成文/A_*.md` 的**标记正文**（`<!-- LATEX-EXPORT:BEGIN/END -->`）
> 自动生成，生成器＝`50_论文/02_章节稿/gen_latex.py`（改正文 → 重跑生成器 → 内容同步）。
> **设计依据**：本地 kb 引擎（`kb/engine/p5_search.py`）检出的《AI论文插图与LaTeX排版》
> ＋ 官方《论文格式规范》（kb 原文）＋ `04_交排版成图方/A_内容与排版绘图交接说明.md` §四。

## 一、编译（稳定工作流）

```bash
xelatex main.tex     # 第一遍：写标签位置
xelatex main.tex     # 第二遍：填交叉引用编号（kb：XeLaTeX 至少两遍）
# 或：latexmk -xelatex main.tex
```

实测（TeX Live 2026 / XeLaTeX）：**0 编译错误**、**0 未定义引用或题录**、**0 `Float too large`**、**0 `Overfull \vbox`**；
含附录 **@@PAGES@@ 页**（其中**正文 @@BODY@@ 页**，见 §六 页数；该两数由生成器**自动读取上一次编译的实测值**，重编译后重跑生成器即同步，避免手写的页数记录与实测不符）。

## 二、文件归属（谁可以改、重生成时会不会被覆盖）

| 文件 | 归属 | 重新生成时 |
|---|---|---|
| `sections/*.tex`、`frontmatter/*.tex` | **我方内容**（自动生成） | **覆盖**（内容以成文为准，勿在此改文字） |
| `main.tex`、`preamble.tex` | **贵方版式**（字号／行距／宏包／页面） | **只在缺失时生成**，已存在则**保留不覆盖** |
| `figures/` | **贵方投放**（成品图） | 仅投放说明，不生成内容 |
| `code/` | **我方镜像**（源程序，来源 `20_交付包/09_代码与复现/code/`） | **镜像同步**（源目录没有的 `.py`／`.ps1` 会被删除） |

> 内容疑问 → 回询我方（`交接说明` §六）；**贵方不改内容、我方不改版式**。

## 三、分节决策（对"原有分节是否合理"的处置，逐条可核）

**① 合并写入**（原文分处不同文件，LaTeX 中属同一结构单元）

| 处置 | 说明 |
|---|---|
| 题名 ＋ 摘要 ＋ 关键词 → **摘要专用页**一件 | 官方第三条：电子版第一页＝摘要专用页（含标题与关键词，≤1 页）；关键词行取自摘要件 |
| 原"结果分析（5.5）"→ **并入第五章**「模型建立与求解」 | 它本就是该章的 5.5 节（生成后为 `\subsection`，编号自动为 5.5） |

**② 排除不写**（不能／不应写入 LaTeX 的成分）

各稿的**元信息块、占位清单、自查、撰写说明、引用位置对照、字段核验留痕、变更记录**，
以及关键词件的**选择理由表**（内部论证）—— 由正文标记界定，**定稿件本身不含这些内容**。

**③ 结构映射**

| LaTeX | 来源 |
|---|---|
| `\section` | 问题重述／问题分析／模型假设／符号说明／模型建立与求解／模型检验／模型评价与推广 |
| `\subsection`／`\subsubsection` | 各章 5.0–5.5、6.1–6.11、2.1–2.4 等（**编号与我们冻结的章-节号一致**） |
| `\section*{AI 工具使用声明}` | 不编号；**位置在参考文献之前**（官方 AI 规定第 3 条） |
| `thebibliography`＋`\bibitem` | 18 条题录（GB/T 7714）；正文引用处为 `\textsuperscript{\cite{...}}` |
| `\appendix`＋附录 A／B／C | 附录 A 支撑材料文件列表（长表）、附录 B 源程序、附录 C 中间结果索引 ＋ **附录补充图（图A-1–图A-30）** |

> **附录图的处置**：图A-1–图A-30 由正文（第六章）**引用**，figure 环境**统一在附录呈现**——
> 既符合"附录补充图"的定位，也避免 30 张图把**正文页数**推过官方 30 页限制（实测省 7 页）。

## 四、编号已冻结（**请勿重排而不改引用**）

图 `5-n`／`6-n`（第六章图按章号连续）、表 **一律"章-序"**（`1-1／2-1／4-1／5-1…5-10／A-1／B-1／C-1` —— 原"题面强制表呈现为 表 1–表 6"的独立编号已按用户口径**取消**，全篇表号统一）、式 `(5-n)`／`(6-n)`、题录 `[1]–[18]`
（**口径**：章节稿中的 `表 0-1` 是**内部标签键**，编译期按章号呈现为 **表 4-1**；同理第六章的图以 `fig:A-n` 为标签键、呈现为 **图 6-n**。正文引用一律走 `\ref`，PDF 内自洽。）
**全部显式写号**，与 `50_论文/03_对照与索引/A_图表编号对照.md` 及正文引用**逐号一致**。
正文引用已用 `\ref`／`\eqref`／`\cite` 建立交叉引用（编译两遍即自洽）；
若贵方按自有体系重排编号，请**同步改写引用**（我方回收验收清单第 4 项核对编号漂移）。

## 五、图与源程序的投放

* **图（依 `03_对照与索引/A_图表编号对照.md` 自动解析）**：每张图给出**三个候选文件名**，
  依次尝试、命中即插入（`.pdf` 优先，其次 `.png`）：
  ① `figures/图NN.pdf`（**PDF 文件索引号**，交付命名）→ ② `figures/F-xx.pdf`（F 号／规格卡命名）
  → ③ `figures/fig-<论文内索引号>.pdf`（本工程原名）。
  三者皆缺时显示「图占位」框（框内列出候选名），**工程仍可编译**；逐号清单见 `figures/README_图片投放说明.md`。
* **源程序（附录 B）**：**已随包递归镜像**至 `code/`（来源 `20_交付包/09_代码与复现/code/`，
  含 `innov/` 子目录 ＝ 改进链脚本）。附录 B **只嵌入关键程序正文**（B.1–B.7：公共模块 ＋ 四问求解的
  交付核与主流程），其余（B.8–B.12 检验脚本、B.13 其余脚本）**只列文件名清单**（正文不全量收录），
  全文随支撑材料提交并与附录 A 表 A-1 逐项对应；块序见 `04_交排版成图方/附录B_代码块对应源文件.md`。
  如需替换，请改源目录后重跑生成器（本目录**镜像同步**：源目录没有的 `.py`／`.ps1` 会被删除）。
  **不写运行环境与硬件信息**（官方体例）。

## 六、页数（实测）与官方红线

| 编译口径 | 实测 |
|---|---|
| 摘要专用页 | **1 页**（**不跨页**，含标题与关键词） |
| **正文（不含附录）** | **@@BODY@@ 页** ✅ 在官方第四条红线（≤30 页）之内 |
| 全文（含附录） | **@@PAGES@@ 页**（附录页数官方**不限**） |
| 版面质量 | `Float too large` **0**｜`Overfull \vbox` **0**｜稀疏页（＜300 字且无图表的正文页）**0** |

> **页数与"收口"说明**：官方第四条要求**正文不超过 30 页**。本工程正文 **@@BODY@@ 页**，已达标；余量＝30 − 本页数
> （本页数由生成器**自动读取编译实测值**回填，故重编译后重跑生成器即可刷新）。`13_论文可删减部分` 的删简项保留作缓冲。
> 达标由**两条腿**共同支撑：① **内容侧**（各章按《A_论文减法优化计划》逐层压缩，表 1–表 6 与全部数值未动）；
> ② **版式侧**——官方第八条明示"字号、字体、行距**不作统一要求**"，故 `preamble.tex` 的
> "**v4 版面调参区**"（`\linespread{1.12}` ＋ 浮动密度）属**可选优化**：
> **贵方可整体采纳、替换或撤销**（旧版已备份为 `preamble.tex.bak`）；我方未改动该区块之外的任何版式设置。

> **★ 图表嵌版（本轮机制修复，请勿回退）**：
> ① **表一律用非浮动 `longtable`** —— 浮动态表一旦高于一页即触发 `Float too large` 而被**截断**
>    （此前实测：符号表超 111.13pt、第五章选型表超 73.43pt、**附录 11 张表超 70–1440pt**），
>    且会被推成"浮动页"造成"整页只有一张表"。改后长表超页自动分页并重复表头（题注自带"（续）"时不重复标记）。
> ② **图宽按"逐张口径"配置**（生成器 `FIG_WIDTH`／`FIG_PAIRS`，**改脚本即可，不必动 `sections/*.tex`**）——
>   默认 **0.66 `\textwidth`**；信息密度高的框图**放足整版文字宽度**（图 5-1 ＝ **1.00**）；
>   机制同源的两图**并置成对**（图 5-5／图 5-6 ＝ 各自 **0.485**：同一 `figure` 内两个 `minipage`，
>   **各自保留图号与 `\label`**，正文 `\ref` 不变）。既利于与正文同页，也消除"整页一张图"。

**已落实的其他红线**：无目录 ✓｜表题在上、图题在下 ✓｜三线表（booktabs，全篇无竖线）✓｜
长表 `longtable` 自动重复表头并标「（续）」✓｜**不在章/节间加人为断页** ✓（唯一 `\clearpage`
位于摘要页之后，属"前置件边界"，为官方第三条"摘要单独一页"所需）｜图内无标题与编号 ✓｜
匿名（无身份/学校/赛区信息）✓。

## 七、回收验收

按 `A_内容与排版绘图交接说明.md` **§七 回收验收清单（8 项）**逐项核对；回稿后我方复跑：

```bash
python 50_论文/01_写作计划/code/build_indexes.py --check
python 50_论文/01_写作计划/code/paper_lint.py --mode doc --dir 50_论文
```
"""

# ★ 页数自动回填：读上一次编译的实测值（`main.log` 总页数；正文页数＝附录 A 起始页 − 2），
#   使 README 的页数记录**不再手写、不会与实测不符**（本表在重编译后重跑生成器即刷新）。
def _page_stats():
    total = body = None
    try:
        m = re.search(r"Output written on \S+ \((\d+) pages\)",
                      io.open(os.path.join(OUT, "main.log"), encoding="utf-8", errors="ignore").read())
        total = int(m.group(1)) if m else None
    except Exception:                                                # noqa: BLE001
        pass
    try:
        t = io.open(os.path.join(OUT, "main.aux"), encoding="utf-8", errors="ignore").read()
        m = re.search(r"支撑材料文件列表\}\{(\d+)\}", t)
        body = int(m.group(1)) - 2 if m else None
    except Exception:                                                # noqa: BLE001
        pass
    return total, body


_pt, _pb = _page_stats()
README = README.replace("@@PAGES@@", str(_pt) if _pt else "待编译") \
               .replace("@@BODY@@", str(_pb) if _pb else "待编译")
W["README_排版交付说明.md"] = README.split("\n")

print("LaTeX 工程生成（%s）→ %s" % ("落盘" if APPLY else "预演", OUT))
if APPLY:
    write(W)
print("  统计：图 %d ｜ 表 %d ｜ 编号式 %d ｜ 题录 %d ｜ 分节文件 %d"
      % (STAT["fig"], STAT["tab"], STAT["eq"], STAT["cite"], len(W)))

# ── 缺口报告（图表对照）──
_nomap = sorted(FIG_SEEN - set(FIGMAP), key=lambda x: (x[:1], len(x), x))
print("  图表对照：成文图号 %d 个 ｜ 对照表命中 %d ｜ **无比对行 %d**"
      % (len(FIG_SEEN), len(FIG_SEEN) - len(_nomap), len(_nomap)))
if _nomap:
    print("    ★ 无比对行的图号（需在《A_图表编号对照.md》补登）：%s" % " ".join(_nomap))
if FIG_ORPHANS:
    print("    ★ 已收割但未进论文（对照表末列为空）：%s"
          % "；".join("%s %s(%s)" % (f, n, p) for f, n, p in FIG_ORPHANS))
_used = sorted(k for k in FIGMAP if k in FIG_SEEN)
print("  对照表已回填且本工程已引用：%d 个" % len(_used))
if not APPLY:
    print("（预演不写盘；确认后加 --apply）")
