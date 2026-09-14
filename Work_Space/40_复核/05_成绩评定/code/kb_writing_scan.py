# -*- coding: utf-8 -*-
"""论文写作专项 kb 检索器（**只读**；证据仅内部使用，不得进入论文／交付包）。

产物：`40_复核/05_成绩评定/temp/_kb_writing_scan_round<N>.txt`
用法：`python kb_writing_scan.py`（全部轮次）｜`--round 4`｜`--limit 20`
"""
import os
import sys
import argparse
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ENG = os.path.join(ROOT, 'kb', 'engine', 'p5_search.py')
OUTDIR = os.path.join(ROOT, '40_复核', '05_成绩评定', 'temp')

ROUNDS = {
    1: ('摘要与标题', ['摘要写法 摘要四要素 摘要字数 关键词', '摘要 模型 结果 结论 写法']),
    2: ('问题重述与问题分析', ['问题重述 问题分析 背景 技术路线 框架图']),
    3: ('模型假设与符号说明', ['模型假设 假设合理性 假设依据 符号说明 符号表']),
    4: ('模型建立与求解（含公式与算法叙述）', ['模型建立 公式推导 算法步骤 求解过程 参数设置']),
    5: ('结果分析与数据引用', ['结果分析 数据引用 图表引用 对比 规律']),
    6: ('模型检验章', ['模型检验 误差分析 灵敏度分析 稳健性检验 验证 检验章节']),
    7: ('模型评价与改进展望', ['模型评价 优缺点 改进与展望 推广性 局限性']),
    8: ('参考文献与引用规范', ['参考文献 GB/T 7714 引用规范 文内标注 文献数量']),
    9: ('语言表述与常见扣分', ['语言表达 术语一致 逻辑自洽 常见错误 扣分点 数据引用不准确']),
    10: ('写作流程与合规自查', ['写作顺序 时间分配 摘要最后写 查重 AI痕迹 学术不端 自查清单']),
}


def run_one(q, limit):
    try:
        r = subprocess.run([sys.executable, ENG, q, '--limit', str(limit)],
                           capture_output=True, text=True, encoding='utf-8',
                           errors='replace', cwd=ROOT)
        return (r.stdout or '').strip()
    except Exception as e:  # noqa: BLE001
        return '*** ERROR %r ***' % (e,)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--round', type=int, default=0)
    ap.add_argument('--limit', type=int, default=20)
    a = ap.parse_args()
    if not os.path.exists(ENG):
        print('ENGINE NOT FOUND: %s' % ENG)
        return 1
    os.makedirs(OUTDIR, exist_ok=True)
    rs = [a.round] if a.round else sorted(ROUNDS)
    tot = 0
    for r in rs:
        title, qs = ROUNDS[r]
        out = []
        for q in qs:
            out.append('=' * 96)
            out.append('### [R%d] %s' % (r, q))
            out.append('=' * 96)
            out.append(run_one(q, a.limit))
            out.append('')
            tot += 1
        p = os.path.join(OUTDIR, '_kb_writing_scan_round%d.txt' % r)
        with open(p, 'w', encoding='utf-8') as f:
            f.write('KB WRITING SCAN · R%d %s ｜ 检索词 %d ｜ --limit %d\n\n'
                    % (r, title, len(qs), a.limit))
            f.write('\n'.join(out) + '\n')
        print('R%-2d OK -> %s (%d queries)' % (r, os.path.relpath(p, ROOT), len(qs)))
    print('TOTAL QUERIES: %d' % tot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
