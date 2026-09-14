# -*- coding: utf-8 -*-
"""
Q3 · E5 灵敏度分析（**以"烘干结束时间 t_end"为输出**）
================================================================================
说明：Q2 的 E5 是在 1 h 时程上做 OAT（输出为 C(R)）；
     Q3 的**目标量就是 t_end**，故灵敏度必须以 t_end 为输出
     ——这是 Q3 与 Q2 在检验设计上的关键差异（依《A_Q3求解思路与工作流》§2.2）。

参数与档位（±20%）：
  · T_inf  恒温段环境温度      ±1.0 ℃（对应约 ±2%）
  · C_inf  恒温段环境浓度      ±20%
  · h      表面对流换热系数    ±20%
  · k_m    表面对流传质系数    ±20%
  · D0     扩散系数前置因子    ±20%（等价于整体缩放 D）

实现：**多进程并行**（每个算例独立，环境查表在子进程内重建）。
      每个算例的事件驱动终止与主力完全一致（判据 C<0.15，熔断 150 h）。

⚠ 敏感性指标用"相对灵敏度"S = (Δt_end/t_end) / (Δp/p)。

用法：python q3_e5_sensitivity.py
产出：q3_e5_S.csv（供口径表取用）+ q3_e5_log.txt
"""
import sys
import os
import time
from concurrent.futures import ProcessPoolExecutor

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'q3_e5_log.txt')
BUF = []


def say(s=''):
    print(s)
    BUF.append(s)


def _worker(job):
    """子进程入口：跑一个扰动算例，返回 t_end（h）。"""
    import os as _os
    import sys as _sys
    for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        _os.environ.setdefault(_v, '1')
    import numpy as _np
    import openpyxl as _xl
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _sys.path.insert(0, _here)
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_here), 'Q2', 'code'))
    import q2_core_c as _base
    import q3_core as _q3

    name, d_h, d_km, d_D0, d_Tinf, d_Cinf, max_h = job
    P = _base.DEF2
    _ws_root = _os.path.abspath(_os.path.join(_here, '..', '..', '..'))
    _wb = _xl.load_workbook(_os.path.join(_ws_root, '10_赛题', 'A题', '附件',
                                          '附件1.xlsx'), data_only=True)
    _sh = _wb.active
    _rows = [r for r in _sh.iter_rows(values_only=True)][1:]
    _d = [r for r in _rows if r[0] is not None]
    _t = _np.array([float(r[0]) for r in _d])
    _T = _np.array([float(r[1]) for r in _d])
    _C = _np.array([float(r[2]) for r in _d])
    _wb.close()
    ts, Tv, Cv = _q3.env_tables_from_att1(_t, _T, _C,
                                          T_tail=50.00 + d_Tinf,
                                          C_tail=0.04999 * (1.0 + d_Cinf))

    N, DR = 80, 2.5e-4
    NC = N + 1
    DT_OUT = 60.0
    H_IN = 1.0 / 32.0
    NSUB = int(round(DT_OUT / H_IN))
    HH = DT_OUT / NSUB
    R0 = P['R0']
    hc = P['h'] * (1.0 + d_h)
    km = P['km'] * (1.0 + d_km)
    d_fac = 1.0 + d_D0

    T = _np.full(NC, P['T0'])
    C = _np.full(NC, P['C0'])
    nsteps_max = int(round(max_h * 3600.0 / DT_OUT))
    orig_fac = _q3.D_FAC                      # 保存原值
    _q3.D_FAC = d_fac                         # 供 step_imex_fast 内部取用
    try:
        for n in range(1, nsteps_max + 1):
            T, C, _ = _q3.step_imex_fast(N, DR, HH, NSUB, R0, hc, km,
                                         T, C, ts, Tv, Cv, (n - 1) * DT_OUT)
            if float(_np.max(C)) < 0.15:
                return (name, n * DT_OUT / 3600.0)
    finally:
        _q3.D_FAC = orig_fac
    return (name, float('nan'))


def main():
    say('=' * 76)
    say('Q3 · E5 灵敏度分析（输出 = 烘干结束时间 t_end）')
    say('=' * 76)
    say('  判据 C<0.15；熔断 150 h；每算例与主力同口径（Δr=0.25mm, 1/32 s）')
    say()
    jobs = []
    for nm, dh, dk, dD, dT, dC in [
            ('T_inf -1.0C', 0, 0, 0, -1.0, 0), ('T_inf +1.0C', 0, 0, 0, +1.0, 0),
            ('C_inf -20%', 0, 0, 0, 0, -0.20), ('C_inf +20%', 0, 0, 0, 0, +0.20),
            ('h -20%', -0.20, 0, 0, 0, 0), ('h +20%', +0.20, 0, 0, 0, 0),
            ('k_m -20%', 0, -0.20, 0, 0, 0), ('k_m +20%', 0, +0.20, 0, 0, 0),
            ('D0 -20%', 0, 0, -0.20, 0, 0), ('D0 +20%', 0, 0, +0.20, 0, 0)]:
        jobs.append((nm, dh, dk, dD, dT, dC, 150.0))

    t0 = time.time()
    nw = min(8, os.cpu_count() or 4)
    say('  并行度 = %d' % nw)
    res = {}
    with ProcessPoolExecutor(max_workers=nw) as ex:
        for nm, te in ex.map(_worker, jobs):
            res[nm] = te
            say('    %-14s t_end = %s' % (nm, '%.4f h' % te if te == te else '未达标'))
    say()
    say('  全部完成，墙钟 %.1f s' % (time.time() - t0))

    base_t = res.get('T_inf +1.0C', float('nan'))
    # 基准用无扰动值：单独跑一次（用 D0 +0% 等价于基准）
    base_t = _worker(('BASE', 0, 0, 0, 0, 0, 150.0))[1]
    say('  基准 t_end（无扰动）= %.4f h' % base_t)
    say()
    say('  %-14s %-12s %-12s %-14s' % ('算例', 't_end/h', 'Δt_end/h', 'S=(ΔT/T)/(Δp/p)'))
    say('  ' + '-' * 58)
    rows = []
    for nm, dp in [('T_inf -1.0C', -1.0 / 50.0), ('T_inf +1.0C', +1.0 / 50.0),
                   ('C_inf -20%', -0.20), ('C_inf +20%', +0.20),
                   ('h -20%', -0.20), ('h +20%', +0.20),
                   ('k_m -20%', -0.20), ('k_m +20%', +0.20),
                   ('D0 -20%', -0.20), ('D0 +20%', +0.20)]:
        te = res.get(nm, float('nan'))
        d = te - base_t
        S = (d / base_t) / dp if dp != 0 else float('nan')
        say('  %-14s %-12.4f %-12.4f %-14.3f' % (nm, te, d, S))
        rows.append((nm, dp, te, d, S))
    say()
    say('  说明：S 的**符号**表示方向；|S| 越大越敏感。')
    say('        T_inf 的 dp 按 ±1.0/50.0 计（相对 50 ℃ 的 ±2%）。')

    with open(os.path.join(HERE, 'q3_e5_S.csv'), 'w', encoding='utf-8') as f:
        f.write('case,dp_rel,t_end_h,dt_end_h,S\n')
        for nm, dp, te, d, S in rows:
            f.write('%s,%.6f,%.6f,%.6f,%.6f\n' % (nm, dp, te, d, S))
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    say('  已写出 q3_e5_S.csv 与 q3_e5_log.txt')


if __name__ == '__main__':
    main()
