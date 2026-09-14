# A 题 · 支撑材料文件列表

> **定位**：`20_交付包/11_支撑材料包/` 的实例文件，对应**官方第十一条红线**：
> 支撑材料与论文内容不符 → 可能取消评奖资格；**文件列表必须放入论文附录**；打包 RAR/ZIP **≤20MB**；全部文件**无身份信息**。
> **当前范围**：**Q1–Q4 全部已完成**（Q1 为 0–1800 s 预热平衡阶段；Q2 为 3 h；Q3 为达标签长时程；Q4 为含收缩的达标签）。
> **⚠ 本表不含 `40_复核/` 下的机构对照实验脚本**：该类材料含外部材料对照，依脱敏红线**不得进入支撑材料**。
> **纪律**：本列表中的每个文件必须**逐一与论文内容核对一致**。

---

## 一、文件列表（论文附录直接使用此表）

> 附录建议格式：**名称 ＋ 大小 ＋ 一句话说明**。下表即为该格式的登记源。

### 1.1 源程序（类别：源程序；**全部完整可运行，不裁剪**）

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 1 | `code/q1_core.py` | 16.4 KB | 求解核：元体平衡（有限体积）＋后向欧拉＋三对角追赶法；中心两条独立装配路径；含退化与物性缩放模式供检验复用 |
| 2 | `code/q1_solver.py` | 11.4 KB | 主力求解：附件核验 → 中心双路比对 → 单遍求解 → 写结果文件 → 程序化格式断言 |
| 3 | `code/q1_e1_gci.py` | 7.3 KB | 检验（收敛性）：空间网格 GCI（1／0.5／0.25 mm）与时间收敛（温度、含水率分别） |
| 4 | `code/q1_e2_series.py` | 10.6 KB | 检验（解析对拍）：圆柱非稳态级数解对拍（常边界＋分段常边界） |
| 5 | `code/q1_e3_explicit.py` | 19.5 KB | 检验（独立实现互验）：显式 FTCS 第二套求解代码，全场逐点比对 |
| 6 | `code/q1_e3_figdata.py` | 2.3 KB | 由互验结果生成对应图数据 CSV |
| 7 | `code/q1_e4_watchdog.py` | 9.1 KB | 检验（物理自检）：看门狗（方向／单调／极值）＋三项退化自检＋边界口径对照＋人为注错演示 |
| 8 | `code/q1_e5_sensitivity.py` | 12.0 KB | 检验（灵敏度）：单因素扰动＋归一化灵敏度系数＋龙卷风图数据 |
| 9 | `code/q1_e6_smooth.py` | 6.9 KB | 检验（预处理对照）：边界移动平均平滑 vs 不平滑 |
| 10 | `code/q1_consistency_check.py` | 2.8 KB | 一致性核验：单遍新版结果与历史两版结果逐值比对（用于关闭"论文数字与程序输出不符"红线风险） |
| 11 | `code/q1_figdata_export.py` | 2.6 KB | 由结果文件导出图表数据 CSV |
| 12 | `code/q1_diag.py` | 4.8 KB | 诊断脚本（保留以溯源）：常数扩散系数线性解与半无限 Robin 估计对照、迭代残差序列 |
| 13 | `code/dq_check.py` | 5.5 KB | 数据质量核查：附件数据点位数、单调性、缺失与异常检查 |
| 14 | `code/q1_conservation.py` | 5.4 KB | 守恒性核算：区域积分闭合（质量＋能量），报告相对残差并归因；核验温度场逐点不超环境 |
| 15 | `requirements.txt` | 0.9 KB | 运行环境与依赖清单（numpy／scipy／openpyxl 版本；已注明绘图库不在本包范围） |
| 16 | `code/q2_core_c.py` | 27.3 KB | **第二问主力求解核（交付采用）**：变物性（附录3）＋ IMEX 交替推进 ＋ 元体平衡/全隐式 ＋ **自实现追赶法**（含 numba JIT；无 numba 时自动降级） |
| 17 | `code/q2_core.py` | 25.2 KB | 第二问求解核（B 版）：同上，但三对角求解用 `scipy.linalg.solve_banded`；用于与 C 版互校 |
| 18 | `code/q2_core_orig.py` | 19.4 KB | 第二问求解核（**优化前基线**，供对照运行；不含 JIT、不用快参数） |
| 19 | `code/q2_solver.py` | 8.8 KB | **第二问主力求解**：附件核验 → 3 h 全程求解 → 写 `result2.xlsx` → 6 项程序化断言；可用环境变量 `Q2_CORE` 切换求解核 |
| 20 | `code/q2_solver_orig.py` | 6.7 KB | 第二问主力求解（**基线前台版**，输出隔离至 `result2_orig.xlsx`，供用户对照运行） |
| 21 | `code/q2_checks.py` | 10.7 KB | 第二问检验：**E3 独立实现互验**（显式 FTCS，同步长＋端点严格对齐）＋ **E7 守恒性核算**（质量／能量区域积分闭合＋极值核验） |
| 22 | `code/q2_e2_frozen.py` | 5.7 KB | 第二问检验：**E2 常物性退化对拍**（与圆柱非稳态导热级数解逐点比对；因变物性无解析解而设） |
| 23 | `code/q2_e5_sensitivity.py` | 5.3 KB | 第二问检验：**E5 灵敏度分析**（OAT；并行执行 12 个算例） |
| 24 | `code/q2_w2_foreground.py` | 5.6 KB | 第二问 **E1（工作流 W2 阶段）步长／网格收敛预试验**（空间二阶、时间一阶的判定依据，对应图 F-20；并行执行 9 个算例） |
| 25 | `code/q2_figdata_export.py` | 5.9 KB | 第二问图表数据导出（F-15～F-20 的 CSV） |
| 26 | `code/q2_verify_BC.py` | 3.2 KB | **双核一致性核对工具**：任取两个求解核跑同一算例，输出逐点最大偏差（用于验证性能优化未改变数值） |
| 27 | `code/q2_bench_ab.py` | 3.6 KB | 优化前后单迭代耗时 A/B 基准（量化"CPU 占用率不变、墙钟缩短"的本质区别） |
| 28 | `code/q2_opt_verify.py` | 6.3 KB | 性能优化的数值等价性校验（组件级逐位比对 ＋ 端到端回归） |
| 29 | `code/q2_diag_picard.py` | 4.2 KB | 诊断：内层 Picard 迭代上限对结果的影响（A/B 对照，用于定量确认迭代截断问题） |
| 30 | `code/q2_quick_check.py` | 2.1 KB | 早期快速自检脚本（已被 `q2_checks.py` 取代，保留以溯源） |
| 31 | `code/q2_w2_prestudy.py` | 4.8 KB | 早期预研脚本（已被 `q2_w2_foreground.py` 取代，保留以溯源） |

**源程序小计**：Q1 基础 **15 个**（14 个脚本 ＋ `requirements.txt`）＋ Q2 **16 个**（第 16–31 项）＝ **31 个**（大小为实测值；打包时按待办 #3 复核）。

> **⚠ 大小列说明（本轮更新）**：`大小` 为**打包时实测值**，随代码更新而变（已更新第 1、2 项）；
> 其余各项在**打包时统一重测并重写本列**（见 §三 待办 #3）。**不得**沿用旧值提交。

### 1.1b 问题1 创新化代码（**本轮新增登记**；全部完整可运行、不裁剪）

> **定位**：Q1 求解模型升级（温度侧改为**时间方向精确推进**）与创新化路径（T0–T3）产生的全部代码。
> 这些脚本**参与了交付数值的生成或验证**，依官方第五条须**全部**进入附录与支撑材料。

**（1）交付求解核新增模块**

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 15b | `code/q1_exact.py` | 9.2 KB | **问题1 温度侧"时间精确推进"求解核**：矩阵指数 ＋ 分段线性 Duhamel 系数（`run_T_expm`）；离线预分解一次、全程复用；被 `q1_core.run_sim_collect` 以 `tmethod='expm'` 调用 |

