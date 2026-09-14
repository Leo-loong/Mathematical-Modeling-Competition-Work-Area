# -*- coding: utf-8 -*-
"""成绩评定指标库（登记 / 判定 / 复算骨架 · 本轮不执行正式评分）

定位：
  把《A_成绩评定方法学总纲》与《A_成绩评定执行计划》中的**评分依据与口径**固化为机读结构，
  供后续"专家评估"阶段调用。本文件**只做三件事**：
    ① 登记（体系／维度／阈值／致命项／契约／缺口口径）；
    ② 结构自检（`--selftest`：登记表内部一致性 + 口径算例校验）；
    ③ 纯函数骨架（折算区间／档位判定／双轨差异／覆盖率披露／改进优先级）。
  **不读任何数据、不产出任何分数**——正式评分需显式 `--go`，且必须满足《执行计划》的前置门禁。

口径来源：`01_评分依据与来源台账.md`（kb 路径:行号逐条登记）＋《执行计划》§六／§七。
纪律：
  - 只读：本模块不写工作区任何文件（除 stdout / 显式 --out）；
  - kb 依据仅作内部论证，不得进论文／交付包／支撑材料。

用法：
  python grade_lib.py --selftest     # 登记表 + 口径算例自检（默认）
  python grade_lib.py --dump         # 打印登记表
  python grade_lib.py --go           # 正式评分（本骨架阶段**拒绝执行**，提示授权流程）
"""
from __future__ import annotations

import argparse
import math
import sys

# ============================================================ 一、体系登记（S1–S9）
SYSTEMS = [
    dict(code='S1', name='官方四大评分标准', kind='score', total=100,
         parts=['假设的合理性:15', '建模的创造性:25', '结果的正确性:25', '文字表述的清晰性:35'],
         src='第一批提取后/老哥讲义！2026数学建模国赛冲奖要点全解析！.md:555-617'),
    dict(code='S2', name='16维度自查（标准版）', kind='checklist', total=115,
         levels=['合格', '存在问题', '严重问题'],
         overall=['合格', '基本合格', '不合格'],
         src='AI提示词合集/02_检测自查与优化/数学建模论文全维度自查与获奖预测提示词！（标准版）.md'),
    dict(code='S3', name='16维度自查（国奖级进阶版）', kind='checklist', total=146,
         levels=['国奖级', '合格', '存在问题', '严重问题'],
         overall=['国奖潜力', '省一水平', '需提升', '不合格'],
         src='AI提示词合集/02_检测自查与优化/AI论文检查与获奖预测！…（进阶版）.md'),
    dict(code='S4', name='AI全自动自查表', kind='checklist', total=26,
         groups=['AI新规合规:4', 'AI幻觉与数据真实性:4', '建模逻辑与题意适配:5',
                 '模型求解及结果合理性:3', '官方写作规范:6', '官方排版及页数:4'],
         src='AI提示词合集/02_检测自查与优化/2026数学建模国赛AI全自动自查表（标准版）.md'),
    dict(code='S5', name='章节权重解析', kind='weight', total=None,
         parts=['摘要:20-25%', '问题分析:5-10%', '假设:5-10%', '模型建立:20-30%',
                '模型求解:15-20%', '结果分析:10-15%', '误差灵敏度稳健性:5-10%',
                '评价与推广:3-5%', '论文规范:3-5%'],
         src='教材_转化/15_赛前规划与全真模拟复盘.md:399'),
    dict(code='S6', name='九维度评分表', kind='score', total=45,
         parts=['摘要:5', '问题分析:5', '模型假设:5', '模型建立:5', '模型求解:5',
                '结果分析:5', '误差灵敏度稳健性:5', '排版规范:5', '整体逻辑:5'],
         src='教材_转化/15_赛前规划与全真模拟复盘.md:414-428'),
    dict(code='S7', name='评委视角五标准', kind='score', total=25,
         parts=['逻辑自洽:5', '术语准确:5', '数据支撑:5', 'AI痕迹:5', '学术规范:5'],
         src='教材_转化/11_AI论文写作与模型优化.md:74-84,96-97'),
    dict(code='S8', name='模型适配性检查', kind='checklist', total=15,
         levels=['合适', '可改进', '不合适'],
         src='AI提示词合集/02_检测自查与优化/数学建模论文AI模型适配性检查提示词！（已修改）.md'),
    dict(code='S9', name='60个核心获奖要点', kind='checklist', total=60,
         src='第一批提取后/2026数学建模国赛60个核心获奖要点！.md:22-57'),
]

