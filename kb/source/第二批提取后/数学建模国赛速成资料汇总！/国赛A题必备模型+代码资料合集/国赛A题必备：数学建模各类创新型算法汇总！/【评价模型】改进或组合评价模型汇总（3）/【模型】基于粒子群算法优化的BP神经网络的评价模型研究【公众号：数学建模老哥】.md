<!-- 第 1 页 -->

## 基于粒子群算法优化的BP 神经网络在海水水质评价中的应用

### 李海涛, 王博睿

#### (青岛科技大学信息科学与技术学院, 山东青岛 266061)

摘要: 针对目前存在的海水水质受多因素影响、评价难的现状, 提出了一种基于粒子群算法(PSO)优化
误差反向传播(BP)神经网络的海水水质评价模型。该模型通过PSO 得到BP 神经网络最优的权值和阈

> # 公众号：数学建模老哥
值, 结合青岛东部海域10 个监测站点的数据得到水质评价结果。实验证明, 该模型和单因子评价、传
统的BP 神经网络评价相比较, 具有训练时间短、预测精度高的特点, 在海水水质评价中具有良好的应
用价值。

关键词: 粒子群算法; BP 神经网络; 海水水质评价
中图分类号: TP391.9    文献标识码: A      文章编号: 1000-3096(2020)06-0031-06
DOI: 10.11759/hykx20191116002

#### 随着海洋污染持续加重, 海洋环境的相关研究关数据, 但同时自身存在易陷入局部极小的问题,

#### 已变得尤为重要。根据各相关指标对海水的水体质导致海水水质评价的预测精度低[11]。常见的BP 神经

#### 量进行综合评判, 可以找出该海域的主要污染问题,  网络的结构示意图如图1 所示。

#### 为该海域的环境管理与决策提供依据[1]。国内外专家

#### 学者经过多年的研讨, 提出了许多评价方法, 诸如

#### 单因子评价法、模糊综合评价法、模糊聚类法、灰

#### 色聚类法等[2-5]。由于水环境污染是多种因素综合引

#### 起的结果, 这使得传统的评价方法存在局限性。

#### BP 神经网络可以很好地处理非平稳性、非时序

#### 性的海洋环境相关数据[6], 被越来越广泛地应用到

#### 海水水质评价中。但是BP 神经网络自身存在着一些

#### 问题, 例如学习效率低下、易陷入局部极小导致无法图1  常见的BP 神经网络的结构示意图
寻求到全局最优解等[7], 限制了其在海水水质评价 Fig. 1  Schematic of a common BP neural network

#### 方面的应用。

#### 1.2  粒子群算法

#### 为了解决以上问题, 本文构建出新的PSO-BP
评价模型, 利用PSO 得到BP 神经网络各层最优的权粒子群算法(PSO, Particle Swarm Optimization)

#### 阈值, 进一步评价青岛东部海域的水质。即群落智能的搜寻方法, 主要是模拟鸟群之间的互

#### 相协作、角逐而产生的群落智能搜寻[12]。该算法将

### 1  粒子群算法优化BP 神经网络的基

#### 优化问题的解都模拟成搜寻空间中的粒子, 这些粒

### 本原理

#### 子可以忽略自身的体积与质量, 却以确定的速度飞

#### 行[13]。粒子选择合适的计算函数求出自身适应度,

#### 1.1  BP 神经网络

#### BP 神经网络(Back-Propagation Network)是误差
收稿日期: 2019-11-16; 修回日期: 2020-02-12

