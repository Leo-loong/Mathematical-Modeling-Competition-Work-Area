<!-- 第 1 页 -->
第21 卷第6 期 安 全与环境学报 Vol．21 No．6

# 2021 年12 月 Journal of Safety and Environment Dec．，2021

Ｒesearch on site selection of maritime 文章编号: 1009-6094( 2021) 06-2443-09

#### transit pilot platform based on PCA- 基于改进的FAHP CＲITIC 法与云

#### relative entropy model 理论的露天矿边坡危险性评估模型*
XU Xiao-feng，XIAO Ying-jie，ZHANG Xue-lai，XU Ya-wei 1，2，王黎蝶1，2

#### 侯克鹏
( College of Merchant Shipping，Shanghai Maritime University，
( 1 昆明理工大学国土资源工程学院，昆明650000;
Shanghai 201306，China)

# 2 云南省中德蓝色矿山与特殊地下空间
开发利用重点实验室，昆明650000)
Abstract: In view of the site selection problem of offshore transit
platforms，a platform evaluation system is established，consider-公众号：数学建模老哥
摘 要: 针对传统评估方法无法同时解决露天矿边坡危险性
ing natural factors，water factors，economic factors，convenience 评估中存在的不确定性和模糊性问题，提出了基于改进
factors，and other constraints．The same trend is normalized． FAHP CＲITIC 法博弈赋权与正态云模型的边坡危险性评估
Principal Component Analysis ( PCA) is introduced to calculate 方法。选取地质、工程、水文条件等多方面因素构建综合评
the weight of the index by using the original index information 价指标体系，首先采用改进FAHP 法和CＲITIC 法分别确定
and mathematical model．According to the projection of the origi- 主、客观权重; 进而通过博弈论模型确定最优综合权重; 然后
nal data in the multi-dimensional space，the original indicators 结合云模型计算各指标的不同等级隶属度，求出不同边坡隶
are combined into a new set of linearly independent comprehen- 属于不同危险等级的综合确定度，由最大隶属度原则划分边
坡的危险性等级。将该模型运用于某露天铜矿边坡危险性
sive indicators，and the weight is calculated according to the cu-
评估，其评估结果与实际情况相符，表明该方法是科学可行
mulative variance contribution rate of each principal component．
的，并与其他方法的评估结果进行对比分析，分析结果进一
The index weights calculated by mathematical models have strong
步证明了该评估模型的可靠性。
objectivity，minimizing the impact of human subjective factors on
关键词: 安全工程; 改进的FAHP 法; CＲITIC 法; 博弈论; 云模
site selection．The concept of relative entropy is used to sort the
型; 综合确定度
evaluation system and obtain the best scheme．Four more suit-
中图分类号: X936 文献标志码: A
able addresses in the channel are selected as alternatives and
DOI: 10. 13637 /j．issn．1009-6094. 2020. 1302
substituted into the model for calculation．According to the ex-
perimental results，the fitting degree ranking result of the method 0 引 言
presented in this paper is T2 ＞T1 ＞T3 ＞T4．As a result，scheme

#### 多年来，我国的露天矿边坡滑坡事故居高不下，
2 is the best address of the offshore transit platform．The above

#### 死亡率居安全总事故首位［1］。因此，对露天矿边坡
evaluation model for offshore transit platform site selection is an

#### 进行危险性评估已是必不可少的环节。很多专家对
objective evaluation method entirely based on index data of influ-

#### 此进行了深入的研究并提出多种理论来探讨边坡的
encing factors．To verify the rationality of the selected method，

#### 危险性，如混沌理论［2］、模糊理论［3］、随机理论［4］、
five pilot station experts are invited to conduct on-site inspections

#### 突变理论［5］、灰色系统理论［6］等。
on the offshore transit platform site selection based on experi-

#### 造成边坡失稳的因素、评估标准和影响因子权
ence．The subjective scores based on various considerations are
4. 2，4. 7，4. 1，3. 5. That is，under expert judgment，scheme 2 重的模糊性使得对边坡危险性等级的划分蕴藏着各

#### 种不确定性［7］。云模型由模糊集理论发展而来，并
is the best selection for the offshore transit platform．It is consist-
ent with the calculation results of the site selection evaluation 于1995 年由李德毅等［8］首次提出，综合了正态分布
model，which verifies the rationality of the method used in this 和钟形隶属函数，能很好地进行定性描述到定量数
paper．It has opened up a new mode for ship pilotage work and 值的不确定转换，同时兼顾了模糊性和随机性，具有
has certain guiding significance for the development of pilotage

#### work． *
收稿日期: 2020 09 21
Key words: safety engineering; site selection; principal compo- 作者简介: 侯克鹏，教授，博士生导师，从事边坡工程与岩
nent analysis; relative entropy; maritime pilot-age 石力学研究，496172617@ qq．com; 王黎蝶( 通
transfer platform 信作者) ，博士研究生，从事边坡工程研究，
CLC number: X951 Document code: A 601419470@ qq．com。
Article ID: 1009-6094( 2021) 06-2438-06 基金项目: 国家自然科学基金项目( 51964023)

<!-- 第 2 页 -->
Vol．21 No．6 安全与环境学 报 第21 卷第6 期

#### 一定的普适性，为边坡危险性评估提供了一种可行 条件、人类活动四个方面，选取岩石质量指标x1、岩

#### 性方法。合理的指标权重是进行正确评估的前提， 体结构特征x2、黏聚力x3、内摩擦角x4、地应力x5、

#### 为解决单一赋权法过于偏主观或客观的问题，陈家 容重x6、坡高x7、坡度x8、年平均降雨量x9、地震烈

#### 良［9］于2003 第一次提出了博弈论组合赋权法，为最 度x10、人类活动x11 来构建露天矿山边坡的危险性

#### 优综合权重的求取开辟了一条新途径。2009 年，周 评估指标体系。参照露天矿边坡工程的相关规

