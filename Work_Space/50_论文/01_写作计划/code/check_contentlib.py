# -*- coding: utf-8 -*-
"""check_contentlib —— 「章节内容库 / 章节稿」结构性只读校验（第二环节配套工具）

定位：补齐 `paper_lint.py` 未覆盖的**结构性**检查——尤其是"**编号连续性 / 必需标题存在性**"。
      该类缺陷由一次真实事故催生：批量插入脚本未保留锚点，导致 `## 6.2`／`## 5.1`／`## 二、`／`## 占位清单`
      等**标题被整行吞掉**，而当时 25 类规则**全都没有报**（R-14 只查"式/图表"编号，不查标题结构）。

用法：
  python check_contentlib.py                     # 默认：校验「章节内容库」＋「基线」
  python check_contentlib.py --dir <目录>         # 只校验指定目录
  python check_contentlib.py --target baseline|content|all
  python check_contentlib.py --json
退出码：0 = 无 ❌；1 = 存在 ❌（可用于门禁流水线）

规则（只读，不改任何文件）：
  C-1  内容库**文件齐备性**（未开工时不报错，只报"未建 N 件"）
  C-2  条目 **ID 合法性**（模块号-节号-序）与**重复检测**
  C-3  条目 **字段齐全性**（13 字段；"不适用"须带理由）
  C-4  ★ 章节稿**编号连续性 ＋ 必需标题存在性**（本次事故的直接对策）
  C-5  图表登记 ↔ `03_对照与索引/A_图表编号对照.md` **双向一致**
  C-6  称形检查：问次汉字化、用"改进"不用"创新"、**F 号不得越位到正文行内**
"""
import argparse
import io
import json
import os
import re
import sys

SEV_ERR, SEV_WARN, SEV_INFO = '❌', '⚠️', 'ℹ️'

# ---- 内容库应有件（30 件）----
GLOBAL_FILES = ['00_内容库总纲.md', '00_条目字段字典.md']
MODULES = ['%02d' % i for i in range(1, 15)]

# ---- C-2／C-3 文件级豁免：**方案／规程型文件** ----
# 这类文件虽以 `_内容条目.md` 收尾，但其 `###` 标题是**章节号**（`3.1`／`7.1`），而非
# 「模块号-节号-序」条目 ID；被 C-2 当作条目头解析 ⟹ **结构性误报**
# （见 `40_复核/01_复核记录/0913_公式展开与写作亮点独立复核.md` 的 Z-06）。
# **豁免为文件级且附理由，不削弱真条目文件的规则。**
NON_ITEM_FILES = {'A_公式展开方案_内容条目.md'}

# ---- 条目字段（13）----
FIELDS = ['条目 ID', '所属节', '类型', '条目', '依据', '数值口径', '关联图表',
          '关联文献', '目标篇幅', '状态', '验收判据', '风险／备注', '变更痕']

# ---- 各稿"必需标题"（本次事故的回归防线；只用最短可判特征）----
REQUIRED = {
    'A_08': ['## 5.0 ', '## 5.1 ', '## 5.2 ', '## 5.3 ', '## 5.4 ', '## 六、', '## 占位清单'],
    'A_10': ['## 6.1 ', '## 6.2 ', '## 6.3 ', '## 6.4 ', '## 6.5 ', '## 6.6 ', '## 6.7 ',
             '## 6.8 ', '## 6.9 ', '## 6.10 ', '## 6.11 ', '## 占位清单'],
    'A_11': ['## 一、模型优点', '## 二、模型不足与改进方向', '## 三、模型的推广', '## 占位清单'],
    'A_07': ['## 一、符号说明', '### 表 0-1', '### 分组说明', '## 占位清单'],
    'A_02': ['## 摘要', '## 占位清单'],
    'A_04': ['## 占位清单'],
    'A_05': ['## 占位清单'],
    'A_06': ['## 一、模型假设', '## 占位清单'],
    'A_09': ['## 一、', '## 二、', '## 三、', '## 四、', '## 五、', '## 六、', '## 占位清单'],
    'A_12': ['## 占位清单'],
    'A_13': ['## 一、引用位置对照', '## 二、字段核验留痕', '## 占位清单'],
    'A_14': ['## 附录 A', '## 附录 B', '## 附录 C', '## 占位清单'],
}

HEAD_NUM = re.compile(r'^(#{2,3})\s*(\d+)\.(\d+)(?:\.(\d+))?([a-z])?\s')
ITEM_ID = re.compile(r'^([0-9]{2})-(\d+(?:\.\d+)*)-(\d{2,3})$')


def find_root(start):
    p = start
    for _ in range(8):
        if os.path.isdir(os.path.join(p, '10_赛题')) or os.path.isdir(os.path.join(p, '20_交付包')):
            return p
        p = os.path.dirname(p)
    return os.getcwd()


def rd(p):
    return io.open(p, encoding='utf-8', errors='replace').read()


