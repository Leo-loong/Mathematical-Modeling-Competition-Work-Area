# -*- coding: utf-8 -*-
"""q1_quarantine.py -- 第一步：把“第二批提取后”中不可索引、且 Agent 无法直读的文件隔离。

判定标准（两条同时满足才保留）：
  1) 扩展名属于引擎 TEXT_EXTS（可被全文建立索引）；
  2) 是纯文本，Agent 用 read_file 可直接读取，无需 OCR / 解析。
不满足者一律移入 source\\temp\\<隔离区>（temp 为引擎 NON_CORPUS，不入索引），
不执行 os.remove（环境 safe-delete 保护，见引擎技术文档 1.2-6）。

用法：
  python q1_quarantine.py            # 演练：只出清单，不移动
  python q1_quarantine.py --apply    # 实际移动
"""
import os
import sys
import csv
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))          # kb/source/temp
SOURCE = os.path.dirname(HERE)                              # kb/source
KB = os.path.dirname(SOURCE)                                # kb
WORKSPACE = os.path.dirname(KB)

TARGET = os.path.join(SOURCE, "第二批提取后")
STAMP = "20260910"
QUAR = os.path.join(SOURCE, "temp", "第二批提取后_不合格_" + STAMP)

# 引擎 p3_meta.py / p1_scan.py 的可索引扩展名（并集）
TEXT_EXTS = {".md", ".m", ".M", ".py", ".c", ".h", ".cpp", ".txt", ".html",
             ".csv", ".json", ".cls", ".bst", ".bib", ".dat", ".sas", ".sty"}
# 引擎已声明跳过的目录
EXCLUDE_DIRS = {"_无效内容"}
NON_CORPUS = {"temp"}

APPLY = "--apply" in sys.argv
# --keep-unlisted-text: 检出为纯文本但扩展名未收录的文件也保留（默认仍隔离）
KEEP_UNLISTED_TEXT = "--keep-unlisted-text" in sys.argv


def sniff_text(path, probe=8192):
    """前 8KB 内无 NUL 且可打印字符占比 >= 0.9 视为纯文本。"""
    try:
        with open(path, "rb") as f:
            b = f.read(probe)
    except OSError:
        return False
    if not b:
        return False
    if b.count(0) > 0:
        return False
    printable = sum(1 for c in b if 32 <= c < 127 or c in (9, 10, 13) or c >= 128)
    return printable / len(b) >= 0.9


def build_origin_names():
    """原始区（第一批/第二批/第一批提取后/教材_转化 等，排除本目录与 temp）文件名索引。"""
    names = set()
    for name in sorted(os.listdir(SOURCE)):
        p = os.path.join(SOURCE, name)
        if not os.path.isdir(p) or name in NON_CORPUS:
            continue
        if os.path.abspath(p) == os.path.abspath(TARGET):
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fn in filenames:
                names.add(fn.lower())
    return names


