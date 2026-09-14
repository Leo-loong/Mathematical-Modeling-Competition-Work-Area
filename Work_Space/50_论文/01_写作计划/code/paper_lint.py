# -*- coding: utf-8 -*-
"""paper_lint —— 章节稿**机械门禁**（内容侧，只读检查）

定位：把《A_论文内容交付规范与约束》§十 的机检契约做成**可执行工具**，
      在**动笔前**即可自检其可用性（`--selftest`），在**写作中**逐节拦截 L1 硬约束违反。

覆盖（与约束编号对应）：
  R-1  W-07 内部代号零出现            R-2  W-01/03 数字回指《A_数值口径总表》
  R-3  W-13 图表占位被引用率          R-4  W-17 摘要禁项
  R-5  W-24 上标引用 ↔ 题录表双向      R-6  C-8/W-20/S-4 禁用词与绝对化表述
  R-7  S-2/S-6 风格密度（的字率/过渡词/高频词）
  R-8  ★ 表格完整性（含"未转义竖线破坏单元格"——本项目已发生 2 次的事故）
  R-9  W-08 编号白名单（只允许 图/表/式/文献 + 假设 H）
  R-10 W-34/W-35 干基标注 / 无量纲数定义式（提示级）
  R-11 DoD 章节稿元信息头与占位清单
  R-12 W-16 摘要四要素与数字个数          〔★ 参数类：**提示级**，暂定·不构成门禁〕
  ⚠ 参数/形态类规则（R-4／R-12／R-19）**一律为提示级**：其阈值来自外部源，属**暂定**、
    **不构成门禁**——**最终由用户在全稿完成后或写作过程中按具体情况决定**（见冲突记录表 C-01…C-18）。

  ---- 以下为"外部判据硬门禁"补充（逐条注明判据出处）----
  R-13 ★ 章节完整性：14 模块覆盖（**目录级**，见 main()）〔判据：赛题官方规范＋章节速查表〕
  R-14 编号连续递增（图/表/式无跳号无重复）        〔判据：赛前复盘"图表编号连续递增"〕
  R-15 图表占位后须紧跟解释句（"这意味着…"）      〔判据：赛前复盘"结果分析有含义解释"〕
  R-16 假设条目三要素（内容＋合理性依据＋适用范围）〔判据：赛前复盘"假设有合理性说明"〕
  R-17 禁推导跳步短语（化简得／易得／显然…）       〔判据：方法学 §2.6〕
  R-18 表外符号（正文符号须在《A_符号表》内）      〔判据：赛前复盘"符号是否全文统一"〕
  R-19 摘要须含"关键词"行（存在性＝门禁）          〔判据：官方"含关键词"；**个数＝C-02 暂定值，提示级**〕
  R-20 正文不得设"目录"章                          〔判据：一键式提示词"无目录"〕
  R-21 模型评价须优点／不足齐备                    〔判据：章节速查表"优点…缺点配改进"〕

用法：
  python paper_lint.py --selftest                     # 自检（内置样例，证明规则可用）
  python paper_lint.py --dir 50_论文/02_章节稿/基线      # 【draft 模式】检查章节稿（默认目录，自动适配）
  python paper_lint.py --file <某章节稿.md>            # 检查单文件
  python paper_lint.py --mode doc --dir 50_论文/01_写作计划   # 【doc 模式】文档体检：仅查数字溯源＋表格完整性
  python paper_lint.py --json                         # 机器可读输出
退出码：0 = 无 ❌；1 = 存在 ❌（可用于门禁流水线）

两种模式（**重要**）：
  draft —— **章节稿**专用：11 组全规则。对"约束／口径类文档"会产生**预期内假阳性**
           （那些文档本身就列举禁用词与内部代号作为反例）。
  doc   —— **文档体检**：只查 R-2 数字溯源 与 R-8 表格完整性，可用于检查我们自己的计划文档。

行内豁免：某行末尾写 `[lint-ignore]` ⟹ 该行跳过"逐行类"检查（用于引用反例／对照表）。
"""
import argparse
import glob
import io
import json
import os
import re
import sys

# ----------------------------------------------------------------------------- 基础
SEV_ERR, SEV_WARN, SEV_INFO = '❌', '⚠️', 'ℹ️'
SEV_ORDER = {SEV_ERR: 0, SEV_WARN: 1, SEV_INFO: 2}

CODE_PAT = re.compile(
    r'(?<![A-Za-z0-9])(RK-\d|MB-\d{2}|L3-\d{2}|[KEMNO]\d{1,2}(?![0-9A-Za-z])|D-\d{2}|E-\d{2}|0?5-G\d)')

WHITELIST_NUM = [
    re.compile(r'\bH\d{1,2}\b'),          # 假设
    re.compile(r'图\s*\d+'),               # 图表
    re.compile(r'表\s*\d+'),
    re.compile(r'图\s*[A-Za-z]\s*[-–]?\s*\d+'),   # 附录图号（图A-1）
    re.compile(r'\b[A-Za-z]\s*[-–]\s*\d+\b'),     # 附录图号的裸写形态（A-1）
    re.compile(r'式\s*\(?\s*\d+'),         # 公式
    re.compile(r'\[\d+\]'),                # 参考文献上标
    re.compile(r'F-\d{2}'),                # 图表规格卡号（占位用）
    re.compile(r'§\s*[\d.]+'),             # 节号
]

BANNED = [
    ('创新点', 'C-8 用"改进"不用"创新"'), ('创新项', 'C-8'), ('创新化', 'C-8'),
    ('进行了研究', 'S-4 通用句'), ('应用前景', 'C-1 摘要零区分力'),
    ('完美', 'W-20 绝对化'), ('最优解是', 'W-20'), ('绝对可靠', 'W-20'),
    ('效果良好', 'W-16 空洞表述'), ('结果令人满意', 'W-16'), ('精度较高', 'W-16'),
    ('在可接受范围内', 'W-31 误差敷衍'), ('较好地', 'W-16'),
]

AI_WORDS = ['因此', '所以', '然而', '但是', '此外', '另外', '同时', '综上所述',
            '值得注意的是', '总的来说', '不仅', '而且', '首先', '其次', '最后']

ABS_FORBID = [('$$', '摘要禁公式'), ('\\cite', '摘要禁引用'), ('\\ref', '摘要禁引用'),
              ('因为', '摘要禁解释性连词'), ('所以', '摘要禁解释性连词'),
              ('这是由于', '摘要禁解释性连词')]

