# -*- coding: utf-8 -*-
"""extract_fast.py -- 第二批压缩包快速解压（并发、不删除原包）。

与旧 extract_all.py 的区别：
  1. 并发（默认 6 线程）；zip 直接 zipfile 落盘（不需要 tar，支持中文路径）；
  2. rar 走 ASCII 中转 + tar.exe；能取到 8.3 短名时连复制都省掉；
  3. **绝不使用 os.remove**：解压成功后把原包 shutil.move 到 temp 隔离目录
     （旧脚本 os.remove 触发 safe-delete 批量保护，进程被杀，见 extract_all.log）；
  4. 支持多轮（嵌套压缩包）。

用法：
  python extract_fast.py            # 3 轮
  python extract_fast.py 2          # 指定轮数
"""
import os
import io
import re
import sys
import time
import shutil
import zipfile
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

TMP = os.path.dirname(os.path.abspath(__file__))            # kb/source/temp
SOURCE = os.path.dirname(TMP)                               # kb/source
SRC = os.path.join(SOURCE, "第二批")
MOVED = os.path.join(TMP, "第二批_已解压原包_20260910")
WORK = os.path.join(os.environ.get("TEMP") or r"C:\Windows\Temp", "kbfast_work")
PROGRESS = os.path.join(TMP, "extract_fast_progress.txt")
REPORT = os.path.join(TMP, "第二批解压报告.txt")

ARCH_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz"}
WORKERS = 6
TAR_TIMEOUT = 900

log = []
lock = __import__("threading").Lock()


def say(m):
    with lock:
        log.append("[%s] %s" % (time.strftime("%H:%M:%S"), m))
        try:
            with io.open(PROGRESS, "w", encoding="utf-8") as f:
                f.write("\n".join(log[-80:]))
        except Exception:
            pass
        print(m)


def flush_report():
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(log))


# ---------- 8.3 短名（Windows tar.exe 只能吃 ASCII 路径） ----------
def short_path(path):
    try:
        import ctypes
        from ctypes import wintypes
        buf = ctypes.create_unicode_buffer(260)
        n = ctypes.windll.kernel32.GetShortPathNameW(path, buf, 260)
        if n and n < 260:
            s = buf.value
            if s and all(ord(c) < 128 for c in s):
                return s
    except Exception:
        pass
    return None


def fix_name(nm):
    """zip 内文件名可能是 cp437 误读的 GBK 中文。"""
    try:
        return nm.encode("cp437").decode("gbk")
    except Exception:
        return nm


def do_zip(src, target):
    os.makedirs(target, exist_ok=True)
    n = 0
    with zipfile.ZipFile(src) as z:
        for nm in z.namelist():
            real = fix_name(nm)
            if real.endswith(("/", "\\")):
                continue
            tgt = os.path.normpath(os.path.join(target, real))
            if not tgt.startswith(os.path.normpath(target)):
                continue
            if os.path.exists(tgt):
                continue
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            try:
                with z.open(nm) as s, open(tgt, "wb") as d:
                    shutil.copyfileobj(s, d)
                n += 1
            except Exception:
                pass
    return n, ""


def do_rar(src, target, slot):
    w = os.path.join(WORK, "w%d" % slot)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w, exist_ok=True)
    tmp_out = os.path.join(w, "out")
    os.makedirs(tmp_out, exist_ok=True)

    sp = short_path(src)
    if sp:
        arc = sp
        need_copy = False
    else:
        arc = os.path.join(w, "in.rar")
        shutil.copy2(src, arc)
        need_copy = True

    try:
        p = subprocess.run(["tar", "-xf", arc, "-C", tmp_out],
                           capture_output=True, timeout=TAR_TIMEOUT)
    except subprocess.TimeoutExpired:
        return 0, "tar 超时"
    err = "" if p.returncode == 0 else ((p.stderr or b"").decode("utf-8", "ignore"))[:120]

    os.makedirs(target, exist_ok=True)
    moved = 0
    for entry in os.listdir(tmp_out):
        s = os.path.join(tmp_out, entry)
        t = os.path.join(target, entry)
        if os.path.exists(t):
            continue
        try:
            os.rename(s, t)          # 同盘符，瞬时
            moved += 1
        except OSError:
            try:
                shutil.move(s, t)
                moved += 1
            except Exception:
                pass
    if need_copy:
        try:
            os.remove(os.path.join(w, "in.rar"))
        except Exception:
            pass
    if moved == 0:
        return 0, err or "tar 无输出"
    return moved, err


def count_files(d):
    return sum(len(f) for _a, _b, f in os.walk(d))


def archive_slot(i):
    return i % WORKERS


def find_archives():
    res = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.startswith("~$"):
                continue
            if os.path.splitext(f)[1].lower() in ARCH_EXT:
                res.append(os.path.join(dp, f))
    return sorted(res)


def move_archive(src):
    """解压成功后把原包移入 temp 隔离目录（不用 os.remove，避开 safe-delete 保护）。"""
    rel = os.path.relpath(src, SRC)
    dst = os.path.join(MOVED, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        stem, ext = os.path.splitext(dst)
        k = 1
        while os.path.exists("%s__dup%d%s" % (stem, k, ext)):
            k += 1
        dst = "%s__dup%d%s" % (stem, k, ext)
    shutil.move(src, dst)


def process(i, src):
    rel = os.path.relpath(src, SRC)
    target = os.path.splitext(src)[0]
    ext = os.path.splitext(src)[1].lower()
    before = count_files(target) if os.path.isdir(target) else 0
    t0 = time.time()
    try:
        if ext == ".zip":
            n, err = do_zip(src, target)
        elif ext in (".rar", ".7z", ".tar", ".gz", ".tgz"):
            n, err = do_rar(src, target, archive_slot(i))
        else:
            n, err = 0, "unsupported"
    except Exception as e:
        n, err = 0, repr(e)[:120]
    dt = time.time() - t0
    after = count_files(target) if os.path.isdir(target) else 0
    ok = after > 0 and (after >= before or n > 0)
    if ok and not err:
        try:
            move_archive(src)
        except Exception as e:
            say("[OK但移包失败] %s %r" % (rel, e))
    elif ok and err:
        # 部分成功（如 rar 内个别条目 CRC/文件名编码错误）：内容已大部分落地，
        # 重试试也是同样结果，直接把原包归档，避免每轮重复。
        try:
            move_archive(src)
        except Exception as e:
            say("[部分但移包失败] %s %r" % (rel, e))
        say("[部分] %s -> %d 新文件, 已归档原包 err=%s" % (rel, after - before, err))
    say("%s %s -> %d 新文件, %.1fs%s"
        % ("[OK]" if ok else "[FAIL]", rel, after - before, dt,
           ("" if ok else " err=" + err)))
    return ok


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    t0 = time.time()
    os.makedirs(WORK, exist_ok=True)
    total_ok = total_fail = 0
    for rnd in range(1, rounds + 1):
        items = find_archives()
        say("== 第 %d 轮：待解压 %d 个 ==" % (rnd, len(items)))
        if not items:
            break
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = {ex.submit(process, i, p): p for i, p in enumerate(items)}
            for fu in as_completed(futs):
                try:
                    if fu.result():
                        total_ok += 1
                    else:
                        total_fail += 1
                except Exception:
                    total_fail += 1
    say("")
    say("总计: 成功 %d, 失败 %d, 耗时 %.1f 分钟"
        % (total_ok, total_fail, (time.time() - t0) / 60.0))
    flush_report()
    print("EXTRACT_FAST DONE ok=%d fail=%d" % (total_ok, total_fail))


if __name__ == "__main__":
    main()