def main():
    origin = build_origin_names()
    rows = []          # (relpath, ext, size, reason, has_origin)
    keep = 0
    for dirpath, dirnames, filenames in os.walk(TARGET):
        dirnames[:] = [d for d in dirnames if d != "temp"]
        rel_dir = os.path.relpath(dirpath, TARGET)
        top = rel_dir.split(os.sep)[0] if rel_dir != "." else ""
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, TARGET)
            ext = os.path.splitext(fn)[1].lower()
            try:
                size = os.path.getsize(full)
            except OSError:
                size = -1
            if top in EXCLUDE_DIRS:
                reason = "已标记_无效内容"
            elif rel_dir == "." and fn.startswith("_"):
                reason = "本目录自建产物"
            elif ext == "":
                reason = "无扩展名_不可索引" + ("_文本" if sniff_text(full) else "")
            elif ext not in TEXT_EXTS:
                reason = ("纯文本_扩展名未收录" if sniff_text(full)
                          else "二进制_不可索引不可直读")
            else:
                keep += 1
                continue
            if KEEP_UNLISTED_TEXT and reason in ("纯文本_扩展名未收录", "无扩展名_不可索引_文本"):
                keep += 1
                continue
            rows.append((rel, ext, size, reason, fn.lower() in origin))

    # 演练：先落清单
    man = os.path.join(HERE, "q1_manifest.csv")
    with open(man, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["relpath", "ext", "size", "reason", "has_origin"])
        for r in rows:
            w.writerow([r[0], r[1], r[2], r[3], "Y" if r[4] else "N"])

    moved = failed = 0
    if APPLY:
        for rel, ext, size, reason, has_origin in rows:
            src = os.path.join(TARGET, rel)
            dst = os.path.join(QUAR, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                stem, e = os.path.splitext(dst)
                i = 1
                while os.path.exists("%s__dup%d%s" % (stem, i, e)):
                    i += 1
                dst = "%s__dup%d%s" % (stem, i, e)
            try:
                shutil.move(src, dst)
                moved += 1
            except OSError as ex:
                failed += 1
                with open(os.path.join(HERE, "q1_move_errors.txt"), "a", encoding="utf-8") as ef:
                    ef.write("%s\t%s\n" % (rel, ex))
        # 清理空目录（失败静默跳过）
        removed_dirs = 0
        for dirpath, dirnames, filenames in os.walk(TARGET, topdown=False):
            if os.path.abspath(dirpath) == os.path.abspath(TARGET):
                continue
            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
                    removed_dirs += 1
            except OSError:
                pass
    else:
        removed_dirs = 0

    # 统计
    by_ext = {}
    by_reason = {}
    no_origin = []
    for rel, ext, size, reason, has_origin in rows:
        by_ext[ext or "(无扩展名)"] = by_ext.get(ext or "(无扩展名)", 0) + 1
        by_reason[reason] = by_reason.get(reason, 0) + 1
        if not has_origin:
            no_origin.append(rel)

    lines = []
    lines.append("第一步：不合格文件隔离报告")
    lines.append("=" * 60)
    lines.append("目标目录 : %s" % TARGET)
    lines.append("隔离区   : %s" % QUAR)
    lines.append("模式     : %s" % ("实际移动 APPLY" if APPLY else "演练 DRY-RUN"))
    lines.append("")
    lines.append("保留(可索引且可直读) : %d" % keep)
    lines.append("隔离(不合格)         : %d" % len(rows))
    lines.append("实际移动成功         : %d" % moved)
    lines.append("移动失败             : %d" % failed)
    lines.append("清理空目录           : %d" % removed_dirs)
    lines.append("")
    lines.append("--- 隔离原因分布 ---")
    for k, v in sorted(by_reason.items(), key=lambda x: -x[1]):
        lines.append("  %-24s %d" % (k, v))
    lines.append("")
    lines.append("--- 隔离文件扩展名分布 ---")
    for k, v in sorted(by_ext.items(), key=lambda x: -x[1]):
        lines.append("  %-14s %d" % (k, v))
    lines.append("")

    unlisted = {}
    for rel, ext, size, reason, has_origin in rows:
        if reason in ("纯文本_扩展名未收录", "无扩展名_不可索引_文本"):
            unlisted[ext or "(无扩展名)"] = unlisted.get(ext or "(无扩展名)", 0) + 1
    lines.append("--- 检出为纯文本、但扩展名不在 TEXT_EXTS（可考虑加扩展名而非删除）---")
    for k, v in sorted(unlisted.items(), key=lambda x: -x[1]):
        lines.append("  %-14s %d" % (k, v))
    lines.append("  合计 %d" % sum(unlisted.values()))
    lines.append("")
    lines.append("--- 原始区无同名副本（需人工确认，共 %d 个）---" % len(no_origin))
    for rel in no_origin[:400]:
        lines.append("  " + rel)
    if len(no_origin) > 400:
        lines.append("  ... 其余 %d 条见 q1_manifest.csv (has_origin=N)" % (len(no_origin) - 400))
    lines.append("")
    lines.append("清单文件: %s" % man)

    rep = os.path.join(HERE, "q1_report.txt")
    with open(rep, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("OK keep=%d quarantine=%d moved=%d failed=%d" % (keep, len(rows), moved, failed))


if __name__ == "__main__":
    main()