#### 建国等［10］首次构建了博弈改进云模型的综合评价 范［17］和工程岩体的分级标准［18］，并借鉴相关学者对

#### 法。方前程等［11］在此基础上建立了基于博弈论和 边坡稳定性或危险性评估指标的分类标准［11 16，19］，将

#### 云模型的边坡稳定性分级方法，但其采用三标度的 边坡危险性划分为Ⅰ、Ⅱ、Ⅲ、Ⅳ、Ⅴ五个等级，各等级的

#### AHP 法和熵权法分别确定主、客观权重，前者忽略 危险性分别为极低、低、较高、高、极高。边坡危险性

# 了主观模糊性，且检测判断矩阵一致性标准( CＲ＜公众号：数学建模老哥评估指标及其等级划分标准见表1。

#### 0. 1) 的科学依据不充分，后者只考虑指标值的信息

#### 2 指标权重确定

#### 量而忽略了指标的相关性，因此也存在不足。

#### 本文采用改进的Fuzzy Analytic Hierarchy 2. 1 基于改进FAHP 法的主观赋权
Process( 简称FAHP) 法计算主观权重，专家们通过 20 世纪70 年代，Saaty［20］首次提出了AHP 法，该

#### 三值判断( 最低可能值、最可能值、最高可能值) 打 法简洁实用，是一种定性定量相结合的系统性决策方

#### 分法来构造模糊判断矩阵，并引入三角模糊函数算 法。1965 年，Zadeh［21］最先提出了Dev 模糊集和三角

#### 法，模糊算法能根据人的心理特点建立模型，更符合 模糊数的概念，可将不确定性语言转化为定量数值，

#### 人的思维，可以增加主观权重的准确性。采用Crite- 为处理模糊性问题奠定了基础。后来相关研究者将
ria Importance Though Intercrieria Correlation ( 简称 模糊数用于AHP 法中，不仅将模糊法和层次分析法

#### CＲITIC) 法计算客观权重，其基于评价因素间的对比 的优势结合起来，还解决了传统AHP 法需要对判断

#### 强度和冲突性来综合衡量指标权重，是一种比熵权法 矩阵反复进行一致性检验的缺陷［22 24］。本文选用改

#### 和标准离散法更好的客观赋权法。在此基础上，采用 进的FAHP 法确定主观权重，在建立判断矩阵时，为

#### 博弈论算法求出最优综合权重。最后建立基于博弈 避免评判太绝对，专家们采用三值判断法来打分，得

#### 论和云模型的露天边坡危险性综合评估模型。 到模糊判断矩阵，并引入三角模糊函数进行计算，将

#### 模糊法与AHP 法的优势结合起来。计算过程和处理

#### 1 评估指标体系的构建

#### 方法如下。

#### 边坡的各种影响因素相互制约相互关联，使得 如图1 所示，三角模糊数A 一般表示为( l，m，

#### 其危险性评估成为一项复杂的系统工程，建立一个 u) 。在论域U 中，如果存在μA( x) : U→［0，1］，则称

#### 全面、系统、合理的评价指标体系是正确评估的基 μA( x) 为x∈A 的隶属度。其中m 为A 的隶属度为1

#### 础，科学可行性、唯一性、主导性、目的性、综合性等 的中值，当x = m 时，x 完全属于A; l 和u 分别为下界

#### 是评价指标体系构建过程中必须遵循的原则。本文 和上界，在l、u 之外的完全不属于模糊数A。

#### ［11 16］，经整理和总结，分 2. 1. 1 模糊判断矩阵构造

#### 结合相关规范及参考文献

#### 1) 假设有n 个评判专家对所有指标进行两两比

#### 别从地质环境特征、边坡几何条件、水文因素和工程

表1 评价指标及其分级
Table 1 Evaluation indicators and their classification
地质环境特征 边坡几何条件 水文因素和工程条件 人类活动
危险性
x1 / x2 / x3 / x4 / x5 / x6 / x7 / x8 / x9 / x10 / x11 /
等级
% % MPa ( °) MPa ( kN·m －3) m ( °) mm 度 %
Ⅰ级［90，100)［90，100)［0. 3，0. 5］［35，45］［0，2) ［35，45］［0，30) ( 0，15) ［0，300) ［0，3) ［0，20) ( 无)
Ⅱ级 ［70，90) ［70，90) ［0. 2，0. 3)［27，35) ［2，8) ［27，35) ［30，45) ［15，30) ［300，500) ［3，5) ［20，40) ( 较弱)
Ⅲ级 ［50，70) ［50，70) ［0. 1，0. 2)［18，27) ［8，14) ［19，27) ［45，60) ［30，45) ［500，800) ［5，7) ［40，60) ( 弱)
Ⅳ级 ［25，50) ［30 ，50)［0. 05，0. 1)［12，18) ［14，20) ［13，19) ［60，80) ［45，60) ［800，1 000) ［7，8) ［60，80) ( 较强)
Ⅴ级 ( 0，25) ( 0，30) ( 0，0. 05) ( 0，12) ［20，25］( 0，13) ［80，100］［60，90) ［1 000，1 500］［8，12］［80，100］( 很强)

<!-- 第 3 页 -->
2021 年12 月 侯克鹏，等: 基于改进的FAHP CＲITIC 法与云理论的露天矿边坡危险性评估模型 Dec．，2021

#### ν( A ≥A1，A2，…，An) = min( A ≥Ai)

#### i = 1，2，…，n ( 8)

#### 在采用改进的FAHP 法确定权重时，当某个指

#### 标的权重较小时，会出现权重为0 的现象，虽不会影

#### 响最终的评估结果，但会导致主观权重的精确度降

#### 低，且与使用传统AHP 法求得的主观权重差距过

#### 大。为解决这一问题，对式( 8) 进行修正，得到式

