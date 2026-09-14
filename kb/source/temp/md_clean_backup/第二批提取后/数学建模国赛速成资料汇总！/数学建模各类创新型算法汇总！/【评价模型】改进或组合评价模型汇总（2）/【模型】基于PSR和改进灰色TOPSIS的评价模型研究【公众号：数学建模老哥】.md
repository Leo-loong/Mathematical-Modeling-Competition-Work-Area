<!-- 第 1 页 -->

### 中国电力
第 55 卷第 3 期 Vol. 55, No. 3

# 2022 年 3 月 ELECTRIC POWER Mar. 2022

## 基于PSR 和改进灰色TOPSIS 的

## 园区客户能效评估模型

#### 赵洪山，李静璇
(华北电力大学 电气与电子工程学院，河北 保定　071003)

> # 公众号：数学建模老哥
摘　要：为提升园区客户能效，在优化客户能效前需评估其能效水平，以寻找用能的薄弱环节。考虑能效
指标间的动态关系，基于压力-状态-响应(PSR) 模型从3 个维度选取评价指标，构建动态能效指标体系。结
合主成分分析和相关性分析优化能效评价指标体系，剔除体系中的冗余指标。构建改进灰色TOPSIS 能效
评估模型，引入熵权法计算指标的客观权重，利用加权灰色关联度代替欧式距离作为距离测度改进模型，
对园区客户能效水平进行综合评估，并从压力、状态和响应3 个子系统维度分析用能状况。通过对工业园
区10 个典型客户能效水平进行评估，分析可知响应性能较好的客户的综合能效评价结果较高，验证了
PSR 指标体系可行性。通过与其他方法评估结果对比验证了评估模型的有效性。
关键词：能效评估；PSR 模型；动态能效指标体系；主成分分析；灰色TOPSIS；熵权法
DOI：10.11930/j.issn.1004-9649.202010084

#### 0    引言分析了状态因素集、评语集、权重系数，建立了
基于模糊综合评价的电力能效评估模型。文献[10]
能源作为人类生存发展的重要资源，与社会利用直觉模糊熵法计算能效指标权重，并且结合

### [1]

的经济发展密切相关。近年来，国家积极推动超效率DEA 模型构建对电力用户进行能效评估。
社会用能效率的提升，缓解能源发展中存在的问文献[11] 根据热力学定律提出园区能效评价指
题。通过开展能效评估工作可以反映客户能效水平，标，利用加权有向图建立系统等效模型，并结合
同时推动客户根据评价指标体系改变原有用能信息熵确定指标权重对系统进行综合能效评价。

### [2-4]

行为，寻求能效优化方向，具有重要的现实意义。文献[12] 对电力用户大规模数据进行分析研究，
工业园区客户拥有数量庞大的能耗设备，用根据用电特征划分用户类别，针对电网用户提出
电负荷大且用能情况较为复杂，具备一定的能效能效评估体系，依据分类评估结果制定个性化用

### [5-7]

提升潜力。在对园区客户进行能效优化前，需能策略。文献[13] 基于OLAP 技术提出能效评估
要对其开展准确、有效的能效评估工作，定位用数据的预处理、初始化和分析模型，引入切片、
能薄弱环节，为提升能效水平提供参考方向。针切块、下钻和上卷数据分析方法，对电力客户的
对能效评估问题，国内外学者进行了不懈的努力能效进行评估。
和探索。文献[8] 针对综合能源系统输入输出指上述研究主要探究了能效评价指标体系的构
标特点，从环保、经济等方面构建评价指标体建和评价方法的选择，忽视了能效评价指标间的
系，基于交叉超效率CCR 模型提出能效评估模动态逻辑关系，指标体系维度有限，且缺少针对
型。文献[9] 构建了多层次能效评估指标体系，工业园区客户能效评估的完整流程，评估方法也
存在不足之处。本文针对工业园区客户群体，考
虑能效指标间的动态关系，基于压力-状态-响应
收稿日期：2020−10−26； 修回日期：2021−03−11。
（pressure-state-response, PSR）模型构建动态能效
基金项目：国家自然科学基金资助项目（冲击负荷下多源
谐波融合的涡簧储能用永磁同步电机系统主动协调控制，多维度评价指标体系，从3 个维度选取能效指
52077078）。标，并结合主成分（principal component analysis，

<!-- 第 2 页 -->

#### 中国电力第 55 卷

PCA）和相关性分析筛选冗余能效指标，建立筛将该模型应用于构建能效评估指标体系。园区客
选后的能效评价指标体系。在评估模型中引入熵户动态能效指标体系可以反映内、外部因素导致
权法，计算指标客观权重，并结合灰色关联度改用户在压力和状态维度的变化，体现客户用能质
进传统TOPSIS 评价方法，将灰色加权关联度作量和状况并反映客户不同程度的响应结果，避免
为距离测度，克服传统欧氏距离的评价缺陷，构指标选取局限性。外部因素体现为压力、响应，
建了园区客户动态能效评估模型。在算例中，对内部因素体现为状态，PSR 模型中子系统的功能
园区客户进行动态能效评估，根据评估结果分析关系如图2 所示。

> # 公众号：数学建模老哥
各客户在不同维度性能表现，验证构建指标体系
的合理性，并通过与其他评价方法所得的评估结
状态
果进行比较，验证了能效评估模型的适应性。
影响改善

#### 1    园区客户动态能效评价流程
减轻
压力响应
为全面了解工业园区客户用能状况，确定园
图 2   PSR 模型子系统关系
区客户动态能效水平综合评价流程，如图1 所
Fig. 2    Subsystem relationship of PSR model
示，主要包含以下环节。
选取能够对客户能效造成影响的压力因素作
为压力子系统指标。本文选取年总用电量作为压

