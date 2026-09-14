# -*- coding: utf-8 -*-
"""T3 索引过期检测验证（Issue#3）。
1) 备份目标 md 的原始字节；
2) 在文件头部插入 2 个空行（模拟外部修改造成的行号漂移，全部 line_no +2）；
3) 查询该文件特征词 -> 断言 stale 告警触发；
4) 字节级还原文件；重建 p4；
5) 再查询 -> 断言无告警。
⚠ 测试会对源文件做临时修改并字节级还原；若中途失败，原始字节保留在 data/_t3_orig.bin。
"""
import os
import sys
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = HERE
ROOT = os.path.dirname(os.path.dirname(HERE))
TARGET = os.path.join(ROOT, "kb", "source", "第一批提取后", "AI 工具使用详情.md")
ORIG_BAK = os.path.join(HERE, "data", "_t3_orig.bin")
TERM = "AI工具使用详情说明"
sys.path.insert(0, HERE)


def run(script):
    r = subprocess.run([sys.executable, os.path.join(ENGINE, script)],
                       capture_output=True, text=True, creationflags=0x08000000)
    if r.returncode != 0:
        raise RuntimeError("%s failed: %s" % (script, r.stderr[-400:]))


def query_stale():
    from p5_search import search
    res, extra, _, st = search(TERM, stale_check=True)
    hit = any("AI 工具使用详情" in r["path"] for r in res)
    return st, hit


def main():
    with open(TARGET, "rb") as f:
        orig = f.read()
    with open(ORIG_BAK, "wb") as f:
        f.write(orig)
    try:
        # 2) 头部插入 2 行制造漂移
        with open(TARGET, "wb") as f:
            f.write(b"\n\n" + orig)
        st1, hit1 = query_stale()
        assert hit1, "修改后查询未命中目标文件，测试前提不成立"
        assert st1["stale"] >= 1, "行号漂移未被检测到（stale=%s）" % st1
        print("step3 OK: stale=%d/%d (drift detected)" % (st1["stale"], st1["checked"]))

        # 4) 字节级还原 + 重建
        with open(TARGET, "wb") as f:
            f.write(orig)
        run("p4_build_index.py")
        st2, hit2 = query_stale()
        assert hit2, "还原后查询未命中目标文件"
        assert st2["stale"] == 0, "还原+重建后仍报过期（stale=%s）" % st2
        print("step5 OK: stale=0 (index fresh again)")
        print("T3 done. PASS")
    finally:
        # 兜底还原
        with open(ORIG_BAK, "rb") as f:
            bak = f.read()
        with open(TARGET, "wb") as f:
            f.write(bak)
        if os.path.exists(ORIG_BAK):
            os.remove(ORIG_BAK)  # 单文件删除（非批量），不触发批量保护；失败则留待手动


if __name__ == "__main__":
    main()
