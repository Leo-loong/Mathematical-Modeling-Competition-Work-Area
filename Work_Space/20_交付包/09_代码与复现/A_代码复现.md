# A 题 · 代码与复现说明

> **定位**：交付包 09 的代码与复现说明，对应官方红线（论文附录须含**全部完整可运行源程序**，不裁剪）。
> **覆盖范围**：**Q1–Q4 的求解与检验代码**（§一 含 Q1／Q2／Q3 三段清单，§六 为 Q4 专章）；各问收口后本文件同步扩充。
> **代码位置**：工作区 `11_建模/11-3_算法与管线/Q1/code/` ↔ 交付副本 `20_交付包/09_代码与复现/code/`（内容一致）。
> 按项目约定，本文件不引用、不记载资料中出现的日期。

---

## 一、代码清单（Q1）

| 脚本 | 功能 | 输入 | 输出 |
|---|---|---|---|
| `q1_core.py` | **求解核（配置化）**：元体平衡（有限体积）＋后向欧拉＋三对角追赶法；中心两条独立装配路径；退化模式与物性缩放（供检验复用） | 参数字典、边界函数 | 场解、快照、迭代统计 |
| `q1_solver.py` | **主力求解**：附件核验 → 中心双路比对 → 单遍求解 → 写 `result1.xlsx` → 程序化格式断言 → 运行日志 | `附件1.xlsx` | `results/result1.xlsx`、`q1_run_log.txt` |
| `q1_e1_gci.py` | **检验（收敛性）**：空间 GCI（1／0.5／0.25 mm）＋时间收敛（温度与含水率分别） | `附件1.xlsx` | `q1_e1_log.txt`、`30_图表/03_图数据准备/fig_gci_data.csv` |
| `q1_e2_series.py` | **检验（解析对拍）**：圆柱非稳态级数解对拍（常边界 ＋ 分段常边界） | `附件1.xlsx` | `q1_e2_log.txt`、`fig_series_check.csv` |
| `q1_e3_explicit.py` | **检验（独立实现互验）**：显式 FTCS 第二套求解代码（无三对角、无 Picard），空间口径与主力一致，差异仅来自时间格式 | `附件1.xlsx` | `q1_e3_log.txt` |
| `q1_e3_figdata.py` | 由互验结果生成图数据 | `q1_e3_log.txt` | `fig_e3_check.csv` |
| `q1_e4_watchdog.py` | **检验（物理自检）**：方向／单调／极值看门狗 ＋ 三项退化自检 ＋ 边界口径对照 ＋ 人为注错演示 | `附件1.xlsx` | `q1_e4_log.txt` |
| `q1_e5_sensitivity.py` | **检验（灵敏度）**：单因素扰动（$D_0,h,k_m$ ±20%；$C_0$ ±5%；$T_0$ ±1 ℃）＋归一化灵敏度系数 ＋ 龙卷风图数据 | `附件1.xlsx` | `q1_e5_log.txt`、`fig_tornado_data.csv` |
| `q1_e6_smooth.py` | **检验（预处理对照）**：边界移动平均平滑 vs 不平滑 | `附件1.xlsx` | `q1_e6_log.txt`、`fig_smooth_check.csv` |
| `q1_consistency_check.py` | **一致性核验**：新旧两版结果逐值比对（用于关闭"论文数字与程序输出不符"的红线风险） | 两份 `result1.xlsx` | `q1_consistency_log.txt` |
| `q1_figdata_export.py` | **图数据导出**：由结果文件生成图表数据 | `results/result1.xlsx` | `fig_q1_field_T.csv`、`fig_q1_field_C.csv`、`fig_q1_curves.csv` |
| `q1_diag.py` | **诊断脚本**（保留以溯源）：常数扩散系数线性解 vs 半无限 Robin 估计、迭代残差序列 | `附件1.xlsx` | `q1_diag_log.txt` |
| **`q1_exact.py`** | **时间方向精确推进模块**（交付口径的核心）：半离散 ODE 装配（`assemble_T_ode`／`assemble_C_ode`）＋ 增广矩阵矩阵指数传播子（`etd_prop`）＋ T 精确推进（`run_T_expm`）＋ C-ETD（`run_C_etd`） | 被 `q1_solver.py`／`q1_core.py` 调用 | — |
| `innov/` 各脚本 | **创新化路径实验**（T0 理论化／T1 独立轨与口径／T2 不确定性量化／T3 算法升级验收）。**只出对照结论，除 T3 外不改交付口径** | `附件1.xlsx` | `innov/logs/*.log`、`fig_q1_stepsize.csv`、`fig_q1_uq.csv`、`fig_q1_gs.csv` |
| `dq_check.py` | **数据质量核查**：附件点位数、步长、缺失、离群、分段特征、物理量程 | `附件1.xlsx`、`附件2.xlsx` | `dq_check_log.txt` |
| `q1_conservation.py` | **守恒性核算**：区域积分闭合（质量 ＋ 能量），报告相对残差**并归因**；同时核验温度场逐点、逐时刻不超环境 | `附件1.xlsx`、`fig_q1_field_C.csv`、`fig_q1_field_T.csv` | `conservation_log.txt` |

