# -*- coding: utf-8 -*-
"""第一步：克隆 36 个唯一 AI 提示词 md 到 kb/source/AI提示词合集/（分类子目录）。
原则：零改动内容、原文件不动、同 hash 只克隆一份、生成映射清单。"""
import os, io, shutil, hashlib, re

ROOT = r'c:/Users/wang-/Desktop/2026数学建模/2025国赛真题/B题/Work_Space/kb/source'
SRC_DIRS = [os.path.join(ROOT, '第一批提取后'), os.path.join(ROOT, '第二批提取后')]
DST = os.path.join(ROOT, 'AI提示词合集')

# 1) 收集全部 AI 提示词/自查/合规 md（提取后目录；文件名可能不含"提示词"三字）
KEYS = ['提示词', '自查表', 'AI红线', '工具使用', '奖项预测', '人工智能工具']
files = []
for sd in SRC_DIRS:
    for dp, dn, fn in os.walk(sd):
        for f in fn:
            if f.endswith('.md') and any(k in f for k in KEYS):
                files.append(os.path.join(dp, f))

# 2) 内容 hash 分组（规范化换行）
groups = {}
for p in files:
    data = open(p, 'rb').read().replace(b'\r\n', b'\n')
    groups.setdefault(hashlib.sha1(data).hexdigest()[:12], []).append(p)

# 3) 分类规则（美赛相关暂不纳入）
def is_mcss(path):
    return ('美赛' in path or 'MCM' in path or 'ICM' in path or '电工杯' in path
            or ('附录' in os.path.basename(path) and re.match(r'^\d+、附录', os.path.basename(path))))

def classify(path):
    b = os.path.basename(path)
    if is_mcss(path):
        return None  # 美赛暂不考虑
    if re.match(r'^0[1-6]_', b) or '一键式全流程' in b:
        return '01_国赛全流程'
    for kw in ['痕迹', '全维度自查', '适配性检查', '国奖级', '图表AI国奖级', '全自动自查表',
               '图表AI自动优化', '奖项预测', 'AI红线']:
        if kw in b:
            return '02_检测自查与优化'
    if '官方通知' in path or 'AI工具使用详情' in b or '工具使用' in path:
        return '06_官方AI合规'
    return None

# 4) 清理旧合集（幂等重建）
import shutil as _sh
if os.path.isdir(DST):
    _sh.move(DST, os.path.join(ROOT, 'temp', '_old_合集_%d' % len(os.listdir(DST))))

# 5) 克隆（每组一份，代表=路径排序第一个；跳过美赛）
mapping, clones, skipped = [], [], []
for h, ps in sorted(groups.items()):
    rep = sorted(ps)[0]
    cls = classify(rep)
    if cls is None:
        skipped.append(rep)
        continue
    dstdir = os.path.join(DST, cls)
    os.makedirs(dstdir, exist_ok=True)
    dst = os.path.join(dstdir, os.path.basename(rep))
    shutil.copy2(rep, dst)
    clones.append(dst)
    mapping.append((h, rep, len(ps), os.path.relpath(dst, ROOT)))

# 6) 00_说明.md
with io.open(os.path.join(DST, '00_说明.md'), 'w', encoding='utf-8') as f:
    f.write('# AI 提示词合集 · 说明\n\n')
    f.write('> 本目录为知识库内 **国赛相关 AI 提示词/自查/官方合规文件** 的分类克隆版\n')
    f.write('> （内容零改动，原文保留在原位）。生成：2026-09-10；唯一内容 %d 份；\n' % len(clones))
    f.write('> 同内容多副本只收一份（映射见下）；docx/pdf 原件未克隆（保留原位，可按文件名检索）。\n')
    f.write('> **美赛相关材料（17 套附录及散件，19 个唯一内容）暂不纳入**，原件在\n')
    f.write('> `第二批(提取后)/2026国赛AI助攻资料合集/AI+数学建模提示词汇总！/`，需要时再迁。\n\n')
    f.write('## 目录结构\n\n')
    f.write('- 01_国赛全流程：七步全流程提示词（赛题分析→数据预处理→问题求解→模型检验→论文写作→图表美化 + 一键式）\n')
    f.write('- 02_检测自查与优化：AI 痕迹检测 V5.0、论文全维度自查（标准/进阶）、模型适配性检查、国奖级论文优化、图表美化、AI 全自动自查表（标准/进阶）、V2.4 升级版\n')
    f.write('- 06_官方AI合规：★官方《人工智能工具使用规定》(2026 试行) + AI 工具使用详情模板×3\n\n')
    f.write('## 来源映射（唯一内容 → 原位置；n=原副本数）\n\n')
    for h, rep, n, dstrel in mapping:
        f.write('- `%s` (n=%d) ← %s\n' % (dstrel, n, os.path.relpath(rep, ROOT)))
    if skipped:
        f.write('\n## 暂缓（美赛，%d 项）\n\n' % len(skipped))
        for p in sorted(skipped):
            f.write('- %s\n' % os.path.relpath(p, ROOT))

print('unique cloned:', len(clones), '| skipped(美赛):', len(skipped))
for c in sorted(clones):
    print(' ', os.path.relpath(c, ROOT))
