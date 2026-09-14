# -*- coding: utf-8 -*-
"""
一键复现调度器（**默认只打印计划，不执行任何计算**）
================================================================
用法：
    python run_all.py            # T0：打印复现计划（脚本清单＋说明），不运行
    python run_all.py --go       # 执行：按序运行全部求解/检验脚本（**须先取得《工作约束》§12 授权**）

设计说明：
  · 本脚本只做**按序调度**，不改变任何被测脚本的行为；各脚本自建日志（见 `README_日志索引.md`）
  · 被测脚本自身遵守 §12 脚本闸门：**默认打印 `[SCALE]` 规模声明后退出**，须显式传 `--go` 才真正计算
    ⟹ 本调度器在 `--go` 模式下会**把 `--go` 透传**给每个脚本
  · 依赖：同目录 `requirements.txt`（`pip install -r requirements.txt`）
  · 运行环境：Python 3；不写任何交付数值，结果文件由各脚本自行产出
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, 'code')


def discover():
    """按问序号收集求解、检验与创新脚本（**递归含 `innov/`**；不改写、不猜测文件名）。

    仅收录以 `q1_`–`q4_` 开头的题目脚本；公共库／非入口模块按下表排除，
    避免把"被 import 的库"当程序跑（如 `*_lib`／`*_par`／`*core*`／`*_base`）。
    """
    solvers = sorted(glob.glob(os.path.join(CODE, 'q[1-4]_solver.py')))
    NON_ENTRY = ('_lib', '_par', 'core', 'exact', '_base', '_invbase', '_aux_lib')
    checks, innos = [], []
    for p in sorted(glob.glob(os.path.join(CODE, '**', '*.py'), recursive=True)):
        if p in solvers:
            continue
        b = os.path.basename(p)
        if not b.startswith(('q1_', 'q2_', 'q3_', 'q4_')):
            continue
        if any(s in b for s in NON_ENTRY):
            continue
        rel = os.path.relpath(p, CODE).replace(os.sep, '/')
        (innos if 'innov/' in rel else checks).append(p)
    seen, plan = set(), []
    for p in solvers + checks + innos:
        if p not in seen:
            seen.add(p)
            plan.append(p)
    return solvers, [p for p in plan if p not in solvers and p not in innos], innos


def usage():
    """打印用法与覆盖范围（`-h`／`--help`）。"""
    print('用法：')
    print('  python run_all.py          # 打印复现计划（不执行任何计算）')
    print('  python run_all.py --go     # 按序执行全部脚本（求解 ＋ 检验 ＋ 创新）')
    print('  python run_all.py -h       # 显示本帮助')
    print('')
    print('覆盖范围：由目录扫描递归得出，含 code/innov/；')
    print('公共库／非入口模块（*_lib／*_par／*core*／*exact* 等）自动排除。')
    print('被测脚本自身遵守规模闸门（默认只打印 [SCALE] 后退出），本调度器会透传 --go。')
    print('跨平台：Windows／macOS／Linux 均可（Python 3.9＋）；无 python 命令时用 python3。')


HELP_FLAGS = ('-h', '--help', '-help', '/?', '-?')
KNOWN_FLAGS = ('--go',)


def main():
    argv = sys.argv[1:]
    if any(a in argv for a in HELP_FLAGS):
        usage()
        return 0
    unknown = [a for a in argv if a not in KNOWN_FLAGS]
    if unknown:
        print('未知参数：%s' % ' '.join(unknown))
        print('（查看用法：python run_all.py -h）\n')
        usage()
        return 2
    go = '--go' in argv
    solvers, checks, innos = discover()
    print('[SCALE] run_all 复现计划：求解 %d 个 ＋ 检验/诊断 %d 个 ＋ 创新 %d 个（共 %d 个脚本）'
          % (len(solvers), len(checks), len(innos), len(solvers) + len(checks) + len(innos)))
    print('[SCALE] 作用域：仅调度现有脚本；不产生新数值；不修改任何交付文件')
    print('-' * 68)
    print('① 求解（主力结果 result1–4.xlsx）')
    for p in solvers:
        print('   -', os.path.basename(p))
    print('② 检验／诊断（日志落 code/…/logs 或本目录 *.txt）')
    for p in checks:
        print('   -', os.path.basename(p))
    if innos:
        print('③ 创新／拓展（code/innov/，不进入交付数值）')
        for p in innos:
            print('   -', os.path.relpath(p, CODE).replace(os.sep, '/'))
    print('-' * 68)
    print('提示：预计墙钟见《A_代码复现.md》与 `README_日志索引.md`；Q4 主求解约 8 min，全量检验合计约 1 h 量级。')
    if not go:
        print('\n【dry-run】未执行任何脚本。确认授权后加 `--go` 运行：python run_all.py --go')
        return 0
    print('\n【执行模式】按序运行（Ctrl+C 可中断）……\n')
    allp = solvers + checks + innos
    for i, p in enumerate(allp, 1):
        print('[%d/%d] %s' % (i, len(allp), os.path.relpath(p, CODE).replace(os.sep, '/')), flush=True)
        rc = subprocess.call([sys.executable, p, '--go'], cwd=os.path.dirname(p))
        print('    → 退出码 %d' % rc, flush=True)
        if rc != 0:
            print('    ⚠ 该脚本非零退出；按《工作约束》§12.9 如实记录后再决定是否继续。')
    print('\n完成。请对照《A_数值口径总表》与各问《结果与分析》核对复现一致性。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
