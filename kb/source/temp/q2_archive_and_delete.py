# -*- coding: utf-8 -*-
"""q2_archive_and_delete.py -- 第二步：压缩包安全筛查 + 隔离区清理删除。

规则（用户 2026-09-10 指示）：
  1. 压缩包若含可执行程序（.exe/.msi/.bat/...）或文件名像软件安装包/破解包，
     一律移入 软件压缩包_待用户处理 目录，由用户自行处置（避免解压触发杀软报警）。
  2. “第二批提取后”内其余不合格文件一律直接删除（原件正在重新下载到“第二批”）。
  3. 频繁处理数据源期间不运行 update.py（索引待下载完成后统一重建）。

用法：
  python q2_archive_and_delete.py            # 演练
  python q2_archive_and_delete.py --apply    # 实际执行
"""
import os
import re
import sys
import csv
import zipfile
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
QUAR = os.path.join(HERE, "第二批提取后_不合格_20260910")
SOFT_DIR = os.path.join(HERE, "软件压缩包_待用户处理_20260910")
UNK_DIR = os.path.join(HERE, "无法扫描压缩包_待确认_20260910")

APPLY = "--apply" in sys.argv

ARCH_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".iso"}
# 可执行 / 可安装程序
EXEC_EXTS = {".exe", ".msi", ".msu", ".bat", ".cmd", ".com", ".scr", ".pif",
             ".appx", ".msix", ".appinstaller", ".jar", ".apk", ".dmg", ".pkg",
             ".deb", ".rpm", ".run", ".bin", ".sh"}
# 程序二进制（不可直接运行，但易触发杀软报警，一并交用户处理）
BIN_EXTS = {".dll", ".lib", ".ocx", ".sys", ".drv", ".vxd", ".so", ".a", ".dylib"}
# 安装包 / 破解包 名称特征
NAME_PAT = re.compile(
    r"(setup|install|installer|crack|keygen|patch|激活|注册机|破解|"
    r"免安装|绿化|安装包|软件|驱动|driver|serial|激活码| licence|license)",
    re.I)


def list_zip(path):
    try:
        with zipfile.ZipFile(path) as z:
            return [i.filename for i in z.infolist()]
    except Exception as e:
        return None


def list_rar(path):
    """用纯 Python 的 rarfile 列目录（仅列目录，不解压，不触发杀软）；失败回退字节嗅探。"""
    try:
        import rarfile
        with rarfile.RarFile(path) as rf:
            return [i.filename for i in rf.infolist()]
    except Exception:
        return None


def sniff_rar_names(path):
    """无解压器时：在原始字节里找 .exe/.msi（含 UTF-16LE 情形）。"""
    try:
        with open(path, "rb") as f:
            b = f.read(4 * 1024 * 1024)
    except OSError:
        return []
    pats = [b".exe", b".EXE", b".msi", b".MSI", b".bat", b".BAT",
            b".e\x00x\x00e\x00", b".m\x00s\x00i\x00"]
    hits = []
    for p in pats:
        if p in b:
            hits.append(p.decode("utf-8", "ignore").replace("\x00", ""))
    return hits


def classify(rel_path, entries):
    """返回 (是否软件/可执行包, 命中说明)"""
    fn = os.path.basename(rel_path)
    name_hit = NAME_PAT.search(fn)
    if entries is None:
        sn = sniff_rar_names(rel_path)
        if sn:
            return True, "字节嗅探命中可执行文件:" + ",".join(sn)
        return None, "无法列目录"
    execs = [e for e in entries if os.path.splitext(e)[1].lower() in EXEC_EXTS]
    bins = [e for e in entries if os.path.splitext(e)[1].lower() in BIN_EXTS]
    if execs:
        return True, "含可执行程序 %d 个，如 %s" % (len(execs), execs[0][:80])
    if bins:
        return True, "含程序二进制 %d 个，如 %s" % (len(bins), bins[0][:80])
    if name_hit:
        return True, "文件名疑似安装包/破解包：%s" % name_hit.group(0)
    return False, "普通资料包（%d 条目，无可执行文件）" % len(entries)