|预处理<br>原始数据<br>指标计算<br>标准化|Col2|指标筛选<br>主成分分析<br>相关性分析|Col4|评估分析<br>整体能效评<br>子系统维度<br>能效分析|
|---|---|---|---|---|

力子系统指标。年总用电量P1 指用户在一年时间
内用电的总量。
状态子系统指标能反映在压力因素作用下，
客户实际的用能状况，可以有效反映电能质量对
图 1   园区客户能效水平综合评价流程客户能效水平产生的影响，本文选取以下5 个指
Fig. 1    Comprehensive energy efficiency evaluation 标作为状态指标。
process of park customers

#### （1）电压不合格累计时长S1，监测点电压在

#### （1）通过前期调研，根据客户用能特征，初监测期（一年）内超出合格范围的累计小时数。
步选取能效评价指标，计算相应指标数值并进行（2）电流不平衡率S2，专用变压器三相电流
数据预处理操作。的不对称程度为

#### （2）为保证指标体系具有代表性，依据筛选 S 2 = max{IA,IB,IC}
（1）
原则，剔除冗余能效指标，进一步优化能效指标 Iav
体系，建立最终的能效评价指标体系。式中：IA，IB，IC 分别表示A，B，C 相电流；

#### （3）选择合理的评价方法，建立能效评估模 Iav 表示三相平均电流。
型，评估客户综合能效水平，同时对子系统动态（3）平均负载率S3 为
能效表现进行评估分析，寻找影响客户用能水平 S 3 = S av
（2）
S TN
的关键因素。
式中：STN 为额定容量；Sav 为平均输出视在功率。

#### （4）功率因数S4，该指标可以反映变压器的

#### 2    基于PSR 模型的动态能效评价指标
运行效率。
PSR 模型根据压力、状态、响应间的动态逻 S 4 = P P
S = √ （3）
Q2 + P2
辑关系建立指标，具有综合性、灵活性，能够反
映系统中因果关系的动态变化，被广泛应用于研式中：P 表示有功功率；Q 表示无功功率。

### [14-15]

究复杂的环境系统中。结合电能使用背景，（5）平均电压S4 指在监测时间段内线路的

<!-- 第 3 页 -->
第 3 期赵洪山等：基于PSR 和改进灰色TOPSIS 的园区客户能效评估模型

平均电压，其中电压偏差范围为−3%～3%。标数据集间的协方差。R 为对称矩阵， rij = r ji 。

#### (2) (2)
响应指标反映客户改变原有用电习惯，使用 Z (:, i) 和Z  (:, j) 表示矩阵的第i 列和第j 列。
能向着健康的方向发展，可以呈现出的不同程度特征方程|R−λEm| = 0对应m 个特征根，将所
的响应结果。本文选取响应子系统指标如下。有特征根从大到小排序，依次对应第一主成分至
（1）万元产值能耗R1，客户每生产一万元价第m 主成分。一般前n(n＜m) 个主成分能够反映
值的产品所需要的电能。数据较多的信息量，通常只对这前n 个主成分进

#### （2）重要能耗设备能效等级R2，根据中国能行分析。本文中n 取2，即仅进行第一、第二主

> # 公众号：数学建模老哥
效标识将能耗设备能效划分为5 个等级，1 表示成分分析。
设备能效最好，5 表示能效最差求取前n 个特征根λj (j = 1,2, ···, n) 所对应的单
位特征向量 b j = [b1 j,··· ,bmj]T，由特征向量构建主

#### 3    基于PCA 和相关性分析的能效指标筛选成分分析矩阵为
 
b11 b12 ... b1n
b21 b22 ... b2n

## 3.1    指标筛选方法
B = ... ... ... ... （6）
能效评估指标应具有代表性。为避免指标包
bm1 bm2 ... bmn
含信息的冗余、重复，本文结合PCA 和相关性分
析，对PSR 动态能效指标体系进行筛选。PCA 将若与同列其他元素相比，bij 的绝对值较小，
原有变量进行重新组合，构成新的综合变量，避则表示该指标对整体的影响较小，可以剔除该指
免主成分所包含的信息重复，同时可以反映大部标。经筛选后构建最终能效评估矩阵为
[16-17]  z11 z12 ... z1q 
分原始变量的信息。通过相关分析，可以寻
z21 z22 ... z2q

### [7]

找指标体系中线性相关程度较高的变量。 Z = ... ... ... ... （7）
利用PCA 提取的第一和第二主成分能够包含 zm1 zm2 ... zmq
大部分信息，因此只需要计算第一和第二主成分
式中：q 为筛选后的指标数量，q≤n；m 为评估
的构成系数，并保留其中系数较大的主要指标，
对象数量。
删除主成分系数较小的次要指标，简化指标体
系。利用相关性分析计算各个评价指标间的相关

#### 4    基于改进灰色TOPSIS 园区客户能效
系数，相关系数大则表示两个指标线性相关性

#### 评估模型
高，应当删除相关冗余指标以避免信息重复。但
当相关分析与PCA 分析结果相反时，应以PCA 结
利用改进TOPSIS 模型综合评估工业园区客户
果为主。如果某一指标与多个指标线性相关，但
能效水平。首先进行数据预处理建立标准化评估
其在主成分的构成中占比很大，应在最终的评价
矩阵。基于第3 节中方法筛选指标，建立筛选后
指标体系中保留该指标。
的标准化评估矩阵。引入熵权法确定能效指标权

## 3.2    主成分分析
重，并结合灰色关联度改进传统TOPSIS 法，基
利用PCA 剔除指标体系中构成系数较小的指
于灰色TOPSIS 模型分析工业园区客户能效。
(2)
标。首先求取标准化后矩阵Z 的相关系数矩阵。

