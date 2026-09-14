# -*- coding: utf-8 -*-
"""
Q2 · 双核数值一致性核对工具
======================================================
用途：比较任意两个求解核在同一算例下的结果差异。
  用法：python q2_verify_BC.py <模块A> <模块B> [nsteps]
  例：  python q2_verify_BC.py q2_core_orig q2_core      1800
        python q2_verify_BC.py q2_core_orig q2_core_c    1800

判定门槛（与《A_数值口径总表》O6 的 4 位小数输出一致）：
  逐点最大偏差 |ΔT| < 1e-4 ℃、|ΔC| < 1e-4 kg/kg  ⟹ 4 位小数输出**完全不受影响**；
  相对偏差 < 5e-5 ⟹ 满足 L3-07 的收敛判定口径。
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
import importlib                                                 # noqa: E402
import numpy as np                                               # noqa: E402

TINF, CINF = 50.00, 0.04999


def run(mod_name, nsteps, N=80, dr=2.5e-4, n_sub=32):
    m = importlib.import_module(mod_name)
    importlib.reload(m)
    t0 = time.perf_counter()
    res, _, _ = m.run_q2(N=N, dr=dr, dt_out=1.0, nsteps=nsteps, n_sub=n_sub,
                         Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: CINF,
                         mode='coupled')
    return res, time.perf_counter() - t0, m


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    ma, mb = sys.argv[1], sys.argv[2]
    nsteps = int(sys.argv[3]) if len(sys.argv) > 3 else 1800

    print('=' * 74)
    print(f'双核一致性核对：{ma}  vs  {mb}     时程 {nsteps} s')
    print('=' * 74)
    ra, wa, moda = run(ma, nsteps)
    rb, wb, modb = run(mb, nsteps)
    print(f'  {ma:16s} 耗时 {wa:7.2f}s   numba={getattr(moda, "_HAS_NUMBA", None)}')
    print(f'  {mb:16s} 耗时 {wb:7.2f}s   numba={getattr(modb, "_HAS_NUMBA", None)}')
    print(f'  ⟹ 加速比 {wa/wb:.2f}×')

    Ta, Ca = ra['T_end'], ra['C_end']
    Tb, Cb = rb['T_end'], rb['C_end']
    dT = float(np.max(np.abs(Ta - Tb)))
    dC = float(np.max(np.abs(Ca - Cb)))
    rT = dT / max(1e-30, float(np.max(np.abs(Ta))))
    rC = dC / max(1e-30, float(np.max(np.abs(Ca))))

    print(f'\n  末端场差异：')
    print(f'    max|ΔT| = {dT:.3e} ℃      相对 {rT:.3e}')
    print(f'    max|ΔC| = {dC:.3e} kg/kg  相对 {rC:.3e}')
    print(f'    T(0): {Ta[0]:.10f} vs {Tb[0]:.10f}   Δ={Ta[0]-Tb[0]:+.3e}')
    print(f'    T(R): {Ta[-1]:.10f} vs {Tb[-1]:.10f}   Δ={Ta[-1]-Tb[-1]:+.3e}')
    print(f'    C(0): {Ca[0]:.10f} vs {Cb[0]:.10f}   Δ={Ca[0]-Cb[0]:+.3e}')
    print(f'    C(R): {Ca[-1]:.10f} vs {Cb[-1]:.10f}   Δ={Ca[-1]-Cb[-1]:+.3e}')

    print()
    ok4 = (dT < 1e-4) and (dC < 1e-4)
    ok5 = (rT < 5e-5) and (rC < 5e-5)
    print(f'  {"PASS" if ok4 else "**FAIL**"}  逐点偏差 < 1e-4 ⟹ 4 位小数输出不受影响')
    print(f'  {"PASS" if ok5 else "**FAIL**"}  相对偏差 < 5e-5 ⟹ 满足 L3-07 口径')
    print('=' * 74)


if __name__ == '__main__':
    main()