**（2）创新化脚本（`code/innov/`，12 个）**

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| i1 | `code/innov/q1_inv_lib.py` | 4.2 KB | 创新模块公共库（附件读取、口径常量、结果写出） |
| i2 | `code/innov/q1_inv_par.py` | 2.8 KB | 并行执行器（创新实验批量调度） |
| i3 | `code/innov/q1_inv_T0.py` | 9.0 KB | **T0 零成本理论化**：${\rm Bi}_m$ 分区定位、$D_{\rm eff}$ 反演、误差预算分配 |
| i4 | `code/innov/q1_inv_T1_duhamel.py` | 6.5 KB | **T1 半解析参照轨**：真实时变边界的 Duhamel／级数解，与主力逐时逐点对拍 |
| i5 | `code/innov/q1_inv_T1_adaptive.py` | 4.2 KB | **T1 误差驱动自适应步长**（Richardson 半步后验估计 ＋ PI 控制器），与固定步长对拍 |
| i6 | `code/innov/q1_inv_T1_iface.py` | 3.3 KB | **T1 界面口径对照**（沿 $1/D$ 调和型积分 vs 现行口径 沿 $D$ 积分平均） |
| i7 | `code/innov/q1_inv_T1_interp.py` | 2.7 KB | **T1 边界插值口径对照**（线性 vs PCHIP；立场＝不动原始数据） |
| i8 | `code/innov/q1_inv_T2_uq.py` | 6.6 KB | **T2 不确定性量化**：边界噪声刻画 → 严格解采样 → 代理 → 蒙特卡洛分位区间 |
| i9 | `code/innov/q1_inv_T2_da.py` | 5.6 KB | **T2 边界数据同化**（Kalman／RTS 平滑），作为第二条约正交 UQ 路线 |
| i10 | `code/innov/q1_inv_T2_gs.py` | 5.2 KB | **T2 全局灵敏度**（Morris $\mu^*$／$\sigma$ ＋ Sobol $S_1$／$S_T$） |
| i11 | `code/innov/q1_inv_T2_adjoint.py` | 8.0 KB | **T2 伴随灵敏度**（连续伴随，与 OAT 交叉验证） |
| i12 | `code/innov/q1_inv_T3.py` | 7.9 KB | **T3 主算法升级**：温度精确积分的正式实现与四闸门验收核 |

**（3）创新检验日志（`code/innov/*.log`，10 份）**

| # | 文件 | 说明 |
|---|---|---|
| L1–L10 | `code/innov/logs/` 下的 `q1_inv_T0.log`／`q1_inv_T1_adaptive.log`／`q1_inv_T1_duhamel.log`／`q1_inv_T1_iface.log`／`q1_inv_T1_interp.log`／`q1_inv_T2_adjoint.log`／`q1_inv_T2_da.log`／`q1_inv_T2_gs.log`／`q1_inv_T2_uq.log`／`q1_inv_T3.log` | 各创新实验的**完整运行日志**（含判据、对照数值与结论），供评委逐条复算。**注**：日志位于 `innov/logs/` **子目录**（非 `innov/` 根） |

**创新化代码小计**：**13 个**源程序（`q1_exact.py` ＋ 12 个创新脚本）＋ **10 份**日志。

> **⟹ 问题1 源程序总计 28 个**（基础 14 脚本 ＋ 精确推进核 1 ＋ 创新脚本 12 ＋ `requirements.txt`）。

### 1.1c 问题1 检验日志（**本轮补登**，11 份，位于 `09_代码与复现/`）

| # | 文件 | 口径批次 | 说明 |
|---|---|---|---|
| J1 | `q1_run_log.txt` | **现行**（精确推进） | 主力求解日志：中心双路比对、单遍收集、程序化断言 PASS |
| J2 | `q1_e1_log.txt` | **现行** ✅ 已重跑 | E1 收敛性：空间 GCI（1／0.5／0.25 mm）＋时间收敛（T、C 分别） |
| J3 | `q1_e2_log.txt` | **现行** ✅ 已重跑 | E2／E2b 解析对拍：圆柱级数解（常边界＋分段常边界） |
| J4 | `q1_e3_log.txt` | **现行** ✅ 已重跑 | E3 独立实现互验：显式 FTCS vs 主力 |
| J5 | `q1_e4_log.txt` | **现行** ✅ 已重跑 | E4 物理看门狗：13/13 PASS ＋ 注错演示 |
| J6 | `q1_e5_log.txt` | **现行** ✅ 已重跑 | E5 灵敏度：OAT（$D_0,h,k_m$ ±20%；$C_0$ ±5%；$T_0$ ±1 ℃） |
| J7 | `q1_e6_log.txt` | **现行** ✅ 已重跑 | E6 预处理对照（温度侧无子步） |
| J8 | `conservation_log.txt` | **现行** ✅ 已重跑 | E7 守恒性核算：质量／能量区域积分闭合 |
| J9 | `q1_consistency_log.txt` | **现行** ✅ **本轮已重跑** | **同口径幂等性核验**：重跑主力 → 与交付文件**逐值一致（$0.000e{+}00$，两表 $1800\times21$）** ⟹ 关闭"论文数字与程序输出不符"红线风险 |
| **J12** | `q1_upgrade_diff_log.txt` | **对照轨**（**非缺陷**） | **升级前后对照**（跨口径）：新版 vs **升级前归档原件** —— 温度最大逐值差 **$1.0\times10^{-4}$ ℃**（14189 格）、**含水率 $0.000e{+}00$ 逐位一致** ⟹ 证明升级**只动温度侧** |
| J10 | `dq_check_log.txt` | 与时间格式**无关** | 数据质量核查（点位数／步长／缺失／离群） |
| J11 | `q1_diag_log.txt` | 与交付口径**无关** | 诊断（**非真值**）：**故意保留旧口径以复现 P-1 缺陷**，故重跑后与旧日志一致，属**自洽复现** |

> **为什么必须登记**：本包其余三问（Q2／Q3／Q4）的检验日志**均已随包交付**，
> 唯 Q1 此前缺失 ⟹ 属**包内惯例不一致**。本轮已全部同步（**SHA256 逐文件核对一致**）。
> **口径批次判定依据**：`q1_e1`–`q1_e6` 与 `conservation` 共 7 份的**文件时间戳晚于 `result1.xlsx` 的生成时刻**，
> 属同一重跑批次 ⟹ 与交付口径**同源**；J9／J11 时间戳早于升级，**如实标注为升级前留痕**。

> **不含绘图代码**：按分工，**最终绘图由写作者执行**；本包不含任何绘图程序（参阅 `04_图表包/figures_reference/README.md`）。

### 1.2 自主查阅数据资料（类别：自主数据）

| # | 文件 | 说明 |
|---|---|---|
| — | **本题无外部查阅数据** | 全部输入均来自题目附件（附件 1 边界时序、附件 2 半径序列、附件 3 结果模板）。按官方规范，**赛题原始数据不必列入支撑材料**（属题目提供），故本类别为空。 |

> **相关声明**：本队**独立完成**全部建模与计算，**未引用任何针对本题的第三方解法或论文**（见 `07_引用与术语/A_题录表.md` §一）。

### 1.3 较大篇幅中间结果图表（类别：中间结果图表）

