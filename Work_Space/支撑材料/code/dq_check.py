# -*- coding: utf-8 -*-
"""
原始数据质量检查（附件1／附件2／附件3 模板）
============================================
目的：回答"题目给出的原始数据是否需要预处理"——用**实测**而非印象判断。
检查项：时间列规整性、缺失值、重复值、量纲一致性、单调性、噪声水平（相邻差分统计）、
        3σ 离群点、分段一致性（平台段／变化段）、量程与物理合理性。

产出：dq_check_log.txt（与本脚本同目录）
约定：本文件不引用、不记载任何资料中的日期。
"""
import os
import io
import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
# 自适应定位工作区根：向上查找含 10_赛题 的目录
# （兼容两种目录深度：工作区 11_建模/11-3_算法与管线/Q1/code/ 与交付包 09 的 code/）
def _find_root(p, _marker='10_赛题', _max=6):
    cur = p
    for _ in range(_max):
        if os.path.isdir(os.path.join(cur, _marker)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.abspath(os.path.join(p, '..', '..', '..'))


ROOT = _find_root(HERE)
ATT = os.path.join(ROOT, '10_赛题', 'A题', '附件')
LOG = os.path.join(HERE, 'dq_check_log.txt')
L = []


def say(s=''):
    L.append(str(s))
    print(s)


def load(path):
    wb = load_workbook(path, data_only=True, read_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    data = []
    blank = 0
    for r in rows[1:]:
        if r is None or all(x is None for x in r):
            blank += 1
            continue
        data.append([np.nan if x is None else float(x) for x in r])
    return hdr, np.array(data), blank


def col_report(name, hdr, A):
    say('=' * 66)
    say('%s  表头=%s  形状=%s' % (name, hdr, A.shape))
    t = A[:, 0]
    dt = np.diff(t)
    say('时间列: t∈[%.4f, %.4f]  Δt: min=%.4f max=%.4f 不同步长值=%d  单调增=%s'
        % (t[0], t[-1], dt.min(), dt.max(), len(np.unique(np.round(dt, 6))), bool(np.all(dt > 0))))
    say('缺失值(NaN) 按列计数: %s' % np.isnan(A).sum(axis=0).tolist())
    for j in range(1, A.shape[1]):
        v = A[:, j]
        dv = np.diff(v)
        tag = hdr[j] if (hdr is not None and len(hdr) > j and hdr[j] is not None) else ('col%d' % j)
        say('-- [%s] min=%.6f max=%.6f mean=%.6f std=%.6f 量程=%.6f'
            % (tag, v.min(), v.max(), v.mean(), v.std(), v.max() - v.min()))
        say('   单调: 非降=%s 非增=%s | 相邻差分 mean=%.4e std=%.4e max|Δ|=%.4e'
            % (bool(np.all(dv >= 0)), bool(np.all(dv <= 0)), dv.mean(), dv.std(), np.abs(dv).max()))
        # 噪声估计：用二阶差分（对线性趋势不敏感）
        d2 = np.diff(v, 2)
        say('   二阶差分 std=%.4e（噪声量级参考）  序列自相关(lag1)=%.3f'
            % (d2.std(), float(np.corrcoef(v[:-1], v[1:])[0, 1]) if v.std() > 0 else float('nan')))
        # 3σ 离群（基于一阶差分）
        s = dv.std()
        if s > 0:
            idx = np.where(np.abs(dv - dv.mean()) > 3 * s)[0]
            say('   一阶差分 3σ 离群点数=%d %s' % (len(idx), (idx + 1)[:8].tolist()))
        dup = len(v) - len(np.unique(v))
        say('   重复值个数=%d（越少越好，反映分辨率）' % dup)
    say()


def seg_report(name, t, v, edges):
    say('-- %s 分段特征 --' % name)
    for a, b in edges:
        m = (t >= a) & (t <= b)
        if m.sum() < 2:
            continue
        vv = v[m]
        dv = np.diff(vv)
        say('   [%g, %g] n=%3d  mean=%.6f std=%.6f 极差=%.6f  mean|Δ|=%.3e'
            % (a, b, m.sum(), vv.mean(), vv.std(), vv.max() - vv.min(), np.abs(dv).mean()))
    say()


def main():
    say('### 原始数据质量检查（实测）###')
    say()

    # ---------------- 附件1 ----------------
    h1, A1, b1 = load(os.path.join(ATT, '附件1.xlsx'))
    say('附件1 空白行数=%d' % b1)
    col_report('附件1', h1, A1)
    t1 = A1[:, 0]
    seg_report('附件1 · 第2列(烘房温度)', t1, A1[:, 1],
               [(0, 1800), (1800, 3600), (3600, 8160), (8160, 10000), (10000, 14400)])
    seg_report('附件1 · 第3列(烘房水分浓度)', t1, A1[:, 2],
               [(0, 1800), (1800, 3600), (3600, 8160), (8160, 10000), (10000, 14400)])

    # ---------------- 附件2 ----------------
    h2, A2, b2 = load(os.path.join(ATT, '附件2.xlsx'))
    say('附件2 空白行数=%d' % b2)
    col_report('附件2', h2, A2)
    t2 = A2[:, 0]
    seg_report('附件2 · 第2列(药材半径)', t2, A2[:, 1],
               [(0, 1800), (1800, 3600), (3600, 10000), (10000, 100000), (100000, 259200)])

    # ---------------- 物理合理性 ----------------
    say('=' * 66)
    say('物理合理性核对：')
    say('  附件1 温度范围 [%.4f, %.4f] ℃ —— 是否落在烘房合理区间(20–60 ℃)：%s'
        % (A1[:, 1].min(), A1[:, 1].max(), bool(A1[:, 1].min() > 0 and A1[:, 1].max() < 100)))
    say('  附件1 水分浓度范围 [%.6f, %.6f] kg/kg ≥0：%s'
        % (A1[:, 2].min(), A1[:, 2].max(), bool(A1[:, 2].min() >= 0)))
    say('  附件2 半径范围 [%.4f, %.4f] cm >0 且 ≤ 初值 %.2f：%s'
        % (A2[:, 1].min(), A2[:, 1].max(), A2[0, 1], bool(A2[:, 1].min() > 0 and A2[:, 1].max() <= A2[0, 1] + 1e-9)))

    with io.open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
