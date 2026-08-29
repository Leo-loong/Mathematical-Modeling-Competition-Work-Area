# -*- coding: utf-8 -*-
"""
matplotlib 中文画图模板（竞赛通用）
====================================
用法：
    1. 直接复制本文件到赛题工作区 03_结果与图表/ 下
    2. 按需选择下面的函数，改数据即可
    3. 所有图统一保存为 PNG，dpi=300

关键点（踩坑记录）：
    - macOS/Windows 默认字体不含中文字形，直接 plt.title("中文") 会显示方框
    - 必须先设置中文字体（见 set_chinese_font()）
    - 保存图片时 font.sans-serif 必须已设置，否则 PDF/PNG 都乱码
    - 论文配图字号 >= 10pt，坐标轴必须带单位
"""

import matplotlib
matplotlib.use("Agg")          # 服务器/无界面环境必须
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# 1. 中文字体设置（每个脚本开头都要调用！）
# ------------------------------------------------------------
def set_chinese_font():
    """自动探测系统中文字体并设置。macOS/Windows/Linux 通用。"""
    import matplotlib.font_manager as fm
    candidates = ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
                  "SimHei", "Arial Unicode MS", "Noto Sans CJK SC",
                  "WenQuanYi Zen Hei", "Heiti SC"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name] + \
                [x for x in candidates if x != name]
            plt.rcParams["axes.unicode_minus"] = False   # 负号正常显示
            print(f"使用中文字体: {name}")
            return
    print("警告：未找到中文字体，中文将显示为方框！")

set_chinese_font()   # 立即调用

# 全局样式（可统一调整）
plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.framealpha": 0.9,
})

# ------------------------------------------------------------
# 2. 折线图（趋势/时序/曲线拟合）
# ------------------------------------------------------------
def line_plot(x, y, xlabel="x", ylabel="y", title="", label=None,
              fname="line.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, "-", lw=1.5, color="#1f77b4", label=label)
    ax.set_xlabel(f"{xlabel}（单位）")
    ax.set_ylabel(f"{ylabel}（单位）")
    ax.set_title(title)
    if label:
        ax.legend()
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)
    print(f"已保存: {fname}")

# ------------------------------------------------------------
# 3. 散点图 + 拟合直线（回归可视化）
# ------------------------------------------------------------
def scatter_fit(x, y, xlabel="x", ylabel="y", title="", fname="scatter.png"):
    x = np.asarray(x, dtype=float)   # 兼容 list 输入（polyfit/min 都要求 ndarray）
    y = np.asarray(y, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, s=18, color="#ff7f0e", alpha=0.7, label="数据点")
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, k * xs + b, "r-", lw=1.5, label=f"拟合: y = {k:.3f}x {b:+.3f}")
    ax.set_xlabel(f"{xlabel}（单位）")
    ax.set_ylabel(f"{ylabel}（单位）")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

# ------------------------------------------------------------
# 4. 柱状图（对比/排名）
# ------------------------------------------------------------
def bar_plot(labels, values, xlabel="", ylabel="", title="",
             fname="bar.png", value_label=True):
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values, color="#2ca02c", edgecolor="black", lw=0.5)
    if value_label:   # 柱顶标数值
        for b, v in zip(bars, values):
            ax.text(b.get_x() + b.get_width() / 2, v,
                    f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel(f"{ylabel}（单位）")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

# ------------------------------------------------------------
# 5. 双 y 轴（两个不同量纲的量）
# ------------------------------------------------------------
def twin_plot(x, y1, y2, labels=("左轴", "右轴"), xlabel="x",
              fname="twin.png"):
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(x, y1, "b-", lw=1.5, label=labels[0])
    ax1.set_ylabel(labels[0])
    ax2 = ax1.twinx()
    ax2.plot(x, y2, "r--", lw=1.5, label=labels[1])
    ax2.set_ylabel(labels[1])
    ax1.set_xlabel(xlabel)
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], loc="upper right")
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

# ------------------------------------------------------------
# 6. 热力图（相关性矩阵）
# ------------------------------------------------------------
def heatmap(matrix, labels, title="", fname="heatmap.png",
            cmap="RdBu_r", vmin=-1, vmax=1):
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
    for i in range(len(labels)):          # 格内标数值
        for j in range(len(labels)):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center",
                    fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

# ------------------------------------------------------------
# 7. 3D 曲面图（两个变量对目标的影响）
# ------------------------------------------------------------
def surface_plot(X, Y, Z, xlabel="x", ylabel="y", zlabel="z",
                 title="", fname="surface.png"):
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9,
                           linewidth=0, antialiased=True)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_zlabel(zlabel)
    ax.set_title(title)
    fig.colorbar(surf, ax=ax, shrink=0.6)
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

# ------------------------------------------------------------
# 8. 子图拼接（多图一张）
# ------------------------------------------------------------
def subplot_demo(data_list):
    """data_list: [(x, y, title), ...]，自动排成 2 列子图。"""
    n = len(data_list)
    cols = 2
    rows = (n + 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
    axes = np.atleast_1d(axes).ravel()
    for ax, (x, y, t) in zip(axes, data_list):
        ax.plot(x, y, lw=1)
        ax.set_title(t)
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig("subplot.png")
    plt.close(fig)

# ------------------------------------------------------------
# 9. 示例：跑一遍确认环境正常
# ------------------------------------------------------------
if __name__ == "__main__":
    x = np.linspace(0, 10, 200)
    line_plot(x, np.sin(x), "角度", "正弦值", "示例：折线图", "demo_line.png")
    print("画图模板测试完成，所有图已保存。")