| # | 文件（打包后的相对路径） | 大小 | 一句话说明 |
|---|---|---|---|
| 16 | `results/result1.xlsx` | 367.4 KB | 问题 1 的完整结果文件（工作表「温度」「水分浓度」，1801 行 × 22 列，4 位小数） |
| 17 | `figdata/fig_q1_field_T.csv` | 304.9 KB | 温度场 $r$–$t$ 全量数据（对应论文温度分布图） |
| 18 | `figdata/fig_q1_field_C.csv` | 268.0 KB | 水分浓度场 $r$–$t$ 全量数据（对应论文含水率分布图） |
| 19 | `figdata/fig_q1_curves.csv` | 62.2 KB | 中心／表面温度与含水率的关键点时程数据 |
| 20 | `figdata/fig_gci_data.csv` | 0.9 KB | 网格与时间收敛（GCI）检验数据 |
| 21 | `figdata/fig_series_check.csv` | 2.3 KB | 解析级数解对拍数据 |
| 22 | `figdata/fig_e3_check.csv` | 0.7 KB | 独立实现互验逐时点比对数据 |
| 23 | `figdata/fig_tornado_data.csv` | 1.7 KB | 参数灵敏度龙卷风图数据 |
| 24 | `figdata/fig_smooth_check.csv` | 0.2 KB | 数据预处理对照数据（对应图 F-14） |
| **24b** | `figdata/fig_q1_stepsize.csv` | **97.9 KB** | **本轮新增**：误差驱动自适应步长的**阶梯轨迹**数据（对应图 **F-41**）。原为 257403 行／5350.8 KB，**已抽稀**为 4964 行（前 200 点全保留＋余按 54 行抽稀），阶梯形态不变 |
| **24c** | `figdata/fig_q1_gs.csv` | 0.6 KB | **本轮新增**：问题1 全局灵敏度（Morris $\mu^*$／$\sigma$ ＋ Sobol $S_1$／$S_T$）（对应图 **F-43**） |
| **25** | `results/result2.xlsx` | **2.44 MB** | **问题 2** 的完整结果文件（工作表「温度」「水分浓度」，**10800 行 × 22 列**，4 位小数；10800 行 × 22 列；6 项程序化断言 PASS） |
| **26** | `figdata/fig_q2_field_T.csv` | 1807.3 KB | 第二问温度场 $r$–$t$ 全量数据（对应图 **F-16**） |
| **27** | `figdata/fig_q2_field_C.csv` | 1561.2 KB | 第二问水分浓度场 $r$–$t$ 全量数据（对应图 **F-17**） |
| **28** | `figdata/fig_q2_curves.csv` | 371.2 KB | 第二问关键点时程数据（对应图 **F-18**） |
| **29** | `figdata/fig_q2_props.csv` | 3.2 KB | 第二问物性随含水率的演化（对应图 **F-15**） |
| **30** | `figdata/fig_q1q2_overlap.csv` | 88.6 KB | 一二问重叠段对照数据（对应图 **F-19**） |
| **31** | `figdata/fig_q2_gci.csv` | 0.7 KB | 第二问收敛性数据（对应图 **F-20**） |

**中间结果小计**：**15 个文件**（Q1 9 ＋ Q2 6），约 **4840 KB**。

**这些文件现在的位置**（打包时从这里复制）：`20_交付包/04_图表包/data/`（与规格卡同处，保证"拿卡＋数据即可出图"）。

### 1.3b 第三问（Q3）源程序与结果（★本轮补充登记）

> **口径说明**：Q3 的界面变系数口径已修正（沿 $C$ 的积分平均），
> 下列脚本与结果文件**均为修正后版本**；部分**检验日志**为修正前留痕（见下）。

**（1）源程序（24 个 `q3_*.py`，全部完整可运行、不裁剪；大小打包时实测）**

| # | 文件 | 一句话说明 |
|---|---|---|
| 32 | `code/q3_core.py` | **Q3 交付求解核**（环境预查表 ＋ 子步循环下沉 njit；`fastmath=False`） |
| 33 | `code/q3_solver.py` | **Q3 主力求解**（事件驱动 ＋ 60 s 输出 ＋ 内部步级二分定位 ＋ 熔断 120 h ＋ 6 项断言） |
| 34 | `code/q3_pretest_bench.py` | T1 冒烟微基准（成本结构分解；不产交付物） |
| 35 | `code/q3_w2_convergence.py` | 检验：长时程收敛性（空间 4 档 ＋ 时间 3 档） |
| 36 | `code/q3_grid_experiment.py` | 检验：网格裁决实验（4 档至 $N=640$） |
| 37 | `code/q3_conservation.py` | 检验：守恒性核算（质量区域积分闭合） |
| 38 | `code/q3_postcheck.py` | 后置检验：表 5 生成 ＋ 与 Q2 重叠段一致性 ＋ 解析量级对照 |
| 39 | `code/q3_e5_sensitivity.py` | 检验：灵敏度（$t_{\rm end}$ 对 5 参数，10 算例并行） |
| 40 | `code/q3_core_nu.py` | 复检：非均匀（表面加密）网格求解核；等距网格上与交付核逐点一致 |
| 41 | `code/q3_verify_nu.py`／`q3_verify_grid.py`／`q3_verify_opt.py` | 复检：非均匀核验证、细网格收尾验证、加速等价性校验 |
| 42 | `code/q3_probe_crit.py`／`q3_probe_dcut.py`／`q3_probe_grid.py` | 复检：判据敏感度、低 $C$ 端 $D$ 冻结对照、$t_{\rm end}$ 网格裁决 |
| 43 | `code/q3_diag_mech.py`／`q3_diag_iface.py` | **界面口径诊断**：常数 $D$ 解析对拍、界面取法单变量对照（修正的直接依据） |
| 44 | `code/q3_impact_check.py`／`q3_surface_theory.py`／`q3_diag_lowC.py`／`q3_diag_surface.py`／`q3_check_maxloc.py` | **只读分析／诊断**（不参与交付数值） |
| 45 | `code/q3_audit_consistency.py`／`q3_audit_tables.py` | **只读审计**：口径一致性扫描、表 5 与 `result3.xlsx` 逐值核对 |

**（2）结果与图数据**

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 46 | `results/result3.xlsx` | 325.8 KB | **问题 3** 完整结果（单表「水分浓度」，**3452 行 × 22 列**，4 位小数；6 项断言 PASS） |
| — | `figdata/` 下 Q3 图数据 **13 件**：`fig_q3_history.csv`（104.8 KB）／`fig_q3_conv.csv`（0.3 KB）／`fig_q3_conv_pos.csv`（0.5 KB）／`fig_q3_gci.csv`（0.3 KB）／`fig_q3_drying_rate.csv`（162.8 KB）／`fig_q3_sensitivity.csv`（0.4 KB）／`fig_q3_gs_morris.csv`（0.2 KB）／`fig_q3_gs_samples.csv`（2.8 KB）／`fig_q3_gs_sobol.csv`（0.1 KB）／`fig_q3_iface_grid.csv`（0.1 KB）／`fig_q3_stepsize_adaptive.csv`（155.5 KB）／`fig_q3_uq_grid.csv`（0.2 KB）／`fig_q3_uq_lhs.csv`（0.3 KB） | 合计约 428.3 KB | **已导出**（对应图 F-33～F-35 及长时程、自适应步长、界面口径对照、全局灵敏度、UQ 各图）；源目录 `30_图表/03_图数据准备/` 与交付包 `04_图表包/data/` **同名单件一致** |

> **⚠ 关于 Q3 检验日志**：`q3_w2_log`／`q3_grid_log`／`q3_conservation_log`／`q3_postcheck_log`
> 为**修正口径前**的留痕；**现行数值以《A_数值口径总表》§十 为准**。
> 打包如需"日志与结论逐行一致"，应复跑对应脚本（代码无需改动）。

**Q3 小计**：源程序 **24 个**（含复检与审计）；结果文件 1 个（325.8 KB）；图数据 **13 个（已导出，合计约 428.3 KB）**。

### 1.2c 第二问（Q2）检验日志（**本轮补充登记**）

> **口径批次判定依据**：文件名自带的"废弃／旧版／旧编号"标注 + 与 `result2.xlsx` 生成时刻的先后。
> **⚠ 纪律**：进入支撑材料的日志**必须能说清自己属于哪一批**；未标注者按"现行"处理时须说明理由。