# ============================================================ 二、16 维度（S3 §8.3）
# count = 基准检查点数；core = 四大核心维度；scope: deliverable=可完整判定 /
# writer=只判素材齐备性（◻） / mixed=主体可判但成品呈现属写作侧。
# level: P=仅全题层 / Q=仅分问层 / B=两层都有（B 类先逐问判、全题取最差态）。
DIM16 = [
    dict(no=1,  name='论文摘要与整体结构', count=12, star=5, core=True,  scope='writer',      level='P'),
    dict(no=2,  name='问题分析与重述',     count=8,  star=3, core=False, scope='deliverable', level='B'),
    dict(no=3,  name='模型假设与符号说明', count=10, star=3, core=False, scope='deliverable', level='B'),
    dict(no=4,  name='模型建立',           count=15, star=5, core=True,  scope='deliverable', level='B'),
    dict(no=5,  name='算法选择与模型求解', count=10, star=3, core=False, scope='deliverable', level='Q'),
    dict(no=6,  name='结果分析与数据可视化', count=10, star=4, core=False, scope='mixed',      level='B'),
    dict(no=7,  name='模型检验与灵敏度分析', count=12, star=5, core=True,  scope='deliverable', level='B'),
    dict(no=8,  name='模型评价与优缺点分析', count=8,  star=3, core=False, scope='deliverable', level='P'),
    dict(no=9,  name='创新点打造与差异化',   count=10, star=5, core=True,  scope='deliverable', level='Q'),
    dict(no=10, name='数据预处理与特征工程', count=8,  star=3, core=False, scope='deliverable', level='B'),
    dict(no=11, name='参考文献引用规范',     count=6,  star=3, core=False, scope='deliverable', level='P'),
    dict(no=12, name='附录与代码可复现性',   count=8,  star=3, core=False, scope='deliverable', level='P'),
    dict(no=13, name='论文格式与排版规范',   count=10, star=4, core=False, scope='writer',      level='P'),
    dict(no=14, name='选题策略与赛题理解',   count=5,  star=3, core=False, scope='deliverable', level='P'),
    dict(no=15, name='论文合规与原创性检测', count=6,  star=4, core=False, scope='deliverable', level='P'),
    dict(no=16, name='整体印象与获奖潜力',   count=8,  star=3, core=False, scope='deliverable', level='P'),
]

# ============================================================ 三、量化阈值（台账 §二）
THRESHOLDS = {
    '摘要字数_标准版': (800, 1000, '字'),
    '摘要字数_国奖级': (800, 1200, '字'),
    '摘要字数_致命下限': (600, None, '字'),
    '关键词数': (3, 5, '个'),
    '假设条数_通用': (3, 5, '条'),
    '假设条数_A题国奖级': (8, 15, '条'),
    '正文页数_合规': (20, 32, '页'),
    '正文页数_最优': (25, 30, '页'),
    '正文页数_硬上限': (None, 30, '页'),
    '检验方法数_下限': (3, None, '种'),
}

# ============================================================ 四、致命项（一票否决）
FATAL = [
    dict(no=1, name='摘要严重不合格',
         rule='摘要 <600 字 或超一页，或无具体数值，或结构混乱无分问描述',
         preset='未触发（素材侧数值齐全；成稿字数属写作侧，须交付前复查）'),
    dict(no=2, name='（整体）模型创新性极低/完全无创新',
         rule='直接套用现成模型、无算法改进、无问题特化策略',
         preset='未触发（四问创新项共 28 项）'),
    dict(no=3, name='排版混乱/图表粗糙/字体不统一/大量空白页',
         rule='交付侧看规格卡与设计语言是否齐备；成品侧由写作者定',
         preset='未触发（素材侧齐备）；成品侧待写作'),
    dict(no=4, name='全文无任何模型检验',
         rule='误差／灵敏度／稳健性／对比验证 同时全缺',
         preset='未触发（本项目最强项）'),
]

