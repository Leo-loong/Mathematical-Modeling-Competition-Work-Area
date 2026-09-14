# -*- coding: utf-8 -*-
"""build_indexes —— "派生视图"生成器（内容侧，**只读章节稿，只写派生表**）

定位：把"论文里的引用关系"从**章节稿**里抽出来，生成 **只读派生表**，落 `50_论文/03_对照与索引/`。
      这样"对照表"**永远不是第二权威** —— 权威内容仍在各权威表里，本脚本只产"索引"。

产出（文首带 `[自动生成 · 勿手改]`）：
  A_图表编号对照.md   F-xx ↔ 图NN（PDF 文件索引号）↔ 图<章号>-<序>（论文内索引号）★ **0 章节稿也可生成**
  A_参考文献对照.md   上标 [n] ↔ 题录 ID（校验是否存在于题录表）↔ 首现章节
  A_符号引用对照.md   正文符号 ↔ 《A_符号表》是否存在 ↔ 首现章节
  A_数值溯源对照.md   正文数值 ↔ 《A_数值口径总表》是否存在 ↔ 首现章节

用法：
  python build_indexes.py            # 生成／刷新三张派生表
  python build_indexes.py --check    # 只核对，不写文件（退出码 1 = 有缺口）
  python build_indexes.py --root <工作区根>

纪律：
  * **不写章节稿**，不改任何权威表；
  * 幂等：同输入恒同输出；
  * 无章节稿时**安全空跑**并明确报"尚无章节稿"（不产空表 -- 空表=伪权威）。
"""
import argparse
import glob
import io
import os
import re
import sys

BANNER = ('[自动生成 · 勿手改]\n\n'
          '> 本文件由 `50_论文/01_写作计划/code/build_indexes.py` 生成，**请勿手改**；\n'
          '> 权威内容在各自的权威表中（见 `50_论文/03_对照与索引/README.md`）；'
          '章节稿变动后**重跑本脚本即同步**。\n')

FIG = re.compile(r'图\s*(\d+)\s*（\s*(F-\d{2})\s*）')
TAB = re.compile(r'表\s*(\d+)')
EQ = re.compile(r'式\s*\((\d+)\s*[-–]\s*(\d+)\)')
SUP = re.compile(r'\[(\d+)\]')
SYM = re.compile(r'\$([^$\n]{1,40})\$')
DEC = re.compile(r'\d+\.\d{2,}')


def find_root(start):
    p = start
    for _ in range(8):
        if os.path.isdir(os.path.join(p, '10_赛题')) or os.path.isdir(os.path.join(p, '20_交付包')):
            return p
        p = os.path.dirname(p)
    return os.getcwd()


def norm_sym(s):
    return re.sub(r'[\s\\{}]', '', s)


def chapters_dir(root):
    """章节稿目录：优先 `02_章节稿/基线/`（三环节结构），回退 `02_章节稿/`。"""
    p1 = os.path.join(root, '50_论文', '02_章节稿', '基线')
    if os.path.isdir(p1) and any(f.startswith('A_') and f.endswith('.md') for f in os.listdir(p1)):
        return p1
    return os.path.join(root, '50_论文', '02_章节稿')