| # | 文件 | 口径批次 | 说明 |
|---|---|---|---|
| Q2-L1 | `q2_run_log.txt` | **现行** ✅ | **交付运行日志**：C 核／IMEX／10800 步／6 项断言全 PASS；表 3／表 4 关键值与口径表 §9.2 逐值一致 |
| Q2-L2 | `q2_checks_log.txt` | **现行** ✅ | E3（独立实现互验）＋E7（守恒核算）合并日志；**以本文件为准**（另有 e4 用例中途修正的旧文本已不含） |
| Q2-L3 | `q2_e3b_log.txt` | **现行** ✅ | E3-b 强制解耦退化检验（单向耦合下改 $h$，含水率场 $\max|\Delta C|=\mathbf{0}$ 逐位不变） |
| Q2-L4 | `q2_e5_log.txt` | **现行** ✅ | E5 OAT 灵敏度（含 $C_0$ 补检） |
| Q2-L5 | `q2_e5b_log.txt` | **现行** ✅ | E5-b 全局灵敏度（Morris＋Sobol） |
| Q2-L6 | `q2_e7_log.txt` | ⚠ **旧版留痕** | E7 守恒核算的**旧口径**输出（**恒定边界 50.0 ℃**，非线性 236.3 s 主求解），**非交付口径**（现行用附件1 时变边界）。其价值在**发现过程**：首次暴露"**变物性下 $\int\rho c_pT\,r\,\mathrm dr$ 不是守恒量**"。**现行 E7 结论以 `q2_checks_log.txt` 为准**（与《日志索引》§二 口径一致） |
| Q2-L7 | `q2_e8_log.txt` | **现行** ✅ | E8 潜热对照（计入 $L$ 后温度系统性偏低 0.074–0.077 ℃） |
| Q2-L8 | `q2_e9_log.txt` | **现行** ✅ | E9 自适应步长（墙钟 47.6→9.9 s，4.80×） |
| Q2-L9 | `q2_diag_picard_log.txt` | **现行**（诊断）✅ | **内层 Picard 上限 A/B 诊断**：A（maxit 8）均 8.000 次/子步＝**跑满**；B（maxit 120、tol $10^{-13}$）均 **16.362** 次/子步 ⟹ **即此前的"16.4"来源**（见《A_Q2可靠性与方法学》§7 更正） |
| Q2-L10 | `q2_opt_verify_log.txt` | **现行** ✅ | B/C 优化核的逐点一致性核对（差异 $\le1.8\times10^{-11}$） |
| Q2-L11 | `w2_foreground_log.txt` | **现行**（预试验） | W2 空间／时间收敛预试验（定 $\Delta r$ 与内部步长） |
| Q2-L12 | `q2_run_orig_log.txt` | **对照轨**（明示） | **优化前基线核**的运行日志（`q2_solver_orig.py`，输出 `result2_orig.xlsx`，与交付件隔离） |
| Q2-L13 | `q2_e1_log_废弃_早期未收敛.txt` | ⚠ **废弃**（文件名自明） | 早期外层迭代未收敛阶段留痕；**不代表现行口径** |
| Q2-L14 | `q2_e3_log_旧版对照.txt` | ⚠ **旧版对照**（文件名自明） | 旧编号体系下的对照文本 |
| Q2-L15 | `q2_e5_log_旧版stdout.txt` | ⚠ **旧版**（文件名自明） | 串行版 stdout 留痕 |
| Q2-L16 | `q2_e5_log_旧编号残留.txt` | ⚠ **旧编号**（文件名自明） | 编号统一前的残留 |

> **已有 4 份日志在文件名内自明标注"废弃／旧版／旧编号"**，属**诚实留痕**；
> 其余 12 份为现行或明确对照轨。**本轮核验已确认交付日志与交付文件、口径表三方逐值一致**。
> **`q2_reship_*.txt`（重交付运行 stdout）与空的 `*_stderr.txt` 不予登记**：
> 前者内容与 `q2_run_log.txt` 重复，后者为 **0 字节**（纯冗余，已从包内清除）。

### 1.3c 第四问（Q4）源程序与结果（★本轮补充登记）

> **为什么必须补**：官方**第五条**要求附录含"建模所用到的**全部完整、可运行**的源程序代码"，
> 并明确"**缺少必要的源程序**……都可能会被取消评奖资格"。此前本表**只登记到 Q3**，
> Q4 的 17 个源程序**全部未登记**，属**合规红线缺口**。本轮已把工作区 `Q4/code/` 的源程序**逐字节同步**入包并登记。
> **口径说明**：Q4 采用 ξ 坐标守恒离散（移动边界）＋ IMEX ＋ 全热路径 njit 子步下沉（`fastmath=False`）。

**（1）源程序（`code/` 下 **24 个 `q4_*.py` ＋ `run_chain.py` ＋ `rerun_chain.ps1`**，全部完整可运行、不裁剪；已做 SHA256 逐字节核对 = 全部 OK）**

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 47 | `code/q4_core.py` | 22.2 KB | **Q4 交付求解核**：ξ 坐标守恒离散（质量 $\xi\partial_t\tilde C=\frac{1}{R^2}\partial_\xi(\xi D\partial_\xi\tilde C)$、能量 $\xi\partial_t[\rho c_pTR^2]=\partial_\xi(k\xi\partial_\xi T)$）＋ 元体平衡 ＋ 中心双路 ＋ njit 子步下沉 |
| 48 | `code/q4_solver.py` | 9.7 KB | **Q4 主力求解**：写 `result4.xlsx` ＝ 表6／论文数值（事件驱动＋子步级二分＋熔断 240 h） |
| 49 | `code/q4_pretest.py` | 13.2 KB | Q4 预试验批次（**S0–S8 共 9 案例**；闸门：默认仅打印 `[SCALE]` 并退出，须 `--go`）：单元自检／冒烟／复用检验／绝热自检／D6 裁定／时间与空间收敛／插值分解／口径移植对照。**S2 判据为双判据**（交付量 C `rel≤1e-9`；监测量 T `\|ΔT\|≤5e-5 K`），严格联合判据同时打印备查 |
| 50 | `code/q4_w6_lib.py` | 4.1 KB | Q4 检验套件公共库 |
| 51 | `code/q4_w6_e15.py` | 3.4 KB | 检验 E1（24 h 三网格 GCI）＋ E5（OAT 11 算例） |
| 52 | `code/q4_w6_e2.py` | 2.9 KB | 检验 E2（常物性＋固定半径**退化对拍**） |
| 53 | `code/q4_w6_e5.py` | 3.8 KB | 检验 E5（参数灵敏度） |
| 54 | `code/q4_w6_e78.py` | 2.5 KB | 检验 E7／E8 合并档 |
| 55 | `code/q4_w6_e78b.py` | 6.5 KB | 检验 E7／E8 增强档（含物性变化项的能量核算；**E8 潜热缺陷修复后的重跑档**） |
| 56 | `code/q4_table6.py` | 1.3 KB | 由 `result4.xlsx` 生成**表6**（含 `table6.csv`） |
| 57 | `code/q4_diag_adiab.py` | 2.9 KB | 诊断：**E3-g-① 绝热自检**（同时关断导热与对流下的 $T\cdot R^2$ 不变量核算） |
| 58 | `code/q4_diag_blow.py` | 4.5 KB | 诊断：**几何吹扫效应**核查 |
| 59 | `code/q4_diag_e3g2.py` | 3.5 KB | 诊断：E3-g-②（$\dot R=0$ ＋附录3 逐位复现 Q2 的退化检验） |
| 60 | `code/q4_core_fixed.py` | 22.2 KB | **修复版对照核**（用于与交付核做数值等价性核对，属"性能／修复未改变数值"的证据） |
| 61 | `code/q4_core_prebug.py` | 21.7 KB | **缺陷前基线核**（供溯源；不作交付） |
| 62 | `code/run_chain.py` | 1.0 KB | Q4 串联执行驱动（按序调用预试验与求解） |
| **63** | `code/q4_INV6_sobol.py` | 4.5 KB | **Q4 创新项 IN-6**：Sobol 方差分解（SALib Saltelli N=16 **二阶，实际 224 次代理求解**；6 维含 C_fr；代理 N=40/n_sub=8）——依赖清单已同步（requirements.txt 补 SALib） |
| — | `code/rerun_chain.ps1` | 0.7 KB | 上述驱动的一键重跑脚本（辅助件，不占编号）；**本轮已改为路径自适应**（`$PSScriptRoot` 定位，无绝对路径） |

**★ 补登（本轮复核新增登记，编号已续编）**：以下 8 个脚本与本表同属 Q4 源程序，此前**整段漏登**，经复核实测补入，编号**顺次续编 64–71**（与上方主表 47–63 共同构成 Q4 源程序 **25 项**）：

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 64 | `code/q4_core_INV.py` | 23.4 KB | **创新项专用求解核**（含 C_fr／if_mode 开关；与交付核**逐位一致**，IN-REG 回归验证） |
| 65 | `code/q4_INV_lib.py` | 4.5 KB | 创新项公共库（数据装载＋事件驱动求解封装） |
| 66 | `code/q4_INV0_regression.py` | 2.3 KB | 创新项 **IN-REG**：innov 核与交付核逐位一致回归验证 |
| 67 | `code/q4_INV1_gci_tend.py` | 4.3 KB | 创新项 **IN-1**：$t_{\rm dry}$ 离散误差带（GCI；空间 3 档＋时间 3 档） |
| 68 | `code/q4_INV2_uq_lowC.py` | 4.0 KB | 创新项 **IN-2**：低 $C$ 端 $D$ 外推 UQ（截断族＋LHS 分位） |
| 69 | `code/q4_INV3_global.py` | 8.2 KB | 创新项 **IN-3**：全局灵敏度（Morris $\mu^*$ ＋ LHS-PRCC，6 维含 C_fr） |
| 70 | `code/q4_INV4_aux.py` | 5.4 KB | 创新项 **IN-4**：判据敏感度／fixR 效应分解／潜热中段曲线／取法×网格 |
| 71 | `code/q4_INV5_theory.py` | 5.5 KB | 创新项 **IN-5**：解析两界夹逼＋压缩温升机理（零 PDE 求解） |

