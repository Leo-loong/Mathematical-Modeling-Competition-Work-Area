# -*- coding: utf-8 -*-
"""A 题 Q2 · 创新 INV-Q2-2：内层 Picard **容限的成本—精度曲线**与容限裁决

动机（kb 依据）
---------------
`kb/source/联网搜索/Picard与Newton迭代收敛性对比_变饱和渗流_Hydrology2017.md`：
  · "**容限并非越小越好**" —— 从 1e-2 收紧到 1e-3 后，继续收紧**只显著增加 CPU、
    精度几无改善**；作者**推荐最小 1e-3**。
  · 但本题 ρ、c_p、k 均随 C 变、D 含 exp(-3850/T) ⟹ 非线性可能**更陡**，未必适用该结论。

本实验用数据裁决：**我们取 tol=1e-9 是否在做无效功？**

做法（单变量隔离：**只变 tol**，其余口径逐字锁死）
--------------------------------------------------
  · 口径：N=80（Δr=0.25 mm）、dt_out=1 s、n_sub=16（内部 1/16 s）、mode='coupled'、
    恒定边界 T∞=50.00 ℃／C∞=0.04999、时程 1 h（与 E5 同口径，便于横向对照）
  · 变的是：内层 Picard 容限 tol ∈ {1e-3, 1e-5, 1e-7, 1e-9, 1e-11}（ω=0.7、maxit=30 固定）
  · 记录：Picard 总迭代数（若核回传）／墙钟／T(0)、T(R)、C(0)、C(R)
  · 判据阈值：**4 位小数最小位 = 5e-5**（℃ 与 kg/kg 均以此为准）

裁决规则（**两种结果都是有效结论**）
------------------------------------
  · 若存在某档与最严档（1e-11）**逐格差 ≤5e-5 且更快** ⟹ **可放宽容限**（动交付须另行授权）；
  · 若必须 1e-9 或更严 ⟹ 给出"**本题非线性更陡**"的定量证据（迭代数随容限收紧的下降更慢），
    并如实写明"我们比文献推荐更严，理由是…"。

运行：python q2_inv_tol_tradeoff.py
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
CODE = os.path.abspath(os.path.join(HERE, '..', 'code'))
sys.path.insert(0, CODE)

import numpy as np                                          # noqa: E402
from concurrent.futures import ProcessPoolExecutor          # noqa: E402

T_EXT, C_EXT = 50.00, 0.04999
NSTEP = 3600            # 1 h
N_SUB = 16              # 内部步长 1/16 s（与 E5 同口径）
TOLS = [1e-3, 1e-5, 1e-7, 1e-9, 1e-10, 1e-11]
DELIV_TOL = 1e-10       # ★现行交付口径：q2_solver.py **未显式传 tol** ⟹ 取核的默认值
THRESH = 5e-5           # 4 位小数最小位
LOG = os.path.join(HERE, 'logs', 'q2_inv_tol_tradeoff.log')
CSV = os.path.join(HERE, 'q2_inv_tol_tradeoff.csv')
BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(str(s))


def _worker(job):
    """子进程内独立求解（tol 作为**函数参数**传入，无全局状态）"""
    tol = job
    from q2_core import run_q2
    t0 = time.time()
    res, _t, _c = run_q2(N=80, dr=2.5e-4, dt_out=1.0, nsteps=NSTEP,
                        Tenv_fn=lambda _t: T_EXT, Cenv_fn=lambda _t: C_EXT,
                        n_sub=N_SUB, mode='coupled', tol=tol, omega=0.7, maxit=30)
    wall = time.time() - t0
    T, C = res['T_end'], res['C_end']
    out = np.array([T[0], T[-1], C[0], C[-1]])
    st = res.get('stats') or {}
    return tol, out, wall, dict(st)


def main():
    t00 = time.time()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    say('=' * 78)
    say('Q2 创新 INV-Q2-2：内层 Picard 容限的"成本—精度"曲线（1 h，恒定边界）')
    say('口径：N=80 / Δr=0.25 mm / dt_out=1 s / n_sub=16 / mode=coupled / ω=0.7 / maxit=30')
    say('单变量隔离：**只变 tol**')
    say('=' * 78)

    ncpu = os.cpu_count() or 4
    with ProcessPoolExecutor(max_workers=min(len(TOLS), max(1, ncpu - 1))) as ex:
        rows = list(ex.map(_worker, TOLS))

    ref = next(r for r in rows if r[0] == min(TOLS))
    oref = ref[1]
    say('')
    say('【逐档结果】参考档 = tol %.0e' % min(TOLS))
    say('%-10s %9s %11s %11s %11s %11s %10s' %
        ('tol', '墙钟/s', 'T(0)', 'T(R)', 'C(0)', 'C(R)', 'Picard总迭代'))
    for tol, out, wall, st in rows:
        it = st.get('total_it', st.get('tot_it', st.get('n_iter', '—')))
        say('%-10.0e %9.1f %11.4f %11.4f %11.6f %11.6f %10s'
            % (tol, wall, out[0], out[1], out[2], out[3], it))

    say('')
    say('【与参考档的逐格差】阈值 = %.0e（4 位小数最小位）' % THRESH)
    say('%-10s %11s %11s %11s %11s %8s' %
        ('tol', 'ΔT(0)', 'ΔT(R)', 'ΔC(0)', 'ΔC(R)', '判定'))
    verdict = []
    for tol, out, wall, st in rows:
        d = np.abs(out - oref)
        ok = bool(np.all(d <= THRESH))
        verdict.append((tol, d, ok, wall))
        say('%-10.0e %11.2e %11.2e %11.2e %11.2e %8s'
            % (tol, d[0], d[1], d[2], d[3], '一致' if ok else '有差'))

    # 裁决：最松的、与参考档一致的容限
    ok_tols = [t for t, _d, ok, _w in verdict if ok]
    say('')
    say('【裁决】')
    wmap = {tol: w for tol, _out, w, _st in rows}
    if ok_tols:
        loosest = max(ok_tols)
        w_ref = wmap[min(TOLS)]
        w_del = wmap.get(DELIV_TOL)
        w_loose = wmap[loosest]
        say('  · 与最严档（%.0e）**逐格一致（≤%.0e）的最松容限 = %.0e**' % (min(TOLS), THRESH, loosest))
        say('  · 现行交付容限 = %.0e（`q2_solver.py` 未显式传 tol ⟹ 核默认值）' % DELIV_TOL)
        if w_del:
            say('  · 墙钟：现行 %.1f s ／ 最松一致档 %.1f s ⟹ 放宽可省 **%.2f×**'
                % (w_del, w_loose, w_del / max(w_loose, 1e-9)))
        # kb 推荐值的实测代价（本题是否适用）
        kb_tol = 1e-3
        if kb_tol in ok_tols:
            say('  · ⟹ kb 推荐的 %.0e **在本题成立**（与最严档一致）' % kb_tol)
        else:
            dd = next(d for t, d, _o, _w in verdict if t == kb_tol)
            say('  · ⟹ **kb 推荐的 %.0e 在本题不成立**：其逐格最大偏差达 **%.2e**（≈ %.0f 个最小位）'
                % (kb_tol, float(np.max(dd)), float(np.max(dd)) / THRESH))
            say('    ⟹ 本题非线性**显著陡于**该文献领域，**必须比文献严得多**。')
        say('')
        if loosest > DELIV_TOL:
            say('  ★ **可放宽**：容限由 %.0e 放至 **%.0e**，与最严档逐格一致（省 %.2f×）。'
                % (DELIV_TOL, loosest, (w_del / max(w_loose, 1e-9)) if w_del else float('nan')))
            up = [t for t in TOLS if t > loosest]
            if up:
                dt_up = next(d for t, d, _o, _w in verdict if t == min(up))
                say('     ⚠ 再松一档（%.0e）即出现 **%.2e** 级偏差 ⟹ %.0e 为**放宽上限**。'
                    % (min(up), float(np.max(dt_up)), loosest))
            say('     ⚠ 替换交付口径**须另行授权 ＋ 四闸门**（本实验仅覆盖 1 h 时程）。')
        elif loosest == DELIV_TOL:
            say('  ★ **现行容限恰为最优点**：已与最严档逐格一致，再松即出现偏差 ⟹ 既非欠收敛、也无无效功。')
        else:
            say('  ★ **现行容限偏严**：可放宽至 %.0e 而零精度损失（省 %.2f×）。'
                % (loosest, (w_del / max(w_loose, 1e-9)) if w_del else float('nan')))
    else:
        say('  · **没有任何档与最严档逐格一致** ⟹ 容限必须保持最严档，不得放宽。')

    say('')
    say('总耗时 %.0f s' % (time.time() - t00))
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    with open(CSV, 'w', encoding='utf-8') as f:
        f.write('tol,wall_s,T0,TR,C0,CR,dT0,dTR,dC0,dCR\n')
        for (tol, out, wall, _st), (_t, d, _ok, _w) in zip(rows, verdict):
            f.write('%.0e,%.1f,%.4f,%.4f,%.6f,%.6f,%.2e,%.2e,%.2e,%.2e\n'
                    % (tol, wall, out[0], out[1], out[2], out[3], d[0], d[1], d[2], d[3]))
    print('LOG:', LOG)
    print('CSV:', CSV)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
