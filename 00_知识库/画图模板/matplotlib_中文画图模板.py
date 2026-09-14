# -*- coding: utf-8 -*-
"""
matplotlib 中文画图模板（竞赛通用，矢量图版）
============================================
用法：
    1. 直接复制本文件到赛题工作区 03_结果与图表/ 下
    2. 按需选择下面的函数，改数据即可
    3. 所有图默认保存为 PDF 矢量图（论文要求：高清矢量、非截图）
    4. 同时可选输出 PNG 位图（用于快速预览）

关键点（踩坑记录）：
    - macOS/Windows 默认字体不含中文字形，直接 plt.title("中文") 会显示方框
    - 必须先设置中文字体（见 set_chinese_font()）
    - PDF 矢量图中文字体需要 pdf.fonttype=42 (TrueType) 确保可嵌入
    - 论文配图字号 >= 10pt，坐标轴必须带单位
    - 所有图表默认输出 PDF 矢量图，满足"非截图、高清矢量"要求
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

# 全局样式（矢量图优化）
plt.rcParams.update({
    "figure.dpi": 150,            # 画布 DPI（仅影响位图预览）
    "savefig.dpi": 300,           # 保存位图时的 DPI（矢量图忽略此值）
    "savefig.bbox": "tight",      # 自动裁剪白边
    "savefig.pad_inches": 0.05,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.framealpha": 0.9,
    # 矢量图字体设置（关键！PDF 中文字体必须用 TrueType 嵌入）
    "pdf.fonttype": 42,           # TrueType 字体嵌入 PDF
    "ps.fonttype": 42,            # TrueType 字体嵌入 PS/EPS
    "svg.fonttype": "none",       # SVG 保持文本可编辑
})


def _savefig(fname, dpi=None):
    """统一保存：矢量 PDF 为主，同时可选输出 PNG 预览。"""
    base = fname.replace(".pdf", "").replace(".png", "")
    # 主输出：PDF 矢量图
    pdf_name = base + ".pdf"
    plt.savefig(pdf_name, dpi=dpi or plt.rcParams["savefig.dpi"])
    print(f"已保存矢量图: {pdf_name}")
    plt.close()


# ------------------------------------------------------------
# 2. 折线图（趋势/时序/曲线拟合）
# ------------------------------------------------------------
def line_plot(x, y, xlabel="x", ylabel="y", title="", label=None,
              fname="line.pdf", multi_lines=None):
    """
    multi_lines: [(x2,y2,label2), ...] 多条线时使用
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    if multi_lines:
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
        for i, (xi, yi, lbl) in enumerate(multi_lines):
            ax.plot(xi, yi, "-", lw=1.5, color=colors[i % len(colors)], label=lbl)
    else:
        ax.plot(x, y, "-", lw=1.5, color="#1f77b4", label=label)
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    ax.set_title(title)
    if label or multi_lines:
        ax.legend()
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 3. 散点图 + 拟合直线（回归可视化）
# ------------------------------------------------------------
def scatter_fit(x, y, xlabel="x", ylabel="y", title="", fname="scatter.pdf"):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, s=18, color="#ff7f0e", alpha=0.7, label="数据点")
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    r2 = 1 - np.sum((y - (k * x + b))**2) / np.sum((y - y.mean())**2)
    ax.plot(xs, k * xs + b, "r-", lw=1.5,
            label=f"拟合: y = {k:.3f}x {b:+.3f}\n$R^2$ = {r2:.4f}")
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 4. 柱状图（对比/排名）
# ------------------------------------------------------------
def bar_plot(labels, values, xlabel="", ylabel="", title="",
             fname="bar.pdf", value_label=True, color="#2ca02c",
             horizontal=False):
    figsize = (9, 5) if not horizontal else (5, max(4, len(labels) * 0.4))
    fig, ax = plt.subplots(figsize=figsize)
    if horizontal:
        bars = ax.barh(labels, values, color=color, edgecolor="black", lw=0.5)
        if value_label:
            for b, v in zip(bars, values):
                ax.text(v, b.get_y() + b.get_height() / 2,
                        f" {v:.2f}", ha="left", va="center", fontsize=9)
        ax.set_xlabel(f"{xlabel}")
    else:
        bars = ax.bar(labels, values, color=color, edgecolor="black", lw=0.5)
        if value_label:
            for b, v in zip(bars, values):
                ax.text(b.get_x() + b.get_width() / 2, v,
                        f"{v:.2f}", ha="center", va="bottom", fontsize=9)
        ax.set_ylabel(f"{ylabel}")
    ax.set_title(title)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 5. 分组柱状图（多组对比，竞赛高频！）
