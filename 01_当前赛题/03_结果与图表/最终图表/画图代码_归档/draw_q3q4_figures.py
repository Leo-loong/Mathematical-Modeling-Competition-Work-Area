# -*- coding: utf-8 -*-
"""
Q3+Q4 图表渲染脚本（修复版: F-33达标/F-44 GCI/F-28瀑布/F-47精度/F-25）
"""
from _fig_common import *  # 共享配置：配色/字体/尺寸/layout()
import os, sys, csv
import numpy as np

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "Work_Space","20_交付包","04_图表包","data"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
def load(name):
    return np.genfromtxt(os.path.join(DATA_DIR,name),delimiter=",",names=True,dtype=float,encoding="utf-8")
def load_d(name):
    return list(csv.DictReader(open(os.path.join(DATA_DIR,name),encoding="utf-8")))
def save(fig,stem):
    for ext in ("pdf","png"):
        fig.savefig(os.path.join(OUT_DIR,f"{stem}.{ext}"))
    plt.close(fig)
    print(f"  [OK] {stem}")
def despine(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# ============================== Q3 ==============================


def draw_f33():
    d = load("fig_q3_history.csv")
    fig, ax = plt.subplots(figsize=(10*CM,6*CM))
    ax.plot(d["t_h"],d["C_center"],color=BLUE,lw=1.5,label="水分浓度 中心 $C_0$")
    ax.plot(d["t_h"],d["C_surface"],color=RED,lw=1.5,label="水分浓度 表面 $C_R$")
    ax.axhline(0.15,color=GRAY,ls="--",lw=1.0)
    ax.text(2,0.165,"达标阈值 $C=0.15$",color=GRAY,fontsize=7,va="bottom")

    t_end = d["t_h"][-1]
    c_center_end = d["C_center"][-1]
    c_surface_end = d["C_surface"][-1]

    ax.axvline(t_end,color=RED,ls=":",lw=1.2)
    ax.annotate(f"$t$={t_end:.2f} h\n$C_0$={c_center_end:.4f}\n$C_R$={c_surface_end:.4f}",
                xy=(t_end,0.15),xytext=(t_end-15,1.0),fontsize=7,color=RED,
                arrowprops=dict(arrowstyle="->",color=RED,lw=1.0))
    ax.set_xlabel("时间 $t$ / h"); ax.set_ylabel("水分浓度 / (kg/kg)")
    ax.set_title("Q3 中心与表面水分浓度长时程演化")
    ax.legend(frameon=False,loc="upper right"); despine(ax)
    layout(fig); save(fig,"图_F33_Q3长时程含水率演化")

def draw_f34():
    d = load("fig_q3_conv.csv")
    dp = load("fig_q3_conv_pos.csv")
    fig,(ax1,ax2,ax3)=plt.subplots(1,3,figsize=(16*CM,7*CM))
    for loc,nm,mk,col in [("C0","中心$r=0$","o",BLUE),("CR","表面$R$","s",RED)]:
        ax1.plot(d["dr_mm"],d[loc],marker=mk,ms=4,lw=1.3,color=col,label=nm)
    ax1.set_xlabel("Δr / mm"); ax1.set_ylabel("水分浓度"); ax1.set_title("(a) 终态值")
    ax1.legend(frameon=False,fontsize=6.5,loc="lower right"); despine(ax1); ax1.set_xscale("log")
    ax2.plot(d["dr_mm"],d["rel_change"],marker="o",color=INK,lw=1.3,ms=4)
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel("Δr / mm"); ax2.set_ylabel("相对变化"); ax2.set_title("(b) 收敛阶")
    ax2.axhline(1e-5,color=GRAY,ls="--",lw=0.8); despine(ax2)
    # 位置列
    pairs_raw = [(p.decode('utf-8') if isinstance(p,bytes) else str(p)) for p in dp["pair"]]
    rels = dp["rel_change"]
    colors_p = [BLUE if "中心" in p or "0.0 cm" in p else RED for p in pairs_raw]
    ax3.barh(range(len(pairs_raw)),rels,color=colors_p,height=0.6)
    ax3.set_yticks(range(len(pairs_raw)))
    ax3.set_yticklabels([p[:15] for p in pairs_raw],fontsize=5.5)
    ax3.set_xlabel("相对变化"); ax3.set_title("(c) 按位置")
    ax3.axvline(1e-5,color=GRAY,ls="--",lw=0.8); despine(ax3)
    fig.suptitle("Q3 长时程收敛性与网格裁决",fontsize=10,y=1.04)
    layout(fig); save(fig,"图_F34_Q3收敛性与网格裁决")

def draw_f35():
    rows = load_d("fig_q3_sensitivity.csv")
    params = [r["param"] for r in rows]; vals = [float(r["S"]) for r in rows]
    order = np.argsort([abs(v) for v in vals])
    pp = [params[i] for i in order]; vv = [vals[i] for i in order]
    cols = [BLUE if v>=0 else RED for v in vv]
    fig,ax=plt.subplots(figsize=(8*CM,6*CM))
    ax.barh(range(len(pp)),vv,color=cols,height=0.55)
    ax.set_yticks(range(len(pp))); ax.set_yticklabels(pp,fontsize=7)
    ax.axvline(0,color=GRAY,ls="--",lw=1.0)
    margin = max(abs(max(vv)), abs(min(vv)), 0.1) * 0.15
    for i,v in enumerate(vv):
        ax.text(v+(margin if v>=0 else -margin),i,f"{v:+.2f}",va="center",fontsize=7,ha="left" if v>=0 else "right")
    ax.set_xlabel("灵敏度系数 $S$"); ax.set_title("Q3 参数灵敏度")
    ax.grid(axis="x"); ax.grid(axis="y",visible=False); despine(ax)
    layout(fig); save(fig,"图_F35_Q3参数灵敏度")

def draw_f36():
    rows = load_d("fig_q3_gci.csv")
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16*CM,7*CM))
    for typ,col,mk in [("spatial",BLUE,"o"),("temporal",GOLD,"^")]:
        sel = [r for r in rows if r["kind"].strip()==typ]
        sel.sort(key=lambda r: float(r["dr_mm"]))
        x = np.array([float(r["dr_mm"]) for r in sel])
        y = np.array([float(r["t_end_h"]) for r in sel])
        ax1.plot(x,y,marker=mk,ms=5,lw=1.3,color=col,label=f"{typ}")
        if len(y)>1:
            rc = np.abs(np.diff(y))/abs(y[-1])
            ax2.plot(x[1:],rc,marker=mk,ms=5,lw=1.3,color=col,label=typ)
    ax1.set_xlabel("步长 (mm 或 s)"); ax1.set_ylabel("$t_{end}$ / h"); ax1.set_title("(a) 终态值")
    ax1.legend(frameon=False, loc="upper right"); despine(ax1)
    ax2.set_xlabel("步长"); ax2.set_ylabel("相对偏差"); ax2.set_title("(b) 收敛趋势")
    ax2.set_yscale("log"); despine(ax2); ax2.legend(frameon=False, loc="lower left")
    fig.suptitle("Q3 离散不确定度与误差带",fontsize=10,y=1.04)
    layout(fig); save(fig,"图_F36_Q3离散不确定度与误差带")

