# -*- coding: utf-8 -*-
"""kb 定向检索器（成绩评定专用）

用途：围绕"模型成绩评定／评分指标／判据"批量检索本地知识库，产出**可溯源的原始证据**。
产物：<工作区>/40_复核/05_成绩评定/temp/_kb_grade_scan_<轮次>.txt（UTF-8）
纪律：
  - 只读（不写 kb、不改任何正式文件）；
  - 结果仅作**内部方法学论证**，不得进入论文／交付包／支撑材料（kb 不外发）；
  - 命中行的 `文件:行号` 须回原件核对后才能写入方法学文档。

用法：
  python kb_grade_scan.py                 # 跑全部轮次
  python kb_grade_scan.py --round 2       # 只跑第 2 轮
  python kb_grade_scan.py --deep          # 附段落级深挖（--deep 透传给引擎）
"""
import os
import sys
import argparse
import subprocess

# 工作区根：本文件位于 <root>/40_复核/05_成绩评定/code/ ⟹ 向上 4 层
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ENG = os.path.join(ROOT, 'kb', 'engine', 'p5_search.py')
OUTDIR = os.path.join(ROOT, '40_复核', '05_成绩评定', 'temp')

# 每轮：轮次说明 + 检索词表（引擎多词为 OR；建议配 --deep 与大 --limit）
ROUNDS = {
    1: ('概览：评分／评审／获奖类高频词', [
        '评分标准', '评阅要点', '评审', '获奖', '模型评价', '模型检验',
        '灵敏度分析', '稳健性', '误差分析', '创新性', '自查表', '避坑',
        '扣分', '摘要', '格式规范', 'AI使用规定',
    ]),
    2: ('评分维度／指标／权重／判据', [
        '评分维度', '评价指标', '指标', '权重', '分值', '得分', '扣分点',
        '加分项', '一票否决', '致命问题', '获奖等级预测', '四维评估',
        '评委视角', '五标准', '整体评价', '合格', '优秀', '国奖', '省一',
    ]),
    3: ('自查表／检查点／篇幅配比', [
        '16大维度', '检查点', '子维度', '篇幅配比', '字数分配', '摘要四要素',
        '推荐篇幅', '结构完整性', '逻辑自洽', '术语一致', '数据引用',
    ]),
    4: ('结果正确性侧的检验指标', [
        '误差分析', '灵敏度', '全局灵敏度', 'Morris', 'Sobol', '不确定度',
        '收敛性', '守恒', 'GCI', 'Richardson', '网格无关性', '双方法验证',
    ]),
    5: ('规则／合规侧红线', [
        '论文格式规范', '支撑材料', '源程序', '匿名', '参考文献规范',
        'GB/T 7714', 'AI 工具使用规定', '学术不端', '引用规范',
    ]),
}


def run_one(query, deep, limit):
    cmd = [sys.executable, ENG, query, '--limit', str(limit)]
    if deep:
        cmd.append('--deep')
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', cwd=ROOT)
        return (r.stdout or '').strip()
    except Exception as e:  # noqa: BLE001
        return '*** ERROR %r ***' % (e,)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', type=int, default=0, help='只跑指定轮次（默认全部）')
    ap.add_argument('--deep', action='store_true', help='段落级深挖')
    ap.add_argument('--limit', type=int, default=30, help='候选条数（建议 20–30）')
    args = ap.parse_args()

    if not os.path.exists(ENG):
        print('ENGINE NOT FOUND: %s' % ENG)
        return 1
    os.makedirs(OUTDIR, exist_ok=True)

    rounds = [args.round] if args.round else sorted(ROUNDS)
    total = 0
    for rd in rounds:
        if rd not in ROUNDS:
            print('SKIP unknown round: %s' % rd)
            continue
        title, queries = ROUNDS[rd]
        out = []
        for q in queries:
            body = run_one(q, args.deep, args.limit)
            out.append('=' * 100)
            out.append('### [ROUND %d] QUERY: %s' % (rd, q))
            out.append('=' * 100)
            out.append(body)
            out.append('')
            total += 1
        path = os.path.join(OUTDIR, '_kb_grade_scan_round%d%s.txt' % (
            rd, '_deep' if args.deep else ''))
        with open(path, 'w', encoding='utf-8') as f:
            f.write('KB SCAN · %s\n检索词数：%d ｜ 引擎：%s ｜ 参数：--limit %d%s\n\n'
                    % (title, len(queries), os.path.relpath(ENG, ROOT).replace('\\', '/'),
                       args.limit, ' --deep' if args.deep else ''))
            f.write('\n'.join(out) + '\n')
        print('ROUND %d OK -> %s (%d queries)' % (rd, os.path.relpath(path, ROOT), len(queries)))
    print('TOTAL QUERIES: %d' % total)
    return 0


if __name__ == '__main__':
    sys.exit(main())
