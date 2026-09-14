<!-- 第 1 页 -->
第21卷第7期 Vol.21  No.7

#### 软件工程    SOFTWARE ENGINEERING
2018年7月 Jul.  2018

文章编号：2096-1472(2018)-07-36-03 DOI:10.19644/j.cnki.issn2096-1472.2018.07.010

## 基于模拟退火算法优化的BP神经网络预测模型

### 蒋美云
(南京工业职业技术学院计算机与软件学院，江苏 南京 210023)

摘  要：神经网络算法是深度学习研究的重点，遗传算法是一种自适应优化搜索算法，模拟退火算法是寻找最优

# 公众号：数学建模老哥
解的算法，本文主要分析了神经网络，遗传算法和模拟退火算法的特点和缺陷，研究BP神经网络和遗传模拟退火算法
相结合的技术，从发挥算法的优点基础上，提出了一个基于模拟退火遗传算法的BP神经网络模型，并应用于某观影俱
乐部，作为新电影上映预测和用户推荐，实验结果表明：该算法在收敛性和准确率上都有较好的效果。
关键词：BP神经网络；模拟退火；遗传算法；收敛
中图分类号：TP391     文献标识码：A

#### A Predication Model of BP Neural Network Based on Genetic

#### Simulated Annealing Algorithms

#### JIANG Meiyun
( Department of Computer and Software,Nanjing Institute of Industry Technology,Nanjing 210023,China)

Abstract:The Neural Network Algorithm is a focus of deep learning,Genetic Algorithm is to search adaptive
optimization and Genetic Simulated Annealing Algorithm is to find the optimal solution.Analyzing the characteristics and
defects of these three algorithms as well as studying the technology of combining BP neural network with genetic simulated
annealing algorithm,this paper proposes a new BP neural network model based on genetic simulated annealing algorithm
from getting the advantages of the algorithm,and the new algorithm has been used in a movie club,where the experimental
results show that this algorithm has better effects on the convergence and accuracy.
Keywords:BP neural network;simulated annealing;Genetic Algorithm;convergence

#### 1   引言(Introduction)  致误差大，预测精度低等局限性。
神经网络作为人工智能的重要组成部分，一直是神经 遗传算法[3,4]GA是一种仿生算法，该算法模拟生物在自然
科学、认知科学、行为科学、计算机科学等关注的焦点。 环境中的遗传和进化过程而形成的一种自适应全局优化概率
自AlphaGo击败职业围棋选手，第一次战胜人类围棋冠军以 搜索算法。遗传算法以求得最适应环境个体为目的，从任意
来，人类再次掀起了研究机器学习，深度学习的热潮。神经 一个初始群体出发，经过选择、交叉、变异操作来产生一个
网络作为深度学习的基本模型，吸引了大批研究人员的注 更适应环境的新的个体，经过多次迭代，使得新群体进化到
意，在神经网络的理论模型，开发工具，学习算法等方面经 搜索空间中越来越好的区域，经过一代代的进化，最后收敛
过多年研究，在语音识别，图像识别，非线性预测模型，模 到一群最适应环境的个体，求得最优解。
式识别等方面取得令人瞩目的成就。我们国家决定从今年开始 模拟退火算法[4]SA从设定一个较高温度开始，伴随温度
大力发展基于大数据的人工智能，即机器学习和深度学习。 参数的不断下降，结合概率突跳特性在解空间中随机寻找目
人工神经网络[1]是能模拟和反映人脑部分特征的一种仿 标函数的全局最优解的过程。
真信息处理系统,该系统基于模仿人脑系统的结构和功能而设 由于BP神经网络易于陷入局部极小值，收敛速度慢等问
计。从神经网络建模或神经网络学习预测的角度分析，神经 题[2,5]，采用梯度下降寻优迭代次数多，效率低下，而GA和
网络都必须包含神经网络拓扑结构[2]，即学习模型，神经元 SA都是基于概率分布机制的优化算法，两者结合，使用SA可
特征函数和目标函数，机器学习算法，存在对训练样本要求 以避免GA早熟问题，从而增强全局和局部搜索能力，本文在
高，数据量要求大的困难，而对于小数据训练样本则容易导 此基础上提出模拟退火遗传算法优化的BP神经网络算法，并

<!-- 第 2 页 -->
第21卷第7期                                                                                                          37蒋美云：基于模拟退火算法优化的BP神经网络预测模型

