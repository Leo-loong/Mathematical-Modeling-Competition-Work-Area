<!-- 第 1 页 -->

# 44 测绘通报 2022 年第10 期

引文格式: 赵侃，师芸，牛敏杰，等．基于改进麻雀搜索算法优化BP 神经网络的PM2. 5 浓度预测［J］．测绘通报，2022( 10) : 44-48．DOI: 10．

# 13474 /j．cnki．11-2246．2022．0292．

#### 基于改进麻雀搜索算法优化BP 神经网络的PM2. 5 浓度预测

#### 赵侃1，师芸2，3，牛敏杰2，3，王虎勤4
( 1．中煤地航测遥感局，陕西西安710199; 2．西安科技大学测绘科学与技术学院，陕西西安710054;
3．自然资源部煤炭资源勘察与综合利用重点实验室，陕西西安710021; 4．西安捷达测控有限公司，
陕西西安710054)

摘要: 针对传统BP 神经网络模型收敛速度慢、易陷入局部极值等问题，本文采用分段线性混沌映射( PWLCM) 和萤火虫算法
( FA) 改进麻雀搜索算法( SSA) ，并优化BP 神经网络模型初始权值和阈值，对西安市PM2. 5 浓度进行预测。通过比较不同模型预
测结果的评价指标，并与性能较优的SSA-BP 模型对比，ISSA-BP 模型预测结果的RMSE、MAPE、MAE 分别下降了3. 70、3. 73、
3. 34。试验结果表明，改进后的麻雀搜索算法具有高效的全局最优搜索能力，优化后的ISSA-BP 神经网络预测稳定性高，精度优
于BP、SSA-BP 神经网络模型，可用于预测PM2. 5 浓度。
关键词: 麻雀搜索算法; 分段线性混沌映射; 萤火虫算法; BP 神经网络; PM2. 5 浓度预测
中图分类号: P237 文献标识码: A 文章编号: 0494-0911( 2022) 10-0044-05

Prediction of PM2. 5 concentration based on optimized BP neural

