# -*- coding: utf-8 -*-
"""PR-01…PR-38 修复状态针对性核验（只读，轻量）
每个 PR 用固定串/结构检查判定：✅已解决 / ❌仍在 / △需人工看 / ➖不适用
"""
import re, sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = Path(r"C:\Users\wang-\Desktop\2026数学建模\Work_Space\50_论文\02_章节稿")
def rd(n): return (D / n).read_text(encoding="utf-8")
st = {}
def mark(k, v, note=""):
    st[k] = (v, note)
    print(f"{v}  {k:8s} {note}")

a02, a04, a05, a06 = rd("A_02_摘要_基线.md"), rd("A_04_问题重述_基线.md"), rd("A_05_问题分析_基线.md"), rd("A_06_模型假设_基线.md")
a07, a08, a09, a10 = rd("A_07_符号说明_基线.md"), rd("A_08_模型建立与求解_基线.md"), rd("A_09_结果分析_基线.md"), rd("A_10_模型检验_基线.md")
a11, a13, a14 = rd("A_11_模型评价与改进_基线.md"), rd("A_13_参考文献_基线.md"), rd("A_14_附录_基线.md")

# PR-01 假设8 虚假声明
mark("PR-01", "✅已解决" if "已对照非均匀收缩律" not in a06 and "已对照非均匀收缩" not in a06 else "❌仍在", "A_06 假设8 表述")
# PR-02 互验温差
mark("PR-02", "✅已解决" if "7.8\\times10^{-5}" not in a10 and "1.004" in a10 else "❌仍在", "A_10 6.3 温差值")
# PR-03 k_m 影响很小
bad = ("对流传质系数影响很小" in a10)
good = ("k_m" in a10 and ("主控" in a10 or "较敏感" in a10 or "问题 2" in a10))
mark("PR-03", "✅已解决" if not bad and good else ("❌仍在" if bad else "△需人工看"), "A_10 6.6 表述")
# PR-04 判据不敏感
mark("PR-04", "✅已解决" if "对判据阈值不敏感" not in a10 else "❌仍在", "A_10 6.10 结论")
# PR-05 ±25%
mark("PR-05", "✅已解决" if "\\pm25" not in a10 else "❌仍在", "A_10 6.10 扰动幅度")
# PR-06 摘要 10^-4
mark("PR-06", "✅已解决" if ("10^{-4} 量级" not in a02 and "10⁻⁴ 量级" not in a02) else "❌仍在", "A_02 守恒量级表述")
# PR-07 没有跳变
mark("PR-07", "✅已解决" if "没有跳变" not in a09 else "❌仍在", "A_09 其三")
# PR-08 GCI 0.0064
n8 = a08.count("0.0064") + a10.count("0.0064")
mark("PR-08", "✅已解决" if n8 == 0 else "❌仍在", f"两稿 0.0064 残留 {n8} 处")
# PR-09 观测阶 1.98–2.09
bad9 = ("1.98–2.09" in a10) or ("1.98–2.09" in a08)
mark("PR-09", "✅已解决" if not bad9 else "❌仍在", "观测阶区间表述")
# PR-10 图5-8/5-19 引用
body08 = a08.split("## 六、本章图与表")[0]
r58 = bool(re.search(r"图\s*5-8", body08)); r519 = bool(re.search(r"图\s*5-19", body08))
mark("PR-10", "✅已解决" if r58 and r519 else ("△部分" if (r58 or r519) else "❌仍在"), f"图5-8引={r58} 图5-19引={r519}")
# PR-11 表6 列数
cols = re.search(r"\| 时间/h \| 0 \| 0\.5 \| 1\.0 \|.*?\|\n\|---", a08)
line = a08[a08.find("**表 6"):a08.find("**表 6")+400] if "**表 6" in a08 else ""
four = "| 时间/h | 0 | 0.5 | 1.0 | 药材表面 |" in a08
five = "| 时间/h | 0 | 0.5 | 1.0 | 1.5 | 药材表面 |" in a08
mark("PR-11", "△已按四列" if four and not five else ("△仍为五列" if five else "△需人工看"), "表6 列结构（属用户裁决项）")
# PR-12 图号体系
mark("PR-12", "△用图A-x" if "图A-1" in a10 else "△需人工看", f"A_10 占位图号形态（属裁决项）；A_08 图5-x={'图 5-1' in a08 or '图5-1' in a08}")
# PR-13 文献 18 条与字段
n_ref = len(re.findall(r"^\[\d+\]", a13, re.M))
mark("PR-13", "△维持18条" if n_ref == 18 else f"△现为{n_ref}条", "条数属裁决项；[3][8][18] 字段见 A_13 §二")
# PR-14 观测阶/err 配对
mark("PR-14", "△需人工看", "A_08 5.4.4 观测阶与误差带配对（grep 见下）")
m14 = re.search(r"空间网格收敛指数[^。\n]*", a08)
print("      当前句：", m14.group(0)[:80] if m14 else "（未找到）")
# PR-16 引用位置对照（[2]/[8] 位置）
c2 = "5.2.1" in a13 and "2.2" in a13
mark("PR-16", "△需人工看", "A_13 §一 对照位置是否已同步")
# PR-17 问题一/问题 1
h1 = len(re.findall(r"问题一", a02)); h5 = len(re.findall(r"问题一", a05)); h8 = len(re.findall(r"问题一", a08))
mark("PR-17", "✅已解决" if h1 + h5 + h8 == 0 else "△残留", f"问题一：A_02×{h1} A_05×{h5} A_08×{h8}")
# PR-18 符号表单位
t_row = re.search(r"\|\s*\$T\(r,t\)\$\s*\|[^|]*\|\s*([^|]+)\|", a07)
mark("PR-18", ("△单位=" + t_row.group(1).strip()) if t_row else "△需人工看", "A_07 T 行单位（℃ 为解决）")
# PR-19 ε/q
used_eps = "ε" in a08 or "\\varepsilon" in a08 or "\\varepsilon" in a10
mark("PR-19", "△ε正文出现" if used_eps else "△ε仍在表中？", f"A_07 列 ε={('ε' in a07 or 'varepsilon' in a07)}；正文用={used_eps}")
# PR-20 附录
mark("PR-20", "△需人工看", f"附录B标题={'关键源程序' in a14}；'全部完整'声明={'全部完整' in a14 or '完整收录' in a14}")
# PR-23 夹逼
mark("PR-23", "✅已解决" if ("8.36" in a08 or "129.48" in a08 or "夹逼" in a08 or "夹逼" in a09) else "❌仍未落位", "Q4-N12 两界夹逼")
# PR-24 输入不确定度/末位支配
mark("PR-24", "✅已解决" if ("输入噪声" in a10 and "末位" in a10) else ("△部分" if "输入噪声" in a10 else "❌仍未"), "A_10 末位支配结论")
# PR-25 T1-3 界面口径对照
mark("PR-25", "✅已落位" if ("不可辨识" in a08 or "不可辨识" in a10 or "8.5" in a10) else "❌仍未", "Q1 界面口径对照")
# PR-28 Q1 守恒
mark("PR-28", "✅已解决" if ("1.16" in a10 and "0.06" in a10) else "❌仍未", "6.5 Q1 守恒值")
# PR-29 表5/6 结束行回填
end5 = re.search(r"\|\s*\*\*烘干结束\*\*[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", a08)
row5 = end5.group(0) if end5 else ""
filled = row5.count("—") == 0 and "0.1477" in row5
mark("PR-29", "✅已回填" if filled else "△仍未回填", f"表5 结束行：{row5[:60]}")
# PR-31 9.6 定位句
mark("PR-31", "✅已解决" if ("多模型融合" in a11 or "单一机理模型" in a11) else "❌仍未", "A_11 定位句")
# PR-33 关键词领域词
mark("PR-33", "✅已加" if ("烘干" in a11 and "药材干燥" in rd("A_03_关键词_基线.md")) else "△未加（可选）", "A_03 领域词")
# PR-35 复杂度
mark("PR-35", "✅已补" if ("487" in a08 or "墙钟" in a08 or "计算成本" in a08) else "❌未补", "A_08 计算成本")
print()
# 汇总 JSON 供后续使用
Path(__file__).with_name("pr_check_summary.json").write_text(json.dumps({k: v[0] for k, v in st.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
print("汇总：", {k: v[0] for k, v in st.items()})
