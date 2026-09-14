# -*- coding: utf-8 -*-
"""后台扫描第二批 PDF 指纹，立即返回。"""
import os
import sys
import subprocess

TMP = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(TMP), "第二批")
env = dict(os.environ)
env["PYTHONUTF8"] = "1"
log = os.path.join(TMP, "scan_pdf.log")
fo = open(log, "wb")
subprocess.Popen(
    [sys.executable, os.path.join(TMP, "scan_index.py"), SRC, "pdf",
     os.path.join(TMP, "idx_b2_pdf.csv")],
    stdout=fo, stderr=fo, env=env, cwd=TMP, creationflags=0x00000008)
print("launched pdf scan")
