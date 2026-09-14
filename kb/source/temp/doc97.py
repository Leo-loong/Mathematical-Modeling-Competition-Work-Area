# -*- coding: utf-8 -*-
"""doc97.py -- 纯 Python 抽取 Word 97-2003 (.doc, OLE2) 正文文本。

思路：OLE2 复合文档的 WordDocument 流里，FIB 的 fcMin/fcMac 指向正文区间；
按 fCompressed 判断是 8-bit(GBK/CP1252) 还是 UTF-16LE 存储，解出后清理控制符。
速度快（毫秒级）、零 COM 依赖、不会因 Office 缺失或文件轻微损坏而失败。
"""
import re
import struct

try:
    import olefile
except ImportError:
    olefile = None

CTRL = re.compile(r"[\x00-\x08\x0b-\x1f]")


def _score(t):
    """按“中文/ASCII 占比”给候选解码打分，用来在 UTF-16LE 与 GBK 之间自动择优。"""
    s = 0
    for ch in t[:4000]:
        o = ord(ch)
        if 0x4E00 <= o <= 0x9FFF or 0x3000 <= o <= 0x303F or 0xFF00 <= o <= 0xFFEF:
            s += 3
        elif 32 <= o < 127 or o in (9, 10, 13):
            s += 1
        elif 0x0080 <= o <= 0x00FF or o == 0xFFFD:
            s -= 3
        else:
            s -= 1
    return s


def _clean(text):
    text = text.replace("\r", "\n")
    text = text.replace("\x07", "\t")   # 单元格/行结束
    text = text.replace("\x0b", "\n")
    text = CTRL.sub("", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract(path):
    if olefile is None:
        return "", "缺 olefile"
    try:
        ole = olefile.OleFileIO(path)
    except Exception as e:
        return "", "OLE 打开失败: %s" % (repr(e)[:60],)
    try:
        if not ole.exists("WordDocument"):
            return "", "无 WordDocument 流"
        data = ole.openstream("WordDocument").read()
    finally:
        ole.close()

    if len(data) < 64:
        return "", "流过短"

    try:
        flags = struct.unpack_from("<H", data, 0x0A)[0]
        fcMin, fcMac = struct.unpack_from("<II", data, 0x18)
    except Exception:
        return "", "FIB 解析失败"

    # 某些文件 FIB 的 fcMin/fcMac 落在备选位置（0x0154/0x0158，FibRgFcLcb 之后）
    if not (0 < fcMin < fcMac <= len(data)):
        for off in (0x0154, 0x00DC, 0x011A):
            try:
                a, b = struct.unpack_from("<II", data, off)
                if 0 < a < b <= len(data):
                    fcMin, fcMac = a, b
                    break
            except Exception:
                continue
    if not (0 < fcMin < fcMac <= len(data)):
        fcMin, fcMac = 0, len(data)

    body = data[fcMin:fcMac]

    cands = []
    if len(body) % 2 == 0:
        try:
            cands.append(body.decode("utf-16-le", errors="replace"))
        except Exception:
            pass
    for enc in ("gb18030", "cp1252", "utf-8"):
        try:
            cands.append(body.decode(enc, errors="replace"))
        except Exception:
            pass
    if not cands:
        return "", "解码失败"
    text = max(cands, key=_score)
    return _clean(text), ""


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        t, err = extract(p)
        print("=" * 20, p, "len=%d" % len(t), err)
        print(t[:400])
