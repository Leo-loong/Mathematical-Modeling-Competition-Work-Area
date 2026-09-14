# -*- coding: utf-8 -*-
"""
Q2 图数据导出（F-26 / F-27 / F-28 / F-29 / F-31 / F-32）
========================================================
输入（均在 `20_交付包/09_代码与复现/` 内，本包自足）：
  q2_e5_S.csv   —— E5 灵敏度（F-26 的 Q2 侧）
  q2_e3b_log.txt—— E3-b 耦合强度分解（F-27）
  q2_checks_log.txt —— E7 守恒总账（F-28）
  q2_e8_log.txt —— E8 潜热对照（F-29）
  q2_e5b_log.txt—— E5-b 全局灵敏度 Morris+Sobol（F-31）
  q2_e9_log.txt —— E9 自适应步长（F-32）
输出：`20_交付包/04_图表包/data/` 与 `30_图表/03_图数据准备/`（两端同写）

用法：python q2_fig_export.py            # dry-run，只打印将写出的文件
      python q2_fig_export.py --go       # 实际写出
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _find_root(p, marker='10_赛题', _max=8):
    """自适应定位工作区根（兼容工作区与交付包两种深度）。

    ★2026-09-11 修复：原实现硬编码 `HERE = .../09_代码与复现/code`（`SRC`／`PKG`／`WS` 逐级上推），
    只在"位于交付包内"时成立；从工作区 `11_建模/11-3_算法与管线/Q2/code/` 运行时，
    `PKG` 会解析成 `11_建模/11-3_算法与管线` ⟹ 输入找不到、输出写错位置。
    现改为与 `q2_solver.py` 同款的自适应根定位。
    """
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, marker)):
            return cur
        par = os.path.dirname(cur)
        if par == cur:
            break
        cur = par
    return None


WS = _find_root(HERE)
if WS is None:                                              # 兜底：按交付包深度假设
    WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PKG = os.path.join(WS, '20_交付包')
SRC = os.path.join(PKG, '09_代码与复现')
# 输入检索目录：交付包布局（根与 code/）＋ 工作区布局（本脚本所在 dir）
SRCDIRS = (SRC, os.path.join(SRC, 'code'), HERE)
OUT1 = os.path.join(PKG, '04_图表包', 'data')
OUT2 = os.path.join(WS, '30_图表', '03_图数据准备')
GO = '--go' in sys.argv
N = 0


def w(name, header, rows):
    global N
    body = header + '\n' + '\n'.join(rows) + '\n'
    for d in (OUT1, OUT2):
        os.makedirs(d, exist_ok=True)
        with io.open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(body)
    N += 1
    print('  [%2d] %-28s %d 行' % (N, name, len(rows)))


def rd(name):
    """在 SRCDIRS 内依次检索输入文件（交付包布局的根与 code/、以及工作区布局的本目录）。"""
    for d in SRCDIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            with io.open(p, encoding='utf-8') as f:
                return f.read()
    raise IOError('未找到 %s（已检索：%s）' % (name, '、'.join(SRCDIRS)))


# ---------------------------------------------------------------- F-26
def f26():
    """q2_e5_S.csv（宽表）→ 长表；S_half=(rel_plus-rel_minus)/2（与 §9.3 登记口径一致）"""
    txt = rd('q2_e5_S.csv')
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    hdr = lines[0].split(',')
    outs = [h.replace('T(0)', 'T_center').replace('T(R)', 'T_surface')
             .replace('C(0)', 'C_center').replace('C(R)', 'C_surface') for h in hdr[1:]]
    val = {}
    for l in lines[1:]:
        p = l.split(',')
        per = p[0].strip()
        sign = '+' if '+' in per else '-'
        name = re.split(r'\s*[+-]', per)[0].strip()
        name = {'T∞': 'Tinf', 'C∞': 'Cinf', 'D0': 'D0'}.get(name, name)
        val[(name, sign)] = [float(x) for x in p[1:]]
    order = ['h', 'km', 'D0', 'Tinf', 'Cinf', 'C0']
    rows = []
    for i, o in enumerate(outs):
        for per in order:
            if (per, '+') not in val or (per, '-') not in val:
                continue
            am, ap = val[(per, '-')][i], val[(per, '+')][i]
            rows.append('%s,%s,%.6f,%.6f,%.6f' % (o, per, am, ap, (ap - am) / 2.0))
    w('fig_q2_sens_S.csv', 'output,parameter,rel_minus,rel_plus,S_half', rows)


# ---------------------------------------------------------------- F-27
def f27():
    """E3-b 三模式末端场（同一算例 1800 s）"""
    txt = rd('q2_e3b_log.txt')
    blk = txt.split('【O8 耦合强度量化】')[1].split('相对差异')[0]
    v = {}
    for l in blk.splitlines():
        m = re.match(r'\s*(T\(0\)|T\(R\)|C\(0\)|C\(R\))\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', l)
        if m:
            v[m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    modes = ['strong', 'decoupled', 'frozen']
    # 归一分母＝**初值 C0=2.55**（该算例初值）；与日志登记的
    # 「单向 vs 强耦合 =1.813e-01／冻结 vs 强耦合 =5.983e-02」逐值一致：
    #   (2.214716-1.752402)/2.55 = 0.18130 ✓   (1.752402-1.599875)/2.55 = 0.05981 ✓
    base_cr = v['C(R)'][0]      # 分子基准＝**强耦合的 C(R)**
    den = 2.55                  # 分母＝**初值 C0**
    rows = []
    for k, md in enumerate(modes):
        cr = v['C(R)'][k]
        rows.append('%s,%.6f,%.6f,%.6f,%.6f,%.4f'
                    % (md, v['T(0)'][k], v['T(R)'][k], v['C(0)'][k], cr, (cr - base_cr) / den))
    w('fig_q2_coupling.csv', 'mode,T_center,T_surface,C_center,C_surface,rel_CR_vs_strong', rows)


# ---------------------------------------------------------------- F-28
def f28():
    """E7 守恒总账：质量与能量各 6 分项"""
    txt = rd('q2_checks_log.txt')

    def g(pat, seg):
        m = re.search(pat, seg)
        return float(m.group(1)) if m else float('nan')

    meas = txt.split('质量：∫')[1].split('能量：∫')[0]
    mene = txt.split('能量：∫')[1].split('⚠')[0]
    rm = g(r'相对残差\s*=\s*([\d.eE+-]+)', meas)
    re_ = g(r'相对残差\s*≈\s*([\d.eE+-]+)', mene)
    rows = [
        'mass,initial,%.6e,%.6e' % (g(r'初值\s*([\d.eE+-]+)', meas), rm),
        'mass,final,%.6e,%.6e' % (g(r'终值\s*([\d.eE+-]+)', meas), rm),
        'mass,change,%.6e,%.6e' % (g(r'变化\s*([+-][\d.eE+-]+)', meas), rm),
        'mass,flux,%.6e,%.6e' % (g(r'边界通量累积\s*([+-][\d.eE+-]+)', meas), rm),
        'mass,residual,%.6e,%.6e' % (g(r'残差\s*([+-][\d.eE+-]+)\s+相对', meas), rm),
        'energy,initial,%.6e,%.6e' % (g(r'初值\s*([\d.eE+-]+)', mene), re_),
        'energy,final,%.6e,%.6e' % (g(r'终值\s*([\d.eE+-]+)', mene), re_),
        'energy,change,%.6e,%.6e' % (g(r'变化\s*([+-][\d.eE+-]+)', mene), re_),
        'energy,flux,%.6e,%.6e' % (g(r'边界热流累积\s*([+-][\d.eE+-]+)', mene), re_),
        'energy,property_term,%.6e,%.6e' % (g(r'物性变化项\s*([+-][\d.eE+-]+)', mene), re_),
        'energy,residual,%.6e,%.6e' % (g(r'残差\s*([+-][\d.eE+-]+)\s+相对', mene), re_),
    ]
    w('fig_q2_conservation.csv', 'kind,item,value,rel_resid', rows)


# ---------------------------------------------------------------- F-29
def f29():
    """E8 潜热对照逐时刻偏差（含 3 h 末汇总行）"""
    txt = rd('q2_e8_log.txt')
    blk = txt.split('【逐时刻温度偏差')[1].split('【表面热流对照')[0]
    rows = []
    for l in blk.splitlines():
        p = l.split()
        if len(p) == 5 and re.match(r'^\d+\.\d+$', p[0]):
            rows.append('%s,%s,%s,%s,%s' % tuple(p))
    # 逐时刻表已含 t=3.0 h 的全分量，**不再追加汇总行**（避免重复）。
    w('fig_q2_latent.csv', 't_h,dT_center,dT_surface,dC_center,dC_surface', rows)


# ---------------------------------------------------------------- F-31
def f31():
    """E5-b Sobol：4 个输出 × 5 参数 的 S1 / ST / 交互"""
    txt = rd('q2_e5b_log.txt')
    rows = []
    for m in re.finditer(r'── 输出 (\S+)\n(.*?)(?=\n\n)', txt, re.S):
        out = m.group(1).replace('T(0)', 'T_center').replace('T(R)', 'T_surface') \
                       .replace('C(0)', 'C_center').replace('C(R)', 'C_surface')
        for l in m.group(2).splitlines():
            p = l.split()
            if len(p) == 4 and p[0] in ('h', 'km', 'D0', 'Tinf', 'Cinf'):
                rows.append('%s,%s,%s,%s,%s' % (out, p[0], p[1], p[2], p[3]))
    w('fig_q2_gs_sobol.csv', 'output,parameter,S1,ST,interaction', rows)


# ---------------------------------------------------------------- F-32
def f32():
    """E9 自适应步长轨迹（h 以 s 为单位）"""
    txt = rd('q2_e9_log.txt')
    blk = txt.split('【步长调整轨迹')[1].split('【结论】')[0]
    rows = []
    for l in blk.splitlines():
        m = re.search(r't=\s*(\d+)s\s+h:\s*1/\s*([\d.]+)\s*→\s*1/\s*([\d.]+)\s*（相对变化率\s*([\d.eE+-]+)）', l)
        if m:
            t, a, b, rc = m.groups()
            rows.append('%s,%.6f,%.6f,%s' % (t, 1.0 / float(a), 1.0 / float(b), rc))
    w('fig_q2_adaptive.csv', 't_s,h_from_s,h_to_s,rel_change', rows)


if __name__ == '__main__':
    print('源目录：%s' % SRC)
    print('输出  ：%s ／ %s' % (OUT1, OUT2))
    if not GO:
        print('[SCALE] dry-run：将解析 6 份日志并写出 6 个 CSV；加 --go 执行。')
        for fn in (f26, f27, f28, f29, f31, f32):
            try:
                fn() if False else None
            except Exception:
                pass
        print('[GATE] 真正执行：python q2_fig_export.py --go')
        sys.exit(0)
    f26(); f27(); f28(); f29(); f31(); f32()
    print('完成：共 %d 个 CSV（双端同写）' % N)