DEC_PAT = re.compile(r'\d+\.\d{2,}')

# 图表编号：兼容两种形态 —— 论文内索引号 `图8-1`（模块-序）与 PDF/最终号 `图06`
FIGNUM = re.compile(r'图\s*(\d+(?:\s*[-–]\s*\d+)?)')
# ★ **附录图号**（`图A-1`／`图A-30`）：论文内索引号的一种**合法形态** —— 附录图统一以字母 A 为前缀，
#   与 PDF 文件索引号 `图NN`、正文图号 `图<章>-<序>` 三者分工互不混用；
#   原实现只识别后两者，致附录图号既未被登记也未被检查（见成文轮临时登记表 R10-01）。
APPXFIG = re.compile(r'图\s*([A-Za-z]\s*[-–]\s*\d+)')

SENT_SPLIT = re.compile(r'[。；！？]')


def sev(id_, sev_, msg_, line=None):
    return {'id': id_, 'sev': sev_, 'msg': msg_, 'line': line}


IGNORE_TAG = '[lint-ignore]'
# 文件级豁免：文首 1200 字符内出现 `[lint-ignore-file]` ⟹ **仅**跳过数字回指（R-2）
# 适用于"引用型"文档（如《A_判据源冲突记录表》），其数值是**引用外部判据的原句**，不是本论文数据。
IGNORE_FILE = '[lint-ignore-file]'


def _skip(ln):
    """行内豁免：该行末尾带 `[lint-ignore]` 时跳过"逐行类"检查（如引用反例、对照表）。"""
    return IGNORE_TAG in ln


_MASK_PATS = [
    r'§\s*\d+(?:\.\d+)*',                              # §6.11
    r'图\s*(?:\d+\s*[-–]\s*\d+|A\s*[-–]\s*\d+)',        # 图 5-16 ／ 图A-17
    r'表\s*(?:\d+\s*[-–]\s*\d+|A\s*[-–]\s*\d+|\d+)',    # 表 5-1 ／ 表A-1 ／ 表 5
    r'式\s*[（(]\s*\d+\s*[-–]\s*\d+\s*[）)]',             # 式 (5-1)
    r'\bQ\s*[1-4]\b',                                    # Q1–Q4
    r'\bF\s*-\s*\d{1,2}\b',                            # F-46
    r'\bL\s*\d{3,5}\b',                                 # 行号 L1234
    r'\d+\.\d+[a-z]?\s*节',                              # 6.11 节
    r'见\s*\d+\.\d+',                                    # 见 5.2.3
    r'[（(]\s*\d+\.\d+\s*[）)]',                          # （5.2.3）
    r'模块\s*\d+', r'假设\s*\d+(?:\s*[–-]\s*\d+)?',
    r'第[一二三四五六七八九十]+章',
    r'\b(?:R|E|D|K|M|N|O|W|G|IN|C|PR)-?\d+[A-Za-z]?\b',    # 内部口径/规则编号
    r'^\s*#{1,6}\s*\d+(?:\.\d+)*',
    r'\b\d{2}-[0-9A-Za-z.]+-\d{2,3}\b',                # 条目 ID（如 10-6.10-038／08-5.1.1b-010）
    r'`[^`\n]*`',                                       # 行内代码（含路径/编号/文件名）
    r'第[一二三四五六七八九十]+章[的\s：:]*[\d.]+(?:\s*[–／/、]\s*[\d.]+)*',   # 第六章 6.1–6.11
    r'(?:所属节|依据|见|详见|参见)[\s：:]*[\d.]+(?:\s*[–／/、]\s*[\d.]+)*',      # 所属节：6.10
    r'(?<![\d.])\d+\.\d+(?:\s*[–／/、]\s*\d+\.\d+)*(?=\s*(?:节|四段|各条|结构|对应|去重|相互印证|的))',
    r'\|\s*\d+\.\d+\s*\|',                          # 表格单元格内的节号
]


def _mask_sec(ln):
    """遮蔽**编号类**记号（节号／图号／表号／式号／内部编号），避免被当作物理量数值（假阳性来源）。"""
    for p in _MASK_PATS:
        ln = re.sub(p, lambda m: '·' * len(m.group(0)), ln)
    return ln


# ----------------------------------------------------------------------------- 规则
def r_code(text, name, ctx):
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln):
            continue
        for m in CODE_PAT.finditer(ln):
            out.append(sev('R-1/W-07', SEV_ERR, '出现内部代号 `%s`：%s' % (m.group(0), ln.strip()[:70]), i))
    return out


def r_number(text, name, ctx):
    if IGNORE_FILE in text[:1200]:
        return [sev('R-2/W-01', SEV_INFO,
                    '文件级豁免（`[lint-ignore-file]`）：数字回指检查跳过（本文件为引用型记录）')]
    ref = ctx.get('numbers')
    if not ref:
        return [sev('R-2/W-01', SEV_INFO, '未加载《A_数值口径总表》，数字回指检查跳过')]
    out, seen = [], set()
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln) or ln.lstrip().startswith('#') or ln.lstrip().startswith('|'):
            # 标题行中的 `2.11` 是节号，不是物理量；
            # ★ **表格行不参与逐值回指**：表格（尤其题面强制的表 1–表 6）的权威是**结果文件**，
            #   本项目对六表有"逐格一致"的独立核验；口径表只登记关键格，
            #   若把整表格值逐格要求回指口径表，会恒报大量假阳性（见成文轮临时登记表 R7-01）。
            continue
        ln = _mask_sec(ln)
        for m in DEC_PAT.finditer(ln):
            v = m.group(0)
            if v in ref:
                seen.add(v)
                continue
            if v in seen:
                continue
            if ln[m.end():m.end() + 2].strip().startswith('节'):
                continue
            out.append(sev('R-2/W-01', SEV_WARN,
                           '数值 `%s` 未在《口径总表》出现 —— 须回表核对（禁手抄/自算）' % v, i))
    return out


