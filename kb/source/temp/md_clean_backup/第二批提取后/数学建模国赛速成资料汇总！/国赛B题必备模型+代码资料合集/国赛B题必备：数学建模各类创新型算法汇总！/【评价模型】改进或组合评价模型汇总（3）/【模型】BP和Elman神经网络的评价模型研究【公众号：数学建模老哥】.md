<!-- 第 1 页 -->

#### 研究与开发

文章编号：1007-1423（2016）22-0003-05 DOI：10.3969/j.issn.1007-1423.2016.22.001

## BP 和Elman 神经网络评价针灸治疗颈椎病疗效研究

#### 韦晓燕1，张洪来1，魏航1，2，林秦烨1，谭火媛1，郭丽纯1

（1. 广州中医药大学医学信息工程学院，广州510006；2. 华南理工大学软件工程学院，广州510006）

# 公众号：数学建模老哥
摘要：

#### 基于PRO 量表在针灸治疗颈椎病的不确定性和复杂性，需要综合多种因子去衡量，且因子与输出的关系是非线性

#### 的，而人工神经网络模型能够解决非线性问题且适合于动态系统辨识，于是分别构建BP 和Elman 人工神经网络，通

#### 过MATLAB 软件运算，分析比较得出BP 模型比Elman 模型精度高，在针灸评价模型中效果更好。为针灸治疗颈椎病
提供相关理论指导。
关键词：

#### PRO 量表；BP 神经网络；Elman 神经网络；针灸评价
基金项目：
国家级创新创业训练项目（No.201510572017）、国家自然科学基金项目（No.81274003）、广东省自然科学基金项目（No.

#### 2015A030310312、2014A030309013）、广东省中医药科学基金研究项目（No.B2014174）





#### 0 引言 作用，因此本文采用BP 神经网络和Elman 神经网络建


立评价模型进行对比分析，为针灸治疗颈椎病疗效提
颈椎病是近些年来增长人数较快的一种疾病，严
供理论基础。
重危害人体的健康，国内外都对颈椎病做了很多的研

#### 究与探索[2-4]，国内也出现了评价针灸治疗颈椎病疗效 1 神经网络的基本原理

#### 的量表模式[5]。并且对PRO 量表进行了相关适用性研

#### 1.1 BP 神经网络

#### 究[6-7]。我们在此背景下采用了SF-36 量表[8]，基于病人

#### BP 神经网络是由多层构成的的前向网络，具备处

#### 自主报告病情，以VAS 疼痛量表[8]作为评分，来建立预
理线性不可分问题，包括输入层、隐含层和输出层，如图
测评价模型。由于颈椎病量表有很大的不确定性以及

#### 1。数据从输入层经隐含层向后传播，若输出层未能够得
复杂性，需要综合多种因子去衡量，且因子与结构的关
到期望输出则误差逆向传播，通过隐层向输入层返回修
系是非线性的，而人工神经网络有大规模的并行处理

#### 改权值直到误差最小。其基本原理和算法参见文献[10]。
以及信息存储能力，可以实现这种处理非线性系统，其
中神经网络中主要包括前向神经网络和反馈神经网

#### 络。BP 神经网络是前向神经网络的核心，由于BP 神经   
网络具有高度的非线性组合能力，处理问题较为广泛，
误差逆向传播，可以提高数据训练以及测试的准确度，
基于此曾做过颈椎病针灸疗效的相关研究[9]。此外由于

#### 量表数据是动态变化的，而Elman 神经网络是反馈型
的神经网络，有很高的稳定性，联想记忆功能，在复杂
度和复杂性中有更高的准确度，具有良好的动态模拟
图1 BP 神经网络模型

#### 髶

#### 现代计算机 2016.08 上

<!-- 第 2 页 -->

#### 研究与开发

#### 其中输入节点为xi，隐含层输出节点为yj，出节点为 隐含层：xk=f（w1xc（k）+w2（u（k-1）））

#### ok，wjk，vij 分别为隐含层到输出层，输入层到隐含层的连 承接层：xc（k）=x（k-1）

#### 接权值。f 为神经元的激活函数，网络的期望输出为dk， n

### 输出误差：e=k=1Σ（yk-dk）2

#### 输出误差为e，网络的各层输出关系为：

#### 输入层： 2 神经网络预测模型的建立与实现
m

### ok=f（j=0Σwjkyj）k=1，2，，3，…，l 2.1 数据的采集

# 公众号：数学建模老哥
本研究数据选自近年来在广东省中医院接受治
输出层：