**Q1 共 15 个脚本**（含 `q1_exact.py`；实存于 `Q1/code/` 的 `.py` 数），全部可独立运行；运行与检验日志与脚本同目录。

### Q2 代码清单（第二问：变物性双向强耦合）

**求解核（三份，数学等价；用于互校与性能对照）**

| 脚本 | 功能 | 输入 | 输出 |
|---|---|---|---|
| **`q2_core_c.py`** | **主力核（交付采用）**：变物性（附录3 物性函数）＋ **IMEX 交替推进**（物性逐内部子步更新）＋ 元体平衡／全隐式 ＋ **自实现追赶法**（numba JIT；无 numba 自动降级）；含 `frozen`／`decoupled` 退化模式 | 参数字典、边界函数 | 场解、快照、迭代统计 |
| `q2_core.py` | 求解核（B 版）：同上，三对角求解用 `scipy.linalg.solve_banded` | 同上 | 同上 |
| `q2_core_orig.py` | 求解核（**优化前基线**）：不用 JIT、不用快参数；**专供对照运行** | 同上 | 同上 |

**驱动与检验**

| 脚本 | 功能 | 输入 | 输出 |
|---|---|---|---|
| `q2_solver.py` | **主力求解**：附件核验 → 3 h 全程 → 写 `result2.xlsx` → **6 项程序化断言**（环境变量 `Q2_CORE` 可切换求解核） | `附件1.xlsx` | `results/result2.xlsx`、`q2_run_log.txt` |
| `q2_solver_orig.py` | **基线前台版**：用优化前核跑同一算例，结果隔离至 `result2_orig.xlsx`（供用户对照） | `附件1.xlsx` | `result2_orig.xlsx` |
| `q2_e2_frozen.py` | **检验 E2（常物性退化对拍）**：把物性**冻结为 $C_0$ 处常数**使问题退化为线性，再与**圆柱非稳态导热级数解**逐点对拍。（变物性下无解析解，这是唯一严谨的替代路径） | — | 对拍偏差表 |
| `q2_checks.py` | **检验 E3 ＋ E7**：E3 用显式 FTCS **独立实现**互验（**同步长＋端点严格对齐**）；E7 做**质量／能量区域积分闭合**核算与逐快照极值核验 | `附件1.xlsx` | `q2_checks_log.txt` |
| `q2_e5_sensitivity.py` | **检验 E5（灵敏度）**：OAT 扰动 ＋ 归一化灵敏度系数；**12 个算例并行** | — | `q2_e5_log.txt` |
| `q2_w2_foreground.py` | **检验 E1（工作流 W2 阶段）步长／网格收敛预试验**（空间二阶、时间一阶的判定依据，对应图 F-20）；**9 个算例并行** | — | `w2_foreground_log.txt` |
| `q2_figdata_export.py` | **图数据导出**：由结果文件与预试验日志生成 F-15～F-20 的数据 CSV；含 **Q1/Q2 重叠段对照**数据 | `results/result2.xlsx`、`result1.xlsx` | `fig_q2_*.csv`、`fig_q1q2_overlap.csv` |

**性能优化与溯源工具**