def draw_f37():
    m = load_d("fig_q3_gs_morris.csv"); s_r = load_d("fig_q3_gs_sobol.csv")
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16*CM,7*CM))
    # Morris — 保持散点，用交错偏移避免标注互撞
    mp = [r["param"] for r in m]; mu = np.array([float(r["mu_star"]) for r in m])
    sg = np.array([float(r["sigma"]) for r in m])
    ax1.scatter(mu,sg,s=50,color=INK,zorder=5)
    # 每个标注用不同偏移方向，参数名>2字则用特殊偏移
    for i in range(len(mp)):
        if len(mp[i]) <= 2:
            ax1.annotate(mp[i],(mu[i],sg[i]),textcoords="offset points",xytext=(10+i*3,5),fontsize=7)
        else:
            ax1.annotate(mp[i],(mu[i],sg[i]),textcoords="offset points",xytext=(-45+i*5,6),fontsize=7)
    ax1.set_xlabel("$\\mu^*$"); ax1.set_ylabel("$\\sigma$"); ax1.set_title("Morris $\\mu^*$-$\\sigma$"); despine(ax1)
    # Sobol
    sp = [r["param"] for r in s_r]; S1 = np.array([float(r["S1"]) for r in s_r])
    ST = np.array([float(r["ST"]) for r in s_r])
    x = np.arange(len(sp)); w=0.35
    ax2.bar(x-w/2,S1,w,color=BLUE,label="$S_1$"); ax2.bar(x+w/2,ST,w,color=GOLD,label="$S_T$")
    for i in range(len(sp)):
        ax2.plot([x[i],x[i]],[S1[i],ST[i]],color=RED,lw=1.2)
    ax2.set_xticks(x); ax2.set_xticklabels(sp,fontsize=7)
    ax2.set_ylabel("灵敏度指数"); ax2.set_title("Sobol $S_1$ vs $S_T$")
    ax2.legend(frameon=False,fontsize=7,loc="upper right"); despine(ax2); ax2.grid(axis="y"); ax2.grid(axis="x",visible=False)
    fig.suptitle("Q3 全局灵敏度",fontsize=10,y=1.04)
    layout(fig); save(fig,"图_F37_Q3全局灵敏度")

