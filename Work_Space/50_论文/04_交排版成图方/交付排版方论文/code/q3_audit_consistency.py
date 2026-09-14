# -*- coding: utf-8 -*-
"""
第三问全量综合复查 · 口径一致性扫描（T0 只读，不重跑任何代码）
================================================================================
基线：11_建模/大白话讲模型/A_第三问求解复盘.md（用户指定）
规则：若基线错 -> 改基线；若其他文件错 -> 对齐基线。

扫描对象：Q3 工作区流程文件 + 结果文件 + 交付包全部相关文件。
检查项：
  A. 关键数值是否全库一致（t_end、判据、网格、步长、内层上限、熔断）
  B. 是否存在互相矛盾的说法
  C. 是否存在重复文档（同内容多份）
  D. 是否存在缺口（该有却没有的文档/条目）
  E. 状态是否过时（计划态/待批准 vs 已完成）
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

WS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

TARGETS = [
    # 基线
    (r'11_建模\大白话讲模型\A_第三问求解复盘.md', '基线'),
    # Q3 工作区
    (r'11_建模\11-3_算法与管线\Q3\A_Q3求解记录.md', '流程'),
    (r'11_建模\11-3_算法与管线\Q3\A_Q3求解思路与工作流.md', '流程'),
    # 交付包
    (r'20_交付包\01_模型叙述\A_Q3模型叙述.md', '交付'),
    (r'20_交付包\01_模型叙述\A_Q3结果与分析.md', '交付'),
    (r'20_交付包\06_可靠性与方法学\A_Q3可靠性与方法学.md', '交付'),
    (r'20_交付包\05_数值口径总表\A_数值口径总表.md', '交付'),
    (r'20_交付包\08_章节素材映射\A_章节素材映射.md', '交付'),
    (r'20_交付包\09_代码与复现\A_代码复现.md', '交付'),
    (r'20_交付包\09_代码与复现\README_日志索引.md', '交付'),
    (r'20_交付包\13_论文可删减部分\A_论文可删减部分.md', '交付'),
    (r'20_交付包\04_图表包\04-1_图表规格卡\F-33_Q3长时程含水率演化与烘干结束时间.md', '交付'),
    (r'20_交付包\04_图表包\04-1_图表规格卡\F-34_Q3收敛性与网格裁决.md', '交付'),
    (r'20_交付包\04_图表包\04-1_图表规格卡\F-35_Q3灵敏度与干壳阻滞.md', '交付'),
]

# (标签, 正则或字面量集合, 期望语义)
CHECKS = [
    # A. 关键数值（★口径修正后：核心答案 57.5314 h）
    ('t_end=57.5314h', [r'57\.5314', r'57\.53\s*h', r'207\s?113'],
     '核心答案：所有文档若提到 t_end，数值须一致（57.5314 h / 207113.094 s）'),
    ('判据=0.15', [r'0\.15'], '达标判据 C<0.15（严格小于）'),
    ('网格0.25mm / N=80', [r'0\.25\s*mm', r'0\.25000', r'N=80'],
     '主力空间网格 Δr=0.25 mm（N=80 区间/81 节点）'),
    ('内部步1/32s', [r'1/32', r'0\.03125\s*s'],
     '内部步长 1/32 s（不得因输出 60 s 而放大）'),
    ('输出60s', [r'60\s*s', r'每\s*60\s*秒'], 'Q3 输出间隔 60 s'),
    ('内层上限30', [r'maxit\s*=?\s*30', r'上限\s*\*?\*?30'],
     'Picard 内层上限 30（Q2 修正值）'),
    ('熔断120h', [r'120\s*h', r'120\s*小时'], '熔断上界 120 h'),
    # B. 敏感度与检验数值（★修正后）
    ('km弹性-0.148/-0.090', [r'0\.148', r'0\.090'],
     'k_m 弹性 −0.148／−0.090（方向正常，非干壳阻滞）'),
    ('h弹性≈-0.003/0', [r'0\.003', r'0\.000'],
     'h 弹性 ≈ −0.003／0.000（几乎无影响）'),
    ('守恒残差2.394e-3', [r'2\.394', r'2\.39'], '质量相对残差 2.394e-3'),
    ('渐近解97.7h(上界)', [r'97\.7'], '圆柱渐近解 97.7 h（作上界）'),
    ('低C端下界25.8h', [r'25\.8'], '分段积分 25.8 h（作下界）'),
    ('表面列相对变化≤9.8e-5', [r'9\.8\\times10\^\{-5\}', r'9\.8e-5'],
     '表面列相邻相对变化 ≤9.8e-5（4 位小数稳定）'),
    # C. 口径与边界声明（★新增）
    ('界面口径=积分平均', [r'积分平均'], '界面变系数取沿 C 的积分平均（口径 M6）'),
    ('低C外推贡献43–66%', [r'43\\?%', r'66\\?%'], '低 C 端 D 外推贡献 43%–66% 时长'),
    ('判据敏感度38.33/85.09', [r'38\.33', r'85\.09'], 'C_crit=0.18/0.13 → 38.33/85.09 h'),
    # D. 状态
    ('已完成(非计划态)', [r'已完成', r'DONE'], '状态不得仍写"计划态/待批准"'),
]


def scan():
    print('=' * 96)
    print('第三问全量综合复查 · 口径一致性扫描（基线=大白话讲模型/A_第三问求解复盘.md）')
    print('=' * 96)
    print()

    exists, missing = [], []
    for rel, kind in TARGETS:
        p = os.path.join(WS, rel)
        (exists if os.path.exists(p) else missing).append((rel, kind, p))

    print('【清点】目标文件 %d 个：存在 %d，缺失 %d' % (len(TARGETS), len(exists), len(missing)))
    for rel, kind, _ in missing:
        print('   ✗ 缺失 [%s] %s' % (kind, rel))
    print()

    # 逐文件逐项扫描
    print('【A～D 逐项命中矩阵】（数字=命中次数，- = 未提及）')
    hdr = '%-34s' % '文件'
    for lbl, _, _ in CHECKS:
        hdr += '%-13s' % lbl[:12]
    print(hdr)
    print('-' * len(hdr))
    table = {}
    for rel, kind, p in exists:
        t = io.open(p, encoding='utf-8').read()
        row = []
        for lbl, pats, _ in CHECKS:
            n = sum(len(re.findall(pt, t)) for pt in pats)
            row.append(n)
        table[rel] = row
        line = '%-34s' % (os.path.basename(rel)[:33])
        for n in row:
            line += '%-13s' % (str(n) if n else '-')
        print(line)
    print()

    # E. 矛盾与过时检测
    print('【E. 状态与矛盾检测】')
    for rel, kind, p in exists:
        t = io.open(p, encoding='utf-8').read()
        issues = []
        # 过时的"计划态/待批准"（排除变更记录与已说明例外）
        for m in re.finditer(r'(计划态|待批准|尚未执行)', t):
            s = max(0, m.start() - 60)
            ctx = t[s:m.end() + 60].replace('\n', ' ')
            if ('v1' in ctx) or ('v2' in ctx) or ('v3' in ctx) or ('原为' in ctx) or ('成文时' in ctx):
                continue
            issues.append('过时状态: ...%s...' % ctx[-80:])
        # 危险表述：把表面值说成已收敛
        if re.search(r'表面.{0,20}(已收敛|收敛到\s*4\s*位)', t):
            issues.append('⚠ 可能过度声明表面值已收敛')
        if issues:
            print('   [%s] %s' % (os.path.basename(rel), rel))
            for it in issues[:3]:
                print('       · %s' % it)
    print('   （无输出 = 未发现过时状态与过度声明）')
    print()

    # F. 重复文档检测（同名不同目录 / 内容高度相似）
    print('【F. 疑似重复文档】')
    seen = {}
    for rel, kind, p in exists:
        base = os.path.basename(rel)
        seen.setdefault(base, []).append(rel)
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    if dup:
        for k, v in dup.items():
            print('   ⚠ 同名多份: %s' % k)
            for x in v:
                print('       · %s' % x)
    else:
        print('   （无同名多份）')
    print()

    # G. 交叉引用有效性（文档中引用的 Q3 文件名是否存在）
    print('【G. 交叉引用有效性】')
    bad = []
    for rel, kind, p in exists:
        t = io.open(p, encoding='utf-8').read()
        for fn in set(re.findall(r'(A_Q3[^\s，。；、）)]*\.md)', t)):
            cand = [os.path.join(WS, d, fn) for d in
                    ('11_建模/大白话讲模型', '11_建模/11-3_算法与管线/Q3',
                     '20_交付包/01_模型叙述', '20_交付包/06_可靠性与方法学',
                     '20_交付包/05_数值口径总表', '20_交付包/09_代码与复现')]
            if not any(os.path.exists(c) for c in cand):
                bad.append((os.path.basename(rel), fn))
    if bad:
        for a, b in sorted(set(bad)):
            print('   ⚠ 悬空引用: %s -> %s' % (a, b))
    else:
        print('   （无悬空引用）')


if __name__ == '__main__':
    scan()