| 脚本 | 功能 |
|---|---|
| `q2_verify_BC.py` | **双核一致性核对**：任取两个核跑同一算例，输出逐点最大偏差（验证性能优化未改变数值） |
| `q2_bench_ab.py` | 优化前后单迭代耗时 A/B 基准（量化"CPU 占用率不变、墙钟缩短"的本质区别） |
| `q2_opt_verify.py` | 优化数值等价性校验（组件级逐位比对 ＋ 端到端回归） |
| `q2_diag_picard.py` | 诊断：内层 Picard 迭代上限对结果的影响（A/B 对照） |
| `q2_quick_check.py`、`q2_w2_prestudy.py` | 早期脚本（已被取代，**保留以溯源**） |

**Q2 共 25 个脚本**（交付主干 16 ＋ 诊断／导出／创新 9）。⟹ **两问合计 40 个脚本**，全部可独立运行。

### Q3 代码清单（第三问：长时程 ＋ 事件驱动终止）

> **说明**：Q3 **复用 Q2 的求解核**（`q2_core_c.py`，经 `q3_core.py` 包装为"环境预插值查表 ＋ 子步循环下沉 njit"的加速版），
> **不新建物性模型**；新增内容集中在**事件驱动终止、达标定位、长时程检验**。

| 脚本 | 功能 | 输入 | 输出 |
|---|---|---|---|
| **`q3_core.py`** | **求解核（交付采用）**：在 `q2_core_c` 基础上实现**两个零精度风险的加速**——① 环境边界**预插值查表**（消除每个内部子步的 Python 函数调用）；② **子步循环下沉进 njit**（一次调用推进整输出步）。`fastmath=False`，与基线**逐位一致** | — | — |
| **`q3_solver.py`** | **★主力求解**：事件驱动（全域 $C<0.15$ 即停）＋ 60 s 输出 ＋ **内部步级二分定位** ＋ **精确末行时间列** ＋ 熔断上界 120 h ＋ **6 项程序化断言** | `附件1.xlsx` | **`results/result3.xlsx`**、`q3_run_log.txt` |
| `q3_pretest_bench.py` | **T1 冒烟微基准**：组件级耗时分解 ⟹ 折算单内部步成本，用作规模与级别判定依据（**不产交付物**） | — | `q3_pretest_bench` 输出 |
| `q3_w2_convergence.py` | **检验 W2（长时程收敛性）**：比较时刻 24 h；空间 4 档（$1.0/0.5/0.25/0.125$ mm）＋ 时间 3 档（$1/16,1/32,1/64$ s） | — | `q3_w2_log.txt` |
| `q3_grid_experiment.py` | **网格裁决实验**：4 档加密至 $N=640$，判定"满足 $0.1\%$ 的最粗网格" | — | `q3_grid_log.txt` |
| `q3_conservation.py` | **检验 E7（守恒性核算）**：质量区域积分闭合与残差归因 | `results/result3.xlsx` | `q3_conservation_log.txt` |
| `q3_postcheck.py` | **后置综合检验**：① 推演偏差归因（圆柱渐近解 vs 实测）；② **表 5 数据生成**；③ **与 Q2 重叠段逐位一致性** | `result3.xlsx`、`result2.xlsx` | `q3_postcheck_log.txt` |
| `q3_e5_sensitivity.py` | **检验 E5（灵敏度）**：输出＝烘干结束时间；5 参数 × ±20%／±1 ℃，10 算例并行 | `附件1.xlsx` | `q3_e5_log.txt`、`q3_e5_S.csv` |
| `q3_impact_check.py` | **影响评估（只读）**：判定 Q3 低含水率端问题**是否波及 Q1／Q2**（值域、回升统计、$\delta/\Delta r$ 判据） | `result1/2.xlsx`、各问 solver | `q3_impact_log.txt` |
| `q3_surface_theory.py` | **表层理论分析（只读）**：收敛阶拟合（$p\approx2.65$）＋ 所需网格外推 ＋ 工况对照 | — | `q3_surface_log.txt` |
| `q3_verify_opt.py` | 加速实现的**数值等价性校验**（与基线逐位比对） | — | 校验日志 |
| `q3_diag_lowC.py`、`q3_diag_surface.py`、`q3_check_maxloc.py` | 诊断脚本：低含水率端行为、表层剖面、**极值位置（ulp 级抖动）**核验 | — | 诊断输出 |
| **`q3_core_nu.py`** | **复检｜变步长（非均匀网格）求解核**：把等距有限体积离散推广为**非等距**（界面取**沿 $C$ 的积分平均**，与沿 $C$ 的积分平均 一致），并支持**低 $C$ 端 $D$ 冻结**；`fastmath=False`；在等距网格上与 `q3_core` **逐点一致 ≤1e-11** | — | — |
| `q3_verify_nu.py` | **复检｜变步长核验证**：等距网格逐点复现交付核、T1 冒烟、表面加密网格几何体检 | `附件1.xlsx` | `q3_verify_nu_log.txt` |
| `q3_verify_grid.py` | **复检｜细网格收尾验证**：细网格 Q2 重叠段 ＋ 细网格时间收敛（$1/32$ vs $1/64$ s） | `result2.xlsx` | `q3_verify_grid_log.txt` |
| `q3_probe_crit.py` | **复检｜P3 判据敏感度**：$C_{\rm crit}=0.18/0.13$ 的 $t_{\rm end}$（探测档熔断 160 h） | `附件1.xlsx` | `q3_probe_crit_log.txt` |
| `q3_probe_dcut.py` | **复检｜P2 $D$ 冻结对照**：$D$ 在 $C_{\rm fr}=0.5/0.3/0.2$ 处冻结 | `附件1.xlsx` | `q3_probe_dcut_log.txt` |
| `q3_probe_grid.py` | **复检｜$t_{\rm end}$ 网格裁决（F-C）**：均匀 $N=80/160/320$ ＋ 表面加密 $M=20/26/30$ | `附件1.xlsx` | `q3_grid_tend_log.txt` |

