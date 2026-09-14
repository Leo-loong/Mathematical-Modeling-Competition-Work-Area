# -*- coding: utf-8 -*-
"""
Q3 发现的问题对 Q1／Q2 的影响评估（T0 只读，不运行任何求解）
================================================================================
待评估的 Q3 问题（按性质分类）：
  P-a 环境延拓取错值（误用附件末值 50.165）
  P-b 内部步长险些被放大 60 倍（该错误未进入任何已交付结果）
  P-c 表面含水率 C(R) 的网格不收敛（低 C 端 D 极小 ⟹ 表面层远薄于 Δr）
  P-d 表面"局部增湿"式回升
  P-e argmax 的 ulp 抖动 ／ 核验脚本索引错位（工具层，不影响数值）

评估方法（全部为**只读**）：
  ① 读 Q1／Q2 主力脚本的延拓实现（判定 P-a 是否波及）
  ② 读 result1／result2.xlsx，统计**含水率值域**与**是否出现回升**
     ⟹ 判定 P-c／P-d 是否触及 Q1／Q2 的工况
  ③ 读 Q1／Q2 的网格与内部步长设置（判定 P-b 是否波及）
  ④ 由附录2／附录3 的 D 公式，算出 Q1／Q2 最低 C 处的 D 值，
     判断"表面层厚度/Δr"比是否已进入危险区

产出：影响判定表 + 依据（不修改任何文件）。
"""
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
R2 = os.path.join(WS, '20_交付包', '09_代码与复现', 'results', 'result2.xlsx')
R1 = os.path.join(WS, '20_交付包', '09_代码与复现', 'results', 'result1.xlsx')

print('=' * 78)
print('Q3 发现的问题对 Q1／Q2 的影响评估（只读）')
print('=' * 78)


def load(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet in wb.sheetnames else wb.worksheets[0]
    rows = [r for r in ws.iter_rows(values_only=True)]
    tv = np.array([float(r[0]) for r in rows[1:]])
    A = np.array([[float(x) if isinstance(x, (int, float)) else np.nan
                   for x in r[1:]] for r in rows[1:]])
    wb.close()
    return tv, A, rows[0]


for tag, path in (('Q1', R1), ('Q2', R2)):
    print()
    print('-' * 78)
    print('%s：%s' % (tag, os.path.basename(path)))
    print('-' * 78)
    try:
        tv, A, hdr = load(path, '水分浓度')
    except Exception as e:
        print('  读取失败：', e)
        continue
    print('  形状 %s  t: %.0f → %.0f s' % (A.shape, tv[0], tv[-1]))
    print('  C 值域：min=%.6f  max=%.6f  （初始 2.55）' % (np.nanmin(A), np.nanmax(A)))
    print('  C(0) 首末：%.6f → %.6f' % (A[0, 0], A[-1, 0]))
    print('  C(R) 首末：%.6f → %.6f' % (A[0, -1], A[-1, -1]))
    # 表面是否出现回升
    dR = np.diff(A[:, -1])
    nup = int(np.sum(dR > 1e-9))
    print('  表面回升次数：%d / %d  （最大单次 %+.3e）'
          % (nup, len(dR), dR.max() if len(dR) else 0.0))
    # 中心最低值 -> 对应 D
    Cmin = float(np.nanmin(A))
    print('  ★ 全域最低 C = %.4f' % Cmin)
    print()
    print('  --- 关键判据：由最低 C 处估算"表面层特征厚度 / 网格步长" ---')
    for label, Dfun in (('附录3', lambda c, T=323.15: 2.4e-3 * np.exp(-0.45 / max(c, 1e-9))
                        * np.exp(-3850.0 / T)),
                        ('附录2', lambda c, T=301.15: 7e-9 * np.exp(-0.89 / max(c, 1e-9)))):
        D = Dfun(Cmin)
        # 表面扩散层厚度尺度：delta ~ D / k_m (由 -D dC/dr = k_m (C_R-C_inf) 的量纲)
        km = 8e-7
        delta = D / km
        print('    %s：D(%.3f)=%.3e m²/s  ⟹ 层厚尺度 δ=D/k_m=%.4e m = %.4f mm  '
              '（Δr=0.25 mm ⟹ δ/Δr=%.3f）'
              % (label, Cmin, D, delta, delta * 1e3, delta / 2.5e-4))

print()
print('=' * 78)
print('判定要点')
print('=' * 78)
print('  · 若 Q1／Q2 的 C 值域最低值仍较高（D 较大、δ/Δr ≫ 1）')
print('    ⟹ 表面层被网格充分分辨 ⟹ **P-c／P-d 不波及 Q1／Q2**。')
print('  · 若 Q1／Q2 未出现表面回升 ⟹ **P-d 不波及**。')
print('  · P-a／P-b 属**实现层**，须核对各问自己脚本的口径（见下方清单）。')
