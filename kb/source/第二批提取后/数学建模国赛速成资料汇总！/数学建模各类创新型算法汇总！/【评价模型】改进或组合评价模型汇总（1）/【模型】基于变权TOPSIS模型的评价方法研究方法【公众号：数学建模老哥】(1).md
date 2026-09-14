<!-- 第 1 页 -->
Vol. 43 No. 1 总第343 期
舰船电子工程

# 134 Ship Electronic Engineering 2023 年第1 期总第343期

## 基于变权TOPSIS 模型的围岩质量评价方法研究 ∗

#### 王凤山钱津
210007）
（陆军工程大学野战工程学院南京
摘要围岩质量评价是一个复杂的多目标风险决策问题。以反映围岩评价本质思想和关键概念为目标，选取了围岩
的抗压强度（单轴）、岩石质量指标、岩体完整性系数、地下水发育状态、岩体声波速度、结构面走向与洞轴线夹角6 个指标，

> # 公众号：数学建模老哥
运用均值化方法组合计算信息熵和变异系数法的指标权值，并结合TOPSIS法构建了围岩质量的评价模型；然后将该模型运
用到新疆克州布伦口－公格尔水电站地下洞室4个标段的围岩质量评价。研究表明，模型计算结果与现场实测数据基本吻
合，说明所建立的围岩质量变权TOPSIS评价模型能有效地得出合理理论。
围岩质量评价；变异系数法；熵值法；均值化；TOPSIS模型
关键词
E917 DOI：10. 3969/j. issn. 1672-9730. 2023. 01. 028
中图分类号

### Research on Evaluation Method of Surrounding Rock Quality

### Based on Variable Weight TOPSIS Model
WANG Fengshan QIAN Jin
（Field Engineering College，Army Engineering University of PLA，Nanjing 210007）
Abstract Surrounding rock quality evaluation is a complex multi - objective risk decision - making problem.To reflect the na⁃
ture of thought and the key concepts surrounding rock evaluation is the target，the selection of the surrounding rock uniaxial com⁃
pressive strength and rock quality index，integrity coefficient of rock mass，groundwater development status，the trend of the acous⁃
tic wave velocity of rock mass，the structural plane and the hole axis Angle of six indicators，information entropy are calculated by
using average method combination and variation coefficient method of index weights. Combined with TOPSIS method，the evaluation
model of surrounding rock quality is established. Then the model is applied to the surrounding rock quality evaluation of four under⁃
ground caverns of Bulunkou-Gongger Hydropower Station. The results show that the calculation results of the model are basically
consistent with the field measured data，which indicates that the variable weight TOPSIS evaluation model established for surround⁃
ing rock quality can effectively obtain a reasonable theory.
Key Words surrounding rock quality evaluation，coefficient of variation method，entropy value method，average method，
TOPSIS model
Class Number E917

#### 1 辨析围岩变形与破坏的衍化机理和致灾过程，

#### 引言

#### 是解析围岩质量评价所要解决的核心节点问题［2］，

#### 围岩作为支撑地下结构荷载的主要成分，其质全面考察影响围岩稳定性的多重要素，以期把握围

#### 量评价是工程界研究的热点问题［1］。围岩受岩体岩质量评价中的模糊性、随机性特征。以弥补常权

#### 决策的偏差为目标，变权TOPSIS 模型强调因素权

#### 结构面、受力状态、地应力环境及开挖扰动等因素

#### 重与因素状态值的联系、演变特征。集合TOPSIS［3］

#### 影响，易引起塌方、岩爆、涌水等工程灾害，有效把

#### 握围岩自然属性与工程特性，科学提取和分析围岩方法应用于围岩质量评价，寻求基于正、负理想方案

#### 质量评价指标，是围岩质量评价的关键事项。间的一致和妥协，以期提高决策结果的科学有效性。

∗ 收稿日期：2022年7月16日，修回日期：2022年8月21日
作者简介：王凤山，男，博士，教授，研究方向：防护工程系统建模与仿真。钱津，男，硕士，研究方向：工程建设与维护
管理。

<!-- 第 2 页 -->

# 2023 年第1 期 135
舰船电子工程

#### 2 交互机制和平衡作用，适应量化评估围岩质量仿真

#### 围岩质量影响因素概述

#### 推演的需要，从系统化角度建立影响围岩质量的结

#### 围岩有着稳定性的系统，但其同时还具有开放构、要素、介质的规范化描述［4］，实现了影响围岩质

#### 量要素及指标提取的一致性语义表达，如图1 所

#### 性，根据位置和时间的不同而变化，遵循地表、地下