def r_figref(text, name, ctx):
    # ★ **台账表行不参与"应有编号"与"已被引用"的判定**：
    #   每节末「占位清单」表逐行列出论文内索引号与 PDF 索引号（如 `图01`／`图19`），
    #   它们是**交付台账**而非论文引用；不排除则这些编号恒报"未见引用句"
    #   （见成文轮临时登记表 R7-04）。
    body = '\n'.join(l for l in text.splitlines() if not l.lstrip().startswith('|'))
    defined = ({t.replace(' ', '') for t in FIGNUM.findall(body)}
               | {t.replace(' ', '') for t in APPXFIG.findall(body)}
               | set(re.findall(r'表\s*(\d+)', body)))
    used = set()
    for m in re.finditer(r'(?:如|见|参见|据|由)\s*图\s*((?:[A-Za-z]\s*[-–]\s*)?\d+(?:\s*[-–]\s*\d+)?)|图\s*((?:[A-Za-z]\s*[-–]\s*)?\d+(?:\s*[-–]\s*\d+)?)\s*所示', body):
        used |= {x.replace(' ', '') for x in m.groups() if x}
    # ★ 表引用同口径（修正：原实现只识别「图」引用、不识别「表」引用，
    #   致使**含表而无图的章节恒告警**（结构性误报）；见成文轮临时登记表 R3-01）
    for m in re.finditer(r'(?:如|见|参见|据|由)\s*表\s*(\d+)', body):
        used.add(m.group(1))
    # ★ 同一引用句内的**表号列表**（"见表 1 与表 2"／"见表 3、表 4"）亦属引用；
    #   原实现只收首个表号，致列表中的后续表恒报"未见引用句"（见成文轮临时登记表 R7-07）。
    for ln in body.splitlines():
        if re.search(r'(?:如|见|参见|据|由)\s*表', ln):
            used |= set(re.findall(r'表\s*(\d+)', ln))
    for m in re.finditer(r'表\s*(\d+)\s*所示', body):
        used.add(m.group(1))
    # ★ 表引用的**括号形式**（如"（表 0-1）"）亦属引用句 —— 中文论文中该形式与"见表 X"等价；
    #   原实现未收此形，致"表以括号引用"的章节恒告警（见成文轮临时登记表 R6-01）
    for m in re.finditer(r'[（(]\s*表\s*(\d+)', body):
        used.add(m.group(1))
    missing = sorted(defined - used)
    if defined and len(missing) == len(defined):
        return [sev('R-3/W-13', SEV_WARN,
                    '共有 %d 个图/表编号，但未见"如图 X 所示/见图 X"式引用句 ⟹ 疑未在正文引用' % len(defined))]
    if missing:
        return [sev('R-3/W-13', SEV_WARN, '图/表 %s 未见引用句' % ','.join('图' + m for m in missing[:10]))]
    return []


def _is_abstract(text, name):
    """摘要识别：文件名含"摘要"，或文首 400 字内出现以"摘要"起首的行（含标题形式）。"""
    if '摘要' in name:
        return True
    for ln in text[:400].splitlines():
        s = ln.strip().lstrip('#').strip()
        if s.startswith('摘要'):
            return True
    return False


def r_abstract(text, name, ctx):
    if not _is_abstract(text, name):
        return []
    out = []
    head = text[:4000]
    for token, why in ABS_FORBID:
        if token in head:
            # ★ 形态类＝提示级（出自教材 12.5 同一节，属暂定、不构成门禁）
            out.append(sev('R-4/W-17', SEV_WARN, '摘要含禁项 `%s`（%s）〔暂定·不构成门禁〕' % (token, why)))
    nums = DEC_PAT.findall(head)
    if len(nums) < 8:
        # ★ 参数类＝提示级（"≥8" 来自单源，属暂定、不构成门禁；见冲突记录表 C-01…C-18）
        out.append(sev('R-12/W-16', SEV_WARN,
                       '摘要精确数字仅 %d 个（外部源建议 ≥8）〔暂定·不构成门禁〕' % len(nums)))
    n_q = len(re.findall(r'针对问题\s*[一二三四]', head))
    if n_q < 4:
        out.append(sev('R-12/C-1', SEV_WARN,
                       '摘要中"针对问题X"式段首仅 %d 处（四问应各 1 处）' % n_q))
    if re.search(r'^\s*[1-9]\.\s', head, re.M):
        out.append(sev('R-4/W-17', SEV_WARN, '摘要出现分点符号（1. 2. 3.）〔暂定·不构成门禁〕'))
    return out


def r_refs(text, name, ctx):
    ref = ctx.get('refnums')
    sup = set(re.findall(r'\[(\d+)\]', text))
    if not ref:
        return [sev('R-5/W-24', SEV_INFO, '未加载题录表 §三，引用对应检查跳过（检出上标 %d 个）' % len(sup))]
    bad = sorted(sup - ref, key=int)
    if bad:
        return [sev('R-5/W-24', SEV_ERR, '上标 [%s] 在题录表中不存在' % ','.join(bad))]
    return []


def r_banned(text, name, ctx):
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln):
            continue
        for w, why in BANNED:
            if w in ln:
                out.append(sev('R-6/W-20', SEV_ERR if w in ('完美', '创新点', '创新项') else SEV_WARN,
                               '禁用表述 `%s`（%s）' % (w, why), i))
    return out


def r_style(text, name, ctx):
    out = []
    body = re.sub(r'^\|.*$', '', text, flags=re.M)      # 表格不计风格
    cjk = len(re.findall(r'[\u4e00-\u9fff]', body))
    if cjk > 200:
        dens = body.count('的') / float(cjk)
        if dens > 0.05:
            out.append(sev('R-7/S-6', SEV_WARN, '"的"字密度 %.1f%%（阈值 3%%–5%%，疑 AI 痕迹）' % (dens * 100)))
        elif dens < 0.03:
            out.append(sev('R-7/S-6', SEV_INFO, '"的"字密度 %.1f%%（低于 3%%）' % (dens * 100)))
    sents = max(1, len(SENT_SPLIT.findall(body)))
    tw = sum(body.count(w) for w in AI_WORDS)
    per = sents / float(max(1, tw))
    if tw and per < 5:
        out.append(sev('R-7/S-2', SEV_WARN, '过渡/AI 词 %d 个／%d 句 ≈ 每 %.1f 句 1 个（宜每 5–8 句 1 个）'
                       % (tw, sents, per)))
    for para in [p for p in body.split('\n\n') if len(p) > 120]:
        c = sum(1 for w in AI_WORDS if para.count(w) >= 1)
        if sum(para.count(w) for w in AI_WORDS) > 3:
            out.append(sev('R-7/S-6', SEV_WARN, '同一段落 AI 高频词 >3 个（%d 个）' % c))
            break
    return out


