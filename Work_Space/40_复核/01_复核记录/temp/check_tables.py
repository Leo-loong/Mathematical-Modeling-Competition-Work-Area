# -*- coding: utf-8 -*-
"""论文表1–6 ↔ result*.xlsx 逐格比对（只读，T0）
表数据硬编码自 50_论文/02_章节稿/A_08_模型建立与求解_基线.md（2026-09-13 读数）。
判据：论文表值（4位小数）与结果文件对应格 4 位舍入后一致。
"""
import sys, io
from pathlib import Path
from openpyxl import load_workbook
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(r"C:\Users\wang-\Desktop\2026数学建模\Work_Space")
RES = ROOT / "20_交付包" / "09_代码与复现" / "results"

# ---------- 论文表值（自 A_08 抄录） ----------
T1 = {  # 时间s: [0,0.5,1.0,1.5,2.0 cm] 温度
    100:[28.0001,28.0003,28.0041,28.0327,28.1800], 300:[28.0408,28.0635,28.1514,28.3680,28.8487],
    600:[28.4534,28.5360,28.8039,29.3159,30.1652], 900:[29.3243,29.4583,29.8754,30.6161,31.7304],
    1200:[30.5427,30.7098,31.2223,32.1125,33.4276], 1500:[31.9957,32.1867,32.7660,33.7463,35.1203],
    1800:[33.5753,33.7720,34.3642,35.3621,36.7855]}
T2 = {  # 水分浓度
    100:[2.5500,2.5500,2.5500,2.5500,2.2490], 300:[2.5500,2.5500,2.5500,2.5492,2.0517],
    600:[2.5500,2.5500,2.5500,2.5352,1.8774], 900:[2.5500,2.5500,2.5497,2.5045,1.7550],
    1200:[2.5500,2.5500,2.5482,2.4646,1.6588], 1500:[2.5500,2.5499,2.5445,2.4206,1.5789],
    1800:[2.5500,2.5497,2.5383,2.3755,1.5104]}
T3 = {  # h → [温度 0,0.5,1.0,1.5,2.0]
    0.5:[32.1893,32.3822,32.9660,33.9608,35.4131], 1.0:[40.3816,40.5536,41.0605,41.8783,42.9977],
    1.5:[45.8468,45.9348,46.1930,46.6051,47.1401], 2.0:[48.4502,48.4881,48.5984,48.7736,49.0033],
    2.5:[49.4670,49.4792,49.5136,49.5653,49.6609], 3.0:[49.8495,49.8553,49.8746,49.9101,49.9664]}
T4 = {  # 水分浓度
    0.5:[2.5499,2.5489,2.5255,2.3258,1.6486], 1.0:[2.5257,2.4947,2.3578,2.0230,1.4711],
    1.5:[2.3860,2.3256,2.1344,1.8020,1.3475], 2.0:[2.1708,2.1084,1.9236,1.6259,1.2311],
    2.5:[1.9567,1.9006,1.7360,1.4720,1.1166], 3.0:[1.7662,1.7165,1.5702,1.3333,1.0081]}
T5 = {  # h → [0,0.5,1.0,1.5,2.0]，None=待回填
    6:[1.0170,0.9881,0.9015,0.7550,0.5328], 12:[0.4562,0.4432,0.4031,0.3298,0.1642],
    18:[0.2989,0.2916,0.2687,0.2253,0.0845], 24:[0.2378,0.2328,0.2167,0.1856,0.0665],
    30:[0.2059,0.2019,0.1892,0.1641,0.0598], 36:[0.1859,0.1826,0.1718,0.1504,0.0566],
    42:[0.1721,0.1692,0.1597,0.1407,0.0548], 48:[0.1619,0.1592,0.1507,0.1335,0.0537],
    54:[0.1539,0.1515,0.1437,0.1278,0.0530], "end":[0.1500,None,None,None,0.0526]}
T6 = {  # h → [0,0.5,1.0,1.5,表面]，None=待回填
    0:[2.5500,2.5500,2.5500,2.5500,2.5500], 6:[1.6276,1.4621,0.9868,"—",0.4173],
    12:[0.7021,0.6248,0.3930,"—",0.1598], 18:[0.3958,0.3576,0.2340,"—",0.0869],
    24:[0.2794,0.2561,0.1763,"—",0.0665], 30:[0.2232,0.2066,0.1477,"—",0.0591],
    36:[0.1909,0.1779,0.1306,"—",0.0558], 42:[0.1699,0.1592,0.1193,"—",0.0540],
    48:[0.1552,0.1460,0.1110,"—",0.0529], "end":[0.1500,None,None,"—",0.0526]}

def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)

