# -*- coding: utf-8 -*-
"""
A题 药材烘干 — 论文图表全部生成脚本
=====================================
用法：把本文件放在 03_结果与图表/最终图表/ 下
     等队长代码跑出 CSV 数据后，直接 python3 draw_all_figures.py
输出：全部 PDF 矢量图存入 ./output_pdf/
数据接口：见每张图前的 DATA_REQUIRED 注释

依赖：本脚本自动从 00_知识库/画图模板/ 加载中文字体和画图函数
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                 '..', '00_知识库', '画图模板'))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# 加载画图模板中的中文字体和画图函数
# ------------------------------------------------------------
# 直接执行模板的设置
import matplotlib.font_manager as fm

def set_chinese_font():
    candidates = ["PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
                  "SimHei", "Arial Unicode MS", "Noto Sans CJK SC",
                  "WenQuanYi Zen Hei", "Heiti SC"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name] + \
                [x for x in candidates if x != name]
            plt.rcParams["axes.unicode_minus"] = False
            print(f"使用中文字体: {name}")
            return
    print("警告：未找到中文字体！")

set_chinese_font()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output_pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.framealpha": 0.9,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def savefig(fname):
    """保存PDF矢量图到 output_pdf/ 目录"""
    path = os.path.join(OUTPUT_DIR, fname)
    plt.savefig(path)
    print(f"  [✓] 已保存: {path}")
    plt.close()


# ============================================================
# 图1  附件1：烘房温度与水分浓度随时间变化（EDA图）
# ============================================================
# DATA_REQUIRED: 附件1.xlsx 原始数据
#   列：时间(s) | 烘房温度(°C) | 烘房水分浓度(kg/kg)

def draw_fig1_air_conditions(data_dir="../data"):
    """
    输入：附件1原始数据
    输出：fig1_air_conditions.pdf —— 双Y轴图，烘房温湿度变化
    """
    import openpyxl
    wb = openpyxl.load_workbook(
        os.path.join(data_dir, "附件1.xlsx"), data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    t = np.array([r[0] for r in rows if r[0] is not None])
    T_air = np.array([r[1] for r in rows if r[1] is not None])
    C_air = np.array([r[2] for r in rows if r[2] is not None])

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(t / 3600, T_air, "r-", lw=1.5, label="烘房温度")
    ax1.set_xlabel("时间 (h)")
    ax1.set_ylabel("烘房温度 (°C)", color="r")
    ax1.tick_params(axis="y", labelcolor="r")

    ax2 = ax1.twinx()
    ax2.plot(t / 3600, C_air, "b--", lw=1.5, label="烘房水分浓度")
    ax2.set_ylabel("烘房水分浓度 (kg/kg)", color="b")
    ax2.tick_params(axis="y", labelcolor="b")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.set_title("图1  烘房温度与水分浓度随时间变化（附件1）")
    fig.tight_layout()
    savefig("fig1_air_conditions.pdf")


# ============================================================
# 图2  Q1 预热阶段 径向温度分布（各时刻剖面）
# ============================================================
# DATA_REQUIRED: Q1温度结果CSV
#   格式：首行 = 径向位置(cm): 0.0, 0.5, 1.0, 1.5, 2.0
#         每行 = 时间(s), T_0, T_0.5, T_1.0, T_1.5, T_2.0

def draw_fig2_q1_temp_profile(data_csv="q1_temperature.csv"):
    """
    输入：Q1完整温度结果CSV（1800行，每行1s）
    输出：fig2_q1_temp_profile.pdf
    """
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t = data[:, 0]
    times_label = [100, 300, 600, 900, 1200, 1500, 1800]
    r_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0])

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(times_label)))
    for i, tt in enumerate(times_label):
        idx = np.argmin(np.abs(t - tt))
        ax.plot(r_cm, data[idx, 1:], "o-", lw=1.5, color=colors[i],
                label=f"t = {tt} s", markersize=4)
    ax.set_xlabel("到药材中心的距离 (cm)")
    ax.set_ylabel("温度 (°C)")
    ax.set_title("图2  预热阶段药材径向温度分布（问题1）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig2_q1_temp_profile.pdf")


# ============================================================
# 图3  Q1 预热阶段 径向水分浓度分布
# ============================================================
# DATA_REQUIRED: Q1水分浓度结果CSV（格式同温度CSV）

def draw_fig3_q1_moisture_profile(data_csv="q1_moisture.csv"):
    """输出：fig3_q1_moisture_profile.pdf"""
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t = data[:, 0]
    times_label = [100, 300, 600, 900, 1200, 1500, 1800]
    r_cm = np.array([0.0, 0.5, 1.0, 1.5, 2.0])

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(times_label)))
    for i, tt in enumerate(times_label):
        idx = np.argmin(np.abs(t - tt))
        ax.plot(r_cm, data[idx, 1:], "o-", lw=1.5, color=colors[i],
                label=f"t = {tt} s", markersize=4)
    ax.set_xlabel("到药材中心的距离 (cm)")
    ax.set_ylabel("水分浓度 (kg/kg)")
    ax.set_title("图3  预热阶段药材径向水分浓度分布（问题1）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig3_q1_moisture_profile.pdf")


# ============================================================
# 图4  Q1 中心与表面温湿度演化（一条时间曲线）
# ============================================================
def draw_fig4_q1_center_surface(temp_csv="q1_temperature.csv",
                                  moist_csv="q1_moisture.csv"):
    """
    输出：fig4_q1_center_surface.pdf —— 双Y轴+双位置
    """
    T_data = np.loadtxt(temp_csv, delimiter=",", skiprows=1)
    C_data = np.loadtxt(moist_csv, delimiter=",", skiprows=1)
    t = T_data[:, 0] / 60  # 转分钟

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(t, T_data[:, 1], "r-", lw=1.5, label="中心温度")
    ax1.plot(t, T_data[:, -1], "r--", lw=1.5, label="表面温度")
    ax1.set_xlabel("时间 (min)")
    ax1.set_ylabel("温度 (°C)", color="r")
    ax1.tick_params(axis="y", labelcolor="r")

    ax2 = ax1.twinx()
    ax2.plot(t, C_data[:, 1], "b-", lw=1.5, label="中心水分浓度")
    ax2.plot(t, C_data[:, -1], "b--", lw=1.5, label="表面水分浓度")
    ax2.set_ylabel("水分浓度 (kg/kg)", color="b")
    ax2.tick_params(axis="y", labelcolor="b")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)
    ax1.set_title("图4  预热阶段中心与表面温湿度演化（问题1）")
    fig.tight_layout()
    savefig("fig4_q1_center_surface.pdf")


# ============================================================
# 图5  Q2 前3h 径向温度分布
# ============================================================
def draw_fig5_q2_temp_profile(data_csv="q2_temperature.csv"):
    """
    输出：fig5_q2_temp_profile.pdf
    时间点：0.5, 1.0, 1.5, 2.0, 2.5, 3.0 h
    """
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t = data[:, 0]  # 单位 s
    times_h = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    r_cm = np.linspace(0, 2, data.shape[1] - 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(times_h)))
    for i, th in enumerate(times_h):
        idx = np.argmin(np.abs(t - th * 3600))
        ax.plot(r_cm, data[idx, 1:], "o-", lw=1.5, color=colors[i],
                label=f"t = {th} h", markersize=4)
    ax.set_xlabel("到药材中心的距离 (cm)")
    ax.set_ylabel("温度 (°C)")
    ax.set_title("图5  烘干过程药材径向温度分布（问题2，前3 h）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig5_q2_temp_profile.pdf")


# ============================================================
# 图6  Q2 前3h 径向水分浓度分布
# ============================================================
def draw_fig6_q2_moisture_profile(data_csv="q2_moisture.csv"):
    """输出：fig6_q2_moisture_profile.pdf"""
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t = data[:, 0]
    times_h = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    r_cm = np.linspace(0, 2, data.shape[1] - 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(times_h)))
    for i, th in enumerate(times_h):
        idx = np.argmin(np.abs(t - th * 3600))
        ax.plot(r_cm, data[idx, 1:], "o-", lw=1.5, color=colors[i],
                label=f"t = {th} h", markersize=4)
    ax.set_xlabel("到药材中心的距离 (cm)")
    ax.set_ylabel("水分浓度 (kg/kg)")
    ax.set_title("图6  烘干过程药材径向水分浓度分布（问题2，前3 h）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig6_q2_moisture_profile.pdf")


# ============================================================
# 图7  Q3 中心含水率演化（全程，直到烘干结束）
# ============================================================
def draw_fig7_q3_drying_curve(data_csv="q3_moisture.csv",
                               target_C=0.15, dry_time_h=None):
    """
    输出：fig7_q3_drying_curve.pdf
    dry_time_h: 如果已知精确烘干时间，画竖线标注
    """
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t_h = data[:, 0] / 3600
    C_center = data[:, 1]   # r=0 中心点
    C_surface = data[:, -1] # 表面

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_h, C_center, "b-", lw=1.5, label="中心水分浓度")
    ax.plot(t_h, C_surface, "b--", lw=1.2, label="表面水分浓度")
    ax.axhline(y=target_C, color="r", ls="--", lw=1, alpha=0.7,
               label=f"烘干标准 C = {target_C} kg/kg")

    if dry_time_h is not None:
        ax.axvline(x=dry_time_h, color="g", ls=":", lw=1.5, alpha=0.8)
        ax.annotate(f"烘干终点\n{dry_time_h:.1f} h",
                    xy=(dry_time_h, target_C), fontsize=9, color="g")

    ax.set_xlabel("时间 (h)")
    ax.set_ylabel("水分浓度 (kg/kg)")
    ax.set_title("图7  药材烘干过程水分浓度变化（问题3）")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig7_q3_drying_curve.pdf")


# ============================================================
# 图8  Q3 每6h径向水分浓度分布
# ============================================================
def draw_fig8_q3_6h_profiles(data_csv="q3_moisture.csv",
                               dump_csv="q3_6h_summary.csv"):
    """
    输出：fig8_q3_6h_profiles.pdf
    优先用 q3_6h_summary.csv（每6h一行），没有则从全量数据采样
    """
    if os.path.exists(dump_csv):
        data = np.loadtxt(dump_csv, delimiter=",", skiprows=1)
        times_h = data[:, 0] / 3600
        profiles = data[:, 1:]
        r_cm = np.linspace(0, 2, profiles.shape[1])
    else:
        data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
        t = data[:, 0]
        times_h = np.arange(6, t[-1] / 3600 + 1, 6)
        r_cm = np.linspace(0, 2, data.shape[1] - 1)
        profiles = np.array([data[np.argmin(np.abs(t - th * 3600)), 1:]
                             for th in times_h])

    fig, ax = plt.subplots(figsize=(9, 5))
    n = len(times_h)
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, n))
    for i in range(min(n, 12)):  # 最多画12条
        ax.plot(r_cm, profiles[i], "o-", lw=1.2, color=colors[i],
                label=f"t = {times_h[i]:.0f} h", markersize=3)
    ax.set_xlabel("到药材中心的距离 (cm)")
    ax.set_ylabel("水分浓度 (kg/kg)")
    ax.set_title("图8  每隔6小时药材径向水分浓度分布（问题3）")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    savefig("fig8_q3_6h_profiles.pdf")


# ============================================================
# 图9  Q4 半径随时间收缩
# ============================================================
def draw_fig9_q4_radius(data_csv="q4_radius_history.csv"):
    """
    输出：fig9_q4_radius_shrinkage.pdf
    DATA_REQUIRED: 两列 CSV — 时间(s), 半径(cm)
    """
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t_h = data[:, 0] / 3600
    R_cm = data[:, 1]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t_h, R_cm, "k-", lw=2)
    ax.fill_between(t_h, 1.0, R_cm, alpha=0.08, color="gray")
    ax.set_xlabel("时间 (h)")
    ax.set_ylabel("药材半径 (cm)")
    ax.set_title("图9  药材半径随烘干时间收缩过程（问题4）")
    # 标注起点和终点
    ax.annotate(f"$R_0$ = {R_cm[0]:.2f} cm",
                xy=(t_h[0], R_cm[0]), fontsize=9,
                xytext=(t_h[0] + 3, R_cm[0] + 0.1),
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate(f"$R_f$ = {R_cm[-1]:.2f} cm",
                xy=(t_h[-1], R_cm[-1]), fontsize=9,
                xytext=(t_h[-1] - 20, R_cm[-1] + 0.2),
                arrowprops=dict(arrowstyle="->", lw=0.8))
    fig.tight_layout()
    savefig("fig9_q4_radius_shrinkage.pdf")


# ============================================================
# 图10  Q4 收缩坐标下水分浓度分布
# ============================================================
def draw_fig10_q4_shrink_profiles(data_csv="q4_moisture.csv"):
    """
    输出：fig10_q4_shrink_profiles.pdf
    DATA_REQUIRED: Q4结果CSV（归一化半径坐标x=r/R(t)）
    """
    data = np.loadtxt(data_csv, delimiter=",", skiprows=1)
    t = data[:, 0]
    # 取6h间隔
    times_h = np.arange(0, t[-1] / 3600 + 1, 6)
    x = np.linspace(0, 1, data.shape[1] - 1)

    fig, ax = plt.subplots(figsize=(8, 5))
    n = len(times_h)
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, n))
    for i, th in enumerate(times_h):
        idx = np.argmin(np.abs(t - th * 3600))
        ax.plot(x, data[idx, 1:], "-", lw=1.2, color=colors[i],
                label=f"t = {th:.0f} h" if th == 0 or th % 12 == 0 else "")
    ax.set_xlabel("归一化半径 x = r / R(t)")
    ax.set_ylabel("水分浓度 (kg/kg)")
    ax.set_title("图10  收缩药材内部水分浓度分布（问题4，归一化坐标）")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    savefig("fig10_q4_shrink_profiles.pdf")


# ============================================================
# 图11  Q3 vs Q4 烘干曲线对比
# ============================================================
def draw_fig11_comparison(csv_q3="q3_moisture.csv",
                            csv_q4="q4_moisture.csv",
                            dry_q3_h=None, dry_q4_h=None):
    """
    输出：fig11_q3_vs_q4_comparison.pdf
    对比考虑收缩与不考虑收缩的中心含水率演化
    """
    d3 = np.loadtxt(csv_q3, delimiter=",", skiprows=1)
    d4 = np.loadtxt(csv_q4, delimiter=",", skiprows=1)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(d3[:, 0] / 3600, d3[:, 1], "b-", lw=1.5,
            label="不考虑收缩（问题3）— 中心")
    ax.plot(d4[:, 0] / 3600, d4[:, 1], "r--", lw=1.5,
            label="考虑收缩（问题4）— 中心")
    ax.axhline(y=0.15, color="gray", ls=":", lw=1, alpha=0.7,
               label="烘干标准 C = 0.15")

    if dry_q3_h:
        ax.axvline(x=dry_q3_h, color="b", ls=":", lw=1, alpha=0.5)
    if dry_q4_h:
        ax.axvline(x=dry_q4_h, color="r", ls=":", lw=1, alpha=0.5)

    ax.set_xlabel("时间 (h)")
    ax.set_ylabel("中心水分浓度 (kg/kg)")
    ax.set_title("图11  考虑收缩与不考虑收缩的中心含水率对比")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig11_q3_vs_q4_comparison.pdf")


# ============================================================
# 图12  模型验证：与附件1实测温度对比
# ============================================================
def draw_fig12_validation(model_csv="q1_temperature.csv",
                            data_dir="../data"):
    """
    输出：fig12_validation.pdf
    将Q1模型计算的表面温度与附件1烘房温度对比
    并标注模型预测与实测的误差
    """
    import openpyxl
    model = np.loadtxt(model_csv, delimiter=",", skiprows=1)
    t_model = model[:, 0]
    T_surface_model = model[:, -1]

    wb = openpyxl.load_workbook(
        os.path.join(data_dir, "附件1.xlsx"), data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    t_air = np.array([r[0] for r in rows if r[0] is not None])
    T_air = np.array([r[1] for r in rows if r[1] is not None])

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(t_air / 3600, T_air, "k-", lw=1.5, label="烘房温度（附件1实测）")
    ax.plot(t_model / 3600, T_surface_model, "r--", lw=1.5,
            label="药材表面温度（模型计算）")

    # 计算模型vs烘房的差异
    idx_common = np.array([np.argmin(np.abs(t_model - ta)) for ta in t_air[:60]])
    rmse = np.sqrt(np.mean((T_surface_model[idx_common] - T_air[:60])**2))
    ax.text(0.02, 0.95, f"RMSE = {rmse:.2f} °C",
            transform=ax.transAxes, fontsize=10, va="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    ax.set_xlabel("时间 (h)")
    ax.set_ylabel("温度 (°C)")
    ax.set_title("图12  模型验证：药材表面温度与烘房实测温度对比")
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig12_validation.pdf")


# ============================================================
# 图13  灵敏度分析：关键参数±20%扰动
# ============================================================
def draw_fig13_sensitivity(sens_data_csv="sensitivity_results.csv"):
    """
    输出：fig13_sensitivity.pdf
    DATA_REQUIRED: 灵敏度分析结果CSV
      列：参数名, -20%, -10%, 基准, +10%, +20%
    如果没有CSV但有列表数据，直接传参
    """
    if not os.path.exists(sens_data_csv):
        print("  [!] 灵敏度分析数据未就绪，跳过图13")
        return

    data = np.loadtxt(sens_data_csv, delimiter=",", dtype=str)
    params = data[1:, 0]
    values = data[1:, 1:].astype(float)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.array([-20, -10, 0, 10, 20])
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    for i, (p, v) in enumerate(zip(params, values)):
        ax.plot(x, v, "o-", lw=1.5, color=colors[i % len(colors)], label=p,
                markersize=5)

    ax.set_xlabel("参数变化 (%)")
    ax.set_ylabel("烘干时间 (h)")
    ax.set_title("图13  关键参数灵敏度分析")
    ax.axvline(x=0, color="gray", ls="--", lw=0.8, alpha=0.5)
    ax.legend(fontsize=8)
    fig.tight_layout()
    savefig("fig13_sensitivity.pdf")


# ============================================================
# 图14  网格无关性验证
# ============================================================
def draw_fig14_grid_independence(grid_csv="grid_study.csv"):
    """
    输出：fig14_grid_independence.pdf
    DATA_REQUIRED: 网格研究CSV
      列：网格分辨率(cm), 表面温度(°C), 表面水分浓度(kg/kg)
    """
    if not os.path.exists(grid_csv):
        print("  [!] 网格无关性数据未就绪，跳过图14")
        return

    data = np.loadtxt(grid_csv, delimiter=",", skiprows=1)
    dr = data[:, 0]
    T_surf = data[:, 1]
    C_surf = data[:, 2]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    ax1.plot(dr, T_surf, "o-", lw=1.5, color="#d62728", markersize=6)
    ax1.set_xlabel("网格步长 Δr (cm)")
    ax1.set_ylabel("表面温度 (°C)")
    ax1.set_title("网格无关性 — 温度")
    ax1.invert_xaxis()

    ax2.plot(dr, C_surf, "s-", lw=1.5, color="#1f77b4", markersize=6)
    ax2.set_xlabel("网格步长 Δr (cm)")
    ax2.set_ylabel("表面水分浓度 (kg/kg)")
    ax2.set_title("网格无关性 — 水分浓度")
    ax2.invert_xaxis()

    fig.suptitle("图14  网格无关性验证")
    fig.tight_layout()
    savefig("fig14_grid_independence.pdf")


# ============================================================
# 图M1 技术路线/流程图
# ============================================================
def draw_figM1_flowchart():
    """
    输出：figM1_flowchart.pdf
    用 matplotlib 画简单的技术路线框图（文字+箭头）
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("图M1  本文技术路线", fontsize=13, fontweight="bold", pad=20)

    boxes = [
        (0.5, 2.5, "赛题分析\n传热传质机理"),
        (3.0, 3.5, "问题一\n定物性预热模型"),
        (3.0, 1.5, "问题二\n变物性烘干模型"),
        (5.5, 3.5, "问题三\n烘干时间确定"),
        (5.5, 1.5, "问题四\n收缩移动边界"),
        (8.0, 2.5, "结果验证\n误差/灵敏度"),
    ]
    for x, y, text in boxes:
        ax.text(x, y, text, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.4", facecolor="lightblue",
                          edgecolor="gray", alpha=0.8))

    arrows = [
        (1.5, 2.5, 2.5, 3.2), (1.5, 2.5, 2.5, 1.8),
        (4.0, 3.5, 5.0, 3.5), (4.0, 1.5, 5.0, 1.5),
        (5.5, 3.2, 5.5, 2.8), (6.5, 3.5, 7.5, 2.8), (6.5, 1.5, 7.5, 2.5),
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="gray"))

    fig.tight_layout()
    savefig("figM1_flowchart.pdf")


