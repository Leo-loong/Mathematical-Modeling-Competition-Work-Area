# -*- coding: utf-8 -*-
"""ppt97.py -- 纯 Python 抽取 PowerPoint 97-2003 (.ppt, OLE2) 文本。

原理：PowerPoint Document 流由「记录头(8B) + 数据」顺序组成，
正文存放在 TextBytesAtom(0x0FA0, 单字节) / TextCharsAtom(0x0FA8, UTF-16LE) 中。
线性扫描即可按幻灯片顺序拿到全部文字，无需 COM / LibreOffice。
"""
import re
import struct

try:
    import olefile
except ImportError:
    olefile = None

TEXT_CHARS_ATOM = 0x0FA0   # UTF-16LE 文本
TEXT_BYTES_ATOM = 0x0FA8   # 单字节文本
CTRL = re.compile(r"[\x00-\x08\x0b-\x1f]")


def extract(path):
    if olefile is None:
        return "", "缺 olefile"
    try:
        ole = olefile.OleFileIO(path)
    except Exception as e:
        return "", "OLE 打开失败: %s" % (repr(e)[:60],)
    try:
        if not ole.exists("PowerPoint Document"):
            return "", "无 PowerPoint Document 流"
        data = ole.openstream("PowerPoint Document").read()
    finally:
        ole.close()

    out = []
    pos, n = 0, len(data)
    while pos + 8 <= n:
        try:
            rec_type, rec_len = struct.unpack_from("<HI", data, pos + 2)
        except Exception:
            break
        body_start = pos + 8
        body_end = body_start + rec_len
        if rec_len < 0 or body_end > n:
            break
        if rec_type == TEXT_BYTES_ATOM:
            try:
                out.append(data[body_start:body_end].decode("gb18030", "replace"))
            except Exception:
                pass
        elif rec_type == TEXT_CHARS_ATOM:
            try:
                out.append(data[body_start:body_end].decode("utf-16-le", "replace"))
            except Exception:
                pass
        pos = body_end

    text = "\n".join(x for x in out if x.strip())
    text = text.replace("\r", "\n").replace("\x0b", "\n")
    text = CTRL.sub("", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), ""


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        t, err = extract(p)
        print("=" * 20, p, "len=%d" % len(t), err)
        print(t[:400])
