# -*- coding: utf-8 -*-
"""画图脚本共享配置 — 模拟演练同款 seaborn 精致样式"""
import logging, warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# 配色 — 与 F-01 TikZ 风格一致（学术色）
BLUE  = "#1F3A93"   # 深蓝（主色）
GOLD  = "#F39C12"   # 金色
GREEN = "#27AE60"   # 绿色
RED   = "#C0392B"   # 红色
GRAY  = "#9E9E9E"   # 灰色
INK   = "#333333"   # 墨色
GRID  = "#E0E0E0"

# 极浅填充色（对应 TikZ 的 cBlue!8 等）
BLUE_BG  = "#E8ECF4"  # cBlue!8
GOLD_BG  = "#FDF4E3"  # cGold!8
GREEN_BG = "#E8F5E9"  # cGreen!8
RED_BG   = "#FCE4EC"  # cRed!8
GRAY_BG  = "#F4F6F7"  # cBg

CM = 1 / 2.54

def despine(ax):
    pass  # seaborn 已去掉 top/right spine

def layout(fig):
    fig.tight_layout(pad=0.3)


# 流程图公共工具（F-01 TikZ 风格基准）
def add_box(ax, x, y, w, h, text, fc=BLUE_BG, ec=BLUE, fontsize=8, rounded=True):
    """绘制带填充色的矩形文本框，用于流程图节点
    - rounded=True: 圆角（F-01 风格）
    - fc: 填充色（默认用极浅色）
    """
    if rounded:
        rect = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
                                   boxstyle="round,pad=0.05",
                                   fc=fc, ec=ec, lw=1.0,
                                   zorder=2, clip_on=False)
    else:
        rect = mpatches.Rectangle((x-w/2, y-h/2), w, h, fc=fc, ec=ec, lw=1.0,
                             zorder=2, clip_on=False)
    ax.add_patch(rect)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, zorder=3)


def add_arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.0, ls="-"):
    """绘制箭头，用于流程图连线（默认灰色，F-01 风格）"""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, ls=ls))