#### ( 9) ，即将最小可能度( 0 除外) 作为这个模糊数的初

#### 始权重。

# 公众号：数学建模老哥图1 三角模糊数的几何模型

#### v( A ≥A1，A2，…，An) = min( A ≥
Fig．1 Geometric model of triangular fuzzy numbers

#### Ai ≠0) i = 1，2，…，n ( 9)

#### 较，则得到一列模糊数，分别为( l1，m1，u1) ，( l2，m2， 3) 标准化处理初始权重，得到最终权重。

#### u2) ，…，( ln，mn，un) 。 2. 2 基于CＲITIC 法的客观赋权

#### 2) 由式( 1) 整合模糊数，使每两个指标比较后 相比于熵权法只考虑指标值的信息量而忽略了

#### 得到一个模糊数。并重复以上步骤，直到判断矩阵 指标间的相关性，CＲITIC 法根据评价指标之间的对

#### 中任意两个指标比较后均为一个模糊数为止。

#### 比强度和冲突性来综合确定指标权重，同时考虑了

#### ( )

#### l1 + l2 + … + ln，m1 + m2 + … + mn，u1 + u2 + … + un

#### 指标间的差异性和相关性，是一种更加科学的客观

#### n n n

#### 赋权方法［7，25 26］。具体计算步骤如下。

#### ( 1)

#### 1) 分别按式( 10) 和( 11) 对益稳型和逆稳型指

#### 2. 1. 2 各指标的模糊三值权重确定

#### 标进行处理，得到标准化矩阵。

#### 按式( 2) ～( 4) 处理A1( l1，m1，u1) 、A2( l2，m2，

#### xij －xi－min

#### u2) ，由式( 5) 计算指标的模糊三值权重。 mij = ( 10)

#### xi－max －xi－min

#### A1 + A2 = ( l1 + l2，m1 + m2，u1 + u2) ( 2)

#### xi－max －xij

#### A1 ⊗A2 = ( l1l2，m1m2，u1u2) ( 3) mij = ( 11)

#### xi－max －xi－min

#### ( )

#### 1 1l ，1m ，1

#### A = ( 4) 确定指标的标准差

#### u
n n n n －

#### Pxi = Σ aij ÷ Σ( ) Σ i = 1( mij －mj) 2

#### i = 1 Σ a i，j = 1，2，…，n

## ij σj = • ( 12)

#### j = 1 j = 1 n － 1

#### ( 5) n

#### － j = 1

#### m n Σ mij ( 13)

#### 式中 aij表示第i 个指标与第j 个指标进行重要度
i = 1

#### 比较所得的模糊数。 3) 确定指标冲突性。

#### 2. 1. 3 最终权重确定 n

#### Ｒj = Σ ( 1 －rij) ( 14)

#### 1) A1( l1，m1，u1) 、A2( l2，m2，u2) 是三角模糊
i = 1

#### 数，A1 ≥A2 的可能度用三角模糊函数定义为 n － －

#### Σ ( mi －m) ( mj －m)

#### v( A1 ≥A2) = supx≥y［min( μA1( x) ，μA2( y) ) ］

#### rij = i，j = 1 ( 15)

#### ( 6) n － n －

#### Σ ( mi －m) 2Σ ( mj －m) 2

#### 1 m1≥m2 i = 1 j = 1

####  4) 计算信息量。

#### l2 －l1

#### v( A1≥A2) =  m1≤m2，u1≥l2

#### ( m1 －u1) －( m2 －l2) cj = σjＲj ( 16)

#### 

####  5) 对cj进行归一化处理，得客观权重。

#### 0 其他情况

#### ( 7) 2. 3 基于博弈论最优综合权重的确定

#### 2) 一个模糊数大于其他( n －1) 个模糊数的可 基于博弈论组合赋权，同时考虑主、客观权重，

#### 能度定义为 通过各权重间的偏差最小化，使其相互竞争又协调

<!-- 第 4 页 -->
Vol．21 No．6 安全与环境学 报 第21 卷第6 期

#### 一致［27］。具体计算步骤如下。

#### 3 基于改进FAHP CＲITIC 法博弈赋权的

#### 1) 建立基本权重向量集。若由m 种方法确定n

#### 云模型理论

#### 个指标的权重，得到m 组指标权重为wi = ( wi1，wi2，

#### …，win) ( i = 1，2，…，m) ，由此得到一个权重集w = 3. 1 云模型理论

#### T( j = 1，2，…，n) 。 云模型的概念常用3 个云特征参数来表示，即

#### ( wij，w2j，…，wmj)

#### Ex、En、He。其中期望Ex 代表论域的中心值; 熵En

#### 2) 确定最优综合权重。对m 组权向量进行任

#### 用来度量定性概念的不确定性，概念模糊度随En 增
m

#### 意线性组合为w = Σi = 1 αiwTi ( αi ＞0) ，对αi 进行优

#### 大而增大; 超熵He 表示熵的不确定及云滴的凝聚程

#### 度，He 越大，云层越厚［7］。由正向云发生器生成的
m

#### 化使w 和wi 的离差极小化，即minΣi = 1 αiwTi －wi( i =

# 公众号：数学建模老哥云滴来构建边坡危险性评价云模型的步骤如下。

#### 1) 根据表1 和式( 19) ［16］计算各指标不同等级

#### 1，2，…，m) ，由矩阵的微分性质导出该式的最优一

#### 下的云特征参数( Exij，Enij，Heij) ，结果见表2。

#### 阶导数为

#### Exij = a1ij + a2

####  w1wT w1wT … w1wT   α1   w1wT  ij

#### 1 2 m m 

####       2

#### T T T T 

####  w2w w2w … w2w   α2   w2w 

#### 1 2 m = m Enij = a1ij －a2 ( 19)

####       ij

####   ⋱    

####       2. 335

#### 