def draw_f38():
    dg = load("fig_q3_uq_grid.csv"); dl = load("fig_q3_uq_lhs.csv")
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16*CM,7*CM))
    ax1.plot(dg["C_fr"],dg["t_end_h"],"o-",color=BLUE,lw=1.5,ms=4,label="确定性")
    ax1.set_xlabel("$C_{fr}$"); ax1.set_ylabel("$t_{end}$ / h"); ax1.set_title("(a) 截断族")
    ax1.legend(frameon=False, loc="upper right"); despine(ax1)
    ax2.scatter(dl["C_fr"],dl["t_end_h"],s=25,color=GREEN,alpha=0.7)
    ax2.set_xlabel("$C_{fr}$"); ax2.set_ylabel("$t_{end}$ / h"); ax2.set_title(f"(b) LHS (n={len(dl)})"); despine(ax2)
    fig.suptitle("Q3 低 $C$ 端外推不确定度",fontsize=10,y=1.04)
    layout(fig); save(fig,"图_F38_Q3低C端外推不确定度")

def draw_f39():
    rows = load_d("fig_q3_iface_grid.csv")
    cases = [r["case"] for r in rows]; vals = [float(r["t_dry_h"]) for r in rows]
    fig,ax=plt.subplots(figsize=(10*CM,6*CM))
    colors = [BLUE,GREEN,GOLD,GOLD,RED,RED][:len(vals)]
    ax.bar(range(len(cases)),vals,color=colors,width=0.55)
    ax.set_xticks(range(len(cases))); ax.set_xticklabels(cases,fontsize=6,rotation=20,ha="right")
    ax.set_ylabel("$t_{dry}$ / h"); ax.set_title("Q3 界面取法 × 网格分辨率对照")
    ax.axhline(vals[0],color=GRAY,ls="--",lw=1.0)
    ax.text(len(cases)-0.5,vals[0]+1,f"基准 {vals[0]:.1f} h",color=GRAY,fontsize=7,ha="right")
    ax.grid(axis="x",visible=False); despine(ax)
    layout(fig); save(fig,"图_F39_Q3界面取法与网格对照")

def draw_f40():
    d = load("fig_q3_drying_rate.csv")
    fig,ax=plt.subplots(figsize=(10*CM,6*CM))
    ax.plot(d["t_h"],d["u_kg_per_kg_h"],color=BLUE,lw=1.3,label="干燥速率")
    ax.set_xlabel("时间 $t$ / h"); ax.set_ylabel("干燥速率 / (kg/kg·h)")
    ax.set_title("Q3 干燥速率曲线")
    # 前30%找峰值
    rate = d["u_kg_per_kg_h"]; n30 = max(1,int(len(rate)*0.3))
    imax = int(np.argmax(np.abs(rate[:n30])))
    ax.annotate(f"峰值 {rate[imax]:.4f}",xy=(d["t_h"][imax],rate[imax]),
                xytext=(d["t_h"][imax]+5,rate[imax]*1.5),fontsize=7,color=RED,
                arrowprops=dict(arrowstyle="->",color=RED,lw=0.8))
    ax.legend(frameon=False, loc="upper left"); despine(ax)
    layout(fig); save(fig,"图_F40_Q3干燥速率曲线")

# ============================== Q4 ==============================

def draw_f44():
    rows = load_d("fig_q4_INV1_gci.csv")
    fig,ax=plt.subplots(figsize=(10*CM,6*CM))
    labels = []; vals = []
    for r in rows:
        k = r["kind"].strip()
        key = r["key"].strip()
        N = int(float(r["N"])); nsub = int(float(r["n_sub"]))
        t_h = float(r["t_dry_s"])/3600.0
        labels.append(f"{k} N={N} sub={nsub}"); vals.append(t_h)
    ax.barh(range(len(vals)),vals,color=BLUE,alpha=0.6,height=0.5)
    for i in range(len(vals)):
        ax.text(vals[i]+0.003,i,f"{vals[i]:.4f} h",fontsize=7,va="center")
    ax.set_yticks(range(len(vals))); ax.set_yticklabels(labels,fontsize=7)
    ax.set_xlabel("$t_{dry}$ / h"); ax.set_title("Q4 离散误差带 (GCI)")
    ax.axvline(vals[2],color=GRAY,ls="--",lw=1.0)
    ax.text(vals[2]+0.005,3.5,f"最密 {vals[2]:.5f} h",color=GRAY,fontsize=7)
    despine(ax)
    layout(fig); save(fig,"图_F44_Q4离散误差带GCI")

