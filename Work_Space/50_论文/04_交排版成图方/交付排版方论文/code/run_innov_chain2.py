# -*- coding: utf-8 -*-
"""Q4 innov 补跑链（INV3 修复版 -> INV4）。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, 'logs')
os.makedirs(LOGS, exist_ok=True)   # 交付副本内该目录可能不存在，先确保存在
os.chdir(HERE)

STEPS = [
    ([sys.executable, 'q4_INV3_global.py', '--go'], 'inv3_stdout.txt'),
    ([sys.executable, 'q4_INV4_aux.py', '--go'], 'inv4_stdout.txt'),
]

for cmd, out in STEPS:
    with open(os.path.join(LOGS, out), 'w', encoding='utf-8') as f:
        f.write('[chain] running %s\n' % ' '.join(cmd))
        f.flush()
        rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=HERE)
    with open(os.path.join(LOGS, out), 'a', encoding='utf-8') as f:
        f.write('[chain] exit=%d\n' % rc)

with open(os.path.join(LOGS, 'innov_chain2_done.txt'), 'w', encoding='utf-8') as f:
    f.write('INNOV CHAIN2 DONE\n')
