# -*- coding: utf-8 -*-
import io
import sys
import re
sys.path.insert(0, r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp")
import fix_ocr_md as fx

p = r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\第一批提取后\老哥讲义！2026数学建模国赛冲奖要点全解析！.md"
md = io.open(p, encoding="utf-8").read()
lines = md.split("\n")
pages = fx.split_pages(lines)
out = []
for no, body in pages:
    if no != 20:
        continue
    i = 0
    while i < len(body):
        s = body[i].strip()
        if fx.RE_HEADING.match(s) and fx.looks_like_cell(fx.RE_HEADING.match(s).group(2)):
            j = i
            block = []
            while j < len(body):
                t = body[j].strip()
                mh = fx.RE_HEADING.match(t)
                if mh and fx.looks_like_cell(mh.group(2)):
                    block.append(mh.group(2)); j += 1
                elif t and fx.looks_like_cell(t):
                    block.append(t); j += 1
                else:
                    break
            out.append("BLOCK len=%d first=%r last=%r" % (len(block), block[0] if block else "", block[-1] if block else ""))
            out.append("  try_table -> %r" % (fx.try_table(block) is not None,))
            if block:
                m = len(block)
                cands = [c for c in range(2, 9) if m % c == 0 and 2 <= m // c <= 25]
                out.append("  m=%d candidate cols=%s" % (m, cands))
            break
        i += 1
    break
io.open(r"C:\Users\wang-\Desktop\2026数学建模\2025国赛真题\B题\kb\source\temp\dbg.txt", "w", encoding="utf-8").write("\n".join(out))
print("\n".join(out))