#### 等外力作用下围岩地质体系统物质、能量和信息的示。

> # 公众号：数学建模老哥
图1
影响围岩质量要素描述

#### 图1 中，围岩质量评价要素在结构上反映评价
        - s11 s12 … s1n•

#### || ||

#### s21 s22 … s2n （1）

#### 模型的本质思想和关键概念，是考察围岩质量整体 Sm × n = || ||

#### | ⋮ ⋮ … ⋮ |

#### 作用体系的重要工具［5］。围岩稳定性受岩体质量、 | |
        - sm1 sm2 … smn•

#### 完整程度、地壳外力等多种内外因素的影响，对围式（1）中，i 表示评价方案数量，j 表示指标属性个

#### 岩质量评价要素的辨识和集合设计，目的是构建围

#### 数，sij 为第i 个方案第j 个指标值。

#### 岩质量评价模型的指标体系，为质量评价模型和系 2）采取极差法对围岩质量评估原始数据矩阵

#### 统分析建立基础，参考文献资料和行业规范［6］，选

#### Smn 进行标准化处理。结合式（2）、式（3）计算标准

#### 取6 个因素作为围岩稳定性评价的指标，分别为岩

#### 化矩阵S' 。

#### 石抗压强度（单轴）K1 、岩石质量指标K2 、岩体完

#### 围岩质量指标呈现效益型特征时：

#### 整性系数K3 、地下水发育状态K4 、岩体声波速度

#### sij - minj (sij)

#### ij = （2）

#### K5 以及结构面走向与洞轴线夹角K6 ，建立指标体 s'

#### max(sij) - minj (sij)

#### 系集合，K ={K1,K2，……Kn}，(1 ≤n ≤6) 。 j

#### 围岩质量指标呈现成本型特征时：

#### 3 指标权重计算 max(sij) - sij

#### ij = j （3）

#### s'

#### max(sij) - minj (sij)

#### 3.1 熵值法计算指标权重 j

#### 3）根据熵值计算方法（4），围岩质量第i 个要

#### 熵值法［7］以原始信息作为数据支撑，是一种度

#### 素指标下Si 的熵值为

#### 量无序程度的客观赋权方法。其中心思想是通过

#### ln(m)Σ1 m （4）

#### 监测各项指标的变异程度来测算出指标熵值的大 zi = - pij × ln(pij)

#### 小：熵值越大，反映出该指标信息的不确定性越大， i = 1

#### 式（4）中pui 表示围岩质量第i 项指标下，第m 个标

#### 包含的信息越小；反之，熵值越小，则该指标信息的

#### 段的特征比重，则：

#### 稳定性越好，相应包含的信息越大。

#### 1 + s'

#### 1）设对m 种方案si(1 ≤i ≤m) 构成围岩质量方 ij （5）

#### pij =

#### Σm

#### 案集合S ={si|1 ≤i ≤m 进行对比评价，结合n 项指} (1 + s'ij)
i = 1

#### 标属性构成m × n 原始数据矩阵，记作式（4）中，zi 表示围岩质量各指标要素的信息熵

#### Smn ={sij}m × n ，即为

#### 值，熵值越大，表示出围岩质量指标体系的整体稳

<!-- 第 3 页 -->

# 136 王凤山等：基于变权TOPSIS模型的围岩质量评价方法研究总第343期

#### 定性越差，权重越小。至此，计算围岩质量评估指且距离负理想解最远，则为最佳方案，反之最差［8］。

#### 但TOPSIS 方法［12］所采取的指标权重基本上是

#### 标的权重αi 为

#### 1 - Zi 由专家主观确定的，其客观准确度较低。因此运用

#### αi = （6）

#### Σn 均值化方法组合计算信息熵和变异系数法的指标

#### (1 - Zi)

#### i = 1 权值，取代了以专家经验主观上确定权重的方法，

#### 式（6）中，0 ≤αi ≤1，Σn 同时根据TOPSIS 法结合各指标属性的评价值［13］，

#### αi = 1。

#### i = 1 对最终的目标方案进行整体评价。

#### 3.2 变异系数法计算指标权重

#### 1）建立目标方案评价模型的决策矩阵并进行

#### 传统熵值法仅依赖于数据本身的离散性，在测相应的标准化处理，得到矩阵S ，如式（11）。

> # 公众号：数学建模老哥

#### 算权重时出现有的权重过大或过小的情况，对应指

#### 标数据为0 和1 时算出熵值均为0，很容易会造成 S =(sij)m × n =(yij/ Σm （11）

#### yij2)m × n

#### ［8］是衡量方案中各个 i = 1