# ============================================================ 五、判定态与契约
# 判定态（4 级 + 2 特态）；键＝明细表 CSV 的"判定"列取值；⬜ 不计分母，◻ 不计我方得分
JUDGEMENTS = {
    '🏆': dict(name='国奖级',   ordinal=0,    counts=True,  note='达到国奖级标准'),
    '✅': dict(name='合格',     ordinal=1,    counts=True,  note='符合国赛基本要求'),
    '⚠️': dict(name='存在问题', ordinal=2,    counts=True,  note='可改，影响档次'),
    '❌': dict(name='严重问题', ordinal=3,    counts=True,  note='硬伤，直接影响获奖'),
    '⬜': dict(name='待取证',   ordinal=None, counts=False, note='无五类证据之一，不计入分母'),
    '◻': dict(name='写作侧',   ordinal=None, counts=False, note='写作侧/外部依赖，不计我方得分'),
    '∅': dict(name='不适用',   ordinal=None, counts=False, note='该检查点对本题不适用（既不计得分也不计问题）'),
}

# 双轨差异定级（序数刻度差）
TRACK_DIFF = {0: '同判-采纳', 1: '半档-对账取保守', 2: '跨档-必回询'}

# D2 明细表列契约（CSV，UTF-8-sig）
CSV_SCHEMA = ['层级', '问', '维度号', '维度', '检查点号', '检查点',
              '判定', '证据类型', '证据指针', '扣分下限', '扣分上限', '备注']

# 五类证据
EVIDENCE_TYPES = {
    'E-A': '数值真值（《A_数值口径总表》）',
    'E-B': '结果文件（results/result*.xlsx）',
    'E-C': '图数据（04_图表包/data/*.csv ＋ 规格卡 ＋ 总规划）',
    'E-D': '代码与日志（Q*/code/*.py ＋ logs/*）',
    'E-E': '文档条文（20_交付包/…）',
}

# ============================================================ 六、计分口径
# L3 折算规则参数（方法学总纲 §5.1；执行阶段可调，但须在报告中声明并经"校准"）
FOLD = dict(champion_ratio=(0.00, 0.00),  # 🏆 国奖级：不扣
            pass_ratio=(0.01, 0.02),      # ✅ 合格：扣 [1%, 2%]·M（国奖级视角下的余地）
            warn_ratio=(0.05, 0.10),      # ⚠️ 存在问题：扣 [5%, 10%]·M
            severe_ratio=(0.18, 0.25),    # ❌ 严重问题：扣 [18%, 25%]·M
            unknown_upper=0.08)           # ⬜/◻ 仅抬高上界 8%·M/项

# 四大核心维度放大系数（方法学总纲 §7.2）
KAPPA = dict(core=1.5, fatal_related=2.0, normal=1.0)

# S3 档位判定矩阵（阈值；判定须同时满足；按从严顺序排列）
GRADE_RULES = [
    dict(grade='不合格',   severe_gt=5, core_severe_ge=3, fatal=True,
         pred='可能未获奖', note='须注明触发的致命项'),
    dict(grade='需提升',   severe_le=5, core_severe=2,
         pred='省二/省三', note='有明显短板，需针对性修改'),
    dict(grade='省一水平', severe_le=2, warn_le=25, core_severe=0,
         pred='省一潜力，修改后有望冲国二', note='省奖 ≈前 25%'),
    dict(grade='国奖潜力', severe_le=0, warn_le=15, champion_ge=30, core_severe=0,
         pred='国一/国二潜力（不写"水平"）', note='国奖 ≈3%（国一 ≈0.5%、国二 ≈1.5%）'),
]

# S6 九维度 → 本项目 16 维映射
S6_TO_DIM16 = {
    '摘要': [1],
    '问题分析': [2],
    '模型假设': [3],
    '模型建立': [4],
    '模型求解': [5],
    '结果分析': [6],
    '误差灵敏度稳健性': [7],
    '排版规范': [13],
    '整体逻辑': [2, 4, 8, 16],
}

# S5 权重配平的离散度判据
S5_DISPERSION_MAX = 0.25

# S7 固定抽样位（防挑样本）
S7_SAMPLING = ['10_摘要与结论要点/摘要要点卡.md',
               '01_模型叙述/A_Q2模型叙述.md 或 A_Q3模型叙述.md',
               '01_模型叙述/A_Q*结果与分析.md（任一）',
               '06_可靠性与方法学/A_Q*.md（任一）']