**Q3 共 24 个交付脚本**（与 `11-3/Q3/` 根目录实存一致）。⟹ **三问合计 64 个脚本**，全部可独立运行。

> **另：Q3 创新项实验专区（不属交付主干）**：`11-3/Q3/innov/` 下另有 **7 个实验脚本**
> —— 自适应时间步（`q3_solver_INV1.py`）、CN 独立互验（`q3_e3_INV2_cn.py`）、
> 全局灵敏度（`q3_e5b_INV3_global.py`）、离散误差带 GCI（`q3_gci_INV4_tend.py`）、
> 低 $C$ 端 UQ（`q3_uq_INV4_lowC.py`）、分辨率扫描（`q3_xchk_dt.py`）、
> 界面取法 × 网格对照（脚本与过程日志留痕于建模方工作区 Q3 复检记录；**本包仅以 `data/fig_q3_iface_grid.csv` 取数**）；并含只读副本基线（`*_INVbase.py`）。
> 其**产物一律带 `INV` 标记、不进入交付主干**；结果与采纳裁定见
> 《11-5_实验与决策链/A_Q3创新项与外部核验·成果汇总与采纳裁定》。

> **Q3 的两个"只读分析"脚本**（`q3_impact_check.py`、`q3_surface_theory.py`）**不参与交付数值**，
> 仅用于**方法论评估**：判定历史结论是否受低含水率端问题影响。
> 其结论为"**Q1／Q2 因 $\delta/\Delta r=51$–$60\gg1$，网格充分分辨，故不受影响**"。

> ## ✅ Q3 复检发现与处置（**已完成修复**）
> `q3_probe_grid.py` 的 $t_{\rm end}$ 网格裁决曾暴露：**初版正式答案 $t_{\rm end}=87.4933$ h 存在约 $+52\%$ 的系统偏差**——
> 均匀 $N=160\to60.4965$ h、$N=320\to57.9159$ h；表面加密非均匀网格 $\to57.5284$ h。
> **根因**：界面变系数误用"两端点调和平均"（该式只对界面处系数**间断**成立），
> 而本问尾部单个网格胞内 $D$ 跨约两个数量级 ⟹ **低估**胞内有效扩散系数 ⟹ 表面通量被低估、长时程累积使 $t_{\rm end}$ 被高估。
> **处置**：界面系数改为**沿 $C$ 的积分平均**（沿 $C$ 的积分平均），已重跑主力并重生成 `result3.xlsx` 与表 5；
> 现行答案为 **$t_{\rm end}=57.5314$ h**（表面加密网格交叉印证 $57.5284$ h，差 $0.005\%$）。
> **✅ 日志口径提示（本轮更新）**：`q3_w2_log`／`q3_grid_log`／`q3_conservation_log`／`q3_postcheck_log`
> **已按现行口径复跑并与工作区同步**（旧版归档于工作区 `logs/_legacy_preM6/`）；现行值与《A_数值口径总表》§十一致。
> 详见《11_建模/11-5_实验与决策链/A_Q3复检与优化记录.md》。

