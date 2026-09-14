# -*- coding: utf-8 -*-
"""
A 题 Q2 主力求解：变物性双向耦合 · 0–3 h 全程 → result2.xlsx
======================================================
口径（全部引自《A_数值口径总表》，禁止手抄）
------------------------------------------
  K10  Q2 全程用附录3、无物性阶段切换
  N7–N10  变物性公式（ρ、c_p、k、D）
  N4/N5   h=25、k_m=8e-7（H5 沿用附录2）
  H6/N19/N20  t>14400 s 外推：T∞=50.00 ℃、C∞=0.04999 kg/kg
  K12/O3  result2 = 0–3 h @1 s（10800 行 × 22 列），4 位小数（O6）
  O5      内部 SI，输出回填 s / cm / ℃

数值设置（W2 预试验定值）
------------------------
  Δr = 0.25 mm（N=80 区间／81 节点）—— 输出点＝计算点
  内部步长 h = 1/32 s（n_sub=32，T 与 C 统一）
  格式：IMEX 交替推进（物性每内部子步更新；滞后误差 ∝ h ≈ 1e-8 K 量级）

运行（**须显式 `--go`**，见《工作约束》§12.1 运行闸门；前台带进度，结束后按 Enter 退出）：
  Linux/macOS :  Q2_CORE=c python q2_solver.py --go
  Windows PS  :  $env:Q2_CORE='c'; python q2_solver.py --go
不加 --go 时**只打印 [SCALE] 规模声明并退出**，不执行求解。
"""
import sys
import os
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# 线程环境变量须早于 numpy 导入：小规模三对角求解无需 BLAS/OMP 多线程，
# 关闭可避免每次调用的线程调度开销（零数值影响，纯环境级优化）
for _v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np                                              # noqa: E402
from openpyxl import Workbook                                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# 求解核可切换（环境变量 Q2_CORE）：
#   ★默认 'c'   ——  q2_core_c   ★B+C 版（numba JIT ＋ 手写追赶法）
#                   **唯一符合 M6 口径（界面系数沿 C 的积分平均）的 Q2 核；
#                   交付文件 result2.xlsx 必须由本核产出**（见《A_复核差异台账》D-22）
#   'b'         ——  q2_core     B 版（numba JIT ＋ solve_banded）
#                   ⚠ 旧口径：界面系数仍为"距离加权调和平均"，
#                   **不得用于重出交付文件**（仅保留作口径对照）
#   'orig'      ——  q2_core_orig 优化前基线（仅供对照，不建议在主力中使用）
_CORE = os.environ.get('Q2_CORE', 'c').strip().lower()
if _CORE == 'c':
    from q2_core_c import run_q2, DEF2                            # noqa: E402
elif _CORE == 'orig':
    from q2_core_orig import run_q2, DEF2                         # noqa: E402
else:
    from q2_core import run_q2, DEF2                              # noqa: E402


def _find_root(p, marker='10_赛题', _max=6):
    """自适应定位工作区根（兼容工作区与交付包两种深度）"""
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
        par = os.path.dirname(cur)
        if par == cur:
            break
        cur = par
    return os.path.abspath(os.path.join(p, '..', '..', '..'))


ROOT = _find_root(HERE)
ATT1 = os.path.join(ROOT, '10_赛题', 'A题', '附件', '附件1.xlsx')
RESDIR = os.path.join(ROOT, '20_交付包', '09_代码与复现', 'results')
RES2 = os.path.join(RESDIR, 'result2.xlsx')
LOG = os.path.join(HERE, 'q2_run_log.txt')

# ---------------- 数值设置 ----------------
DR = 2.5e-4        # 空间步长（m）
N = 80             # 区间数（节点 81）
DT_OUT = 1.0       # 输出步长（s）
NSTEP = 10800      # 3 h（K12）
NSUB = 32          # 内部子步数（内部步长 1/32 s，W2 定值）
COLS = np.arange(0, N + 1, 4)     # 0, 0.1, …, 2.0 cm（21 列）
SNAP = (1800, 3600, 5400, 7200, 9000, 10800)   # 表3/表4 取用时刻（0.5–3 h）
T_EXT, C_EXT = 50.00, 0.04999     # H6/N19/N20 外推值

BUF = []


