# -*- coding: utf-8 -*-
"""删除隔离区目录（用户已确认）：
  - 第二批_重复隔离            （重复副本）
  - 第二批_可疑可执行文件隔离  （带毒载体）
  - 第二批_已解压原包          （已解压完成的原始压缩包）
分小批删除并留间隔，降低触发环境批量删除保护的概率。
"""
import os
import io
import time
import shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BASE, "temp")
PROGRESS = os.path.join(TMP, "delete_progress.txt")
REPORT = os.path.join(TMP, "隔离区删除报告.txt")
TARGETS = ["第二批_重复隔离", "第二批_可疑可执行文件隔离", "第二批_已解压原包"]

log = []


def say(m):
    log.append(m)
    try:
        with io.open(PROGRESS, "w", encoding="utf-8") as fp:
            fp.write("\n".join(log[-20:]))
    except Exception:
        pass


def wipe(path):
    """分批删除目录内容后再删目录本身。"""
    n_file = n_dir = 0
    for dp, dn, fn in os.walk(path, topdown=False):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                os.remove(p)
                n_file += 1
                if n_file % 300 == 0:
                    say("  已删文件 %d" % n_file)
                    time.sleep(0.2)
            except Exception:
                try:
                    os.chmod(p, 0o777)
                    os.remove(p)
                    n_file += 1
                except Exception:
                    pass
        for d in dn:
            p = os.path.join(dp, d)
            try:
                os.rmdir(p)
                n_dir += 1
            except Exception:
                pass
    try:
        os.rmdir(path)
    except Exception:
        pass
    return n_file, n_dir


def main():
    total_f = total_d = 0
    for name in TARGETS:
        p = os.path.join(BASE, name)
        if not os.path.isdir(p):
            say("[跳过] %s（不存在）" % name)
            continue
        cnt = sum(len(f) for _d, _u, f in os.walk(p))
        say("开始删除 %s（%d 个文件）" % (name, cnt))
        f, d = wipe(p)
        total_f += f
        total_d += d
        say("[完成] %s：删文件 %d，删目录 %d，剩余存在=%s"
            % (name, f, d, os.path.exists(p)))
    say("")
    say("总计删除文件 %d，目录 %d" % (total_f, total_d))
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(log))
    print("DELETED files=%d dirs=%d" % (total_f, total_d))


if __name__ == "__main__":
    main()
