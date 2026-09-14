# src-new/ 代码目录（实验包-2：问题3 v2.0）

> 基于 src/（实验包-1 v1.5，已归档只读）的修改版。
> 一键复现（在 B题 根目录）：
> matlab -batch "addpath('src-new/model'); addpath('src-new/validation'); w2_model_checks"
> 同理可跑 exp6_w3_si 与 exp7_sic_w4_exp8。
> 输出：模型设计/实验包-2/work/out/

## 目录结构

model/
- drude_params.m — 固定文献 Drude 参数（DI-1 零自由参数）：换算式成文、边缘带外选择规则、敏感性扫描档位
- v20_airy_forward.m — M-A 主线：Airy 三介质正演（审核定稿 T1.3）；退化开关 opt.airy/opt.drude
- v20_tmm.m — M-B 校验器：特征矩阵法（独立公式路线；时间约定已与 M-A 校至机器精度）

validation/
- w2_model_checks.m — 退化测试 + TMM 交叉校验（三组）+ Drude 边缘复核 → 记录_W2_校验.md
- p1_si_inspect.m — Si 数据体检（附件3/4） → 记录_P1_Si.md
- exp6_w3_si.m — EXP-6 判定 + W-3 Si 反演 + Si 形态合成闭环 → 记录_EXP-6.md、记录_闭环Si.md
- exp7_sic_w4_exp8.m — EXP-7 效应分离 + W-4 SiC 修正重算 + EXP-8 量化 → 记录_EXP-7.md（含 EXP-8）

figures/ — 论文图制作脚本（设计者预留）

## 与 src/（v1.5）的关系

v1.5 的三域估计器与主管线未复制入本目录（原拷贝已清理）——问题3 反演以 v2.0 E3（Airy+固定 Drude，d 轮廓+线性 nuisance）为主；E1/E2 对 Si 形态不可用（记录_P1_Si 第3节），对 SiC 已由 v1.5 定稿（Airy 开关无可辨改善）。需要 v1.5 复算时用归档的 src/。
共享算子（poly7 条纹分量提取、d 轮廓、Δchi2=1 曲率 σ、游程/lag-1 诊断）在各脚本内自含，口径与 v1.5 一致。

## 设计要点（复现必读）

1. 固定 Drude（DI-1）：σp/γ/ε∞ 零自由参数；σp 敏感性扫描替代拟合（EXP-4 教训：自由拟合 d 漂移 +31%）；
2. 等离子体边缘选择规则：σ_edge=σp/√ε∞ 必须在条纹带外（T1.9）；SiC baseline σp=700（幅度反演，边缘 275）、Si 选型 σp=4157（扫描内点极小，边缘 543）；SiC 修正口径另取跨角度一致档 σp=4600（W-4）；
3. 双盆地/周跳防护：v2.0 E3 用 d 轮廓（粗格 0.02 + 抛物线细化），内层参数线性闭式求解——无 lsqnonlin 盆地问题；
4. 数字口径：SiC 融合基准 8.026 μm（v1.5）；Si 主数字 3.43 μm（±0.01 stat ±0.15 sys）；SiC v2.0 修正 8.665/8.601 μm（10°/15°，+0.61 μm 属系统区间上缘）——一律以 results/final/ 与 交接材料/03-1 §E 为准。