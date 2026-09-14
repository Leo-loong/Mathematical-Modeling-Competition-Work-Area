# -*- coding: utf-8 -*-
"""
总览示意类图表（4张：F-01/F-02/F-04/F-05）
数据源：F-04 使用 fig_q4_shrinkage.csv，其余为示意类
输出：01_当前赛题/03_结果与图表/最终图表/
"""
from _fig_common import *  # 共享配置：配色/字体/尺寸/layout()
import os, sys, csv
import numpy as np

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "Work_Space","20_交付包","04_图表包","data"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
def load_csv(name):
    return np.genfromtxt(os.path.join(DATA_DIR,name),delimiter=",",
                         names=True,dtype=float,encoding="utf-8")
def save(fig,stem):
    for ext in ("pdf","png"):
        fig.savefig(os.path.join(OUT_DIR,f"{stem}.{ext}"))
    plt.close(fig)
    print(f"  [OK] {stem}")
def despine(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ====== F-01 总体建模流程图 ======


def draw_f01():
    fig, ax = plt.subplots(figsize=(16*CM, 10*CM))
    ax.set_xlim(0,16); ax.set_ylim(0,12); ax.axis("off")

    # 步骤节点
    steps = [
        (1.5, 10.5, "赛题分析\n(附件1/2、附录2/3/4)", "#FFF3E0", GOLD),
        (4.5, 10.5, "模型建立\n(PDE + 边界条件)", "#E3F2FD", BLUE),
        (7.5, 10.5, "数值求解\n(FVM + 隐式 + Picard)", "#E8F5E9", GREEN),
        (10.5,10.5, "结果验证\n(对照附件、收敛性)", "#F3E5F5", "#6A1B9A"),
        (13.5,10.5, "论文呈现\n(结果+检验+评价)", "#FCE4EC", RED),
    ]
    for x, y, txt, fc, ec in steps:
        add_box(ax, x, y, 2.6, 1.2, txt, fc, ec, 7)
    for i in range(len(steps)-1):
        add_arrow(ax, steps[i][0]+1.3, steps[i][1], steps[i+1][0]-1.3, steps[i+1][1])

    # Q1-Q4 展开
    add_box(ax, 7.5, 7.0, 12, 1.2,
            "同一 PDE 框架，逐问加码：Q1 定物性 → Q2 变物性 → Q3 长时程+终止判据 → Q4 移动边界(收缩)",
            "#FFFFFF", GRAY, 7.5)

    # 核心方程 — 左右各一个盒，双向箭头
    add_box(ax,  3.2, 5.5, 5.0, 2.0,
        "热传导方程\n$\\rho c_p\\frac{\\partial T}{\\partial t}"
        "=\\frac{1}{r}\\frac{\\partial}{\\partial r}(kr\\frac{\\partial T}{\\partial r})$",
        "#E3F2FD", BLUE, 7)
    add_box(ax, 10.2, 5.5, 5.0, 2.0,
        "Fick 扩散方程\n$\\frac{\\partial C}{\\partial t}"
        "=\\frac{1}{r}\\frac{\\partial}{\\partial r}(Dr\\frac{\\partial C}{\\partial r})$",
        "#E8F5E9", GREEN, 7)

    # 双向耦合（热传导右边缘=5.7, Fick左边缘=7.7, 间距=2.0 从容）
    mid_x, mid_y = 6.7, 5.5
    add_arrow(ax, mid_x-0.45, mid_y, mid_x+0.45, mid_y, RED, 2.0)
    add_arrow(ax, mid_x+0.45, mid_y+0.35, mid_x-0.45, mid_y+0.35, RED, 2.0)
    ax.text(mid_x, mid_y+0.8, "双向耦合", ha="center", va="center",
            fontsize=7.5, color=RED, fontweight="bold")

    # 边界条件 — 精简，放在两个方程盒下方居中
    add_box(ax, 6.7, 3.8, 11.0, 0.9,
        "边界条件：$r{=}0$: 对称 $\\partial_r{=}0$（中心） | "
        "$r{=}R$: $-k\\partial_r T{=}h(T_R{-}T_\\infty)$，$-D\\partial_r C{=}k_m(C_R{-}C_\\infty)$（第三类 Robin）",
        "#FFF3E0", GOLD, 6.5)

    # 数值方法行
    add_box(ax, 8, 2.5, 14, 1.0,
            "数值方法：守恒型有限体积法 ｜ 全隐式时间推进 ｜ Picard 非线性迭代($\\omega$=0.7, tol=$10^{-10}$) ｜ Q4: 物质坐标 $\\xi=r/R(t)$",
            "#F5F5F5", GRAY, 7)

    fig.suptitle("总体建模流程图：热–湿耦合 PDE 求解体系", fontsize=11, y=1.04)
    layout(fig); save(fig, "图_F01_总体建模流程图")

# ====== F-02 四问递进关系图 ======
def draw_f02():
    fig, ax = plt.subplots(figsize=(16*CM, 10*CM))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis("off")

    # 四个问题框 - 简化内容，增大间距
    q_data = [
        (2.0, 6.5, "Q1 预热阶段", "0–1800 s\n附录2 定物性\n固定半径 2 cm"),
        (6.0, 6.5, "Q2 变物性", "0–3 h\n附录3 变物性\n$\\rho(C),c_p(C),k(C),D(C,T)$"),
        (10.0, 6.5, "Q3 长时程", "至达标\n$\\max_r C(r,t)<0.15$\n烘干时间确定"),
        (14.0, 6.5, "Q4 移动边界", "考虑收缩\n$R=R(t)$\n物料坐标变换"),
    ]

    # 主框
    for x, y, title, detail in q_data:
        add_box(ax, x, y, 3.2, 2.0, f"{title}\n\n{detail}", BLUE_BG, BLUE, 7)

    # 递进箭头
    for i in range(3):
        x1 = q_data[i][0] + 1.6
        x2 = q_data[i+1][0] - 1.6
        add_arrow(ax, x1, 6.5, x2, 6.5, RED, 1.8)

    # 底部说明框
    add_box(ax, 8, 3.5, 15.0, 1.0,
            "统一框架：轴对称圆柱 1D 径向模型 (L/R=12.5) ｜ 热传导 + Fick 扩散 PDE 耦合 ｜ 全隐式 FVM + Picard 迭代",
            GOLD_BG, GOLD, 7.5)

    # 连接箭头
    for x, y, title, detail in q_data:
        add_arrow(ax, x, 5.5, x, 4.0, GRAY, 0.8)

    fig.suptitle("四问递进关系：同一模型的三次加码", fontsize=11, y=1.02)
    layout(fig); save(fig, "图_F02_四问递进关系图")

# ====== F-04 药材半径收缩曲线 ======
def draw_f04():
    d = load_csv("fig_q4_shrinkage.csv")
    fig, ax = plt.subplots(figsize=(9*CM, 5*CM))
    ax.plot(d["t_h"], d["R_cm"], color=BLUE, lw=1.8)
    ax.set_xlabel("时间 $t$ / h"); ax.set_ylabel("药材半径 $R$ / cm")
    ax.set_title("药材半径随干燥时间收缩（附件2）")
    # 标注
    ax.annotate(f"初始 $R_0$={d['R_cm'][0]:.2f} cm",
                xy=(0, d["R_cm"][0]), xytext=(1, d["R_cm"][0]-0.05),
                fontsize=7, color=INK,
                arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.8))
    ax.annotate(f"最终 $R$={d['R_cm'][-1]:.4f} cm\n收缩比 {d['R_cm'][-1]/d['R_cm'][0]:.3f}",
                xy=(d["t_h"][-1], d["R_cm"][-1]),
                xytext=(d["t_h"][-1]*0.7, d["R_cm"][-1]+0.08),
                fontsize=7, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))
    despine(ax)
    layout(fig); save(fig, "图_F04_药材半径收缩曲线")