def draw_f45():
    df = load("fig_q4_INV2_uq_family.csv"); dl = load("fig_q4_INV2_uq_lhs.csv")
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16*CM,7*CM))
    ax1.plot(df["C_fr"],df["t_dry_h"],"o-",color=BLUE,lw=1.5,ms=4)
    ax1.set_xlabel("$C_{fr}$"); ax1.set_ylabel("$t_{dry}$ / h"); ax1.set_title("(a) 截断族"); despine(ax1)
    ax2.scatter(dl["C_fr"],dl["t_dry_h"],s=25,color=GREEN,alpha=0.7)
    ax2.set_xlabel("$C_{fr}$"); ax2.set_ylabel("$t_{dry}$ / h"); ax2.set_title(f"(b) LHS (n={len(dl)})"); despine(ax2)
    fig.suptitle("Q4 低 $C$ 端外推不确定度",fontsize=10,y=1.04)
    layout(fig); save(fig,"图_F45_Q4低C端外推UQ")

def draw_f46():
    # 复用 F-50 csv 逻辑，用 csv.DictReader 读取带字符串列的CSV
    rows = load_d("fig_q4_INV3_morris.csv")
    params = [r["param"].strip() for r in rows]
    mu_s = np.array([float(r["mu_star"]) for r in rows])
    sig = np.array([float(r["sigma"]) for r in rows])
    fig,ax=plt.subplots(figsize=(9*CM,6*CM))
    ax.scatter(mu_s,sig,s=60,color=INK,zorder=5)
    # 交错偏移：奇数向下-左, 偶数向上-右
    offsets_f46 = [(12,7),(-40,-9),(14,-5),(-44,8),(10,9),(-38,-6)]
    for i in range(len(params)):
        dx,dy = offsets_f46[i % len(offsets_f46)]
        ax.annotate(params[i],(mu_s[i],sig[i]),textcoords="offset points",xytext=(dx,dy),fontsize=7)
    ax.set_xlabel("$\\mu^*$"); ax.set_ylabel("$\\sigma$"); ax.set_title("Q4 全局灵敏度 Morris (6 参数)"); despine(ax)
    layout(fig); save(fig,"图_F46_Q4全局灵敏度")

def draw_f47():
    q3_base, prop_eff, shrink_eff, q4_actual = 57.53, 71.9, -78.8, 50.78
    net = q3_base + prop_eff + shrink_eff
    steps = [q3_base, q3_base + prop_eff, q3_base + prop_eff + shrink_eff, q4_actual]
    labels = ["Q3 基准", "物性变化 +71.9 h", "收缩效应 -78.8 h", "Q4 实际"]
    bar_vals = [q3_base, prop_eff, shrink_eff, q4_actual]

    fig, ax = plt.subplots(figsize=(10 * CM, 7 * CM))
    x = np.arange(4)
    colors = [BLUE, RED, GREEN, BLUE]
    # 画阶梯线和柱
    for i in range(4):
        bottom = 0 if i == 0 else (steps[i - 1] if bar_vals[i] > 0 else steps[i - 1] + bar_vals[i])
        ax.bar(i, bar_vals[i], bottom=bottom, color=colors[i], width=0.45, alpha=0.7)
    # 连接线
    for i in range(3):
        ax.hlines(y=steps[i], xmin=i + 0.22, xmax=i + 0.78, color=INK, lw=1.5)
        ax.hlines(y=steps[i], xmin=i + 0.78, xmax=i + 1.22, color=INK, lw=1.0, ls="--")
    # 标注
    for i, (v, s) in enumerate(zip(bar_vals, steps)):
        if i == 1:
            ax.text(i, s + 8, f"+{v:.1f} h", ha="center", fontsize=9, fontweight="bold", color=RED)
        elif i == 2:
            ax.text(i, s - 12, f"{v:+.1f} h", ha="center", fontsize=9, fontweight="bold", color=GREEN)
        else:
            ax.text(i, s + 5, f"{v:.1f} h", ha="center", fontsize=9, fontweight="bold")
    # 净效应标注在右上空白区
    ax.text(0.98, 0.92, f"净 = {net:+.1f} h", transform=ax.transAxes, fontsize=10,
            fontweight="bold", ha="right", va="top", color=INK,
            bbox=dict(boxstyle="round", fc="white", ec=GRAY, pad=0.5))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, rotation=30, ha="right")
    ax.set_ylabel("烘干时间 / h")
    ax.set_title("Q4 收缩--物性双效应分解")
    ax.grid(axis="x", visible=False)
    despine(ax)
    layout(fig)
    save(fig, "图_F47_Q4收缩物性双效应分解")

