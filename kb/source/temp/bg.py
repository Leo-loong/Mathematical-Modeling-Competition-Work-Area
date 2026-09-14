# -*- coding: utf-8 -*-
"""通用「无窗口后台启动器」——替代此前会弹出 cmd 窗口的做法。

用法:
  python bg.py <脚本.py> [参数...]

要点（避免弹 cmd 窗口）：
  1. 优先用 pythonw.exe（GUI 子系统，系统不分配控制台）
  2. 同时传 CREATE_NO_WINDOW(0x08000000) | DETACHED_PROCESS(0x8)
  3. stdout/stderr 重定向到日志文件
"""
import os
import sys
import subprocess

TMP = os.path.dirname(os.path.abspath(__file__))
CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008


def launch(script, args=None, logname=None):
    args = args or []
    py = sys.executable
    pyw = py.replace("python.exe", "pythonw.exe")
    if os.path.exists(pyw):
        py = pyw
    log = os.path.join(TMP, logname or (os.path.splitext(os.path.basename(script))[0] + ".log"))
    fo = open(log, "wb")
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.Popen(
        [py, os.path.join(TMP, script)] + [str(a) for a in args],
        stdout=fo, stderr=fo, stdin=subprocess.DEVNULL,
        env=env, cwd=TMP,
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS)
    return proc.pid, log


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python bg.py <script.py> [args...]")
        sys.exit(1)
    pid, log = launch(sys.argv[1], sys.argv[2:])
    print("launched pid=%d log=%s" % (pid, log))
