# -*- coding: utf-8 -*-
"""P2 规则化精修：仅处理名字含"提取后"目录下的 .md（动态发现；原始区永不修改）。
⚠ 约束：本引擎任何脚本禁止用 os.remove / shutil.rmtree 删除语料或索引文件
  （会触发环境安全删除保护导致进程异常）；需要清理时一律移动到 source/temp 隔离目录。
规则全部保守、可回滚：
  R1 汉字间空格折叠（OCR 伪影；跳过代码块与含反引号的行）
  R2 营销水印行降级为引用块（保留原文文字，加 "> " 前缀）
  R3 形近字上下文修正：弟(?=数字/中文数字+步天章节等) -> 第
  R4 连续 3+ 空行折叠为 1 个空行
改动前先整份备份到 data/p2_backup/<原相对路径>。
输出：data/p2_refine_report.txt
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(HERE), "source")  # 动态推导，kb 可整体移动
DATA = os.path.join(HERE, "data")
BACKUP = os.path.join(DATA, "p2_backup")
# 动态发现：只精修名字含"提取后"的目录（原始区永不修改）；新增批次自动纳入
AREAS = [d for d in os.listdir(ROOT)
         if os.path.isdir(os.path.join(ROOT, d)) and "提取后" in d]
CJK = r'[\u4e00-\u9fff\u3400-\u4dbf\u3001-\u303f\uff01-\uff5e]'
R1 = re.compile(r'(?<=%s)[ \t]{1,}(?=%s)' % (CJK, CJK))
R2 = re.compile(r'(微信公众号【|公众号[：:]?\s*数学建模|QQ群[：:]?\s*\d{4,}|'
                r'扫码关注|扫码添加|关注公众号|领取更多|完整资料领取|粉丝群)')
R3 = re.compile(r'弟(?=[0-9一二三四五六七八九十百]+\s*[步天章节讲课部分])')


def refine(text):
    stats = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
    lines = text.split("\n")
    in_fence = False
    out = []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence and "`" not in ln:
            new, n1 = R1.subn("", ln)
            if n1:
                stats["R1"] += n1
            ln2, n3 = R3.subn("第", new)
            if n3:
                stats["R3"] += n3
            if R2.search(ln2) and not ln2.lstrip().startswith(">"):
                ln2 = "> " + ln2.lstrip()
                stats["R2"] += 1
            out.append(ln2)
        else:
            out.append(ln)
    body = "\n".join(out)
    # R4: 3+ 连续空行 -> 1 空行
    new_body, n4 = re.subn(r"\n{4,}", "\n\n", body)
    if n4:
        stats["R4"] += n4
    return new_body, stats


def main():
    changed, total = 0, 0
    report = ["# P2 精修报告\n"]
    for area in AREAS:
        base = os.path.join(ROOT, area)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != "_无效内容"]
            for fn in filenames:
                if not fn.lower().endswith(".md"):
                    continue
                total += 1
                full = os.path.join(dirpath, fn)
                with open(full, "rb") as f:
                    raw = f.read()
                try:
                    text = raw.decode("utf-8")
                    enc = "utf-8"
                except UnicodeDecodeError:
                    text = raw.decode("gbk", errors="replace")
                    enc = "gbk"
                new_text, stats = refine(text)
                if new_text == text:
                    continue
                changed += 1
                rel = os.path.relpath(full, ROOT)
                dst = os.path.join(BACKUP, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst):
                    with open(full, "rb") as fsrc, open(dst, "wb") as fdst:
                        shutil.copyfileobj(fsrc, fdst)
                with open(full, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new_text)
                report.append("- %s [%s] %s" % (rel, enc,
                                 ", ".join("%s=%d" % kv for kv in stats.items() if kv[1])))
    report.insert(1, "\n- 扫描 md 总数: %d\n- 修改文件数: %d\n- 备份目录: %s\n"
                  % (total, changed, BACKUP))
    with open(os.path.join(DATA, "p2_refine_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("P2 done. md=%d changed=%d" % (total, changed))


if __name__ == "__main__":
    main()