> **检验编号说明**：第二问的检验编号已与第一问**统一**（E1 收敛／E2 解析对拍／E3 独立互验／
> E4 看门狗／E5 灵敏度／E6 数据预处理对照（仅 Q1）／E7 守恒核算）。
> 历史文档中的旧编号对照：**W2→E1、E4→E3、E6→E5**。

### Q4 代码清单（第四问：移动边界 · 附录4 物性 ＋ 附件2 半径收缩）

> **说明**：Q4 以 `q2_core_c.py`（Q2 交付核）**复制**到 `11-3/Q4/code/` 改造为 `q4_core.py`（**只复制不回改** Q2 文件）；
> 核心改造＝**物料坐标 $\xi=r/R(t)$ 守恒形式**（能量方程含几何压缩项）＋ **输出插值到固定欧拉距离列（域外掩蔽）** ＋ 事件驱动终止＋子步级二分。
> **交付脚本置于 `code/` 根目录**（Q4 创新项脚本亦在同级、以 `INV` 命名区分；`code/innov/` 仅含 Q1／Q2 创新项脚本）。

| 脚本 | 功能 | 输出 |
|---|---|---|
| **`q4_core.py`** | **交付求解核**：ξ 坐标守恒离散（质量 $\xi\partial_t\tilde C=\frac1{R^2}\partial_\xi(\xi D\partial_\xi\tilde C)$、能量 $\xi\partial_t[\rho c_pTR^2]=\partial_\xi(k\xi\partial_\xi T)$）＋元体平衡＋中心双路极限＋子步循环下沉 njit（`fastmath=False`） | — |
| **`q4_solver.py`** | **★主力求解**：0→$t_{\rm dry}$ 事件驱动（全域 $\max_rC<0.15$ 严格）＋子步级二分（1e-3 s）＋**熔断 240 h**（`BREAK_H = 240.0`）＋60 s 输出＋域外掩蔽＋精确末行＋**6 项程序化断言** | **`results/result4.xlsx`**、`q4_solve_log.txt` |
| `q4_table6.py` | **表6 抽样生成**：每 6 h ×（0／0.5／1.0 cm＋药材表面）＋"烘干结束"行 | `results/table6.csv` |
| `q4_pretest.py` | **W2 预试验批次（S0–S8）**：单元自检／冒烟／复用检验／绝热自检／D6 取层裁定／时间与空间收敛／插值分解／口径移植对照（默认只声明，`--go` 实跑） | `logs/q4_pretest_log.txt` |
| `q4_w6_lib.py`、`q4_INV_lib.py` | 检验套件公共库（数据装载／事件驱动求解封装） | — |
| `q4_w6_e15.py` | 检验 **E1**（24 h，$N=80/160/320$）＋ **E5**（OAT 11 算例） | `logs/q4_w6_e1.txt`／`q4_w6_e5.txt` |
| `q4_w6_e2.py` | 检验 **E2**：冻结附录4＋固定半径 vs 圆柱 Robin 级数解（57600 s） | `logs/q4_w6_e2.txt` |
| `q4_w6_e78.py`、`q4_w6_e78b.py` | 检验 **E7**（质量＋能量守恒核算）＋ **E8**（潜热对照）；`e78b` 为潜热缺陷修复后的增强档（含物性变化项） | `logs/q4_w6_e78b.txt`、`q4_e7_hist.csv` |
| `q4_diag_adiab.py` | 诊断｜几何自检 **E3-g-①**：绝热退化 $T\cdot R^2$ 不变量（修复版 vs 缺陷版对照） | `logs/q4_diag_adiab.txt` |
| `q4_diag_e3g2.py` | 诊断｜几何自检 **E3-g-②**：$\dot R=0$＋附录3 退化 vs `q2_core_c` 逐位复现 | `logs/q4_diag_e3g2.txt` |
| `q4_diag_blow.py` | 诊断：几何吹扫效应核查（历史问题定位） | — |
| `q4_core_fixed.py`、`q4_core_prebug.py` | **修复版对照核**／**缺陷前基线核**（"修复未改变数值"的证据；不作交付） | — |
| `q4_core_INV.py` | 创新项专用求解核（含 C_fr／if_mode 开关，与交付核**逐位一致**） | — |
| `q4_INV0_regression.py` | 创新项 **IN-REG**：innov 核与交付核逐位一致回归 | `innov/logs/q4_INV0_regression.txt` |
| `q4_INV1_gci_tend.py` | 创新项 **IN-1**：$t_{\rm dry}$ **离散误差带（GCI）**（空间 3 档＋时间 3 档） | `innov/out/fig_q4_INV1_gci.csv` |
| `q4_INV2_uq_lowC.py` | 创新项 **IN-2**：低 $C$ 端 $D$ 外推 UQ（截断族＋LHS 分位） | `innov/out/fig_q4_INV2_uq_*.csv` |
| `q4_INV3_global.py` | 创新项 **IN-3**：全局灵敏度（Morris $\mu^*$ ＋ LHS-PRCC，6 维含 $C_{\rm fr}$） | `innov/out/fig_q4_INV3_*.csv` |
| `q4_INV4_aux.py` | 创新项 **IN-4**：判据敏感度／fixR 效应分解／潜热中段曲线／取法×网格 | `innov/out/fig_q4_INV4_*.csv` |
| `q4_INV5_theory.py` | 创新项 **IN-5**：解析两界夹逼＋压缩温升机理（零 PDE 求解） | `innov/out/fig_q4_INV5_compression.csv` |
| `q4_INV6_sobol.py` | 创新项 **IN-6**：**Sobol 方差分解**（SALib Saltelli $N=16$ 二阶，224 代理求解） | `innov/out/fig_q4_INV6_sobol{,_S2}.csv` |
| `run_chain.py`（＋`rerun_chain.ps1`） | 一键串联驱动（按序调用预试验与主力求解）；**跨平台请用 `run_chain.py`**（`rerun_chain.ps1` 为 Windows 便捷脚本，保留作溯源） | — |

