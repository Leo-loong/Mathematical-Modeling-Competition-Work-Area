# -*- coding: utf-8 -*-
"""知识库内容覆盖度评估：对照国赛国奖能力要求，统计资料覆盖情况。"""
import os
import io
import re
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = [os.path.join(BASE, "第一批提取后"), os.path.join(BASE, "第二批提取后")]
REPORT = os.path.join(BASE, "temp", "资料充足性评估报告.txt")

SKIP_DIRS = ("_数据文件", "_无效内容", "_完整版")

# 评估维度：国赛国奖所需能力 -> 关键词
DIMS = {
    "赛题分析/问题拆解": ["问题重述", "问题分析", "题意", "隐含条件", "赛题分析", "问题分解", "子问题"],
    "数据预处理": ["数据预处理", "缺失值", "异常值", "归一化", "标准化", "插值", "数据清洗", "特征工程", "去噪"],
    "优化模型": ["线性规划", "整数规划", "非线性规划", "多目标规划", "动态规划", "目标函数", "约束条件", "最优解"],
    "预测模型": ["灰色预测", "时间序列", "ARIMA", "回归分析", "神经网络预测", "马尔可夫", "指数平滑", "LSTM"],
    "评价模型": ["层次分析法", "AHP", "模糊综合评价", "熵权法", "TOPSIS", "主成分分析", "因子分析", "灰色关联"],
    "分类与聚类": ["聚类", "K-means", "决策树", "支持向量机", "SVM", "随机森林", "贝叶斯", "判别分析"],
    "图论与网络": ["图论", "最短路径", "最小生成树", "网络流", "Dijkstra", "TSP", "遍历"],
    "微分方程/机理": ["微分方程", "偏微分", "常微分", "机理分析", "动力学", "有限元", "传热", "有限元分析"],
    "智能算法": ["遗传算法", "粒子群", "模拟退火", "蚁群", "禁忌搜索", "神经网络", "机器学习", "深度学习"],
    "统计分析检验": ["显著性检验", "假设检验", "方差分析", "相关分析", "残差", "拟合优度", "置信区间", "P值"],
    "模型检验/灵敏度": ["灵敏度分析", "误差分析", "稳健性", "鲁棒性", "检验", "误差", "收敛性", "稳定性"],
    "论文写作规范": ["摘要", "关键词", "问题重述", "模型假设", "符号说明", "参考文献", "论文结构", "写作"],
    "图表与排版": ["图表", "三线表", "流程图", "示意图", "Visio", "Origin", "Matlab绘图", "排版", "美化"],
    "代码资源": ["MATLAB", "Matlab", "Python", "Lingo", "SPSS", "代码", "程序", "源代码"],
    "优秀论文范例": ["优秀论文", "一等奖", "二等奖", "获奖论文", "国赛论文", "范文"],
}

TYPES = {"A题（机理/物理）": ["机理", "物理", "力学", "热传导", "微分方程", "A题"],
         "B题（综合/优化）": ["B题", "优化", "决策", "调度", "规划"],
         "C题（数据分析）": ["C题", "数据分析", "数据挖掘", "统计", "大数据"],
         "D题（运筹/网络）": ["D题", "运筹", "网络", "路径", "路径规划"],
         "E题（机理预测）": ["E题", "预测", "预报", "环境", "评价预测"]}


def iter_md():
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, _dn, fn in os.walk(root):
            if any(k in dp for k in SKIP_DIRS):
                continue
            for f in fn:
                if f.lower().endswith(".md"):
                    yield os.path.join(dp, f)


def main():
    files = list(iter_md())
    texts = {}
    for p in files:
        try:
            texts[p] = io.open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            texts[p] = ""
    all_text = "\n".join(texts.values())
    n_files = len(files)
    total_chars = sum(len(t) for t in texts.values())

    out = []
    out.append("# 资料充足性评估报告")
    out.append("")
    out.append("知识库 Markdown 文件: %d 个，总字符 %d（约 %.1f 万字）"
               % (n_files, total_chars, total_chars / 10000.0))
    out.append("")

    out.append("## 一、能力维度覆盖度")
    out.append("%-18s %8s %10s" % ("维度", "命中文件", "出现次数"))
    dim_files = {}
    for dim, kws in DIMS.items():
        cnt = 0
        hits = set()
        for p, t in texts.items():
            c = sum(t.count(k) for k in kws)
            if c:
                cnt += c
                hits.add(p)
        dim_files[dim] = (len(hits), cnt)
        out.append("%-18s %8d %10d" % (dim, len(hits), cnt))
    out.append("")

    out.append("## 二、赛题类型覆盖（按文件名/内容）")
    for t, kws in TYPES.items():
        c = sum(all_text.count(k) for k in kws)
        fn = sum(1 for p in texts if any(k in os.path.basename(p) for k in kws))
        out.append("  %-16s 内容命中 %8d 次, 文件名命中 %4d 个" % (t, c, fn))
    out.append("")

    out.append("## 三、资料形态统计")
    code_ext = defaultdict(int)
    for root in ROOTS:
        for dp, _dn, fn in os.walk(root):
            for f in fn:
                e = os.path.splitext(f)[1].lower()
                if e in (".m", ".py", ".c", ".mat", ".fig", ".r", ".jl"):
                    code_ext[e] += 1
    for e, c in sorted(code_ext.items(), key=lambda kv: -kv[1]):
        out.append("  代码/数据文件 %-6s %d" % (e, c))
    out.append("")

    out.append("## 四、最常被覆盖的主题词 TOP 30")
    common = ["遗传算法", "粒子群", "神经网络", "层次分析法", "灰色预测", "时间序列",
              "线性规划", "整数规划", "多目标", "模拟退火", "蚁群", "支持向量机",
              "决策树", "聚类", "主成分分析", "模糊综合评价", "熵权法", "TOPSIS",
              "微分方程", "图论", "蒙特卡洛", "回归分析", "马尔可夫", "小波分析",
              "BP神经", "LSTM", "背包问题", "排队论", "博弈论", "元胞自动机",
              "灵敏度分析", "误差分析", "残差检验", "假设检验"]
    cnts = Counter()
    for w in common:
        c = all_text.count(w)
        if c:
            cnts[w] = c
    for w, c in cnts.most_common(30):
        out.append("  %-14s %d" % (w, c))
    out.append("")

    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))
    print("ASSESSED files=%d chars=%d" % (n_files, total_chars))


if __name__ == "__main__":
    main()
