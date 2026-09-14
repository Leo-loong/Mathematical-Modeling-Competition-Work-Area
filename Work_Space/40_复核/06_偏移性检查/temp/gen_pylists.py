# -*- coding: utf-8 -*-
"""从附录 B 实际嵌入的源程序里**自动抽取**：函数/类名、全大写常量、import 的模块别名。

产物：`交付排版方论文/pylists.tex`（供 preamble `\input`，勿手改；改代码后重跑本脚本即可）。
"""
import os, re, io, collections

ROOT = r'c:\Users\wang-\Desktop\2026数学建模\Work_Space'
DELIV = os.path.join(ROOT, '50_论文', '04_交排版成图方', '交付排版方论文')
TEX = os.path.join(DELIV, 'sections', '10_附录.tex')

src = io.open(TEX, encoding='utf-8', errors='ignore').read()
files = re.findall(r'\\srcfile\{([^}]*)\}', src)
print('附录 B 实际嵌入的源程序 = %d 个' % len(files))

code_root = os.path.join(DELIV, 'code')
funcs, consts, mods = collections.Counter(), collections.Counter(), collections.Counter()
missing = 0
for fn in files:
    p = os.path.join(code_root, fn)
    if not os.path.isfile(p):
        missing += 1
        continue
    t = io.open(p, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'(?m)^\s*(?:def|class)\s+(\w+)', t):
        funcs[m.group(1)] += 1
    for m in re.finditer(r'(?m)^([A-Z][A-Z0-9_]{1,})\s*=', t):
        consts[m.group(1)] += 1
    for m in re.finditer(r'(?m)^\s*import\s+([\w\.]+)(?:\s+as\s+(\w+))?', t):
        mods[(m.group(2) or m.group(1).split('.')[0])] += 1
    for m in re.finditer(r'(?m)^\s*from\s+([\w\.]+)\s+import\s+(.+)', t):
        mods[m.group(1).split('.')[0]] += 1

print('抽取结果（去重）：函数/类 %d ｜ 大写常量 %d ｜ 模块别名 %d ｜ 缺文件 %d'
      % (len(funcs), len(consts), len(mods), missing))
print('   函数例：', ' '.join(f for f, _ in funcs.most_common(12)))
print('   常量例：', ' '.join(f for f, _ in consts.most_common(12)))
print('   模块例：', ' '.join(f for f, _ in mods.most_common(12)))

BUILTIN = ['abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'float', 'int', 'len', 'list', 'max', 'min',
           'open', 'print', 'range', 'round', 'set', 'sorted', 'str', 'sum', 'tuple', 'zip', 'isinstance',
           'super', 'staticmethod', 'classmethod', 'property', 'Exception', 'ValueError', 'TypeError']


def lst(items, cap=None):
    items = list(items)
    if cap:
        items = items[:cap]
    return ','.join(items)


fn_list = lst([f for f, _ in funcs.most_common()], 260)
const_list = lst([c for c, _ in consts.most_common()], 120)
mod_list = lst(sorted(set(list(mods) + BUILTIN)))

out = io.open(os.path.join(DELIV, 'pylists.tex'), 'w', encoding='utf-8')
out.write(r'''% ============================================================================
% 本文件由 `40_复核/06_偏移性检查/temp/gen_pylists.py` **自动生成**（勿手改）；
% 内容＝从附录 B 实际嵌入的源程序里抽取的**函数/类名、全大写常量、import 模块别名**，
% 供 `preamble.tex` 的 `\lstdefinestyle{pycode}` 做"IDE 式"识别着色。
% 代码改动后重跑该脚本即可刷新（本文件缺失时 preamble 会自动退回基础样式，不会编译失败）。
% ============================================================================
\definecolor{pyfn}{HTML}{795E26}    % 函数/方法名（VS Code Light+ 的函数色）
\definecolor{pyid}{HTML}{001080}    % 普通标识符（≈变量；VS Code 变量色）
\definecolor{pynum}{HTML}{098658}   % 数字字面量（VS Code 数字色）
\lstdefinestyle{pycode}{%
  language=Python,%
  basicstyle=\lstmonofam\scriptsize,%
  keywordstyle=\color{pykw}\bfseries,%
  stringstyle=\color{pystr},%
  commentstyle=\color{pycmt},%
  identifierstyle=\color{pyid},%
  emphstyle={[1]\color{pyfn}},%
  emphstyle={[2]\color{pyfn!75!black}},%
  emphstyle={[3]\color{pynum!85!black}},%
''')
out.write('  emph={[1]' + fn_list + '},%\n')
out.write('  emph={[2]' + const_list + '},%\n')
out.write('  emph={[3]' + mod_list + '},%\n')
digits = ' '.join('{%d}{{\\color{pynum}\\char"%02X}}1' % (i, 0x30 + i) for i in range(10))
out.write('  literate=' + digits + ',%\n')
out.write(r'''  showstringspaces=false,%
  breaklines=true,%
  extendedchars=true,%
  columns=fullflexible,%
  keepspaces=true,%
}
''')
out.close()
print('已写出：', os.path.join(DELIV, 'pylists.tex'))