**Q4 小计**：源程序 **26 项**＝`code/` 下 **24 个 `q4_*.py`**（交付主干 16 ＋ 创新项 8）＋ `run_chain.py` ＋ `rerun_chain.ps1`
（原登记"17 个／18 个"系漏登所致，**本轮已按实测改正**；编号 **47–63 共 17 项 ＋ 64–71 共 8 项 ＝ 25 项**，加辅助件 1 项 ＝ **26 项**）。

**Q4 结果与图数据**：

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 64 | `results/result4.xlsx` | 226.2 KB | **问题 4** 完整结果（表6 数值来源） |
| 65 | `results/result4_data.csv` | 348.5 KB | 问题 4 结果的 CSV 形态（便于第三方逐值核对） |
| — | `results/table6.csv` | 0.4 KB | 论文**表6** 的机读形态 |

> **⚠ Q4 待补（打包前须处理）**：
> ① ~~工作区的 `q4_e7_hist.csv`（**292 KB**，能量核算历史）**尚未入包**~~ → **已入包**（本轮 Q4 检验闭环：`09_代码与复现/q4_e7_hist.csv`，E7 守恒核算的历史序列，供复算）；
> ② ~~Q4 **图目未登记**（图表总规划约定自 **F-44** 起编），故本表暂无 Q4 图数据行~~ → **已补齐**（本轮复核：`04_图表包/04-0_图表总规划.md` 已登记 **F-44～F-50（7 张）**，总数 **43→50 张**；Q4 的 11 个图数据 CSV 在 `04_图表包/data/` 与 `30_图表/03_图数据准备/` 两侧**逐字节一致**）；
> ③ ~~工作区存在 **4.4 MB** 的 `q4_w6_e5_stderr.txt`（stderr 冗余输出）~~ **★ 已删除（R1 执行：三副本 MD5 均 `5837B07D8B45F8ABE2A6117956E6884C`、各 4.42 MB；其内容为 `multiprocessing.spawn` 崩溃刷屏，**实质结果仍保留在 `q4_w6_e5.txt`（0.9 KB）与 `q4_w6_e5_stdout.txt`（0.8 KB）**）与 `.pyc`／`.nbc` 缓存——
> **均不得进支撑材料**（既非源程序亦非结果图表），已确认**未**复制入包。

### 1.3d 第二问（Q2）创新化代码（**本轮新增登记**）

> **定位**：Q2 创新化（INV 系列）产生的脚本与数据；与 §1.1b（Q1 创新化）同规则登记。
> **纪律**：`innov/` 下的脚本**参与交付数值的生成或验证**，依官方第五条须**全部**进入附录与支撑材料。

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 66 | `code/innov/q2_inv_tol_tradeoff.py` | 8.1 KB | **INV-Q2-2**：内层 Picard **容限的成本—精度曲线**（6 档 $10^{-3}\sim10^{-11}$，单变量隔离；5 档并行） |
| 67 | `code/innov/logs/q2_inv_tol_tradeoff.log` | 2.3 KB | 上述实验的**完整日志**（逐档墙钟／四处输出／与最严档逐格差／裁决结论） |
| 68 | `code/innov/q2_inv_tol_tradeoff.csv` | 0.5 KB | 上述实验的**机读数据**（tol／墙钟／T(0)、T(R)、C(0)、C(R)／逐格差） |
| **69** | `code/innov/q2_inv_monolithic.py` | 9.6 KB | **INV-Q2-1**：**整体式（Monolithic）Newton** 实现（块联立求解 ＋ 两条耦合通道的解析耦合块），与"分区式外层迭代"及 IMEX 做**三方同口径对照** |
| **70** | `code/innov/logs/q2_inv_monolithic.log` | 2.2 KB | 上述三方对照的**完整日志**（终态对照／与 IMEX 的逐格差／墙钟与迭代成本／实现复杂度） |
| **71** | `code/innov/q2_inv_tol_delivery.py` | 5.0 KB | **INV-Q2-2 后续 · 放宽裁决**：在**交付口径**（3 h／n_sub$=32$／时变边界）下重做 tol 单变量对照（$10^{-10}$ vs $10^{-9}$） |
| **72** | `code/innov/logs/q2_inv_tol_delivery.log` | 1.9 KB | 上述裁决的**完整日志**（整表逐格差／表 3、表 4 关键值对照／裁决结论） |
| **73** | `code/innov/q2_inv_tol_converge.py` | 5.2 KB | **INV-Q2-2 后续 · 收敛充分性裁决**：tol 四档扫描（$10^{-9}\!\sim\!10^{-12}$，以最严档为参考） |
| **74** | `code/innov/logs/q2_inv_tol_converge.log` | 2.1 KB | 上述扫描的**完整日志**（四档墙钟／内层迭代数／逐格差／表 3、表 4 随 tol 的变化） |

> **INV-Q2-1 的结论（供论文"模型求解"节取用）**：三条路线同口径对照（600 s 方法级）——
> ① **整体式 Newton 与 IMEX 逐格一致**（$|\Delta T|\le2.5\times10^{-5}$ ℃、$|\Delta C|\le8.6\times10^{-7}$）
> ⟹ **IMEX 与联立求解等价**，是"为何不必联立"的最强证据；
> ② **分区式外层迭代跑满 20 轮仍未收敛**，$C(R)$ 偏 **1.283 kg/kg**（T 偏 1.054 ℃）
> ⟹ 实测复现 kb 论断"强耦合下分区式收敛慢"；
> ③ **成本**：IMEX **4.1 s** vs 整体式 Newton **62.9 s** vs 分区式 **65.1 s** ⟹ IMEX 约 **1/15 成本**达同一解。
> ⚠ **自披露局限**：本实现的 Jacobian 为**不精确 Newton**（缺界面级交叉导数）⟹ 收敛线性、成本对照**对 Newton 不利（保守）**。

> **该实验的结论（供论文"模型求解"节取用）**：① **kb 文献推荐的 tol $=10^{-3}$ 在本题不成立**——
> 其逐格最大偏差达 $1.39\times10^{-1}$ kg/kg（≈2775 个最小位）⟹ 本题非线性**显著陡于**该文献领域；
> ② **在本实验口径**（1 h／n_sub$=16$／恒定边界）下，与最严档（$10^{-11}$）逐格一致的**最松容限 $=10^{-9}$**，
> 而**现行交付取 $10^{-10}$**（`q2_solver.py` 未显式传 tol ⟹ 核默认值）。
> ⚠ **替换交付口径须另行授权 ＋ 四闸门**（本实验仅覆盖 1 h 时程）。

> **⚠⚠ 上述②的"可放宽"结论已被后续裁决实验推翻（2026-09-11，经授权执行）**：在**交付口径**
> （3 h／n_sub$=32$／**时变边界**）下重做单变量扫描——**$10^{-9}$ 与最严档不一致**
> （$\max\lvert\Delta C\rvert=1.73\times10^{-4}$，$C(R,3\,\mathrm h)$ 由 1.008113 → **1.008212**，4 位小数末位改变）
> ⟹ **放宽不可行、不予采纳**；而**现行 $10^{-10}$ 与最严档（$10^{-12}$）逐格一致**
> （$\Delta C=1.6\times10^{-5}<\tfrac12$ 最小位）⟹ **已收敛、可交付**。
> **⟹ 交付容限维持 $10^{-10}$，`result2.xlsx` 不重出。**
> **两条方法学教训（论文可正面引用）**：**(a)** $10^{-10}$ **不是经验冗余而是"临界必要档"**
> （再松一档即出 $1.7\times10^{-4}$ 偏差）；**(b)** **短时程／恒定边界下的容限结论不可外推至交付口径**
> ——3 h 时程与时变边界使 Picard 滞后误差得以累积，正是"**检验必须在交付口径下做**"的实例。


