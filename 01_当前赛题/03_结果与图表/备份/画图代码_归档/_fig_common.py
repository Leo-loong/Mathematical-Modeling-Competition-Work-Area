# -*- coding: utf-8 -*-
"""画图脚本共享配置 — 模拟演练同款 seaborn 精致样式"""
import logging, warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# seaborn 全局样式 — 与模拟演练完全一致，必须最先设
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.0)

# 所有 rcParams 在 seaborn *之后* 覆盖，确保字体/字号不被重置
plt.rcParams.update({
    "font.sans-serif": ["Hiragino Sans GB", "Arial Unicode MS", "STHeiti"],
    "font.family": "sans-serif",
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "legend.fontsize": 7.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

warnings.filterwarnings("ignore", message=".*CFF.*FDArray.*")
warnings.filterwarnings("ignore", message=".*FontDict.*PaintType.*")

# 配色 — 与模拟演练一致
BLUE  = "#2166AC"
GOLD  = "#D6604D"
GREEN = "#4DAF4A"
RED   = "#B2182B"
GRAY  = "#9E9E9E"
INK   = "#333333"
GRID  = "#E0E0E0"

CM = 1 / 2.54

def despine(ax):
    pass  # seaborn 已去掉 top/right spine

def layout(fig):
    fig.tight_layout(pad=0.3)