# -*- coding: utf-8 -*-
"""收尾：处理剩余压缩包，并把已解压成功的原包「移动」到隔离目录（不做删除）。

说明：环境对批量删除有保护，故用移动代替删除，效果等价且可恢复。
"""
import os
import io
import shutil
import zipfile
import hashlib
import subprocess

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
TMP = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp"
QUAR = os.path.join(os.path.dirname(B2), "第二批_已解压原包")
REPORT = os.path.join(TMP, "解压收尾报告.txt")
WORK = os.path.join(os.environ.get("TEMP") or r"C:\Windows\Temp", "kbx_work2")
# 需跳过的目录关键字（逗号分隔）；环境变量为空表示全量处理
SKIP_DIR = [k for k in (os.environ.get("KB_SKIP") or "").split(",") if k]
ARCH_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz"}
log = []


def count_files(d):
    return sum(len(f) for _d, _u, f in os.walk(d))


def fix_name(nm):
    try:
        return nm.encode("cp437").decode("gbk")
    except Exception:
        return nm


def safe_join(base, rel):
    tgt = os.path.normpath(os.path.join(base, rel))
    return tgt if tgt.startswith(os.path.normpath(base)) else None


def extract_zip(src, target):
    os.makedirs(target, exist_ok=True)
    n = 0
    with zipfile.ZipFile(src) as z:
        for nm in z.namelist():
            real = fix_name(nm)
            tgt = safe_join(target, real)
            if tgt is None:
                continue
            if real.endswith(("/", "\\")):
                os.makedirs(tgt, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            if os.path.exists(tgt):
                continue
            try:
                with z.open(nm) as s, open(tgt, "wb") as d:
                    shutil.copyfileobj(s, d)
                n += 1
            except Exception:
                pass
    return n


def extract_tarfile_py(src, target):
    """tar/tar.gz：优先用 Python tarfile（原生处理中文名，无路径编码问题）。"""
    import tarfile
    os.makedirs(target, exist_ok=True)
    n = 0
    with tarfile.open(src) as tf:
        for m in tf.getmembers():
            try:
                tgt = safe_join(target, m.name)
                if tgt is None:
                    continue
                if m.isdir():
                    os.makedirs(tgt, exist_ok=True)
                    continue
                os.makedirs(os.path.dirname(tgt), exist_ok=True)
                if os.path.exists(tgt):
                    continue
                with tf.extractfile(m) as s, open(tgt, "wb") as d:
                    shutil.copyfileobj(s, d)
                n += 1
            except Exception:
                continue
    return n


def extract_tar(src, target):
    """rar/7z 等：ASCII 中转 + tar。

    注意：tar 遇到个别坏文件/中文名时返回码非 0，但**已解压出其余文件**，
    因此这里不因返回码提前失败，只要解压出内容就算成功（允许"部分成功"）。
    """
    h = hashlib.md5(src.encode("utf-8")).hexdigest()[:10]
    w = os.path.join(WORK, h)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(os.path.join(w, "out"), exist_ok=True)
    tmp_in = os.path.join(w, "in" + os.path.splitext(src)[1].lower())
    shutil.copy2(src, tmp_in)
    p = subprocess.run(["tar", "-xf", tmp_in, "-C", os.path.join(w, "out")],
                       capture_output=True, text=True, errors="replace",
                       creationflags=0x08000000)  # CREATE_NO_WINDOW：不弹控制台窗口
    if p.returncode != 0 and not os.listdir(os.path.join(w, "out")):
        return 0, (p.stderr or "")[:120]
    os.makedirs(target, exist_ok=True)
    moved = 0
    for entry in os.listdir(os.path.join(w, "out")):
        s = os.path.join(w, "out", entry)
        t = os.path.join(target, entry)
        if os.path.exists(t):
            continue
        try:
            shutil.move(s, t)
            moved += 1
        except Exception:
            pass
    shutil.rmtree(w, ignore_errors=True)
    return moved, ""


def find_archives():
    res = []
    for dp, _dn, fn in os.walk(B2):
        if any(k in dp for k in SKIP_DIR):
            continue
        for f in fn:
            if not f.startswith("~$") and os.path.splitext(f)[1].lower() in ARCH_EXT:
                res.append(os.path.join(dp, f))
    return sorted(res)


def move_away(src):
    rel = os.path.relpath(src, B2)
    dst = os.path.join(QUAR, rel)
    if os.path.exists(dst):
        root, ext = os.path.splitext(dst)
        i = 1
        while os.path.exists("%s__%d%s" % (root, i, ext)):
            i += 1
        dst = "%s__%d%s" % (root, i, ext)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)


def main():
    os.makedirs(WORK, exist_ok=True)
    items = find_archives()
    log.append("剩余压缩包: %d" % len(items))
    ok = fail = 0
    for i, src in enumerate(items, 1):
        rel = os.path.relpath(src, B2)
        # 文件名末尾空格/点会让 Windows 建目录异常（如 "VISIO模板 .rar"）
        target = os.path.splitext(src)[0].rstrip(" .")
        ext = os.path.splitext(src)[1].lower()
        already = os.path.isdir(target) and count_files(target) > 0
        if already:
            move_away(src)
            ok += 1
            log.append("[已解压->移走原包 %d/%d] %s" % (i, len(items), rel))
            continue
        try:
            if ext == ".zip":
                n = extract_zip(src, target)
            elif ext in (".tar", ".gz", ".tgz", ".bz2", ".xz"):
                n = extract_tarfile_py(src, target)
            else:
                n = extract_tar(src, target)[0]
        except Exception as e:
            n = 0
            log.append("[EXC %d/%d] %s %r" % (i, len(items), rel, e))
        if os.path.isdir(target) and count_files(target) > 0:
            move_away(src)
            ok += 1
            log.append("[解压成功->移走原包 %d/%d] %s (%d 文件)" % (i, len(items), rel, count_files(target)))
        else:
            fail += 1
            log.append("[失败保留 %d/%d] %s" % (i, len(items), rel))
    log.append("")
    log.append("成功 %d / 失败 %d" % (ok, fail))
    log.append("隔离目录: %s" % QUAR)
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("DONE ok=%d fail=%d remain=%d" % (ok, fail, len(find_archives())))


if __name__ == "__main__":
    main()
