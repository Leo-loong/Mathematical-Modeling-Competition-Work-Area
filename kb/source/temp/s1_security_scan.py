# -*- coding: utf-8 -*-
"""s1_security_scan.py -- “第二批”安全扫描：找出可执行程序与含可执行程序的压缩包。
命中项移入 kb/source/temp/第二批_软件隔离_20260910/ 交用户处理，不解压、不删除。

用法：
  python s1_security_scan.py           # 演练
  python s1_security_scan.py --apply   # 实际移动
"""
import os
import re
import csv
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(HERE)
TARGET = os.path.join(SOURCE, "第二批")
OUT = os.path.join(HERE, "第二批_软件隔离_20260910")

APPLY = "--apply" in sys.argv

EXEC_EXTS = {".exe", ".msi", ".msu", ".bat", ".cmd", ".com", ".scr", ".pif",
             ".appx", ".msix", ".appinstaller", ".jar", ".apk", ".dmg", ".pkg",
             ".deb", ".rpm", ".run", ".bin"}
BIN_EXTS = {".dll", ".lib", ".ocx", ".sys", ".drv", ".vxd", ".so", ".a", ".dylib"}
ARCH_EXTS = {".zip", ".rar", ".7z", ".iso"}
NAME_PAT = re.compile(
    r"(setup|install|installer|crack|keygen|patch|激活|注册机|破解|"
    r"免安装|绿化|安装包|驱动|driver|serial)", re.I)


def entries_of(path, ext):
    try:
        if ext == ".zip":
            with zipfile.ZipFile(path) as z:
                return [i.filename for i in z.infolist()]
        if ext == ".rar":
            import rarfile
            with rarfile.RarFile(path) as rf:
                return [i.filename for i in rf.infolist()]
    except Exception as e:
        return None
    return None


def main():
    loose, soft, unknown, normal = [], [], [], []
    for dirpath, dirnames, filenames in os.walk(TARGET):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, TARGET)
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXEC_EXTS or ext in BIN_EXTS:
                loose.append((rel, "散落可执行/程序二进制 (%s)" % (ext or "?")))
                continue
            if ext in NAME_PAT.pattern and False:
                pass
            if ext in ARCH_EXTS:
                ents = entries_of(full, ext)
                if ents is None:
                    unknown.append((rel, "无法列目录"))
                    continue
                ex = [e for e in ents if os.path.splitext(e)[1].lower() in EXEC_EXTS]
                bn = [e for e in ents if os.path.splitext(e)[1].lower() in BIN_EXTS]
                if ex:
                    soft.append((rel, "含可执行程序 %d 个，如 %s" % (len(ex), ex[0][:90])))
                elif bn:
                    soft.append((rel, "含程序二进制 %d 个，如 %s" % (len(bn), bn[0][:90])))
                elif NAME_PAT.search(fn):
                    soft.append((rel, "文件名疑似安装包/破解包：%s" % NAME_PAT.search(fn).group(0)))
                else:
                    normal.append((rel, "普通资料包（%d 条目）" % len(ents)))

    moved = 0
    failed = []
    if APPLY:
        import shutil
        for rel, why in loose + soft + unknown:
            src = os.path.join(TARGET, rel)
            dst = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.move(src, dst)
                moved += 1
            except OSError as e:
                failed.append((rel, str(e)))

    lines = []
    lines.append("“第二批”安全扫描报告")
    lines.append("=" * 60)
    lines.append("扫描目录 : %s" % TARGET)
    lines.append("隔离目录 : %s" % OUT)
    lines.append("模式     : %s" % ("实际移动 APPLY" if APPLY else "演练 DRY-RUN"))
    lines.append("")
    lines.append("散落可执行文件/程序二进制 : %d" % len(loose))
    lines.append("软件/可执行压缩包         : %d" % len(soft))
    lines.append("无法扫描压缩包(一并隔离)  : %d" % len(unknown))
    lines.append("普通资料包(可安全解压)    : %d" % len(normal))
    lines.append("实际移动                  : %d（失败 %d）" % (moved, len(failed)))
    lines.append("")
    for title, seq in (("散落可执行文件/程序二进制", loose),
                       ("软件/可执行压缩包", soft),
                       ("无法扫描压缩包", unknown)):
        lines.append("--- %s ---" % title)
        for rel, why in seq:
            lines.append("  %s  << %s" % (rel, why))
        lines.append("")

    with open(os.path.join(HERE, "s1_security_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(HERE, "s1_archives.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "relpath", "detail"])
        for rel, why in loose:
            w.writerow(["loose_exec", rel, why])
        for rel, why in soft:
            w.writerow(["software", rel, why])
        for rel, why in unknown:
            w.writerow(["unknown", rel, why])
        for rel, why in normal:
            w.writerow(["normal", rel, why])
    print("OK loose=%d soft=%d unknown=%d normal=%d moved=%d failed=%d"
          % (len(loose), len(soft), len(unknown), len(normal), moved, len(failed)))


if __name__ == "__main__":
    main()
