# -*- coding: utf-8 -*-
"""重复组「最优副本」选择 + 交换。

评分原则（优先级从高到低）：
  1) 【组完整性】所在目录聚集度：若某目录本身是完整资料包（含大量重复组成员），
     优先保留该目录下的副本 —— 即使别处副本的文件名更规范，也不拆散现有组。
  2) 【文件名规范】无 (1)/(2)、副本、复件、copy、新建 等重复下载痕迹；无乱码。
  3) 【路径规范】层级适中、不含「新建文件夹/临时/备份/旧版」等。
  4) 【内容完整】字符数更多、可正常解析（PDF 有文本层、docx 可打开）优先。

输出: temp/最优副本选择报告.txt   进度: temp/pick_progress.txt
"""
import os
import io
import re
import sys
import shutil
import hashlib
from collections import defaultdict, Counter

TMP = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TMP)
B2 = os.path.join(BASE, "第二批")
QUAR = os.path.join(BASE, "第二批_重复隔离")
PROGRESS = os.path.join(TMP, "pick_progress.txt")
REPORT = os.path.join(TMP, "最优副本选择报告.txt")
# 需要跳过的目录关键字（逗号分隔）；环境变量为空表示全量处理
EXCLUDE = [k for k in (os.environ.get("KB_SKIP") or "").split(",") if k]
MIN_CHARS = 100

sys.path.insert(0, TMP)
import scan_index as si  # noqa: E402

log = []


def say(m):
    log.append(m)
    print(m)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as fp:
            fp.write("\n".join(log[-30:]))
    except Exception:
        pass


def excluded(p):
    return any(k in p for k in EXCLUDE)


BAD_NAME = re.compile(r"\(\d+\)|（\d+）|\s-\s*副本|副本|复件|copy|Copy|新建|~\)|^\d+$")
BAD_PATH = re.compile(r"新建文件夹|未命名|临时|temp|Temp|备份|旧版|副本|复件|混乱|杂项")
GARBAGE = re.compile(r"[\ue000-\uf8ff\ufffd]")


def name_score(fname):
    s = 0.0
    stem = os.path.splitext(fname)[0]
    if BAD_NAME.search(stem):
        s -= 40
    if GARBAGE.search(fname):
        s -= 25
    if len(stem) < 2:
        s -= 15
    if "  " in fname or fname != fname.strip():
        s -= 10
    return s


def path_score(rel):
    s = 0.0
    parts = rel.split(os.sep)
    depth = len(parts) - 1
    if depth > 7:
        s -= 10
    if BAD_PATH.search(rel):
        s -= 30
    if len(rel) > 160:
        s -= 10
    # 语义化目录名（含明确主题词）轻微加分
    if any(k in rel for k in ("国赛", "美赛", "算法", "模型", "论文", "代码", "资料", "模板", "优秀")):
        s += 5
    return s


def scan_all():
    """返回 [(tag, rel, md5, sha1, chars, note, size)]，tag ∈ b2/quar。"""
    rows = []
    for root, tag in ((B2, "b2"), (QUAR, "quar")):
        n = 0
        for dp, _dn, fn in os.walk(root):
            if excluded(dp):
                continue
            for f in fn:
                if f.startswith("~$"):
                    continue
                p = os.path.join(dp, f)
                try:
                    md5 = si.file_md5(p)
                except Exception:
                    continue
                rows.append(dict(tag=tag, rel=os.path.relpath(p, root), md5=md5,
                                 sha1="", chars=0, note="", size=os.path.getsize(p)))
                n += 1
                if n % 3000 == 0:
                    say("扫描 %s: %d" % (tag, n))
        say("扫描完成 %s: %d" % (tag, n))
    return rows


def fill_content(rows):
    """同一 md5 只提取一次文本（组内字节必然相同）。"""
    by_md5 = defaultdict(list)
    for r in rows:
        by_md5[r["md5"]].append(r)
    say("唯一 md5: %d（逐个提取文本）" % len(by_md5))
    for i, (md5, lst) in enumerate(by_md5.items(), 1):
        rep = None
        for r in lst:
            if r["tag"] == "b2":
                rep = r
                break
        rep = rep or lst[0]
        root = B2 if rep["tag"] == "b2" else QUAR
        p = os.path.join(root, rep["rel"])
        ext = os.path.splitext(p)[1].lower()
        try:
            text, note = si.extract(p, ext)
            norm = re.sub(r"\s+", "", text)
            sha1 = hashlib.sha1(norm.encode("utf-8", "ignore")).hexdigest()
            chars = len(text)
        except Exception as e:
            sha1, chars, note = "", 0, "ERR %s" % e
        for r in lst:
            r["sha1"] = sha1
            r["chars"] = chars
            r["note"] = note
        if i % 2000 == 0:
            say("文本提取 %d/%d" % (i, len(by_md5)))