def check(name, book, sheet, paper, tkeys, time_mode, col_idx, extra_col=None):
    ws = book[sheet]
    hdr = [c.value for c in ws[1]]
    ok = bad = na = 0
    bads = []
    for tk in tkeys:
        # 结果文件行定位
        if time_mode == "s":
            tsec = int(tk)
            row = tsec  # A列自1 s起 ⟹ 第 tsec+1 行(含表头) ⟹ 数据行 = tsec+1 (1-based within data)
            excel_row = tsec + 2  # 行1=表头, 行2=t=1
            if tsec == 0:
                excel_row = None
        else:
            tsec = int(round(float(tk) * 3600))
            excel_row = None
        rowvals = None
        if time_mode == "s" and excel_row:
            rowvals = [ws.cell(excel_row, c).value for c in range(1, len(hdr) + 1)]
            at = rowvals[0]
            if at is None or abs(float(at) - tsec) > 0.5:
                rowvals = None
        if time_mode == "h":
            # 60 s 网格：数据行 = ceil;  或精确末行
            target = tsec
            best = None
            r = 2
            while True:
                v = ws.cell(r, 1).value
                if v is None:
                    break
                if abs(float(v) - target) < 1e-6:
                    best = r
                    break
                if float(v) > target:
                    break
                r += 1
            if best:
                rowvals = [ws.cell(best, c).value for c in range(1, len(hdr) + 1)]
        if tk == "end":
            # 末行
            r = ws.max_row
            rowvals = [ws.cell(r, c).value for c in range(1, len(hdr) + 1)]
        if rowvals is None:
            print(f"  [{name}] t={tk}: 结果文件未找到对应行 ⟹ 跳过")
            na += 1
            continue
        for j, pv in enumerate(paper.items() if False else enumerate(paper)):
            j, pv = j, pv
        for j, pv in enumerate(paper):
            if pv is None or pv == "—":
                na += 1
                continue
            xv = rowvals[col_idx[j]] if col_idx[j] < len(rowvals) else None
            if extra_col is not None and j == len(paper) - 1 and extra_col:
                xv = rowvals[extra_col]
            if xv is None or xv == "":
                bads.append((tk, j, pv, "文件为空"))
                bad += 1
                continue
            if abs(r4(xv) - pv) > 1e-9:
                bads.append((tk, j, pv, r4(xv)))
                bad += 1
            else:
                ok += 1
    print(f"[{name}] 一致 {ok} ｜ 不一致 {bad} ｜ 跳过/空 {na}")
    for b in bads[:15]:
        print(f"    t={b[0]} 列{j2c(b[1])} 论文={b[2]} 文件={b[3]}")
    if len(bads) > 15:
        print(f"    ... 共 {len(bads)} 处")

def j2c(j):
    return ["0cm","0.5cm","1.0cm","1.5cm","2.0cm","表面"][j] if j < 6 else str(j)

b1 = load_workbook(RES / "result1.xlsx", read_only=True)
b2 = load_workbook(RES / "result2.xlsx", read_only=True)
b3 = load_workbook(RES / "result3.xlsx", read_only=True)
b4 = load_workbook(RES / "result4.xlsx", read_only=True)

# result1: A列时间(s)自1起，行 = 时间+1（数据区），列 = 距离 0,0.1..2.0 ⟹ 0.5cm 间隔列 = 表列1..5 → 数据列 2,7,12,17,22
c05 = [2, 7, 12, 17, 22]
check("表1 温度 vs result1.xlsx[温度]", b1, "温度", T1, list(T1), "s", c05)
check("表2 水分 vs result1.xlsx[水分浓度]", b1, "水分浓度", T2, list(T2), "s", c05)
check("表3 温度 vs result2.xlsx[温度]", b2, "温度", T3, list(T3), "s", c05)
check("表4 水分 vs result2.xlsx[水分浓度]", b2, "水分浓度", T4, list(T4), "s", c05)
check("表5 水分 vs result3.xlsx", b3, b3.sheetnames[0], T5, list(T5), "h", [2, 7, 12, 17, 22])
# result4: 列 = 0,0.1..1.9 + 末列"药材表面"(第22列) ⟹ 论文列0,0.5,1.0,1.5 → 2,7,12,17；表面→22
check("表6 水分 vs result4.xlsx", b4, b4.sheetnames[0], T6, list(T6), "h", [2, 7, 12, 17, 22], extra_col=22)

# 附件2 规格核验
print()
print("== 附件2 规格核验 ==")
import glob
att2 = list((ROOT / "10_赛题" / "A题" / "附件").glob("附件2.xlsx"))
print("附件2 路径:", att2)
if att2:
    wb = load_workbook(att2[0], read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    print("表头:", rows[0])
    print("首行:", rows[1], " 末行:", rows[-1], " 数据点数:", len(rows) - 1)
    # 相邻时间步
    ts = [float(r[0]) for r in rows[1:]]
    steps = set(round(ts[i+1]-ts[i], 3) for i in range(len(ts)-1))
    print("时间步长集合:", steps, " 末值:", ts[-1], "=", ts[-1]/3600, "h")