# 写作侧"素材齐备性"判据表（◻；不计我方得分）
WRITER_READINESS = {
    '摘要素材': ['四要素齐备（问题→方法→结果→结论）',
                 '每问 ≥1-2 个对比性数字',
                 '关键词 3-5 个（模型/方法＋领域＋关键技术）',
                 '分问段落结构建议已给出',
                 '字数目标已标注（800-1000 / 800-1200）',
                 '创新点已给"编号＋效果量化"清单'],
    '成品呈现素材': ['三方一致：总规划 ↔ 规格卡 ↔ data/*.csv',
                     '规格卡含七要素 ＋ 2 新增必填（标签文本／字体与公式）',
                     '设计语言覆盖（配色／线型语义冻结／字号 ≥7 pt）',
                     '参考图已渲染或已列明"待渲染"清单'],
    '排版素材': ['字体与公式硬约束已落库（含字体嵌入）',
                 '导出要求（300 DPI PNG ＋ 矢量 PDF）已入规格卡',
                 '官方红线清单可执行（匿名／无目录／正文 ≤30 页／P3 摘要页）',
                 '三线表与图表编号规则已明确'],
}

# 已知缺口口径（《执行计划》§1.4 K-1…K-6）
KNOWN_GAPS = {
    'K-1': dict(fact='参考文献仅 2 条（数量<5、字段待补全）',
                disposition='照常计分', detail='维度十一判 ❌严重问题；原因只在"说明"中陈述'),
    'K-2': dict(fact='F-07/F-21/F-26 待对方补绘；F-04/F-05 待出卡',
                disposition='标注不计分', detail='记 ◻ 外部依赖（卡与参考图已就绪）'),
    'K-3': dict(fact='q1_e1/e3/e5 日志数值未随代码刷新（D-19/D-24 遗留）',
                disposition='标 ⬜待取证', detail='不计入分母；列入"收口完整性"缺口；重跑需 T2 授权'),
    'K-4': dict(fact='q2_solver.py 默认核 Q2_CORE 未改（D-22 遗留一行）',
                disposition='计为已登记遗留', detail='维度五/十二记一条 ⚠️；不影响交付数值'),
    'K-5': dict(fact='交付包内 14 份日志含工作区绝对路径',
                disposition='不计分', detail='属留证原文，已按规则例外③闭环'),
    'K-6': dict(fact='rerun_out/、root_temp/ 未登记（疑另一 Agent 产物）',
                disposition='不计分', detail='标"非正式区"，不作为评估对象'),
}

# 覆盖率/披露口径
UNCERTAIN_MAX_RATIO = 0.10   # ⬜ 占比上限；超过则"判定完整性不足"


# ============================================================ 七、纯函数骨架
def total_checkpoints(dims=None):
    """基准检查点总数。"""
    return sum(d['count'] for d in (dims or DIM16))


def core_dimensions(dims=None):
    return [d for d in (dims or DIM16) if d['core']]


def writer_side_dimensions(dims=None):
    return [d for d in (dims or DIM16) if d['scope'] == 'writer']


def _r1(x):
    """保留 1 位小数，**四舍五入（half-up）**——避免 Python 银行家舍入把 24.25 变成 24.2。"""
    return math.floor(x * 10.0 + 0.5 + 1e-9) / 10.0


def fold_range(m, n_champion=0, n_pass=0, n_warn=0, n_severe=0, n_unknown=0, fold=None):
    """按 FOLD 折算单条标准的分值区间 [下界, 上界]。

    规则（方法学总纲 §5.1；参数经 **Q1 先例校准**，见报告 §六 校准留痕）：
        扣分下限 = M·(0.01·n_pass + 0.05·n_warn + 0.18·n_severe)
        扣分上限 = M·(0.02·n_pass + 0.10·n_warn + 0.25·n_severe + 0.08·n_unknown)
    其中 🏆 不扣；**⬜/◻ 只抬高上界（下界不预留）**；结果截断到 [0, M]，保留 1 位小数（half-up）。
    """
    f = fold or FOLD
    lo_cut = (f['pass_ratio'][0] * n_pass + f['warn_ratio'][0] * n_warn
              + f['severe_ratio'][0] * n_severe) * m
    hi_cut = (f['pass_ratio'][1] * n_pass + f['warn_ratio'][1] * n_warn
              + f['severe_ratio'][1] * n_severe + f['unknown_upper'] * n_unknown) * m
    hi = max(0.0, m - lo_cut)          # 上界：扣得少
    lo = max(0.0, m - hi_cut)          # 下界：扣得多
    if lo > hi:                        # 防御：不得出现倒挂
        lo = hi
    return _r1(lo), _r1(hi)


