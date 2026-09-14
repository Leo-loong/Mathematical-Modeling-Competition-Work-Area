# -*- coding: utf-8 -*-
"""P4 构建 SQLite 检索库 data/catalog.db：
  files      文件级元数据（含 content_sha/nlines/ocr_like，支撑过期检测与标签）
  chunks     正文段落块（md/text 段落级；code 整文件或分段）
  fts_files  文件级 FTS5(trigram)：title+summary+keywords
  fts_chunks 正文 FTS5(trigram)
无 trigram 时自动降级 unicode61（短查询走 LIKE 兜底）。
幂等：库内 DROP TABLE 重建，不做任何文件系统删除（触发环境安全删除保护）。
"""
import os
import re
import json
import sqlite3
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(os.path.dirname(HERE))  # kb 的上级；path 字段相对此目录
DATA = os.path.join(HERE, "data")
DB = os.path.join(DATA, "catalog.db")
PAGE_MARK = re.compile(r"<!--\s*第\s*\d+\s*页\s*-->")
WS = re.compile(r"\s+")
MD_EXTS = {".md"}
CODE_EXTS = {".m", ".M", ".py", ".c", ".h", ".cpp"}


def read_text_best(path):
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def chunk_md(text, max_len=800):
    """段落切块，块带所在标题上下文；返回 [(section, line_no, body)]"""
    text = PAGE_MARK.sub("", text)
    lines = text.split("\n")
    chunks, section, buf, start, lineno = [], "", [], None, 0
    def flush():
        nonlocal buf, start
        if buf:
            body = "\n".join(buf).strip()
            if body:
                chunks.append((section, (start if start is not None else lineno) + 1, body))
            buf, start = [], None
    for i, ln in enumerate(lines):
        h = re.match(r"^(#{1,6})\s+(.+)$", ln.strip())
        if h:
            flush()
            section = h.group(2).strip()[:80]
            chunks.append((section, i + 1, ln.strip()))  # 标题本身也是可检索单元
            continue
        if not ln.strip():
            flush()
            continue
        if start is None:
            start = i
        buf.append(ln)
        if sum(len(x) for x in buf) >= max_len:
            flush()
    flush()
    return chunks


def chunk_code(text, max_lines=120):
    lines = text.split("\n")
    if len(lines) <= max_lines:
        return [(1, text)]
    return [(i + 1, "\n".join(lines[i:i + max_lines])) for i in range(0, len(lines), max_lines)]


def main():
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "files.json"), encoding="utf-8") as f:
        records = json.load(f)
    con = sqlite3.connect(DB)
    cur = con.cursor()
    # 幂等重建：清空旧表（SQL 层，避免文件系统删除触发环境保护）
    for t in ("fts_probe", "fts_files", "fts_chunks", "files", "chunks"):
        cur.execute("DROP TABLE IF EXISTS %s" % t)
    con.commit()
    try:
        tok = "trigram"
        cur.execute("CREATE VIRTUAL TABLE fts_probe USING fts5(x, tokenize='trigram')")
        cur.execute("DROP TABLE fts_probe")
    except sqlite3.OperationalError:
        tok = "unicode61"
    cur.execute("""CREATE TABLE files(
        fid INTEGER PRIMARY KEY, path TEXT UNIQUE, area TEXT, kind TEXT,
        title TEXT, summary TEXT, keywords TEXT, nchars INTEGER, dup_group TEXT,
        content_sha TEXT, nlines INTEGER, ocr_like INTEGER)""")
    cur.execute("""CREATE TABLE chunks(
        cid INTEGER PRIMARY KEY, fid INTEGER, section TEXT, line_no INTEGER, body TEXT)""")
    cur.execute("CREATE INDEX idx_chunks_fid ON chunks(fid)")
    cur.execute("CREATE VIRTUAL TABLE fts_files USING fts5(title,summary,keywords, tokenize='%s')" % tok)
    cur.execute("CREATE VIRTUAL TABLE fts_chunks USING fts5(body, tokenize='%s')" % tok)

    n_chunk = 0
    for rec in records:
        full = os.path.join(WORKSPACE, rec["path"])
        if rec["kind"] == "doc":
            # 二进制文献：不解码文本（乱码会污染指纹与 OCR 启发式），指纹用原始字节
            try:
                with open(full, "rb") as f:
                    raw = f.read()
            except OSError:
                continue
            text = ""
            content_sha = hashlib.sha1(raw).hexdigest()[:16]
            nlines, ocr_like = 0, 0
        else:
            try:
                text = read_text_best(full)
            except OSError:
                continue
            # Issue#3: 内容指纹（查询时比对，外部修改导致行号漂移可被感知）
            content_sha = hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]
            nlines = text.count("\n") + 1
            # Issue#6: 疑似 OCR 启发式——简体文献中几乎不出现的繁体形近字密度
            rare_hits = sum(1 for ch in text if ch in "題於説間時點個們這裡後開關際難隨機")
            ocr_like = 1 if (rare_hits >= 3 and rec["kind"] == "md") else 0
        norm = WS.sub("", PAGE_MARK.sub("", text))
        dup = hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12] if norm else ""
        cur.execute("""INSERT INTO files(path,area,kind,title,summary,keywords,nchars,dup_group,
                       content_sha,nlines,ocr_like) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                    (rec["path"], rec["area"], rec["kind"], rec["title"], rec["summary"],
                     " ".join(rec["keywords"]), rec["nchars"], dup,
                     content_sha, nlines, ocr_like))
        fid = cur.lastrowid
        cur.execute("INSERT INTO fts_files(rowid,title,summary,keywords) VALUES(?,?,?,?)",
                    (fid, rec["title"], rec["summary"], " ".join(rec["keywords"])))
        if rec["kind"] == "code":
            for line_no, body in chunk_code(text):
                cur.execute("INSERT INTO chunks(fid,section,line_no,body) VALUES(?,?,?,?)",
                            (fid, "", line_no, body))
                cur.execute("INSERT INTO fts_chunks(rowid,body) VALUES((SELECT last_insert_rowid()),?)", (body,))
                n_chunk += 1
        elif rec["kind"] in ("md", "text"):
            for section, line_no, body in chunk_md(text):
                cur.execute("INSERT INTO chunks(fid,section,line_no,body) VALUES(?,?,?,?)",
                            (fid, section, line_no, body))
                cur.execute("INSERT INTO fts_chunks(rowid,body) VALUES((SELECT last_insert_rowid()),?)", (body,))
                n_chunk += 1
        if fid % 500 == 0:
            con.commit()
            print("indexed %d files, %d chunks" % (fid, n_chunk))
    con.commit()
    con.execute("ANALYZE")
    con.close()
    size = os.path.getsize(DB) / 1048576
    print("P4 done. files=%d chunks=%d tokenizer=%s db=%.1fMB" % (len(records), n_chunk, tok, size))


if __name__ == "__main__":
    main()