# ------------------------------------------------------------
def grouped_bar(labels, groups, group_names=None,
                xlabel="", ylabel="", title="", fname="grouped_bar.pdf"):
    """
    groups: [[v1,v2,...], [v1,v2,...], ...]  每组一列数据
    group_names: ["组1", "组2", ...]
    """
    n_groups = len(groups)
    n_items = len(labels)
    x = np.arange(n_items)
    width = 0.8 / n_groups
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    fig, ax = plt.subplots(figsize=(max(8, n_items * 0.8), 5))
    for i, vals in enumerate(groups):
        offset = (i - (n_groups - 1) / 2) * width
        lbl = group_names[i] if group_names else f"组{i+1}"
        ax.bar(x + offset, vals, width, label=lbl, color=colors[i % len(colors)],
               edgecolor="black", lw=0.3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(f"{ylabel}")
    ax.set_xlabel(f"{xlabel}")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 6. 双 y 轴（两个不同量纲的量）
# ------------------------------------------------------------
def twin_plot(x, y1, y2, labels=("左轴", "右轴"), xlabel="x",
              fname="twin.pdf", title=""):
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(x, y1, "b-", lw=1.5, label=labels[0])
    ax1.set_ylabel(labels[0])
    ax2 = ax1.twinx()
    ax2.plot(x, y2, "r--", lw=1.5, label=labels[1])
    ax2.set_ylabel(labels[1])
    ax1.set_xlabel(xlabel)
    if title:
        ax1.set_title(title)
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], loc="upper right")
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 7. 热力图（相关性矩阵）
# ------------------------------------------------------------
def heatmap(matrix, labels, title="", fname="heatmap.pdf",
            cmap="RdBu_r", vmin=-1, vmax=1):
    n = len(labels)
    fig, ax = plt.subplots(figsize=(max(7, n * 0.8), max(6, n * 0.7)))
    im = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(n)); ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks(range(n)); ax.set_yticklabels(labels)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center",
                    fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 8. 3D 曲面图（两个变量对目标的影响）
# ------------------------------------------------------------
def surface_plot(X, Y, Z, xlabel="x", ylabel="y", zlabel="z",
                 title="", fname="surface.pdf"):
    from mpl_toolkits.mplot3d import Axes3D  # noqa
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.9,
                           linewidth=0, antialiased=True)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_zlabel(zlabel)
    ax.set_title(title)
    fig.colorbar(surf, ax=ax, shrink=0.6)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 9. 子图拼接（多图一张）
# ------------------------------------------------------------
def subplot_grid(data_list, fname="subplot.pdf", cols=2):
    """
    data_list: [(x, y, title), ...] 或 [(x, y, title, "bar"/"scatter"), ...]
    自动排成子图网格。
    """
    n = len(data_list)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    axes = np.atleast_1d(axes).ravel()
    for i, item in enumerate(data_list):
        ax = axes[i]
        if len(item) >= 4 and item[3] == "scatter":
            ax.scatter(item[0], item[1], s=10, color="#ff7f0e")
        elif len(item) >= 4 and item[3] == "bar":
            ax.bar(item[0], item[1], color="#2ca02c")
        else:
            ax.plot(item[0], item[1], lw=1)
        ax.set_title(item[2], fontsize=10)
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 10. 饼图（占比展示，用到时才用）
# ------------------------------------------------------------
def pie_plot(labels, values, title="", fname="pie.pdf"):
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct="%1.1f%%",
        colors=plt.cm.Set3(np.linspace(0, 1, len(labels))),
        startangle=90, pctdistance=0.6)
    for t in autotexts:
        t.set_fontsize(9)
    ax.set_title(title)
    _savefig(fname)