#### network with improved sparrow search algorithm
ZHAO Kan1，SHI Yun2，3，NIU Minjie2，3，WANG Huqin4
( 1．Aerial Photogrammetry and Remote Sensing Bureau，Xi'an 710199，China; 2．College of Geomatics，Xi'an University of Science and Technology，
Xi'an 710054，China; 3．Key Laboratory of Coal Resources Exploration and Comprehensive Utilization，Ministry of Land and Resources，
Xi'an 710021，China; 4．Xi'an Jieda Measurement and Control Co．，Ltd．，Xi'an 710054，China)
Abstract: Aiming at the problems of slow convergence speed and easy to fall into local extremum of traditional BP neural network
model，this paper uses PWLCM( piece wise linear chaotic map) and FA( firefly algorithm) to improve SSA( sparrow search algorithm)
and optimize the initial weights and thresholds of the BP neural network model to predict the PM2. 5 concentration in Xi'an．By
comparing the evaluation indicators of the prediction results of different models，compared with the better-performing SSA-BP model，
the RMSE，MAPE and MAE of the ISSA-BP model prediction results decrease by 3. 70，3. 73 and 3. 34，respectively． The
experimental results show that the improved sparrow search algorithm has efficient global optimal search ability．The optimized ISSA-BP
neural network has high prediction stability and accuracy，which is better than BP and SSA-BP neural network models and can be used
to predict PM2. 5 concentration．
Key words: sparrow search algorithm; piece wise linear chaotic map; firefly algorithm; BP neural network; PM2. 5 concentration prediction

近年来，随着经济的飞速发展、城市工业化的力，能够依据大气污染物和气象因素与PM2. 5 浓度
不断推进及城市化进程的加快，城市污染问题逐渐之间的非线性关系，获得较高的预测精度，如随机
突出，PM2. 5 浓度成为判断城市空气质量的重要参森林、支持向量、神经网络等模型。BP 神经网络具
考指标［1-2］。因此，有效预测PM2. 5 浓度并采取干预有较强的非线性映射、学习、自适应及容错能力，被广
措施，对降低健康风险具有重要意义。目前PM2. 5 泛应用于PM2. 5 浓度预测［4］。文献［5］建立了基于历
浓度预测模型可分为确定型模型、统计学模型及机史污染物浓度数据的BP 神经网络预测模型，预测结
器学习预测模型3 大类［3］。与传统的确定型和统果的准确率达70%以上。由于传统BP 神经网络收
计学模型相比，机器学习模型具有良好的泛化能敛速度慢、易陷入局部最优，粒子群、灰狼、遗传算法

收稿日期: 2021-09-21
基金项目: 国家自然科学基金( 41674013; 41874012)
作者简介: 赵侃( 1997—) ，男，硕士，助理主程师，主要研究方向为环境遥感。E-mail: 19210061015@ stu．xust．edu．cn
通信作者: 师芸。E-mail: shiyun0908@ hotmail．com

<!-- 第 2 页 -->

# 2022 年第10 期赵侃，等: 基于改进麻雀搜索算法优化BP 神经网络的PM2. 5 浓度预测 45
等元启发式算法被广泛应用于BP 神经网络优化。发现者位置的更新规则为

### {

#### ( )
文献［6］利用遗传算法优化BP 神经网络，对PM2. 5 浓－i
Xti，jexp R2 ＜ST
度进行了预测，该模型具有较好的学习、泛化能力，但 Xt+1i，j = αImax ( 1)
未考虑气象因素的影响。文献［7］利用粒子群优化 Xti，j + QL R2 ≥ST
算法改进遗传算法，优化BP 神经网络的初始权值和式中，t 为当前迭代数; Xt+1i，j 为t + 1 次迭代中第i 只麻
阈值，获得了良好的PM2. 5 浓度预测效果。雀在第j 维中的位置; Imax 为最大迭代数; α 为( 0，1］中
针对上述元启发式算法存在的寻优能力差、收的随机数; R2 和ST 分别代表警戒值和安全值; Q 为服
敛速度慢等问题，本文提出一种改进麻雀搜索算法从正态分布的随机数; L 为一行多维的全一矩阵。
( improved sparrow search algorithm，ISSA) ，对BP 神追随者位置的更新规则为

## {

#### ( )
经网络模型的初始权值和阈值进行优化，避免模型 Xtworst －Xt i ＞n
i，j
Qexp
陷入局部最优; 结合西安市2016—2021 年逐日的空 Xt+1i，j = i2 2 ( 2)
气质量和气象数据，利用ISSA-BP 神经网络模型进 t+1 t+1 + L
X + Xti，j －X A 其他
p p
行PM2. 5 浓度预测，并与BP 神经网络、SSA-BP 神经式中，Xp 为发现者所在的最佳位置; Xworst 为当前全
网络预测结果进行对比，以验证ISSA-BP 的可靠性。局最差位置; A 为一行多维的元素为1 或－1 的矩
+ = A －1。
阵，A T( AAT)

#### 1 ISSA-BP 神经网络模型
警戒者位置的更新规则为

# {

### 1. 1 BP 神经网络 tbest + β Xti，j －Xt

X fi ＞fg
best

#### BP 神经网络是由文献［8—9］首次提出的一种 ( )
Xt+1i，j = Xti，j －Xt ( 3)
Xti，j + K worst fi = fg
根据误差进行训练的多层反向反馈神经网络模型。
( fi －fw) + ε
该模型的特点是信号向前传播，误差向后传播，实
式中，Xbest 为当前全局最佳位置; β 为步长控制参
现一种从输入到输出的任意的非线性映射［10］。BP
数; fi 为当前适应度; fg 和fw 分别为当前最佳和最差
神经网络模型分为输入层、隐含层、输出层3 层网络
适应度; ε 为一个避免分母为0 的常数; K 为［－1，1］
结构。正向传播中，输入信号经隐含层分配权重，
中的随机数。
传递到输出层计算输出值。正向传播完成后，若预改进麻雀搜索算法

### 1. 3

测结果超出期望误差，则利用反向传播修改权值和改进麻雀搜索算法首先利用PWLCM 混沌映射
阈值，得到最优参数，以建立模型［11-12］。图1 为BP
初始化种群，增强全局搜索能力; 然后在更新发现
神经网络的结构示意图。者位置时加入非线性权重，协调局部搜索和全局搜
索能力，加快收敛速度; 最后利用萤火虫扰动优化
策略对最优解位置进行扰动，产生新解，避免陷入
局部最优。

### 1. 3. 1 混沌映射

SSA 采用随机生成的方式对种群进行初始化，
使得麻雀种群分布均匀，影响后期迭代寻优。而混
沌映射具有随机性和规律性，对初始条件和遍历性
较敏感，可使用混沌序列对麻雀种群进行初始
化［16］。目前常用的混沌映射有Logistics 映射［17］、
图1 BP 神经网络结构［18］、PWLCM 映射［19］等。其中PWLCM 映
Tent 映射
射更加均匀且分布稳定，本文采用该映射进行种群

### 1. 2 麻雀搜索算法

初始化，其表达式为
SSA( sparrow search algorithm) 是受麻雀觅食行
 xi－1
为和反捕食行为启发而提出的一种新型群智能优 0 ≤xi－1 ＜β

β
化算法，与其他算法相比，具有搜索精度高、稳健性
 ( xi－1 －β)
强的特点［13-14］。麻雀种群内部存在明显的分工，一
xi =  β ≤xi－1 ＜0. 5 ( 4)

### 0. 5 －β

部分麻雀负责觅食并提供觅食指导，其余麻雀则进
 0 xi－1 = 0. 5
行食物获取。同时，麻雀意识到危险时，会及时发

出警报信号，整个种群将立刻做出反捕食行为［15］。 F( 1 －xi－1，β) 0. 5 ＜xi－1 ＜1. 0

<!-- 第 3 页 -->

# 46 测绘通报 2022 年第10 期
式中，β 为控制参数。为控制参数β 和x0 赋值，经循者位置更新规则进行位置更新。
环迭代得到0～1 的随机序列。 ( 6) 将剩余个体作为追随者，并按照位置更新
1. 3. 2 非线性惯性权重规则更新位置。
SSA 算法中缺乏对于步长的有效控制，发现最 ( 7) 随机选取部分个体为警戒者，进行位置
优解后，其他个体迅速向最优解靠拢，难以协调局更新。
部寻优和全局寻优能力，从而陷入局部最优。因 ( 8) 计算更新后种群的适应度，找到全局最
此，引入非线性惯性权重控制搜索范围和收敛速优个体，对其进行萤火虫扰动，产生新解。
度［16，20］。惯性权重计算方式为 ( 9) 计算种群适应度，判断是否达到结束条件。

#### ( tmax+t) 若是，则程序结束，输出最优解; 否则跳转至步骤
1－tmax－t
ω = e ( 5) ( 2) ，继续执行。
在迭代过程中，随着惯性权重的不断自适应变 ( 10) 将网络最优结构参数输入BP 神经网络结
化，将有利于协调算法在探索与开发之间的平衡，构中，进行网络训练。
改进后的发现者位置更新规则为 1. 5 模型评价指标

#### {
xti，jω R2 ＜ST 针对PM2. 5 浓度预测这一回归问题，本文采用
xt+1i，j = ( 6)
xti，j + Q R2 ≥ST 均方根误差( RMSE) 、平均绝对误差( MAE) 和平均
绝对百分误差( MAPE) 作为BP、SSA-BP、ISSA-BP

### 1. 3. 3 萤火虫扰动优化策略

神经网络预测模型的评价指标，公式分别为
在萤火虫优化算法中，萤火虫的位置表示优化
问题的可行解，亮度对应萤火虫位置的适应度值。 1 n

#### RMSE = n ∑( yi －y*i ) 2 ( 10)
萤火虫不断向更亮萤火虫移动，以搜索更优位置， i = 1
直至搜索到优化问题的最优解，完成寻优 MAE = 1 n

#### n ∑ yi －y* ( 11)
［21-22］。 i
任务 i = 1
MAPE = 1 n yi －y*
萤火虫的相对荧光亮度为 i

#### n ∑ ( 12)
－γri，j yi
I = I0e ( 7) i = 1
式中，n 为样本数量; yi 为实际值; y*i 为预测值。
式中，I0 为萤火虫的固有亮度; γ 为光亮度吸收系

#### 数; r 为任意两个个体间的空间距离。 2 实例分析
萤火虫的相互吸引力公式为

### 2. 1 试验数据

－γr2
β = β0e i，j ( 8)
PM2. 5 浓度变化受空气污染物和气象因素的共
式中，β0 为最大吸引度; γ 为光亮度吸收系数; r 为任
同影响。本文利用西安市2016 年1 月至2020 年
意两个个体间的空间距离。 12 月逐日的空气污染物和气象数据，对PM2. 5 浓度
萤火虫i 被吸引向萤火虫j 移动的位置更新公
预测模型进行研究。空气质量数据来自中国环境
式为监测总站空气质量实时发布平台，包括PM2. 5、
xi = xi + β( xj －xi) + α( rand －1 /2) ( 9) PM10、SO2、NO2、O3、CO。其中，CO 的浓度单位为
式中，xi、xj 为萤火虫i 和j 所处在的空间位置; α 为 3，其余5 类的浓度单位为μg /m3，观测数据采
mg /m
步长因子; rand 为服从均匀分布的随机数。样率分别为1 d。气象数据来源于美国国家海洋和

### 1. 4 ISSA-BP 算法步骤大气管理局国家环境信息中心的全球地面国际交

( 1) 初始化预测网络，确定输入层、隐含层及输换站57131 泾河站逐日的观测数据。其中，逐日观
出层的节点数。测数据包括平均气温、露点温度、海平面气压、平均

#### ( 2) 利用PWCLM 混沌映射初始化种群，将模风速，采样率为1 d。
型中的权值和阈值表示为ISSA 算法中d 维空间 2. 2 数据预处理
向量。由于空气质量和气象数据存在缺失现象，因此

#### ( 3) 完成ISSA 参数初始化。需对缺失数据进行插值。根据数据特点，选用线性

#### ( 4) 计算个体适应度值并排序，得到最优和最插值法进行填充，公式为
差适应度及其对应个体位置。 yt = yu + yv －yu
v －u ( t －u) ( 13)

#### ( 5) 选取位置较优的个体为发现者，按照发现

<!-- 第 4 页 -->

# 2022 年第10 期赵侃，等: 基于改进麻雀搜索算法优化BP 神经网络的PM2. 5 浓度预测 47

式中，t 为缺失数据所在的时间点; u 和v 分别为t 时出层节点数; z 为1 ～10 之间的整数。试凑法最终
刻前后未缺失数据的时间点; yu 和yv 分别为u 和v时确定的隐含层节点数为11 层。
刻的数据值; yt 为插值结果。

#### 3 试验结果分析
由于空气质量数据和气象数据的量纲和数量
级不同，会影响网络训练过程和算法收敛速度，因根据以上参数建立ISSA-BP 神经网络，进行
此需对数据进行归一化处理，公式为 PM2. 5 浓度预测，以2016 年1 月至2020 年11 月为
y －ymin 输入数据，预测2020 年12 月的PM2. 5 浓度。图3
M = ( 14)
ymax －ymin 为逐日预测结果的绝对误差。表1 为逐日的预测结
式中，M 为归一化后的变量值; y 为变量原始值; ymin 果精度统计。
为变量最小值; ymax 为变量最大值。

### 2. 3 数据相关性分析

PM2. 5 浓度易受其他污染物浓度变化影响，并
与气象因素具有一定相关性。因此，利用与PM2. 5
显著相关的影响因素建立预测模型。在SPSS 软件
中进行PM2. 5 浓度与影响因素之间的相关性分析，
结果如图2 所示。可以看出，PM2. 5 浓度与影响因
子均为显著相关。

图3 PM2. 5 浓度预测结果
由图3 可知，BP 神经网络模型的预测值与实际
值偏差过大，尤其是在PM2. 5 浓度波动较大时，预测
值与实际值偏差更大。SSA-BP 与本文提出的ISSA-
BP 神经网络模型预测能力有明显提升，但与ISSA-
BP 神经网络模型相比，SSA-BP 神经网络在局部时
间段预测结果与实际值仍存在一定偏差。ISSA-BP
神经网络预测模型在所有时间段都有较好的预测
结果，能够有效学习突变时刻的预测信息，有效避
免了PM2. 5 浓度突变时预测偏差过大的情况。
图2 SPSS 相关性分析结果
表1 逐日PM2. 5 浓度预测精度指标

### 2. 4 模型相关参数

模型 RMSE/( mg/m3) MAPE/( %) MAE/( mg/m3)
分别采用BP、SSA-BP、ISSA-BP 神经网络模型
BP 13. 95 25. 53 10. 92
进行PM2. 5 浓度逐日的预测，预测输入数据为10
SSA-BP 8. 57 12. 46 6. 77
维，输出数据为1 维。网络模型的训练次数固定为
ISSA-BP 4. 87 8. 73 3. 43

# 1000 次，学习率为0. 000 1，分别使用tansig 和
purelin 函数作为输入-隐含层和隐含-输入层的激活由表1 可知，逐日PM2. 5 浓度预测中，SSA-BP
函数，SSA 和ISSA 的种群数量和迭代次数分别设为和ISSA-BP 神经网络预测误差离散性较小，RMSE

# 100 和200。值明显减小，BP 神经网络、SSA-BP 神经网络、ISSA-
隐含层节点数首先由经验公式确定，然后采用 BP 神经网络预测模型的RMSE 值分别为13. 95、
试凑法选取训练集均方根误差小的值作为隐含层 8. 57、4. 87 mg /m3，ISSA-BP 模型的预测精度最高。
节点数。经验公式为逐时PM2. 5 浓度预测中，BP 神经网络、SSA-BP 神
m = n + l + z ( 15) 经网络、ISSA-BP 神经网络的MAPE 指标分别为
式中，m 为隐含层节点数; n 为输入层节点数; l 为输 25. 53%、12. 46%、8. 73%，说明SSA-BP 和ISSA-BP

<!-- 第 5 页 -->

# 48 测绘通报 2022 年第10 期

神经网络预测结果优于BP 神经网络，且ISSA-BP 度学习网络预测具有广阔的应用前景。
神经网络预测结果最好。根据MAE 指标，SSA-BP
参考文献:
和ISSA-BP 神经网络的预测精度明显提升，其中
ISSA-BP 神经网络的预测精度最高。综上所述，本［1］ DI Qian，KOUTRAKIS P，SCHWARTZ J． A hybrid
文建立的ISSA-BP 神经网络预测模型学习能力强、 prediction model for PM2. 5 mass and components using a
容错性好，能够有效防止数据过拟合，具有稳定的 chemical transport model and land use regression［J］．
Atmospheric Environment，2016，131: 390-399．
预测能力和较强的稳健性。
［2］ ZHAO Rui，GU Xinxin，XUE Bing，et al．Short period
以训练数据集和测试数据集整体均方误差平
PM2. 5 prediction based on multivariate linear regression
均值为适应度函数，其值越小，说明模型具有可靠
model［J］．PLoS One，2018，13( 7) : e0201011．
的泛化能力和稳健性。SSA-BP 和ISSA-BP 神经网
［3］贾澎涛，何华灿，刘丽，等．时间序列数据挖掘综述
络的适应度曲线如图4 所示，SSA-BP 神经网络模型
［J］．计算机应用研究，2007，24( 11) : 15-18．
适应度陷入了局部最优，ISSA-BP 与SSA-BP 相比跳［4］高愈霄，汪巍，黄永海，等．基于神经网络和数值模
出了局部最优，获得了更优的收敛精度，说明改进型的重点区域PM2. 5 预报比较分析［J］．环境科学，
后的SSA 具有更高的准确度、更好的稳定性及效率 2022，43( 2) : 663-674．
更高的全局最优搜索能力。［5］孙宝磊，孙暠，张朝能，等．基于BP 神经网络的大
气污染物浓度预测［J］．环境科学学报，2017，37

#### ( 5) : 1864-1871．
［6］杨云，付彦丽．关于空气中PM2. 5 质量浓度预测研究
［J］．计算机仿真，2016，33( 3) : 413-418．
［7］张旭，杜景林．改进PSO-GA-BP 的PM2. 5 浓度预测
［J］．计算机工程与设计，2019，40( 6) : 1718-1723．
［8］ RUMELHART D E，HINTON G E，WILLIAMS R J．
Learning representations by back-propagating errors［J］．
Nature，1986，323( 6088) : 533-536．
［9］ RUMELHART D E，MCCLELLAND J L，GROUP P R．
Parallel distributed processing: explorations in the
microstructure of cognition，Volume 1: foundations［Z］．
Cambridge，Ma: MIT Press，1986．
图4 PM2. 5 浓度预测适应度曲线［10］黄丽．BP 神经网络算法改进及应用研究［D］．重庆:
重庆师范大学，2008．

#### 4 结论［11］CHEN Yegang． Prediction algorithm of PM2. 5 mass
concentration based on adaptive BP neural network［J］．
本文融合PWCLM 映射、非线性惯性权重、萤火
Computing，2018，100( 8) : 825-838．
虫优化扰动，改进了麻雀搜索算法，进行了BP 神经
［12］胡娟，郑军，许文龙，等．利用多源数据建立GA-BP
网络初始权值和阈值优化，具有良好的泛化能力和算法模型估算PM2. 5 的研究［J］．气象科学，2021，
收敛速度; 结合西安市的空气质量数据和气象数 41( 3) : 314-322．
据，对PM2. 5 进行了预测，并与BP 和SSA-BP 神经［13］薛建凯．一种新型的群智能优化技术的研究与应用:
网络预测结果进行对比，结论如下。麻雀搜索算法［D］．上海: 东华大学，2020．
( 1) 改进后的麻雀搜索算法具有更高的准确［14］XUE Jiankai，SHEN Bo．A novel swarm intelligence
optimization approach: sparrow search algorithm［J］．
度、更优的收敛精度，有效避免了优化过程中陷入
Systems Science ＆Control Engineering，2020，8( 1) :
局部最优的现象。
22-34．

#### ( 2) 在BP、SSA-BP、ISSA-BP 神经网络预测模
［15］ZHANG Jiangnan，XIA Kewen，HE Ziping，et al．
型预测结果的精度评定指标中，SSA-BP 和ISSA-BP
Semi-supervised ensemble classifier with improved
神经网络指标优于BP 神经网络，其中ISSA-BP 更
sparrow search algorithm and its application in
优于SSA-BP，预测精度最高。 pulmonary nodule detection［J］．Mathematical Problems
改进的ISSA-BP 模型适用于PM2. 5 浓度预测， in Engineering，2021: 1-18．
能够为政府机构治理空气污染提供理论依据。深 ( 下转第104 页)

<!-- 第 6 页 -->

# 104 测绘通报 2022 年第10 期

［4］ SUN X F，ROSIN P L，MARTIN R R，et al．Fast and 的点云法向量估计方法［J］．测绘科学，2019，44
effective feature-preserving mesh denoising［J］．IEEE ( 10) : 101-108．
Transactions on Visualization and Computer Graphics，［10］王丽辉，袁保宗．鲁棒的模糊C 均值和点云双边滤波
2007，13( 5) : 925-938．去噪［J］．北京交通大学学报，2008，32( 2) : 18-21．
［5］曹爽，岳建平，马文．基于特征选择的双边滤波点云［11］宣伟．地面激光点云数据质量评价与三维模型快速
去噪算法［J］．东南大学学报( 自然科学版) ，2013，43 重建技术研究［D］．武汉: 武汉大学，2017: 73-74．
( S2) : 351-354．［12］杨荣华．地面三维激光扫描电晕角度分辨率与数据
［6］朱德海．点云库PCL 学习教程［M］．北京: 北京航空处理模型研究［D］．武汉: 武汉大学，2011: 90-104．
航天大学出版社，2012: 274-281．［13］武剑洁．基于点的散乱点云处理技术的研究［D］．武
［7］陆建华，刘闯，吕志才．最优邻域二次误差曲面的点汉: 华中科技大学，2004: 38-45．
云简化算法［J］．测绘通报，2018( 12) : 101-104．［14］傅祖芸．信息论: 基础理论与应用［M］．北京: 电子工
［8］ YANG Bisheng，DONG Zhen． A shape-based 业出版社，2001: 15-18．
segmentation method for mobile laser scanning point ［15］陈西江，章光，花向红．于法向量夹角信息熵的点云
clouds ［J］．ISPRS Journal of Photogrammetry and 简化算法［J］．中国激光，2015，42( 8) : 336-344．
Remote Sensing，2013，81: 19-30． ( 责任编辑: 侯琳)
［9］宣伟，花向红，邹进贵，等．自适应最优邻域尺寸选择

- •••••••••••••••••••••••••••••••••••••••••••••
( 上接第48 页)
［16］毛清华，张强．融合柯西变异和反向学习的改进麻 piecewise linear chaotic map［J］．Applied Mathematics
雀算法［J］．计算机科学与探索，2021，15 ( 6) : and Computation，2007，190( 2) : 1637-1645．
1155-1164．［20］段玉先，刘昌云．基于Sobol 序列和纵横交叉策略的麻
［17］PAREEK N K，PATIDAR V，SUD K K． Image 雀搜索算法［J］．计算机应用，2022，42( 1) : 36-43．
encryption using chaotic logistic map［J］．Image and ［21］YANG Xinshe，HE Xingshi．Firefly algorithm: recent
Vision Computing，2006，24( 9) : 926-934． advances and applications［J］．International Journal of
［18］LI Chunhu，LUO Guangchun，QIN Ke，et al．An image Swarm Intelligence，2013，1( 1) : 36．
encryption scheme based on chaotic tent map ［J］．［22］YANG Xin she．Firefly algorithm，stochastic test functions
Nonlinear Dynamics，2017，87( 1) : 127-133． and design optimization［J］．International Journal of Bio-
［19］XIANG Tao，LIAO Xiaofeng，WONG K W．An improved Inspired Computation，2010，2( 2) : 78-84．
particle swarm optimization algorithm combined with ( 责任编辑: 纪银晓)

- •••••••••••••••••••••••••••••••••••••••••••••
( 上接第85 页)
［14］麻学锋，杨雪．大湘西高级别景区时空分布特征及［19］禹文豪，艾廷华，周启．设施POI 的局部空间同位模
影响因素的空间异质性［J］．自然资源学报，2019，式挖掘及范围界定［J］．地理与地理信息科学，
34( 9) : 1902-1916． 2015，31( 4) : 6-11．
［15］周涛，陆惠玲，任海玲，等．基于粗糙集的属性约简［20］BARUA S，SANDER J．Mining statistically significant
算法综述［J］．电子学报，2021，49( 7) : 1439-1449． co-location and segregation patterns ［J ］． IEEE
［16］JIANG H B，HU B Q．A decision-theoretic fuzzy rough Transactions on Knowledge and Data Engineering，2014，
set in hesitant fuzzy information systems and its 26( 5) : 1185-1199．
application in multi-attribute decision-making ［J］．［21］MOHAN P，SHEKHAR S，SHINE J A，et al．A
Information Sciences，2021，579: 103-127． neighborhood graph based approach to regional co-
［17］魏中宇．地铁建设对城市内部土地利用变化的影响: location pattern discovery: a summary of results［C］/ /
以西安地铁1、2 号线为例［D］．西安: 陕西师范大 Proceedings of the 19th ACM SIGSPATIAL International
学，2019． Conference on Advances in Geographic Information
［18］卢阳禄．基于高分影像的道路交通对建设用地功能 Systems．Chicago，USA: ［s．n．］，2011: 122-132．
格局的影响分析: 以从化区中心城区规划区为例 ( 责任编辑: 胡淼)
［D］．广州: 华南农业大学，2016．