#### 疗，纳入符合纳入标准的128 例颈椎病患者。以SF-36
n

### yj=f（i=0ΣVijXi），j=1，2，3，…，m 量表主要疗效指标，以视觉模拟评分（VAS）为次要疗
效指标。
输出误差：

#### 2.2 数据的预处理
l l m n
e= 1 k=1Σ（dk-ok）2= 1 k=1Σ{dk-f[j=0Σwjkf（i=0Σvijxi）]}2 （1）数据归一化。为了消除数据量纲的影响，所有

#### 2 2

#### 变量在数据集规范化为了在[0-1]区间内，即所有的变

#### 1.2 Elman 神经网络 量都是使用以下转换为图3 中公式来规范化，见表1：

#### 基本的Elman 神经网络由输入层、输出层、隐含 rij= xij-min{xij}

#### 层、连接层组成。与BP 网络相比，在结构上多了一个连 {xij}-min{xij}
接层，连接层的输出函数为线性函数，但是多了一个延 表1 归一化后的部分针灸数据
迟单元，可以记忆过去的状态，并在下一时刻与网络的

|� 学|��� 学建|������ 学建|表1 �������� 建|归一化后的部 ��������|部分针灸数据 ��������|据 ��������|��������|
|---|---|---|---|---|---|---|---|
|<br> <br>|<br> <br>|~~~~<br><br>|~~~~ ~~~~
<br><br>|~~~~ ~~~~<br><br>|~~~~ ~~~~ <br><br>|~~	~~<br><br>|~~~~ ~~~~<br>|
||<br>|<br>|<br>|<br>|<br>|<br>||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>||
||<br>|<br>|<br>|<br>|<br>|<br>||
|<br>|<br>|<br>|<br>|					<br>|						<br><br>|<br>||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>||
|<br>|<br>|<br>|<br>|<br>|<br> <br>|<br>||
||<br>|
<br>|
<br>|
<br>|
<br> <br>|
<br>|
|
||<br>|<br>|<br>|						<br>|					<br> <br>|<br>||
|<br>|<br>|<br>|<br>|<br>|<br>|<br>||
|<br> <br>|<br> 
<br>|<br>|	<br>|<br>|<br><br>|	<br>|	|

输入一起作为隐含层输入，使网络具有很强的联想记

#### 忆功能。其基本原理和算法参见文献[11]。


t 

t

tt
 t t

#### 

#### （2）因子分析。由于SF-36 量表中条目较多，且条

#### 目之间具有较高的相关性，在KMO 检验和Bartlett 检

#### 
 验中，本例中KMO 取值为0.773，标明可以进行因子分


#### 	
 析，Barlett 检验中sig=0.000，说明数据来自正态分布总

#### 体，适合作进一步分析。见表2。经主成分分析（Prin-

#### 图2 Elman 网络的结构模型 cipal Components Analysis，PCA），已累计贡献率大于一

#### 定百分比（如73.055%）的主成分数目为因子数目为8，

#### 其中，输入层节点为ur，隐含层输出节点为xn，承

#### 接层输出节点为xc，输出层节点为ym，w1，w2，w3 分别为 且经过因子旋转，因子得分计算，最终得到8 个因子的

#### 数据表，如表3。
承接层到隐含层、输入层到隐含层、隐含层到输出层的

#### 连接权值，g（·）为输出神经元的激活函数，f（·）为隐含 表2 KMO 检验和Bartlett 检验结果

#### 层神经元的激活函数，网络的期望输出为dk，输出误差