def r_table(text, name, ctx):
    """★ 表格完整性：列数一致 + 单元格内未转义竖线（本项目已发生 2 次）"""
    out, blk = [], []
    def chk(b):
        if len(b) < 2:
            return
        cnt = [x.count('|') for _, x in b]
        if len(set(cnt)) > 1:
            base = max(set(cnt), key=cnt.count)
            badln = [i for (i, x), c in zip(b, cnt) if c != base]
            out.append(sev('R-8', SEV_ERR, '表格列数不一致（期望 %d 个竖线）：行 %s'
                           % (base, ','.join(map(str, badln[:5]))), b[0][0]))
        for i, x in b:
            for m in re.finditer(r'\$[^$]*\$', x):
                if '|' in m.group(0) and '\\|' not in m.group(0):
                    out.append(sev('R-8', SEV_ERR,
                                   '单元格数学式内含**未转义竖线**（会截断表格）：`%s`' % m.group(0)[:60], i))
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith('|'):
            blk.append((i, ln))
        else:
            chk(blk); blk = []
    chk(blk)
    return out


def r_whitelist(text, name, ctx):
    """R-9：除白名单外，不应出现"字母+数字"式自造编号"""
    out, hits = [], set()
    for m in re.finditer(r'(?<![A-Za-z0-9])([A-Z]{1,3}-?\d{1,2})(?![0-9A-Za-z])', text):
        tok = m.group(1)
        if tok.startswith(('F-',)) or re.fullmatch(r'H\d{1,2}', tok):
            continue
        if any(p.fullmatch(tok) or p.match(tok) for p in WHITELIST_NUM):
            continue
        if CODE_PAT.fullmatch(tok):
            continue
        hits.add(tok)
    if hits:
        out.append(sev('R-9/W-08', SEV_INFO,
                       '出现疑似自造编号：%s（白名单仅 图/表/式/文献 + 假设 H；请确认）' % ','.join(sorted(hits)[:8])))
    return out


def r_domain(text, name, ctx):
    out = []
    if re.search(r'含水率', text) and not re.search(r'干基', text):
        out.append(sev('R-10/W-34', SEV_WARN, '出现"含水率"但全篇未见"干基"字样 ⟹ 首次出现处须注明干基'))
    uni = set(re.findall(r'(Bi_[mT]|Bi\b|\bFo\b)', text))
    if uni and not re.search(r'定义|=\s*\\frac|＝|=' , text):
        out.append(sev('R-10/W-35', SEV_INFO, '出现无量纲数 %s ⟹ 须给出定义式与本题取值' % ','.join(sorted(uni))))
    return out


def r_dod(text, name, ctx):
    need = ['素材来源', '真值核对', '术语核对', '占位清单', '自查']
    miss = [k for k in need if k not in text[:3000]]
    if miss:
        return [sev('R-11/DoD', SEV_WARN, '章节稿元信息头缺少：%s' % '、'.join(miss))]
    return []


SHORTCUT = ['化简得', '经过计算可得', '易得', '不难得到', '容易看出', '显然成立', '显而易见']
EXPLAIN = ('这意味着', '表明', '说明', '可见', '反映', '意味', '由此可见')
EVID_TOK = ('依据', '根据', '文献', '实测', '经验', '附录', '题面', '数据', '守恒', '定义')
RANGE_TOK = ('适用', '范围', '前提', '当 ', '若 ', '有效', '失效')


# 模块文件 → 论文章号（仅用于 R-14：区分"本章定义的图"与"引用他章的图"）
OWN_CH = {'A_04': 1, 'A_05': 2, 'A_06': 3, 'A_07': 4, 'A_08': 5, 'A_09': 5, 'A_10': 6, 'A_11': 7}


def _normalize_sym(s):
    return re.sub(r'[\s\\{}]', '', s)


def r_numbering(text, name, ctx):
    """R-14：图/表/式 编号连续递增，无跳号、无重复。

    图号支持两种形态：**论文内索引号** `图<章号>-<序>`（按章查连续）与 `图NN`（全文查连续）。
    ★ 只检查**本章自有**的图号分组：章节稿常**引用他章图号**（如"模型假设"节引第六章的检验图），
    若把他章图号并入本章分组，会恒报"图号不连续"（结构性误报）；见成文轮临时登记表 R5-01。
    """
    out = []
    # ★ **台账表行不参与编号连续性检查**：每节末「占位清单」逐行登记 F 号与 PDF 文件索引号
    #   （如 `图04`／`图05(a/b)`），它们是**交付台账编号**而非论文内索引号，
    #   计入则恒报"图号不连续"（见成文轮临时登记表 R10-02）。
    body = '\n'.join(l for l in text.splitlines() if not l.lstrip().startswith('|'))
    toks = [t.replace(' ', '') for t in FIGNUM.findall(body)]
    per = {}
    for t in toks:
        if '-' in t or '–' in t:
            a, b = re.split(r'[-–]', t)
            per.setdefault(int(a), set()).add(int(b))
    own = OWN_CH.get(name[:4])
    if per:
        for mod, idxs in sorted(per.items()):
            if own is not None and mod != own:
                continue                      # 他章图号：本文只引用、不定义 ⟹ 不查连续性
            miss = [n for n in range(1, max(idxs) + 1) if n not in idxs]
            if miss:
                out.append(sev('R-14/编号连续', SEV_WARN,
                               '图%d-? 编号不连续：缺 %s（现用 %s）'
                               % (mod, ','.join('图%d-%d' % (mod, m) for m in miss),
                                  ','.join('图%d-%d' % (mod, n) for n in sorted(idxs)[:12]))))
    else:
        nums = sorted({int(t) for t in toks})
        if nums:
            miss = [n for n in range(1, max(nums) + 1) if n not in nums]
            if miss:
                out.append(sev('R-14/编号连续', SEV_WARN,
                               '图号不连续：缺 %s（现用 %s）'
                               % (','.join('图%02d' % m for m in miss),
                                  ','.join('图%02d' % n for n in nums[:12]))))
    # ★ 表号：**章内要素表**（表 5-1／表A-1，按"章-序"编号）**不参与全篇连续序列**，
    #   仅检查**题面强制表（全篇连续 表 1–表 6）**的连续性。
    #   原实现把两类编号混作一列，致使"首张表为 表 N-1（N>1）"的章节恒报"缺 表1"（结构性误报）；
    #   见成文轮临时登记表 R4-01。
    for label, pat in (('表', r'表\s*(\d+)(?!\s*[-–]\s*\d)'),):
        nums = sorted({int(x) for x in re.findall(pat, body)})
        miss = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []
        if miss:
            out.append(sev('R-14/编号连续', SEV_WARN,
                           '%s号不连续：缺 %s（现用 %s）'
                           % (label, ','.join('%s%d' % (label, m) for m in miss),
                              ','.join(str(n) for n in nums[:12]))))
    # 公式号：形如 式 (8-3) —— 按"章-序"分子表检查连续性
    per = {}
    # ★ 式号既可能以正文引用形式出现（"式 (5-3)"），也可能只在公式块内以编号出现（`\tag{5-3}`）；
    #   原实现只收前者，致"用 \tag 编号但不逐式回引"的章节恒报"式号不连续"
    #   （见成文轮临时登记表 R7-05）。
    tags = (re.findall(r'式\s*\((\d+)\s*[-–]\s*(\d+)\)', text)
            + re.findall(r'\\tag\{(\d+)\s*[-–]\s*(\d+)\}', text))
    for ch, idx in tags:
        per.setdefault(int(ch), set()).add(int(idx))
    # ★ 只检查**本章自有**的式号分组（与图号同规则，见 R5-01）：附录与其他章节常**引用他章式号**
    #   （如附录按"对应论文位置"列 `式 (5-9)`），引用方不承担该组的连续性义务；
    #   不设该守卫则引用他章式号的模块恒报"式号不连续"（见成文轮临时登记表 R14-01）。
    own = OWN_CH.get(name[:4])
    for ch, idxs in sorted(per.items()):
        if own != ch:
            continue                          # 他章式号／本模块不定义式号：只引用 ⟹ 不查连续性
        miss = [n for n in range(1, max(idxs) + 1) if n not in idxs]
        if miss:
            out.append(sev('R-14/编号连续', SEV_WARN,
                           '式(%d-?) 编号不连续：缺 %s' % (ch, ','.join(map(str, miss)))))
    return out


