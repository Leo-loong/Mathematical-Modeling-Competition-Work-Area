# -*- coding: utf-8 -*-
"""把超大文件的完整版 *.full.md 移入 _完整版/ 子目录。
主目录只保留摘要版，避免 Agent 检索时命中超大文件被拖垮；
需要完整内容时按提示读取 _完整版/ 下同名文件。"""
import os
import io
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = [os.path.join(BASE, "第一批提取后"), os.path.join(BASE, "第二批提取后")]
log = []

for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dp, _dn, fn in os.walk(root):
        for f in list(fn):
            if not f.endswith(".full.md"):
                continue
            if "_完整版" in dp:
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root)
            target = os.path.join(root, "_完整版", rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.move(p, target)
            log.append("移动 " + rel)

with io.open(os.path.join(BASE, "temp", "完整版移动记录.txt"),
             "w", encoding="utf-8") as fp:
    fp.write("\n".join(log))
print("MOVED_FULL=%d" % len(log))