|Col1|  |Col3|
|---|---|---|
|"|$%&’||
|"|$%&’||
|#!|#!|#!|
|#!|#!||
||$ (||
||(((||

	
	

#### 为e。

#### 输入层：yk=g[w3x（k）]  !

#### 

#### 髷 现代计算机 2016.08 上

<!-- 第 3 页 -->

#### 研究与开发

####  表3 因子得分数据

|Col1|<br>|<br>|<br> |<br>  |<br>  | <br>  | <br>  | <br> | <br> |
|---|---|---|---|---|---|---|---|---|---|
||||
|||

	|
|		|
|
|||	|		|
	||			|	
|||
||||	
|
|	|
||	|	|
|||<br>			
|<br>	
	|<br>

|<br>|<br>	|<br>	|<br>	|<br>	|
|||
|


|		|			|
	|	|	
||
||<br>|
<br>|	<br>|	
<br>|	<br>|	<br>|<br>|<br>|
	<br>|
||<br>|<br>|	
<br>|
<br>|<br>|

<br>|
<br>|<br>|<br>|

# 公众号：数学建模老哥

#### 2.3 神经网络模型 线如图6 所示，在经过1000 次训练后，网络的性能达

#### （1）BP 神经网络模型的建立 到了要求。

#### 分析输入输出数据，建立多层BP 神经网络。其中

#### 输入变量8 个，输出变量1 个，在开始时放入比较少的
神经元，逐步增加隐层节点的数目，直到达到比较合理
的隐层节点数目为止。最后，神经网络模型的各层节点

#### 数分别为：输入层8 个，分别对应前文分析出来的8 个

#### 特征因子；隐含层的节点为7 个；输出层为1 个，如图3。


图4 训练误差图


图3 BP 神经网络结构图

#### 本次建模中，隐层采用S 型正切函数tansig，输出

#### 层采用S 型对数函数logsig。通过对不同的lr 和mc 的


#### 取值进行了考察，确定本文神经网络模型的参数为lr=
图5 Elman 神经网络结构图

#### 0.5，nc=0.9。误差根据实际情况确定，本文神经网络的

#### 误差界值为0.01 ，能够很好地满足网络的性能要求即

#### 在选代计算时误差值E≤0.01 时，则认为学习完成，停

#### 止计算，输出结果训练的误差变化曲线如图4 所示，

#### 在经过60 次训练后，神经网络的性能达到了要求。

#### （2）Elman 神经网络模型建立

#### 实验采用单隐层的Elman 神经网络，其中输入层

#### 神经元的个数为8；输出层神经元的个数为1。为了使
网络的诊断误差最小，经过多次训练检验，发现将隐含

#### 层神经元的个数设定为20，能够很好地满足网络的性

#### 能要求，如图5。

#### 将119 份的训练样本输入到Elman 神经网络中，
图6 Elman 神经网络训练误差图

#### 本文神经网络的误差界值为0.01。训练的误差变化曲

#### 髸

#### 现代计算机 2016.08 上

<!-- 第 4 页 -->

#### 研究与开发

#### 3 BP 与Elman神经网络的测试结果对比 病的疗效下具有切实可行性。但就预测误差与性能对

#### 分析 比分析发现BP 神经网络预测优于Elman 神经网络预

#### 测。因此，利用BP 神经网络模型能根据患者自主评估

#### 采用9 组测试样本分别在训练好的BP 和Elman

#### 填写的PRO 量表，来预测VAS 疼痛评分通过对于针灸

#### 网络预测。测试结果如表4 所示。结果显示BP 神经网
治疗前后以此判断针灸疗效，从而可以帮助医生针灸

#### 络测验的误差为0.0088，Elman 神经网络测验的误差
临床治疗提供参考。

#### 为0.1228。 对比两种神经网络的训练过程及检测结

# 公众号：数学建模老哥表4 BP 和Elman 测试结果对比

#### 果，可以得出BP 神经网络收敛速度相对较慢，而且有

#### 可能收敛于局部极小值；Elman 神经网络的参数调整 
	
  
	

|<br>|Col2|<br>|哥<br><br>|<br> |
|---|---|---|---|---|
||<br>|<br>|<br>|
<br>|
||<br>|<br>|<br>|<br>|
||<br>|<br>|<br>|<br>|
||<br>|<br>|<br>|<br>|
||<br>|<br>|<br>|	<br>|
||<br>|<br>|<br>|<br>|
||<br>|<br>|<br>	<br>|<br><br>|
||<br>|<br>|<br>|
<br>|
||!<br>||<br>|<br>|

#### 方便，与BP 神经网络相比诊断误差要大一些。因此，

#### 经过对比分析BP 神经网络构建针灸治疗颈椎病疗效
评价模型预测结果更优。

#### 4 结语

#### 从实验结果看出，使用BP 神经网络和Elman 神
经网络都可以实现针灸治疗颈椎病疗效的预测。可以

#### 得出人工神经网络在基于PRO 量表下针灸治疗颈椎

参考文献：
[1]梁兆晖，朱晓平，符文彬. 基于病人报告结局测量的针刺治疗颈椎病疗效评价及相关性分析. 颈腰痛杂志.2010（08）:1229-1232.
[2]熊键，谢青，鲍勇等. 颈椎病评定量表的研究进展[J]. Chinese Journal of Rehabilitation，2010，25（4）:296-297.
[3]针刺治疗颈椎病颈痛患者生存质量分析[J]. 针灸治疗痛症国际学术研讨会论文汇编，2009.5.15:3-6.
[4]Witt CM，Jena S，Brinkhaus B，et.al. Aeupuneture for Patients with Chronie Neck Pain[J]. Pain，2006，125（1-2）:98-106.
[5]劳丽陶等. 颈椎病针灸治疗评价中的病人报告结局评价模式探讨[J]. 广州：中医药导报.2010.8.28:2-3.
[6]张继福，梁兆辉等. 患者报告结局评价技术在针灸疗效评价中的适用性研究[J]. 广州：广州中医药大学学报.2012.3.20:1-3;
[7]张建源. 颈椎病疗效评价量表信度与效度考核[D]. 广州：广州中医药大学学报.2011.4.1:3-52.
[8]梁兆辉，朱小平等. 针刺治疗慢性颈椎病颈痛疗效评价[J]. 新中医.2008.10.5:1-2.
[9]王芳慧. 基于人工神经网络的PRO 评价针灸治疗颈椎病的疗效研究[D]. 广州.广州中医药大学，2014.:1-6.
[10]袁曾任. 人工神经网络及其应用[M]. 北京:清华大学出版社，2010: 78-125.
[11]陈明等. MATLAB 神经网络原理与实例精解[M]. 北京.清华大学出版社，2013.3:296-301.

作者简介：
韦晓燕，女（1996-），安徽阜阳人，本科，学生，研究方向为数据分析、人工神经网络
张洪来，男，山东人，医学博士，研究员，副主任中医师，研究方向为针灸治疗颈椎病及针灸临床资料数据挖掘
魏航，女，广东人，在读博士，讲师，研究方向为数理统计、机器学习与计算机应用
林秦烨（1994-），男，广东潮州人，在读本科，研究方向为数据分析
谭火媛（1993-），女，广东云浮人，在读本科，研究方向为机器学习、数据挖掘
郭丽纯（1993-），女，广东揭阳人，在读本科，研究方向为数据分析
收稿日期：2016-05-31 修稿日期：2016-07-28
（下转第12 页）

#### 髺 现代计算机 2016.08 上

<!-- 第 5 页 -->

#### 研究与开发

Research on PSO-SVR Based on Nonlinear Time Series in Dairy Cow

#### Movement Detection Model

#### WANG Yong-bo

（Patent Examination Cooperation Guangdong Center of the Patent Office of SIPO，Guangzhou 510530）

# 公众号：数学建模老哥
Abstract：
The livestock behavior and movements can be used for predicting its abnormal behavior like diseases or estrus and which has proved to
be of significance importance for the development of large-scale livestock production. Establishes a time series model used for motion
prediction based on particle swarm optimization (PSO) and support vector regression (SVR) and is optimized by using data collected with a
tri-axial accelerometer. By choosing the appropriate embedding dimension and epsilon-SVR parameters, establishes a time series model
to predict behavioral activity levels in cows. After training samples and choosing the appropriate embedding dimension and epsilon-SVR
parameters, uses some indicators for performance evaluation of regression. Experimental results show that, compared with an ARMA time
series model, the proposed method is more accurate and more credible, and it also provides a new way to produce real-time forecast of
cow behavior.
Keywords：
Time Series; Nonlinear Regression Analysis; Embedding Dimension; Particle Swarm Optimization(PSO); Support Vector Machine(SVR)

#### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

（上接第6 页）

Research on Effectiveness Assessment of Acupuncture for Cervical

#### Spondylosis Based on BP and Elman Neural Network

WEI Xiao-yan1，ZHANG Hong-lai1，WEI Hang1，2，LIN Qin-ye1，TAN Huo-yuan1，GUO Li-chun1

（1. School of Medical Information Engineering，Guangzhou University of Chinese Medicine，Guangzhou 510006；
2. School of Computer & Engineering，South China University of Technology，Guangzhou 510006）

Abstract：
Based on PRO scale in the acupuncture treatment of cervical spondylosis exists uncertainty and complexity, it is difficult to judge by a
single factor, but a comprehensive variety of factors to measure, and the relationship between the factor and the output is non-linear, and
the neural network model can approximate arbitrary nonlinear function and suitable for dynamic system identification feature, so con-
structs the evaluation model BP and Elman artificial neural network by MATLAB software operation, comparative examples drawn BP
model is higher than the Elman model accuracy.
Keywords：
PRO Scale; BP Neural Network; Elman Neural Network; Acupuncture Evaluation

#### 趯趤 现代计算机 2016.08 上
