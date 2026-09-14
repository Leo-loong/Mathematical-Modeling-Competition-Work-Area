# -*- coding: utf-8 -*-
"""
A题 药材烘干 — 论文图表重制版 统一画图配置
============================================
字体：思源黑体 Source Han Sans SC（替代原 MATLAB 导出的 Helvetica 轮廓）
输出：矢量 PDF（中文可搜索文本，非轮廓）

依赖：matplotlib seaborn numpy pandas
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import os, warnings

# ---- 数据路径 ----
DATA_DIR = "/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output_pdf_remastered")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- 字体（必须在 seaborn 之后设置，否则被重置） ----
plt.rcParams.update({
    "font.sans-serif": ["Source Han Sans SC"],
    "font.family": "sans-serif",
    "mathtext.fontset": "stix",
    "axes.unicode_minus": False,
})

# ---- 全局样式 ----
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": None,
    "savefig.pad_inches": 0.05,
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "legend.fontsize": 7,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.4,
    "grid.linewidth": 0.6,
    "grid.color": "#D0D0D0",
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

warnings.filterwarnings("ignore", message=".*CFF.*FDArray.*")
warnings.filterwarnings("ignore", message=".*FontDict.*PaintType.*")

# ---- 配色（与归档 MATALB 脚本一致） ----
BLUE  = "#2166AC"
GOLD  = "#D6604D"
GREEN = "#4DAF4A"
RED   = "#B2182B"
GRAY  = "#9E9E9E"
INK   = "#333333"
GRID  = "#E0E0E0"

# 浅色填充（用于背景/标注）
BLUE_BG  = "#E8ECF4"
GOLD_BG  = "#FDF4E3"
GREEN_BG = "#E8F5E9"
RED_BG   = "#FCE4EC"

CM = 1 / 2.54  # cm → inch


def savefig(fig, fname):
    """保存矢量 PDF，关闭 figure；自动为非坐标轴边加浅色闭合线"""
    for ax in fig.axes:
        for spine_name in ("top", "right"):
            spine = ax.spines[spine_name]
            if not spine.get_visible():
                spine.set_visible(True)
                spine.set_color("#D0D0D0")
                spine.set_linewidth(0.6)
    path = os.path.join(OUTPUT_DIR, fname)
    fig.savefig(path, dpi=300, pad_inches=0.05)
    print(f"  [OK] {fname}")
    plt.close(fig)


def read_csv(name, **kwargs):
    """读取数据 CSV，自动处理 comment 行"""
    fpath = os.path.join(DATA_DIR, name)
    if "comment" not in kwargs:
        kwargs["comment"] = "#"
    return pd.read_csv(fpath, **kwargs)


def read_matrix(name):
    """读取数值矩阵 CSV（首列为索引），返回 t, Z"""
    data = np.loadtxt(os.path.join(DATA_DIR, name), delimiter=",", skiprows=1)
    return data[:, 0], data[:, 1:]