#### 逆向传递的神经网络, 通常由3 个层次的神经元组
基金项目: 农业部水产养殖数字农业建设试点项目(2017-A2131-

#### 成, 分别为输入层、中间层(隐含层)及输出层[8-10]。 130209-K0104-004)
[Foundation: Pilot project of digital agriculture construction in Ministry of

#### 其主要特点是信号从输入层到输出层正向传输, 而
Agriculture, No. 2017-A2131-130209-K0104-004]
误差从输出层逆向传达到输入层。BP 神经网络可以作者简介: 李海涛(1978-), 男, 山东菏泽人, 副教授,硕士生导师, 研
究方向为智慧海洋、智慧渔业、地理信息系统, 电话: 0532-80866089,

#### 很好地处理非平稳性、非时序性的海水水质评价相
E-mail: taohaili@sina.com

#### Marine Sciences / Vol. 44, No. 6 / 2020  31

<!-- 第 2 页 -->

#### 通过自身以及群落当下的最优点的适应度值动态 (2) 设置群落规模、粒子初始飞行速度和对应点

#### 调整自己的飞行速度和对应点位, 最终搜寻到全局位。选取粒子当前的最佳点位为初始点位, 而群落的

#### 的最优点。粒子调整速度V 与点位X 分别如式(1) 最佳点位为全局最佳点位。

#### 所示。  (3) 每个粒子均含有一个适应度值, 用于反映
vk1  ωvk  c r p( k  X k )  c r ( pk  X k ) 粒子优劣程度。对BP 神经网络进行训练后, 将得到

####

#### i i 1 1 i i 2 2 g i ,  (1)

####   的训练误差作为粒子当前点位的适应度值, 并将结

#### X k 1  X k  vk 1
i i i

#### 果与以往最佳点位的值进行比较, 若好于以往的最

#### 其中, ω 为惯性权重; k 为当前迭代次数; i=1, 2,…, m;

#### 佳点位则将其替代, 否则不变。

#### r1和r2是[0, 1]区间内均匀分布的随机数; c1和c2是学

> # 公众号：数学建模老哥

#### (4) 如果全局的最佳点位不及当前粒子以往的

#### 习因子; ip 是第k 次迭代的最优解;k p 为目前为止的k

#### g 最佳点位, 则用以往的最佳点位取代全局的最佳点

#### 全局最优解。

#### 位, 否则不变。

#### 1.3  粒子群算法优化BP 神经网络  (5) 根据式(1)重新规划粒子的飞行速度以及对

#### BP 神经网络的随机产生的权阈值会影响模型的应点位。

#### 精度[14], 本文充分发挥PSO 的优势得到BP 神经网 (6) 检查算法是否满足终止条件(迭代次数达到

#### 络最佳的权阈值, 构建出新的评价模型(PSO-BP),  最大迭代次数或误差精度达到初始设置的目标误差

#### 应用到海水水质评价中。精度), 若终止条件成立, 则输出最佳的权阈值, 然

#### 实验具体步骤如下:   后进一步对模型进行仿真, 否则跳转到步骤(3)。

#### (1) 确定BP 神经网络的结构和相关参数。本文模型的构建流程按照如图2 所示进行。

图2  PSO-BP 神经网络流程图
Fig. 2  Flowchart of PSO-BP neural network

#### 32  海洋科学 / 2020 年 / 第44 卷 / 第6 期

<!-- 第 3 页 -->

### 2  应用分析  2.4  模型参数设置

#### 从理论上来说, 3 个层次的 BP 神经网络能够以

#### 2.1  评价标准

#### 任意精密度迫近连贯的非线性函数, 可以处理实际

#### 本文参照《中华人民共和国海水水质标准》(GB

#### 应用中的各种非线性数据问题[18]。因此, 本文建立

#### 3097—1997), 根据青岛东部海域的实际情况, 选取

#### 3 层BP 神经网络, 选取DO、COD、无机氮、活性

#### DO、COD、无机氮、活性磷酸盐和石油类这5 个指标

#### 磷酸盐和石油类这5 个指标为输入层节点, 水质评

#### 作为评价指标[15]。其中, 评价指标的标准值如表1 所示。

#### 价结果为输出层节点。由于目前还欠缺完善的理论

#### 依据能够准确计算中间层(隐含层)的节点数, 可以

> # 表1  水质评价指标的标准值公众号：数学建模老哥
Tab. 1  Standard value of water quality assessment   通过常见的估算公式来确定中间层(隐含层)节点个

#### in dicators  数范围[19], 如式(3)所示。

#### 评价指标  Ⅰ  Ⅱ  Ⅲ  Ⅳ  劣Ⅴ类 g  a  b  c ,            (3)
DO  6  5  4  3  ≤3

#### 其中, g 为中间层(隐含层)节点的数量, a 为输入层节
COD  2  3  4  5  ＞5

#### 点的数量, b 为输出层节点的数量, c 为1 到10 之间
无机氮  0.2  0.3  0.4  0.5  ＞0.5

#### 的随机数。
活性磷酸盐  0.015  0.030  0.030  0.045  ＞0.045

#### 本文经过式(3)计算, 得出中间层结点的区间范
石油类  0.05  0.05  0.30  0.50  ＞0.50

#### 围为[4, 13], 但由于该区间范围较大, 导致误差过大,

#### 预测结果不够准确。经过多次试验后, 当中间层的节

#### 2.2  数据来源

#### 点数量为6 时, 该模型预测的精确度最高, 所以中间

#### 本文选取青岛东部海域2017 年10 个监测站点层节点数量确定为6 个。根据以上设计思想, 该神经

#### 的监测数据作为评价数据, 训练样本是依据海水水网络的网络结构设计为5-6-1。

#### 质评价标准而产生的, 通过随机均匀插值[16]的方式,

#### 确定神经网络3 个层次的结构后, 设定相关参数规

#### 在Ⅰ到Ⅴ五个水质级别中每个级别随机生成100 个格。输入层、中间层(隐含层)之间的网络转移函数选用
训练样本, 共生成500 个样本, 随机插入各级评价标 Matlab 中的Sigmod 函数; 中间层(隐含层)、输出层之间

#### 准内, 解决了只用各个等级评价指标的标准值作为的网络转移函数选用Matlab 中purelin 函数。此外, 神
样本数量不足的问题, 并选取0.1, 0.3, 0.5, 0.7, 0.9 作经网络的学习步长设定为0.05, 训练次数设定为500 次,

#### 为Ⅰ、Ⅱ、Ⅲ、Ⅳ、Ⅴ五类水质评价指标的为期望输误差的期望为0.001; 粒子群算法中的群落规模为100,

#### 出值, 如表2 所示。学习因子c1和c2均为1.494, 惯性权重ω 设置为0.7, 迭

#### 代的极大次数设置为200。
表2  水质评价指标的期望输出值

#### 2.5 评价结果及对比分析
Tab. 2  Expected output value of water quality assessment
indicators

#### 在Matlab2014a 下训练设计好的PSO-BP 评价模
评价指标  Ⅰ  Ⅱ  Ⅲ  Ⅳ  劣Ⅴ类

#### 型, 得到神经网络的权阈值如下:
期望输出值  0.1  0.3  0.5  0.7  0.9

#### 输入层到隐含层的权值W1 和阈值B1:

#### 0.743 3 3.169 8 3.766 2 2.469 8 2.166 2

#### 2.3  数据预处理   0.713 9 2.013 4 1.907 6 0.636 6 1.485 9

####

#### 2.878 8 2.587 5 0.426 4 0.839 6 1.736 8

#### 由于不同指标之间的数据存在较大的量级差异,  W

#### 1  0.646 2 0.372 2 0.1819 0.7419 0.879 5

#### 必须进行归一化处理[17]消除数据量级的差别, 使数

#### 0.738 2 1.235 6 0.524 7 0.8317 0.623 7

####  0.578 2 2.6217 0.195 3 1.2841 0.7516

#### 据在0 和1 之间散布, 否则, 各维度影响因素量级的

#### 差别会造成输出结果的误差较大。本文归一化计算  0.866 4

####

#### 公式如(2)式所示:   0.456 6

####

#### X  X  0.447 4

#### X  k min ,          (2)  B

#### k X  X 1 1.227 7

####
max min

####  0.389 8

#### 其中, Xmax 是该样本数据集中的最大值, Xmin 是该样

####

#### 本数据集中的最小值。   0.5371 .

#### Marine Sciences / Vol. 44, No. 6 / 2020  33

<!-- 第 4 页 -->

#### 隐含层到输出层的权值W1 和阈值B2:   结合监测数据和表4 的对比分析可以得出, 本

#### W    , 文的PSO-BP 评价模型得出的结果更贴合青岛市海

## 2.270 5 1.3717 1.226 7 1.335 8 2.570 4  2.743 7
2

#### B    洋环境公报中的水质评价结果。单因子评价结果出

#### 1.425 9 .
2

#### 得到该神经网络的权阈值矩阵后, 因为这些权现了过激情况, 在6 号监测站点和7 号监测站点的评

#### 阈值表达了网络输入、输出间的非线性关系 , 所以价结果分别偏重和偏轻, 并对该海域总体评价结果

#### 训练后将这些权阈值矩阵进行保存, 从而避免神经偏差, 这可能是由于单因子评价只突出污染状况最

#### 网络的反复训练, 并使用该训练好的海水水质评价为严峻的因素, 而削弱了其他因素的作用, 不能直

#### 模型对青岛东部海域10 个站点的水质进行评价, 如观展示整体的水质状况; 而传统的BP 网络可能由于

> # 公众号：数学建模老哥

#### 表3 所示, 得到各监测点的水质评价等级。自身存在的易陷入局部极小的缺陷, 导致在9 号监

#### 测站点的评价结果与其他评价方法的结果相比有较
表3  各监测点位的水质评价结果

#### 大的差别, 会间接影响该海域总体的评价结果; 本
Tab. 3  Water quality evaluation results of each moni-

#### toring point  文评价模型运用PSO 来优化BP 神经网络的权阈值,

#### 监测 COD 无机氮活性磷 PSO-BP 很好的摆脱了污染物超标情况对权重值的影响, 具
DO  石油类

#### 点位酸盐评价结果有更高的精确度和更好的性能。

# 001  6.62  2.21  0.914 7 0.153 6 0.015 5  Ⅱ

### 3  结论

# 002  8.37  1.89  0.453 5 0.004 2 0.026 7  Ⅱ

# 003  7.17  3.24  0.876 2 0.053 6 0.043 6  Ⅱ

#### 本文充分发挥了粒子群算法(PSO)的优势, 提出

# 004  7.83  2.85  1.486 7 0.034 7 0.017 4  Ⅱ

#### 了PSO-BP 海水水质评价模型, 缩短了训练次数, 达

# 005  6.24  1.87  1.111 9 0.186 3 0.034 5  Ⅲ

#### 到了较高的精度;以青岛东部海域10 个监测站的监

# 006  5.90  1.35  1.586 8 0.169 8 0.075 2  Ⅲ

#### 测数据作为评价样本, 将PSO-BP 神经网络运用到海

# 007  7.53  1.81  0.647 7 0.001 4 0.023 7  Ⅲ
008  6.81  2.04  0.511 6 0.098 7 0.038 7  Ⅱ  水水质评价中, 得出的结果更贴合真实状况, 为青
009  7.41  1.98  0.313 1 0.053 4 0.017 8  Ⅱ  岛东部海域的环境治理提供理论基础; 与传统的单
010  6.67  1.34  0.565 0 0.123 9 0.035 7  Ⅱ  因子、BP 神经网络海水水质评价方法相比, 该模型

#### 能够较为准确合理地得到海水水质等级, 具有一定

#### 为了进一步分析PSO-BP 评价模型, 将本文结

#### 的推广价值。

#### 果与2017 年青岛市海洋环境公报中这10 个站点的水

#### 质评价结果以及单因子评价、传统的BP 神经网络的参考文献:

#### 评价结果作比较。具体的评价结果对比如表4 所示。
[1]  兰文辉, 安海燕. 环境水质评价方法的分析与探讨[J].
干旱环境监测, 2002, 16(3): 42-44.
表4  不同评价方法的结果对比
Lan Wenhui, An Haiyan. Discussion on methods water
Tab. 4  Comparison of results of different evaluation
quality assessment[J]. Arid Environmental Monitoring,
methods
2002, 16(3): 42-44.
监测点位环境公报单因子 BP 神经 PSO-BP 神
[2]  杨旭, 曾祥亮. 基于单因子评价法和污染指数法的郑
评价评价网络评价经网络评价
州大学眉湖水质评价[J]. 江苏科技信息, 2014, (5):

# 001  Ⅱ  Ⅲ  Ⅱ  Ⅱ  51-53.
002  Ⅱ  Ⅱ  Ⅲ  Ⅱ  Yang Xu, Zeng Xiangliang. Water quality evaluation of
003  Ⅱ  Ⅱ  Ⅲ  Ⅱ  Zhengzhou University’s Meihu Lake based on single
004  Ⅰ  Ⅲ  Ⅱ  Ⅱ  factor evaluation method and pollution index method[J].
005  Ⅲ  Ⅳ  Ⅲ  Ⅲ  Jiangsu Science & Technology Information, 2014, (5):
51-53.

# 006  Ⅱ  V  Ⅳ  Ⅲ
[3]  宣卓. 模糊综合评价法在水质评价中的应用[J]. 绿

# 007  Ⅲ  Ⅰ  Ⅱ  Ⅲ
色科技, 2012, (2): 160-162.

# 008  Ⅱ  Ⅱ  Ⅱ  Ⅱ
Xuan Zhuo. Application of fuzzy comprehensive

# 009  Ⅱ  Ⅲ  Ⅳ  Ⅱ
evaluation in water quality assessment[J]. Journal of

# 010  Ⅱ  Ⅱ  Ⅱ  Ⅱ
Green Science and Technology, 2012, (2): 160-162.

#### 34  海洋科学 / 2020 年 / 第44 卷 / 第6 期

<!-- 第 5 页 -->
[4]  慕金玻, 侯克复. 灰色聚类法在水环境质量评价中的 Wei Jinjun. Improvement and application of particle
应用[J]. 环境科学, 1991, 12(2): 86-89.  swarm optimization[D]. Taiyuan: Taiyuan University of
Mu Jinbo, Hou Kefu. Application of grey clustering  Technology , 2015.
method in water environment quality evaluation[J].  [13] 李宁. 粒子群优化算法的理论分析与应用研究[D].
Environmental Science, 1991, 12(2): 86-89.  武汉: 华中科技大学, 2006.
[5]  倪深海, 白玉慧. BP 神经网络模型在地下水水质评 Li Ning. Analysis and application of particle swarm
价中的应用[J]. 系统工程理论与实践, 2000, 20(8):  optimization[D]. Wuhan: Huazhong University of Sci-
124-127.  ence and Technology , 2006.
Ni Shenhai, Bai Yuhui. Application of BP neural net- [14] 魏津瑜, 张玮, 李欣. 基于PSO-BP 神经网络的高炉
work model in groundwater quality evaluation[J]. Sys- 煤气柜位预测模型及应用[J]. 中南大学学报(自然科

> # 公众号：数学建模老哥
tems Engineering-Theory & Practice, 2000, 20(8): 124-  学版), 2013, S1: 266-270.
127.  Wei Jinyu, Zhang Wei, Li Xin. BFG holder forecasting
[6]  周蓉蓉. 基于ANN 与遗传算法的胶州湾近岸海域水 model and application based on PSO-BP neural network
污染总量控制研究[D]. 青岛: 中国海洋大学, 2009.  model[J]. Journal of Central South University(Science
Zhou Rongrong. Research on total amount control for  and Technology), 2013, S1: 266-270.
Jiaozhou Bay near shore area pollution based on ANN  [15] 孙优善, 孙鹤鲲, 王学昌, 等. 胶州湾近岸海域水质
and genetic algorithms[D]. Qingdao: Ocean University  状况调查与评价[J]. 海洋湖沼通报, 2007, (4): 93-97.
of China, 2009.  Sun Youshan, Sun Hekun, Wang Xuechang, et al. Survey
[7]  尚敬强, 原思聪, 卫东东, 等. 基于遗传算法的BP and appraisal of sea water quality in Jiaozhou Bay[J].
神经网络在塔式起重机故障诊断中的应用[J]. 起重 Transactions of Oceanology and Limnology, 2007, (4):
运输机械, 2012, (4): 61-64.  93-97.
Shang Jingqiang, Yuan Sicong, Wei Dongdong, et al.  [16] 楼文高. 海水水质评价的人工神经网络模型研究[J].
Application of genetic algorithm-based BP neural net- 海洋环境科学, 2001, 20(4): 49-53.
work in diagnosis to tower crane[J]. Hoisting and  Lou Wengao. Sea water quality assessment model using
Conveying Machinery, 2012, (4): 61-64.  artificial neural networks[J]. Marine Environmental
[8]  王祖麟, 王丽霞. 一种前馈神经网络算法[J]. 科技广 Science, 2001, 20(4): 49-53.
场, 2004, (8): 51-53.  [17] 宋勇, 蔡志平. 大数据环境下基于信息论的入侵检测
Wang Zulin, Wang Lixia. A modified feed-forward  数据归一化方法[J]. 武汉大学学报(理学版), 2018,
neural network algorithm[J]. Science Mosaic, 2004, (8):  64(2) : 121-126.
51-53.  Song Yong, Cai Zhiping. Normalization method of intru-
[9]  Yu Feng, Xu Xiaozhong. A short-term load forecasting  sion detection data based on information theory in big
model of natural gas based on optimized genetic algo- data environment[J]. Journal of Wuhan University(Natural
rithm and improved BP neural network[J]. Applied En- Science Edition), 2018, 64(2) : 121-126.
ergy, 2014, 134: 102-113.   [18] 姚洪磊, 张彦. 基于BP 神经网络的铁路互联网售票

|Shang Jingqiang, Yuan Sicong, Wei Dongdong, et al. Application of genetic algorithm-based BP neural net- work in diagnosis to tower crane[J]. Hoisting and Conveying Machinery, 2012, (4): 61-64. 王祖麟, 王丽霞. 一种前馈神经网络算法[J]. 科技广场, 2004, (8): 51-53. Wang Zulin, Wang Lixia. A modified feed-forward neural network algorithm[J]. Science Mosaic, 2004, (8): 51-53. Yu Feng, Xu Xiaozhong. A short-term load forecasting model of natural gas based on optimized genetic algo- rithm and improved BP neural network[J]. Applied En- ergy, 2014, 134: 102-113.  众号：数学|Col2|
|---|---|
|Zhao Y, Nan J, Cui F, et al. Water quality forecast<br>|Zhao Y, Nan J, Cui F, et al. Water quality forecast<br>|
|through application of BP neural network at Yuqiao res-<br>|through application of BP neural network at Yuqiao res-<br>|
|ervoir[J]. Journal of Zhejiang University-Science A,<br>|ervoir[J]. Journal of Zhejiang University-Science A,<br>|
|2007, 8(9): 1482-1487<br>|.<br>|

系统信息安全评估方法[J]. 信息网络安全, 2014, (7):
81-86.
Yao Honglei, Zhang Yan. Approach of information se-
curity assessment for railway Internet ticketing system
[11] 卞建民, 胡昱欣, 李育松, 等. 基于BP 神经网络的 based on BP model of artificial neural network[J].
辽河源头区水质评价研究[J]. 水土保持研究, 2014,  Netinfo Security, 2014, (7): 81-86.
21(1): 147-151.  [19] 王嵘冰, 徐红艳, 李波, 等. BP 神经网络隐含层节点
Bian Jianmin, Hu Yuxin, Li Yusong, et al. Water quality  数确定方法研究[J]. 计算机技术与发展, 2018, 28(4):
assessment in source area of Liao River based on BP  31-35.
neural network[J]. Research of Soil and Water  Wang Rongbing, Xu Hongyan, Li Bo, et al. Research
Conservation, 2014, 21(1): 147-151.  on method of determining hidden layer nodes in BP
[12] 魏晋军. 粒子群优化算法的改进及应用[D]. 太原:  neural network[J]. Computer Technology and Develop-
太原理工大学, 2015.  ment, 2018, 28(4): 31-35.

#### Marine Sciences / Vol. 44, No. 6 / 2020  35

<!-- 第 6 页 -->

## Application of BP neural network based on particle swarm

## optimization in seawater quality assessment

#### LI Hai-tao, WANG Bo-rui
(College of Information Science and Technology, Qingdao University of Science and Technology, Qingdao

#### 266061, China)

> # 公众号：数学建模老哥
Received: Nov. 16, 2019
Key words: particle swarm optimization; BP neural network; seawater quality assessment

Abstract: To address the current situation in which seawater quality is affected by many factors and is difficult to
evaluate, a seawater quality assessment model based on particle swarm optimization (PSO) optimized-error back-
propagation (BP) neural network is proposed. The model uses the optimal weight and threshold of a BP neural net-
work through PSO to obtain water quality evaluation results based on data from 10 monitoring stations in the east-
ern sea area of Qingdao. Experiments show that the model has a shorter training time and higher prediction accu-
racy compared with single-factor evaluation and traditional BP neural network evaluation. Overall, the proposed
model has good application value in seawater quality assessment.

#### (本文编辑: 康亦兼)

#### 36  海洋科学 / 2020 年 / 第44 卷 / 第6 期
