# -*- coding: utf-8 -*-
"""
A 题 Q2 · 检验 E3-b：强制解耦退化 ＋ 耦合强度量化（O2 ＋ O8）
======================================================
【O2 强制解耦退化检验】——关闭"`decoupled` 分支从未被验证"的缺口

  `decoupled` 模式的含义：把物性改为**单向依赖**——
    · 温度侧：ρ(C)、c_p(C)、k(C) 仍随含水率变（但**不**随温度变）；
    · 水分侧：D 只依赖 C，**去掉温度因子** e^{-3850/T}。
  此时 C 不依赖 T、T 依赖 C ⟹ 物理上是**单向耦合**（可"先解 C、再解 T"）。

  **判据（强判据，可证伪）**：单向耦合下，改动**温度侧参数**（h）
  **不应改变含水率解**——若改变，说明实现里混入了不该有的温度依赖 ⟹ 有 bug。

【O8 耦合强度量化】——把"双向强耦合"从定性说法变成**有数字的结论**

  比较三种模式在同一算例下的末端场：
    · `coupled`   双向强耦合（主力口径）
    · `decoupled` 单向（去掉 D 的温度依赖）
    · `frozen`    物性全程冻结为初始常数（完全无耦合）
  ⟹ 差值分别量化"温度依赖"与"物性演化"两项耦合的贡献。

运行：python q2_e3b_decoupled.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np                                              # noqa: E402
import q2_core as qc                                            # noqa: E402

LOG = os.path.join(HERE, 'q2_e3b_log.txt')
BUF = []
TINF, CINF = 50.00, 0.04999
T_END, NSUB = 1800, 32


def say(s=''):
    print(s, flush=True)
    BUF.append(s)


def flush_log():
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')


def run(mode, h=None):
    h0 = qc.DEF2['h']
    if h is not None:
        qc.DEF2['h'] = h
    try:
        res, _, _ = qc.run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=T_END,
                              Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                              n_sub=NSUB, mode=mode)
    finally:
        qc.DEF2['h'] = h0
    return res['T_end'].copy(), res['C_end'].copy()


def main():
    t0 = time.time()
    say('=' * 76)
    say('Q2 检验 E3-b：强制解耦退化 ＋ 耦合强度量化')
    say('=' * 76)

    # ---------- O2：单向耦合的核心判据 ----------
    say('\n【O2 判据】单向耦合下，改温度侧参数 h 应**不改变**含水率解')
    base_T, base_C = run('decoupled')
    say(f'  基线（decoupled）         T(0)={base_T[0]:.10f}  C(0)={base_C[0]:.10f}  '
        f'C(R)={base_C[-1]:.10f}')
    ok_all = True
    for frac in (-0.2, +0.2):
        hh = 25.0 * (1 + frac)
        Tp, Cp = run('decoupled', h=hh)
        dC = float(np.max(np.abs(Cp - base_C)))
        dT = float(np.max(np.abs(Tp - base_T)))
        same = (dC == 0.0)
        ok_all &= same
        say(f'  h {frac:+.0%}（={hh:.1f}）       T(0)={Tp[0]:.10f}  '
            f'C(0)={Cp[0]:.10f}  C(R)={Cp[-1]:.10f}')
        say(f'      ⟹ 含水率场 max|ΔC| = {dC:.3e}  {"✅ 逐位不变" if same else "⚠ **变了**"}'
            f'   温度场 max|ΔT| = {dT:.3e}（温度**应当**改变）')
    say(f'  ⟹ 判定：{"✅ 通过——实现中不存在隐性的温度→水分依赖" if ok_all else "⚠ 未通过"}')

    # ---------- O8：耦合强度量化 ----------
    say('\n【O8 耦合强度量化】三种模式的末端场差异（同一算例，1800 s）')
    Tc, Cc = run('coupled')
    Td, Cd = run('decoupled')
    Tf, Cf = run('frozen')

    def rel(a, b):
        return float(np.max(np.abs(a - b))) / max(1e-30, float(np.max(np.abs(b))))

    say(f'\n  {"量":<8}{"强耦合":>14}{"单向decoupled":>16}{"完全冻结frozen":>16}')
    for nm, i in (('T(0)', 0), ('T(R)', -1)):
        say(f'  {nm:<8}{Tc[i]:>14.6f}{Td[i]:>16.6f}{Tf[i]:>16.6f}')
    for nm, i in (('C(0)', 0), ('C(R)', -1)):
        say(f'  {nm:<8}{Cc[i]:>14.6f}{Cd[i]:>16.6f}{Cf[i]:>16.6f}')

    say(f'\n  相对差异（以强耦合为基准）：')
    say(f'    含水率 C(R)：单向 vs 强耦合 = {rel(Cd, Cc):.3e}   冻结 vs 强耦合 = {rel(Cf, Cc):.3e}')
    say(f'    温度   T(R)：单向 vs 强耦合 = {rel(Td, Tc):.3e}   冻结 vs 强耦合 = {rel(Tf, Tc):.3e}')

    say('\n  结论（供论文引用）：')
    say('    · 「温度→水分」通道（D 的 e^{-3850/T} 项）的贡献 = 单向与强耦合的差异；')
    say('    · 「物性演化」通道（ρ,c_p,k 随 C 变）的贡献 = 冻结与强耦合的差异；')
    say('    · 两通道共同构成"双向耦合"，其量化值即为上表。')

    say(f'\n总耗时 {time.time()-t0:.1f}s')
    flush_log()


if __name__ == '__main__':
    main()
    try:
        if sys.stdin.isatty():
            input('\n按 Enter 键退出...')
    except Exception:
        pass