## 4.1    建立标准化评估矩阵
 
z11(2) z12(2) ... z1n(2) (1)
利用原始数据建立评估矩阵Z 为
z21(2) z22(2) ... z2n(2)
Z(2) =  

#### （4） z(1)11 z(1)12 ... z(1)1n
... ... ... ...
z(1)21 z(1)22 ... z(1)2n
Z(1) = （8）
zm1(2) zm2(2) ... zmn(2) ... ... ... ...
(2)
式中：z 为标准化后的指标值。 z(1)m1 z(1)m2 ... z(1)mn
ij
R = [rij]m×m （5）
式中：n 为初选能效评价指标个数；m 为被评估
(1)
式中：rij = cov(Z(2)(:;i),Z(2)(:; j))为第i 个和第j 个指的客户数量；Z ij 表示客户i 对应第j 个评价指标

<!-- 第 4 页 -->

#### 中国电力第 55 卷

的原始数值。 fij ln fij = 0。
在能效评估前对数据进行预处理，统一数据定义第j 个指标的熵权重为

### [18]

的类型和去量纲化。将PSR 能效指标划分为 1−H j
w j = （14）

# 3 类。效益型指标数值越大，表示客户能效水平 ∑q
q− H j
越高；成本型指标数值越小，表示客户能效水平
j=1
越高；区间型指标表示当指标数值在某一区间内
∑q
时，反映客户能效水平较高。为使后续数据处理式中： 0≤w j≤1, w j = 1。W = [w1,w2,··· ,wq]即为

> # 公众号：数学建模老哥
较为简洁，将指标类型统一为效益型。 j=1
指标权重向量。
效益型指标为

## 4.3    改进灰色TOPSIS 评估法
zij∗= zij(1) （9）
TOPSIS 法作为一种多目标决策综合评价方
成本型指标为法，依据正负理想解距离来评估排序评价对象的

### [22-26]

zij∗= maxz j −zij(1) （10）优劣性，能直观分析评估对象的整体情况。
但传统TOPSIS 法存在以下缺点。
设指标最佳区间为[a, b]，区间型指标为
 （1）传统TOPSIS 法利用欧式距离计算评估
a−z(1)
ij ,z(1)ij ＜a 客户到正负理想解的距离，如果不能考虑各评估
1−
M
指标之间的线性关系，欧氏距离会失效，影响评
zij∗= 1, a≤z(1)ij ≤b

#### （11）估结果的准确性。
z(1)ij −b
,z(1)ij ＞b （2）欧氏距离存在的缺陷导致传统TOPSIS
1−
M
{ {z j(1)} {z j(1)} } 法无法准确反映各方案的位置关系，可能存在方
M = max a−min ,max −b
案与正负理想解都接近的情况，不能完全反映各
式中：zij(1)为指标对应的原始数值；zij∗为转化成
评估对象能效水平的优劣。
效益型后的指标值。（3）本文从多维度建立了能效指标，需要分
统一指标类型后，根据式（12）进行标准化
析客户在不同维度的性能表现，而传统TOPSIS
处理，避免量纲不同对结果造成影响。
仅能获得最终的能效评估数值，无法满足分析子
/ vt m
∑ 系统性能的需求。
zij(2) = zij∗ zij∗2
（12）
为解决上述问题，本文通过改进模型来评估
i=1
工业园区客户能效。灰色关联度分析通过量化系
经数据预处理后，建立标准化能效评估矩阵

#### (2) 统变化态势来分析动态历程。灰色TOPSIS 改进
Z ，如式（4）所示。

## 4.2    熵权法计算指标权重评估模型将指标间加权灰色关联度作为距离测
确定指标权重时，为避免主观偏好对评价结度，代替原有的欧式距离测度。根据指标数据间
果造成影响，充分考虑指标数据间的客观差异，整体趋势的相似程度来评价各方案与正负理想解
本文引入熵权法客观量化指标的重要程度。赋权间的距离，可以反映评估方案之间的内部变化规
时，指标值变化较大则对应熵值越小，指标可以律，弥补欧式判据的不足，提高评估准确性。同
提供较大的信息量，因此对应的权重系数越时引入子系统维度分析环节，在获得综合能效评

### [19-21]

大。根据最终能效评估矩阵Z，如式（7），估结果的同时分析PSR 各维度性能的评估结果。
计算评估指标权重。改进灰色TOPSIS 园区客户能效评估步骤如下。
定义第j 个评估指标的熵为（1）经标准化及筛选处理，建立最终能效评
∑m 估矩阵Z，如式（7）所示。
Hij∗= −k fij ln fij, j = 1,2,··· ,q （13）
+ -

#### （2）计算正理想解Z 和负理想解Z 。在步
i=1
/ m 骤1 中评估指标类型均统一为效益型指标，因此
∑
式中： fij = zij zij,k = 1/lnm 。当 fi j = 0 时， + -
解Z 和Z 定义为
i=1

<!-- 第 5 页 -->
第 3 期赵洪山等：基于PSR 和改进灰色TOPSIS 的园区客户能效评估模型

maxzij=
{z1+,z2+,··· ,zq+} 表 1   初始PSR 能效评估体系
Z+ =
Table 1   Initial PSR energy efficiency evaluation system
j
minzij= 指标系统具体指标指标类型
{z1−,z2−,··· ,zq−}
Z−= （15）
压力指标年用电总量/(kW·h) 成本型
j
电压不合格累计时长/ h 成本型
式中： z1+,z2+,··· ,zq + 表示正理想方案指标值；
电流不平衡率/ % 成本型
z1−,z2−,··· ,zq− 表示负理想方案指标值。
状态指标平均负载率/ % 效益型