**Q4 共 24 个脚本**（`code/` 下 `q4_*.py`：交付主干 16 ＋ 创新项 8，另 `run_chain.py`／`rerun_chain.ps1` 为驱动）。
⟹ **四问合计 88 个脚本**（Q1 15 ＋ Q2 25 ＋ Q3 24 ＋ Q4 24），全部可独立运行；`code/innov/` 另含 Q1 12 ＋ Q2 4 个创新项脚本。

**核对输出**（与《A_数值口径总表》§十一对应）：

| 核对项 | 期望值 |
|---|---|
| `result4.xlsx` 断言 | `assertions overall: PASS`（6/6） |
| 工作表与维度 | `Sheet1`，**3041 行 × 22 列**（含表头 ⟹ 3040 数据行＝3039 个 60 s 行 ＋ 1 精确 $t_{\rm dry}$ 行） |
| 表头 | `时间\到药材中心的距离` ＋ `0, 0.1, …, 1.9` ＋ `药材表面`；$r>R(t)$ 留空 |
| $t_{\rm dry}$ | **182348.109 s**（50.6523 h；离散误差带 ±0.0249 h） |
| 末端 $C(0)$ | 0.14999954（4 位显示 0.1500） |
| 末端 $C(R)$ | 0.0526 kg/kg |
| $R(t_{\rm dry})$ | 1.200 cm（仍在附件2 覆盖期内，H7 末段外推未触发） |
| Tmax | 54.6274 ℃（＞环境上限 50.246 ℃，压缩温升 F-Q4-2） |

**运行**（在 `code/` 目录下）：`python q4_solver.py`（主力，实测墙钟 487 s）→ `python q4_table6.py`；
检验：`python q4_w6_e2.py`／`q4_w6_e15.py`（E1＋E5）／`q4_w6_e78b.py`（E7＋E8）／`q4_diag_adiab.py`／`q4_diag_e3g2.py`；
创新项：`python q4_INV6_sobol.py`（需 `SALib`，见 `requirements.txt`；**不装不影响求解与主检验**）。