def build_groups(rows):
    """先按 md5，再把「md5 不同但内容相同」的合并。"""
    by_md5 = defaultdict(list)
    for r in rows:
        by_md5[r["md5"]].append(r)
    groups = list(by_md5.values())
    # sha1 二级合并
    by_sha = defaultdict(list)
    for g in groups:
        s = usable(g[0])
        if s:
            by_sha[s].append(g)
    merged = []
    used = set()
    for s, glist in by_sha.items():
        if len(glist) > 1:
            flat = [r for g in glist for r in g]
            merged.append(flat)
            for g in glist:
                used.add(id(g))
    for g in groups:
        if id(g) not in used:
            merged.append(g)
    return [g for g in merged if len(g) > 1]


def usable(r):
    if not r["sha1"]:
        return None
    if r["chars"] < MIN_CHARS:
        return None
    if r["note"] in ("NO_TEXT_LAYER", "DOC_LEGACY", "UNSUPPORTED", "MD5_ONLY"):
        return None
    return r["sha1"]


def uniq_dest(dst):
    if not os.path.exists(dst):
        return dst
    root, ext = os.path.splitext(dst)
    i = 1
    while os.path.exists("%s__dup%d%s" % (root, i, ext)):
        i += 1
    return "%s__dup%d%s" % (root, i, ext)


def main():
    rows = scan_all()
    say("纳入文件: %d" % len(rows))
    fill_content(rows)
    groups = build_groups(rows)
    say("重复组: %d" % len(groups))

    # 目录聚集度：每个目录下「属于重复组」的成员数（当前在第二批的）
    dup_members = set()
    for g in groups:
        for r in g:
            if r["tag"] == "b2":
                dup_members.add(r["rel"])
    dir_cnt = Counter(os.path.dirname(r) for r in dup_members)
    max_cnt = max(dir_cnt.values()) if dir_cnt else 1
    say("目录聚集度: 最大 %d，目录数 %d" % (max_cnt, len(dir_cnt)))

    def score(r):
        d = os.path.dirname(r["rel"])
        s = 60.0 * (dir_cnt.get(d, 0) / float(max_cnt))      # 组完整性（最高权重）
        s += name_score(os.path.basename(r["rel"]))
        s += path_score(r["rel"])
        s += min(r["chars"] / 2000.0, 8.0)                    # 内容完整度（小幅）
        if r["note"] in ("NO_TEXT_LAYER", "DOC_LEGACY") or str(r["note"]).startswith("ERR"):
            s -= 15
        return s

    swapped = 0
    changed = []
    for g in groups:
        b2_members = [r for r in g if r["tag"] == "b2"]
        if not b2_members:
            continue
        cur = b2_members[0]
        best = max(g, key=score)
        if best is cur or best["rel"] == cur["rel"]:
            continue
        if score(best) - score(cur) < 5:      # 差异不显著则不折腾
            continue
        src_keep = os.path.join(B2, cur["rel"])
        dst_keep = uniq_dest(os.path.join(QUAR, cur["rel"]))
        src_best = os.path.join(QUAR, best["rel"])
        dst_best = os.path.join(B2, best["rel"])
        if not (os.path.exists(src_keep) and os.path.exists(src_best)):
            continue
        try:
            os.makedirs(os.path.dirname(dst_keep), exist_ok=True)
            shutil.move(src_keep, dst_keep)
            os.makedirs(os.path.dirname(dst_best), exist_ok=True)
            shutil.move(src_best, dst_best)
            swapped += 1
            if len(changed) < 60:
                changed.append("组: %s\n   原保留: %s (%.1f)\n   改为:   %s (%.1f)" % (
                    os.path.basename(cur["rel"]), cur["rel"], score(cur),
                    best["rel"], score(best)))
        except Exception as e:
            say("交换失败 %s -> %s : %r" % (cur["rel"], best["rel"], e))
        if swapped % 300 == 0:
            say("已交换 %d 组" % swapped)

    say("")
    say("发生交换的组: %d / %d" % (swapped, len(groups)))
    out = list(log)
    out.append("")
    out.append("## 交换明细（前 %d 条）" % len(changed))
    out.extend(changed)
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))
    print("PICK DONE swapped=%d" % swapped)


if __name__ == "__main__":
    main()