def main():
    archives, others = [], []
    for dirpath, dirnames, filenames in os.walk(QUAR):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, QUAR)
            ext = os.path.splitext(fn)[1].lower()
            (archives if ext in ARCH_EXTS else others).append((rel, full))

    soft, unknown, normal = [], [], []
    for rel, full in archives:
        ext = os.path.splitext(full)[1].lower()
        entries = list_zip(full) if ext == ".zip" else (
            list_rar(full) if ext in (".rar", ".7z") else None)
        is_soft, why = classify(full, entries)
        rec = (rel, why)
        soft.append(rec) if is_soft else (unknown.append(rec) if is_soft is None else normal.append(rec))

    moved_soft = moved_unk = 0
    if APPLY:
        for rec, dst_root, counter in ((soft, SOFT_DIR, "s"), (unknown, UNK_DIR, "u")):
            for rel, why in rec:
                src = os.path.join(QUAR, rel)
                dst = os.path.join(dst_root, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    import shutil
                    shutil.move(src, dst)
                    if counter == "s":
                        moved_soft += 1
                    else:
                        moved_unk += 1
                except OSError as e:
                    with open(os.path.join(HERE, "q2_move_errors.txt"), "a", encoding="utf-8") as ef:
                        ef.write("%s\t%s\n" % (rel, e))

    # 删除其余不合格文件
    deleted = failed = 0
    removed_dirs = 0
    if APPLY:
        for dirpath, dirnames, filenames in os.walk(QUAR, topdown=False):
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                try:
                    os.remove(p)
                    deleted += 1
                except OSError as e:
                    failed += 1
                    with open(os.path.join(HERE, "q2_delete_errors.txt"), "a", encoding="utf-8") as ef:
                        ef.write("%s\t%s\n" % (p, e))
            if os.path.abspath(dirpath) != os.path.abspath(QUAR):
                try:
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                        removed_dirs += 1
                except OSError:
                    pass

    lines = []
    lines.append("第二步：压缩包安全筛查 + 隔离区清理")
    lines.append("=" * 60)
    lines.append("隔离区   : %s" % QUAR)
    lines.append("软件隔离 : %s" % SOFT_DIR)
    lines.append("待确认   : %s" % UNK_DIR)
    lines.append("模式     : %s" % ("实际执行 APPLY" if APPLY else "演练 DRY-RUN"))
    lines.append("")
    lines.append("压缩包总数 : %d" % len(archives))
    lines.append("  软件/可执行程序包 : %d" % len(soft))
    lines.append("  无法扫描待确认    : %d" % len(unknown))
    lines.append("  普通资料包(可删)  : %d" % len(normal))
    lines.append("")
    lines.append("--- 软件/可执行程序压缩包（不删除，交用户处理）---")
    for rel, why in soft:
        lines.append("  %s  << %s" % (rel, why))
    lines.append("")
    lines.append("--- 无法扫描、需人工确认 ---")
    for rel, why in unknown:
        lines.append("  %s  << %s" % (rel, why))
    lines.append("")
    lines.append("--- 普通资料包（已随隔离区删除）---")
    for rel, why in normal[:60]:
        lines.append("  %s  << %s" % (rel, why))
    if len(normal) > 60:
        lines.append("  ... 其余 %d 个" % (len(normal) - 60))
    lines.append("")
    lines.append("移动软件包 : %d" % moved_soft)
    lines.append("移动待确认 : %d" % moved_unk)
    lines.append("删除文件   : %d（失败 %d）" % (deleted, failed))
    lines.append("清理空目录 : %d" % removed_dirs)
    lines.append("")
    lines.append("注：本次未运行 update.py（数据源频繁变动期间暂停重建索引）。")

    with open(os.path.join(HERE, "q2_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(HERE, "q2_archives.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["relpath", "category", "detail"])
        for rel, why in soft:
            w.writerow([rel, "software", why])
        for rel, why in unknown:
            w.writerow([rel, "unknown", why])
        for rel, why in normal:
            w.writerow([rel, "normal", why])
    print("OK arch=%d soft=%d unknown=%d normal=%d deleted=%d failed=%d"
          % (len(archives), len(soft), len(unknown), len(normal), deleted, failed))


if __name__ == "__main__":
    main()
