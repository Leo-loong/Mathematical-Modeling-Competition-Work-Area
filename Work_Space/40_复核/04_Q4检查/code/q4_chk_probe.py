# -*- coding: utf-8 -*-
# 用途：Q4 证据链检查·口径取证（只读）
#   Q4 脚本用途 / 熔断常数 / T>env 计数定义 / 预试验脚本行为与依赖
"""执行前取证：脚本用途、熔断常数、T>env 计数口径、预试验脚本行为。"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))


def _find_root(p, _marker="10_赛题", _max=8):
    """向上探测含 10_赛题 的目录作为工作区根（与项目既有脚本同一约定）。"""
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, _marker)):
            return cur
        cur = os.path.dirname(cur)
    raise SystemExit("未找到工作区根")


ROOT = _find_root(HERE)
CODE = os.path.join(ROOT, "20_交付包", "09_代码与复现", "code")
Q4C = os.path.join(ROOT, "11_建模", "11-3_算法与管线", "Q4", "code")


def first_doc(path, n=150):
    try:
        txt = io.open(path, "r", encoding="utf-8", errors="replace").read()
    except OSError:
        return "(读不到)"
    m = re.search(r'"""(.*?)(?:"""|$)', txt, re.S)
    if not m:
        return "(无 docstring)"
    s = " ".join(m.group(1).split())
    return s[:n]


print("=" * 74)
print("[1] 交付包 code/ 下 24 个 q4_*.py 的用途首句")
for fn in sorted(f for f in os.listdir(CODE) if f.startswith("q4_") and f.endswith(".py")):
    print("  %-26s %s" % (fn, first_doc(os.path.join(CODE, fn), 110)))

print()
print("[2] 熔断常数 / 240 / 150 h 的出现处（q4_solver.py + q4_core.py）")
for fn in ("q4_solver.py", "q4_core.py"):
    p = os.path.join(CODE, fn)
    for i, ln in enumerate(io.open(p, "r", encoding="utf-8", errors="replace"), 1):
        if re.search(r"(熔断|fuse|FUSE|3600\s*\*\s*(150|240)|t_max|T_MAX|abort)", ln):
            print("  %s:%d  %s" % (fn, i, ln.rstrip()[:130]))

print()
print("[3] T>env / 140261 计数口径")
for fn in ("q4_solver.py", "q4_core.py"):
    p = os.path.join(CODE, fn)
    for i, ln in enumerate(io.open(p, "r", encoding="utf-8", errors="replace"), 1):
        if re.search(r"(>env|env_max|n_above|above|steps with|140261)", ln):
            print("  %s:%d  %s" % (fn, i, ln.rstrip()[:130]))

print()
print("[4] q4_pretest.py 行为（写哪些文件 / 是否可单跑某一 S）")
p = os.path.join(Q4C, "q4_pretest.py")
for i, ln in enumerate(io.open(p, "r", encoding="utf-8", errors="replace"), 1):
    if re.search(r"(open\(|argv|def run|def S|sys\.argv|LOG|log_path|print\(f?\"?\[S)", ln):
        print("  %d: %s" % (i, ln.rstrip()[:130]))
print()
print("[5] q4_pretest.py 是否 import 交付核 / 只读依赖")
for i, ln in enumerate(io.open(p, "r", encoding="utf-8", errors="replace"), 1):
    if re.match(r"^\s*(import|from)\s", ln):
        print("  %d: %s" % (i, ln.rstrip()[:120]))
print("=" * 74)
