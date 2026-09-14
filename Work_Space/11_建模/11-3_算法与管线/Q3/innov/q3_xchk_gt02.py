# -*- coding: utf-8 -*-
"""
外部核验 XCHK-2｜**在"机构等效配置"上做单变量实验**，定位机构 Q3 与
我方 Q3（57.5314 h）之间巨大差异的根因
================================================================================
背景（第一手资料，非转述）：
  · 机构 GT02（MATLAB）`drying_common.m`：**界面系数一律用距离加权调和平均**
    （`coefFace = harmonic_mean(coef(1:end-1),coef(2:end))`，T 传 k、C 传 D）；
  · **Picard 仅 3 次**（`cfg.picardIter = 3`）、松弛 0.85、容差 1e-7；
  · Q3 用 `dt = 30 s`、N = 20；
  · 环境 `air_at` 用 **pchip 并把 t 钳位到附件1 末点**（t>14400 s 后取 50.165 / 0.04986）。
  机构 `result3.xlsx` / `q3_每6小时含水率汇总.xlsx` 的真实输出：
    C(0): 6 h→1.0201, 12 h→0.4576, 48 h→0.2757, **552 h→0.1508 ⟹ t_dry ≈ 552–558 h**
  （机构论文写 55.13 h，与其自身代码输出**相差约 10 倍**。）

本实验：把上述每一项做成**可切换开关**，逐项分离贡献：
  dmode：D 的界面取法 0=调和(机构) 1=算术 2=沿C积分(我方)
  kmode：k 的界面取法 同上
  maxit/omega/tol：Picard（机构 3 / 0.85 / 1e-7；我方 30 / 0.7 / 1e-10）
  airmode：1=附件1末点(机构) 2=后段均值(我方 50.00/0.04999)
  nsub：每 60 s 的子步数（30 s→2；1/32 s→1920）
  N：网格（机构 20；我方 80）

纪律：只读附件1 与我方既有核；产物写入 innov/；不触碰任何正式文件。
用法：python q3_xchk_gt02.py [--smoke]
"""
import os
import sys
import time
import argparse

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np


def _find_root(p, marker='10_赛题', _max=6):
    cur = os.path.abspath(p)
    for _ in range(_max):
        cur = os.path.dirname(cur)
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
    return None


HERE = os.path.dirname(os.path.abspath(__file__))
Q3DIR = os.path.dirname(HERE)
WS = _find_root(HERE)
sys.path.insert(0, Q3DIR)
sys.path.insert(0, os.path.join(WS, '11_建模', '11-3_算法与管线', 'Q2', 'code'))
OUTDIR = os.path.join(HERE, 'out')
LOGDIR = os.path.join(HERE, 'logs')
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(LOGDIR, exist_ok=True)

import openpyxl                                                      # noqa: E402
from q2_core_c import (njit, _rho_nb, _cp_nb, _k_nb,                 # noqa: E402
                       _assemble_T_nb, _rhs_T_nb, _assemble_C_nb,
                       _rhs_C_nb, _thomas_nb, DEF2)
import q3_core as q3                                                 # noqa: E402

R0, HC, KM = DEF2['R0'], DEF2['h'], DEF2['km']
DT_OUT, C_CRIT = 60.0, 0.15
BUF = []


def say(s=''):
    print(s)
    BUF.append(str(s))


# ────────────────────────────────────────────────────────────────
# 界面系数（三种取法，njit）
# ────────────────────────────────────────────────────────────────
@njit(cache=True, fastmath=False)
def _D_node(Carr, Tarr, i, d_fac):
    c = Carr[i]
    if c < 1e-9:
        c = 1e-9
    return d_fac * 2.4e-3 * np.exp(-0.45 / c) * np.exp(-3850.0 / (Tarr[i] + 273.15))


@njit(cache=True, fastmath=False)
def _faceD(Carr, Tarr, d_fac, mode, nsamp):
    """界面 D：0=节点 D 的调和平均（机构）1=算术平均 2=沿 C 积分平均（我方）"""
    n = Carr.shape[0] - 1
    out = np.zeros(n)
    for i in range(n):
        if mode == 2:
            a = Carr[i]
            b = Carr[i + 1]
            Tm = 0.5 * (Tarr[i] + Tarr[i + 1])
            s = 0.0
            for k in range(nsamp):
                x = a + (b - a) * (k + 0.5) / nsamp
                if x < 1e-9:
                    x = 1e-9
                s += d_fac * 2.4e-3 * np.exp(-0.45 / x) * np.exp(-3850.0 / (Tm + 273.15))
            out[i] = s / nsamp
        else:
            dl = _D_node(Carr, Tarr, i, d_fac)
            dr = _D_node(Carr, Tarr, i + 1, d_fac)
            if mode == 0:
                out[i] = 2.0 * dl * dr / (dl + dr) if (dl > 0.0 and dr > 0.0) else 0.0
            else:
                out[i] = 0.5 * (dl + dr)
    return out