def say(s=''):
    print(s, flush=True)
    BUF.append(s)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')


def load_att1():
    """读附件1（烘房温度与水分浓度时序），返回 (t, T, C)"""
    from openpyxl import load_workbook
    wb = load_workbook(ATT1, data_only=True)
    ws = wb.active
    rows = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    hdr = rows[0]
    data = [r for r in rows[1:] if r[0] is not None]
    t = np.array([float(r[0]) for r in data], dtype=float)
    T = np.array([float(r[1]) for r in data], dtype=float)
    C = np.array([float(r[2]) for r in data], dtype=float)
    return t, T, C, hdr


def main():
    open(LOG, 'w', encoding='utf-8').close()
    t0 = time.time()
    say('=' * 78)
    say('A 题 · 第二问（Q2）主力求解：变物性双向耦合 0–3 h')
    say(f'求解核：{_CORE.upper()} 版（Q2_CORE 环境变量；b=numba+solve_banded，'
        f'c=numba+手写追赶法）')
    say('=' * 78)

    # ---------- 附件核验 ----------
    t1, T1, C1, hdr = load_att1()
    say(f'[附件1] 表头={hdr}  点数={len(t1)}  时间 {t1[0]:.0f}–{t1[-1]:.0f} s  '
        f'步长={t1[1]-t1[0]:.0f} s')
    say(f'        温度 {T1.min():.4f}–{T1.max():.4f} ℃   '
        f'水分浓度 {C1.min():.5f}–{C1.max():.5f} kg/kg')
    say(f'        外推（H6，t>{t1[-1]:.0f} s）：T∞={T_EXT} ℃，C∞={C_EXT} kg/kg')

    def Tenv(t):
        return float(np.interp(t, t1, T1)) if t <= t1[-1] else T_EXT

    def Cenv(t):
        return float(np.interp(t, t1, C1)) if t <= t1[-1] else C_EXT

    # ---------- 求解 ----------
    say(f'\n[求解] Δr={DR*1e3:.2f} mm（N={N}区间/{N+1}节点）  输出步长={DT_OUT:g} s  '
        f'内部步长=1/{NSUB} s  格式=IMEX')
    say(f'       共 {NSTEP} 个输出步，预计约 {NSTEP*NSUB*0.0006/60:.1f} 分钟…')
    res, tableT, tableC = run_q2(N=N, dr=DR, dt_out=DT_OUT, nsteps=NSTEP,
                                 Tenv_fn=Tenv, Cenv_fn=Cenv, n_sub=NSUB,
                                 mode='coupled', cols=COLS, snap_at=SNAP,
                                 progress=1800)
    wall = time.time() - t0
    st = res['stats']
    say(f'[完成] 耗时 {wall:.1f} s  内层均 {st["inner_tot"]/max(1,st["nsub"]):.1f} 次/步  '
        f'内层最大残差 {st["resC_max"]:.2e}  异常标记 {st["flags"]}')

    T_end, C_end = res['T_end'], res['C_end']
    say(f'[终态] T(0)={T_end[0]:.4f} ℃  T(R)={T_end[-1]:.4f} ℃  '
        f'C(0)={C_end[0]:.6f}  C(R)={C_end[-1]:.6f}  max_r C={C_end.max():.6f}')

    # ---------- 写 result2.xlsx ----------
    os.makedirs(RESDIR, exist_ok=True)
    wb = Workbook(write_only=True)
    for name, tab in (('温度', tableT), ('水分浓度', tableC)):
        ws = wb.create_sheet(name)
        # 表头与附件3 模板一致（首列名 + 数值型距离列头）
        ws.append(['时间\\到药材中心的距离'] + [round(c * DR * 100, 1) for c in COLS])
        t = time.time()
        for i in range(NSTEP):
            ws.append([i + 1] + [round(float(v), 4) for v in tab[i]])
        say(f'  写入表「{name}」：{NSTEP} 行 × {len(COLS)+1} 列  {time.time()-t:.1f}s')
    wb.save(RES2)
    say(f'[输出] {os.path.relpath(RES2, ROOT)}  '
        f'（{os.path.getsize(RES2)/1048576:.2f} MB）')

    # ---------- 程序化断言 ----------
    # 判据上界一律由**输入数据**推出，不得硬编码（旧版写死 50.01，而附件1 实测最高
    # 50.246 ℃ —— 只是"碰巧"未触发，属判据缺陷，本轮修正）
    T_ENV_MAX = float(np.max(T1))          # 附件1 环境温度最大值
    T_ENV_MIN = float(np.min(T1))
    T_UB = T_ENV_MAX + 0.01                # 容差 0.01 ℃
    T_LB = min(T_ENV_MIN, DEF2['T0']) - 0.01
    say('\n[断言]')
    chk = []
    chk.append((f'形状 {NSTEP}×{len(COLS)+1}', tableT.shape == (NSTEP, len(COLS))
                and tableC.shape == (NSTEP, len(COLS))))
    chk.append((f'温度不超环境极值 {T_UB:.4f} ℃', bool(np.nanmax(tableT) <= T_UB)))
    chk.append((f'温度不低于下界 {T_LB:.4f} ℃', bool(np.nanmin(tableT) >= T_LB)))
    chk.append(('含水率非负', bool(np.nanmin(tableC) >= 0.0)))
    dC = np.diff(tableC, axis=0)
    chk.append(('含水率单调不增', bool(np.all(dC <= 1e-9))))
    chk.append((f'含水率不超初值 {DEF2["C0"]}', bool(np.nanmax(tableC) <= DEF2['C0'] + 1e-4)))
    for name, ok in chk:
        say(f'   {"PASS" if ok else "FAIL"}  {name}')
    if not all(ok for _, ok in chk):
        say('\n⚠ 有断言未通过，请勿采信本结果！')
    else:
        say('\n✅ 全部断言通过。')

    # ---------- 表3/表4 关键值 ----------
    say('\n[表3/表4 取用时刻的关键值]  （0.5–3 h）')
    say(f'{"t/h":>6} {"T(0)":>10} {"T(R)":>10} {"C(0)":>12} {"C(R)":>12} {"maxC":>12}')
    for n in SNAP:
        Tv, Cv = res['T_snap'][n], res['C_snap'][n]
        say(f'{n/3600:6.1f} {Tv[0]:10.4f} {Tv[-1]:10.4f} '
            f'{Cv[0]:12.6f} {Cv[-1]:12.6f} {Cv.max():12.6f}')

    say(f'\n总耗时 {time.time()-t0:.1f} s   日志：{LOG}')


