# -*- coding: utf-8 -*-
"""convert_docs2.py -- 第二批文本文档 -> Markdown（无 COM 依赖版）。

相比 convert_batch2.py 的改进：
  1. **不用 Word COM**：按文件魔数分流
       - PK          -> 实为 .docx，直接 python-docx 解析（含 .doc 伪装的 16 个，COM 必失败的那批）
       - D0CF11E0    -> 真 .doc，交给 LibreOffice 无头批量转 .docx，失败再降级转 .txt
       - {\\rtf      -> LibreOffice
       - 其它        -> 按 txt / html 直读
  2. **流式产出**：每转完一个立刻写 md，不再“先全批转码再统一输出”。
  3. **并发**：python-docx / txt / html 用线程池；仅 LibreOffice 串行批处理。
  4. LibreOffice 侧用“序号命名 + 独立批次目录”，彻底规避中文路径与同名冲突。

用法：
  python convert_docs2.py
"""
import os
import io
import re
import sys
import time
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

TMP = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.dirname(TMP)
SRC = os.path.join(SOURCE, "第二批")
DST = os.path.join(SOURCE, "第二批提取后")
CACHE = os.path.join(TMP, "lo_cache")
PROGRESS = os.path.join(TMP, "docs2_progress.txt")
REPORT = os.path.join(TMP, "第二批文档转换报告.txt")

sys.path.insert(0, TMP)
import docx_core as dc  # noqa: E402
import doc97  # noqa: E402

DOC_EXT = {".doc", ".docx", ".txt", ".html", ".htm", ".rtf", ".mht", ".wps"}
WORKERS = 8
BATCH = 40

log = []
_lock = __import__("threading").Lock()


def say(m):
    with _lock:
        log.append("[%s] %s" % (time.strftime("%H:%M:%S"), m))
        print(m)
        try:
            with io.open(PROGRESS, "w", encoding="utf-8") as f:
                f.write("\n".join(log[-80:]))
        except Exception:
            pass


def out_path(src):
    rel = os.path.relpath(src, SRC)
    return os.path.join(DST, os.path.splitext(rel)[0] + ".md")


def write_md(dst, body):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8") as f:
        f.write(body)


def magic(path):
    try:
        with open(path, "rb") as f:
            b = f.read(8)
    except OSError:
        return ""
    if b[:4] == b"\xd0\xcf\x11\xe0":
        return "ole2"
    if b[:2] == b"PK":
        return "zip"
    if b[:5] == b"{\\rtf":
        return "rtf"
    if b[:2] == b"%P":
        return "pdf"
    return "text"