@njit(cache=True, fastmath=False)
def _facek(Carr, mode):
    """界面 k：0=调和 1=算术 2=沿 C 积分平均（解析式，附录3）"""
    n = Carr.shape[0] - 1
    out = np.zeros(n)
    for i in range(n):
        a = Carr[i]
        b = Carr[i + 1]
        ka = 0.21 + 0.38 * a / (a + 1.0)
        kb = 0.21 + 0.38 * b / (b + 1.0)
        if mode == 0:
            out[i] = 2.0 * ka * kb / (ka + kb) if (ka + kb) > 0.0 else 0.0
        elif mode == 1:
            out[i] = 0.5 * (ka + kb)
        else:
            dC = b - a
            if dC < 1e-14 and dC > -1e-14:
                out[i] = ka
            else:
                out[i] = 0.21 + 0.38 * ((b - np.log(1.0 + b))
                                        - (a - np.log(1.0 + a))) / dC
    return out


@njit(cache=True, fastmath=False)
def _step(N, dr, h, n_sub, R0, hc, km, T, C, t0, ts_env, Tenv_v, Cenv_v,
          d_fac, dmode, kmode, nsamp, omega, tol, maxit):
    """一个输出步（n_sub 个内部子步）；Picard 参数与机构一致时可完全等效。
    ⚠ 与机构的唯一结构性差异：机构在 Picard 内**同时迭代 T 与 C**，
      本核先解一次 T、再对 C 做 Picard（属我方既有实现，已在文中声明）。"""
    NC = N + 1
    Tcur = T.copy()
    Ccur = C.copy()
    aT = np.zeros(NC); bT = np.zeros(NC); cT = np.zeros(NC)
    aC = np.zeros(NC); bC = np.zeros(NC); cC = np.zeros(NC)
    dT = np.zeros(NC); dC = np.zeros(NC)
    inner = 0
    for s in range(n_sub):
        ts = t0 + (s + 1) * h
        tinf = q3._interp1_nb(ts, ts_env, Tenv_v)
        cinf = q3._interp1_nb(ts, ts_env, Cenv_v)
        rho = _rho_nb(Ccur); cp = _cp_nb(Ccur); kk = _k_nb(Ccur)
        kf = _facek(Ccur, kmode)
        _assemble_T_nb(N, dr, h, R0, hc, rho, cp, kk, aT, bT, cT, kf)
        _rhs_T_nb(N, dr, h, R0, hc, rho, cp, Tcur, tinf, dT)
        Tcur = _thomas_nb(aT, bT, cT, dT)

        _rhs_C_nb(N, dr, h, R0, km, Ccur, cinf, dC)
        bse = dC.copy()
        Cit = Ccur.copy()
        for it in range(1, maxit + 1):
            Df = _faceD(Cit, Tcur, d_fac, dmode, nsamp)
            _assemble_C_nb(N, dr, h, Df, R0, km, aC, bC, cC)
            Ctry = _thomas_nb(aC, bC, cC, bse)
            Cnew = np.empty(NC)
            for i in range(NC):
                Cnew[i] = omega * Ctry[i] + (1.0 - omega) * Cit[i]
            num = 0.0; den = 0.0
            for i in range(NC):
                v = abs(Cnew[i] - Cit[i])
                if v > num: num = v
                w = abs(Cnew[i])
                if w > den: den = w
            if den < 1.0: den = 1.0
            rr = num / den
            Cit = Cnew
            inner += 1
            if rr < tol:
                break
        Ccur = Cit
    return Tcur, Ccur, inner