> # 公众号：数学建模老哥（3）计算客户i 与正、负理想解对应评价指
功率因数效益型
标j 的加权灰色关联系数γij +和γij−。
平均电压/ V 区间型
zij −z j++ρmax zij −z j+
mini min max –1
万元产值能耗/ ((kW·h)·万元 ) 成本型
γij+ = j i j 响应指标
zij −z j++ρmax zij −z j+
重要能耗设备能效等级成本型
max
i j
zij −z j−+ρmax zij −z j−
mini min max 表1 中定义平均电压指标的稳定区间为
γij−= j i j
zij −z j−+ρmax zij −z j− （16）
[374.2, 383.8]。
max
i j 对10 个用户在监测期内的相关数据进行正向
式中：ρ ∈[0,1]，称为分辨率系数，一般取 ρ = 0.5 化和去量纲化处理，获得客户标准能效指标数

#### （4）计算改进灰色TOPSIS 法的距离测度。据，如表2 所示。
定义改进后的距离测度为第i 个评估对象与正负对预处理后的能效指标数据进行主成分分
理想解的加权灰色关联度。析，计算指标在第一和第二主成分的构成系数，
∑q
S i+ = 寻找主成分系数较小的冗余指标，PCA 筛选结果
w jγ+
ij
如表3 所示。通过相关性分析，计算指标间的相
j=1
∑q 关系数值，寻找相关性程度高的能效指标，相关
S i−= w jγ− （17）
ij 性分析结果如图3 所示。
j=1
由表3 可知，功率因数在第一主成分和第二
式中：权重值w j由熵权法求得。
主成分的构成系数均较小(–0.009 9 和0.065 9)，其

#### （5）计算相对贴进度Di。
作为次要指标予以剔除。由图3 可知，电压不合
S +
Di = （18）格累计时长S1 和重要能耗设备能效等级R2 2 个指
S −+S +
标显著相关，相关系数为0.810（相关系数大于
式中：Di 越大代表该方案越贴近正理想解，即该

### 0.75），但由于这2 个指标在主成分的构成系数

客户能效水平越高。
较大，根据指标筛选原则，仍然予以保留。经指

#### （6）根据贴进度Di 对客户的能效评估结果
标筛选后构建最终的PSR 能效评价指标体系，该
进行排序比较。
体系共包含7 个能效指标，如图4 所示。