#### wmwT wmwT … wmwT α wmwT Heij = k

# 1 2 m m m

#### ( 17) 式中 a1ij 、a2ij 分别为指标在相应等级标准的上下

#### 由式( 17) 求得( α1，α2，…，αm) ，归一化处理后 限值; k 为常数，可根据评语模糊程度进行调整，本

#### 得到权重最优分配比系数α*i ; 通过式( 18) ，求得最 文k 取0. 01。

#### * 。 2) 借助Matlab 软件，由表2 的云特征参数和边

#### 优综合权重w

#### 坡实测数据进行隶属度计算，并生成指标云图，具体
m

#### * = Σ * T 算法见图2［28］。

#### w i = 1 αi w ( 18)
i

表2 不同等级下各指标的云特征参数
Table 2 Cloud characteristic parameters of each index at different levels
评估标准
指标
Ⅰ级 Ⅱ级 Ⅲ级 Ⅳ级 Ⅴ级
x1 ( 95，4. 283，0. 01) ( 80，8. 565，0. 01) ( 60，8. 565，0. 01) ( 37. 5，0. 707，0. 01) ( 12. 5，10. 707，0. 01)
x2 ( 95，4. 283，0. 01) ( 80，8. 565，0. 01) ( 60，8. 565，0. 01) ( 40，8. 565，0. 01) ( 15，12. 848，0. 01)
x3 ( 0. 4，0. 086，0. 01) ( 0. 25，0. 043，0. 01) ( 0. 15，0. 043，0. 01) ( 0. 075，0. 021，0. 01) ( 0. 025，0. 021，0. 01)
x4 ( 40，4. 283，0. 01) ( 31，3. 426，0. 01) ( 22. 5，3. 854，0. 01) ( 15，2. 570，0. 01) ( 6，5. 139，0. 01)
x5 ( 1，0. 857，0. 01) ( 5，2. 570，0. 01) ( 11，2. 570，0. 01) ( 17，2. 570，0. 01) ( 22. 5，2. 141，0. 01)
x6 ( 40，4. 283，0. 01) ( 31，3. 426，0. 01) ( 23，3. 426，0. 01) ( 16，2. 570，0. 01) ( 6. 5，5. 570，0. 01)
x7 ( 15，12. 848，0. 01) ( 37. 5，6. 424，0. 01) ( 52. 5，6. 424，0. 01) ( 70，8. 565，0. 01) ( 90，8. 565，0. 01)
x8 ( 7. 5，6. 424，0. 01) ( 62. 5，6. 424，0. 01) ( 37. 5，6. 424，0. 01) ( 52. 5，6. 424，0. 01) ( 75，12. 848，0. 01)
x9 ( 150，128. 48，0. 01) ( 400，85. 653，0. 01) ( 650，128. 48，0. 01) ( 900，85. 653，0. 01) ( 1250，214. 133，0. 01)
x10 ( 1. 5，1. 285，0. 01) ( 4，0. 857，0. 01) ( 6，0. 857，0. 01) ( 7. 5，0. 428，0. 01) ( 10，1. 713，0. 01)
x11 ( 90，8. 565，0. 01) ( 70，8. 565，0. 01) ( 50，8. 565，0. 01) ( 30，8. 565，0. 01) ( 10，8. 565，0. 01)

<!-- 第 5 页 -->
2021 年12 月 侯克鹏，等: 基于改进的FAHP CＲITIC 法与云理论的露天矿边坡危险性评估模型 Dec．，2021

#### 3. 2 综合确定度计算和边坡危险性等级判断

#### 4 实例分析

#### 1) 根据已求得的最优综合权重w*i 和各边坡各

#### 评价指标不同等级隶属度μ( xik) ，由式( 20) 计算边 为验证基于改进FAHP CＲITIC 博弈组合赋权法

#### 坡危险性等级的综合确定度Dk。 的云模型评估边坡危险性的可行性，运用该模型对云

#### n 南某露天铜矿的3 个边坡进行危险性评估。各边坡的

#### Dk = Σi = 1 μ( xik) w* ( 20)

#### i 评价指标实测值见表3，该评估模型的计算流程见图3。

#### 式中 n 为评价指标数，k 为评价等级，w*i 为各指标 4. 1 指标权重的计算

#### 的最优综合权重，μ( xik) 为第i 个指标对第k 个等 4. 1. 1 基于改进FAHP 法的指标主观权重计算

#### 级的隶属度。 1) 专家们采用三值判断法对各指标进行两两

# 公众号：数学建模老哥2) 根据最大确定度，判断边坡危险性等级V。 比较，得到初级模糊判断矩阵。经过式( 1) 处理

#### V = max( Dk) k = 1，2，3，4，5 ( 21) 后，可得模糊判断矩阵A。
 ( 1，1，1) ( 1，2，3) ( 1，2，3) ( 3，4，5) ( 1 /3，1 /2，1) ( 1，2，3) ( 1，2，3) ( 3，4，5) ( 3，4，5) ( 2，3，4) ( 2，3，4) 
 ( 1 /3，1 /2，1) ( 1，1，1) ( 1 /2，1，1) ( 2，3，4) ( 1 /4，1 /3，1 /2) ( 1 /2，1，1) ( 1，1，2) ( 2，3，4) ( 2，3，4) ( 1，2，3) ( 1，2，3) 
 ( 1 /3，1 /2，1) ( 1，1，2) ( 1，1，1) ( 2，3，4) ( 1 /4，1 /3，1 /2) ( 1，1，2) ( 1 /2，1，1) ( 2，3，4) ( 2，3，4) ( 1，2，3) ( 1，2，3) 
 ( 1 /5，1 /4，1 /3) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1，1，1) ( 1 /7，1 /6，1 /5) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1 /2，1，1) ( 1，1，2) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1) 
 ( 1，2，3) ( 2，3，4) ( 2，3，4) ( 5，6，7) ( 1，1，1) ( 2，3，4) ( 2，3，4) ( 5，6，7) ( 5，6，7) ( 4，5，6) ( 1 /3，1 /2，1) 
