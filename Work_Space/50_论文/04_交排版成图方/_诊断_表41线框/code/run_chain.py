# -*- coding: utf-8 -*-
"""Q4 修复后全链重跑串行启动器（E7b/E8b -> 主求解 -> E5 -> E1）。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# 日志目录：优先 <上级>/logs；交付副本内无该目录时回退到上级目录本身
# （与同目录 rerun_chain.ps1 的语义一致），并确保目录存在
LOGS = os.path.join(HERE, '..', 'logs')
if not os.path.isdir(LOGS):
    LOGS = os.path.dirname(HERE)
os.makedirs(LOGS, exist_ok=True)
os.chdir(HERE)

STEPS = [
    ([sys.executable, 'q4_w6_e78b.py', '--go'], 'rerun_e78b.txt'),
    ([sys.executable, 'q4_solver.py', '--go'], 'rerun_solve.txt'),
    ([sys.executable, 'q4_w6_e5.py', '--go'], 'rerun_e5.txt'),
    ([sys.executable, 'q4_w6_e15.py', 'e1'], 'rerun_e1.txt'),
]

for cmd, out in STEPS:
    with open(os.path.join(LOGS, out), 'w', encoding='utf-8') as f:
        f.write('[chain] running %s\n' % ' '.join(cmd))
        f.flush()
        rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=HERE)
    with open(os.path.join(LOGS, out), 'a', encoding='utf-8') as f:
        f.write('[chain] exit=%d\n' % rc)

with open(os.path.join(LOGS, 'rerun_chain_done.txt'), 'w', encoding='utf-8') as f:
    f.write('CHAIN DONE\n')