def r_figexplain(text, name, ctx):
    """R-15：正文出现的**图号**（论文内索引号 `图8-1` 或 `图NN`）之后 3 行内须有解释句。

    每个图号**只检首次出现**（避免同图多次引用重复报警）。
    """
    lines = text.splitlines()
    out, seen = [], set()
    for i, ln in enumerate(lines):
        if _skip(ln) or ln.lstrip().startswith('#') or ln.lstrip().startswith('|'):
            # ★ **表格行不参与解释句检查**：图注＋解释句义务针对**叙述性正文**；
            #   每节末的「占位清单」表逐行列出图号（含 PDF 索引号），属台账而非引用，
            #   不跳过则每个图号都会恒报"未见解释句"（见成文轮临时登记表 R7-02）。
            continue
        for tok in (FIGNUM.findall(ln) + APPXFIG.findall(ln)):
            tok = tok.replace(' ', '')
            if tok in seen:
                continue
            seen.add(tok)
            # ★ 观察窗取"本行 ＋ 后 5 行"：学术论文的**标准排布**是
            #   「引用句 →（空行）→ 图注 →（空行）→ 从图 X 可见…」，
            #   解释句天然落在引用行之后第 4 行；原 3 行窗口会把这种排布误判为"未见解释句"
            #   （见成文轮临时登记表 R7-03）。
            tail = '\n'.join(lines[i:i + 6])
            if not any(t in tail for t in EXPLAIN):
                out.append(sev('R-15/图表解释', SEV_WARN,
                               '图%s 之后未见"这意味着/表明/说明"式解释句（L%d）' % (tok, i + 1), i + 1))
    return out


def _is_hypo_doc(text, name):
    return '假设' in name or re.search(r'^#{1,3}\s*.*模型假设', text, re.M)


def r_hypo3(text, name, ctx):
    """R-16：假设条目须含合理性依据词（内容＋依据＋适用范围）。"""
    if not _is_hypo_doc(text, name):
        return []
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln):
            continue
        if not re.match(r'^\s*(?:[-*]\s*)?(?:\|\s*)?\**\s*H\d{1,2}\b', ln):
            continue
        if not any(t in ln for t in EVID_TOK):
            out.append(sev('R-16/假设三要素', SEV_WARN,
                           '假设条目未见"依据/根据/文献/实测"等合理性依据词（L%d）' % i, i))
    if not any(t in text for t in RANGE_TOK):
        out.append(sev('R-16/假设三要素', SEV_WARN, '全篇未见"适用范围／前提"类限定语 ⟹ 每条须给适用范围'))
    return out


def r_shortcut(text, name, ctx):
    """R-17：禁推导跳步短语（方法学 §2.6："禁'化简得／经过计算可得'"）。"""
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln) or ln.lstrip().startswith('#'):
            continue
        for w in SHORTCUT:
            if w in ln:
                out.append(sev('R-17/推导跳步', SEV_ERR,
                               '出现跳步短语 `%s` ⟹ 须补出推导步骤（L%d）' % (w, i), i))
    return out


def r_offtable_sym(text, name, ctx):
    """R-18：正文数学符号须在《A_符号表》内（表外符号 = 全文符号不统一）。"""
    ref = ctx.get('symbols')
    if not ref:
        return [sev('R-18/表外符号', SEV_INFO, '未加载《A_符号表》，符号比对跳过')]
    out, seen = [], set()
    body = re.sub(r'^\|.*$', '', text, flags=re.M)          # 表格内的符号不查（假设／口径文档）
    for m in re.finditer(r'\$([^$\n]{1,40})\$', body):
        raw = m.group(1)
        if re.fullmatch(r'[\d\s.,%+\-=()]*', raw):
            continue
        if len(raw) > 20:
            continue
        if len(_normalize_sym(raw)) < 1 or _normalize_sym(raw)[0].isdigit():
            continue
        if _normalize_sym(raw) in ref:
            continue
        if raw in seen:
            continue
        seen.add(raw)
        out.append(sev('R-18/表外符号', SEV_WARN,
                       '符号 `$%s$` 未见于《A_符号表》⟹ 须补表或改用表内符号' % raw))
        if len(out) >= 8:
            break
    return out


def r_keyword(text, name, ctx):
    """R-19：摘要须含"关键词"行（**存在性为门禁**）；个数 **＝5** 属**暂定**（→ C-02），**不构成门禁**。"""
    if not _is_abstract(text, name):
        return []
    m = re.search(r'^.*关键词\s*[:：]\s*(.+)$', text, re.M)
    if not m:
        return [sev('R-19/关键词', SEV_ERR, '摘要未见"关键词：…"行')]
    items = [x for x in re.split(r'[;；]', m.group(1)) if x.strip()]
    if not items:
        return [sev('R-19/关键词', SEV_ERR, '"关键词"行为空')]
    if len(items) != 5:
        return [sev('R-19/关键词', SEV_WARN, '关键词 %d 个 ⟹ 应为 **5 个**（源存在分歧，已人工裁定 → C-02）' % len(items))]
    return []


