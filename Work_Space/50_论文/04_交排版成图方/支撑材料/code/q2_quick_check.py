# -*- coding: utf-8 -*-
"""
A 题 Q2 · 快速正确性自检（秒级）
======================================================
目的：在跑任何长时程之前，先用**极短时程**把"数值解 vs 级数解"比一遍，
      确认离散与实现无误（若此处不过，长跑毫无意义）。

做法：frozen 模式（物性=常数）＋ 恒定边界 ⟹ 与圆柱级数解逐点对拍。
时程：1 / 10 / 100 / 600 s（秒级完成）
"""
import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q2_core import run_q2, rho_of, cp_of, k_of, D_of, DEF2   # noqa: E402
from q2_e2_frozen import char_roots, series_theta, TINF        # noqa: E402

R0, H = DEF2['R0'], DEF2['h']
T0, C0 = DEF2['T0'], DEF2['C0']


def main():
    rho = float(rho_of(C0)); cp = float(cp_of(C0)); kk = float(k_of(C0))
    alpha = kk / (rho * cp)
    Bi = H * R0 / kk
    mus = char_roots(Bi)
    print(f"E2 前置：alpha={alpha:.6e}  Bi={Bi:.6f}  根数={len(mus)}  "
          f"[自检] θ(Fo→0)={series_theta(0.0, 1e-12, Bi, mus):.8f}")

    print(f"\n{'t(s)':>7} {'T0_num':>12} {'T0_ana':>12} {'ΔT0':>10} "
          f"{'TR_num':>12} {'TR_ana':>12} {'ΔTR':>10} {'wall(s)':>8}")
    for t_end in (1, 10, 100, 600):
        t0 = time.time()
        res, _, _ = run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=int(t_end),
                           Tenv_fn=lambda _t: TINF, Cenv_fn=lambda _t: 0.04999,
                           subT=32, subC=10, mode='frozen')
        w = time.time() - t0
        Fo = alpha * t_end / R0 ** 2
        a0 = TINF + (T0 - TINF) * series_theta(0.0, Fo, Bi, mus)
        aR = TINF + (T0 - TINF) * series_theta(1.0, Fo, Bi, mus)
        n0, nR = float(res['T_end'][0]), float(res['T_end'][-1])
        print(f"{t_end:7.0f} {n0:12.6f} {a0:12.6f} {n0-a0:+10.2e} "
              f"{nR:12.6f} {aR:12.6f} {nR-aR:+10.2e} {w:8.2f}")

    print("\n判定：偏差应由**时间离散**主导（不随空间网格减小），"
          "量级 ~1e-3 ℃ 属预期；若出现 1e-1 或更大，说明实现有误。")


if __name__ == '__main__':
    main()