A =  ( 1 /3，1 /2，1) ( 1，1，2) ( 1 /2，1，1) ( 2，3，4) ( 1 /4，1 /3，1 /2) ( 1，1，1) ( 1，1，2) ( 2，3，4) ( 2，3，4) ( 1，2，3) ( 1，2，3) 

####  
( 1 /3，1 /2，1) ( 1 /2，1，1) ( 1，1，2) ( 2，3，4) ( 1 /4，1 /3，1 /2) ( 1 /2，1，1) ( 1，1，1) ( 2，3，4) ( 2，3，4) ( 1，2，3) ( 1，2，3)

####  
( 1 /5，1 /4，1 /3) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1，1，2) ( 1 /7，1 /6，1 /5) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1，1，1) ( 1 /2，1，1) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1)

####  
( 1 /5，1 /4，1 /3) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1 /2，1 /2，1) ( 1 /7，1 /6，1 /5) ( 1 /4，1 /3，1 /2) ( 1 /4，1 /3，1 /2) ( 1，1，2) ( 1，1，1) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1)

####  
( 1 /4，1 /3，1 /2) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1) ( 1，2，3) ( 1 /6，1 /5，1 /4) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1) ( 1，2，3) ( 1，2，3) ( 1，1，1) ( 1 /2，1，1)
( 1 /4，1 /3，1 /2) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1) ( 1，2，3) ( 1 /6，1 /5，1 /4) ( 1 /3，1 /2，1) ( 1 /3，1 /2，1) ( 1，2，3) ( 1，2，3) ( 1，1，2) ( 1，1，1)

#### 2) 由式( 2) ～( 5) 可得各指标的三值权重。 Px3 = ( 0. 049，0. 098，0. 203)

#### Px1 = ( 0. 076，0. 162，0. 294) Px4 = ( 0. 018，0. 032，0. 068)

#### Px2 = ( 0. 065，0. 098，0. 195) Px5 = ( 0. 133，0. 237，0. 679)

#### Px6 = ( 0. 049，0. 098，0. 203)

#### Px7 = ( 0. 047，0. 098，0. 195)

#### Px8 = ( 0．018，0．032，0．068)

#### Px9 = ( 0．018，0．032，0．068)

#### Px10 = ( 0. 025，0. 058，0. 142)

#### Px11 = ( 0．027，0．058，0．133)

#### 3) 对三值权重去模糊化，由式( 6) ～( 9) 可得初

#### 级权重为

#### w'1 = ( v1，v2，…，v11) = ( 0. 6848，0. 3092，

#### 0. 3353，0. 2240，1. 000，0. 3354，0. 3090，

#### 0. 2240，0. 2240，0. 0450，0. 3587)

#### 4) 对初级权重进行标准化处理得最终权重为
图2 正向云发生器流程

#### w1 = ( 0. 1691，0. 0764，0. 0828，0. 0533，
Fig．2 Algorithm flow of forward cloud generator

#### 0. 2469，0. 0828，0. 0763，0. 0553，0. 0553，

表3 各边坡不同指标实测值
Table 3 Actual value of each index of each slope
边坡编号 x1 /% x2 /% x3 /MPa x4 /( °) x5 /MPa x6 /( kN·m －3) x7 /m x8 /( °) x9 /mm x10 /度 x11 /%
S1 82 80 0. 045 48 2 26 70 25 1 000 6 80
S2 61 70 0. 025 25 10 19 100 30 1 100 7 60
S3 40 40 0. 020 16 25 20 95 29 1 200 7 60

<!-- 第 6 页 -->
Vol．21 No．6 安全与环境学 报 第21 卷第6 期

0. 0111，0. 0887) w1w1 = 0. 13187272，w1 wT 2 = w2 wT 1 = 0. 07394352，T

#### 4. 1. 2 基于CＲITIC 法的指标客观权重计算 w2w2 = 0. 13443172，由式( 17) 可得T

### ( ) α( ) ( )

#### 1) 将表3 中的x1、x2、x3、x4、x6 五个益稳指标和 α1

#### 0. 1319 0. 0739 0. 1319

#### =

#### x5、x7、x8、x9、x10、x11 六个逆稳指标分别按式( 10) 和

#### 0. 0739 0. 1344 0. 1344
2

#### ( 11) 进行处理，可得标准化矩阵B。

#### 解得α1 = 0. 6364，α2 = 0. 6485 ，归一化处理后

####  1 1 1 1 1 1 1 1 1 1 1

#### 得权重最优分配比系数: α* = 0. 4953，α* =

#### B =   1 2

### 0. 5 0. 725 0. 2 0. 2 0. 652 0 0 0 0. 5 0 0

#### 0. 5047。

# 0 0 0 0 0 0. 145 0. 167 0. 2 0 0 0

#### 由式( 18) 可得最优综合权重为

#### 2) 根据式( 12) ～( 16) ，并借助Matlab 软件计算

#### w* = ( 0. 0943，0. 0628，0. 0695，0. 0461，

#### 得出各指标的客观权重。