def track_delta(sym_a, sym_b):
    """双轨差异的序数刻度差；参与不了比对（⬜/◻）返回 None。"""
    oa = JUDGEMENTS.get(sym_a, {}).get('ordinal')
    ob = JUDGEMENTS.get(sym_b, {}).get('ordinal')
    if oa is None or ob is None:
        return None
    return abs(oa - ob)


def track_verdict(delta):
    if delta is None:
        return '不参与比对（⬜/◻）'
    return TRACK_DIFF.get(delta, '跨档-必回询') if delta <= 2 else '跨档-必回询'


def grade_from_counts(n_severe, n_warn, n_champion, core_severe):
    """按 GRADE_RULES 判档（从严顺序）。返回 (档位, 预测, 说明)。"""
    if n_severe > 5 or core_severe >= 3:
        r = next(x for x in GRADE_RULES if x['grade'] == '不合格')
    elif n_severe <= 5 and core_severe >= 2:
        r = next(x for x in GRADE_RULES if x['grade'] == '需提升')
    elif n_severe <= 2 and n_warn <= 25 and core_severe == 0:
        if n_severe == 0 and n_warn <= 15 and n_champion >= 30:
            r = next(x for x in GRADE_RULES if x['grade'] == '国奖潜力')
        else:
            r = next(x for x in GRADE_RULES if x['grade'] == '省一水平')
    else:
        r = next(x for x in GRADE_RULES if x['grade'] == '需提升')
    return r['grade'], r['pred'], r['note']


def disclosure(rows):
    """按 §3.4 口径算覆盖率披露：分母／⬜／◻／达标率。

    rows: 可迭代的 判定符号（🏆/✅/⚠️/❌/⬜/◻/∅）。
    """
    cnt = {s: 0 for s in ('🏆', '✅', '⚠️', '❌', '⬜', '◻', '∅')}
    for r in rows:
        if r in cnt:
            cnt[r] += 1
    denom = sum(v for k, v in cnt.items() if JUDGEMENTS[k]['counts'])
    passed = cnt['🏆'] + cnt['✅']
    rate = (passed / denom) if denom else 0.0
    uncertain_ratio = (cnt['⬜'] / (denom + cnt['⬜'])) if (denom + cnt['⬜']) else 0.0
    return dict(counts=cnt, denominator=denom, passed=passed, rate=round(rate, 4),
                uncertain_ratio=round(uncertain_ratio, 4),
                uncertain_ok=(uncertain_ratio <= UNCERTAIN_MAX_RATIO))


def priority(weight, score_ratio, is_core=False, fatal_related=False):
    """改进优先级 = 权重 x (1 - 得分率) x kappa。"""
    kappa = KAPPA['fatal_related'] if fatal_related else (
        KAPPA['core'] if is_core else KAPPA['normal'])
    return weight * (1.0 - score_ratio) * kappa


def within_range(value, key):
    """阈值区间检查（None 表示该侧无界）。"""
    lo, hi, _unit = THRESHOLDS[key]
    if lo is not None and value < lo:
        return False
    if hi is not None and value > hi:
        return False
    return True


def s5_dispersion(rates):
    """S5 分布自洽性：返回 (离散度, 是否通过)。"""
    if not rates:
        return 0.0, True
    d = max(rates) - min(rates)
    return round(d, 4), d <= S5_DISPERSION_MAX