# ---------------------------------------------------------------------------
# 运行闸门（《工作约束》§12.1）：默认只"声明规模"并退出；须显式 `--go`
# （或环境变量 ALLOW_RUN=1）且规模不超批准值，才真正执行。
# 首行输出 [SCALE] 声明行，便于事后审计。
# ---------------------------------------------------------------------------
def _gate(name, scale, approved=None, argv=None, env=None):
    args = sys.argv if argv is None else argv
    envv = os.environ if env is None else env
    print('[SCALE] %s | ' % name + ' | '.join('%s=%s' % (k, v) for k, v in scale.items()),
          flush=True)
    if not (('--go' in args) or (envv.get('ALLOW_RUN', '') == '1')):
        print('[GATE] 未传入 --go（或 ALLOW_RUN=1）⟹ 仅声明规模，不执行。', flush=True)
        print('[GATE] 真正执行：Q2_CORE=c python %s --go'
              % os.path.basename(__file__), flush=True)
        return False
    if approved:
        bad = ['%s %s>%s' % (k, scale[k], approved[k])
               for k in approved if k in scale and scale[k] > approved[k]]
        if bad:
            print('[GATE] 规模超批准值（%s）⟹ 拒绝执行。' % '；'.join(bad), flush=True)
            return False
    print('[GATE] 规模在校验范围内 ⟹ 执行。', flush=True)
    return True


if __name__ == '__main__':
    if not _gate('Q2 主力求解',
                 dict(核=_CORE, 网格='Δr=0.25 mm（81 节点）',
                      输出='0–10800 s @1 s（10800 行）', 内部子步='1/32 s',
                      预计耗时='约 85–130 s')):
        sys.exit(0)
    main()
    try:
        if sys.stdin.isatty():          # 仅在交互式终端下等待，避免后台运行挂起
            input('\n按 Enter 键退出...')
    except Exception:
        pass
