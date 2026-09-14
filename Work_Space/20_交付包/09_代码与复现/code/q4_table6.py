# -*- coding: utf-8 -*-
"""表6 抽样：每 6 h x (0/0.5/1.0/1.5 cm + 药材表面) + 烘干结束行。"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, '..', 'results', 'result4_data.csv')
rows = list(csv.reader(open(src, encoding='utf-8')))
hdr = rows[0]
cols = [1, 6, 11, 16, 21]           # 0, 0.5, 1.0, 1.5, 药材表面
out = []
for r in rows[1:]:
    t = float(r[0])
    if abs(t % 21600.0) < 1e-6:
        out.append((t, [r[c] if r[c] != '' else None for c in cols]))
    elif t != int(t):               # 精确 t_dry 行（非整数秒）
        out.append((t, [r[c] if r[c] != '' else None for c in cols]))
lines = ['时间/h,0 cm,0.5 cm,1.0 cm,1.5 cm,药材表面']
md = ['| 时间/h | 0 cm | 0.5 cm | 1.0 cm | 1.5 cm | 药材表面 |', '|---|---|---|---|---|---|']
for (t, v) in out:
    is_end = t != int(t)
    label = ('%.4f' % (t / 3600.0)) if is_end else str(int(t // 3600.0))
    if is_end:
        label = '烘干结束(%.4f h)' % (t / 3600.0)
    vals = ['' if x is None else '%.4f' % float(x) for x in v]
    lines.append(label + ',' + ','.join(vals))
    md.append('| ' + label + ' | ' + ' | '.join(vals) + ' |')
dst = os.path.join(HERE, '..', 'results', 'table6.csv')
open(dst, 'w', encoding='utf-8').write('\n'.join(lines))
print('\n'.join(md))
print('WROTE', dst)