# ============================================================
# 主函数：按需调用
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("A题 药材烘干 — 论文图表批量生成")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 50)

    # ---- EDA / 附件数据 ----
    print("\n[1/14] 附件1烘房条件图...")
    draw_fig1_air_conditions()

    # ---- Q1 图表 ----
    print("\n[2-4/14] 问题1图表...")
    draw_fig2_q1_temp_profile()
    draw_fig3_q1_moisture_profile()
    draw_fig4_q1_center_surface()

    # ---- Q2 图表 ----
    print("\n[5-6/14] 问题2图表...")
    draw_fig5_q2_temp_profile()
    draw_fig6_q2_moisture_profile()

    # ---- Q3 图表 ----
    print("\n[7-8/14] 问题3图表...")
    draw_fig7_q3_drying_curve()
    draw_fig8_q3_6h_profiles()

    # ---- Q4 图表 ----
    print("\n[9-10/14] 问题4图表...")
    draw_fig9_q4_radius()
    draw_fig10_q4_shrink_profiles()

    # ---- 对比与验证 ----
    print("\n[11-12/14] 对比与验证...")
    draw_fig11_comparison()
    draw_fig12_validation()

    # ---- 灵敏度与网格无关性 ----
    print("\n[13-14/14] 检验图表...")
    draw_fig13_sensitivity()
    draw_fig14_grid_independence()

    # ---- 流程图 ----
    print("\n[+] 技术路线图...")
    draw_figM1_flowchart()

    print(f"\n{'=' * 50}")
    print(f"全部完成！PDF矢量图已保存至:")
    print(f"  {OUTPUT_DIR}")
    print(f"{'=' * 50}")