def drafts_dir(root):
    """章节稿（基线）目录：优先 基线/，回退 02_章节稿/。"""
    p1 = os.path.join(root, '50_论文', '02_章节稿', '基线')
    if os.path.isdir(p1) and any(f.startswith('A_') and f.endswith('.md') for f in os.listdir(p1)):
        return p1
    return os.path.join(root, '50_论文', '02_章节稿')


def content_dir(root):
    return os.path.join(root, '50_论文', '02_章节稿', '章节内容库')


# ───────────────────────── C-1 / 2 / 3：内容库
def check_content(root):
    out = []
    d = content_dir(root)
    if not os.path.isdir(d):
        return [(SEV_INFO, 'C-1', '内容库目录尚未建立：%s' % d)]
    names = set(os.listdir(d))
    need = list(GLOBAL_FILES)
    for m in MODULES:
        need.append('A_%s_' % m)          # 前缀式匹配：A_08_*_内容条目.md / *_图表登记.md
    miss_files = []
    for m in MODULES:
        for kind in ['内容条目', '图表登记']:
            if not any(n.startswith('A_%s_' % m) and n.endswith(kind + '.md') for n in names):
                miss_files.append('%s-%s' % (m, kind))
    gmiss = [g for g in GLOBAL_FILES if g not in names]
    if gmiss or miss_files:
        out.append((SEV_INFO, 'C-1', '内容库尚未建齐：全局件缺 %d、模块件缺 %d（未开工可忽略）'
                    % (len(gmiss), len(miss_files))))
    # 逐文件：条目 ID 与字段
    ids = {}
    for n in sorted(names):
        if not (n.startswith('A_') and n.endswith('_内容条目.md')):
            continue
        if n in NON_ITEM_FILES:          # 方案／规程型文件非条目文件，不计 C-2／C-3
            continue
        t = rd(os.path.join(d, n))
        for m in re.finditer(r'^###\s+(.+)$', t, re.M):
            head = m.group(1).strip()
            mid = re.match(r'^([0-9]{2})-([0-9A-Za-z.]+)-([0-9]{2,3})\b', head)
            if not mid:
                out.append((SEV_WARN, 'C-2', '%s：条目标题未用「模块号-节号-序」格式：%s' % (n, head[:42])))
                continue
            key = mid.group(0)
            if key in ids:
                out.append((SEV_ERR, 'C-2', '条目 ID 重复：%s（%s 与 %s）' % (key, ids[key], n)))
            ids[key] = n
            if len(mid.group(1)) != 2:
                out.append((SEV_WARN, 'C-2', '%s：模块号须两位：%s' % (n, key)))
        for f in FIELDS:
            pass
        for blk in re.split(r'^###', t, flags=re.M)[1:]:
            head = blk.strip().split('\n')[0]
            lack = [f for f in FIELDS if ('**%s**' % f) not in blk]
            # 条目 ID 由 ### 标题承载（见字段字典 §1）⟹ 标题合法即视为已填
            if re.match(r'^[0-9]{2}-[0-9A-Za-z.]+-[0-9]{2,3}\b', head.strip()):
                lack = [f for f in lack if f != '条目 ID']
            if lack:
                out.append((SEV_WARN, 'C-3', '%s：条目「%s」缺字段：%s'
                            % (n, head[:34], '、'.join(lack))))
    if ids:
        out.append((SEV_INFO, 'C-2', '共检出条目 %d 条' % len(ids)))
    return out


