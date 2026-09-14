# -*- coding: utf-8 -*-
"""隔离被 Defender 点名的带毒压缩包（软件安装包类，非建模资料），并触发官方扫描。"""
import os
import io
import shutil

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
QUAR = os.path.join(os.path.dirname(B2), "第二批_可疑可执行文件隔离")
TARGETS = ["yaahp", "Graph安装包", "AHP层次分析法软件", "灰色关联分析软件"]
ARCH_EXT = {".zip", ".rar", ".7z", ".exe", ".msi"}

log = []
moved = 0
for dp, _dn, fn in os.walk(B2):
    for f in fn:
        if os.path.splitext(f)[1].lower() not in ARCH_EXT:
            continue
        if not any(k in f for k in TARGETS):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, B2)
        dst = os.path.join(QUAR, rel)
        if os.path.exists(dst):
            root, ext = os.path.splitext(dst)
            i = 1
            while os.path.exists("%s__%d%s" % (root, i, ext)):
                i += 1
            dst = "%s__%d%s" % (root, i, ext)
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(p, dst)
            moved += 1
            log.append("[隔离] " + rel)
        except Exception as e:
            log.append("[失败] %s %r" % (rel, e))

with io.open(os.path.join(os.path.dirname(B2), "temp", "带毒压缩包隔离.txt"),
             "w", encoding="utf-8") as fp:
    fp.write("隔离 %d 个\n%s" % (moved, "\n".join(log)))
print("QUARANTINED %d" % moved)
