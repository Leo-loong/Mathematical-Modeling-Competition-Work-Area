# -*- coding: utf-8 -*-
"""后台执行压缩包解压整理，立即返回。"""
import os
import sys
import subprocess

TMP = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ)
env["PYTHONUTF8"] = "1"
log = os.path.join(TMP, "extract_stdout.log")
fo = open(log, "wb")
subprocess.Popen(
    [sys.executable, os.path.join(TMP, "extract_all.py"), "2"],
    stdout=fo, stderr=fo, env=env, cwd=TMP, creationflags=0x00000008)
print("launched extract")
