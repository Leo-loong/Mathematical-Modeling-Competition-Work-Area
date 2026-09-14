# -*- coding: utf-8 -*-
"""绕过 tar 的中文路径问题：复制到 ASCII 临时路径后解压，验证 tar 是否支持 rar。"""
import os
import shutil
import subprocess

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
WORK = r"C:\Users\wang-\AppData\Local\Temp\kbx"
SKIP = "数学建模国赛速成资料汇总"

os.makedirs(WORK, exist_ok=True)
log = []

# 找两个 rar
files = []
for dp, _dn, fn in os.walk(B2):
    if SKIP in dp:
        continue
    for f in fn:
        if f.lower().endswith(".rar"):
            files.append(os.path.join(dp, f))
log.append("rar count=%d" % len(files))

for i, src in enumerate(files[:2]):
    tmp_in = os.path.join(WORK, "in%d.rar" % i)
    tmp_out = os.path.join(WORK, "out%d" % i)
    shutil.rmtree(tmp_out, ignore_errors=True)
    os.makedirs(tmp_out, exist_ok=True)
    shutil.copy2(src, tmp_in)
    p = subprocess.run(["tar", "-xf", tmp_in, "-C", tmp_out],
                       capture_output=True, text=True, errors="replace")
    n = sum(len(f) for _d, _u, f in os.walk(tmp_out))
    log.append("[%s] size=%d rc=%d files=%d err=%s" % (
        os.path.basename(src)[:30], os.path.getsize(src), p.returncode, n,
        (p.stderr or "")[:150]))
    # 备用：PowerShell Expand-Archive 不支持 rar；尝试 python 的 rarfile
    if n == 0:
        try:
            import rarfile
            log.append("  rarfile available: %s" % rarfile.__name__)
        except Exception as e:
            log.append("  rarfile NOT available: %r" % (e,))

with open(r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp\rar_test.txt",
          "w", encoding="utf-8") as fp:
    fp.write("\n".join(log))
print("\n".join(log))
