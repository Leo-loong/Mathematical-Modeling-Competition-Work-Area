# -*- coding: utf-8 -*-
"""第四轮评估 · **客观事实测量**（不打分）。

用途：为 146 点逐点判定提供**可复核的计数证据**（页数／公式数／图表数／引用数／
关键词命中／结构清单等）。只读；不写任何交付物；产物 = stdout ＋ temp/_grade_facts4.txt。

真值来源：`50_论文/04_交排版成图方/交付排版方论文/`（编译输入与产物）、
          `50_论文/02_章节稿/成文/*.md`（我方内容稿）、`main.aux`（页数）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PAPER = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
SEC = os.path.join(PAPER, 'sections')
BODY = os.path.join(ROOT, '50_论文', '02_章节稿', '成文')

OUT = []


def p(s=''):
    OUT.append(s)
    print(s)


def read(path):
    if not os.path.exists(path):
        return ''
    return io.open(path, encoding='utf-8', errors='replace').read()


def count(pat, text, flags=0):
    return len(re.findall(pat, text, flags))


def cjk_len(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))


def strip_tex(s):
    s = re.sub(r'%.*', '', s)
    s = re.sub(r'\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?', ' ', s)
    s = re.sub(r'[{}$&_^~\\]', ' ', s)
    return s


def main():
    secs = sorted(os.listdir(SEC)) if os.path.isdir(SEC) else []
    alltex = ''
    for f in secs:
        if f.endswith('.tex'):
            alltex += read(os.path.join(SEC, f)) + '\n'
    aux = read(os.path.join(PAPER, 'main.aux'))
    log = read(os.path.join(PAPER, 'main.log'))

    p('=' * 92)
    p('第四轮评估 · 客观事实测量（generate by grade_facts4.py）')
    p('=' * 92)

    p('\n## 〇 编译产物与页数')
    m = re.search(r'Output written on main\.pdf \((\d+) pages\)', log)
    p('  全文页数（main.log）= %s' % (m.group(1) if m else '?'))
    apx = re.findall(r'\\newlabel\{(?:app:[^}]*|支撑材料文件列表)[^}]*\}\{\{[^}]*\}\{(\d+)\}', aux)
    lab = re.findall(r'\\newlabel\{([^}]*)\}\{\{[^}]*\}\{(\d+)\}', aux)
    for name, pg in lab:
        if 'app' in name.lower() or '附录' in name:
            p('  附录标签 %-34s 起页 p%s' % (name, pg))
    npage = re.search(r'\\newlabel\{([^}]*)\}\{\{[^}]*\}\{(\d+)\}', aux)
    p('  体积 = %s' % (('%.2f MB' % (os.path.getsize(os.path.join(PAPER, 'main.pdf')) / 1048576.0))
                    if os.path.exists(os.path.join(PAPER, 'main.pdf')) else '?'))

    p('\n## 一 结构（sections/*.tex）')
    for f in secs:
        t = read(os.path.join(SEC, f))
        p('  %-28s %6d 行  ｜ section %d  ｜ subsection %d  ｜ subsubsection %d'
          % (f, t.count('\n'), count(r'\\section\{', t), count(r'\\subsection\{', t),
             count(r'\\subsubsection\{', t)))
    p('  一级 \\section 清单:')
    for s in re.findall(r'\\section\*?\{([^}]*)\}', alltex):
        p('     · %s' % s)

    p('\n## 二 公式（编号／非编号）')
    eq_env = count(r'\\begin\{equation\}', alltex) + count(r'\\begin\{align\}', alltex)
    disp = count(r'\\\[', alltex) + count(r'\$\$', alltex) // 2
    p('  equation/align 环境 = %d' % eq_env)
    p('  非编号显示式（\\[ 或 $$）= %d' % disp)
    p('  公式合计（环境＋显示式+行内）≈ %d' % (eq_env + disp))
    p('  行内 $...$ 计数 ≈ %d' % (count(r'(?<!\$)\$(?!\$)[^$]{2,}?(?<!\$)\$(?!\$)', alltex)))
    p('  \\begin{equation}（带编号）逐文件:')
    for f in secs:
        t = read(os.path.join(SEC, f))
        p('     %-28s eq=%d  align=%d  disp\\[=%d' % (f, count(r'\\begin\{equation\}', t),
                                                    count(r'\\begin\{align\}', t), count(r'\\\[', t)))

    p('\n## 三 图（includegraphics）与表（longtable/tabular）')
    p('  \\includegraphics 总数 = %d' % count(r'\\includegraphics', alltex))
    p('  \\caption 总数 = %d  ｜ \\label{fig: = %d  ｜ \\label{tab: = %d'
      % (count(r'\\caption', alltex), count(r'\\label\{fig:', alltex), count(r'\\label\{tab:', alltex)))
    p('  longtable 数 = %d  ｜ tabular 数 = %d  ｜ 三线表 \\toprule = %d'
      % (count(r'\\begin\{longtable\}', alltex), count(r'\\begin\{tabular\}', alltex), count(r'\\toprule', alltex)))
    p('  图标签清单:')
    for s in re.findall(r'\\label\{(fig:[^}]*)\}', alltex):
        p('     · %s' % s)

    p('\n## 四 引用与参考文献')
    cites = re.findall(r'\\(?:up)?cite\{([^}]*)\}', alltex)
    p('  \\cite/\\upcite 命令数 = %d（展开后引用次数 = %d）' % (len(cites), sum(len(c.split(',')) for c in cites)))
    refmd = read(os.path.join(BODY, 'A_13_参考文献.md'))
    bib = re.findall(r'^\s*\[(\d+)\]\s', refmd, re.M)
    p('  参考文献条目（A_13 顶格 [n]）= %d' % len(bib))
    p('  条目编号序列: %s' % (','.join(bib[:40])))
    p('  文献类型标注: [J]=%d [M]=%d [C]=%d [D]=%d [S]=%d [EB]=%d'
      % (count(r'\[J\]', refmd), count(r'\[M\]', refmd), count(r'\[C\]', refmd),
         count(r'\[D\]', refmd), count(r'\[S\]', refmd), count(r'\[EB', refmd)))

    p('\n## 五 摘要与关键词')
    abst = read(os.path.join(SEC, '01_摘要.tex'))
    if not abst:
        cands = [f for f in secs if '摘要' in f]
        abst = read(os.path.join(SEC, cands[0])) if cands else ''
    plain = strip_tex(abst)
    p('  摘要文件字符数（去 TeX）= %d  ｜ 汉字数 = %d' % (len(plain.strip()), cjk_len(plain)))
    kw = re.search(r'关键词[：:]\s*([^\n]*)', plain)
    p('  关键词行 = %s' % (kw.group(1).strip()[:120] if kw else '(未命中)'))
    p('  摘要内小数（精确数值）个数 = %d' % len(re.findall(r'\d+\.\d+', plain)))

    p('\n## 六 假设与符号')
    a06 = read(os.path.join(BODY, 'A_06_模型假设.md'))
    p('  A_06 内「假设 N」条数 = %d' % len(re.findall(r'\*\*假设\s*[1-9]\d*\*\*', a06)))
    a04 = read(os.path.join(BODY, 'A_04_符号说明.md'))
    p('  A_04 符号表行数（以 | 开头且含 $）= %d' % len(re.findall(r'^\s*\|.*\$', a04, re.M)))

    p('\n## 七 检验体系关键词命中（全文 tex）')
    for kw in ['灵敏度', '稳健', '鲁棒', '误差', '收敛', 'GCI', 'Richardson', '守恒',
               '不确定度', '蒙特卡洛', 'Morris', 'Sobol', '对拍', '互验', '外推', '交叉验证',
               '解析解', '基准', '残差', '网格无关']:
        p('  %-10s ×%d' % (kw, alltex.count(kw)))

    p('\n## 八 独立章节自查（S3 1.9/1.10/1.11、7.1、8.6）')
    for kw in ['灵敏度', '模型评价', '评价与改进', '稳健', '模型检验', '检验']:
        hits = re.findall(r'\\section\*?\{([^}]*%s[^}]*)\}' % kw, alltex)
        p('  \\section 含「%s」= %s' % (kw, hits if hits else '(无)'))

    p('\n## 九 附录结构')
    apx = read(os.path.join(SEC, '10_附录.tex'))
    p('  \\srcfile 嵌入数 = %d' % count(r'\\srcfile\{', apx))
    p('  附录内 longtable 数 = %d' % count(r'\\begin\{longtable\}', apx))
    p('  文件名清单行数 = %d' % count(r'^\\noindent \\texttt', apx, re.M))
    for s in re.findall(r'\\section\*?\{([^}]*)\}', apx):
        p('     · %s' % s)
    for s in re.findall(r'\\textbf\{([AB]\.\d+[^}]*)\}', apx):
        p('     · 块 %s' % s[:60])

    p('\n## 十 图表件数与篇幅配额')
    p('  正文呈现图数（\\includegraphics，排除附录）= %d' % count(r'\\includegraphics', '' .join(
        read(os.path.join(SEC, f)) for f in secs if not f.startswith('10_'))))
    p('  正文表数（非附录 longtable）= %d' % count(r'\\begin\{longtable\}', ''.join(
        read(os.path.join(SEC, f)) for f in secs if not f.startswith('10_'))))
    tag = re.findall(r'图\s*(\d+-\d+)', alltex)
    p('  正文「图 X-Y」引用出现次数 = %d（去重 %d）' % (len(tag), len(set(tag))))
    tb = re.findall(r'表\s*(\d+(?:-\d+)?)', alltex)
    p('  正文「表 n／表 X-Y」引用出现次数 = %d（去重 %d）' % (len(tb), len(set(tb))))

    with io.open(os.path.join(ROOT, '40_复核', '05_成绩评定', 'temp', '_grade_facts4.txt'),
                 'w', encoding='utf-8') as f:
        f.write('\n'.join(OUT) + '\n')
    print('\n[留证] 40_复核/05_成绩评定/temp/_grade_facts4.txt')


if __name__ == '__main__':
    main()
