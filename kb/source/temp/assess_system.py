# -*- coding: utf-8 -*-
"""从「体系 / 流程 / 规则 / 套路」维度评估知识库，用于约束 Agent 建模行为。"""
import os
import io

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = [os.path.join(BASE, "第一批提取后"), os.path.join(BASE, "第二批提取后")]
REPORT = os.path.join(BASE, "temp", "体系流程覆盖评估.txt")
SKIP = ("_数据文件", "_无效内容", "_完整版")

DIMS = {
    "建模标准流程": ["七步解题法", "建模流程", "标准体系", "解题步骤", "建模步骤", "标准七步",
                "时间分配", "三天", "工作流程", "解题法"],
    "题型判断与选题": ["题型判断", "选题", "赛题类型", "题目类型", "A题", "B题", "C题", "命题规律"],
    "方法选型规则": ["模型选择", "算法选择", "方法选择", "选型", "适用", "模型推荐", "算法推荐",
                 "什么情况用", "对比"],
    "评分标准/评委视角": ["评分标准", "评审", "评分点", "评委", "打分", "评分", "国奖标准",
                    "获奖", "一等奖", "二等奖"],
    "避坑与误区": ["避坑", "误区", "常见错误", "错误", "不要", "禁止", "注意", "易错", "扣分点"],
    "论文结构模板": ["模板", "论文结构", "标准结构", "问题重述", "模型假设", "符号说明",
                 "参考文献", "章节", "框架"],
    "摘要与关键词": ["摘要", "关键词", "首页", "题目"],
    "模型假设规范": ["假设", "模型假设", "简化", "前提条件"],
    "灵敏度与检验套路": ["灵敏度分析", "误差分析", "稳健性", "鲁棒性", "检验", "假设检验",
                   "残差", "收敛性"],
    "图表与排版规范": ["三线表", "图表规范", "排版", "字体", "流程图", "示意图", "绘图", "单位"],
    "AI 使用合规": ["AI声明", "AI 使用", "AI生成", "AI红线", "自查表", "合规", "检测", "痕迹"],
    "创新点设计": ["创新点", "创新", "亮点", "改进", "特色", "优势"],
    "结果分析套路": ["结果分析", "结果", "对比分析", "讨论", "可视化", "结论"],
}


def iter_md():
    for root in ROOTS:
        for dp, _dn, fn in os.walk(root):
            if any(k in dp for k in SKIP):
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

    out = ["# 体系 / 流程 / 规则 维度覆盖评估", ""]
    out.append("检索 %d 个 Markdown" % len(files))
    out.append("")
    out.append("%-18s %8s %10s  %s" % ("维度", "命中文件", "出现次数", "代表文件"))
    for dim, kws in DIMS.items():
        hits = {}
        total = 0
        for p, t in texts.items():
            c = sum(t.count(k) for k in kws)
            if c:
                hits[p] = c
                total += c
        best = ""
        if hits:
            bp = max(hits.items(), key=lambda kv: kv[1])[0]
            best = os.path.basename(bp)[:44]
        out.append("%-18s %8d %10d  %s" % (dim, len(hits), total, best))
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))
    print("SYSTEM ASSESSED")


if __name__ == "__main__":
    main()