def read_text_auto(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return ""


def html_to_md(text):
    text = re.sub(r"(?is)<(script|style).*?</\1>", "", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n\n", text)
    text = re.sub(r"(?i)<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", text)
    text = re.sub(r"(?i)</h[1-6]>", "\n", text)
    text = re.sub(r"(?i)<li[^>]*>", "\n- ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def txt_to_md(text):
    out = []
    for ln in text.split("\n"):
        s = ln.rstrip()
        if not s.strip():
            out.append("")
            continue
        try:
            k, payload = dc.classify(s, False, False)
        except Exception:
            k, payload = "text", None
        if k == "sep":
            out.append("---")
        elif k == "list":
            out.append("  " * payload[0] + "- " + payload[1])
        else:
            out.append(s.rstrip())
    body = "\n".join(out)
    while "\n\n\n" in body:
        body = body.replace("\n\n\n", "\n\n")
    return body.strip() + "\n"


def find_soffice():
    cands = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "LibreOffice", "program", "soffice.exe"),
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    w = shutil.which("soffice")
    return w


def lo_batch(soffice, items, tag, to="docx"):
    """items: [(src, slot_name)]；复制到批次目录并批量转换，返回 {slot: 产物路径}。"""
    if not items:
        return {}
    bdir = os.path.join(CACHE, "b_" + tag)
    outdir = os.path.join(bdir, "out")
    shutil.rmtree(bdir, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)
    for src, slot in items:
        try:
            shutil.copy2(src, os.path.join(bdir, slot + os.path.splitext(src)[1].lower()))
        except OSError:
            pass
    cmd = [soffice, "--headless", "--norestore", "--convert-to", to,
           "--outdir", outdir]
    cmd += [os.path.join(bdir, slot + os.path.splitext(s)[1].lower()) for s, _ in items]
    try:
        subprocess.run(cmd, capture_output=True, timeout=600)
    except subprocess.TimeoutExpired:
        pass
    res = {}
    for slot, _ in items:
        ext = ".docx" if to == "docx" else ".txt"
        p = os.path.join(outdir, slot + ext)
        if os.path.exists(p) and os.path.getsize(p) > 0:
            res[slot] = p
    return res


def main():
    t0 = time.time()
    os.makedirs(DST, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    files = []
    for dp, _dn, fn in os.walk(SRC):
        for f in fn:
            if f.startswith("~$"):
                continue
            if os.path.splitext(f)[1].lower() in DOC_EXT:
                files.append(os.path.join(dp, f))
    files.sort()

    groups = {"zip": [], "ole2": [], "rtf": [], "html": [], "text": []}
    for p in files:
        m = magic(p)
        ext = os.path.splitext(p)[1].lower()
        if m == "zip":
            groups["zip"].append(p)
        elif m == "ole2":
            groups["ole2"].append(p)
        elif m == "rtf":
            groups["rtf"].append(p)
        elif ext in (".html", ".htm", ".mht"):
            groups["html"].append(p)
        else:
            groups["text"].append(p)
    say("扫描 %d 个文档 -> docx类 %d / 真doc %d / rtf %d / html %d / txt %d"
        % (len(files), len(groups["zip"]), len(groups["ole2"]),
           len(groups["rtf"]), len(groups["html"]), len(groups["text"])))

    ok = fail = 0
    failed = []

    def do_text(p):
        try:
            body = txt_to_md(read_text_auto(p))
            if not body.strip():
                return (False, p, "空文本")
            write_md(out_path(p), body)
            return (True, p, "")
        except Exception as e:
            return (False, p, repr(e)[:100])

    def do_html(p):
        try:
            body = html_to_md(read_text_auto(p))
            if not body.strip():
                return (False, p, "空文本")
            write_md(out_path(p), body)
            return (True, p, "")
        except Exception as e:
            return (False, p, repr(e)[:100])

    def do_docx(p, real=None):
        try:
            body = dc.docx_to_md(real or p)
            if not body.strip():
                return (False, p, "空文本")
            write_md(out_path(p), body)
            return (True, p, "")
        except Exception as e:
            return (False, p, repr(e)[:100])

    def run_pool(fn, items, label):
        nonlocal ok, fail
        n = len(items)
        if not n:
            return
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs = [ex.submit(fn, p) for p in items]
            done = 0
            for fu in as_completed(futs):
                good, p, err = fu.result()
                done += 1
                if good:
                    ok += 1
                else:
                    fail += 1
                    failed.append((os.path.relpath(p, SRC), err))
                if done % 50 == 0 or done == n:
                    say("%s 进度 %d/%d" % (label, done, n))

    # 1) 直接可解析的三类，先出成果
    run_pool(do_docx, groups["zip"], "docx")
    run_pool(do_html, groups["html"], "html")
    run_pool(do_text, groups["text"], "txt")
    say("快通道完成：成功 %d 失败 %d，耗时 %.1f 分钟" % (ok, fail, (time.time() - t0) / 60.0))

    # 2) 真 .doc（OLE2）-> 纯 Python 正文抽取 doc97（无 COM / 无 LibreOffice）
    legacy = groups["ole2"]
    if legacy:
        def do_ole2(p):
            try:
                text, err = doc97.extract(p)
                if len(text) < 100:
                    return (False, p, err or ("正文过短 %d 字" % len(text)))
                write_md(out_path(p), txt_to_md(text))
                return (True, p, "")
            except Exception as e:
                return (False, p, repr(e)[:100])

        run_pool(do_ole2, legacy, "doc97")
        say("真 .doc 通道完成：%d 个" % len(legacy))

    # 3) RTF：优先 LibreOffice（若存在），否则粗剥离
    rtf = groups["rtf"]
    if rtf:
        soffice = find_soffice()
        if soffice:
            say("RTF %d 个，走 LibreOffice" % len(rtf))
            slots = {"f%05d" % i: p for i, p in enumerate(rtf)}
            items = sorted(slots.items())
            converted = {}
            for bi in range(0, len(items), BATCH):
                chunk = items[bi:bi + BATCH]
                converted.update(lo_batch(soffice, [(v, k) for k, v in chunk],
                                          "r%03d" % (bi // BATCH), "docx"))
            for k, v in converted.items():
                good, p, err = (do_docx(slots[k], v) if v.endswith(".docx")
                                else do_text_r(v, slots[k]))
                if good:
                    ok += 1
                else:
                    fail += 1
                    failed.append((os.path.relpath(p, SRC), err))
        else:
            say("RTF %d 个：无 LibreOffice，跳过" % len(rtf))
            failed += [(os.path.relpath(p, SRC), "RTF 无转换后端") for p in rtf]
            fail += len(rtf)

    say("")
    say("总计: 成功 %d, 失败 %d, 耗时 %.1f 分钟" % (ok, fail, (time.time() - t0) / 60.0))
    say("--- 失败清单（前 60）---")
    for rel, err in failed[:60]:
        say("  %s  << %s" % (rel, err))
    with io.open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("DOCS2 DONE ok=%d fail=%d" % (ok, fail))


def do_text_r(real, src):
    """LO 降级产出的 txt -> md（写到 src 对应的输出路径）。"""
    try:
        body = txt_to_md(read_text_auto(real))
        if not body.strip():
            return (False, src, "空文本")
        write_md(out_path(src), body)
        return (True, src, "")
    except Exception as e:
        return (False, src, repr(e)[:100])


if __name__ == "__main__":
    main()
