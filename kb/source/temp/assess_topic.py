# -*- coding: utf-8 -*-
"""针对 2025 B 题（碳化硅外延层厚度 / 红外干涉）的专项资料检索。"""
import os
import io
import re
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOTS = [os.path.join(BASE, "第一批提取后"), os.path.join(BASE, "第二批提取后")]
REPORT = os.path.join(BASE, "temp", "B题专项资料评估.txt")
SKIP = ("_数据文件", "_无效内容", "_完整版")

GROUPS = {
    "光学干涉机理": ["干涉", "干涉条纹", "光程差", "相位差", "薄膜干涉", "多光束", "Fabry", "法布里",
                 "等厚干涉", "等倾干涉", "驻波"],
    "折射率模型": ["折射率", "折射", "色散", "Sellmeier", "Cauchy", "柯西", "Drude", "载流子浓度",
                "介电常数", "消光系数"],
    "光谱信号处理": ["傅里叶", "FFT", "频谱", "小波", "滤波", "峰值检测", "插值", "包络",
                 "光谱", "波数", "反射率", "吸光度"],
    "参数反演/拟合": ["反演", "参数估计", "最小二乘", "拟合", "寻优", "迭代", "牛顿法", "梯度下降",
                  "反问题", "正则化"],
    "半导体/材料背景": ["碳化硅", "外延", "晶圆", "半导体", "硅片", "掺杂", "衬底", "红外"],
    "误差与可靠性": ["误差分析", "可靠性", "不确定度", "灵敏度", "稳健性", "残差", "置信", "精度"],
    "优化/智能算法": ["遗传算法", "粒子群", "模拟退火", "神经网络", "机器学习"],
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
    out = ["# 2025 B 题（碳化硅外延层厚度）专项资料评估", ""]
    out.append("检索范围: %d 个 Markdown（两批次提取后主目录）" % len(files))
    out.append("")
    for g, kws in GROUPS.items():
        hit_files = {}
        total = 0
        for p, t in texts.items():
            c = sum(t.count(k) for k in kws)
            if c:
                hit_files[p] = c
                total += c
        out.append("## %s" % g)
        out.append("  命中文件 %d 个，累计 %d 次" % (len(hit_files), total))
        if hit_files:
            top = sorted(hit_files.items(), key=lambda kv: -kv[1])[:6]
            for p, c in top:
                out.append("    %5d  %s" % (c, os.path.basename(p)[:70]))
        else:
            out.append("    （未命中）")
        out.append("")
    with io.open(REPORT, "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))
    print("TOPIC ASSESSED")


if __name__ == "__main__":
    main()
