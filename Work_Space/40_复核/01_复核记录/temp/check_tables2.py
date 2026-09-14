# -*- coding: utf-8 -*-
"""论文表1–6 ↔ result*.xlsx 逐格比对 v2（只读）"""
import sys, io
from pathlib import Path
from openpyxl import load_workbook
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"C:\Users\wang-\Desktop\2026数学建模\Work_Space")
RES = ROOT / "20_交付包" / "09_代码与复现" / "results"

T1 = {100:[28.0001,28.0003,28.0041,28.0327,28.1800],300:[28.0408,28.0635,28.1514,28.3680,28.8487],
      600:[28.4534,28.5360,28.8039,29.3159,30.1652],900:[29.3243,29.4583,29.8754,30.6161,31.7304],
      1200:[30.5427,30.7098,31.2223,32.1125,33.4276],1500:[31.9957,32.1867,32.7660,33.7463,35.1203],
      1800:[33.5753,33.7720,34.3642,35.3621,36.7855]}
T2 = {100:[2.5500,2.5500,2.5500,2.5500,2.2490],300:[2.5500,2.5500,2.5500,2.5492,2.0517],
      600:[2.5500,2.5500,2.5500,2.5352,1.8774],900:[2.5500,2.5500,2.5497,2.5045,1.7550],
      1200:[2.5500,2.5500,2.5482,2.4646,1.6588],1500:[2.5500,2.5499,2.5445,2.4206,1.5789],
      1800:[2.5500,2.5497,2.5383,2.3755,1.5104]}
T3 = {0.5:[32.1893,32.3822,32.9660,33.9608,35.4131],1.0:[40.3816,40.5536,41.0605,41.8783,42.9977],
      1.5:[45.8468,45.9348,46.1930,46.6051,47.1401],2.0:[48.4502,48.4881,48.5984,48.7736,49.0033],
      2.5:[49.4670,49.4792,49.5136,49.5653,49.6609],3.0:[49.8495,49.8553,49.8746,49.9101,49.9664]}
T4 = {0.5:[2.5499,2.5489,2.5255,2.3258,1.6486],1.0:[2.5257,2.4947,2.3578,2.0230,1.4711],
      1.5:[2.3860,2.3256,2.1344,1.8020,1.3475],2.0:[2.1708,2.1084,1.9236,1.6259,1.2311],
      2.5:[1.9567,1.9006,1.7360,1.4720,1.1166],3.0:[1.7662,1.7165,1.5702,1.3333,1.0081]}
T5 = {6:[1.0170,0.9881,0.9015,0.7550,0.5328],12:[0.4562,0.4432,0.4031,0.3298,0.1642],
      18:[0.2989,0.2916,0.2687,0.2253,0.0845],24:[0.2378,0.2328,0.2167,0.1856,0.0665],
      30:[0.2059,0.2019,0.1892,0.1641,0.0598],36:[0.1859,0.1826,0.1718,0.1504,0.0566],
      42:[0.1721,0.1692,0.1597,0.1407,0.0548],48:[0.1619,0.1592,0.1507,0.1335,0.0537],
      54:[0.1539,0.1515,0.1437,0.1278,0.0530],"end":[0.1500,None,None,None,0.0526]}
T6 = {0:[2.5500,2.5500,2.5500,2.5500,2.5500],6:[1.6276,1.4621,0.9868,"—",0.4173],
      12:[0.7021,0.6248,0.3930,"—",0.1598],18:[0.3958,0.3576,0.2340,"—",0.0869],
      24:[0.2794,0.2561,0.1763,"—",0.0665],30:[0.2232,0.2066,0.1477,"—",0.0591],
      36:[0.1909,0.1779,0.1306,"—",0.0558],42:[0.1699,0.1592,0.1193,"—",0.0540],
      48:[0.1552,0.1460,0.1110,"—",0.0529],"end":[0.1500,None,None,"—",0.0526]}

