# -*- coding: utf-8 -*-
"""
A 题 Q2 · W2 预试验：空间/时间收敛（定步长）
======================================================
目的：在正式求解前定出三个参数——
      · 空间步长 Δr（沿用 Q1 的 0.25 mm，需复核）
      · 温度内部子步 Δt_T（候选 1 → 1/32 s）
      · 含水率内部子步 Δt_C（候选 1 → 0.1 s）
判定标准（L3-07）：关键量相对变化 < 5e-5（保证第 4 位小数有效）。

设置（刻意隔离变量）：
  · 时程      ：1800 s（0.5 h；足够显出收敛趋势，避免预试验过慢）
  · 边界条件  ：恒定（T∞=50.00 ℃、C∞=0.04999 kg/kg）
                —— 恒定边界可**排除外推/插值差异对收敛性判断的干扰**
  · 模式      ：'coupled'（主力双向强耦合）

用法：
  python q2_w2_prestudy.py smoke     # 冒烟：1 组，验证代码可跑
  python q2_w2_prestudy.py space     # 空间收敛（Δr）
  python q2_w2_prestudy.py timeT     # 温度时间收敛（Δt_T）
  python q2_w2_prestudy.py timeC     # 含水率时间收敛（Δt_C）
  python q2_w2_prestudy.py all       # 全部（较慢）
"""
import sys
import os
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q2_core import run_q2, DEF2          # noqa: E402

T_END = float(os.environ.get('Q2_TEND', '1800'))       # 预试验时程（s）
DT_T_REF = float(os.environ.get('Q2_DTT', '0.03125'))  # space/timeC 组固定的温度子步（s）
TINF, CINF = 50.00, 0.04999               # 恒定边界（H6 的恒温段外推值）


def Tenv(_t):
    return TINF


def Cenv(_t):
    return CINF


def run_case(N, dr, dtT, dtC, tag):
    """跑一组并返回关键量与统计。"""
    nsteps = int(T_END)
    subT = max(1, int(round(1.0 / dtT)))
    subC = max(1, int(round(1.0 / dtC)))
    t0 = time.time()
    res, _, _ = run_q2(N=N, dr=dr, dt_out=1.0, nsteps=nsteps,
                       Tenv_fn=Tenv, Cenv_fn=Cenv, subT=subT, subC=subC,
                       mode='coupled')
    T, C = res['T_end'], res['C_end']
    st = res['stats']
    out = dict(tag=tag, N=N, dr=dr, dtT=dtT, dtC=dtC,
               Tc=float(T[0]), Ts=float(T[-1]),
               Cc=float(C[0]), Cs=float(C[-1]), Cmax=float(np.max(C)),
               outer_avg=st['outer_tot'] / max(1, st['nsub']),
               outer_max=st['outer_max'], inner_avg=st['inner_tot'] / max(1, st['nsub']),
               resT=st['resT_max'], resC=st['resC_max'],
               flags=st['flags'], wall=time.time() - t0)
    print(f"  [{tag:22s}] dr={dr*1e3:>5.2f}mm dtT={dtT:<7.4f}s dtC={dtC:<5.2f}s "
          f"| T0={out['Tc']:.6f} TR={out['Ts']:.6f} C0={out['Cc']:.8f} "
          f"CR={out['Cs']:.8f} | outer×{out['outer_avg']:.2f} "
          f"inner×{out['inner_avg']:.1f} | {out['wall']:.1f}s", flush=True)
    if out['flags']:
        print(f"      ⚠ 未收敛标记：{out['flags']}", flush=True)
    return out


def rel_change(vals, key):
    """相对变化（相对最细基准）"""
    v = np.array([x[key] for x in vals], dtype=float)
    ref = v[-1]
    return np.abs(v - ref) / max(1e-30, abs(ref))


def report(title, rows, key):
    print("\n" + "=" * 78)
    print(f"【{title}】")
    rel = rel_change(rows, key)
    for r, e in zip(rows, rel):
        print(f"   {r['tag']:22s}  {key}={r[key]:.8f}   相对变化={e:.3e}"
              f"   {'✅' if e < 5e-5 else '⚠'}")
    print("   判定阈值：相对变化 < 5e-5（L3-07）")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else 'smoke'
    print(f"Q2 W2 预试验：{what} | 时程 {T_END:.0f} s | 恒定边界 "
          f"({TINF} ℃, {CINF} kg/kg) | 模式 coupled")

    if what == 'smoke':
        run_case(80, 2.5e-4, 0.5, 1.0, 'smoke')
        return

    if what in ('space', 'all'):
        print(f"\n▶ 空间收敛（固定 dtT={DT_T_REF:g} s, dtC=0.1 s）")
        rows = []
        for dr, N in ((1.0e-3, 20), (5.0e-4, 40), (2.5e-4, 80)):
            rows.append(run_case(N, dr, DT_T_REF, 0.1, f'dr={dr*1e3:.2f}mm'))
        report('空间收敛', rows, 'Ts')

    if what in ('timeT', 'all'):
        print("\n▶ 温度时间收敛（固定 dr=0.25 mm, dtC=0.1 s）")
        rows = []
        for dtT in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
            rows.append(run_case(80, 2.5e-4, dtT, 0.1, f'dtT={dtT:.4f}s'))
        report('温度时间收敛', rows, 'Ts')

    if what in ('timeC', 'all'):
        print(f"\n▶ 含水率时间收敛（固定 dr=0.25 mm, dtT={DT_T_REF:g} s）")
        rows = []
        for dtC in (1.0, 0.5, 0.25, 0.1):
            rows.append(run_case(80, 2.5e-4, DT_T_REF, dtC, f'dtC={dtC:.2f}s'))
        report('含水率时间收敛', rows, 'Cs')


if __name__ == '__main__':
    main()
