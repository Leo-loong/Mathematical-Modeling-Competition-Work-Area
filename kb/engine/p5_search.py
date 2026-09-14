# -*- coding: utf-8 -*-
"""P5 本地搜索引擎查询接口。
用法：
  python p5_search.py 蒙特卡洛                 # 文件级命中（默认含最佳段落定位）
  python p5_search.py 符号说明 三线表           # 多词 OR 查询（nargs + 词表按词扩展）
  python p5_search.py 薄膜干涉 --deep          # 追加段落级深挖（文件:行号）
  python p5_search.py wavelet --type code      # 只搜代码
  python p5_search.py 小波 --json              # JSON 输出（供 Agent 消费）
  python p5_search.py 外延层 --rebuild-if-stale  # 检测到索引过期时自动重建后重查
特性：别名词表按词扩展；重复组折叠；ASCII 短词整词校验（抑制 sic⊂Basic 类误配）；
索引过期检测（content_sha 比对，结果头部告警）；质量/语言标签透出。
"""
import os
import re
import sys
import json
import hashlib
import sqlite3
import argparse
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
WORKSPACE = os.path.dirname(KB)  # files.path 相对此目录（kb/source/...、refs/... 等）
DB = os.path.join(HERE, "data", "catalog.db")
sys.path.insert(0, HERE)
from p3_meta import ALIAS  # noqa: E402


def read_text_best(path):
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def word_list(query):
    """Issue#1/#5: 多词查询按空白拆分，逐词处理。"""
    return [w for w in re.split(r"\s+", query.strip()) if w]


def expand_terms(query):
    """每个查询词独立做别名词表双向扩展。"""
    terms, seen = [], set()
    for w in word_list(query):
        cands = [w]
        wl = w.lower()
        for std, aliases in ALIAS.items():
            group = [std] + aliases
            if any(t.lower() in wl for t in group) or \
               any(wl in t.lower() for t in group if len(wl) >= 2):
                cands.extend(group)
        for t in cands:
            tl = t.lower()
            if t and tl not in seen:
                seen.add(tl)
                terms.append(t)
    return terms


def fts_expr(terms):
    """trigram 只支持 >=3 字；短词由 LIKE 兜底。"""
    long_t = ['"%s"' % t.replace('"', '""') for t in terms if len(t) >= 3]
    return " OR ".join(long_t) if long_t else ""


def _is_ascii_token(t):
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\-]*", t))


def ascii_word_filters(terms):
    """Issue#2: 纯 ASCII 且 <=5 字符的词（SiC/LP/GRU...）trigram 子串误配严重，
    返回整词边界正则，用于命中后的有效性校验。"""
    return [re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", re.IGNORECASE)
            for t in terms if len(t) <= 5 and _is_ascii_token(t)]


def text_valid(txt, ascii_res, terms):
    """有效性校验：至少有一个查询词以'正当方式'命中（ASCII 短词需整词，其余子串即可）。"""
    if not ascii_res:
        return True
    for rx in ascii_res:
        if rx.search(txt):
            return True
    tl = txt.lower()
    for t in terms:
        if len(t) > 5 or not _is_ascii_token(t):
            if t.lower() in tl:
                return True
    return False


def build_tags(f):
    """质量与语言标签。f: (fid,path,kind,title,summary,nchars,dup_group,content_sha,nlines,ocr_like)"""
    tags = [{"md": "文档", "code": "代码", "text": "文本", "doc": "文献原件"}.get(f[2], f[2])]
    if "提取后" not in f[1] and f[2] != "doc":
        tags.append("原始区")
    if f[2] != "doc" and f[5] is not None and f[5] < 500:
        tags.append("低信息量")
    if f[8]:
        tags.append("疑OCR(繁体混入)")  # 含简体文献罕用繁体形近字，OCR 错字风险高，数字引用需回原件
    return tags


def check_stale(cur, fids, max_check=10):
    """Issue#3: 抽查命中文件的 content_sha，外部修改导致行号漂移可被感知。
    返回 (stale数, 抽查数)。"""
    fids = [str(f) for f in fids if f is not None][:max_check]
    if not fids:
        return 0, 0
    try:
        rows = cur.execute("SELECT fid, path, kind, content_sha FROM files WHERE fid IN (%s)"
                           % ",".join(fids)).fetchall()
    except sqlite3.OperationalError:  # 旧库无该列
        return 0, 0
    checked = stale = 0
    for _fid, path, kind, sha in rows:
        if not sha:
            continue
        checked += 1
        try:
            full = os.path.join(WORKSPACE, path)
            if kind == "doc":  # 二进制文献按原始字节比对（与 p4 口径一致）
                with open(full, "rb") as f:
                    now_sha = hashlib.sha1(f.read()).hexdigest()[:16]
            else:
                text = read_text_best(full)
                now_sha = hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]
        except OSError:
            stale += 1
            continue
        if now_sha != sha:
            stale += 1
    return stale, checked