---

## 二、运行环境

- **语言**：Python 3.14.7
- **依赖**：
  - `numpy`（≥2.x）、`openpyxl`（≥3.1）——**主力求解与全部检验脚本的必需依赖**；
  - `scipy`（≥1.18）——仅 `q1_e2_series.py` 需要（贝塞尔函数与特征根求根）；
    **主力求解不依赖 scipy**（三对角追赶法为自研实现），故无 scipy 的环境亦能独立复现结果文件；
  - `matplotlib` 非必需（绘图由图表侧按规格卡执行）。
- **平台**：Windows 11 实测通过（代码未使用平台相关特性，理论可跨平台）；
  链式启动器已完成跨平台适配（`sys.executable` ＋ 日志目录兜底），
  跨平台一键复现说明见本目录 `README_跨平台一键复现.md`
- **耗时实测**：主力求解 `q1_solver.py` 约 **56 s**（单机单线程）；六个检验脚本合计实测约 **15.5 min**（E1 104 s／E2 49 s／E3 46 s／E4 88 s／E5 508 s／E6 136 s，其中灵敏度 11 次求解最耗时）

### 2.1 工作区根目录的自适应定位（重要）

所有脚本以**自身位置**为基准定位工作区根，且采用**向上探测**而非固定层数：

```python
HERE = os.path.dirname(os.path.abspath(__file__))
# 向上查找含 10_赛题 的目录作为工作区根
def _find_root(p, _marker='10_赛题', _max=6): ...
ROOT = _find_root(HERE)
```

⟹ **同一份脚本在工作区（`11_建模/11-3_算法与管线/Q1/code/`）与交付副本（`20_交付包/09_代码与复现/code/`）两种深度下均可直接运行**，无需修改。

---

## 三、复现指南（第三方视角）

**1. 目录要求**：保持下列结构（脚本按**自身位置**定位，无需配置环境变量）：

```
<工作区根>/
├── 10_赛题/A题/附件/附件1.xlsx              ← 输入数据（题目附件）
├── 11_建模/11-3_算法与管线/Q1/code/         ← 全部脚本（工作区位置）
├── 20_交付包/09_代码与复现/
│   ├── code/                                ← 代码快照（与工作区内容一致）
│   └── results/result1.xlsx                 ← 输出
└── 30_图表/03_图数据准备/                    ← 图数据 CSV
```

> 注：脚本不要求同时存在两份代码；两处均可用，探测逻辑会自动找到工作区根。

**2. 依次运行**（在 `code/` 目录下执行）：

```
python q1_solver.py            # 产出 result1.xlsx；末行应输出 DONE assert=True
python q1_e1_gci.py            # 收敛与 GCI；产出 fig_gci_data.csv
python q1_e2_series.py         # 解析对拍（需 scipy）；产出 fig_series_check.csv
python q1_e3_explicit.py       # 独立实现互验；末行输出互验结论
python q1_e4_watchdog.py       # 物理看门狗；末行应输出失败 0 项
python q1_e5_sensitivity.py    # 灵敏度（11 次求解，约 8 min）；产出 fig_tornado_data.csv
python q1_e6_smooth.py         # 预处理对照（3 次求解）；产出 fig_smooth_check.csv
python q1_figdata_export.py    # 图数据导出
python q1_conservation.py      # 守恒性核算（质量＋能量，报告相对残差与归因）
```

**创新化路径（Q1，`innov/` 目录；除 T3 外均不动交付数值）**

```powershell
python q1_inv_T0.py            # T0 干燥工程判据（Bi_m 分区）＋ 精度预算
python q1_inv_T1_duhamel.py    # T1-1 Duhamel 半解析（真实连续时变边界对拍）
python q1_inv_T1_adaptive.py   # T1-2 误差驱动步长（Richardson 半步后验误差）
python q1_inv_T1_iface.py      # T1-3 界面系数口径对照（现行口径 vs 沿 1/D 调和型）
python q1_inv_T1_interp.py     # T1-4 边界插值口径对照（线性 vs PCHIP）
python q1_inv_T2_uq.py         # T2-1 边界噪声 UQ（严格采样 ＋ 代理 ＋ MC）
python q1_inv_T2_da.py         # T2-2 边界数据同化（Kalman ＋ RTS，level+slope）
python q1_inv_T2_gs.py         # T2-3 全局灵敏度（Morris ＋ Sobol）
python q1_inv_T2_adjoint.py    # T2-4 连续伴随灵敏度（与 OAT 交叉验证）
python q1_inv_T3.py            # T3 四闸门验收（温度精确推进 ＋ C-ETD）
```

