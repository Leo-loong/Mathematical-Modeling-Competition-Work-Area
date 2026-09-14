# -*- coding: utf-8 -*-
"""把第二批中的「代码 / 数据 / 演示程序 / 图片」类素材迁移到「第二批提取后」，
保持相对目录结构。

目的：知识库（提取后目录）自包含——Agent 命中后可直接读取代码与数据原文件，
无需再从「第二批」跳转一次索引。

保留在第二批（不迁移）的：.docx/.doc/.pdf/.txt/.html/.htm/.md
  —— 这些是文档原件，作为"原始内容"供 Agent 在提取内容有损时回查。
"""
import os
import io
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "第二批")
DST = os.path.join(BASE, "第二批提取后")
REPORT = os.path.join(BASE, "temp", "素材迁移报告.txt")

KEEP_IN_SRC = {".docx", ".doc", ".pdf", ".txt", ".html", ".htm", ".md"}
# 图片类不迁移：用户明确"可保留但不存入知识库"，且非文本内容不应进入检索目录
IMAGE_EXT = {".bmp", ".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".ico", ".emf", ".wmf"}

log = []


def main():
    moved = 0
    skipped = 0
    failed = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.startswith("~$"):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in KEEP_IN_SRC or ext in IMAGE_EXT:
                skipped += 1
                continue
            src = os.path.join(dp, f)
            rel = os.path.relpath(src, SRC)
            dst = os.path.join(DST, rel)
            if os.path.exists(dst):
                skipped += 1
                continue
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
                moved += 1
            except Exception as e:
                failed.append((rel, repr(e)))
            if moved % 1000 == 0:
                log.append("已迁移 %d" % moved)
    log.append("迁移完成: 移动 %d, 跳过 %d, 失败 %d" % (moved, skipped, len(failed)))
    for rel, err in failed[:30]:
        log.append("  失败: %s  %s" % (rel, err))

    n_src = sum(len(f) for _d, _u, f in os.walk(SRC))
    n_dst = sum(len(f) for _d, _u, f in os.walk(DST))
    log.append("第二批剩余文件: %d" % n_src)
    log.append("第二批提取后文件: %d" % n_dst)
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("MOVED=%d SRC=%d DST=%d" % (moved, n_src, n_dst))


if __name__ == "__main__":
    main()