建立模型用于预测。 ∑=(I,Q,T,X)
2 基于遗传模拟退火的BP神经网络(BP neural  其中，I={i1,i2,…,im}是初始输入集合，即神经元节点的值；
network based on genetic simulated annealing  Q是一个权值W的矩阵，其原始值随机生成；

#### algorithm) T是一个阈值的矩阵，原始值随机生成；

#### 2.1   遗传模拟退火算法 X是一个w*t的矩阵，对应输入层到第一个隐藏层的阈值
遗传模拟退火算法是将遗传算法和模拟退火算法相结 矩阵，获知第一个隐藏层到第二个隐藏层的阈值矩阵……
合，模拟退火算法具有较强的全局搜索能力寻得最优解的效 设计输出误差作为目标函数： ，
率高，并能使搜索过程避免陷入局部最优解，但模拟退火算 算法求解的过程就是利用模拟退火算法寻求最优解的过程。

#### 法对全局解空间了解不多。而遗传算法的局部搜索能力较 3.2   算法
差，易于陷入局部最优解，但把握搜索过程的总体能力较 Begin

# 公众号：数学建模老哥
强，遗传模拟退火算法以提高算法效率为目的，结合了遗传 While不满足性能要求do
算法和模拟退火算法的优点。    Temp=10；
遗传模拟算法[3]从一组随机产生的初始解开始进行全局最    ‘产生初始任务集；
优解的搜索过程，该过程正好符合反向神经网络解空间最优 ∑=(I,Q,T,X)；
值的搜寻，通过选择、交叉、变异等遗传操作产生一组新的 TA={I，R[1..n]}；
个体，热后对所产生的各个个体进行模拟退火过程，类似随    当temp==1循环
机梯度下降法，以其结果作为下一代群体中的个体。      i’=crossover(i)；’对样本进行交叉运算

#### 2.2   BP神经网络      i’’=mutation(i’)；’样本进行变异运算
BP神经网络[6,7]，也叫反向传播神经网络，按反向误差      ‘根据目标函数对每个个体进行模拟退火即选择；
传播算法训练权重和阈值的多层神经网络，采用梯度下降算 ；’目标函数
法作为优化函数，对权重和阈值的误差求导，获得新的权值 如果(∆di<0)
和阈值来跟新整个神经网络的权值和阈值，以求得全局最小 则采用新方案
值。误差计算通常用LSM[8]公式，计算如下：
否则{计算prob=exp ；
随机产生一个rand(0<rand<1)；
如果(prob<rand)则采用新方案；
其中，outputs是神经网络输出集合，D是所有训练样本的集               否则放弃新方案；
合，tkd是和训练样本d对应的第k个真实值，okd是与训练样例d }
对应的第k个输出值。这个函数的解空间有对应无数函数，构 temp=temp*a；
成了一个搜索误差曲面[8]，需要在这个解空间上找到这个曲面 BP神经网络算法训练
上的最小值点即最优解。问题转化为在曲面空间求极值，为 end；

#### 了保证能找到最小值，确保算法快速收敛，优化效率提升， 3.3   算法分析
合适的学习步长是一个重要参数，不宜太大也不宜太小。 该算法的优化过程是基于对目标函数的最小化过程，∆di

#### 2.3   基于遗传模拟退火的BP神经网络 的最小化过程模拟自然界的退火过程，由一个逐步冷却的温
利用模拟退火算法[3]优化遗传算法并利用遗传算法的全局 度temp来控制，一个冷却机制Tempi+1=α*tempi，α称为冷
寻优搜索功能，获得每一次的最优种群(权重和阈值)，接着利 却率，0<α<1,此处α用作神经网络的步长，步长的大小影
用BP的局部寻优特征反向寻得最优值[9]。  响最小化的过程，模拟退火算法易于避免陷入局部最优，结

#### 3  基于遗传模拟退火的BP神经网络算法及模型(The 合遗产算法全局搜索提高算法效率。
BP neural network algorithm and model based K是玻尔兹曼常数，temp也可以看成是一个常数。

#### on genetic simulated annealing algorithms) 3.4   数据模型

#### 3.1   数据模型 首先需要一个强大的数据银行来建立模型，这些数
假设输入节点为三个i 1、i 2、i 3，隐藏节点为两个h 1、h 2, 据从MovieLens提供的数据库获得[10]，这些数据包括六个
输出节点为一个o的三次神经网络，随机生成初始BP神经网络 csv文件，一个影评文件，包括userId、movieId、rating、
权值和阈值。 timestamp；一个标签文件，包括userId、movieId、tag、
输入层到隐藏层权值W=[[ih11,ih12],[ih21,ih22],[ih31,ih32]] timestamp；一个电影文件，包括movieId、title、genres；
隐藏层的阈值t=[t1,t2] 一个链接文件(电影来源)，包括movieId、imdbId、tmdbId；
隐藏层到输出层权值OW=[[ho12],[h021]] 两个标记相关性文件，包括movieId、tagId、relevance、
输出层的阈值OT=[ot3] tagId、tag。这些数据显示每个观众观影信息及影评，本文的
为了使用遗传模拟退火对BP神经网络的权值和阈值进行 目标是利用遗传模拟退火的BP神经网络模型，对这些数据建
训练优化，根据任务，可以建立以下四元组： 立模型，通过对模型的训练进行预测。

<!-- 第 3 页 -->
38                                                    软件工程                                               2018年7月

预测某观影俱乐部中的n位会员对于某部电影的评分范 过调参后预测值可以更接近真实值。

#### 围，首先对电影tag和分类数据进行汇总处理，得到电影的特 4   结论(Conclusion)
征(电影类型和n个最高的tag)，计算电影A与某个用户曾经 传统的神经网络存在收敛效果差，易于陷入局部最小值
看过所有电影的相似度以相似度最高的影片的评分，作为评 等问题[13]，在本文中引入遗传算法和模拟退火算法，模拟退
分。实验数据描述见表1。 火符合随机梯度下降优化算法需求，能提高收敛速度和减少
表1 实验数据描述 迭代次数，提高算法效率，遗传算法是一种全局搜索优化算
Tab.1 Description of data
法，能改进传统神经网络陷入局部最优解的问题，从而提高
数据 条件属性 学习样本 测试样本 误差函数 算法的效率。本算法结合遗传算法和模拟退火算法，使得传

# 5000 8 4500 50 MSE 统BP神经网络算法在经过遗传模拟退火算法优化后不仅提高

# 公众号：数学建模老哥了收敛速度[14]，而且提高了预测精度。

#### 3.5   实验结果与分析

#### 参考文献(References)
通过特征提取降维操作，得到核心属性为五个
(A1,A2,A3,A4,A5),见表2。 [1] Lin Guangfeng,Caixia Fan,Hong Zhu,et al.Visual feature
表2 实验数据核心属性 coding based on heterogeneous structure fusion for   image
Tab.2 Key attributes of data classification[J].information Fusion,2017(36):275-283.
[2] 王崇骏,于汶滌,陈兆乾,等.一种基于遗传算法的BP神经网络
userId movieId tag timestamp relevance
算法及其应用[J].南京大学学报自然科学版,2003,5:1-4.

# 18 4141 Mark Waters 1240597190 3302500000000000
[3] 蒋美云.遗传模拟退火算法在云调度中的应用研究[J].计算机
65 208 Dark hero 1368150078 0569999999999995 与现代化,2013(13):3-4.
65 521 Noir thriller 1368149983 67625 [4] 何炎祥,陈莘萌.Agent和多Agent系统的设计与应用[M].武汉
采用十折交叉选取数据进行实验[11]，该实验预测某一 大学学术丛书:64-70.
影片的评分，loss是损失函数的大小,val_loss是validation_ [5] F Guzmán,S Joty,L Màrquez,et al.Machine translation
loss，指验证集的loss，均方误差。并通过Keras搭建神经网络 evaluation with neural networks[J].Computer Speech &
仿真平台获得以下实验结果[12]。 Language[J].2017(45):180-200.
[6] 刘浩然,赵翠香,李轩,等.一种基于改进遗传算法的神经网络
优化算法研究[J].仪器仪表学报,2016,37(7):1573-1580.
[7] 高玉明,张仁津.基于遗传算法和BP神经网络的房价预测分
析[J].计算机工程,2014,40(4):187-191.
[8] 曾小华,李广含,宋大凤,等.基于遗传算法优化的BP神
经网络侧翻预警算法[J].华南理工大学学报自然科学
版,2017,45(2):30-38.
[9] 何涛,张洪伟,邹书蓉.特征提取与多目标机器学习研究及应
图1 迭代次数和误差函数
用[J],四川理工学院学报(自然科学版)2013(1):30-35.
Fig.1 Iteration number and error function
[10] MR Mahdiani.A Modified Neural Network Model
从图1可以看出，基于模拟退火的BP神经网络有较好的收
for Predicting the Crude Oil Price[J].Intellectual
敛性，在迭代20次左右算法趋于收敛。收敛速度快，无锯齿
Economics,2017:22-30.
现象。
[11] https://www.superdatascience.com.
[12] AJD Silva.WRD Oliveira Comments on "Quantum
artificial neural networks with applications"[J].Information
Sciences,2016,370-371:120-122.
[13] JürgenSchmidhuber.Deep Learning in neural networks:An
overview[J].Neural Nerworks,2015(61):85-117.
[14] 王倩,王莹,邱继勤.基于灰色GM(1,1)和BP神经网络的房价
预测[J].时代金融,2012(36):332-333.

#### 作者简介：
图2 真实评分和预测评分对比 蒋美云(1977-)，女，硕士，讲师.研究领域：人工智能，机器
Fig.2 Comparison of real score and predicted score 学习，深度学习.
从图2可以看出，系统的预测值和真实值之间的比较，通
