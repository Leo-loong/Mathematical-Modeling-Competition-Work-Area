# -*- coding: utf-8 -*-
"""验证：部分报错的压缩包是否已经解压出可用文件（tar 末尾报错但内容已释放）。"""
import os
import io
import shutil
import zipfile
import subprocess

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
WORK = os.path.join(os.environ.get("TEMP") or r"C:\Windows\Temp", "kbx_part")

TESTS = [
    r"数学建模国赛速成资料汇总！\国赛A题必备模型+代码资料合集\国赛A题必备：数学建模编程学习\数学建模42种常用算法程序包Matlab版（公众号：数学建模老哥）\程序包：《MATLAB+神经网络43个案例分析》源代码&数据(1)\《MATLAB 神经网络43个案例分析》源代码&数据\chapter15.rar",
    r"数学建模国赛速成资料汇总！\国赛A题必备模型+代码资料合集\国赛A题必备：数学建模编程学习\数学建模42种常用算法程序包Matlab版（公众号：数学建模老哥）\程序包：《MATLAB+神经网络43个案例分析》源代码&数据(1)\《MATLAB 神经网络43个案例分析》源代码&数据\chapter20.rar",
    r"2026数学建模核心资料\国赛B题必备模型+代码资料合集\国赛B题必备优化模型——混合整数规划\Matlab工具包混合整数规划\Mixed Integer Linear Program\lp_solve_3.0.tar.gz",
]

out = []
for i, rel in enumerate(TESTS):
    p = os.path.join(B2, rel)
    w = os.path.join(WORK, "t%d" % i)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(os.path.join(w, "out"), exist_ok=True)
    ext = os.path.splitext(p)[1].lower()
    if not os.path.exists(p):
        out.append("MISSING %s" % rel)
        continue
    shutil.copy2(p, os.path.join(w, "in" + ext))
    pr = subprocess.run(["tar", "-xf", os.path.join(w, "in" + ext),
                         "-C", os.path.join(w, "out")],
                        capture_output=True, text=True, errors="replace")
    n = sum(len(f) for _d, _u, f in os.walk(os.path.join(w, "out")))
    out.append("[%s] rc=%d 解压出 %d 个文件" % (os.path.basename(rel)[:30], pr.returncode, n))
    if n:
        for root, dirs, files in os.walk(os.path.join(w, "out")):
            for f in files[:5]:
                out.append("      " + os.path.relpath(os.path.join(root, f), os.path.join(w, "out")))
            break

    # 对 tar.gz 额外尝试 Python tarfile
    if ext in (".gz", ".tgz", ".tar"):
        try:
            import tarfile
            with tarfile.open(p) as tf:
                members = tf.getmembers()
                out.append("      python-tarfile 可读: %d 项" % len(members))
        except Exception as e:
            out.append("      python-tarfile 失败: %r" % (e,))

with io.open(r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp\partial_test.txt",
             "w", encoding="utf-8") as fp:
    fp.write("\n".join(out))
print("\n".join(out))