**3. 核对输出**（与《A_数值口径总表》"Q1 求解结果与检验结论登记"逐项对应）：

| 核对项 | 期望值 |
|---|---|
| `result1.xlsx` 断言 | `DONE assert=True` |
| 工作表与维度 | 「温度」「水分浓度」，各 1801 行 × 22 列，全表 4 位小数 |
| $T(0,1800)$ | 33.5753 ℃ |
| $T(R,1800)$ | 36.7855 ℃ |
| $C(0,1800)$ | 2.5500 kg/kg（全精度 2.549992） |
| $C(R,1800)$ | 1.5104 kg/kg（全精度 **1.510381**；网格外推极限 ≈1.510249，误差带 $\pm2\times10^{-4}$，保守） |
| 空间观测阶 | $p\approx2.00$–2.03 |
| 物理看门狗 | 13 项全部通过，失败 0 项 |

**4. 已知环境相关差异**：不同 numpy 版本下浮点末位可能有 1 ULP 级差异（不影响 4 位小数结果）。

---

## 四、红线自查

- [x] **附录＝全部源程序**（求解核、主力求解、6 类检验／核验脚本、诊断脚本、数据质量与图数据导出；**无裁剪**）
- [x] **无硬编码个人路径**（全部以脚本自身位置为基准做相对定位，并自适应工作区根）
- [x] **程序可运行**（重构后已实跑验证：`q1_solver.py` 输出 `DONE assert=True`；`dq_check.py` 正常读取附件）
- [x] **结果与论文逐数字一致**（全部取自《A_数值口径总表》，禁止手抄中间输出）
- [x] 源程序同步放入「`20_交付包/11_支撑材料包/`」（**已完成**：`A_支撑材料文件列表.md` 已列全 Q1–Q4 源程序）

---

## 五、状态与残留待补

1. ✅ **Q4 的求解与检验脚本**及 `result4.xlsx` 的生成脚本**已就位**（见 §一 Q4 清单；Q4 引入附件2 体积收缩，已在 `q4_core.py` 内完成物料坐标改造）。
2. ✅ **一键复现脚本**（`run_all.py`）**已补**：**默认只打印复现计划**（不执行任何计算），
   加 `--go` 才按序运行并**把 `--go` 透传**给各脚本（被测脚本自身仍遵守《工作约束》§12 闸门：
   默认打印 `[SCALE]` 规模声明后退出）；脚本清单由**目录扫描**得出（不写死文件名），避免与源程序改名脱节。
   **覆盖范围**：求解 4 ＋ 检验/诊断 68 ＋ 创新 14（**递归包含 `code/innov/`**，共 86 个脚本）；
   公共库／非入口模块（`*_lib`／`*_par`／`*core*`／`*exact*` 等）自动排除，不会误当成程序执行。
3. 新增脚本一律放 `11_建模/11-3_算法与管线/Q<n>/`，并同步至交付副本 `09_代码与复现/code/`。

> **已完成项（原列于此）**：✅ Q1–Q4 的求解与检验脚本（实存共 **88 个**：Q1 15 ＋ Q2 25 ＋ Q3 24 ＋ Q4 24）及 `result1/2/3/4.xlsx` 的生成脚本
> **均已就位**；✅ 日志索引已并入 `README_日志索引.md`（**已扩展为全题索引**）。
>
> **Q3 口径修正的代码影响（本轮登记）**：界面变系数由"两端点调和平均"改为"**沿 $C$ 的积分平均**"，
> 已在 `q1_core`／`q2_core_c`／`q3_core`／`q3_core_nu` 四处核内统一；`result1/2/3.xlsx` 与表 5 已随重跑更新。
> **Q4 侧同一口径问题已登记**（`q4_core.py` 在研，未强改）。