# ------------------------------------------------------------
# 11. 箱线图（数据分布对比，统计分析常用）
# ------------------------------------------------------------
def box_plot(data_list, labels=None, ylabel="", title="", fname="box.pdf"):
    """
    data_list: [[data1], [data2], ...]  每组一列数据
    """
    fig, ax = plt.subplots(figsize=(max(6, len(data_list) * 1.2), 5))
    bp = ax.boxplot(data_list, patch_artist=True, labels=labels,
                    showmeans=True, meanprops=dict(marker="D", markerfacecolor="red"))
    colors = ["#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f", "#cab2d6"]
    for patch, color in zip(bp["boxes"], colors[:len(data_list)]):
        patch.set_facecolor(color)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 12. 雷达图（多指标综合评价展示）
# ------------------------------------------------------------
def radar_plot(values_list, categories, labels=None, title="", fname="radar.pdf"):
    """
    values_list: [[v1,v2,...], [v1,v2,...]]  多组数据
    categories: ["指标1", "指标2", ...]
    labels: ["方案A", "方案B", ...]
    """
    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # 闭合

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for i, vals in enumerate(values_list):
        vals_closed = vals.tolist() if hasattr(vals, 'tolist') else list(vals)
        vals_closed += vals_closed[:1]
        lbl = labels[i] if labels else f"方案{i+1}"
        ax.fill(angles, vals_closed, alpha=0.1, color=colors[i % len(colors)])
        ax.plot(angles, vals_closed, "o-", lw=1.5, color=colors[i % len(colors)],
                label=lbl, markersize=4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_title(title, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 13. 误差棒图（带置信区间的折线/柱状）
# ------------------------------------------------------------
def errorbar_plot(x, y, yerr, xlabel="x", ylabel="y", title="",
                  fname="errorbar.pdf", capsize=3):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.errorbar(x, y, yerr=yerr, fmt="o-", lw=1.5, capsize=capsize,
                color="#1f77b4", ecolor="#888888", elinewidth=1,
                markersize=5, markerfacecolor="#1f77b4")
    ax.set_xlabel(f"{xlabel}")
    ax.set_ylabel(f"{ylabel}")
    ax.set_title(title)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 14. 等高线图（灵敏度分析双参数联合分析最佳搭档）
# ------------------------------------------------------------
def contour_plot(X, Y, Z, xlabel="参数A", ylabel="参数B", title="",
                 fname="contour.pdf", filled=True):
    fig, ax = plt.subplots(figsize=(8, 6))
    if filled:
        cs = ax.contourf(X, Y, Z, levels=15, cmap="viridis", alpha=0.9)
        fig.colorbar(cs, ax=ax, shrink=0.8)
    cs2 = ax.contour(X, Y, Z, levels=8, colors="black", linewidths=0.5)
    ax.clabel(cs2, inline=True, fontsize=8, fmt="%.1f")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    _savefig(fname)


# ------------------------------------------------------------
# 15. 示例：跑一遍确认环境正常
# ------------------------------------------------------------
if __name__ == "__main__":
    x = np.linspace(0, 10, 200)
    # 折线图
    line_plot(x, np.sin(x), "角度 (rad)", "正弦值", "示例：折线图", fname="demo_line.pdf")
    # 散点+拟合
    np.random.seed(42)
    x2 = np.linspace(0, 5, 30)
    y2 = 2 * x2 + 1 + np.random.randn(30) * 0.5
    scatter_fit(x2, y2, "x", "y", "示例：散点图+拟合", fname="demo_scatter.pdf")
    # 柱状图
    bar_plot(["A", "B", "C", "D"], [3.2, 5.1, 2.8, 4.6],
             ylabel="得分", title="示例：柱状图", fname="demo_bar.pdf")
    print("画图模板测试完成，所有矢量图（PDF）已保存。")