# 公众号：数学建模老哥
w2 = ( 0. 0209，0. 0495，0. 0565，0. 0390， 0. 1400，0. 1259，0. 1269，0. 1232，0. 0379，

#### 0. 0351，0. 1682，0. 1766，0. 1899， 0. 0669，0. 1054)

#### 0. 0209，0. 1217，0. 1217) 4. 2 云图的生成和指标等级隶属度的计算

#### 4. 1. 3 基于博弈论模型的指标最优综合权重确定 根据云特征参数和各边坡指标的实测数据，在

#### 1) 由以上求得的w1 和w2 的权重集可计算出 Matlab 环境下输入程序，生成指标云图，并计算各边

#### 坡各指标在不同等级的隶属度。由于篇幅限制，只

#### 展示3 个典型云图和边坡S1的各指标不同等级隶属

#### 度，分别见图4 和表4。

#### 4. 3 综合确定度的计算和各边坡危险性等级的

#### 判断

#### 由式( 20) 可得各边坡在不同等级下的综合确

#### 定度Dk。根据式( 21) 可判断出3 个待评估边坡的

#### 危险性等级，结果见表5。

#### 由表5 可知，边坡S1、S2、S3 的危险性分别为低

#### ( Ⅱ级) 、较高( Ⅲ级) 、很高( Ⅴ级) ，与各边坡实际情

#### 况相符，表明了该评估模型的科学性和可行性

#### 4. 4 评估模型的准确性验证和算法组合的必要性
图3 博弈论与云模型的计算流程图

#### 1) 为了验证改进FAHP CＲITIC 法博弈赋权的
Fig．3 Calculation flow chart of game theory

#### 准确性，在本文求得的最优综合权重的基础上，分别
and cloud model

#### 采用未确知测度理论和模糊综合评价法进行综合性
表4 边坡S1的各指标等级隶属度
Table 4 Grade membership degree of each index of slope S1
等级 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11
I 0. 009 8 0. 002 2 0. 000 8 0. 174 3 0. 512 8 0. 004 7 0. 000 1 0. 024 2 0. 000 0 0. 002 3 0. 505 2
Ⅱ 0. 973 1 1. 000 0 0. 000 0 0. 000 0 0. 506 0 0. 347 2 0. 000 0 0. 927 1 0. 000 0 0. 073 0 0. 505 5
Ⅲ 0. 369 4 0. 006 6 0. 013 6 0. 000 0 0. 002 1 0. 681 4 0. 024 1 0. 150 5 0. 024 5 1. 000 0 0. 002 2
Ⅳ 0. 000 2 0. 000 0 0. 274 9 0. 000 0 0. 000 0 0. 000 5 1. 000 0 0. 000 1 0. 505 8 0. 001 8 0. 000 0
Ⅴ 0. 000 0 0. 000 0 0. 423 6 0. 000 0 0. 000 0 0. 002 2 0. 065 6 0. 000 5 0. 505 9 0. 064 7 0. 000 0
表5 评估结果及对比
Table 5 Evaluation results and comparison
综合确定度 本文 实际 未确知 模糊综 AHP 物元
边坡编号
D( Ⅰ) D( Ⅱ) D( Ⅲ) D( Ⅳ) D( Ⅴ) 方法 情况 测度 合评价 可拓模型
S1 0. 137 94 0. 441 49 0. 180 58 0. 165 39 0. 061 60 Ⅱ Ⅱ Ⅱ Ⅱ Ⅲ
S2 0. 000 62 0. 259 63 0. 507 33 0. 115 01 0. 188 41 Ⅲ Ⅲ Ⅲ Ⅲ Ⅲ
S3 0. 000 69 0. 127 75 0. 245 24 0. 271 75 0. 323 00 Ⅴ Ⅴ Ⅴ Ⅴ Ⅳ

<!-- 第 7 页 -->
2021 年12 月 侯克鹏，等: 基于改进的FAHP CＲITIC 法与云理论的露天矿边坡危险性评估模型 Dec．，2021

#### 5 结 论

#### 1) 采用改进的FAHP 法确定主观权重，专家利

#### 用三值判断法打分，可以避免判断结果太绝对，更符

#### 合人的思维; 且该法中引入了模糊三角函数模型，模

#### 糊算法能根据人的心理特点建立模型，更符合人的

#### 思维，增加了主观权重的准确性。

#### 2) 相比于熵权法，CＲITIC 法兼顾了边坡实测数

#### 据的关联度及指标间的差异性和相关性，使求得的

# 公众号：数学建模老哥客观权重更可靠; 引入博弈思想，在主、客观权重之

#### 间寻找一种平衡，得到最优综合权重，增加了评估结

#### 果的准确性。

#### 3) 云模型可以将抽象的定性概念转换为具体的

#### 定量数值，且具有很强的普适性，对边坡危险性分级

#### 的随机性和模糊性具有很好的处理效果。

参考文献( Ｒeferences) :

［1］秦宏楠．紫金山金铜矿排土场滑坡诱发机理及监测预
警技术研究［D］．北京: 北京科技大学，2016.
QIN H N．Study on waste dump landslide inducement
mechanism and monitoring and early warning technology of
Zijinshan gold and copper mine［D］．Beijing: University
of Science and Technology Beijing，2016.
［2］黄志全，崔江利，刘汉东．边坡稳定性预测的混沌神
经网络方法［J］．岩石力学与工程学报，2004，23

#### ( 22) : 3808 3812.
HUANG Z Q，CUI J L，LIU H D．Chaotic neural network
method for slope stability prediction［J］．Chinese Journal
of Ｒock Mechanics and Engineering，2004，23 ( 22 ) :
图4 典型指标的等级云图 3808 3812.
Fig．4 Grade cloud chart of typical indicators
［3］李云，刘霁．基于模糊集理论与CSMＲ的岩质边坡稳
定性分析［J］．中南大学学报( 自然科学版) ，2012，43

#### 评估，结果见表5。对比可得，3 种方法的评估结果

#### ( 5) : 1940 1946.

#### 一致，表明了本文所使用赋权方法的准确性和评估
LI Y，LIU J．Assessment of rock slope stability using

#### 模型中算法组合的可靠性。
fuzzy set and CSMＲ［J］．Journal of Central South Univer-
2) 为进一步证明本文评估模型中所使用算法组 sity ( Science and Technology) ，2012，43 ( 5 ) : 1940