def load(root):
    """载入权威表（只读）与章节稿（只读）。"""
    ctx = {'refnums': set(), 'symbols': set(), 'numbers': set()}
    p = os.path.join(root, '20_交付包', '07_引用与术语', 'A_题录表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['refnums'] = {str(i) for i in range(1, 19)} if ('§三' in t or '题录' in t) else set()
    p = os.path.join(root, '20_交付包', '02_符号表', 'A_符号表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['symbols'] = {norm_sym(x) for x in SYM.findall(t)}
    p = os.path.join(root, '20_交付包', '05_数值口径总表', 'A_数值口径总表.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        ctx['numbers'] = set(DEC.findall(t))
    d = chapters_dir(root)
    chaps = []
    for f in sorted(glob.glob(os.path.join(d, 'A_*.md'))):
        chaps.append((os.path.basename(f),
                      io.open(f, encoding='utf-8', errors='replace').read()))
    return ctx, chaps


def collect(chaps):
    """按出现顺序收集引用关系。"""
    out = {'fig': [], 'tab': [], 'eq': [], 'ref': [], 'sym': [], 'num': []}
    for name, txt in chaps:
        for n, f in FIG.findall(txt):
            out['fig'].append((int(n), f, name))
        for n in TAB.findall(txt):
            out['tab'].append((int(n), name))
        for c, s in EQ.findall(txt):
            out['eq'].append(('%s-%s' % (c, s), name))
        for n in SUP.findall(txt):
            out['ref'].append((n, name))
        for s in SYM.findall(txt):
            if re.fullmatch(r'[\d\s.,%+\-=()]*', s):
                continue
            out['sym'].append((s, name))
        for v in DEC.findall(txt):
            out['num'].append((v, name))
    return out


def first_seen(rows):
    """(key, 首现章节)，保序去重。"""
    seen, res = set(), []
    for k, f in rows:
        if k in seen:
            continue
        seen.add(k)
        res.append((k, f))
    return res


def table(head, rows):
    s = '| ' + ' | '.join(head) + ' |\n|' + '---|' * len(head) + '\n'
    for r in rows:
        s += '| ' + ' | '.join(str(x) for x in r) + ' |\n'
    return s if rows else s + '| （尚无数据） |' + ' |' * (len(head) - 1) + '\n'


def build(ctx, chaps):
    c = collect(chaps)
    ref = table(['上标 `[n]`', '题录表是否存在', '首现章节'],
                [(n, '✅' if (not ctx['refnums'] or n in ctx['refnums']) else '❌ **不在题录表**', f)
                 for n, f in first_seen(c['ref'])])
    sym = table(['正文符号', '《A_符号表》是否存在', '首现章节'],
                [('`$%s$`' % s, '✅' if (not ctx['symbols'] or norm_sym(s) in ctx['symbols'])
                  else '⚠️ **表外符号**', f) for s, f in first_seen(c['sym'])])
    num = table(['正文数值', '《A_数值口径总表》是否存在', '首现章节'],
                [(v, '✅' if (not ctx['numbers'] or v in ctx['numbers']) else '⚠️ **未回指**', f)
                 for v, f in first_seen(c['num'])])
    return {
        'A_参考文献对照.md': ('# 参考文献对照（正文上标 ↔ 题录 ID）\n\n'
                         '> **它回答**：正文每个上标 `[n]` 出现在哪一节、是否在题录表内。'
                         '**它不回答**：文献条目内容（→ `20_交付包/07_引用与术语/A_题录表.md` §三）。\n\n' + ref),
        'A_符号引用对照.md': ('# 符号引用对照（正文符号 ↔ 符号表）\n\n'
                         '> **它回答**：正文用了哪些符号、首现在哪一节、是否都在《A_符号表》。'
                         '**它不回答**：符号的含义与单位（→ `20_交付包/02_符号表/A_符号表.md`）。\n\n' + sym),
        'A_数值溯源对照.md': ('# 数值溯源对照（正文数值 ↔ 口径表）\n\n'
                         '> **它回答**：正文每个数值首现在哪一节、能否在《A_数值口径总表》回指。'
                         '**它不回答**：数值本身（→ 口径表；正文取数**只认该表**）。\n\n' + num),
    }


def gen_fig_map(root, chaps):
    """《A_图表编号对照.md》—— **三套编号的桥**（F 号 ↔ PDF 文件索引号 ↔ 论文内索引号）。

    权威源：`30_图表/05_交付清单/A_图表交付清单.md` **§七 编号映射**（成品图号 ↔ F 号 ↔ 图名）。
    到位判定：**只看 `50_论文/05_成品图/`（交付版唯一副本）** —— 对方投递口 `30_图表/最终图表/`
    是"稿源"，**不作论文用图来源**（见 `50_论文/05_成品图/README.md` 与 `03_对照与索引/README.md` §六）。
    论文内索引号：从**章节稿的「占位清单」**表行抽取（`图<章号>-<序>` ＋ `F-xx` 同行；**章号＝该模块在论文中的章序**）。
    **本表可在 0 份章节稿时独立生成**（不依赖章节稿）。
    """
    rows = []
    p = os.path.join(root, '30_图表', '05_交付清单', 'A_图表交付清单.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8', errors='replace').read()
        m = re.search(r'##\s*七、.*?(?=\n##\s*八、)', t, re.S)
        seg = m.group(0) if m else ''
        raw = []
        for line in seg.splitlines():
            if not line.startswith('|'):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) != 9:
                continue
            if '成品图号' in cells[0]:                       # 表头
                continue
            if not cells[0] or set(cells[0]) <= set('-: '):   # 分隔行
                continue
            raw.append(cells)
        # §七 是三段并排（每行 3 组），须**按段取**才得顺序：先全表第 1 段，再第 2、第 3 段
        for k in (0, 3, 6):
            for cells in raw:
                fno = re.sub(r'[^A-Za-z0-9\-]', '', cells[k + 1])
                if not re.match(r'^F-\d{2}$', fno):
                    continue
                nm = re.sub(r'\*\*', '', cells[k + 2])
                nm = re.sub(r'（\s*(已重画|本轮补登|本轮新增)\s*）', '', nm).strip()
                rows.append((fno, nm, cells[k]))

    # 到位口径：**只看 `50_论文/05_成品图/`（交付版唯一副本）** —— 对方投递口 `30_图表/最终图表/` 不作数
    arrived = set()
    d0 = os.path.join(root, '50_论文', '05_成品图')
    if os.path.isdir(d0):
        for n in os.listdir(d0):
            mm = re.match(r'图(\d+)', n)
            if mm and n.lower().endswith('.pdf'):
                arrived.add(mm.group(1))

    used = {}
    for nm, txt in chaps:
        for line in txt.splitlines():
            if not line.startswith('|'):
                continue
            cs = [c.strip().strip('`*') for c in line.strip().strip('|').split('|')]
            idx = [c.replace(' ', '') for c in cs
                   if re.fullmatch(r'图\s*(?:\d+\s*-\s*\d+|A\s*-\s*\d+)', c)]
            fn = [c for c in cs if re.fullmatch(r'F-\d{2}', c)]
            if idx and fn:
                used.setdefault(fn[0], '%s（%s）' % (idx[0], nm.replace('.md', '')))

    body = ['# 图表编号对照（**三套编号的桥**）', '',
            '> **它回答**：`F-xx` ↔ `图NN`（PDF 文件索引号）↔ `图<章号>-<序>`（论文内索引号）。',
            '> **它不回答**：图名清单与交付状态（→ `30_图表/05_交付清单/A_图表交付清单.md` §七）；'
            '图数据（→ `20_交付包/04_图表包/data/*.csv`）。', '',
            '> **正文只写「论文内索引号」**；F 号与 PDF 文件索引号**只出现在每节稿末的「占位清单」**'
            '（定稿时整块删除）。', '',
            '| F 号 | 图名 | PDF 文件索引号 | 到位（`05_成品图/`） | 论文内索引号（首现章节） |',
            '|---|---|---|---|---|']
    ok = 0
    for fno, nm, pno in rows:
        num = re.sub(r'[^0-9]', '', pno)[:2] if pno else ''
        got = '✅' if (num and num in arrived) else '⬜ 未收割'
        if num and num in arrived:
            ok += 1
        body.append('| %s | %s | %s | %s | %s |'
                    % (fno, nm, pno or '—', got, used.get(fno, '')))
    body += ['', '**小计**：F 号 **%d** 个；已在 `05_成品图/`（**交付版唯一副本**）**收割 %d** 个；'
                 '论文内索引号**已回填 %d** 个（随章节稿增长）。'
             % (len(rows), ok, len(used))]
    # ★ **同源产出机器可读版 `A_图表编号对照.json`**（与上面 .md 同一份数据，一次性写出，杜绝两处解析分歧）；
    #   下游（如 `50_论文/02_章节稿/gen_latex.py`）一律读 JSON，**不再解析 Markdown 表格**。
    import json
    items = []
    for fno, nm, pno in rows:
        num = re.sub(r'[^0-9]', '', pno)[:2] if pno else ''
        ref = used.get(fno, '')
        m = re.match(r'^\s*图\s*([A-Za-z]?\s*-?\s*\d+(?:\s*-\s*\d+)?)', ref)
        # `pdf_index` 须**剥掉加粗标记与空格**（对照表里部分行的 PDF 索引号写作 `**图24**`）——
        # 否则下游按该串查成品图目录会失配、退回占位框（本轮实测 6 张）。
        items.append({'f_no': fno, 'name': nm,
                      'pdf_index': (pno or '').replace('**', '').replace(' ', '').strip(),
                      'pdf_no': num, 'arrived': bool(num and num in arrived),
                      'paper_index': (m.group(1).replace(' ', '') if m else ''),
                      'first_chapter': (re.search(r'（([^）]*)）', ref).group(1) if ref else '')})
    doc = {'generated_by': 'build_indexes.py（与 A_图表编号对照.md 同源，勿手改）',
           'updated': 'rebuild by rerunning build_indexes.py',
           'counts': {'f_total': len(rows), 'arrived': ok, 'paper_index_filled': len(used)},
           'figures': items}
    return '\n'.join(body) + '\n', json.dumps(doc, ensure_ascii=False, indent=1) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=None)
    ap.add_argument('--check', action='store_true', help='只核对不写文件')
    a = ap.parse_args()
    root = a.root or find_root(os.path.dirname(os.path.abspath(__file__)))
    ctx, chaps = load(root)
    outdir = os.path.join(root, '50_论文', '03_对照与索引')
    print('== build_indexes ==')
    print('工作区根：%s' % root)
    print('权威表：题录 %d ｜ 符号 %d ｜ 口径表数值 %d'
          % (len(ctx['refnums']), len(ctx['symbols']), len(ctx['numbers'])))
    md, jtxt = gen_fig_map(root, chaps)
    files = {'A_图表编号对照.md': md}
    if not chaps:
        print('章节稿：**0 份** ⟹ 文献／符号／数值三张对照**不生成**（空表＝伪权威）；')
        print('  《A_图表编号对照.md》**可独立生成**（权威源＝交付清单 §七 ＋ 成品图）。')
        print('  章节稿目录：%s' % chapters_dir(root))
    else:
        print('章节稿：%d 份' % len(chaps))
        files.update(build(ctx, chaps))
    bad = 0
    for _, body in files.items():
        bad += body.count('❌') + body.count('⚠️')
    for name, body in files.items():
        p = os.path.join(outdir, name)
        if a.check:
            # 逐字节比对**完整文件**（BANNER ＋ body）；旧写法按首个换行切分，
            # 会把 BANNER 的剩余部分留进左侧 ⟹ 恒不相等（已修正）。
            ok = (os.path.exists(p)
                  and io.open(p, encoding='utf-8').read() == BANNER + body)
            print('  [check] %-22s %s' % (name, '一致' if ok else '**需刷新**'))
        else:
            io.open(p, 'w', encoding='utf-8').write(BANNER + body)
            print('  [write] %-22s %d 行' % (name, body.count('\n') + 1))
    jp = os.path.join(outdir, 'A_图表编号对照.json')          # ★ 机器可读版（无 BANNER，纯 JSON）
    if a.check:
        okj = os.path.exists(jp) and io.open(jp, encoding='utf-8').read() == jtxt
        print('  [check] %-22s %s' % ('A_图表编号对照.json', '一致' if okj else '**需刷新**'))
    else:
        io.open(jp, 'w', encoding='utf-8').write(jtxt)
        print('  [write] %-22s %d 行' % ('A_图表编号对照.json', jtxt.count('\n') + 1))
    print('异常项合计（❌／⚠️）：%d ⟹ %s' % (bad, '见上表' if bad else '全部可回指'))
    return 1 if (bad and a.check) else 0


if __name__ == '__main__':
    sys.exit(main())
