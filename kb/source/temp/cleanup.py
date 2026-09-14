# -*- coding: utf-8 -*-
"""清理调试中间文件，保留核心脚本与最终报告。"""
import os
import shutil

TMP = os.path.dirname(os.path.abspath(__file__))
KEEP_FILES = {
    "docx_core.py", "pdf_core.py", "convert_all.py", "ocr_tsv_to_md.py",
    "render_pages.py", "winocr.ps1", "launch_winocr.py", "final_check.py",
    "最终核对报告.txt", "转换说明.md", "cleanup.py",
}
KEEP_DIRS = {"ocr_tsv"}

removed = 0
freed = 0
for name in os.listdir(TMP):
    p = os.path.join(TMP, name)
    if name in KEEP_FILES or name in KEEP_DIRS:
        continue
    try:
        if os.path.isdir(p):
            freed += sum(os.path.getsize(os.path.join(dp, f))
                         for dp, _dn, fn in os.walk(p) for f in fn)
            shutil.rmtree(p)
        else:
            freed += os.path.getsize(p)
            os.remove(p)
        removed += 1
    except Exception:
        pass
print("removed %d items, freed %.1f MB" % (removed, freed / 1048576.0))
print("kept: %s" % ", ".join(sorted(os.listdir(TMP))))
