# -*- coding: utf-8 -*-
"""测试各种解压后端对 rar / zip 的支持情况（Python 调用，避免终端编码问题）。"""
import os
import sys
import glob
import zipfile
import subprocess
import tempfile

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
OUT = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp\extract_test"

SKIP_DIR = "数学建模国赛速成资料汇总"


def find(ext, n=2):
    res = []
    for dp, _dn, fn in os.walk(B2):
        if SKIP_DIR in dp:
            continue
        for f in fn:
            if f.lower().endswith(ext):
                res.append(os.path.join(dp, f))
    return res[:n]


def try_tar(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = subprocess.run(["tar", "-xf", path, "-C", outdir],
                       capture_output=True, text=True, errors="replace")
    n = sum(len(f) for _d, _u, f in os.walk(outdir))
    return p.returncode, n, (p.stderr or "")[:200]


def try_zipfile(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for nm in names:
            # 修正 GBK 编码的中文文件名
            try:
                real = nm.encode("cp437").decode("gbk")
            except Exception:
                real = nm
            tgt = os.path.join(outdir, real)
            if real.endswith("/"):
                os.makedirs(tgt, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            try:
                with z.open(nm) as src, open(tgt, "wb") as dst:
                    dst.write(src.read())
            except Exception:
                pass
    n = sum(len(f) for _d, _u, f in os.walk(outdir))
    return 0, n, ""


log = []
for ext, func in ((".rar", try_tar), (".zip", try_tar), (".zip", try_zipfile)):
    files = find(ext)
    for f in files:
        tag = os.path.basename(f)[:40]
        outdir = os.path.join(OUT, "%s_%s" % (func.__name__, os.path.splitext(os.path.basename(f))[0][:20]))
        try:
            rc, n, err = func(f, outdir)
            log.append("[%s] %s -> rc=%d files=%d %s" % (func.__name__, tag, rc, n, err))
        except Exception as e:
            log.append("[%s] %s -> EXC %r" % (func.__name__, tag, e))

with open(os.path.join(os.path.dirname(OUT), "extract_test.txt"), "w", encoding="utf-8") as fp:
    fp.write("\n".join(log))
print("\n".join(log))