# ============================================================ 八、自检
def selftest():
    problems = []

    # 1) 维度编号连续、检查点合计 146
    nos = [d['no'] for d in DIM16]
    if nos != list(range(1, 17)):
        problems.append('DIM16 编号不连续：%r' % nos)
    if total_checkpoints() != 146:
        problems.append('DIM16 检查点合计 = %d，期望 146' % total_checkpoints())

    # 2) 四大核心维度
    cores = {d['no'] for d in core_dimensions()}
    if cores != {1, 4, 7, 9}:
        problems.append('四大核心维度异常：%r' % sorted(cores))

    # 3) 写作侧维度
    ws = {d['no'] for d in writer_side_dimensions()}
    if ws != {1, 13}:
        problems.append('写作侧维度异常：%r（期望 {1,13}）' % sorted(ws))

    # 4) level 标注合法
    bad = [d['no'] for d in DIM16 if d['level'] not in ('P', 'Q', 'B')]
    if bad:
        problems.append('DIM16 level 非法：%r' % bad)

    # 5) 致命项 4 条
    if len(FATAL) != 4:
        problems.append('致命项数量 = %d，期望 4' % len(FATAL))

    # 6) S1 / S6 / S4 分值校验
    s1 = next(s for s in SYSTEMS if s['code'] == 'S1')
    if sum(int(p.split(':')[1]) for p in s1['parts']) != 100:
        problems.append('S1 分值合计异常')
    s6 = next(s for s in SYSTEMS if s['code'] == 'S6')
    if sum(int(p.split(':')[1]) for p in s6['parts']) != 45:
        problems.append('S6 分值合计异常')
    s4 = next(s for s in SYSTEMS if s['code'] == 'S4')
    if sum(int(g.split(':')[1]) for g in s4['groups']) != 26:
        problems.append('S4 子维度合计异常')

    # 7) 判定态 ordinal 与 counts 自洽
    for k, v in JUDGEMENTS.items():
        if v['counts'] and v['ordinal'] is None:
            problems.append('判定态 %s：counts=True 但 ordinal=None' % k)
        if (not v['counts']) and v['ordinal'] is not None:
            problems.append('判定态 %s：counts=False 但 ordinal 非空' % k)

    # 8) CSV 契约列数
    if len(CSV_SCHEMA) != 12:
        problems.append('CSV_SCHEMA 列数 = %d，期望 12' % len(CSV_SCHEMA))

    # 9) S6→DIM16 映射覆盖全部 9 个 S6 维度，且目标合法
    s6_names = [p.split(':')[0] for p in s6['parts']]
    if set(s6_names) != set(S6_TO_DIM16):
        problems.append('S6_TO_DIM16 键与 S6 维度不一致：%r' % sorted(set(s6_names) ^ set(S6_TO_DIM16)))
    for k, v in S6_TO_DIM16.items():
        if not all(1 <= x <= 16 for x in v):
            problems.append('S6_TO_DIM16[%s] 目标越界：%r' % (k, v))

    # 10) 折算算例（校准后）：M=25, 5×✅ → (22.5, 23.8)
    lo, hi = fold_range(25, n_pass=5)
    if (lo, hi) != (22.5, 23.8):
        problems.append('折算算例不符：得 (%s, %s)，期望 (22.5, 23.8)' % (lo, hi))
    # 🏆 不扣
    if fold_range(25, n_champion=5) != (25.0, 25.0):
        problems.append('🏆 规则错误：不应扣分')
    # ⬜/◻ 只抬上界：增 ⬜ 不应改变上界，但应降低下界
    if fold_range(25, n_pass=5)[1] != fold_range(25, n_pass=5, n_unknown=3)[1]:
        problems.append('⬜ 规则错误：不应改变上界')
    if fold_range(25, n_pass=5, n_unknown=3)[0] >= fold_range(25, n_pass=5)[0]:
        problems.append('⬜ 规则错误：应降低下界')

    # 11) 双轨差异定级（按判定符号）
    if track_delta('✅', '✅') != 0:
        problems.append('track_delta 同判应为 0')
    if track_delta('✅', '⚠️') != 1:
        problems.append('track_delta 半档应为 1')
    if track_delta('✅', '❌') != 2:
        problems.append('track_delta 跨档应为 2')
    if track_delta('⬜', '❌') is not None:
        problems.append('track_delta 对 ⬜ 应返回 None')

    # 12) 档位判定抽样
    if grade_from_counts(0, 10, 40, 0)[0] != '国奖潜力':
        problems.append('档位判定：国奖潜力样例不符')
    if grade_from_counts(1, 20, 10, 0)[0] != '省一水平':
        problems.append('档位判定：省一水平样例不符')
    if grade_from_counts(3, 5, 5, 0)[0] != '需提升':
        problems.append('档位判定：需提升样例不符（严重>2 且核心未超）')
    if grade_from_counts(6, 0, 0, 0)[0] != '不合格':
        problems.append('档位判定：不合格样例不符')

    # 13) 覆盖率披露
    d = disclosure(['🏆'] * 30 + ['✅'] * 60 + ['⚠️'] * 50 + ['❌'] * 5 + ['⬜'] * 1 + ['∅'] * 4)
    if d['denominator'] != 145 or d['passed'] != 90 or d['counts']['∅'] != 4:
        problems.append('disclosure 分母/达标数/不适用数不符：%r' % d)
    if disclosure(['⬜'] * 20 + ['✅'] * 100)['uncertain_ok']:
        problems.append('⬜ 占比上限未生效')

    # 14) 优先级核心放大
    if not (priority(1.0, 0.5, is_core=True) > priority(1.0, 0.5)):
        problems.append('priority 核心放大系数未生效')

    # 15) 阈值与 S5 离散度
    if within_range(500, '摘要字数_致命下限'):
        problems.append('阈值判定异常：500 字应触发致命下限')
    if not s5_dispersion([0.8, 0.85, 0.9])[1]:
        problems.append('S5 离散度：0.10 应判通过')
    if s5_dispersion([0.5, 0.9])[1]:
        problems.append('S5 离散度：0.40 应判不通过')

    # 16) 已知缺口 6 条
    if len(KNOWN_GAPS) != 6:
        problems.append('KNOWN_GAPS 条数 = %d，期望 6' % len(KNOWN_GAPS))

    if problems:
        print('[SELFTEST FAIL]')
        for p in problems:
            print('  - ' + p)
        return 1
    print('[SELFTEST OK]')
    print('  体系 S1-S9：%d 套；16 维度检查点：%d；四大核心维度：%r'
          % (len(SYSTEMS), total_checkpoints(), sorted(cores)))
    print('  致命项：%d 条；写作侧维度：%r；阈值：%d 项；已知缺口：%d 条'
          % (len(FATAL), sorted(ws), len(THRESHOLDS), len(KNOWN_GAPS)))
    print('  契约：CSV %d 列；证据类型 %d 类；判定态 %d 种；S6映射 %d 项'
          % (len(CSV_SCHEMA), len(EVIDENCE_TYPES), len(JUDGEMENTS), len(S6_TO_DIM16)))
    print('  算例：M=25, 5×✅ → %r ；M=25, 5×🏆 → %r（校准：Q1 三项与先例重叠）'
          % (fold_range(25, n_pass=5), fold_range(25, n_champion=5)))
    return 0