### 1.3e 第二问（Q2）创新链支持脚本（**本轮补登**）

> **定位**：第 2 问**创新化（INV 系列）**的支持脚本——参与**交付数值的生成或验证**（BDF2 对照、潜热对照、强制解耦、全局灵敏度、自适应、Pareto、图数据导出、结果核验），依官方第五条须**全部**进入附录与支撑材料。
> **纪律**：说明文字取自各脚本**自身 docstring 首句**；`innov/logs/` 下的日志已在 §1.3d 登记。

| # | 文件 | 大小 | 一句话说明 |
|---|---|---|---|
| 75 | `code/run_innov_chain.py` | 1.0 KB | Q4 innov 四支求解档串行启动器（INV1->INV2->INV3->INV4）。 |
| 76 | `code/run_innov_chain2.py` | 0.8 KB | Q4 innov 补跑链（INV3 修复版 -> INV4）。 |
| 77 | `code/q2_core_bdf2.py` | 28.8 KB | A 题 Q2 求解核 · BDF2 变体（二阶时间精度） |
| 78 | `code/q2_core_latent.py` | 29.7 KB | A 题 Q2 求解核 · 潜热对照变体（检验 E8） |
| 79 | `code/q2_e3b_decoupled.py` | 5.1 KB | A 题 Q2 · 检验 E3-b：强制解耦退化 ＋ 耦合强度量化 |
| 80 | `code/q2_e5b_global.py` | 9.0 KB | A 题 Q2 · 检验 E5-b：全局灵敏度（Morris 筛选 ＋ Sobol 定量） |
| 81 | `code/q2_e8_latent.py` | 6.7 KB | A 题 Q2 · 检验 E8：蒸发潜热对照（假设 H3） |
| 82 | `code/q2_e9_adaptive.py` | 7.3 KB | A 题 Q2 · 检验 E9：自适应时间步 |
| 83 | `code/q2_f30_pareto.py` | 4.4 KB | F-30 精度–效率帕累托图 · 数据导出 |
| 84 | `code/q2_fig_export.py` | 8.5 KB | Q2 图数据导出（F-26 / F-27 / F-28 / F-29 / F-31 / F-32） |
| 85 | `code/q2_verify_results.py` | 4.9 KB | Q2 · 基线版 vs 优化版（B+C）结果全表逐点核对 |

**创新链支持脚本小计**：**11 个**（A-10 回验补登）。
### 1.4 AI 工具使用详情（官方 AI 规定要求）

| # | 文件 | 说明 |
|---|---|---|
| 25 | `AI工具使用详情`（**口径＝`12_AI工具使用详情/A_AI工具使用登记.json`**） | JSON（现行件；**登记条数以机读源为准**，滚动进行中） | **唯一口径是 JSON**（含官方四要素：工具名称版本／使用目的环节／关键提示与交互／采纳与人工核验）。**md／PDF 按需导出**（`python tools\gen_ai_log.py build --pdf` ⟹ 输出至 `99_过程与归档/AI登记表_导出归档/`，**不外发**；**不要求每次更新都导出**）。**提交前**如需随材料附 PDF，跑一次该命令即得（**2026-09-12 导出件 1.06 MB／1,114,936 B 已归档**；机制见 `00_规则/工作约束.md` §8.1 v5、`40_复核/02_差异台账/` §十一）。**⚠ 已知导出限制**：本机字体（Microsoft YaHei）缺 `⟹ ✅ 📊 ⏳ 🔒 ↔ Ṙ` 等字形，pandoc 导出时逐处报 `Missing character` ⟹ 这些符号在 PDF 中**显示为空缺**（**文字内容不受影响**）；如需修正，须改**机读源**（装饰性符号改文本）或改用含符号字形的字体 |

> **⚠ 本轮发现并闭合的一处"登记与实际不符"**：本项此前已登记为 `AI工具使用详情.pdf`，但**全盘检索确认该 PDF 当时并不存在**
> （`12_AI工具使用详情/` 下只有 `00_模板.md` 与 `A_AI工具使用登记.md`）——属"**清单≠实际**"类漂移。
> **本轮已实际导出**（pandoc 3.10.2 ＋ xelatex／TeXLive 2026，`mainfont=Microsoft YaHei` 以覆盖 CJK 与希腊字母），
> 产物 **1.01 MB**（当时版本）。**⚠ 时点说明（2026-09-12）**：该 PDF **已按"交付包只留 JSON"的裁定移出交付包**，现归档于 `99_过程与归档/AI登记表_导出归档/`（**按需重出**：`python tools\gen_ai_log.py build --pdf`）；交付包 `12_AI工具使用详情/` 现为 `00_模板.md` ＋ `A_AI工具使用登记.json` ＋ `README.md`（说明见该目录 `README.md`）。
>
> **导出配方（供打包者复现，勿凭记忆重写）**：
> ```
> （现行导出方式：`python tools\gen_ai_log.py build --pdf`，输出至 `99_过程与归档/AI登记表_导出归档/`；等价 pandoc 命令如下）
>   --pdf-engine=xelatex -V mainfont="Microsoft YaHei" -V CJKmainfont="Microsoft YaHei" \
>   -V monofont="Consolas" -V geometry:margin=1.5cm --toc --toc-depth=1
> ```
> **两个必须的开关及原因（否则导不出）**：**(a)** `-f markdown-raw_tex` —— 文档正文含 **Windows 路径反斜杠**
> （如 `11-3_算法与管线\Q2\...`），pandoc 默认会当作**裸 LaTeX** 传入而报 `Undefined control sequence`；
> **(b)** 字体须用 **Microsoft YaHei** 而非 TeX 默认拉丁字体 —— 正文含 $\approx$／$\rho$／$\le$／$\ge$／$\tau$／$\Longrightarrow$／①
> 等符号，拉丁字体缺字形。**另**：本轮另修复了登记表中 **5 处非法转义 `\*`**（LaTeX 数学中非法，改为 `*`）。
> **⚠ 纪律**：**登记表内容一经改动，本 PDF 必须重出**（否则提交件与登记表不符）。

---

### 1.5 四问检验日志（**本轮按真源补入并登记**）

> **背景**：本轮交付同步时按 `11-3_算法与管线/Q{1,2,3,4}/` 全树（含 `logs/` 与 `innov/logs/`）对交付副本 `09_代码与复现/` 回验，**四问日志合计 153 份**（按本问相对路径计；等价重名去重后入包），本轮**补入 69 份**并在此逐名登记，后续同一目录新增日志**随包同步、按目录批量登记**。

**Q1（23 份）**：

- `code/_e5_rerun_stdout.txt`
- `code/conservation_log.txt`
- `code/dq_check_log.txt`
- `code/q1_consistency_log.txt`
- `code/q1_diag_log.txt`
- `code/q1_e1_log.txt`
- `code/q1_e2_log.txt`
- `code/q1_e3_log.txt`
- `code/q1_e4_log.txt`
- `code/q1_e5_log.txt`
- `code/q1_e6_log.txt`
- `code/q1_run_log.txt`
- `code/q1_upgrade_diff_log.txt`
- `innov/logs/q1_inv_T0.log`
- `innov/logs/q1_inv_T1_adaptive.log`
- `innov/logs/q1_inv_T1_duhamel.log`
- `innov/logs/q1_inv_T1_iface.log`
- `innov/logs/q1_inv_T1_interp.log`
- `innov/logs/q1_inv_T2_adjoint.log`
- `innov/logs/q1_inv_T2_da.log`
- `innov/logs/q1_inv_T2_gs.log`
- `innov/logs/q1_inv_T2_uq.log`
- `innov/logs/q1_inv_T3.log`

**Q2（24 份）**：

- `code/q2_checks_log.txt`
- `code/q2_diag_picard_log.txt`
- `code/q2_e1_log_废弃_早期未收敛.txt`
- `code/q2_e3_log_旧版对照.txt`
- `code/q2_e3b_log.txt`
- `code/q2_e5_log.txt`
- `code/q2_e5_log_旧版stdout.txt`
- `code/q2_e5_log_旧编号残留.txt`
- `code/q2_e5b_log.txt`
- `code/q2_e7_log.txt`
- `code/q2_e8_log.txt`
- `code/q2_e9_log.txt`
- `code/q2_opt_verify_log.txt`
- `code/q2_reship_c_stderr.txt`
- `code/q2_reship_c_stdout.txt`
- `code/q2_reship_stderr.txt`
- `code/q2_reship_stdout.txt`
- `code/q2_run_log.txt`
- `code/q2_run_orig_log.txt`
- `code/w2_foreground_log.txt`
- `innov/logs/q2_inv_monolithic.log`
- `innov/logs/q2_inv_tol_converge.log`
- `innov/logs/q2_inv_tol_delivery.log`
- `innov/logs/q2_inv_tol_tradeoff.log`

