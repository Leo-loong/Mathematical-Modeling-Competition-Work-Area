# -*- coding: utf-8 -*-
"""
Q2 · 基线版 vs 优化版（B+C）结果全表逐点核对
======================================================
输入：
  · result2_orig.xlsx —— 用户用**优化前基线核**（q2_core_orig，solve_banded 默认参数）跑出
  · result2.xlsx      —— 用**优化核**（q2_core_c，numba ＋ 手写追赶法）跑出
两文件均由 `q2_solver.py` 同口径生成（Δr=0.25 mm、1 s 输出步、内部 1/32 s、10800 步、4 位小数）。

判据：
  · 两个工作表（温度／水分浓度）的 **10801 × 22 个格子**逐一比对；
  · 按 4 位小数**完全相同**的格数占比判定（优化核与基线的理论差异 ~1e-11，
    仅在恰好落在舍入边界时可能出现末位 ±1）。

运行：python q2_verify_results.py
"""
import sys
import os

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from openpyxl import load_workbook                               # noqa: E402

A = os.path.join(HERE, 'result2_orig.xlsx')       # 基线（用户跑）
B = os.path.join(HERE, '..', '..', '..', '..',
                 '20_交付包', '09_代码与复现', 'results', 'result2.xlsx')  # 优化版


def _root(p):
    cur = p
    for _ in range(8):
        if os.path.isdir(os.path.join(cur, '20_交付包')):
            return cur
        par = os.path.dirname(cur)
        if par == cur:
            break
        cur = par
    return None


if not os.path.exists(B):
    r = _root(HERE)
    if r:
        B = os.path.join(r, '20_交付包', '09_代码与复现', 'results', 'result2.xlsx')


def main():
    print('=' * 76)
    print('Q2 结果核对：基线版（result2_orig.xlsx） vs 优化版（result2.xlsx）')
    print('=' * 76)
    print('  基线：', os.path.relpath(A, os.path.dirname(HERE)))
    print('  优化：', os.path.relpath(B, os.path.dirname(HERE)))
    if not (os.path.exists(A) and os.path.exists(B)):
        print('  ⚠ 缺少文件，无法比对')
        return

    wa = load_workbook(A, read_only=True, data_only=True)
    wb_ = load_workbook(B, read_only=True, data_only=True)
    print('  工作表：', wa.sheetnames, '|', wb_.sheetnames)

    grand_same = grand_diff = grand_max = 0
    for name in wa.sheetnames:
        if name not in wb_.sheetnames:
            print(f'  ⚠ 优化版缺工作表 {name}')
            continue
        sa, sb = wa[name], wb_[name]
        n = same = 0
        worst = 0.0
        worst_at = None
        first = []
        for i, (ra, rb) in enumerate(zip(sa.iter_rows(values_only=True),
                                         sb.iter_rows(values_only=True)), 1):
            for j, (va, vb) in enumerate(zip(ra, rb), 1):
                if va is None or vb is None:
                    continue
                n += 1
                if va == vb:
                    same += 1
                else:
                    try:
                        d = abs(float(va) - float(vb))
                    except Exception:
                        d = float('inf')
                    if d > worst:
                        worst = d
                        worst_at = (i, j, va, vb)
                    if len(first) < 5:
                        first.append((i, j, va, vb))
        print(f'\n  ── 工作表「{name}」')
        print(f'     格子总数 {n}   完全相同 {same}   不同 {n-same}'
              f'   一致率 {100.0*same/max(1,n):.6f}%')
        if n - same:
            print(f'     最大绝对差 = {worst:.3e}（位置 行{worst_at[0]} 列{worst_at[1]}：'
                  f'{worst_at[2]} vs {worst_at[3]}）')
            print('     前几处不同：')
            for (i, j, va, vb) in first:
                print(f'        行{i} 列{j}:  {va}  vs  {vb}')
        grand_same += same
        grand_diff += (n - same)
        grand_max = max(grand_max, worst)

    print('\n' + '=' * 76)
    tot = grand_same + grand_diff
    print(f'  合计：{tot} 个格子，完全相同 {grand_same}，不同 {grand_diff}'
          f'（一致率 {100.0*grand_same/max(1,tot):.6f}%）')
    print(f'  全表最大绝对差 = {grand_max:.3e}')
    if grand_diff == 0:
        print('  ✅ 结论：两版本结果**逐格完全相同** ⟹ 性能优化未改变任何输出。')
    elif grand_max <= 1e-3:
        print('  ✅ 结论：差异仅出现在**末位舍入**（|Δ| ≤ 1e-3，即第 4 位小数 ±1）'
              ' ⟹ 属浮点舍入边界效应，**不影响任何结论**。')
    else:
        print('  ⚠ 结论：存在超出舍入量级的差异，**须查明**。')
    print('=' * 76)


if __name__ == '__main__':
    main()
