# -*- coding: utf-8 -*-
"""T1 增量更新验证。
步骤：
  1) 记录基线（files/chunks 数）
  2) 投放测试语料：kb/source/_engine_test/（唯一标记 md + 现有 md 的改名副本）
  3) 重跑 p3 -> p4
  4) 验证：新内容可查；副本与原文件在结果中折叠为一条；旧查询仍正常
  5) 撤除测试语料（移动到 temp，不物理删除），重跑 p3 -> p4
  6) 核对恢复到基线
输出：data/t1_incremental_report.txt
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = HERE
SRC = os.path.dirname(os.path.dirname(HERE))  # B题 根目录
SRC_KB = os.path.join(SRC, "kb", "source")
TEMP = os.path.join(SRC_KB, "temp")
TEST_DIR = os.path.join(SRC_KB, "_engine_test")
UNIQUE = "QZXUNIQ2026量子透射测厚法"
PY = sys.executable


def run(script):
    r = subprocess.run([PY, os.path.join(ENGINE, script)],
                       capture_output=True, text=True,
                       creationflags=0x08000000)
    if r.returncode != 0:
        raise RuntimeError("%s failed: %s" % (script, r.stderr[-500:]))
    return r.stdout.strip().splitlines()[-1] if r.stdout else ""


def counts():
    sys.path.insert(0, ENGINE)
    import sqlite3
    con = sqlite3.connect(os.path.join(ENGINE, "data", "catalog.db"))
    n_f = con.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    n_c = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    con.close()
    return n_f, n_c


def query_hit(term):
    sys.path.insert(0, ENGINE)
    from p5_search import search
    res, extra, _, _ = search(term, deep=True, limit=20)
    paths = [r["path"] for r in res] + [r["path"] for r in extra]
    return paths


def main():
    rep = ["# T1 增量更新验证\n"]
    base_f, base_c = counts()
    rep.append("- 基线: files=%d chunks=%d" % (base_f, base_c))

    # 2) 投放测试语料
    os.makedirs(TEST_DIR, exist_ok=True)
    probe_path = os.path.join(TEST_DIR, "增量测试_唯一方法.md")
    with open(probe_path, "w", encoding="utf-8") as f:
        f.write("# %s\n\n本文档用于验证搜索引擎增量更新。%s 是一个库中不存在的方法名，"
                "正文含唯一探针串 %s。\n\n## 原理\n\n该方法通过 %s 探针验证文件级与段落级检索。\n"
                % (UNIQUE, UNIQUE, UNIQUE, UNIQUE))
    dup_src = os.path.join(SRC_KB, "第一批提取后", "AI 工具使用详情.md")
    dup_dst = os.path.join(TEST_DIR, "重复副本_改名测试.md")
    shutil.copyfile(dup_src, dup_dst)
    rep.append("- 投放: _engine_test/增量测试_唯一方法.md + 重复副本_改名测试.md(=第一批 AI工具使用详情.md)")

    # 3) 重跑
    rep.append("- p3: " + run("p3_meta.py"))
    rep.append("- p4: " + run("p4_build_index.py"))
    inc_f, inc_c = counts()
    rep.append("- 增量后: files=%d (+%d) chunks=%d (+%d)"
               % (inc_f, inc_f - base_f, inc_c, inc_c - base_c))

    # 4) 验证
    sys.path.insert(0, ENGINE)
    paths = query_hit(UNIQUE)
    hit_new = any("_engine_test" in p for p in paths)
    rep.append("- 新文件命中(文件级/段落级): %s -> %s" % (hit_new, paths[:2]))
    dup_paths = query_hit("AI红线检测")
    n_dup = sum(1 for p in dup_paths if "_engine_test" in p)
    rep.append("- 副本折叠: 查询副本独有词命中 %d 条结果中，副本出现 %d 次（期望 0~1，且与原文件只留一条）"
               % (len(dup_paths[:5]), n_dup))
    old_paths = query_hit("蒙特卡洛")
    rep.append("- 旧查询回归: '蒙特卡洛' 仍命中 %d 条" % len(old_paths))

    # 5) 撤除
    dst = os.path.join(TEMP, "_engine_test_removed")
    if os.path.exists(dst):
        shutil.rmtree(dst, ignore_errors=True)
    shutil.move(TEST_DIR, dst)
    rep.append("- p3: " + run("p3_meta.py"))
    rep.append("- p4: " + run("p4_build_index.py"))
    fin_f, fin_c = counts()
    rep.append("- 撤除后: files=%d chunks=%d (基线 %d/%d, 差异 f=%d c=%d)"
               % (fin_f, fin_c, base_f, base_c, fin_f - base_f, fin_c - base_c))
    ok = (fin_f == base_f)
    rep.append("- 结论: 增量更新%s" % ("通过" if ok and hit_new else "存在差异，见上文明细"))
    with open(os.path.join(ENGINE, "data", "t1_incremental_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("T1 done. result=%s" % ("PASS" if ok and hit_new else "CHECK"))


if __name__ == "__main__":
    main()