**Q3（59 份）**：

- `innov/logs/q3_INV1_adaptive.log`
- `innov/logs/q3_INV2_3h_stderr.txt`
- `innov/logs/q3_INV2_3h_stdout.txt`
- `innov/logs/q3_INV2_e3.log`
- `innov/logs/q3_INV2_stderr.txt`
- `innov/logs/q3_INV2_stdout.txt`
- `innov/logs/q3_INV3_global.log`
- `innov/logs/q3_INV3_stderr.txt`
- `innov/logs/q3_INV3_stdout.txt`
- `innov/logs/q3_INV4_gci.log`
- `innov/logs/q3_INV4_stderr.txt`
- `innov/logs/q3_INV4_stdout.txt`
- `innov/logs/q3_INV4_uq.log`
- `innov/logs/q3_INV4uq_stderr.txt`
- `innov/logs/q3_INV4uq_stdout.txt`
- `innov/logs/q3_energy_stdout.txt`
- `innov/logs/q3_xchk_dt.log`
- `innov/logs/q3_xchk_gt02.log`
- `innov/logs/q3_xchk_gt02_stderr.txt`
- `innov/logs/q3_xchk_gt02_stdout.txt`
- `logs/_legacy_preM6/q3_conservation_log.txt`
- `logs/_legacy_preM6/q3_grid_log.txt`
- `logs/_legacy_preM6/q3_postcheck_log.txt`
- `logs/_legacy_preM6/q3_w2_log.txt`
- `logs/q3_conservation_log.txt`
- `logs/q3_diag_iface_log.txt`
- `logs/q3_diag_mech_T_log.txt`
- `logs/q3_diag_mech_log.txt`
- `logs/q3_e5_log.txt`
- `logs/q3_energy_log.txt`
- `logs/q3_grid_log.txt`
- `logs/q3_grid_tend_log.txt`
- `logs/q3_impact_log.txt`
- `logs/q3_postcheck_log.txt`
- `logs/q3_probe_crit_log.txt`
- `logs/q3_probe_dcut_log.txt`
- `logs/q3_run_log.txt`
- `logs/q3_surface_log.txt`
- `logs/q3_verify_grid_log.txt`
- `logs/q3_verify_nu_log.txt`
- `logs/q3_w2_log.txt`
- `q3_audit_consistency_log.txt`
- `q3_audit_tables_log.txt`
- `q3_check_maxloc_log.txt`
- `q3_conservation_log.txt`
- `q3_diag_iface_log.txt`
- `q3_diag_mech_log.txt`
- `q3_e5_log.txt`
- `q3_grid_log.txt`
- `q3_grid_tend_log.txt`
- `q3_impact_log.txt`
- `q3_postcheck_log.txt`
- `q3_probe_crit_log.txt`
- `q3_probe_dcut_log.txt`
- `q3_run_log.txt`
- `q3_surface_log.txt`
- `q3_verify_grid_log.txt`
- `q3_verify_nu_log.txt`
- `q3_w2_log.txt`

**Q4（47 份）**：

- `innov/logs/innov_chain2_done.txt`
- `innov/logs/innov_chain_done.txt`
- `innov/logs/inv1_stdout.txt`
- `innov/logs/inv2_stdout.txt`
- `innov/logs/inv3_stdout.txt`
- `innov/logs/inv3b_stderr.txt`
- `innov/logs/inv3b_stdout.txt`
- `innov/logs/inv4_stderr.txt`
- `innov/logs/inv4_stdout.txt`
- `innov/logs/inv6_stderr.txt`
- `innov/logs/inv6_stdout.txt`
- `innov/logs/q4_INV0_regression.txt`
- `innov/logs/q4_INV1_gci_tend.txt`
- `innov/logs/q4_INV2_uq_lowC.txt`
- `innov/logs/q4_INV3_global.txt`
- `innov/logs/q4_INV4_aux.txt`
- `innov/logs/q4_INV5_theory.txt`
- `innov/logs/q4_INV6_sobol.txt`
- `logs/_legacy_r1_storage_fix/q4_pretest_log_r1.txt`
- `logs/_legacy_r1_storage_fix/q4_solve_log.txt`
- `logs/_legacy_r1_storage_fix/q4_w6_e1.txt`
- `logs/_legacy_r1_storage_fix/q4_w6_e7.txt`
- `logs/_legacy_r1_storage_fix/q4_w6_e8.txt`
- `logs/_pretest_run1_20260912.txt`
- `logs/_pretest_stderr.txt`
- `logs/_pretest_stdout.txt`
- `logs/_pretest_stdout2.txt`
- `logs/q4_diag_adiab.txt`
- `logs/q4_diag_e3g2.txt`
- `logs/q4_pretest_log.txt`
- `logs/q4_solve_log.txt`
- `logs/q4_solve_progress.txt`
- `logs/q4_w6_e1.txt`
- `logs/q4_w6_e2.txt`
- `logs/q4_w6_e5.txt`
- `logs/q4_w6_e5_stderr.txt` —— **★ 已删除（R1 执行）**：4.42 MB 的 stderr 冗余输出，已从工作区、交付包与 rerun 快照三处移出；实质结果保留在同名 `.txt`／`_stdout.txt`
- `logs/q4_w6_e5_stdout.txt`
- `logs/q4_w6_e7.txt`
- `logs/q4_w6_e78b.txt`
- `logs/q4_w6_e78b_stderr.txt`
- `logs/q4_w6_e78b_stdout.txt`
- `logs/q4_w6_e8.txt`
- `logs/rerun_chain_done.txt`
- `logs/rerun_e1.txt`
- `logs/rerun_e5.txt`
- `logs/rerun_e78b.txt`
- `logs/rerun_solve.txt`

---

## 二、体量与红线自查

| 检查项 | 要求 | 现状 | 判定 |
|---|---|---|---|
| 压缩包体量 | RAR/ZIP **≤20MB**（**提交组委会的支撑材料包**，非交付包目录） | 实测约 **10.4 MB**：源程序 ≈1.1 MB（Q1 基础 14 ＋ 精确推进核 1 ＋ 创新 12 ＋ Q2 16 ＋ Q3 24 ＋ **Q4 24** ＋ 依赖清单）＋ 结果文件 ≈3.7 MB（`result1–4` ＋ `result4_data.csv`）＋ 中间结果图表 ≈4.9 MB（37 个 CSV）＋ `AI工具使用详情.pdf`（**提交前按需导出后再纳入**；现行导出件 **1.06 MB**）| ✅ 余量充足 |
| 文件与论文一致 | 逐项对照，不得出现论文未提及的文件／反之 | 本表与论文附录、正文数字一一对应（各问数字取自《数值口径总表》相应节） | ✅（待全包整体复核） |
| 源程序完整性 | **全部完整可运行，不裁剪**（官方第五条红线） | **四问源程序 125 个（`code/` 顶层 80 ＋ `code/innov/` 45）＋ 1 份依赖清单**全部在列 —— **按交付副本 `code/` 实测**：顶层 `q*.py` **78**（Q1 15／Q2 25／Q3 24／Q4 16）＋ `code/innov/` **45**（Q1 12／Q2 4／Q3 17／Q4 12）＝ **125**；与真源 `11-3_算法与管线/Q{1,2,3,4}/{code,innov}` **逐件一致、basename 零缺**（等价路径去重后） | ✅（**已按包内实测重算**；Q4 曾整段缺失，前轮已闭合；本轮再补 **29 个 innov 脚本落位** ＋ **16 个重复副本清除**） |
| 无身份信息 | 姓名／学校／赛区／Logo 一律不得出现 | 文件名与内容均为中性技术命名 | ✅（打包前再核一次） |
| 承诺书／编号页 | **不放**入支撑材料 | 未纳入 | ✅ |
| 文件列表入附录 | 论文附录须含本表（名称＋大小＋一句话说明） | 本表即为附录素材 | ✅ |
| 无支撑材料时的声明 | 若确无支撑材料，附录须注明"本论文没有支撑材料" | 本题**有**支撑材料，不适用 | — |
| **零外部本题引用** | 不得含任何针对本题的第三方解法／数据 | 已扫描确认（`07_引用与术语/A_题录表.md` §一 红线） | ✅ |

