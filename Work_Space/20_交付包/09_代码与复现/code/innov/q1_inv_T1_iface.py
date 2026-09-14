# -*- coding: utf-8 -*-
"""T1-3 界面系数口径对照：M6（沿 C 的积分平均） vs 沿 1/D 的调和型积分

M6（现行交付口径）：  D_face = ⟨D⟩ = (1/ΔC)∫_{Cl}^{Ch} D(C) dC
调和型（稳态通量精确）： 1/D_face = (1/ΔC)∫_{Cl}^{Ch} dC/D(C)

Q1 内 D(C) 仅变 21% ⟹ 预期差异很小；本项的意义是**口径完备性**与为 Q2–Q4（强变物性）留证。
**无论结果如何，均不改动 Q1 已收口的交付口径。**

运行：python q1_inv_T1_iface.py
"""
import numpy as np

from q1_inv_lib import Rec, env_fns
import q1_core as core

rec = Rec('q1_inv_T1_iface.log')
SNAP = (100, 300, 600, 900, 1200, 1500, 1800)
RHO = [0.0, 0.25, 0.5, 0.75, 1.0]


def faceD_quad(Carr, D0, bD, Dfac=1.0, nsamp=64, mode='avg'):
    """mode='avg'  : 沿 C 的积分平均（M6 现行口径）
       mode='harm' : 沿 1/D 的调和型积分（稳态通量精确取法）"""
    C = np.asarray(Carr, dtype=float)
    lo = np.minimum(C[:-1], C[1:])
    hi = np.maximum(C[:-1], C[1:])
    xs = lo[:, None] + (hi - lo)[:, None] * (np.arange(nsamp) + 0.5)[None, :] / nsamp
    xs = np.maximum(xs, 1e-9)
    if mode == 'avg':
        fv = np.exp(-bD / xs).mean(axis=1)
    else:
        fv = 1.0 / np.exp(bD / xs).mean(axis=1)
    flat = (hi - lo) < 1e-14
    if flat.any():
        fv[flat] = np.exp(-bD / np.maximum(lo[flat], 1e-9)) if mode == 'avg' else \
            np.exp(-bD / np.maximum(lo[flat], 1e-9))
    return D0 * Dfac * fv


def run(t, Tinf, Cinf, p, mode):
    orig = core.faceD_int
    core.faceD_int = lambda Carr, D0, bD, Dfac=1.0, nsamp=8, _m=mode: \
        faceD_quad(Carr, D0, bD, Dfac, max(nsamp, 64), _m)
    try:
        res, tabT, tabC = core.run_sim_collect(
            N=80, dr=0.25e-3, dt_out=1.0, nsteps=1800, p=p,
            Tenv_fn=lambda s: float(np.interp(s, t, Tinf)),
            Cenv_fn=lambda s: float(np.interp(s, t, Cinf)),
            sub=10, subT=1, cols=np.arange(0, 81, 4), snap_at=set(SNAP))
    finally:
        core.faceD_int = orig
    return res


def main():
    t, Tinf, Cinf, Tenv, Cenv = env_fns()
    p = dict(core.DEF)
    rec('=== T1-3 界面系数口径对照（M6 积分平均 vs 沿 1/D 调和型积分）===')
    rec('')
    ra = run(t, Tinf, Cinf, p, 'avg')
    rh = run(t, Tinf, Cinf, p, 'harm')
    idx = [int(round(r * 0.02 / 0.25e-3)) for r in RHO]
    rec('%6s %14s %14s %12s' % ('t/s', 'M6 积分平均', '调和型积分', 'Δ'))
    dm = 0.0
    for s in SNAP:
        d = float(np.max(np.abs(ra['C_snap'][s][idx] - rh['C_snap'][s][idx])))
        dm = max(dm, d)
        rec('%6d %14.6f %14.6f %12.2e' % (s, ra['C_snap'][s][idx[-1]], rh['C_snap'][s][idx[-1]], d))
    rec('')
    rec('全场（7 快照 × 5 列）|ΔC| 最大 = %.3e kg/kg' % dm)
    rec('4 位小数分辨率 = 5e-5；判定：差异%s量级'
        % ('在末位以下' if dm < 5e-5 else '已进入末位'))
    rec('')
    rec('结论：Q1 内 D(C) 仅变 21%% ⟹ 两种取法差异%s；'
        % ('不可辨识' if dm < 5e-5 else '可辨识，须回询'))
    rec('      **Q1 交付口径维持 M6 不变**；本项价值在为 Q2–Q4（D 跨数量级）统一口径提供依据。')
    print('LOG:', rec.save())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