#### （7）子系统维度性能分析。基于步骤4 中各
根据筛选后得到的最终能效评估矩阵Z，采
子系统能效指标所对应的加权灰色关联度，计算
PSR 3 个子系统的相对贴进度值作为子系统评分。用熵权法计算能效指标权重，最终评估体系中各
指标的权重为W=[0.073 4, 0.081 3, 0.104 4, 0.327 8, 0.210 6,

#### 5    算例分析 0.100 2, 0.102 3]，平均负载率和平均电压2 个指标
所占权重较大，年用电量的权重值最小。

## 5.1    园区客户能效评价过程根据4.3 节中的改进灰色TOPSIS 评估法，计
针对某工业园区10 kV 工业专线用户的用能算各评价客户加权灰色关联系数、灰色距离测度
数据，对其中10 个用户进行能效评估分析。初及相对贴进度，并以相对贴进度值作为能效综合
选PSR 评价指标体系包括8 个指标，建立园区客评价结果，对客户能效水平进行排序，结果如表4
户初始PSR 能效评估体系，如表1 所示。所示。

<!-- 第 6 页 -->

#### 中国电力第 55 卷

表 2   标准化能效指标数据
Table 2   Standardized energy efficiency index data
压力(P) 状态(S) 响应(R)
客户
年用电量电压不合格累计时长电流不平衡率平均负载率功率因数平均电压万元产值能耗重要能耗设备能效等级
1 0.000 0 0.361 9 0.327 9 0.158 2 0.313 4 0.092 1 0.397 8 0.298 1
2 0.377 1 0.365 5 0.439 2 0.574 2 0.316 7 0.286 6 0.242 8 0.447 2
3 0.296 3 0.364 5 0.215 6 0.160 1 0.326 7 0.491 2 0.457 8 0.298 1

> # 公众号：数学建模老哥
4 0.210 7 0.354 1 0.238 0 0.456 3 0.330 0 0.046 1 0.395 0 0.149 1
5 0.248 9 0.319 7 0.508 7 0.448 7 0.323 4 0.450 3 0.374 4 0.298 1
6 0.356 7 0.372 5 0.407 5 0.224 3 0.323 4 0.491 2 0.383 5 0.447 2
7 0.379 6 0.000 0 0.124 7 0.249 1 0.313 4 0.087 0 0.289 0 0.000 0
8 0.371 9 0.135 9 0.299 6 0.244 4 0.326 7 0.000 0 0.143 1 0.149 1
9 0.366 2 0.372 3 0.000 0 0.135 0 0.263 4 0.450 3 0.161 1 0.447 2
10 0.346 3 0.281 3 0.257 4 0.140 7 0.320 0 0.107 5 0.000 0 0.298 1

表 3   能效指标主成分系数

|建<br>能效指标<br>压力状态响应<br>电<br>压<br>电万<br>年不平重要<br>流平元<br>用合均能耗<br>不均产<br>电格负设备<br>平电值<br>总累载能效<br>衡压能<br>量计率等级<br>率耗<br>时<br>长|Col2|Col3|
|---|---|---|
|压力<br>|压力<br>|压力<br>|
|年<br>用<br>电<br>总<br>量<br>|年<br>用<br>电<br>总<br>量<br>|年<br>用<br>电<br>总<br>量<br>|
|年<br>用<br>电<br>总<br>量<br>|年<br>用<br>电<br>总<br>量<br>|重要<br>能耗<br>设备<br>能效<br>等级<br>|

Table 3    Principal component coefficient of energy effi-
ciency index
主成分系数第一主成分第二主成分
年用电总量 –0.012 9 –0.235 9
电压不合格累计时长 0.384 2 0.028 4
电流不平衡率 0.228 4 0.569 8
平均负载率 0.102 5 0.630 7
功率因数 –0.009 9 0.065 9
平均电压 0.710 7 –0.292 5
万元产值能耗 0.237 1 0.324 3
重要能耗设备能效等级 0.477 6 –0.161 3
图 4   筛选后的能效指标体系
Fig. 4    Selected energy efficiency index system

### 1.00

P1 1.000 −0.353−0.204 0.066 −0.153 0.214 −0.499 0.050

## 0.75 现，结果如图5 所示。
S1 −0.353 1.000 0.259 0.113 −0.131 0.544 0.295 0.810

## 0.50 5.2    园区客户能效评价结果分析
S2 −0.204 0.259 1.000 0.566 0.634 0.128 0.271 0.253

## 0.25 对10 个客户的能效水平进行评价分析，由
能效指标S3 0.066 0.113 0.566 1.000 0.343 −0.034 0.218 0.010

# 0 表4 可知客户2 能效水平最高（0.666 5），客户
S4 −0.153−0.131 0.634 0.343 1.000 −0.282 0.329 −0.373

# 7 能效水平最低（0.410 7），客户综合能效排序
−0.25
S5 0.214 0.544 0.128 −0.034−0.282 1.000 0.345 0.690 为2＞5＞6＞3＞9＞4＞1＞10＞8＞7。根据图5，
−0.50
R1 −0.499 0.295 0.271 0.218 0.329 0.345 1.000 −0.034 对于客户2 其各子系统在所有客户中都达到很好
−0.75
R2 0.050 0.810 0.253 0.010 −0.373 0.690 −0.034 1.000 的性能，因此客户2 的综合能效水平优于其他
−1.00
P1 S1 S2 S3 S4 S5 R1 R2 9 个客户。客户2 在响应维度评分为0.624，产值
能效指标
能耗指标有待提高，为进一步优化其综合能效水
图 3   相关性分析热力图平，需要采取节能措施以优化其响应指标。因为
Fig. 3    Correlation analysis thermal diagram
响应子系统指标可以对压力和状态产生反馈，进
计算客户在压力、状态、响应各子系统的评而提升客户整体能效水平。对于客户7，其状态
分，分析客户在不同子系统维度的动态性能表维度评分仅为0.379，响应维度评分仅为0.390。

<!-- 第 7 页 -->
第 3 期赵洪山等：基于PSR 和改进灰色TOPSIS 的园区客户能效评估模型

表 4   灰色TOPSIS 评估结果状态因素反映客户电能质量状况，状态性能较好
Table 4    Grey TOPSIS evaluation results
会对客户的最终能效水平产生积极影响。外部因
正理想解灰色负理想解灰色相对贴进
客户 + – 排名素中，压力因素年用电总量对能效影响程度相对
距离测度S 距离测度S 度D
较小。而响应性能较好的客户都获得了较高的综

# 1 0.520 4 0.621 1 0.455 9 7
合能效评价结果，响应因素对能效影响较大，反

# 2 0.834 9 0.417 7 0.666 5 1
映出优化响应维度指标是提高客户能效水平科学

# 3 0.682 7 0.508 5 0.573 1 4
有效的措施，因为客户主要是通过各种节能技改

> # 公众号：数学建模老哥4 0.598 5 0.553 4 0.519 6 6
措施来提高能效水平。因此，客户对响应维度表

# 5 0.761 1 0.419 0 0.644 9 2
现应予以重视。同时，通过分析客户在压力、状

# 6 0.751 7 0.455 9 0.622 5 3
态、响应3 个维度性能，验证了基于PSR 模型的

# 7 0.470 5 0.675 1 0.410 7 10
园区客户动态能效指标体系具有科学性、合理性。

# 8 0.477 1 0.660 1 0.419 6 9
利用PSR 能效指标模型及改进灰色TOPSIS 评

# 9 0.636 0 0.581 2 0.522 5 5
价法，可以有效评估园区客户的整体能效水平，

# 10 0.482 7 0.653 0 0.425 0 8
同时反映客户在不同子系统维度的表现，寻找影
响客户用能水平的指标因素，为进行能效优化工

### 1.0

作提供参考方向。

## 0.9 压力；

## 0.8 状态； 5.3    模型适应性分析
响应

### 0.7

为分析改进灰色-TOPSIS 模型的适应性，根

### 0.6

评分据原始数据和指标的权重，采用不同评价方法对

### 0.5

## 0.4 客户能效进行评价，结果见表5。

### 0.3

## 0.2 表 5   不同评价方法结果对比

## 0.1 Table 5   Results of different evaluation methods
0

# 1 2 3 4 5 6 7 8 9 10 客户排名
客户名称评价方法

# 1 2 3 4 5 6 7 8 9 10

### [9]

图 5   园区客户子系统维度表现模糊评价法 7 1 4 6 2 3 10 9 5 8

### [19]

Fig. 5    Performance of park customers in subsystem 层次分析法 7 1 4 6 2 3 10 9 5 8
dimension [24]
TOPSIS法 7 1 5 6 2 3 10 9 4 8
其重要能耗设备能效等级最差，电压不合格时长改进灰色-TOPSIS 7 1 4 6 2 3 10 9 5 8
及电流不平衡率指标也较差。在10 个客户的状态根据3 个不同的模型评价结果分析，园区客
和响应子系统评分中最低，响应、状态性能表现户在不同评价模型中，其评估排序情况基本一
最差，因此该客户综合能效水平最低。考虑到子致，因此验证本文提出的新动态能效评估模型的
系统维度评分和指标权重，客户7 在状态和响应有效性。与传统TOPSIS 法相比较，客户3、9 的
维度仍有较大提升空间。对于客户6，其状态维能效排名略有差别，因为传统TOPSIS 法中当评
度表现与客户2 存在一定的差距，最终整体能效价对象距离正负理想解相近时，存在单一欧式距
水平排名位于第3，略低于客户2 的排名。但用离无法准确反映各方案位置的缺陷，而本文新模
户6 在响应维度评分达到0.684，与大多数客户相型中的改进加权灰色关联度测度距离能够准确反
比较，其响应能力较强。由于该客户具有较好的映各客户能效评估与最优方案间的测度关系，其
响应能力，其综合能效水平名次较高。评估结果准确度提高。在AHP 和模糊评价法中，
此外，由图5 可知10 个客户在压力、状态、评估较为依靠评价者的主观经验，评估客观性较
响应3 个维度的表现各不相同，各子系统评分结弱，缺少对指标细化分析，而本文提供的方法可
果对最终综合能效水平产生了不同的影响。内部以更加充分利用指标数据，不包含主观偏好因

<!-- 第 8 页 -->

#### 中国电力第 55 卷

素，提高了评估结果的客观性。同时相较于其他 Power Systems, 2015, 39(19): 1–8.
方法仅能获得最终能效评估排名，改进后的模型 [4] 鲁刚. 中国能源互联网发展基本特征[J]. 中国电力, 2018, 51(8):
能够感知客户在压力、状态、响应3 个不同维度 17–23.
的动态变化，获得各维度性能表现，对PSR 能效 LU  Gang.  Basic  characteristics  of  China's  energy  Internet
development[J]. Electric Power, 2018, 51(8): 17–23.
指标进行深入分析，评估结果更全面、细致。
[5] KONG L B, ZHAO J Y, LI J H, et al. Evaluating energy efficiency
improvement of pulp and paper production: case study from factory

#### 6    结语
> 公众号：数学建模老哥level[J]. Journal of Cleaner Production, 2020, 277: 124018.
[6] 王丹, 范孟华, 贾宏杰. 考虑用户舒适约束的家居温控负荷需求响
本文基于PSR 模型构建动态能效评价指标体
应和能效电厂建模[J].  中国电机工程学报,  2014,  34(13):
系，这种能效指标评价体系考虑了指标间的动态
2071–2077.
逻辑关系，提高园区客户智慧用能评估的全面性
WANG Dan, FAN Menghua, JIA Hongjie. User comfort constraint
和科学性。其次，本文结合PCA 和相关性分析
demand response for residential thermostatically-controlled loads and
法，剔除包含重复、冗余信息的能效指标，建立
efficient  power  plant  modeling[J].  Proceedings  of  the  CSEE,  2014,
筛选后的多维度动态能效评价指标体系。建立改
34(13): 2071–2077.
进灰色TOPSIS 评估模型，基于熵权法确定指标 [7] XU T, YOU J X, LI H, et al. Energy efficiency evaluation based on
客观权重，并引入灰色关联度加权距离测度改进 data  envelopment  analysis:  a  literature  review[J].  Energies,  2020,
原有欧式距离，可以反映各评估方案内部变化规 13(14): 3548.
律，弥补传统TOPSIS 法的缺陷。最后，通过算 [8] 李金良, 刘怀东, 王睿卓, 等. 基于交叉超效率CCR 模型的综合能
例分析，对园区客户进行动态能效评估，使客户源系统综合效率评价[J]. 电力系统自动化, 2020, 44(11): 78–86.
能够了解其总体能效水平以及在压力、状态、响 LI Jinliang, LIU Huaidong, WANG Ruizhuo, et al. Comprehensive
应3 个子系统维度的能效表现。分析可知客户 efficiency  evaluation  of  integrated  energy  system  based  on  cross-
super-efficiency  CCR  model[J].  Automation  of  Electric  Power

# 2 能效水平较高，客户7 能效水平较低。当客户
Systems, 2020, 44(11): 78–86.
在响应维度性能表现较好时，其综合能效评价结
[9] 吴剑飞, 姚建刚, 陈华林, 等. 电力客户能效状态模糊综合评估[J].
果较高。根据评估结果可以对关键用能设备、生
电力系统保护与控制, 2010, 38(13): 94–98,103.
产环节及用能习惯做出调整，为进一步优化能效
WU  Jianfei,  YAO  Jiangang,  CHEN  Hualin,  et al.  Fuzzy
水平提供参考依据，使电能使用朝着健康的方向
comprehensive  evaluation  of  power  customer  energy  efficiency
发展。
assessment[J]. Power System Protection and Control, 2010, 38(13):
94–98,103.

#### 参考文献：
[10] 卢锦玲, 黄金鹏, 杨行, 等. 基于改进超效率DEA 电力用户能效评
估模型[J]. 电力科学与工程, 2019, 35(9): 29–35.
[1] 邓建玲. 能源互联网的概念及发展模式[J]. 电力自动化设备, LU Jinling, HUANG Jinpeng, YANG Xing, et al. Improved energy
2016, 36(3): 1–5. efficiency evaluation model for DEA power users based on improved
DENG  Jianling.  Concept  of  energy  Internet  and  its  development efficiency[J]. Electric Power Science and Engineering, 2019, 35(9):
modes[J]. Electric Power Automation Equipment, 2016, 36(3): 1–5. 29–35.
[2] 龙涛, 别朝红. 面向终端能源互联网的能效优化调度[J]. 中国电 [11] 田立亭, 程林, 李荣, 等. 基于加权有向图的园区综合能源系统多场
力, 2019, 52(6): 2–10. 景能效评价方法[J]. 中国电机工程学报, 2019, 39(22): 6471–6483.
LONG Tao, BIE Zhaohong. Energy efficiency optimal dispatch for TIAN Liting, CHENG Lin, LI Rong, et al. A multi-scenario energy
terminal energy Internet[J]. Electric Power, 2019, 52(6): 2–10. efficiency evaluation method for district multi-energy systems based
[3] 孙宏斌, 郭庆来, 潘昭光. 能源互联网: 理念、架构与前沿展望[J]. on  weighted  directed  graph[J].  Proceedings  of  the  CSEE,  2019,
电力系统自动化, 2015, 39(19): 1–8. 39(22): 6471–6483.
SUN  Hongbin,  GUO  Qinglai,  PAN  Zhaoguang.  Energy  Internet: [12] 徐超. 大数据智能电网用户行为特征辨识与能效评估体系研
concept, architecture and frontier outlook[J]. Automation of Electric 究[D]. 北京: 华北电力大学(北京), 2017

<!-- 第 9 页 -->
第 3 期赵洪山等：基于PSR 和改进灰色TOPSIS 的园区客户能效评估模型

XU  Chao.  Research  on  big  data  smart  grid  user  behavior  feature ZHANG  Muyong,  HUO  Juan,  RUI  Xiaoming.  Fuzzy  reliability
recognition  and  energy  efficiency  evaluation  system[D].  Beijing: evaluation of wind turbines modified by entropy weights[J]. Electric
North China Electric Power University, 2017. Power, 2014, 47(5): 136–140.
[13] 许娟, 郭素平, 戴鸿昊, 等. 基于OLAP 技术的电力客户能效评估 [21] 刘庆时, 邹朋, 赵贺, 等. 智能用电小区综合用能评价[J]. 电测与仪
模型[J]. 沈阳工业大学学报, 2020, 42(5): 499–503. 表, 2016, 53(21): 59–64.
XU  Juan,  GUO  Suping,  DAI  Honghao,  et al.  Energy  efficiency LIU  Qingshi,  ZOU  Peng,  ZHAO  He,  et al.  Comprehensive  energy
evaluation model for power customers based on OLAP technology[J]. efficiency evaluation for smart power consumption communities[J].
> 公众号：数学建模老哥Journal  of  Shenyang  University  of  Technology,  2020,  42(5):
Electrical Measurement & Instrumentation, 2016, 53(21): 59–64.
499–503. [22] 马超. 配电网电能质量薄弱点评估[D]. 济南: 山东大学, 2020
[14] 宋琪, 文福拴, 王维洲, 等. 智能电网社会效益测评的压力—状态 MA  Chao.  Power  quality  weak  bus  evaluation  of  distributed
—响应模型[J]. 电力系统自动化, 2014, 38(2): 23–32. network[D]. Jinan: Shandong University, 2020.
SONG Qi, WEN Fushuan, WANG Weizhou, et al. Evaluating social [23] 吕志鹏, 吴鸣, 宋振浩, 等. 电能质量CRITIC-TOPSIS 综合评价方
welfare  of  smart  grid  development  in  pressure-state-response 法[J]. 电机与控制学报, 2020, 24(1): 137–144.
framework[J]. Automation of Electric Power Systems, 2014, 38(2): LÜ  Zhipeng,  WU  Ming,  SONG  Zhenhao,  et al.  Comprehensive
23–32. evaluation of power quality on CRITIC-TOPSIS method[J]. Electric
[15] ZHANG  D  D,  SHEN  J  Q,  LIU  P  F,  et al.  Allocation  of  flood Machines and Control, 2020, 24(1): 137–144.
drainage  rights  based  on  the  PSR  model  and  Pythagoras  fuzzy [24] 李慧玲, 芦新波, 刘大川, 等. 基于AHP-TOPSIS 的电力能效项目
TOPSIS method[J]. International Journal of Environmental Research 综合评价[J]. 现代电力, 2014, 31(4): 88–94.
and Public Health, 2020, 17(16): 5821. LI  Huiling,  LU  Xinbo,  LIU  Dachuan,  et al.  A  comprehensive
[16] 刘文慧, 徐遵义, 张旭冉, 等. 基于互信息和PCA 理论的湿法烟气 evaluation  method  for  power  energy  efficiency  project  based  on
脱硫工况特征提取方法[J]. 中国电力, 2020, 53(8): 158–163. AHP-TOPSIS[J]. Modern Electric Power, 2014, 31(4): 88–94.
LIU  Wenhui,  XU  Zunyi,  ZHANG  Xuran,  et al.  Feature  extraction [25] 曹华珍, 王天霖, 张黎明, 等. 基于组合赋权-TOPSIS 交直流配电网
method  for  wet  flue  gas  desulfurization  under  operating  conditions
能效评估[J]. 南方电网技术, 2021, 15(3): 55–67.
based  on  mutual  information  and  PCA  theory[J].  Electric  Power,
CAO  Huazhen,  WANG  Tianlin,  ZHANG  Liming,  et al.  Energy
2020, 53(8): 158–163.
efficiency  evaluation  of  AC/DC  distribution  network  based  on
[17] 曾博, 李英姿, 刘宗歧, 等. 基于均衡主成分分析的智能配电网环境
combined  weighting  TOPSIS[J].  Southern  Power  System
效益综合评价方法[J]. 电网技术, 2016, 40(2): 396–404.
Technology, 2021, 15(3): 55–67.
ZENG Bo, LI Yingzi, LIU Zongqi, et al. Comprehensive evaluation
[26] 王利利, 贾梦雨, 韩松, 等. 基于TOPSIS—灰色关联度的农网投资
method  for  environmental  benefits  of  smart  distribution  network
效益与风险能力综合评价[J]. 电力科学与技术学报, 2020, 35(4):
based  on  TO-PCA[J].  Power  System  Technology,  2016,  40(2):
76–83.
396–404.
[18] 孟金岭, 胡嘉骅, 文福拴, 等. 利用电参数的工业用户能效模糊综合 WANG Lili, JIA Mengyu, HAN Song, et al. Synthesized evaluation
评估[J]. 电力建设, 2016, 37(11): 16–22. of  investment  efficiency  and  risk  ability  of  rural  network  based  on
MENG  Jinling,  HU  Jiahua,  WEN  Fushuan,  et al.  Fuzzy TOPSIS-gray  incidence[J].  Journal  of  Electric  Power  Science  and
comprehensive  evaluation  for  energy  efficiency  of  industrial Technology, 2020, 35(4): 76–83.
consumers  employing  electric  parameters[J].  Electric  Power
作者简介：
Construction, 2016, 37(11): 16–22.
赵洪山（1965—），男，博士，教授，从事电力系统
[19] 贾乐刚, 杨军. 基于AHP-熵权法的电动汽车充电站运行能效评估
运行与控制、电力设备故障预测与优化运维等研究，
[J]. 电力建设, 2015, 36(7): 209–215.
E-mail：zhaohshcn@ncepu.edu.cn；
JIA  Legang,  YANG  Jun.  Running  energy  efficiency  assessment  in
李静璇（1996—），女，通信作者，硕士研究生，从
electric  vehicle  charging  station  based  on  AHP-entropy  method[J].
事能效评估与优化等研究，E-mail：lijingxuansd@163.
Electric Power Construction, 2015, 36(7): 209–215.
com。
[20] 张穆勇, 霍娟, 芮晓明. 基于熵权修正的风电机组可靠性模糊评价
方法[J]. 中国电力, 2014, 47(5): 136–140. （责任编辑　吴恒天）

<!-- 第 10 页 -->

#### 中国电力第 55 卷

Energy Efficiency Evaluation Model of Park Customers Based on PSR and

#### Improved Grey TOPSIS

#### ZHAO Hongshan, LI Jingxuan
(School of Electrical & Electronic Engineering, North China Electric Power University, Baoding 071003, China)

Abstract: In order to improve the energy efficiency level of park customers, it is necessary to evaluate the energy efficiency level of
customers to find out the weak links of energy consumption before energy efficiency optimization. Considering the logical dynamic

> # 公众号：数学建模老哥
relationship between energy efficiency indicators, the dynamic energy efficiency index system is constructed by selecting evaluation
indexes from three dimensions based on PSR model. Combining principal component analysis and correlation analysis, the index
system is optimized and redundant indexes are eliminated. An improved Grey TOPSIS energy efficiency evaluation model is
constructed where entropy weight method is introduced to calculate the objective weight of indexes. The weighted grey correlation
degree is used to replace the Euclidean distance as the distance measurement to evaluate the customers energy efficiency level, and
the energy consumption status is analyzed from three dimensions. Finally, the energy efficiency level of 10 typical park customers is
evaluated. The result shows that the comprehensive energy efficiency evaluation results of customers with good response
performance are higher, which verifies the feasibility of PSR index system. Compared with the results of other methods, the
effectiveness of the evaluation model is verified.
This work is supported by National Natural Science Foundation of China (Active Coordinated Control of PMSM System for Energy
Storage of Vortex Spring with Multi-source Harmonic Fusion Under Impact Load, No.52077078).
Keywords: energy efficiency evaluation; PSR model; dynamic energy efficiency index system; principal component analysis; Grey
TOPSIS; entropy weight method

(上接第194 页)

#### Experimental Study on Wind Acceleration Effect in Wind Farms

#### with Complex Terrain

# 1 2 2 3

#### YAN Xiaosheng , LI Yue , GAO Xiaoxia , WANG Xi
(1. Fujian Wind Power Co., Ltd., China Guodian Corporation, Fuzhou 350800, China; 2. School of Energy Power and Mechanical
Engineering, North China Electric Power University, Baoding 071003, China; 3. Hebei Longyuan
Wind Power Co., Ltd., Zhangjiakou 075000, China)

Abstract: Sloping land makes the speed of the inflow on the flat land increase after a certain height difference, which results in the
wind acceleration effect. Experiments were conducted in a mountain wind farm to obtain the flow field data of the slope wind field
and study the influence of slope terrain on the wind acceleration effect. Experimental results show that the acceleration effect is
related to the altitude of the slope, and the measured acceleration ratio at high altitudes is only about 16.9% of that predicted by
Taylor’s original algorithm. Moreover, both the slope and the wind direction are also factors affecting the acceleration effect.
Generally, the acceleration effect becomes more prominent when the slope is greater. In this experiment, the acceleration ratio in the
positions with a larger slope is increased by 61.6%, and the acceleration ratio on the crosswind side of the slope is about 10% larger
than that on the windward side. Meanwhile, the reasons for errors generated by Taylor’s original algorithm are analyzed, and the
modified formula of Taylor’s method suitable for complex terrain is proposed in this paper.
This work is supported by National Natural Youth Science Foundation of China (Theoretical and Experimental Studies on the 3D
Single and Wind Farm Wake Characteristics for Horizontal Wind Turbine, No.51606068), Natural Science Foundation of Hebei
Province  (Study  on  Collaborative  Control  Strategy  of  Wind  Farm  Under  the  Coupling  Action  of  Terrain  and  Wake  ,
No.E2019502072), and Fundamental Research Fund for the Central Universities (Study on the Internal Flow Mechanism of Wind
Farm Under the Coupling Action of Terrain and Wake, No.2020MS107).
Keywords: acceleration effect of sloping land; wind farm experiment; complex terrain; inflow conditions; Taylor algorithm
