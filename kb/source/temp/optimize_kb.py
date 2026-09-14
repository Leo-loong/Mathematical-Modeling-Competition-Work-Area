# -*- coding: utf-8 -*-
"""知识库净化：把「数据型 / 无效型」Markdown 移出主目录，避免 Agent 浪费上下文。

判定：
  数据型 = 中文占比极低(<3%) 且（数字+符号+空白）占比高(>70%) 且 长度>5000
          典型：pca 的 input.md（数值矩阵）、测试数据集、编码输出
  无效型 = 有效字符 < 50（空文件、转换失败残留）

处理：移动到 提取后/_数据文件/ 或 提取后/_无效内容/（保留不删除，可回查）
"""
import os
import io
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = [os.path.join(BASE, "第一批提取后"), os.path.join(BASE, "第二批提取后")]
REPORT = os.path.join(BASE, "temp", "知识库净化报告.txt")
CJK = re_cjk = None
import re
CJK = re.compile(r"[\u4e00-\u9fa5]")
DS = re.compile(r"[0-9\s\.\,\;\:\+\-\*\/\(\)\[\]\{\}\=\<\>\|]")

log = []


def uniq(dst):
    if not os.path.exists(dst):
        return dst
    root, ext = os.path.splitext(dst)
    i = 1
    while os.path.exists("%s__%d%s" % (root, i, ext)):
        i += 1
    return "%s__%d%s" % (root, i, ext)


def main():
    moved_data = moved_bad = 0
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        ddir = os.path.join(root, "_数据文件")
        bdir = os.path.join(root, "_无效内容")
        for dp, dn, fn in os.walk(root):
            if "_数据文件" in dp or "_无效内容" in dp:
                continue
            for f in list(fn):
                if not f.lower().endswith(".md"):
                    continue
                p = os.path.join(dp, f)
                try:
                    raw = open(p, "rb").read()
                    if raw.startswith(b"\xef\xbb\xbf"):
                        raw = raw[3:]
                    text = raw.decode("utf-8", errors="replace")
                except Exception:
                    continue
                n = max(1, len(text))
                cjk = len(CJK.findall(text))
                ds = len(DS.findall(text))
                cjk_r = cjk / float(n)
                ds_r = ds / float(n)
                rel = os.path.relpath(p, root)
                target = None
                if len(text.strip()) < 50:
                    target = os.path.join(bdir, rel)
                    moved_bad += 1
                    log.append("[无效] %s (%d 字符)" % (rel, len(text.strip())))
                elif cjk_r < 0.03 and ds_r > 0.70 and len(text) > 5000:
                    target = os.path.join(ddir, rel)
                    moved_data += 1
                    log.append("[数据型] %s (中文%.2f%% 数据%.0f%% %d字符)"
                               % (rel, cjk_r * 100, ds_r * 100, len(text)))
                if target:
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    shutil.move(p, uniq(target))
        log.append("")
    log.append("移出数据型: %d，移出无效型: %d" % (moved_data, moved_bad))
    for root in ROOTS:
        if os.path.isdir(root):
            n = sum(len(f) for d, _u, f in os.walk(root)
                    if "_数据文件" not in d and "_无效内容" not in d)
            log.append("%s 主目录剩余 md: %d" % (os.path.basename(root), n))
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("DATA=%d BAD=%d" % (moved_data, moved_bad))


if __name__ == "__main__":
    main()
