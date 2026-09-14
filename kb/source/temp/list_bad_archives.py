# -*- coding: utf-8 -*-
"""列出所有不能正常解压的压缩包，并诊断原因（损坏 / 加密 / 不支持 / 空包）。"""
import os
import io
import re
import sys
import shutil
import zipfile
import hashlib
import subprocess

B2 = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第二批"
TMP = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp"
REPORT = os.path.join(TMP, "不能解压的压缩包清单.txt")
WORK = os.path.join(os.environ.get("TEMP") or r"C:\Windows\Temp", "kbx_diag")
ARCH_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bz2", ".xz"}

SIG = {
    b"PK\x03\x04": "ZIP",
    b"Rar!\x1a\x07\x00": "RAR4",
    b"Rar!\x1a\x07\x01\x00": "RAR5",
    b"7z\xbc\xaf\x27\x1c": "7z",
}


def detect(path):
    try:
        with open(path, "rb") as f:
            head = f.read(16)
    except Exception as e:
        return "读取失败 %r" % (e,)
    for sig, name in SIG.items():
        if head.startswith(sig):
            return name
    if head[:2] == b"\x1f\x8b":
        return "GZIP"
    return "未知/非压缩包"


def diag(path):
    """返回 (是否可解压, 原因)。"""
    fmt = detect(path)
    ext = os.path.splitext(path)[1].lower()
    try:
        size = os.path.getsize(path)
    except Exception:
        size = -1
    if size == 0:
        return False, "空文件(0字节)"
    if fmt.startswith("未知"):
        return False, "文件头非压缩包（可能下载未完成/损坏）：%s" % fmt

    if fmt == "ZIP" and ext == ".zip":
        try:
            with zipfile.ZipFile(path) as z:
                bad = z.testzip()
                names = z.namelist()
                if bad:
                    return False, "ZIP 内 %s 校验失败（损坏）" % bad
                if not names:
                    return False, "ZIP 空包"
                return True, "可解压（%d 项）" % len(names)
        except zipfile.BadZipFile as e:
            return False, "ZIP 结构损坏：%s" % e
        except Exception as e:
            return False, "ZIP 打开失败：%r" % (e,)

    # rar / 7z / tar.gz：用 tar 试解（ASCII 中转）
    h = hashlib.md5(path.encode("utf-8")).hexdigest()[:10]
    w = os.path.join(WORK, h)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(os.path.join(w, "out"), exist_ok=True)
    tmp_in = os.path.join(w, "in" + ext)
    try:
        shutil.copy2(path, tmp_in)
    except Exception as e:
        return False, "复制失败 %r" % (e,)
    p = subprocess.run(["tar", "-xf", tmp_in, "-C", os.path.join(w, "out")],
                       capture_output=True, text=True, errors="replace",
                       creationflags=0x08000000)  # CREATE_NO_WINDOW
    n = sum(len(f) for _d, _u, f in os.walk(os.path.join(w, "out")))
    err = (p.stderr or "").strip().replace("\n", " ")[:200]
    if p.returncode == 0 and n > 0:
        ok = True, "可解压（%d 个文件）" % n
    else:
        if "password" in err.lower() or "encrypt" in err.lower():
            reason = "需要密码/加密"
        elif "truncated" in err.lower() or "unexpected eof" in err.lower():
            reason = "文件不完整（下载未完成/截断）"
        elif "not supported" in err.lower() or "unsupported" in err.lower():
            reason = "格式不受支持"
        else:
            reason = "解压失败：%s" % (err or ("返回码 %d" % p.returncode))
        ok = False, reason
    shutil.rmtree(w, ignore_errors=True)
    return ok


def main():
    items = []
    for dp, _dn, fn in os.walk(B2):
        for f in fn:
            if f.startswith("~$"):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in ARCH_EXT:
                items.append(os.path.join(dp, f))
    items.sort()
    log = ["不能正常解压的压缩包清单", "第二批中剩余压缩包总数: %d" % len(items), ""]
    bad = []
    for i, p in enumerate(items, 1):
        ok, reason = diag(p)
        rel = os.path.relpath(p, B2)
        try:
            size = os.path.getsize(p)
        except Exception:
            size = -1
        if not ok:
            bad.append((rel, size, detect(p), reason))
            log.append("[不可解压] %s" % rel)
            log.append("            大小 %d  格式 %s  原因 %s" % (size, detect(p), reason))
        else:
            log.append("[可解压]   %s  (%s)" % (rel, reason))
    log.append("")
    log.append("===== 汇总 =====")
    log.append("剩余压缩包 %d 个，其中不能解压 %d 个" % (len(items), len(bad)))
    log.append("")
    log.append("## 不可解压清单（%d 个）" % len(bad))
    for rel, size, fmt, reason in bad:
        log.append("%8d  %-6s  %s" % (size, fmt, rel))
        log.append("          原因: %s" % reason)
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("ARCHIVES=%d BAD=%d" % (len(items), len(bad)))


if __name__ == "__main__":
    main()