def load_env(airmode):
    wb = openpyxl.load_workbook(
        os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'), data_only=True)
    ws = wb.active
    rows = [r for r in ws.iter_rows(values_only=True)][1:]
    d = [r for r in rows if r[0] is not None]
    t = np.array([float(r[0]) for r in d])
    T = np.array([float(r[1]) for r in d])
    C = np.array([float(r[2]) for r in d])
    wb.close()
    if airmode == 1:                      # 机构：钳位到附件1 末点
        return q3.env_tables_from_att1(t, T, C, t_tail=t[-1],
                                       T_tail=float(T[-1]), C_tail=float(C[-1]))
    return q3.env_tables_from_att1(t, T, C)     # 我方：后段均值 50.00/0.04999


def run_case(N, nsub, dmode, kmode, maxit, omega, tol, airmode, max_hours,
             ts, Tv, Cv):
    dr = R0 / N
    h = DT_OUT / nsub
    T = np.full(N + 1, DEF2['T0'])
    C = np.full(N + 1, DEF2['C0'])
    nmax = int(round(max_hours * 3600.0 / DT_OUT))
    t0 = time.time()
    t_end = None
    for n in range(1, nmax + 1):
        t_start = (n - 1) * DT_OUT
        Tp, Cp = T.copy(), C.copy()
        T, C, _ = _step(N, dr, h, nsub, R0, HC, KM, T, C, t_start, ts, Tv, Cv,
                        1.0, dmode, kmode, 8, omega, tol, maxit)
        if float(np.max(C)) < C_CRIT:
            lo, hi = 1, nsub
            while lo < hi:
                mid = (lo + hi) // 2
                _, Ca, _ = _step(N, dr, h, mid, R0, HC, KM, Tp, Cp, t_start, ts, Tv, Cv,
                                 1.0, dmode, kmode, 8, omega, tol, maxit)
                if float(np.max(Ca)) < C_CRIT:
                    hi = mid
                else:
                    lo = mid + 1
            t_end = (t_start + lo * h) / 3600.0
            break
    return t_end, float(C[0]), float(C[-1]), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--smoke', action='store_true')
    args = ap.parse_args()

    say('=' * 104)
    say('XCHK-2 | 机构等效配置的单变量实验（Q3 · 附录3 · 判据 max C < 0.15）')
    say('=' * 104)
    say('  机构第一手事实：界面=调和平均；Picard 仅 3 次(ω=0.85, tol=1e-7)；')
    say('                  Q3 用 dt=30 s、N=20；环境钳位到附件1 末点；')
    say('                  其 result3 真实输出 t_dry ≈ 552–558 h（论文写 55.13 h）')

    tsA, TvA, CvA = load_env(1)
    tsB, TvB, CvB = load_env(2)
    wb = openpyxl.load_workbook(
        os.path.join(WS, '10_赛题', 'A题', '附件', '附件1.xlsx'), data_only=True)
    _r = [v for v in wb.active.iter_rows(values_only=True)]
    say('  [附件1] 末点 T=%.4f ℃, C=%.5f（机构钳位值）；后段均值口径 = 50.00 / 0.04999'
        % (float(_r[-1][1]), float(_r[-1][2])))
    wb.close()

    # (标签, N, nsub, dmode, kmode, maxit, omega, tol, airmode, max_hours)
    cases = [
        ('A 机构原版等效(调和·P3·30s·N20·末点)', 20, 2, 0, 0, 3, 0.85, 1e-7, 1, 700),
        ('B 仅收敛Picard(调和·P30·30s)', 20, 2, 0, 0, 30, 0.7, 1e-10, 1, 700),
        ('C 仅改界面(积分·P3·30s)', 20, 2, 2, 2, 3, 0.85, 1e-7, 1, 700),
        ('D 改界面+收敛(积分·P30·30s)', 20, 2, 2, 2, 30, 0.7, 1e-10, 1, 700),
        ('E 机构+L1我方口径(积分·P30·1/32s·N80·均值)', 80, 1920, 2, 2, 30, 0.7, 1e-10, 2, 120),
        ('F 机构口径但细网格(N80·调和·P3·30s)', 80, 2, 0, 0, 3, 0.85, 1e-7, 1, 700),
    ]
    if args.smoke:
        cases = [
            ('A 机构原版等效(调和·P3·30s·N20·末点)', 20, 2, 0, 0, 3, 0.85, 1e-7, 1, 60),
            ('D 改界面+收敛(积分·P30·30s)', 20, 2, 2, 2, 30, 0.7, 1e-10, 1, 60),
        ]

    say('')
    say('  %-46s %-10s %-11s %-11s %-9s' %
        ('配置', 't_dry/h', 'C(0)末', 'C(R)末', '墙钟/s'))
    say('  ' + '-' * 96)
    rec = []
    for (lab, N, nsub, dm, km_, mx, om, tl, am, mh) in cases:
        tsv, Tv, Cv = (tsA, TvA, CvA) if am == 1 else (tsB, TvB, CvB)
        te, c0, cR, wall = run_case(N, nsub, dm, km_, mx, om, tl, am, mh,
                                    tsv, Tv, Cv)
        rec.append((lab, te, c0, cR, wall))
        if te is None:
            say('  %-46s %-10s %-11.5f %-11.5f %-9.1f' % (lab, '>%g未达标' % mh, c0, cR, wall))
        else:
            say('  %-46s %-10.4f %-11.5f %-11.5f %-9.1f' % (lab, te, c0, cR, wall))

    say('')
    say('  【判读】')
    d = dict((r[0][0], r[1]) for r in rec)
    if d.get('A') is not None and d.get('B') is not None:
        say('   · A→B（仅把 Picard 由 3 次提到收敛）：%.4f → %.4f h' % (d['A'], d['B']))
    say('   · 若 A 远超 B ⟹ **Picard 欠收敛**是机构偏离的主因')

    with open(os.path.join(LOGDIR, 'q3_xchk_gt02.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(BUF) + '\n')
    if not args.smoke:
        with open(os.path.join(OUTDIR, 'fig_q3_xchk_gt02.csv'), 'w', encoding='utf-8') as f:
            f.write('case,t_dry_h\n')
            for lab, te, _, _, _ in rec:
                f.write('%s,%.6f\n' % (lab.split()[0], -1 if te is None else te))
    say('')
    say('  已写出 logs/q3_xchk_gt02.log 与 out/fig_q3_xchk_gt02.csv')


if __name__ == '__main__':
    main()