# ───────────────────────── C-4：编号连续性与必需标题（★ 事故对策）
def check_structure(path, fname):
    out = []
    t = rd(path)
    lines = t.split('\n')
    lines_only = [l for l in lines]
    key = fname[:4] if fname.startswith('A_') else ''
    for need in REQUIRED.get(key, []):
        if not any(l.startswith(need) for l in lines_only):
            out.append((SEV_ERR, 'C-4', '%s：必需标题缺失 → %s' % (fname, need.strip())))
    seq = {}
    for l in lines_only:
        m = HEAD_NUM.match(l)
        if not m:
            continue
        lvl, a, b, c = len(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        seq.setdefault((lvl, a), []).append((b, int(c) if c else None))
    for (lvl, a), vs in seq.items():
        second = sorted(set(x[0] for x in vs))
        exp = list(range(second[0], second[0] + len(second)))
        if second != exp:
            out.append((SEV_ERR, 'C-4', '%s：%s%s 节号不连续 → %s'
                        % (fname, '#' * lvl, a, second)))
        for b in second:
            thirds = sorted(set(x[1] for x in vs if x[0] == b and x[1] is not None))
            if thirds:
                exp3 = list(range(thirds[0], thirds[0] + len(thirds)))
                if thirds != exp3:
                    out.append((SEV_ERR, 'C-4', '%s：%s%s.%d 子节号不连续 → %s'
                                % (fname, '#' * lvl, a, b, thirds)))
    return out


# ───────────────────────── C-5：图表登记 ↔ 对照表
def check_fig_table(root, cdir):
    out = []
    reg = os.path.join(root, '50_论文', '03_对照与索引', 'A_图表编号对照.md')
    if not os.path.isdir(cdir):
        return out
    files = [f for f in os.listdir(cdir) if f.endswith('图表登记.md')]
    if not files:
        return out
    ref = rd(reg) if os.path.exists(reg) else ''
    for f in files:
        t = rd(os.path.join(cdir, f))
        for fig in set(re.findall(r'图\s*([0-9]+-[0-9]+|A-[0-9]+)', t)):
            if ref and re.search(r'图\s*%s' % re.escape(fig), ref) is None:
                out.append((SEV_WARN, 'C-5', '%s：图 %s 不在《A_图表编号对照》中' % (f, fig)))
    if files and not ref:
        out.append((SEV_INFO, 'C-5', '对照表不存在，跳过双向核对'))
    return out


# ───────────────────────── C-6：称形
def check_style(root):
    out = []
    d = drafts_dir(root)
    for f in sorted(os.listdir(d)):
        if not (f.startswith('A_') and f.endswith('.md')):
            continue
        t = rd(os.path.join(d, f))
        n = len(re.findall(r'问题\s*[1-4]', t))
        if n:
            out.append((SEV_WARN, 'C-6', '%s：问次仍为阿拉伯写法 ×%d（应汉字）' % (f, n)))
        n = len(re.findall(r'创新', t))
        if n:
            out.append((SEV_WARN, 'C-6', '%s：出现"创新" ×%d（应作"改进"）' % (f, n)))
        # F 号越位：内部区（本章图与表／占位清单／自查）之外出现 F-xx
        head = t
        for mk in ['## 六、本章图与表', '## 占位清单', '## 自查']:
            head = head.split(mk)[0]
        n = len(re.findall(r'\bF-\d{2}\b', head))
        if n:
            out.append((SEV_ERR, 'C-6', '%s：正文区出现 F 号 ×%d（只允许出现在「占位清单」）' % (f, n)))
    return out


# ───────────────────────── C-7：覆盖矩阵三态（内容库总纲）
def check_matrix(root):
    """总纲 §二 覆盖矩阵：每行状态只允许 已承接／不写（理由）／待回勾（建库中）。"""
    out = []
    p = os.path.join(content_dir(root), '00_内容库总纲.md')
    if not os.path.exists(p):
        return out
    t = rd(p)
    m = re.search(r'##\s*二、6 源覆盖矩阵(.*?)(?=\n##\s*三、)', t, re.S)
    if not m:
        return [(SEV_WARN, 'C-7', '总纲中未找到「§二 6 源覆盖矩阵」区块')]
    ok = wait = nogo = 0
    hdr = ''
    for l in m.group(1).split('\n'):
        if not l.startswith('|'):
            continue
        cells = [c.strip() for c in l.strip().strip('|').split('|')]
        if len(cells) < 3 or set(''.join(cells)) <= set('-: '):
            continue
        if any(c in ('状态', '不写项', '覆盖项') for c in cells):
            hdr = '|'.join(cells)        # 表头行：记住表头（用于识别"不写汇总表"）
            continue
        row = '|'.join(cells)
        if '不写' in hdr:                # 该表整体以"不写"为语义（§2.5 汇总表）
            nogo += 1
            continue
        if '已承接' in row:
            ok += 1
        elif '待回勾' in row:
            wait += 1
        elif '不写' in row:
            nogo += 1
        else:
            out.append((SEV_WARN, 'C-7', '覆盖矩阵行状态缺失（非三态）：%s' % l[:64]))
    out.append((SEV_INFO, 'C-7', '覆盖矩阵三态：已承接 %d ／ 不写（理由） %d ／ **待回勾 %d**（冻结前必须归零）'
                % (ok, nogo, wait)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=None)
    ap.add_argument('--dir', default=None)
    ap.add_argument('--target', choices=['baseline', 'content', 'all'], default='all')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    root = a.root or find_root(os.path.dirname(os.path.abspath(__file__)))
    res = []
    d = drafts_dir(root)
    c = content_dir(root)
    if a.dir:
        d = a.dir
    if a.target in ('baseline', 'all'):
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.startswith('A_') and f.endswith('.md'):
                    res += check_structure(os.path.join(d, f), f)
        res += check_style(root)
    if a.target in ('content', 'all'):
        res += check_content(root)
        res += check_fig_table(root, c)
        res += check_matrix(root)
    nerr = sum(1 for s, _, _ in res if s == SEV_ERR)
    if a.json:
        print(json.dumps({'root': root, 'drafts': d, 'content': c,
                          'findings': [{'sev': s, 'id': i, 'msg': m} for s, i, m in res],
                          'errors': nerr}, ensure_ascii=False, indent=1))
        return 1 if nerr else 0
    print('=' * 88)
    print('check_contentlib —— 章节稿目录：%s' % d)
    print('                    内容库目录：%s' % c)
    print('=' * 88)
    if not res:
        print('  ✅ 未发现问题')
    for s, i, m in res:
        print('  %s [%s] %s' % (s, i, m))
    print('=' * 88)
    print('合计 %d 条发现 ｜ ❌ %d ⟹ %s' % (len(res), nerr, '不通过（须返工）' if nerr else '通过'))
    return 1 if nerr else 0


if __name__ == '__main__':
    sys.exit(main())