def r_no_toc(text, name, ctx):
    """R-20：正文不得设"目录"（一键式提示词：无目录）。"""
    for i, ln in enumerate(text.splitlines(), 1):
        if _skip(ln):
            continue
        if re.match(r'^\s*#{1,4}\s*(目录|目\s*录)\s*$', ln):
            return [sev('R-20/禁目录', SEV_ERR, '正文出现"目录"标题 ⟹ 国赛论文不设目录（L%d）' % i, i)]
    return []


def r_eval_pair(text, name, ctx):
    """R-21：模型评价须优点／不足齐备（缺点须配改进方向）。"""
    if not ('评价' in name or re.search(r'^#{1,3}\s*.*模型评价', text, re.M)):
        return []
    out = []
    if not re.search(r'优点|优势|长处', text):
        out.append(sev('R-21/评价优缺点', SEV_WARN, '模型评价未见"优点/优势"条目'))
    if not re.search(r'不足|缺点|局限|适用范围', text):
        out.append(sev('R-21/评价优缺点', SEV_WARN, '模型评价未见"不足/缺点/局限"条目 ⟹ 缺点须诚实并配改进方向'))
    return out


def r_ai_declare(text, name, ctx):
    """R-25：整包须有「AI 工具使用声明」模块，且位置在「参考文献」之前（**官方强制**）。

    判据：官方《人工智能工具使用规定》第 3 条（"参赛队应在论文**参考文献之前**设置
    'AI 工具使用声明'"）＋ 模块 12（见 `A_判据源冲突记录表.md` **C-17**）。
    **目录级**检查只在「章节稿目录中字典序最小的 `A_*.md`」上报一次；**尚未开写时不报**。
    """
    out = []
    root = ctx.get('root')
    if not root:
        return out
    cdir = os.path.join(root, '50_论文', '02_章节稿', '基线')
    if not (os.path.isdir(cdir) and any(f.startswith('A_') for f in os.listdir(cdir))):
        cdir = os.path.join(root, '50_论文', '02_章节稿')
    if not os.path.isdir(cdir):
        return out
    files = sorted(f for f in os.listdir(cdir)
                   if f.startswith('A_') and f.endswith('.md'))
    if not files:
        return out                                  # 尚未开写 ⟹ 不报
    if os.path.basename(name.replace('\\', '/')) != files[0]:
        return out                                  # 目录级：只报一次

    def modnum(fn):
        m = re.match(r'A_(\d+)', fn)
        return int(m.group(1)) if m else 99

    ai = [f for f in files if 'AI' in f or '声明' in f]
    ref = [f for f in files if '参考' in f or '文献' in f]
    if not ai:
        out.append(sev('R-25/AI声明', SEV_ERR,
                       '整包未见「AI 工具使用声明」模块（模块 12，**官方强制**）'
                       '⟹ 须置于「参考文献」之前'))
        return out
    if ref and modnum(ai[0]) > modnum(ref[0]):
        out.append(sev('R-25/AI声明', SEV_ERR,
                       '「AI 工具使用声明」（%s）排在「参考文献」（%s）**之后** '
                       '⟹ 官方要求：参考文献**之前**' % (ai[0], ref[0])))
    body = ''
    for f in ai:
        try:
            body += open(os.path.join(cdir, f), encoding='utf-8', errors='ignore').read()
        except OSError:
            pass
    if not re.search(r'未使用|使用了|本参赛队', body):
        out.append(sev('R-25/AI声明', SEV_ERR,
                       '「AI 工具使用声明」内容为空或非官方二择一句式'
                       '（"本参赛队未使用AI工具"／"…使用了AI工具…"）'))
    # ★ **R-5 反向（整包级）**：题录表 §三 的**每条**都须在正文（基线或成文，参考文献模块除外）
    #   出现过上标 —— 内容库明令"**列而不引者删**"；原实现只查"上标→题录表"单向
    #   （见成文轮临时登记表 R13-01）。
    tb = os.path.join(root, '20_交付包', '07_引用与术语', 'A_题录表.md')
    if os.path.isfile(tb):
        try:
            tbtxt = open(tb, encoding='utf-8', errors='ignore').read()
        except OSError:
            tbtxt = ''
        sec3 = tbtxt.split('## 三')[1].split('\n## ')[0] if '## 三' in tbtxt else ''
        ids = {int(x) for x in re.findall(r'^\|\s*\*{0,2}\[(\d{1,2})\]\*{0,2}\s*\|', sec3, re.M)}
        cited = set()
        for d2 in ('基线', '成文'):
            dd = os.path.join(root, '50_论文', '02_章节稿', d2)
            if not os.path.isdir(dd):
                continue
            for f2 in os.listdir(dd):
                if not (f2.startswith('A_') and f2.endswith('.md')):
                    continue
                if '参考' in f2 or '文献' in f2:
                    continue                      # 参考文献列表自身不算"正文引用"
                try:
                    cited |= {int(x) for x in re.findall(
                        r'\[(\d{1,2})\]', open(os.path.join(dd, f2), encoding='utf-8',
                                               errors='ignore').read())}
                except OSError:
                    continue
        notcite = sorted(i for i in ids if i not in cited)
        if notcite:
            out.append(sev('R-5/W-24', SEV_WARN,
                           '题录表 §三 有 %d 条**未见正文上标**（列而不引）：[%s]'
                           % (len(notcite), ','.join(str(i) for i in notcite))))
    return out