# ====== F-05 Q4 物质坐标变换示意 ======
def draw_f05():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16*CM, 8*CM))

    # (a) 物理域 - 同心圆
    theta = np.linspace(0, 2*np.pi, 200)
    r_vals = [2.0, 1.6, 1.2]
    colors_p = [BLUE, GOLD, RED]
    for r_val, c in zip(r_vals, colors_p):
        ax1.add_patch(plt.Circle((0,0), r_val/2.5, fill=False, ec=c, lw=1.5,
                                  ls=["-","--","-"][r_vals.index(r_val)]))
    ax1.set_xlim(-1, 1); ax1.set_ylim(-1, 1); ax1.set_aspect("equal")
    ax1.text(0, 0, "$r=0$", ha="center", fontsize=8)
    ax1.annotate("$r=R(t)$\n随 $t$ 递减", xy=(0.8, 0), xytext=(0.6, 0.5),
                fontsize=8, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax1.set_title("(a) 物理域 $r$: 边界移动", fontsize=9, pad=10)
    ax1.axis("off")

    # (b) 计算域 - 水平线
    for i, (r_v, c) in enumerate(zip(r_vals, colors_p)):
        y0 = 2 - i*0.8
        ax2.plot([0, 1], [y0, y0], color=c, lw=1.5, ls=["-","--","-"][i],
                label=f"$R$={r_v} cm → $\\xi$∈[0,1]")
    ax2.set_xlim(0, 1); ax2.set_ylim(-0.5, 2.5)
    ax2.set_xlabel("归一化坐标 $\\xi = r/R(t)$", fontsize=9)
    ax2.set_yticks([])
    ax2.set_title("(b) 计算域 $\\xi$: 固定网格", fontsize=9, pad=10)
    ax2.legend(fontsize=7, loc="upper right", frameon=True)
    ax2.text(0.5, -0.2, "变换后方程：\n$\\partial_t(\\rho c_p T R^2)\\xi = ...$\n含压缩项 $-2(\\dot R/R)\\rho c_p T$",
             ha="center", fontsize=7, color=INK,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, lw=0.8))
    despine(ax2)
    for sp in ["left", "right"]:
        ax2.spines[sp].set_visible(False)

    fig.suptitle("Q4 物质坐标变换：物理域 $r$ → 计算域 $\\xi=r/R(t)$", fontsize=11, y=1.02)
    layout(fig); save(fig, "图_F05_Q4物质坐标变换示意")


if __name__ == "__main__":
    figs = [("F-01", draw_f01), ("F-02", draw_f02),
            ("F-04", draw_f04), ("F-05", draw_f05)]
    print(f"== 开始渲染总览示意图表（{len(figs)}张）==")
    for name, func in figs:
        try:
            func()
        except Exception as e:
            print(f"  [FAIL] {name} -> {repr(e)}")
            import traceback; traceback.print_exc()
    print("== 总览示意图表渲染完成 ==")