def draw_f48():
    d = load("fig_q4_INV4_latent_dT.csv")
    fig,ax=plt.subplots(figsize=(9*CM,5*CM))
    ax.plot(d["t_h"],d["dT_K"],color=RED,lw=1.3)
    ax.set_xlabel("时间 $t$ / h"); ax.set_ylabel("ΔT / K")
    ax.set_title("Q4 潜热中段温降曲线")
    imax = int(np.argmax(d["dT_K"]))
    y_range = np.max(d["dT_K"]) - np.min(d["dT_K"])
    ax.annotate(f"峰值 {d['dT_K'][imax]:.4f} K @ {d['t_h'][imax]:.2f} h",
                xy=(d["t_h"][imax],d["dT_K"][imax]),
                xytext=(d["t_h"][imax]+1.5,d["dT_K"][imax]+y_range*0.4),
                fontsize=7,color=INK,arrowprops=dict(arrowstyle="->",color=GRAY,lw=0.8))
    ax.axhline(0,color=GRAY,ls="--",lw=1.0); despine(ax)
    layout(fig); save(fig,"图_F48_Q4潜热中段温降曲线")

def draw_f49():
    d = load("fig_q4_INV5_compression.csv")
    fig,ax=plt.subplots(figsize=(10*CM,6*CM))
    ax.plot(d["t_h"],d["TR"],color=BLUE,lw=1.5,label="$T_R$ 表面温度")
    ax.plot(d["t_h"],d["T_ad"],color=RED,lw=1.2,ls="--",label="$T_{ad}$ 绝热包络")
    ax.plot(d["t_h"],d["theta_meas"],color=GREEN,lw=1.2,label="$\\theta_{meas}$ 实测")
    ax.plot(d["t_h"],d["theta_qs"],color=GOLD,lw=1.2,ls="-.",label="$\\theta_{qs}$ 准稳态")
    ax.set_xlabel("时间 $t$ / h"); ax.set_ylabel("温度 / ℃")
    ax.set_title("Q4 压缩温升机理与绝热包络")
    ax.legend(frameon=False,fontsize=7); despine(ax)
    layout(fig); save(fig,"图_F49_Q4压缩温升机理与绝热包络")

def draw_f50():
    rows = load_d("fig_q4_INV4_iface_grid.csv")
    labels = [f"{r['iface'].strip()} N={r['N'].strip()}" for r in rows]
    vals = [float(r["t_dry_h"]) for r in rows]
    fig,ax=plt.subplots(figsize=(9*CM,5*CM))
    colors = [BLUE,GREEN,RED,GOLD][:len(vals)]
    ax.bar(range(len(vals)),vals,color=colors,width=0.5)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels,fontsize=7)
    ax.set_ylabel("$t_{dry}$ / h"); ax.set_title("Q4 界面取法 × 网格对照")
    ax.axhline(vals[0],color=GRAY,ls="--",lw=1.0)
    ax.text(len(vals)-0.5,vals[0]+0.3,f"基准 {vals[0]:.2f} h",color=GRAY,fontsize=7,ha="right")
    ax.grid(axis="x",visible=False); despine(ax)
    layout(fig); save(fig,"图_F50_Q4界面取法与网格对照")


if __name__=="__main__":
    figs = [
        ("F-33",draw_f33),("F-34",draw_f34),("F-35",draw_f35),
        ("F-36",draw_f36),("F-37",draw_f37),("F-38",draw_f38),
        ("F-39",draw_f39),("F-40",draw_f40),
        ("F-44",draw_f44),("F-45",draw_f45),("F-46",draw_f46),
        ("F-47",draw_f47),("F-48",draw_f48),("F-49",draw_f49),
        ("F-50",draw_f50),
    ]
    print(f"== Q3+Q4 修复渲染（{len(figs)}张）==")
    for name,func in figs:
        try: func()
        except Exception as e:
            print(f"  [FAIL] {name} -> {repr(e)}")
            import traceback; traceback.print_exc()
    print("== Q3+Q4 完成 ==")