def r_index_gate(text, name, ctx):
    """R-22/R-23/R-24：`03_对照与索引/` 的"防第二权威"门禁 ＋ 指针有效性。

    详见 `50_论文/03_对照与索引/README.md`：本目录只准放"指针表"或"派生视图"。
    """
    out = []
    rel = name.replace('\\', '/')
    if '03_对照与索引' in rel:
        if not re.search(r'\[指针表|\[自动生成', text[:1200]):
            out.append(sev('R-23/索引形态', SEV_WARN,
                           '本目录文件文首须声明形态：`[指针表]` 或 `[自动生成 · 勿手改]`'))
        data, blk = 0, []
        for ln in text.splitlines():
            if ln.startswith('|'):
                blk.append(ln)
            else:
                if len(blk) >= 2:
                    data += len(blk) - 2          # 减去表头与分隔行
                blk = []
        if len(blk) >= 2:
            data += len(blk) - 2
        if data >= 20 and not re.search(r'\[自动生成', text[:1200]):
            # ★ R-22 豁免：文首声明 `[自动生成 · 勿手改]` 的「乙·派生视图」由 build_indexes.py 生成，
            #   权威侧一改、重跑即同步 ⟹ 不构成第二权威 ⟹ 不受 <20 行限制。
            out.append(sev('R-22/禁复述权威', SEV_WARN,
                           '表格数据行 %d ≥ 20 ⟹ 疑在复述权威表；应改为"指针表"或交 `build_indexes.py` 生成' % data))
    root = ctx.get('root')
    if root:
        seen = set()
        for m in re.finditer(r'`((?:20_交付包|30_图表|50_论文)/[^`\n]+?\.(?:md|csv|py))`', text):
            relp = m.group(1)
            if relp in seen or any(c in relp for c in '*<>…'):
                continue
            seen.add(relp)
            if not os.path.exists(os.path.join(root, relp.replace('/', os.sep))):
                out.append(sev('R-24/指针有效', SEV_WARN, '指针失效（目标不存在）：`%s`' % relp))
    return out


RULES = [(r_code, '内部代号'), (r_number, '数字回指'), (r_figref, '图表引用'),
         (r_abstract, '摘要'), (r_refs, '文献对应'), (r_banned, '禁用词'),
         (r_style, '风格密度'), (r_table, '表格完整性'), (r_whitelist, '编号白名单'),
         (r_domain, '领域口径'), (r_dod, 'DoD 元信息头'),
         (r_numbering, '编号连续性'), (r_figexplain, '图表解释句'),
         (r_hypo3, '假设三要素'), (r_shortcut, '推导跳步'),
         (r_offtable_sym, '表外符号'),          (r_keyword, '关键词行'),
         (r_no_toc, '禁目录'), (r_eval_pair, '评价优缺点'),
         (r_ai_declare, 'AI 声明存在性'), (r_index_gate, '对照与索引门禁')]

# 模式：draft = 章节稿全规则；doc = 「文档体检」只查结构类（数字溯源 ＋ 表格完整性）
# 说明：约束／口径类文档**本身就列举禁用词与内部代号作为反例**，用 draft 模式会产生大量预期内假阳性。
RULES_DOC = [(r_number, '数字回指'), (r_table, '表格完整性')]
MODE_RULES = {'draft': RULES, 'doc': RULES_DOC}


# ----------------------------------------------------------------------------- 上下文
def find_root(start):
    p = start
    for _ in range(8):
        if os.path.isdir(os.path.join(p, '10_赛题')):
            return p
        p = os.path.dirname(p)
    return os.getcwd()