#### 合的必要性，又采用AHP 物元可拓模型进行评估， 1946.
其评估结果分别为Ⅲ级、Ⅲ级、Ⅳ级，边坡S1和S3的 ［4］MAＲK H J ，WEST T Ｒ，WOO I．Probabilistic analysis of
评估结果与实际情况不一致。这一方面表明仅采用 rock slope stability and random properties of discontinuity
parameters，Interstate Highway 40，Western North Caro-

#### AHP 法确定权重，会导致权重失衡，进而影响评估
lina，USA［J］．Engineering Geology，2005，79 ( 3 /4) :

#### 结果的准确性; 另一方面，物元可拓模型的不确定性

# 230 250.

#### 主要侧重于系统中是与非的转化，而云模型的不确
［5］ 张艺冰，刘汉东，杨继红，等．基于改进突变理论的

#### 定性主要表现在处理数据的模糊性和随机性，因此，
水库边坡稳定性风险分析———以前坪水库右坝肩边

#### 对于模糊性问题，云模型的处理效果更好。这进一
坡为例［J］．科学技术与工程，2020，20 ( 8) : 3246

#### 步证明了文中所构建的评估模型的科学可行性和算 3251.

#### 法组合的必要性。 ZHANG Y B，LIU H D，YANG J H，et al．Slope stabili-

<!-- 第 8 页 -->
Vol．21 No．6 安全与环境学 报 第21 卷第6 期

ty risk analysis of reservoir based on improved catastrophe 济，2020( 10) : 105 108.
theory: a case study of right abutment slope of Qianping CHEN H，ZHANG C Y，WEI ＲY．Grading evaluation
Ｒeservoir［J］． Science Technology and Engineering， of slope stability based on combination weighting of game
2020，20( 8) : 3246 3251. theory and ideal point method［J］．Inner Mongolia Sci-
［6］汪中杰．基于灰色理论的土质边坡稳定性分析及应用 ence Technology ＆Economy，2020( 10) : 105 108.
［D］．成都: 西南交通大学，2014. ［14］赵军，宋扬．改进熵权正态云模型在边坡稳定性评
WANG Z J． Analysis and application of soil stability 价中的应用［J］．水电能源科学，2016，34( 4) : 120
based on grey theory［D］．Chengdu: Southwest Jiaotong 122，165.
University，2014. ZHAO J，SONG Y．Slope stability evaluation based on
［7］王加闯，黄明健，过江．基于CＲITIC 有限区间云模 improved entropy weight-cloud model［J］． Water Ｒe-
公众号：数学建模老哥型的边坡稳定性评价［J］．中国安全生产科学技术， sources and Power，2016，34( 4) : 120 122，165.
2019，15( 6) : 113 119. ［15］ 刘洋洋，李永强，郭增长，等．基于AHP Fuzzy 和
WANG J C，HUANG M J，GUO J．Evaluation of slope 激光点云数据的公路边坡危险性评估研究［J］．灾害
stability based on CＲITIC finite interval cloud model［J］． 学，2018，33( 1) : 206 212.
Journal of Safety Science and Technology，2019，15( 6) : LIU Y Y，LI Y Q，GUO Z Z，et al．Ｒesearch on risk

# 113 119. evaluation of highway slope based on AHP Fuzzy and
［8］ 李德毅，孟海军，史雪梅．隶属云和隶属云发生器 laser point cloud data［J］．Journal of Catastrophology，
［J］．计算机研究与发展，1995，32( 6) : 15 20. 2018，33( 1) : 206 212.
LI D Y，MENG H J，SHI X M．Membership clouds and ［16］汪伟，罗周全，熊立新，等．基于改进物元可拓模型
membership cloud generators［J］．Computer Ｒesearch and 的采空区稳定性评价［J］．安全与环境学报，2015，
Development，1995，32( 6) : 15 20. 15( 1) : 21 25.
［9］陈加良．基于博弈论的组合赋权评价方法研究［J］． WANG W，LUO Z Q，XIONG L X，et al．Ｒesearch of
福建电脑，2003( 9) : 15 16. goaf stability evaluation based on improved matter-ele-
CHEN J L．Ｒesearch on evaluation method of combination ment extension model［J］．Journal of Safety and Envi-
weighting based on game theory［J］．Journal of Fujian ronment，2015，15( 1) : 21 25.
Computer，2003( 9) : 15 16. ［17］ 非煤露天矿边坡工程技术规范: GB 51016—2014
［10］ 周建国，段三良．烟气同时脱硫脱硝技术综合评 ［S］．
价———基于博弈改进云模型［J］．技术经济，2009， Technical code for non-coal open-pit mine slope engi-
28( 8) : 66 71，114. neering: GB 51016—2014［S］．
ZHOU J G，DUAN S L．Comprehensive evaluation on ［18］工程岩体分级标准: GB/T 50218—2014［S］．
simultaneous removal of SO2 and NOx from flue gas: Standard for engineering classification of rock mass: GB/
based on game theory and improving cloud model［J］． T 50218—2014［S］．
Technology Economics，2009，28( 8) : 66 71，114. ［19］刘洋洋，郭增长，李永强，等．基于熵权集对分析和
［11］方前程，商丽．基于博弈论云模型的露天矿岩质边 车载激光扫描的公路边坡危险性评价模型［J］．岩土
坡稳定性分析［J］．安全与环境学报，2019，19( 1) : 力学，2018，39( S2) : 131 141.