def search(query, ftype=None, deep=False, limit=20, stale_check=True):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    terms = expand_terms(query)
    fexpr = fts_expr(terms)
    like_terms = [t for t in terms if len(t) < 3]
    ascii_res = ascii_word_filters(terms)

    type_clause = " AND f.kind=?" if ftype else ""
    args_type = (ftype,) if ftype else ()

    # 1) 文件级：FTS（>=3字词） + LIKE（keywords/title/summary 命中）
    hits = {}
    if fexpr:
        sql = """SELECT f.rowid, bm25(fts_files) AS rank
                 FROM fts_files JOIN files f ON f.fid=fts_files.rowid
                 WHERE fts_files MATCH ?""" + type_clause
        try:
            for fid, rank in cur.execute(sql, (fexpr,) + args_type):
                hits[fid] = max(hits.get(fid, -99), -float(rank))
        except sqlite3.OperationalError:
            pass
    for t in terms:
        pat = "%%%s%%" % t
        sql = """SELECT fid, (title LIKE ?)*3 + (summary LIKE ?)*2 + (keywords LIKE ?)*2
                 FROM files WHERE (title LIKE ? OR summary LIKE ? OR keywords LIKE ?)""" \
              + (" AND kind=?" if ftype else "")
        args = (pat, pat, pat, pat, pat, pat) + args_type
        for fid, sc in cur.execute(sql, args):
            if sc > 0:
                hits[fid] = hits.get(fid, 0) + sc

    # 2) 段落级：取 cid+得分（不带 body），按文件折叠，补 body 后做 ASCII 整词校验
    if fexpr:
        sql = """SELECT c.cid, c.fid, c.line_no, c.section, bm25(fts_chunks)
                 FROM fts_chunks JOIN chunks c ON c.cid=fts_chunks.rowid
                 WHERE fts_chunks MATCH ? LIMIT 50000"""
        try:
            raw_rows = cur.execute(sql, (fexpr,)).fetchall()
        except sqlite3.OperationalError:
            raw_rows = []
    else:
        raw_rows = []
    if like_terms and not raw_rows:
        pat = like_terms[0]
        raw_rows = cur.execute("""SELECT cid, fid, line_no, section, 0 FROM chunks
                                  WHERE body LIKE ? LIMIT 20000""",
                               ("%%%s%%" % pat,)).fetchall()
    best = {}
    for cid, fid, line_no, section, rank in raw_rows:
        sc = -float(rank) if rank else 1
        if fid not in best or sc > best[fid][0]:
            best[fid] = (sc, cid, line_no, section)
    # 取候选体量放大 3 倍，供整词校验过滤后仍有足够余量
    top_pairs = sorted(best.values(), key=lambda x: -x[0])[:1500 if ascii_res else 500]
    cid2meta = {}
    if top_pairs:
        qmarks = ",".join("?" * len(top_pairs))
        cid2meta = {r[0]: (r[1], r[2], r[3]) for r in cur.execute(
            "SELECT cid, fid, line_no, section FROM chunks WHERE cid IN (%s)" % qmarks,
            [c[1] for c in top_pairs])}
    chunk_hits = []
    for sc, cid, line_no, section in top_pairs:
        meta = cid2meta.get(cid)
        if not meta:
            continue
        fid = meta[0]
        row = cur.execute("SELECT body FROM chunks WHERE cid=?", (cid,)).fetchone()
        body = row[0] if row else ""
        if not text_valid(body, ascii_res, terms):  # Issue#2
            continue
        chunk_hits.append({"fid": fid, "cid": cid, "line": line_no,
                           "section": section, "body": body, "score": sc})
        if len(chunk_hits) >= 500:
            break
    chunk_hits.sort(key=lambda x: -x["score"])

    # 3) 组装：文件记录 + 每文件最佳段落
    files = {r[0]: r for r in cur.execute(
        "SELECT fid,path,kind,title,summary,nchars,dup_group,content_sha,nlines,ocr_like FROM files")}
    best_chunk = {}
    for ch in chunk_hits:
        fid = ch["fid"]
        if fid not in best_chunk or ch["score"] > best_chunk[fid]["score"]:
            best_chunk[fid] = ch

    def make_result(fid, sc, ch):
        f = files[fid]
        return {
            "score": round(sc, 2), "kind": f[2], "title": f[3],
            "path": f[1].replace("\\", "/"),  # 相对工作区根，如 kb/source/...
            "line": ch["line"] if ch else None,
            "section": ch["section"] if ch else "",
            "snippet": (re.sub(r"\s+", " ", ch["body"])[:160] if ch else f[4]),
            "tags": build_tags(f),
        }

    results = []
    for fid, sc in sorted(hits.items(), key=lambda kv: -kv[1])[:limit * 5]:
        if fid not in files:
            continue
        f = files[fid]
        # 文件级有效性：title/summary 子串整词校验（keywords 命中已由 FTS 保证）
        if not text_valid((f[3] or "") + " " + (f[4] or ""), ascii_res, terms):
            continue
        results.append(make_result(fid, sc, best_chunk.get(fid)))
        if len(results) >= limit * 2:
            break
    if not results:  # 文件级无命中但有段落命中
        for fid, ch in sorted(best_chunk.items(), key=lambda kv: -kv[1]["score"])[:limit]:
            if fid not in files:
                continue
            results.append(make_result(fid, ch["score"], ch))

    # 4) 重复组折叠：同 dup_group 只保留最优一条
    by_path = {v[1].replace("\\", "/"): v[6] for v in files.values()}
    final, folded = [], {}
    for r in results:
        g = by_path.get(r["path"], "")
        if g:
            if g in folded:
                folded[g] += 1
                continue
            folded[g] = 1
        final.append(r)
    final = final[:limit]

    # 5) 索引过期检测（Issue#3）
    stale, checked = 0, 0
    if stale_check:
        final_rels = {r["path"] for r in final}
        probe_fids = [k for k, v in files.items()
                      if v[1].replace("\\", "/") in final_rels][:10]
        stale, checked = check_stale(cur, probe_fids)

    extra = []
    if deep:
        for ch in chunk_hits:
            f = files.get(ch["fid"])
            if not f:
                continue
            extra.append({"kind": f[2], "title": f[3],
                          "path": f[1].replace("\\", "/"),
                          "line": ch["line"], "section": ch["section"],
                          "snippet": re.sub(r"\s+", " ", ch["body"])[:160],
                          "tags": build_tags(f)})
        extra = extra[:limit * 3]
    return final, extra, terms, {"stale": stale, "checked": checked}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+", help="查询词（空格分隔多词，OR 关系）")
    ap.add_argument("--type", choices=["md", "code", "text"])
    ap.add_argument("--deep", action="store_true", help="追加段落级深挖结果")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--rebuild-if-stale", action="store_true",
                    help="检测到索引过期时自动重跑 p3+p4 后重查")
    ap.add_argument("--no-stale-check", action="store_true", help="跳过索引新鲜度抽查")
    a = ap.parse_args()
    query = " ".join(a.query)  # Issue#1

    res, extra, terms, st = search(query, a.type, a.deep, a.limit,
                                   stale_check=not a.no_stale_check)
    if st["stale"] and a.rebuild_if_stale:
        for script in ("p3_meta.py", "p4_build_index.py"):
            r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                               capture_output=True, text=True, creationflags=0x08000000)
            if r.returncode != 0:
                print("rebuild failed at %s:\n%s" % (script, r.stderr[-400:]))
                sys.exit(2)
        res, extra, terms, st = search(query, a.type, a.deep, a.limit, stale_check=True)

    stale_note = ""
    if st["stale"]:
        stale_note = ("⚠ 索引过期：抽查 %d 个命中文件中 %d 个内容已变更（行号可能漂移），"
                      "请重跑 p3_meta.py + p4_build_index.py，或加 --rebuild-if-stale"
                      % (st["checked"], st["stale"]))
    if a.json:
        print(json.dumps({"expanded_terms": terms, "stale": st,
                          "warning": stale_note or None,
                          "hits": res, "deep": extra},
                         ensure_ascii=False, indent=1))
        return
    out = []
    if stale_note:
        out.append(stale_note)
        out.append("")
    out.append("扩展词: " + " | ".join(terms[:12]))
    out.append("命中: %d 条" % len(res))
    out.append("")
    for i, r in enumerate(res, 1):
        loc = "%s:%s" % (r["path"], r["line"] or "-")
        out.append("%2d. [%s] %s" % (i, "/".join(r["tags"]), r["title"]))
        if r["section"]:
            out.append("    小节: %s" % r["section"])
        out.append("    位置: %s" % loc)
        out.append("    摘要: %s" % r["snippet"])
    if extra:
        out.append("")
        out.append("── 段落级深挖（前 %d 条）──" % len(extra))
        for i, r in enumerate(extra, 1):
            out.append("%2d. %s:%s  %s" % (i, r["path"], r["line"], r["snippet"][:100]))
    print("\n".join(out))


if __name__ == "__main__":
    main()