def dump():
    print('== 体系（S1-S9）==')
    for s in SYSTEMS:
        n = s.get('total')
        print('  %-3s %-22s %-9s %s' % (s['code'], s['name'], s['kind'], n if n else '-'))
    print('== 16 维度（S3 国奖级）==')
    for d in DIM16:
        print('  %2d  %-20s %3d 点  star=%d  core=%-5s level=%s  scope=%s'
              % (d['no'], d['name'], d['count'], d['star'], d['core'], d['level'], d['scope']))
    print('  合计：%d 点' % total_checkpoints())
    print('== 致命项 ==')
    for f in FATAL:
        print('  %d) %s' % (f['no'], f['name']))
    print('== 阈值 ==')
    for k, (lo, hi, u) in THRESHOLDS.items():
        print('  %-22s [%s, %s] %s' % (k, lo, hi, u))
    print('== 档位矩阵 ==')
    for r in GRADE_RULES:
        print('  %s → %s' % (r['grade'], r['pred']))
    print('== 已知缺口口径 ==')
    for k, v in KNOWN_GAPS.items():
        print('  %s %s → %s' % (k, v['fact'], v['disposition']))
    return 0


def refuse_go():
    print('[REFUSED] 正式评分未启动——本模块当前仅为登记与判定骨架。')
    print('原因与流程（依《执行计划》v2）：')
    print('  1) 前置：锁定《00_执行要点.md》§五 A-E 五项裁定，产出 D0《评估口径锁定单》；')
    print('  2) 门禁：G1 基线冻结（D1 指纹齐全）→ G2 覆盖率100%/证据率>=95%/⬜<=10%')
    print('           → G3 计分六项校核（含以 Q1 先例 80-93 校准）→ G4 双轨差异定级 → G5 复现一致；')
    print('  3) 授权：若需重跑任何求解/检验脚本取证 ⟹ 升 T2，须先出《§12.3 六栏申请单》；')
    print('  4) 全程只读外围，只写本工作区文档。')
    return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true', help='登记表 + 口径算例自检（默认）')
    ap.add_argument('--dump', action='store_true', help='打印登记表')
    ap.add_argument('--go', action='store_true', help='正式评分（本阶段拒绝执行）')
    args = ap.parse_args()
    if args.go:
        return refuse_go()
    if args.dump:
        return dump()
    return selftest()


if __name__ == '__main__':
    sys.exit(main())
