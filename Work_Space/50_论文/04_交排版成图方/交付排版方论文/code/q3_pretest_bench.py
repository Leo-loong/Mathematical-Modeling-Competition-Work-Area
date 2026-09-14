# -*- coding: utf-8 -*-
"""
A 题 Q3 · W0 预测试：组件级微基准（SMOKE）
=================================================================
级别：T1（依《工作约束》§12.1）
  · 本脚本**不运行任何求解**（不调用 run_q2 / step_imex 的完整时程推进）
  · 仅测量 **单个组件函数的调用耗时**，用于按结构外推 Q3 总耗时
  · **不产出任何交付物**，不写结果文件
  · 控制台输出全部加 [SMOKE] 前缀

目的：
  1. 测出"一次 Picard 迭代"与"一个内部子步"的耗时；
  2. 按 Q3 的预期内部步数（约 3.0e6）外推总耗时；
  3. **用 Q2 的实测数据（10800 s / 46.9 s）反验外推法**是否可靠——
     这是本预测试的核心价值：先证明"外推可信"，再用于外推 Q3。

禁止：本脚本不得被改装成求解脚本；不得写入 result3.xlsx。

用法：python q3_pretest_bench.py
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Q3 复用 Q2 的优化核（依用户指令：只用优化后版本，禁止 _orig）
_Q2CODE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Q2', 'code')
sys.path.insert(0, _Q2CODE)
_CORE = os.environ.get('Q2_CORE', 'c')
if _CORE == 'c':
    import q2_core_c as core          # B+C 优化核（默认）
else:
    import q2_core as core            # B 优化核

N, DR = 80, 2.5e-4
H = 1.0 / 32.0
R0, HC, KM = core.DEF2['R0'], core.DEF2['h'], core.DEF2['km']
NC = N + 1

print('[SMOKE] ============================================================')
print('[SMOKE] Q3 W0 预测试 · 组件级微基准')
print('[SMOKE] 核 = %s (Q2_CORE=%s) | N=%d | h=1/32 s | numba=%s'
      % (core.__name__, _CORE, N, getattr(core, 'NUMBA_OK', 'n/a')))
print('[SMOKE] ============================================================')


def bench(fn, n=2000, warm=200):
    """返回单次调用的平均耗时（微秒）。先热身以排除 JIT 编译开销。"""
    for _ in range(warm):
        fn()
    t0 = time.perf_counter()
    for _ in range(n):
        fn()
    return (time.perf_counter() - t0) / n * 1e6


# ---- 构造典型状态（仅用于计时，不构成任何求解）----
T = np.linspace(28.0, 49.9, NC)
C = np.linspace(2.55, 1.0, NC)
Tinf, Cinf = 50.0, 0.04999

bufT = (np.zeros(NC), np.zeros(NC), np.zeros(NC))
bufC = (np.zeros(NC), np.zeros(NC), np.zeros(NC))
dTbuf = np.zeros(NC)
dCbuf = np.zeros(NC)

# ---- 各组件微基准 ----
t_rho = bench(lambda: core.rho_of(C))
t_cp = bench(lambda: core.cp_of(C))
t_k = bench(lambda: core.k_of(C))
t_D = bench(lambda: core.D_of(C, T))


def _iface():
    return core.iface(core.D_of(C, T))


t_if = bench(_iface)


def _asmC():
    a, b, c = core.assemble_C_var(N, DR, H, core.iface(core.D_of(C, T)), R0, KM, out=bufC)
    return a


t_asmC = bench(_asmC)


def _rhsC():
    return core.rhs_C_var(N, DR, H, R0, KM, C, Cinf, out=dCbuf)


t_rhsC = bench(_rhsC)


def _thom():
    a, b, c = bufC
    return core.thomas(a, b, c, dCbuf)


t_thom = bench(_thom)

print('[SMOKE] --- 单次调用耗时（微秒）---')
print('[SMOKE]   rho_of            %8.2f' % t_rho)
print('[SMOKE]   cp_of             %8.2f' % t_cp)
print('[SMOKE]   k_of              %8.2f' % t_k)
print('[SMOKE]   D_of              %8.2f' % t_D)
print('[SMOKE]   iface(D)          %8.2f' % t_if)
print('[SMOKE]   assemble_C_var    %8.2f' % t_asmC)
print('[SMOKE]   rhs_C_var         %8.2f' % t_rhsC)
print('[SMOKE]   thomas            %8.2f' % t_thom)

# ---- 组装"一次含水率 Picard 迭代"的等效耗时 ----
t_iter_C = t_D + t_if + t_asmC + t_rhsC + t_thom
print('[SMOKE]')
print('[SMOKE] --- 派生量 ---')
print('[SMOKE]   一次含 C 的 Picard 迭代（等效）= %.2f us' % t_iter_C)

# ---- 用 Q2 的已知结构反验外推法 ----
#   Q2 实测：10800 输出步 × 32 子步 = 345600 内部步；实测墙钟 46.9 s（B+C 核）
Q2_INNER = 10800 * 32
Q2_WALL_MEAS = 46.9
mu_per_inner_q2 = Q2_WALL_MEAS * 1e6 / Q2_INNER
print('[SMOKE]')
print('[SMOKE] --- 反验：以 Q2 实测校准"单内部步耗时" ---')
print('[SMOKE]   Q2 内部步数 = %d' % Q2_INNER)
print('[SMOKE]   Q2 实测墙钟 = %.1f s' % Q2_WALL_MEAS)
print('[SMOKE]   => 折算单内部步 = %.2f us' % mu_per_inner_q2)
print('[SMOKE]   说明：该值含 T 方程＋C 迭代＋环境函数调用＋循环开销，')
print('[SMOKE]         故应显著大于上面"单次 Picard 迭代"的 %.2f us。' % t_iter_C)
print('[SMOKE]   ⚠ 诚实声明：该折算值由 Q2 实测"反推"，再用于外推 Q3，')
print('[SMOKE]       属"同一数据的正反使用"，**不是独立验证**；')
print('[SMOKE]       其成立前提 = "Q3 每内部步成本与 Q2 相同"（同网格、同格式 ⟹ 合理）。')
_share = t_iter_C / mu_per_inner_q2 * 100.0
print('[SMOKE]   ★ 结构占比：一次 C-Picard 迭代仅占单内部步的 %.1f%%' % _share)
print('[SMOKE]      ⟹ 其余 %.1f%% 为 T 方程＋环境函数调用＋循环开销'
      % (100.0 - _share))
print('[SMOKE]      ⟹ **优化重点应在后者，而非 C 迭代本身**。')

# ---- 外推 Q3（注意单位：mu_per_inner_q2 为微秒）----
print('[SMOKE]')
print('[SMOKE] --- 外推 Q3 总耗时（按 t_end 情景）---')
print('[SMOKE]   %-10s %-12s %-14s %-16s' % ('t_end', '内部步数', '基线外推(s)', 'A+B优化1.5x(s)'))
for h_end in (20, 26, 32, 45):
    inner = int(h_end * 3600 / H)
    wall = inner * mu_per_inner_q2 / 1e6          # 微秒 -> 秒
    print('[SMOKE]   %-10s %-12d %-14.1f %-16.1f'
          % ('%d h' % h_end, inner, wall, wall / 1.5))

print('[SMOKE]')
print('[SMOKE] --- 全流程总量估算（约 20-25 次运行）---')
inner26 = int(26 * 3600 / H)
base26 = inner26 * mu_per_inner_q2 / 1e6
print('[SMOKE]   单次主力（26 h，未优化 A/B）= %.1f s = %.1f min' % (base26, base26 / 60))
print('[SMOKE]   若 A+B 优化 1.5x           = %.1f s' % (base26 / 1.5))
print('[SMOKE]   若 A+B+C(自适应 4.8x)      = %.1f s' % (base26 / 1.5 / 4.8))
print('[SMOKE]   全流程 22 次的累计墙钟（三种情形）: %.0f min / %.0f min / %.0f min'
      % (base26 * 22 * 0.35 / 60, base26 / 1.5 * 22 * 0.35 / 60,
         base26 / 1.5 / 4.8 * 22 * 0.35 / 60))
print('[SMOKE]   （×0.35：只有主力与收敛重验按全程跑，灵敏度/对照多为短时程）')
print('[SMOKE]')
print('[SMOKE] 本脚本未运行任何求解、未写出任何文件。')