def load(path, sheet=None):
    wb = load_workbook(path, read_only=True)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    data = {}
    first = True
    last_t = None
    last_row = None
    ncols = None
    for row in ws.iter_rows(values_only=True):
        if first:
            hdr = row
            ncols = len([h for h in hdr if h is not None])
            first = False
            continue
        t = row[0]
        if t is None:
            continue
        t = float(t)
        data[round(t, 3)] = row
        last_t, last_row = t, row
    wb.close()
    return data, last_t, last_row, ncols

def r4(x):
    return None if x is None else round(float(x), 4)

def cmp(name, data, last_row, paper, mode, cols):
    ok = bad = na = 0
    bads = []
    for tk, pvs in paper.items():
        if tk == "end":
            row = last_row
        else:
            tsec = int(tk) if mode == "s" else int(round(float(tk) * 3600))
            row = data.get(float(tsec)) or data.get(round(float(tsec), 3))
        if row is None:
            bads.append((tk, None, "行缺失"))
            continue
        for j, pv in enumerate(pvs):
            if pv is None or pv == "—":
                na += 1
                continue
            xv = row[cols[j]] if cols[j] < len(row) else None
            if xv is None or xv == "":
                bads.append((tk, j, f"文件空(论文{pv})"))
                bad += 1
                continue
            if abs(r4(xv) - pv) > 1e-9:
                bads.append((tk, j, f"论文{pv} vs 文件{r4(xv)}"))
                bad += 1
            else:
                ok += 1
    print(f"[{name}] 一致 {ok} ｜ 不一致 {bad} ｜ 论文侧空/待回填 {na}")
    for b in bads[:20]:
        print("   ", b)

d1, lt1, lr1, n1 = load(RES / "result1.xlsx", "温度")
d1c, _, _, n1c = load(RES / "result1.xlsx", "水分浓度")
d2, _, lr2, n2 = load(RES / "result2.xlsx", "温度")
d2c, _, lr2c, n2c = load(RES / "result2.xlsx", "水分浓度")
d3, lt3, lr3, n3 = load(RES / "result3.xlsx")
d4, lt4, lr4, n4 = load(RES / "result4.xlsx")
print(f"列数: r1温度{n1}/r1浓度{n1c}/r2温度{n2}/r2浓度{n2c}/r3{n3}/r4{n4}")
print(f"末行时间: r3={lt3}s({lt3/3600:.4f}h)  r4={lt4}s({lt4/3600:.4f}h)")
c05 = [1, 6, 11, 16, 21]  # 0-based: 距离 0/0.5/1.0/1.5/2.0
c4 = [1, 6, 11, 17, 21]   # result4: 表面=第21列(0-based, 即第22列)
cmp("表1 温度", d1, None, T1, "s", c05)
cmp("表2 水分", d1c, None, T2, "s", c05)
cmp("表3 温度", d2, None, T3, "s", c05)
cmp("表4 水分", d2c, None, T4, "s", c05)
cmp("表5 水分", d3, lr3, T5, "h", c05)
cmp("表6 水分", d4, lr4, T6, "h", c4)
# 附加：result4 的 1.5cm 列（第4列,0-based 4? → 距离1.5=第16个0.1格 → 0-based 17? 0,0.1..: idx=1+15=16? 需核实表头）
wb = load_workbook(RES / "result4.xlsx", read_only=True)
ws = wb[wb.sheetnames[0]]
hdr4 = next(ws.iter_rows(values_only=True))
print("result4 表头:", hdr4)
print("result3 表头:", next(load(RES / "result3.xlsx")[0] and iter([]), None) if False else "")
wb.close()

# 附件2 规格核验
print()
print("== 附件2 规格核验 ==")
att2 = list((ROOT / "10_赛题" / "A题" / "附件").glob("附件2.xlsx"))
wb = load_workbook(att2[0], read_only=True)
ws = wb[wb.sheetnames[0]]
rows = list(ws.iter_rows(values_only=True))
print("表头:", rows[0], " 数据点数:", len(rows) - 1)
ts = [float(r[0]) for r in rows[1:] if r[0] is not None]
steps = sorted(set(round(ts[i+1]-ts[i], 3) for i in range(len(ts)-1)))
print("时间首末:", ts[0], "→", ts[-1], f"({ts[-1]/3600:.1f} h)", " 步长集合:", steps, " R首末:", rows[1][1], rows[-1][1])
