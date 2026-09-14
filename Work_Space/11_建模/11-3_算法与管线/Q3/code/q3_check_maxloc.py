# -*- coding: utf-8 -*-
"""Q3 复核：全域最大值位置（argmax）的异常定位。

查明 result3_raw.xlsx 中 argmax 非 0 的行，判断其为
"数值可分辨范围内的小抖动"还是"真实的违反"。
"""
import openpyxl
import numpy as np

wb = openpyxl.load_workbook('result3_raw.xlsx', read_only=True)
ws = wb.active
rows = [r for r in ws.iter_rows(values_only=True)]
data = np.array([[float(x) for x in r[1:]] for r in rows[1:]])
t = np.array([float(r[0]) for r in rows[1:]])
wb.close()

imax = np.argmax(data, axis=1)
u, c = np.unique(imax, return_counts=True)
print('  argmax 列分布:', dict(zip(u.tolist(), c.tolist())))
bad = np.argwhere(imax != 0).ravel()
print('  非 0 的行数: %d / %d' % (len(bad), len(imax)))
print()
for i in bad[:10]:
    r = data[i]
    print('    t=%9.1f s (%6.3f h)  argmax=%2d  C[0]=%.8f  C[1]=%.8f  diff=%+.3e'
          % (t[i], t[i] / 3600.0, imax[i], r[0], r[1], r[1] - r[0]))
print()
d01 = data[:, 1] - data[:, 0]
print('  C(0.1cm)-C(0) 的最大值 = %+.3e' % d01.max())
print('  C(0.1cm)-C(0) 的均值   = %+.3e' % d01.mean())
print()

# 判据关键复核：达标时刻的 max 位置
mm = data.max(axis=1)
k = int(np.argmax(mm < 0.15))
print('  ★ 达标时刻 t=%.1f s (%.4f h)：max=%.8f，位于第 %d 列 (r=%.1f cm)'
      % (t[k], t[k] / 3600.0, mm[k], np.argmax(data[k]), np.argmax(data[k]) * 0.1))
print('    该时刻 C(0)=%.8f  C(0.1cm)=%.8f  diff=%+.3e'
      % (data[k, 0], data[k, 1], data[k, 1] - data[k, 0]))

# 逐时刻中心是否严格为全场最大（用容差判据）
tol = 1e-6
viol = 0
for i in range(len(data)):
    if data[i, 0] < data[i].max() - tol:
        viol += 1
print()
print('  以容差 %.0e 判据（中心值低于全场最大值超过该容差才算违反）：违反 %d 行'
      % (tol, viol))
print('  ⟹ 若为 0，说明差异全在 %.0e 以下，属数值可分辨范围内的小抖动。' % tol)