def build_ctx(root):
    ctx = {'numbers': set(), 'refnums': set(), 'symbols': set(), 'root': root}
    p = os.path.join(root, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['numbers'] = set(DEC_PAT.findall(t))
        # ★ 呈现等价：口径表登记的是全精度值（如 1.766193），论文按呈现口径写 4 位（1.7662）
        #   ⟹ 把每个登记值的 4 位呈现形式一并纳入参照集（否则 R-2 会对**合法的呈现值**报假阳性）
        _extra = set()
        for _x in list(ctx['numbers']):
            try:
                _f = float(_x)
            except ValueError:
                continue
            _extra.add('%.4f' % _f)
            _extra.add(('%.4f' % _f).rstrip('0').rstrip('.'))
            _extra.add('%g' % _f)
        ctx['numbers'] |= _extra
    p = os.path.join(root, '20_交付包', '07_引用与术语', 'A_题录表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['refnums'] = {str(i) for i in range(1, 19)} if ('§三' in t or '题录' in t) else set()
    p = os.path.join(root, '20_交付包', '02_符号表', 'A_符号表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['symbols'] = {_normalize_sym(x) for x in re.findall(r'\$([^$\n]{1,40})\$', t)}
        ctx['symbols'] |= {_normalize_sym(x) for x in re.findall(r'\\\(([^()\n]{1,40})\\\)', t)}
    return ctx


def lint_text(text, name, ctx, rules=None):
    out = []
    for fn, _ in (rules or RULES):
        out += fn(text, name, ctx)
    return sorted(out, key=lambda x: (SEV_ORDER[x['sev']], x['line'] or 0))


# ----------------------------------------------------------------------------- 自检
CLEAN = """# A_01_摘要

> **论文模块**：第 2 模块 · 摘要
> **素材来源**：`20_交付包/10_摘要与结论要点/摘要要点卡.md`
> **真值核对**：已与《A_数值口径总表》§八逐项对表
> **术语核对**：已按 §五 统一定名比对
> **占位清单**：本节无图
> **自查**：见文末

本文针对圆柱形药材热风烘干问题，考虑变物性与尺寸收缩等约束，构建热湿耦合模型。
针对问题一，采用元体平衡与全隐式格式求解，中心温度 33.5753 ℃、表面 36.7855 ℃；中心含水率 2.5500 kg/kg。干基含水率随半径递减。
针对问题二，采用交替推进格式，中心温度 49.8495 ℃、表面 49.9664 ℃；中心含水率 1.7662 kg/kg、表面 1.0081 kg/kg。
针对问题三，以事件驱动定位达标时刻 57.5314 h；针对问题四，收缩域求解得 50.6523 h、最高温度 54.63 ℃。
综上，本文通过界面系数积分平均、时间方向精确推进与事件驱动二分三项改进，提高了结果可靠性。
关键词：热湿耦合；有限体积；干燥；灵敏度分析；改进格式

（下略）
"""

BROKEN = {
    'code': '本问检验编号 E3 与台账 D-24、口径 M6 一并说明。',
    'num': '结果显示中心温度为 99.9999 ℃。',
    'banned': '本文的创新点在于提出完美方案。',
    'table': '| a | b |\n|---|---|\n| $\\max|\\Delta T|$ | 1.0 |\n| x | y | z |\n',
    'abs': '摘要\n针对问题一，结果较好。因为所以，1. 第一点。\n',
    'dod': '# 某节\n正文若干。\n',
}


def selftest():
    ctx = {'numbers': set(), 'refnums': {str(i) for i in range(1, 19)}}
    ok = True
    clean = lint_text(CLEAN, 'A_01_摘要.md', ctx)
    errs = [x for x in clean if x['sev'] == SEV_ERR]
    print('== 自检 ==')
    print('[1] 干净样例：%d 条发现（❌ %d）' % (len(clean), len(errs)))
    for x in clean:
        print('     %s %s %s' % (x['sev'], x['id'], x['msg'][:70]))
    if errs:
        ok = False
        print('     ⟹ 期望无 ❌，实际有 ⟹ 自检失败')
    expect = {'code': 'R-1/W-07', 'num': 'R-2/W-01', 'banned': 'R-6/W-20',
              'table': 'R-8', 'abs': 'R-4/W-17', 'dod': 'R-11/DoD'}
    for k, want in expect.items():
        got = lint_text(BROKEN[k], 'A_09_测试.md', ctx)
        hit = [x for x in got if x['id'] == want]
        print('[2] 破损样例 %-7s ⟹ 期望命中 %-10s %s' % (k, want, '✅' if hit else '❌ 未命中'))
        if not hit:
            ok = False
    print('[3] 表格样例发现明细：')
    for x in lint_text(BROKEN['table'], 'A_09_测试.md', ctx):
        if x['id'] == 'R-8':
            print('     %s %s' % (x['sev'], x['msg'][:80]))
    # [4] 外部判据硬门禁（R-14…R-21）逐条样例
    EXTRA = [
        # ★ 图号口径＝横向基线 §六「按章号」（A_08＝第五章 ⟹ 图5-x）；原样例用旧「模块号制」图8-x，
        #   与现行口径不符（且会与 R-14 新增的"只查本章自有图号分组"冲突），见成文轮临时登记表 R6-02
        ('num2', 'A_08_模型建立与求解.md', '如图5-1所示，温度场表明表面先热。\n如图5-3所示，曲线。\n', 'R-14/编号连续'),
        ('figexplain', 'A_08_模型建立与求解.md', '本节给出温度场结果。\n\n（图8-1）\n\n（下略）\n', 'R-15/图表解释'),
        ('hypo', 'A_06_模型假设.md', '# A_06_模型假设\n\n- **H1** 一维轴对称，温度均匀。\n', 'R-16/假设三要素'),
        ('shortcut', 'A_08_模型建立与求解.md', '由上式化简得 $T=1$。\n', 'R-17/推导跳步'),
        ('toc', 'A_01_摘要.md', '# 目录\n', 'R-20/禁目录'),
        ('eval', 'A_10_模型评价.md', '## 模型评价\n\n本文模型具有明显优点。\n', 'R-21/评价优缺点'),
        ('kw', 'A_01_摘要.md', '# A_01_摘要\n\n针对问题一，中心温度 33.5753 ℃。\n', 'R-19/关键词'),
    ]
    for k, fn, tx, want in EXTRA:
        hit = [x for x in lint_text(tx, fn, ctx) if x['id'] == want]
        print('[4] 硬门禁样例 %-11s ⟹ 期望命中 %-14s %s' % (k, want, '✅' if hit else '❌ 未命中'))
        if not hit:
            ok = False
    print('== 自检结论：%s ==' % ('通过' if ok else '失败'))
    return 0 if ok else 1


# ----------------------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=None)
    ap.add_argument('--dir', default=None)
    ap.add_argument('--file', default=None)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--mode', choices=['draft', 'doc'], default='draft',
                    help='draft=章节稿全规则（默认）；doc=文档体检（仅数字溯源＋表格完整性）')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    rules = MODE_RULES[a.mode]
    root = a.root or find_root(os.path.dirname(os.path.abspath(__file__)))
    ctx = build_ctx(root)
    _b = os.path.join(root, '50_论文', '02_章节稿', '基线')
    _auto = _b if (os.path.isdir(_b) and any(f.startswith('A_') and f.endswith('.md')
                                            for f in os.listdir(_b))) else os.path.join(root, '50_论文', '02_章节稿')
    d = a.dir or _auto
    if not os.path.isabs(d):
        d = os.path.join(root, d)
    files = [a.file] if a.file else sorted(
        p for p in glob.glob(os.path.join(d, '*.md')) if not os.path.basename(p).startswith('00_'))
    if not files:
        print('未发现章节稿（目录：%s）⟹ 门禁待用；可先跑 --selftest 验证规则。' % d)
        print('已加载参照：口径表数值 %d 个 ｜ 题录编号 %d 个 ｜ 本模式规则 %d 组'
              % (len(ctx['numbers']), len(ctx['refnums']), len(rules)))
        return 0
    allf, nerr = [], 0
    for p in files:
        t = io.open(p, encoding='utf-8', errors='replace').read()
        f = lint_text(t, os.path.relpath(p, root).replace('\\', '/'), ctx, rules)
        nerr += sum(1 for x in f if x['sev'] == SEV_ERR)
        allf.append((os.path.relpath(p, root), f))
    if a.json:
        print(json.dumps({'files': [{'file': r, 'findings': f} for r, f in allf]},
                         ensure_ascii=False, indent=1))
        return 1 if nerr else 0
    tot = 0
    for rel, f in allf:
        print('=' * 84)
        print('%s  ⟹ %d 条（❌ %d）' % (rel, len(f), sum(1 for x in f if x['sev'] == SEV_ERR)))
        for x in f:
            tot += 1
            print('  %s [%s] L%s %s' % (x['sev'], x['id'], x['line'] or '-', x['msg']))
    # R-13 ★ 章节完整性（目录级）：14 模块覆盖度
    if a.mode == 'draft' and not a.file:
        mods = {}
        for p in files:
            m = re.match(r'A_(\d{2})_', os.path.basename(p))
            if m:
                mods[int(m.group(1))] = os.path.basename(p)
        miss13 = [n for n in range(1, 15) if n not in mods]
        print('=' * 84)
        if miss13:
            tot += 1
            print('  ⚠️ [R-13/章节完整] 14 模块尚缺 %d 个：%s'
                  % (len(miss13), '、'.join('模块%d' % n for n in miss13)))
        else:
            print('  ✅ [R-13/章节完整] 14 模块齐备（%d 份章节稿）' % len(mods))
    print('=' * 84)
    print('合计 %d 条发现 ｜ ❌ %d ⟹ %s' % (tot, nerr, '不通过（须返工）' if nerr else '通过'))
    return 1 if nerr else 0


if __name__ == '__main__':
    sys.exit(main())