#### 关键信息的丢失。变异系数 2）根据确定的各评价指标权重系数，构建加权

#### 属性值变异程度大小的统计值，变异系数法［9］则是

#### 标准决策矩阵U ，如式（12）。

#### 通过计算各属性在被评价对象上变异程度而得到（12）

#### U = （uij）m × n = ωj ·(sij)m × n

#### 权重的客观赋值方法。

#### 3）确定正理想值U + 和负理想值U - ，计算正、

#### 第一步：对第j 个被评价属性参数值求取均值

#### 负理想值，如式（13）、（14）。

#### sˉj 和标准差σj ：
      - {max1 ≤i ≤muij|j ∈J +,( min1 ≤i ≤muij|j ∈J -)}•

#### U + = （13）
    - sˉj = Σm • •

#### || sij m （1 ≤j ≤n） +,u2+,...un+}
      - {u1 •

#### i = 1 （7）

#### σj = Σm •{min1 ≤i ≤muij|j ∈J +,(max1 ≤i ≤muij|j ∈J -)}•

#### || (sij - sˉj)2 m （1 ≤j ≤n） U - = （14）
      - •
    - •{u1-,u2-,...un-} •
i = 1

#### 第二步：计算第j 个属性指标的变异程度γj ：式（13）、（14）中，J + 为效益型评价指标集，J - 为成

#### γj = σj/yˉj （1 ≤j ≤n）（8）

#### 本型评价指标集。

#### 4）求任一解yij 到正负理想解的距离Li+ 、

#### 第三步：计算出各项指标的权重βj ，通过对相

#### - ，如式（15）、（16）。

#### 应指标的变异程度进行“归一化”处理： Li

#### βj = γj/Σm （9） + = Σn （15）

#### γj （1 ≤j ≤n） Li (uij - uj+)2
i = 1 j = 1

#### 3.3 均值化计算指标权重

#### - = Σn （16）

#### Li (uij - uj-)2

#### 考虑不同单一赋权法间偏差值较大，利用熵值

#### 法和变异系数法分别确定围岩评价权重{ }αj 、{ } j = 1

#### βj 式（15）、（16）中，u+、u- 分别表示正负理想解

#### （1 ≤j ≤n），虽然消除了方案属性量纲的差异，但也的第j 个分量。

#### 5）计算各方案到理想解的贴近度Gi 。

#### 消除了各指标变异程度上的差异，因此，通过引入

#### ［10］对指标权重进行平衡处理，具体如下： - + Li （17）

#### 均值思想 Gi = Li-/(Li +)

#### ω ={ } （10）式（17）中，0 ≤Gi ≤1，i = 1,2,…,m 。

#### ωj (1 ≤j ≤n)
式（10）中，ωj = a · αj +(1 - a)βj ，本文取a = 0.5 。 6）根据相对贴近度Gi 对各个方案进行排序，

#### 选择贴近度最大的方案为较优方案。

#### 4 变权TOPSIS评价模型

#### 5 模型计算

#### TOPSIS 法［11］又叫逼近理想解的排序法，是经

#### 5.1 标准化决策矩阵

#### 典的多属性决策方法。其中心思想在于：对方案进

#### 以地下洞室内典型区域为例，根据文献［11］对

#### 行评价时，首先计算出最佳方案和最差方案，即：评

#### 4 个标段内围岩稳定性指标为例，给出围岩稳定性

#### 价问题的理想解和负理想解，然后利用欧式距离计

#### 算法求出各指标对象与正理想解和负理想解之间样本s1 、s2 、s3 、s4 的相关特征指标取值，构建地

#### 的贴近程度，进而通过与理想解的相对贴近度对方下洞室结构的围岩稳定性质量评价样本集，其量化

#### 参数如表1。

#### 案进行排序和评价，若评价对象距离正理想解最近

<!-- 第 4 页 -->

# 2023 年第1 期 137
舰船电子工程
表1 表4
围岩稳定性质量评价样本集评价方案到正、负理想解的距离
Rc RQD Kv A V θ 熵值法变异系数均值化
方案
K1 K2 K3 K4 K5 K6 L+ L- L+ L- L+ L-
α α β β ω ω
s1 127 81 0.68 47 5200 63 0 0.12 0 0.13 0 0.15
s1
s2 106 68 0.57 73 3500 54 0.06 0.07 0.06 0.07 0.07 0.09
s2
s3 78 51 0.62 112 2900 41 0.11 0.03 0.12 0.02 0.14 0.02
s3
s4 83 49 0.45 105 3200 32 0.11 0.01 0.12 0.01 0.13 0.01
s4

#### 建立方案决策矩阵Y ，利用式（11）对矩阵Y
表5
围岩质量评价方案贴近度

> # 进行规范化处理，则标准化矩阵S 表示如下：公众号：数学建模老哥
熵值法Gα 变异系数Gβ 均值化Gω
  - 0.6323 0.6367 0.5801 0.2665 0.6831 0.6433• 1 1 1
s1

#### ||||0.5278 0.5345 0.4862 0.4139 0.4598 0.5514||||

#### S = 0.5486 0.5541 0.5688

#### 0.3884 0.4009 0.5289 0.6350 0.3810 0.4187 s2
  - 0.4133 0.3851 0.3839 0.5953 0.4204 0.3268• s3 0.1857 0.1622 0.1290

#### 5.2 计算指标权重 s4 0.0859 0.0915 0.0958

#### 根据公式计算熵值法、变异系数法、均值化法 5.6 模型效果分析

#### 下的指标权重，具体如表2所示。根据表5 对围岩质量评价方案贴近度进行排
表2

#### 围岩质量评价指标权重序，熵值法、变异系数法与均值化下的方案贴近度

#### α β ω 排序一致，结果为s1 > s2 > s3 > s4 。数据显示，均值

## 0.17672 0.146468 0.16159

#### Rc 化作用后的围岩质量评价方案中，方案s2 的贴近

## 0.18779 0.155323 0.17155

#### RQD 度高于常权作用下的方案贴近度，且方案s3 、s4 的

## 0.13247 0.10758 0.12003
Kv

#### 贴近度更接近，对比工程实测数据更符合实际。通

## 0.17699 0.228176 0.20258
A

#### 过贴近度大小排序可以清晰得出方案s1 的围岩质

## 0.17516 0.177823 0.17649
V

#### 0.15089 0.184631 0.16776 量最好、稳定性最高，对比工程实测结果一致，表明
θ

#### 基于变权TOPSIS的围岩质量评价模型计算结果可

#### 表2 中，分别表示出三种方法下的指标权重

#### 靠，准确性较高，具有较好的应用价值。

#### α 、β 、ω ，并以此为数据支撑进行各方案正、负理

#### 6 结语

#### 想解求解。

#### 5.3 求解各方案正、负理想解

#### 1）针对围岩质量评价的多指标性，从系统化的

#### 依据式（13）~（14）依次求得各方案正、负理想

#### 角度提取影响围岩质量的各种因素，选取围岩单轴

#### 解，如表3所示。

#### 抗压强度、岩石质量指标、岩石完整性系数、地下水
表3
围岩质量评价方案正、负理想解

#### 发育状态、岩体声波速度、结构面走向与洞轴线夹

#### 熵值法变异系数均值化角作为评价指标，构建围岩质量评价模型［11］。

#### U + U - U + U - U + U - 2）在评价过程中，采用熵值法、变异系数法对
α α β β ω ω

## 0.11 0.07 0.09 0.06 0.08 0.05

#### Rc 评价指标进行均值化赋值，克服了单一赋权法中指

## 0.12 0.07 0.10 0.06 0.09 0.05
RQD

#### 标差异度较大、敏感性较强等特征对围岩质量评价

## 0.08 0.05 0.06 0.04 0.04 0.03
Kv

#### 结果的影响，增强了围岩质量评价模型的科学性、

## 0.05 0.11 0.06 0.14 0.08 0.19
A

#### 安全性。

## 0.12 0.07 0.12 0.07 0.12 0.07

#### V 3）以工程实例为数据支撑进行仿真计算，在围

## 0.12 0.06 0.12 0.06 0.13 0.06
θ

#### 岩现地指标测算值和方法算出组合权重值的基础

#### 5.4 计算到正负理想解的距离

#### 上，计算理性点贴近度与实例工程数据对比，结果

#### 依据式（15）~（16）依次求得各方案到正、负理

#### 表明基于变权TOPSIS的围岩质量评价模型得出的

#### 想解的距离，如表4所示。

#### 结论与实际结果一致，表明该方法、模型的合理可

#### 5.5 计算相对贴近度并排序

#### 行。

#### 根据式（17）依次求得各方案的相对贴近度

#### G ，如表5所示。（下转第191页）

<!-- 第 5 页 -->

# 2023 年第1 期 191
舰船电子工程
［6］戴干策，陈敏恒.化工流体力学［M］.北京：化学工业出版 rent distribution under free convection conditions［J］.
社，1988：10-15. Journal of the Electrochemical Society，2009，107（3）：
［7］Leblanc P，Paillat T，Cabaleiro J.Flow electrification inves⁃ 242-246.
tigated under the effect of the wall shearing stress ［14］Ferziger J H.Computational Methds for Fluid Dynamics
［C］//2016 Electrostatic Joint Conference，2016：154-162. ［M］.Washingon D.C：NBS，2012：20-25.
［8］Leblanc P，Cabaleiro J M，Paillat T，etal.Impact of the lam⁃ ［15］Tang A，Bao J，Skyllas-Kazacos M.Thermal modeling of
inar flow on the electrical double layer development［J］.
battery configuration and self-discharge reactions in va⁃
Journal of Electrostatics，2016（23）：1-5.
nadium redox flow battery［J］.Journal of Power Sources，
［9］Cabaleiro J，Paillat T，Moreau O. Modeling of static devel⁃
2012，216（5）：498-501.
opment and dynamic behavior of the electrical double lay⁃

> # 公众号：数学建模老哥［16］袁镒吾，刘又文.确定平板层流边界层速度分布的一种
er at oil pressboard interface［C］// Electrostatic Joint Con⁃
方法［J］.应用数学和力学，1999，20（4）：427-432.
ference，2009：254-268.
［17］陈涛，张国亮.化工传递过程基础［M］.第三版.北京：化
［10］Leblanc P，Paillat T，Cabaleiro J M，et al.Flow electrifica⁃
学工业出版社，2009：80-81.
tion investigated under the effect of the wall shearing
［18］Mohamed E A，Thierry P，Gerard T.Numerical simulation
stress［C］// 2016 Electrostatics Joint Conference，Proc，
of the electrical double layer development：physicochemi⁃
2016，12（3）：140-155.
cal model at the solid and dielectric liquid interface for
［11］Moreau O，Cabaleiro J，Paillat T，et al.Influence of the
laminar flow electrification phenomenon［J］.IEEE Trans⁃
wall shearing stress on flow electrification［C］// Interna⁃
tional Symposium on Thermal Plasmas Electrical Dis⁃ actions on Dielectrics and Electrical Insulation，2011，18
charges and Dielectric Material，Reunion Island，2016，2 （5）：1463-1475.
（14）：1145-1152. ［19］Sonke S，Kyosti K.Transient solutions of potential steps
［12］王红梅.对流扩散方程的特征有限元方法［D］.济南：山 at the rotating disc electrode with steady state initial con⁃
东大学，2012. centration profiles for one electron transfer reactions［J］.
［13］Kameo A，Fumio H，Shiro Y，et al.Mass transfer and cur⁃ Electrochemica Acta，2011，56（8）：6812-6823.
- ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••

#### （上接第137页）［6］建设部.工程岩体分级标准：GB50218-94［S］.北京：中国
计划出版社，1995.
［7］王凤山，杨志宏，郭子曜.基于改进熵权物元模型的作战
参考文献
方案评估［J］.指挥控制与仿真，2021，43（02）：82-90.
［1］穆成林，黄润秋，等.基于组合赋权—未确知测度理论的［8］王先明，姜枫，赵阳.基于变权理论TOPSIS 的空降场评
围岩稳定性评价［J］.岩土工程学报，2016，38（06）：估方法研究［J］.电子质量，2020，12（04）：5-8.
1057-1063. ［9］Polly P D .Variability in mammalian dentitions：size-relat⁃
［2］常晓林，张美丽，杨海云，等.基于联系熵的围岩稳定性 ed bias in the coefficient of variation［J］. Biological Jour⁃
评价研究［J］.岩土力学，2010，31（01）：99-101. nal of the Linnean Society，2010：64.
［3］王莉芳.基于组合赋权与灰色改进TOPSIS 方法的受灾［10］孙健，魏丽英.基于均值化主成分分析的交通安全评价
点应急物质需求紧迫性分级评价［J］.安全与环境工程，方法研究［J］.交通信息与安全，2012，30（01）：90-93，
2017，24（06）：94-100. 98.
［4］刘永，谭显坤，张航，等.椿树垭隧道岩体结构特征与围［11］曾韬睿，王林峰，翁其能.基于理想点法与组合赋权的
岩稳定性分析［J］.安全与环境工程，2010，17（05）：围岩质量评价模型［J］. 重庆理工大学学报（自然科
106-112. 学），2019（10）：79-85.
［5］Bao X ，Wang Z ，Ma S ，et al. Fine quality evaluation of ［12］王占武，唐凯，严良.基于熵权TOPSIS法的火电厂选址
surrounding rock of an underground hydropower station 综合决策［J］. 安全与环境工程，2011，18（05）：
［J］. E3S Web of Conferences，2020，194（5）：5041. 103-106.