---

## 三、打包待办（Q1 阶段后的执行清单）

| # | 事项 | 归属 | 说明 |
|---|---|---|---|
| 1 | 将 `04_图表包/data/*.csv` 复制为压缩包内的 `figdata/` | 打包步骤 | **数据源已就绪**（9 个）；复制后核对文件数（应为 9 个） |
| 2 | 生成 `AI工具使用详情.pdf`（**按需，非强制**） | 打包步骤 | 唯一口径＝`20_交付包/12_AI工具使用详情/A_AI工具使用登记.json`；导出：`python tools\gen_ai_log.py build --pdf` → `99_过程与归档/AI登记表_导出归档/` |
| 3 | 文件大小复核 | 打包步骤 | 源程序会随 Q2–Q4 增补而变大，**打包时重新生成本表的大小列** |
| 4 | 整体匿名检查 | 复核关口 | 打包前逐文件扫描（含 PDF 元数据中的作者字段） |
| 5 | Q2–Q4 完成后扩充本表 | 建模侧 | 新增脚本／结果文件／图数据同规则登记 |

---

## 四、变更记录

| 版次 | 变更 |
|---|---|
| v1 | 首版（Q1 阶段）：Q1 源程序／结果／图数据登记 ＋ 打包规范 |
| v2 | 扩充至 Q2／Q3（各问源程序、结果、图数据） |
| v3 | **Q4 整段补登**（原"只登记到 Q3"属官方第五条红线缺口）：Q4 源程序主表 47–63 ＋ 结果文件；并闭合"清单≠实际"漂移 |
| **v4** | **本轮（复核闭环）**：① 8 个此前**漏登**的 Q4 脚本**编号顺次续编 64–71**（消除"—"占位与"编号待重排"悬挂），Q4 源程序小计＝**25 项 ＋ 1 辅助件 ＝ 26 项**，与 `code/` **实测 24 个 `q4_*.py` ＋ 2 驱动**一致；② 消除"17 个 vs 18 个"自相矛盾的表述残留（统一为按实测口径）；③ **`rerun_chain.ps1` 改为路径自适应**（不再内嵌绝对路径），并在 §1.3c 标注 |

> **提示**：本表是**登记源**，不是压缩包本身；打包时以本表为清单逐项核对，并在论文附录中按 1.1／1.3／1.4 三类呈现。

---

## 四、变更记录

| 版次 | 变更 |
|---|---|
| v1 | 建立支撑材料文件列表（13 脚本 ＋ 9 中间文件 ＋ AI 详情，含体量与红线自查、打包待办） |
| **v6** | **独立核验后的补登（本轮）**：① 新增 **§1.1c 问题1 检验日志**（11 份）——Q2／Q3／Q4 日志均已随包，唯 Q1 缺失，属**包内惯例不一致**，已同步并 SHA256 核对；② 每份日志标注"**口径批次**"（现行 ✅ 已重跑／⚠ 升级前留痕／与时间格式无关），判定依据为**文件时间戳与 `result1.xlsx` 的先后**；③ 更正 v3 中"移除旧口径 `harm`"的**错误表述**（`harm` 实际仍保留于代码、仅供对照、不参与生产路径） |
| **v5** | **合规缺口闭合（自检发现）**：① 新增 **§1.3c 第四问源程序与结果**——补登 Q4 的 **17 个源程序**（此前**整段缺失**，触官方第五条"缺少必要的源程序可取消评奖资格"红线）＋ `result4.xlsx`／`result4_data.csv`／`table6.csv`；② 全部 Q4 源程序已**逐字节（SHA256）核对**入包，并发现交付核 `q4_core.py` 曾落后工作区 **0.8 KB**（已同步）；③ 修正 §1.1b 日志路径为实际所在的 `code/innov/logs/`（此前写作 `code/innov/*.log`，与实际目录不符——**清单一度与实际不一致**）；④ 修正 §二 的"源程序完整性"行（原写"14 个脚本"，实为四问合计 **84 个**）与体量重算（≈**10.4 MB**）；⑤ 明确 **Q4 待补三项**（`q4_e7_hist.csv` 未入包、Q4 图目未登记、4.4 MB stderr 与缓存**不得进包**） |
| **v4** | **Q1 模型升级后的同步（本轮）**：① 新增 **§1.1b 问题1 创新化代码**——登记 `q1_exact.py`（精确推进核）＋ `innov/` **12 个创新脚本**＋ **10 份创新日志**，并声明"问题1 源程序总计 28 个"；② 更新 `q1_core.py`／`q1_solver.py` 的**实测大小**并新增"大小列须打包时重测"的显式提示；③ §1.3 新增 `fig_q1_stepsize.csv`（**已抽稀** 5350.8 KB → 97.9 KB）与 `fig_q1_gs.csv`；④ §二 体量改为按**支撑材料压缩包**口径重算（≈**9.6 MB**，纠正此前仅计 Q1＋Q2 的低估）；⑤ 明确**机构对照实验脚本不得进支撑材料**（脱敏红线） |
| **v2** | ①**新增 `requirements.txt`**（第 15 项）并**修正"13 个脚本"的计数矛盾**；②**中间文件路径修正**为实际位置 `04_图表包/data/`（原登记指向工作区路径，打包时会找不到）；③待办 #1 状态更新为"**数据源已就绪**"；④新增**零外部本题引用**自查项；⑤新增**变更记录**节 |
| **v3** | **Q1 收口同步（本轮）**：① 修正**源程序小计**与表格计数不符（Q1 15 ＋ Q2 16 ＝ **31**）；② 新增 Q1 交付素材并登记——**论文表格素材**（`01_模型叙述/A_Q1论文表格_表1表2.md`）与 **Q1 日志索引节**（`09_代码与复现/README_日志索引.md` §一）；③ 登记 **Q1 代码口径清理**（~~`q1_core.py` 移除旧口径 `harm`~~ **此说法经代码核对有误**：`harm` **仍保留于代码中，仅供旧口径对照、不参与生产路径**；生产路径为 `faceD_int`；`q1_e3_explicit.py`／`q1_diag.py` 界面 $D$ 已对齐），**待统一重跑验证**；④ **Q4 支撑材料待补**（独立于本表，待 Q4 收口） |
| **v1.x（A-10 回验补登）** | **补登 Q2 创新链支持脚本 2 个**（`code/innov/` 与 `run_innov_chain*.py`）——此前"盘上有、清单没有"，撞官方第十一条"支撑材料与论文不符"红线；说明取自各脚本 docstring 首句。来源：`40_复核/05_成绩评定/temp/_check_support_list.py` 双向回验 |

| **v6（交付同步轮 · 源＝`20_交付包/`）** | **按真源回验并补登**：① **源程序完整性行按包内实测重算**（`code/` 顶层 **80** ＋ `code/innov/` **45** ＝ **125**；四问顶层 Q1 15／Q2 25／Q3 24／Q4 16）—— 原"88 个"系旧口径计数，**已作废**；② **新增 §1.5 四问检验日志逐名登记**（按 `Q*/{logs,innov/logs}` 全树），本轮**补入 69 份**、**清除 16 个重复副本**、**29 个 innov 脚本按真源落位到 `code/innov/`**；③ 未改动任何数值、结果文件（`result1–4`／`result4_data.csv`／`table6.csv`）与题面附件 |
| **v7（复核轮）** | **Q3 创新项中间产物不入包（判据＝是否被引用）**：`11-3_算法与管线/Q3/innov/out/` 的 **9 件 CSV**（`fig_q3_INV1_stepsize`／`INV2_e3`／`INV3_morris`／`INV3_samples`／`INV3_sobol`／`INV4_gci`／`INV4_uq_grid`／`INV4_uq_lhs`／`xchk_gt02`）**未被论文正文、规格卡与图表总规划引用** ⟹ 属**中间产物**，**不入支撑材料包**（保留于工作区）；包内 `innov_out/` 仍只放**被引用**的 Q4 十件。**未改动任何数值与已登记条目** |
