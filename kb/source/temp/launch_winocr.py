# -*- coding: utf-8 -*-
"""后台并行拉起 Windows 内置 OCR（多分片进程），立即返回。"""
import os
import sys
import subprocess

TMP = os.path.dirname(os.path.abspath(__file__))
SHARDS = int(sys.argv[1]) if len(sys.argv) > 1 else 4

for i in range(SHARDS):
    log = os.path.join(TMP, "winocr_%d.log" % i)
    err = os.path.join(TMP, "winocr_%d.err.log" % i)
    fo = open(log, "wb")
    fe = open(err, "wb")
    subprocess.Popen(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", os.path.join(TMP, "winocr.ps1"),
         "-Shard", str(i), "-Shards", str(SHARDS)],
        stdout=fo, stderr=fe, cwd=TMP)
    print("launched shard %d" % i)
