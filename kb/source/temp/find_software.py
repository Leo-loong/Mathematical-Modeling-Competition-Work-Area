# -*- coding: utf-8 -*-
"""统计（可选删除）软件类打包文件。

判定：压缩包/安装包类扩展名 且 文件名命中软件关键词。
"""
import os
import io
import sys

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
QUAR_EXEC = os.path.join(os.path.dirname(B2), "第二批_可疑可执行文件隔离")
PKG_EXT = {".zip", ".rar", ".7z", ".exe", ".msi", ".iso", ".tar", ".gz",
           ".dmg", ".apk", ".bin"}
KEYWORDS = ["软件", "安装包", "安装程序", "绿色版", "破解", "注册机", "激活",
            "汉化", "setup", "Setup", "SETUP", "install", "Install",
            "crack", "Crack", "patch", "keygen", "yaahp", "YAHP", "Graph",
            "SPSS", "Lingo", "MATLAB", "Origin", "Visio", "AxGlyph",
            "MathType", "ArcGIS", "EndNote", "Photoshop"]


def scan(root, tag):
    hits = []
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            ext = os.path.splitext(f)[1].lower()
            if ext not in PKG_EXT:
                continue
            if any(k in f for k in KEYWORDS):
                hits.append((tag, os.path.join(dp, f)))
    return hits


def main():
    do_delete = "--delete" in sys.argv
    hits = scan(B2, "第二批")
    hits += scan(QUAR_EXEC, "隔离区")
    lines = ["匹配到软件类打包文件: %d 个" % len(hits), ""]
    for tag, p in hits:
        try:
            sz = os.path.getsize(p)
        except Exception:
            sz = -1
        lines.append("%8d  [%s] %s" % (sz, tag, os.path.relpath(p, os.path.dirname(B2))))
    if do_delete:
        lines.append("")
        ok = fail = 0
        for tag, p in hits:
            try:
                os.remove(p)
                ok += 1
            except Exception as e:
                fail += 1
                lines.append("  删除失败: %s (%r)" % (p, e))
        lines.append("删除结果: 成功 %d, 失败 %d" % (ok, fail))
    with io.open(os.path.join(os.path.dirname(B2), "temp", "软件类文件清单.txt"),
                 "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))
    print("HITS=%d DELETE=%s" % (len(hits), do_delete))


if __name__ == "__main__":
    main()