# 8 13. LIU Y Y，GUO Z Z，LI Y Q，et al．Ｒisk assessment
FANG Q C，SHANG L．Analysis of the rock slope sta- model of highway slope based on entropy weight set pair
bility for the open-pit mine based on the game theory and analysis and vehicle laser scanning［J］．Ｒock and Soil
the cloud model［J］．Journal of Safety and Environment， Mechanics，2018，39( S2) : 131 141.
2019，19( 1) : 8 13. ［20］ SAATY T L．Applications of analytical hierarchies［J］．
［12］方前程，商丽．基于变权重理论正态云模型的边坡 Mathematics and Computers in Simulation，1979，21
稳定性研究［J］．安全与环境学报，2018，18 ( 5) : ( 1) : 1 20.
1681 1685. ［21］ZADEH L A．Fuzzy sets［J］．Information and Control，
FANG Q C，SHANG L．On the slope stability based on 1965，8( 3) : 338 353.
the variable weight theory normal cloud model［J］．Jour- ［22］AZADEH A，ZADEH S A．An integrated fuzzy analytic
nal of Safety and Environment，2018，18 ( 5) : 1681 hierarchy process and fuzzy multiple-criteria decision-
1685. making simulation approach for maintenance policy se-
［13］陈昊，张楚怡，魏荣誉．基于博弈论组合赋权与理想 lection［J］．Simulation，2016，92( 1) : 3 18.
点法的边坡稳定性分级评价［J］．内蒙古科技与经 ［23］李强，汪永超，侯力，等．基于改进的FAHP CＲIT-

<!-- 第 9 页 -->
2021 年12 月 侯克鹏，等: 基于改进的FAHP CＲITIC 法与云理论的露天矿边坡危险性评估模型 Dec．，2021

IC 和VIKOＲ法的专用机床优选方法［J］．组合机床 slope risk assessment of open-pit mine，this paper constructs a
与自动化加工技术，2020( 11) : 135 138，143. weight determination method based on the Improved Fuzzy Ana-
LI Q，WANG Y C，HOU L，et al．Optimization method lytic Hierarchy Process ( FAHP ) -the Criteria Importance
of special machine tools based on improved FAHP Through Intercrieria Correlation ( CＲITIC) method，and then
CＲITIC and VIKOＲmethods［J］．Modular Machine Tool puts forward the slope risk assessment method based on the nor-
＆Automatic Manufacturing Technique，2020( 11) : 135 mal cloud theory．The selected 11 evaluation indexes are ana-
138，143. lyzed，including the rock quality，rock mass structure character-
［24］陈卫卫，李涛，李志刚，等．基于模糊层次分析法的 istic，cohesive force，internal friction angle，ground stress，high
云服务评估方法［J］．解放军理工大学学报( 自然科 density，slope height，slope，average annual rainfall，earthquake
学版) ，2016，17( 1) : 25 30. intensity，and human activity．The above 11 evaluation indexes
公众号：数学建模老哥CHEN W W，LI T，LI Z G，et al．Method of cloud are chosen from five aspects in geological environmental charac-
service evaluation based on fuzzy analytic hierarchy teristics，hydrological factors，engineering conditions，slope ge-
process［J］．Journal of PLA University of Science and ometries．The risk grades of slope in the combination of the
Technology ( Natural Science Edition) ，2016，17( 1) : above indicators are divided into five levels: extremely low risk，
25 30. low risk，higher risk，high risk，and very high risk．Firstly，we
［25］ 万林，章国宝，陶杰．基于AHP CＲITIC 的电梯安 respectively adopt the improved FAHP method and the CＲITIC
全性评估［J］．安全与环境学报，2017，17( 5) : 1696 method to determine the subjective and objective weights of each
1700. evaluation index，then employ the game theory to find a balance
WAN L，ZHANG G B，TAO J．On the safety evaluation between the subjective and objective weights，determining the
of the elevator based on AHP CＲITIC criteria［J］． optimal comprehensive weights of each index．Meanwhile，the
Journal of Safety and Environment，2017，17( 5) : 1696 forward cloud generator of the cloud model is used to calculate
1700. the membership degree of each finger grade of each slope that
［26］ DIAKOULAKI D，MAVＲOTAS G，PAPAYANNAKIS needs to be evaluated according to the cloud digital characteris-
L．Determining objective weights in multiple criteria tics calculated in the paper．Based on the optimal comprehensive
problems: the CＲITIC method［J］．Computers ＆Oper- weights and grade membership degree of each index obtained
ations Ｒesearch，1995，22( 7) : 763 770. above，the comprehensive determination degree of each slope to
［27］贾玉霞．基于博弈论组合赋权和模糊评价的我国跨境电 be evaluated can be calculated．Finally，according to the maxi-
商物流模式研究［D］．杭州: 浙江工商大学，2017. mum certainty principle，the risk grade of the slope is divided．
FEI Y X．Ｒesearch on cross border ecommerce logistics The model is applied to assess the risk of three slopes of an open-
model based on game theory and fuzzy comprehensive pit copper mine．Fortunately，the assessment results are consist-
evaluation［D］．Hangzhou: Zhejiang Gongshang Univer- ent with the reality，namely grade II，grade III，and grade V，
sity，2017. indicating the accuracy and feasibility of the assessment model．
［28］ LIU Y，ECKEＲT C M，EAＲL C．A review of fuzzy Compared with the results of other methods，the analysis further
AHP methods for decision-making with subjective judge- proves that the evaluation model mentioned above is scientific
ments［J］．Expert Systems with Applications，2020， and feasible，and can be applied to the slope risk assessment of
161: 113738. open-pit mine．
Key words: safety engineering; improved FAHP method; CＲIT-
Ｒisk assessment model of open-pit IC method; game theory; cloud model; comprehen-
sive degree of certainty

#### mine slope based on improved FAHP
CLC number: X936 Document code: A
CＲITIC method and cloud theory Article ID: 1009-6094( 2021) 06-2443-09
HOU Ke-peng1，2，WANG Li-die1，2

( 1 Faculty of Land Ｒesource Engineering，Kunming University of
Science and Technology，Kunming 650000，China; 2 Key Labo-
ratory of Sino-German Blue Mining and Utilization of Special Un-
derground Space，Kunming 650000，China)

Abstract: Aiming at the uncertainty and fuzziness existing in the
