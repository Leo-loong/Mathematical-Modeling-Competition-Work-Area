<!-- 第 1 页 -->

#### 第31 卷第3 期 Vo1.31 No.3

#### 自然灾害学报

#### 2022 年6 月 JOURNAL OF NATURAL DISASTERS Jun. 2022
文章编号：1004－4574（2022）03－0157－10 DOI：10.13577 / j.jnd.2022.0316

## 基于CRITIC法与TOPSIS地铁车站施工安全评价

#### 胥明1，许杰2，万友生1，覃君3，吴波2，谢云杰3
（1.南昌轨道交通集团有限公司，江西南昌330038；2.广西大学土木建筑工程学院，广西南宁530004；

### 3.中铁二局第六工程有限公司，四川成都610036）

> # 公众号：数学建模老哥

#### 摘要：地铁车站周边环境复杂，施工难度大，风险极高，具有较大的模糊性和不确定性，为保证其施

#### 工安全，提出采用CRITIC 法与逼近理想排序法（TOPSIS）相结合进行地铁车站施工的安全评价方法。

#### 选取人员、施工、环境和管理4个方面的主要因素，共建立20个三级评价指标，构建地铁车站施工安全

#### 评价指标体系，运用CRITIC 法计算各指标的权重，利用TOPSIS 对各评价指标进行综合决策，建立地

#### 铁车站安全评价模型。依托南昌市轨道交通3 号线车站工程项目，对该评价方法进行验证，结果表

#### 明：该方法能客观、合理地进行地铁车站施工安全评价，评价结果与工程实际情况相符合，该方法具有

#### 良好的实用性、客观性与准确性，可以给类似工程施工提供理论指导。

#### 关键词：施工安全评价；地铁车站；复杂环境；CRITIC；TOPSIS

#### 中图分类号：X947 文献标识码：A

#### Safety evaluation of subway station construction based on

#### CRITIC method and TOPSIS

#### XU Ming1，XU Jie2，WAN Yousheng1，QIN Jun3，WU Bo2，XIE Yunjie3
（1. Nanchang Rail Transit Group Co.，Ltd.，Nanchang 330038，China；
2. College of Civil Engineering and Architecture，Guangxi University，Nanning 530004，China；
3. China Railway Second Bureau Sixth Engineering Co.，Ltd.，Chengdu 610036，China）
Abstract：Due to the complex surrounding environment of subway station，subway construction is difficult and has
great risk，fuzziness and uncertainty. In order to ensure the safety of subway station construction，a safety evalua‐
tion method combining CRITIC method and the approximate ideal sequencing method（TOPSIS）is proposed. Se‐
lecting the main factors of personnel，construction，environment and management，a total of 20 three‐level evalua‐
tion indexes are established to construct the subway station construction safety evaluation index system. The subway
station safety evaluation model is established by using the CRITIC method and TOPSIS. Relying on the Nanchang
Rail Transit Line 3 station project，the evaluation model was verified，and the results were consistent with the actu‐
al safety status of the station，which verified the practicability，feasibility and accuracy of the model，and thus pro‐

#### vide theoretical guidance for similar projects.

|Key words|： construction safety evaluation；subway station；complex environment；CRITIC；TOPSIS|
|---|---|

收稿日期：2020－12－20；修回日期：2021－11－01
基金项目：国家自然基金面上项目（51678164，51478118）；广西自然科学基金项目（2018GXNSFDA138009）；广西科技计划项目（桂科
AD18126011）；广西大学科研基金项目（XTZ160590）；广东省高等职业院校珠江学者岗位计划资助项目（2019）
Supported by：National Natural Science Foundation of China （51678164，51478118）；Guangxi Natural Science Foundation Program
（2018GXNSFDA138009）；Guangxi Science and Technology Plan Projects（AD18126011）；Scientific Research Foundation of
Guangxi University（XTZ160590）；Guangdong Province Universities and Colleges Pearl River Scholar Funded Scheme（2019）
作者简介：胥明（1965－），男，高级工程师，主要从事城市轨道交通土建关键技术研究. E‐mail：1043436542@qq.com
通讯作者：吴波（1971－），男，教授，主要从事隧道与地下工程研究. E‐mail：wubo@gxu.edu.cn

<!-- 第 2 页 -->

#### 158 第31 卷

#### 自然灾害学报

### 引言

#### 随着我国经济的发展和城市人口的剧增，越来越多的城市兴建地铁以缓解日益增长的交通压力。地铁

#### 车站一般修建在城市繁华地区，且具有“深、大、近、难”的特征［1］，往往遇到周边环境复杂的情况：工程地质条

#### 件复杂、施工范围内管线众多、周围房屋密集、交通繁忙、周围居民较多，造成不确定因素多，风险大，施工困

#### 难的问题，需要对地铁车站施工安全做出科学合理的评价。

#### 地铁车站施工安全评价一般使用的方法为故障树法、模糊理论、熵权法、灰色关联度法、层次分析法和

#### 其他方法［2］。薛模美等［3］、周红波等［4］采用故障树法对基坑施工风险进行分析，得出施工各阶段的风险等级

#### 与风险控制措施。Guohua Zhang等［5］、李朝阳等［6］、吴波等［7］基于模糊理论确定施工风险因素的权重，建立了

> # 公众号：数学建模老哥
深基坑风险评估体系。Zhenhua Luo 等［8］、陈蓉芳等［9］、王景春等［10］利用熵权法对评价指标进行加权处理，构

#### 建地铁深基坑的风险评价体系。郎秋玲等［11］利用现场数据和灰色关联度法建立评价模型，对地铁深基坑开
挖稳定安全性进行评价。Yuanshun Shen 等［12］、李凤伟等［13］、聂菁等［14］采用层次分析法对地铁车站风险元素

#### 进行排序，进行安全风险分析。Ping Liu 等［15］使用粒子群优化算法（PSO）的支持向量机（SVM）模型，对地铁

#### 车站施工的安全风险进行预测。Luyuan Wu 等［16］将网络分析法（ANP）和模糊综合评判法（FCE）结合，可对

#### 地铁车站总风险等级进行评价。顾雷雨等［17］基于风险概率统计分析的理论，对复杂环境中基坑施工安全预

#### 警标准研究，提出了一种预警标准设计方法。姜安民等［18］基于突变级数法构建了地铁车站施工风险预测模

#### 型。上述方法虽能较好地对地铁车站基坑施工安全评价，但是却均有一些局限性，如故障树法计算复杂，且

#### 需事先知道所有基本事件发生的概率，否则无法进行定量分析；模糊综合评判法对指标权重矢量的确定主

#### 观性较强，结果可能会出现超模糊现象，分辨率差；熵权法仅依靠数据分析，客观性过强，计算结果常与工程

#### 实际有较大的偏差，无法体现决策者对各个安全评价指标的重视程度；灰色关联度法无法解决评价指标间

#### 相关造成的评价信息重复问题，对指标的最优值难以确定；层次分析法和模糊层次分析法过于依赖决策者

#### 的主观判断，可能受到主观偏好的不利影响。

#### 由此可见，国内外在分析复杂环境地铁车站施工安全性的研究较少，如何综合考虑安全评价指标的主、

#### 客观性，对其量化并确定权重是进行安全评价的关键。文中将CRITIC法与TOPSIS理论结合，综合考虑安全

#### 评价指标的主、客观性，并能将安全评价结果量化，形成一套地铁车站施工安全评价模型：CRITIC 法可以综

#### 合评价指标间的对比强度与冲突性，对评价指标进行客观赋权，将CRITIC 法与TOPSIS 理论相结合，可以克

#### 服采用传统的定性分析或经验模糊数学理论存在主观性大、可靠性不高的缺点，而TOPSIS 理论则可以对多

#### 评价指标进行合理排序、综合决策并求得具体的隶属度。经实例验证，将CRITIC法与TOPSIS理论两者结合

#### 能在地铁车站施工安全评价中得到较好的应用，评价结果较科学、准确，符合工程实际。

### 1 地铁车站施工安全评价流程

#### 1.1 安全评价指标体系

#### 表1

#### 地铁车站施工安全等级

#### Table 1 Safety level of subway

#### station construction
等级区间范围安全性描述损失严重程度
Ⅰ级 0 ≤r < 0.2
安全性极低灾难性的
Ⅱ级 0.2 ≤r < 0.4
安全性较低非常严重的
Ⅲ级 0.4 ≤r < 0.6
安全性中等严重的
Ⅳ级 0.6 ≤r < 0.8
安全性较高需考虑的
Ⅴ级 0.8 ≤r < 1
安全性高可忽略的

#### 图1

#### 地铁车站施工安全性评价指标体系

#### Fig. 1 Safety evaluation index system for subway station

#### construction in complex environment

<!-- 第 3 页 -->

#### 第3 期明，等：基于CRITIC法与TOPSIS地铁车站施工安全评价 159

#### 胥

#### 根据地铁车站施工情况和事故发生的机理，依据相关法律法规［19］和相关文献［20－24］，参考行业专家意见

#### 与类似工程案例，对地铁车站安全性评估系统进行全面分析，建立一套科学合理、操作性强的安全指标体

#### 系：建立4个二级指标，20个三级指标，如图1所示。

#### 为保证评价指标的一致性，结合概率论理论和专家评分习惯，参照相关规范标准［25］中风险发生可能性

#### 与损失等级，将地铁车站施工安全等级和安全性接受准则划分为5个级别，并按［0，1］区间取值，数值越大表

#### 示安全性越高，数值越小表示安全性越低，如表1和表2所示。

#### 表2

#### 地铁车站施工安全接受准则
Table 2 Safety acceptance criteria of subway station construction

> # 公众号：数学建模老哥等级安全接受准则安全对策
Ⅰ级亟需高度重视，采取强制措施规避，否则需降低接受准则至可以接受或不愿接
无法接受
受的水平
Ⅱ级
难以接受高度重视，采取必要的安全处理措施
Ⅲ级
不愿接受需要重视，采取一定的安全处理措施
Ⅳ级
可以接受可以一定的采取安全处理措施
Ⅴ级
可以忽略可以采取安全管理措施

#### 根据相关规范标准［25］与相关文献［22，27－28］，可以得到三级安全评价指标的量化范围，如表3所示。

#### 表3

#### 地铁车站施工安全指标量化范围
Table 3 Quantitative scope of construction safety index for subway station
安全描述
三级指标
极低较低中等较高高
A1 极差（0，60）较差［60，70）一般［70，80）较高［80，90）高［90，100）
A2 极不规范（0，60）不规范［60，70）一般［70，80）较规范［80，90）规范［90，100）
A3 极差（0，60）较差［60，70）一般［70，80）较高［80，90）高［90，100）
B1 极差（0，60）较差［60，70）一般［70，80）较高［80，90）高［90，100）
B2 极不合理（0，60）不合理［60，70）一般［70，80）较合理［80，90）合理［90，100）
B3 极不合适（0，60）不合适［60，70）一般［70，80）较合适［80，90）合适［90，100）
B4 极不合理（0，60）不合理［60，70）一般［70，80）较合理［80，90）合理［90，100）
B5 极差（0，60）较差［60，70）一般［70，80）较高［80，90）高［90，100）
B6 极不规范（0，60）不规范［60，70）一般［70，80）较规范［80，90）规范［90，100）
B7 极不规范（0，60）不规范［60，70）一般［70，80）较规范［80，90）规范［90，100）
C1 极差（0，60）较差［60，70）一般［70，80）较好［80，90）好［90，100）
C2 极差（0，60）较差［60，70）一般［70，80）较好［80，90）好［90，100）
C3 极密集（0，60）较密集［60，70）密集［70，80）较稀疏［80，90）稀疏［90，100）
C4 极密集（0，60）较密集［60，70）密集［70，80）较稀疏［80，90）稀疏［90，100）
C5 极密集（0，60）较密集［60，70）密集［70，80）较稀疏［80，90）稀疏［90，100）
C6 极密集（0，60）较密集［60，70）密集［70，80）较稀疏［80，90）稀疏［90，100）
C7 极多（0，60）较多［60，70）一般［70，80）较少［80，90）少［90，100）
D1 极不合理（0，60）不合理［60，70）一般［70，80）较合理［80，90）合理［90，100）
D2 极不规范（0，60）不规范［60，70）一般［70，80）较规范［80，90）规范［90，100）
D3 极不规范（0，60）不规范［60，70）一般［70，80）较规范［80，90）规范［90，100）

#### 1.2 构建评价矩阵

#### 为综合考虑决策者对各个安全评价指标的重视程度，根据已建立的安全评价指标体系，邀请专家小组

#### 对评价指标进行量化打分，取专家评分平均值构成矩阵S1，将此专家评分结果用于构成评价矩阵，步骤如下：

#### （1）将各专家对每个评价指标的赋值平均，建立一组评价矩阵S1；

<!-- 第 4 页 -->

#### 160 第31 卷

#### 自然灾害学报

#### （2）将表示专家主观因素的评价矩阵S1与表示指标客观因素的地铁车站施工安全等级节点构成评价决

#### 策矩阵D；

#### （3）将评价决策矩阵进行标准化，并通过初等变换得到标准化评价决策矩阵Q，标准化评价决策矩阵Q

#### 是CRITIC法综合赋权的基础矩阵。

#### 1.3 CRITIC法综合赋权

#### Diakoulaki 提出CRITIC 法，该方法用于处理多属性决策的综合赋权问题，将CRITIC 法应用于安全评价

#### 时，可对多个安全评价指标进行综合赋权，不仅能考虑安全评价指标间的对比强度，更能考虑其冲突性，综

#### 合衡量评价指标的客观权重［29］。

#### CRITIC 法计算评价指标组合权重步骤如下：D=（dij）m×n为评价决策矩阵，dij为评价矩阵S1 的元素与地铁

> # 公众号：数学建模老哥

#### 车站施工安全等级节点共同组成，若原始评价指标的量纲和数量级不一致，为消除其影响，需对其进行标准

#### 化处理，得到标准化评价决策矩阵Q，再求出评价指标间的相关系数rtj，构建相关系数矩阵R=（rtj）m×n，其中rtj为：

#### cov(dt,dj)

#### rtj = （1）

#### Ddt Ddj

#### dt,dj = E(( ) ⋅( ))

#### cov( ) dt - E( ) dj - E( ) （2）

#### dt dj

#### 求各评估属性的信息量与权重。各评价指标的客观权重以评价指标间的对比强度和冲突性来综合衡

#### 量，设Cj表示第j个评价指标所包含的信息量：

#### Cj = σj∑n ( )

#### 1 - rtj ，j=1，2，···，n （3）
t = 1

#### σj为第j个评价指标的标准差，rtj为评价指标间的相关系数。CRITIC法的客观性通过评价指标间的对比

#### 强度与冲突性来体现，其中对比强度表示同一个评价指标各在各方案中取值差距的大小，以标准差的形式

#### 来表现，标准差越大，说明该评价指标在各方案之间的差距越大，数据反映的信息量越大；冲突性是以评价

#### 指标间的相关性为基础，计算评价指标间的冲突性，如2 个评价指标存在较强的正相关，则这2 个指标冲突

#### 性较低［29］。式（1）体现了CRITIC 法的赋权综合了评价指标的对比强度与冲突性，显然Cj越大，第j个评价指

#### 标所包含的信息量越大，该指标的相对重要性也就越大，故权重wj为：

#### Cj

#### wj = ，j=1，2，···，n （4）

#### ∑n

#### Cj
j = 1

#### 构建标准化加权评价决策矩阵V=（vij）m×n。

#### d11 ⋅w11 d12 ⋅w12 ⋯ d1n ⋅w1n
  - •

#### | d21 ⋅w21 d22 ⋅w22 ⋯ d2n ⋅w2n |

#### V = ||| ||| （5）

#### ⋮ ⋮ ⋮ ⋮

#### | |

#### dm1 ⋅wm1 dm2 ⋅wm2 ⋯ dmn ⋅wmn
  - •

#### 1.4 TOPSIS理论

#### 1981年C.L.Hwang和K.P.Yoon提出了一种解决单一型或混合型多评价指标决策问题的方法——逼近理
想解排序方法TOPSIS（Technique for Order Preference by Similarity to Solution）［31－32］，其具有易于理解、计算简

#### 单、适用范围广、几何意义直观、结果合理等优点［33］。将TOPSIS 应用于安全评价中，具有以下优点：TOPSIS

#### 理论则可以对多评价指标进行合理排序、综合决策，并求得评价指标具体的隶属度。但该方法需要评价指

#### 标的量化数据，且采用各方案与理想解和负理想解的距离来计算，故受指标的离散程度影响较大。故文中

#### 将其与CRITIC法相结合，以减小上述不足，使其可应用于地铁车站施工安全评价。

#### TOPSIS计算原理为：基于标准化加权评价决策矩阵，定义多评价指标决策问题的正理想解和负理想解，

#### 分别计算各方案与理想解和负理想解的距离，然后计算各方案的综合评价值（即各评价方案与最优方案的

#### 相对接近距离），最后根据综合评价值对各方案进行排序。综合评价指标距离正理想解越近，而距离负理想

#### 解越远，评价结果越优，其方案越好。具体计算如下：

#### 基于标准化加权评价决策矩阵，计算正理想解V+和负理想解V－。

#### V + = ( )

#### v+1,v+2,⋯,v+j ,⋯,v+ （6）
n

<!-- 第 5 页 -->

#### 第3 期明，等：基于CRITIC法与TOPSIS地铁车站施工安全评价 161

#### 胥

#### j = { }

#### (1 ≤i ≤m vij| j ∈J + ,() )

#### v+ max 1 ≤i ≤m vij| j ∈J -min （7）

#### V - = ( )

#### v-1,v-2,⋯,v-j ,⋯,v- （8）
n

#### j = { }

#### (1 ≤i ≤m vij| j ∈J + ,() )

#### v- min 1 ≤i ≤m vij| j ∈J -max （9）

#### 计算各方案到正理想解和负理想解的欧氏距离D+j 、D-j 。

#### j = ∑ 2

#### n (vij - v+) （10）

#### D+
j
j = 1

#### j = ∑ 2

#### n (vij - v-) （11）

> # 公众号：数学建模老哥D-
j
j = 1

#### 计算各方案的相对贴近度。

#### D-

#### C∗i = i （12）

#### D+i + D-
i

#### 1.5 安全评价流程图

#### 将CRITIC法与TOPSIS结合用于评价地铁车站施工安全评价主要流程如下：首先根据安全评价体系，邀

#### 请业内专家对评价工程按评价指标进行打分，再将专家打分结果与安全等级节点构成评价决策矩阵，利用

#### CRITIC 法综合考虑主、客观因素，计算指标权重，再采用TOPSIS计算评价指标具体的隶属度，确定施工安全

#### 等级，最后根据评价结果，参考安全接受准则，实施相应的安全对策，安全评价流程如图2所示。

#### 图2

#### 地铁车站施工安全评价流程图
Fig. 2 Flow chart of construction safety assessment of subway station

### 2 案例分析

#### 2.1 工程概况

#### 施尧站为南昌市轨道交通3号线工程的第8座车站，车站位于江铃六路与迎宾北大道交汇处，车站总长
约197.6 m，标准段宽22.7 m，端头井处宽26.8 m，底板埋深约为16.7 m，端头井处底板埋深约为18.1 m。本车

#### 站采用半盖挖法施工，车站主体围护结构采用800 mm 地下连续墙，内设3 道支撑，第一道为钢筋混凝土支

#### 撑，支撑一端与冠梁连接，另一端与盖板纵向连系梁连接，第二道至第三道支撑为钢支撑，在连系梁位置用

#### 钢筋抱箍固定并预加轴力。车站标准断面图如图3所示。

#### 施尧站位于赣抚冲积平原区的二级阶地，地处鄱阳湖滨湖前后缘地带，地表水系发育，且降雨量多集中

<!-- 第 6 页 -->

#### 162 第31 卷

#### 自然灾害学报

#### 在4～6月，约占全年降雨量的51%，常有暴雨洪涝灾害。地层自上而下依次为0.6～0.7 m厚的杂填土、0.6～
4.0 m厚的素填土、0.8～7.8 m厚的粉质黏土、2.0～11.5 m厚的中砂、1.4～7.5 m厚的粗砂、4.5～12.2 m厚的砾

#### 砂、圆砾、0.5～1.2 m厚的强风化泥质粉砂岩、往下为中风化泥质粉砂岩和钙质泥岩。

#### 场地周边环境主要为居民区、城市道路，道路两边地下管线复杂。车站周边建筑有汽车玻璃厂（距车站

#### 约10 m）、超市（距车站约11 m）、药房（距车站约14 m）、医院综合楼（距车站约16 m）等，建筑较多、较近和密

#### 集；周边城市道路主要为双向4车道的迎宾北大道和江铃六路；周边管线多且密集，见表4。

#### 表4

#### 地铁车站管线情况

#### Table 4 Pipeline condition of subway station

> # 公众号：数学建模老哥距离车站/m
方位属性规格

## 3.75 DN700
污水

# 10 KV强电 4.6 800*100

## 5.5 DN1000
车站东南侧雨水

### 7.9

弱电

## 4.6 DN1000
自来水

## 6.5 DN1000
雨水

# 10 KV强电 4.5 800*100

## 5.4 DN1200
车站东北侧雨水

## 3.7 DN700
污水

## 4.5 DN1000
自来水

## 3.7 DN500
燃气

## 4.6 DN1000
雨水

#### 图3

#### 地铁车站标准断面图 10 KV强电 5.6 800*100
车站西侧

#### Fig. 3 Standard section of the subway station 6.4 700*500
光纤

## 7.6 600*500
光纤

#### 2.2 确定评价指标权重

#### 根据已建立的安全评价指标体系，邀请5位专家对评价指标进行量化打分，评分情况汇总于表5。

#### 表5

#### 专家小组评分汇总表

#### Table 5 Summary table of expert panel scores
专家A 专家B 专家C 专家D 专家E
评价指标最终得分
A1 80 82 81 83 82 81.6
A2 80 75 85 80 85 81
A3 85 86 85 86 84 85.2
B1 85 83 86 85 85 84.8
B2 90 85 89 91 90 89
B3 80 84 85 80 85 82.8
B4 90 88 87 90 90 89
B5 90 89 90 90 87 89.2
B6 84 85 85 85 85 84.8
B7 90 91 85 90 90 89.2
C1 60 62 64 65 61 62.4
C2 70 55 60 70 62 63.4
C3 35 41 46 45 60 45.4
C4 65 50 62 65 70 62.4
C5 65 53 56 55 45 54.8
C6 55 51 48 48 54 51.2
C7 60 65 61 65 62 62.6
D1 75 78 70 80 80 76.6
D2 85 70 81 82 80 79.6
D3 85 82 85 88 86 85.2

<!-- 第 7 页 -->

#### 第3 期明，等：基于CRITIC法与TOPSIS地铁车站施工安全评价 163

#### 胥

#### 将代表主观因素的专家评分平均值与代表客观因素的安全等级节点构建评价决策矩阵，并进行标准化

#### 处理，得到标准化评价决策矩阵Q如下。
- 0.82 0.81 0.85 0.85 0.89 0.83 0.89 0.89 0.85 0.89 0.62 0.63 0.45 0.62 0.55 0.51 0.63 0.77 0.80 0.85•
Q = |0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20 0.20|
||0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40 0.40||
||| |||
|0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60 0.60|
|0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80 0.80|
- •
- 0.0148 0.0144 0.0187 0.0184 0.0241 0.0156 0.0241 0.0243 0.0181 0.0243 0.0173 0.0184 0.0466 0.0186 0.0379 0.0448 0.0170 0.0116 0.0144 0.0187•
I =|0.0152 0.0135 0.019 0.0179 0.0228 0.0164 0.0236 0.0241 0.0184 0.0246 0.0179 0.0145 0.0546 0.0143 0.0309 0.0416 0.0184 0.0121 0.0119 0.0181|
||0.0150 0.0153 0.0187 0.0186 0.0238 0.0166 0.0233 0.0243 0.0184 0.023 0.0185 0.0158 0.0612 0.0178 0.0326 0.0391 0.0173 0.0109 0.0137 0.0187||
||| |||
|0.0153 0.0144 0.0190 0.0184 0.0244 0.0156 0.0241 0.0243 0.0184 0.0243 0.0187 0.0184 0.0599 0.0186 0.0321 0.0391 0.0184 0.0124 0.0139 0.0194|
|0.0152 0.0153 0.0185 0.0184 0.0241 0.0166 0.0241 0.0235 0.0184 0.0243 0.0176 0.0163 0.0798 0.0201 0.0262 0.044 0.0176 0.0124 0.0136 0.0189|
- •

#### 利用CRITIC法可计算得各评价指标的权重如表6所示。
> 公众号：数学建模老哥由此可知，三级评价指标中最重要是C3（周边建筑）、C6（周边人员密集）、C5（周边管线），二级评价指标

#### 的重要性排序为C>B>A>D。

#### 表6 表7

#### 评价指标权重各评价指标的距离及相对贴近度
Table 6 Weight of evaluation index Table 7 The distance and relative closeness of each evaluation index

|三级指标|三级指标权重|二级指标二级指标权重|
|---|---|---|
|A1<br>|3.37%<br>|A<br>B<br>C<br>D<br>10.83%<br>33.26%<br>46.03%<br>9.89%<br>号：|
|A2<br>|3.26%<br>|3.26%<br>|
|A3<br>|4.20%<br>|4.20%<br>|
||||
|B1<br>|4.09%<br>|4.09%<br>|
|B2<br>|5.33%<br>|5.33%<br>|
|B3<br>|3.62%<br>|3.62%<br>|
|B4<br>|5.33%<br>|5.33%<br>|
|B5<br>|5.39%<br>|5.39%<br>|
|B6<br>|4.03%<br>|4.03%<br>|
|B7<br>|5.39%<br>|5.39%<br>|
||||
|C1<br>|4.03%<br>|4.03%<br>|
|C2<br>|3.73%<br>|3.73%<br>|
|C3<br>|13.73%<br>|13.73%<br>|
|C4<br>|4.03%<br>|4.03%<br>|
|C5<br>|7.19%<br>|7.19%<br>|
|C6<br>|9.35%<br>|9.35%<br>|
|C7<br>|3.97%<br>|3.97%<br>|
||||
|D1<br>|2.66%<br>|2.66%<br>|
|D2<br>|3.02%<br>|3.02%<br>|
|D3<br>|4.20%<br>|4.20%<br>|

三级指标 D+ D- 相对贴近度C ∗ 安全指标排序
j j i
A1 0.000 72 0.000 78 0.477 0.523 6
A2 0.002 2 0.002 84 0.436 0.564 10
A3 0.000 54 0.000 7 0.436 0.564 11
B1 0.000 75 0.000 99 0.431 0.569 12
B2 0.001 73 0.002 7 0.391 0.609 17
B3 0.001 4 0.001 59 0.468 0.532 8
B4 0.000 97 0.001 42 0.405 0.595 15
B5 0.000 86 0.001 51 0.362 0.638 19
B6 0.000 22 0.000 43 0.333 0.667 20
B7 0.001 69 0.002 85 0.372 0.628 18
C1 0.002 06 0.001 96 0.513 0.487 3
C2 0.005 19 0.006 02 0.463 0.537 9
C3 0.049 92 0.039 52 0.558 0.442 1
C4 0.006 5 0.009 04 0.418 0.582 13
C5 0.015 69 0.015 25 0.507 0.493 4
C6 0.008 74 0.007 9 0.525 0.475 2
C7 0.002 0.002 1 0.488 0.512 5
D1 0.001 76 0.002 64 0.401 0.599 16
D2 0.002 81 0.004 12 0.406 0.594 14
D3 0.001 68 0.001 84 0.477 0.523 7

#### 根据CRITIC 法计算得到的客观权重，分别将此权重赋予标准化决策矩阵Q，可以得到标准化加权决策

#### 矩阵I。

#### 2.3 地铁车站安全性评价

#### 依据图1 所示的地铁车站施工安全评价指标体系和通过CRITIC 法得到的标准化加权决策矩阵Q，利用

#### TOPSIS理论进行安全性评价。利用式（8）、（9）计算各指标到正理想解和负理想解距离D+j 、D-

#### j ，对评价指标进

#### 行综合决策，利用式（10）计算相对贴近度C∗i，进行合理排序，结果如表7所示。

#### 二级评价指标人员、施工、环境、管理的隶属度分别为：0.550、0.605、0.504、0.572，其中人员、环境、管理

#### 均对应于安全接受准则Ⅲ级，即安全性中等，施工对应于安全接受准则Ⅱ级，即安全性较高。

#### 2.4 多种方法对比分析

#### 为验证本文方法的准确性与实用性，分别采用层次分析法和灰色关联度法，对本地铁车站施工安全性

#### 进行评价，其中灰色关联度无法计算权重，故采用1/n 权重和CRITIC 法权重分别计算，限于篇幅此2 种方法

<!-- 第 8 页 -->

#### 164 第31 卷

#### 自然灾害学报

#### 计算过程不做具体说明。所得结果如图4 所示，其中

#### 方法1 为层次分析法计算结果，方法2 为1/n 权重的灰

#### 色关联度法计算结果，方法3 为CRITIC 法权重的灰色

#### 关联度计算结果，方法4为本文CRITIC 法－TOPSIS 计

#### 算结果。

#### 由图4 可得：层次分析法确实过度依赖决策者的

#### 主观判断，导致各二级评价指标差异过大，对人员、施

#### 工、管理的安全评价过于冒险。灰色关联度法存在无

#### 法计算评价指标权重的缺陷，需与其他权重计算方法

> # 公众号：数学建模老哥

#### 结合使用，当采用CRITIC法权重计算所得隶属度与本

#### 文方法大致相同，但确实可能存在前文所提的超模糊图4

#### 多种方法对比分析结果
现象，分辨率差的问题，如人员指标与施工指标、环境 Fig. 4 Comparison and analysis of results

#### 指标与管理指标的隶属度大小较接近，结果无法很好 by multiple methods

#### 地区分。文中的CRITIC 法结合TOPSIS 进行地铁施工

#### 安全评价，所得结果与本工程验收专家得出的结果一致，与该复杂环地铁车站的实际情况相符，且综合考虑

#### 了评价指标的主、客观因素，不会过分依赖决策者的主观判断，不存在分辨率差的问题，由此可见本方法是

#### 可行且较准确的。

### 3 地铁车站施工安全措施分析

#### 根据上述地铁车站施工安全性分析，结合施尧站实际情况，得出以下安全措施与施工建议。

#### （1）通过上述安全性评价结果可知：指标人员、施工、环境、管理的隶属度分别为：0.550、0.605、0.504、

#### 0.572，其中环境的安全性最低，因此在施工过程中需要加强对周边复杂环境的安全管控，否则一旦发生安全

#### 事故，将会在很大范围内造成人员伤亡与财产损失。

#### （2）在施尧站施工中，周边环境的权重占46.03%，且其安全性程度最低。为保证复杂周边环境地铁车站

#### 的施工安全，可采取以下措施：1）由于地层为富水砂层，且地下水丰富，因此要做好基坑降水工作，承压水必

#### 须控制到确保不发生基底管涌的水位以下；2）加强周边道路、建筑、管线的监控量测，用监测数据指导施工，

#### 特别是对距离基坑较近的重要管线，可以迁移的尽量迁移，对于不能迁移的管线，应对其变形进行监测，保

#### 证不会因基坑施工而破坏；3）开挖基坑是引起道路、建筑、管线等变形的主要原因，在施工过程中，尽量缩短

#### 围护结构暴露时间，土方开挖满足混凝土结构施作条件后，立即展开混凝土结构的施工。

#### （3）二级指标人员与施工安全性评价为中等，因此需要对施工人员进行相应的技术培训与安全培训，保

#### 证其施工作业规范。在土方开挖、围护结构、主体结构等施工过程中，应注意施工工序的合理规范。

### 4 结论

#### 文中采用CRITIC 法与TOPSIS 理论，依托南昌轨道交通3号线施尧站项目，对地铁车站施工进行安全性

#### 评价，主要结论如下：

#### （1）考虑工程实际的不确定性和复杂性，在调研国内外相关学者研究的基础上，较完整合理地建立了地

#### 铁车站施工安全性评价指标体系。将影响地铁车站施工的安全性因素划分为人员因素、环境因素、施工因

#### 素和管理因素，再细分为20个三级指标，既把握全面又突出重点，能为类似工程项目安全评价提供参考。

#### （2）在影响地铁车站施工安全的人员、环境、施工和环境因素中，采用CRITIC法对其进行权重分析，可知

#### 环境的权重较大，且环境的安全评价指标较小，原因是施工现场的建筑、道路、管线等因素对施工安全影响

#### 很大，因此在施工过程中，需要对周边环境给予足够的重视，采取相应保护措施是十分重要的。

#### （3）将CRITIC 法与TOPSIS 理论有效结合，建立了地铁车站施工安全评价模型：采用CRITIC 对各安全性

#### 评价指标进行客观赋权，再利用TOPSIS理论计算本工程的安全评价等级为Ⅲ级，安全性为中等，复杂的环境

#### 是导致本工程安全性较低的主要因素，与工程实际情况一致，证明了本评价模型是合理适用的，可为类似具

<!-- 第 9 页 -->

#### 第3 期明，等：基于CRITIC法与TOPSIS地铁车站施工安全评价 165

#### 胥

#### 有复杂环境的工程提供一种科学合理的安全性评价方法，为后续施工安全保证提供理论支持。

### 参考文献：
［1］王成汤，王浩，覃卫民，等. 基于多态模糊贝叶斯网络的地铁车站深基坑坍塌可能性评价［J］. 岩土力学，2020，41（5）：1670－1679.
WANG Chengtang，WANG Hao，QIN Weimin，et al. Evaluation of collapse possibility of deep foundation pits in metro stations based on
multi‐state fuzzy Bayesian networks［J］. Rock and Soil Mechanics，2020，41（5）：1670－1679.（in Chinese）
［2］于汐，薄景山. 重大岩土工程风险评估研究现状［J］. 自然灾害学报，2015，24（3）：12－19.
YU Xi，BO Jingshan. Review of risk assessment of major geotechnical project［J］. Journal of Natural Disasters，2015，24（3）：12－19.（in Chi‐

> # 公众号：数学建模老哥nese）
［3］薛模美，吴替，张铁军. 金沙洲隧道淤泥质地层明挖深基坑施工风险评估及控制［J］. 铁道标准设计，2010（1）：150－154.
XUE Momei，WU Ti，ZHANG Tiejun. Risk assessment and control of open‐cut deep foundation pit construction in silty stratum of Jinshazhou
Tunnel［J］. Railway Standard Design，2010（1）：150－154.（in Chinese）
［4］周红波，姚浩，卢剑华. 上海某轨道交通深基坑工程施工风险评估［J］. 岩土工程学报，2006（S1）：1902－1906.
ZHOU Hongbo，YAO Hao，LU Jianhua. Construction risk assessment on deep foundation pits of a metro line in Shanghai［J］. Chinese Journal of
Geotechnical Engineering，2006（S1）：1902－1906.（in Chinese）
［5］ ZHANG G，WANG C，JIAO Y，et al. Collapse risk analysis of deep foundation pits in metro stations using a fuzzy Bayesian network and a fuzzy
AHP［J］. Mathematical Problems in Engineering，2020，2020：1－18.
［6］李朝阳，叶聪，沈圆顺. 基于模糊综合评判的地铁基坑施工风险评估［J］. 地下空间与工程学报，2014，10（1）：220－226.
LI Chaoyang，YE Cong，SHEN Yuanshun.Risk assessment of subway pit construction based on fuzzy comprehensive evaluation［J］. Chinese
Journal of Underground Space and Engineering，2014，10（1）：220－226.（in Chinese）
［7］吴波，吴昱芳，黄惟，等. 基于模糊综合判定法地铁深基坑施工安全风险评估［J］. 数学的实践与认识，2020，50（2）：179－187.
WU Bo，WU Yufang，HUANG Wei，et al.Safety risk assessment of metro deep foundation pit construction based on fuzzy comprehensive judg‐
ment method［J］. Mathematics in Practice and Theory，2020，50（2）：179－187.（in Chinese）
［8］ LUO Z，ZENG L，PAN H，et al. Research on construction safety risk assessment of new subway station close‐attached under crossing the exist‐
ing operating station［J］. Mathematical Problems in Engineering，2019：1－20.
［9］陈蓉芳，姜安民，董彦辰，等. 基于熵权可拓模型的深大基坑施工风险评估［J］. 数学的实践与认识，2019，49（2）：311－320.
CHEN Rongfang，JIANG Anmin，DONG Yanchen，et al.Construction risk assessment of deep and large foundation pit based on entropy weight
extension model［J］. Mathematics in Practice and Theory，2019，49（2）：311－320.（in Chinese）
［10］王景春，张法. 基于熵权二维云模型的深基坑施工风险评价［J］. 安全与环境学报，2018，18（3）：849－853.
WANG Jingchun，ZHANG Fa. Risk assessment of the deep foundation pit based on the entropy weight and 2‐dimensional cloud model［J］.
Journal of Safety and Environment，2018，18（3）：849－853.（in Chinese）
［11］郎秋玲，王伟，高成梁. 基于组合权重与灰色关联度分析法的地铁深基坑开挖稳定性评价［J］. 吉林大学学报（地球科学版），2020，50

#### （6）：1823－1832.
LANG Qiuling，WANG Wei，GAO Chengliang. Stability evaluation of deep foundation pit of metro based on grey correlation analysis with com‐
bined weights［J］. Journal of Jilin University（Earth Science Edition），2020，50（6）：1823－1832.（in Chinese）
［12］SHEN Y，WANG P，LI M，et al. Application of subway foundation pit engineering risk assessment：A case study of Qingdao rock area，China
［J］. KSCE Journal of Civil Engineering，2019，23（11）：4621－4630.
［13］李凤伟，杜修力，张明聚，等. 改进的层次分析法在明挖地铁车站施工风险辨识中的应用［J］. 北京工业大学学报，2012，38（2）：167－
172.
LI Fengwei，DU Xiuli，ZHANG Mingju，et al. Application of improved AHP in risk identification during open‐cut construction of a subway sta‐
tion［J］. Journal of Beijing University of Technology，2012，38（2）：167－172.（in Chinese）
［14］聂菁，苏会卫，张念. 基于AHP 的轨道交通施工风险模糊综合评价方法——以福州轨道交通1 号线为例［J］. 自然灾害学报，2014，23

#### （5）：246－252.
NIE Jing，SU Huiwei，ZHANG Nian.Fuzzy comprehensive evaluation method for the risk of construction of rail traffic based on AHP：A case
study of Fuzhou Rail Traffic Line 1［J］. Journalof Natural Disasters，2014，23（5）：246－252.（in Chinese）
［15］LIU P，XIE M，BIAN J，et al. A hybrid PSO‐SVM model based on safety risk prediction for the design process in metro station construction［J］.
International Journal of Environmental Research and Public Health，2020，17（5）：1714.
［16］WU L，BAI H，YUAN C，et al. FANPCE technique for risk assessment on subway station construction［J］. Journal of Civil Engineering and Man‐
agement，2019，25（6）：599－616.
［17］顾雷雨，黄宏伟，陈伟，等. 复杂环境中基坑施工安全风险预警标准［J］. 岩石力学与工程学报，2014，33（S2）：4153－4162.
GU Leiyu，HUANG Hongwei，CHEN Wei，et al.Safety risk early‐warning standard of foundation pit in complex environment during excavating
［J］. Chinese Journal of Rock Mechanics and Engineering，2014，33（S2）：4153－4162.

<!-- 第 10 页 -->

#### 166 第31 卷

#### 自然灾害学报
［18］姜安民，董彦辰，刘霁. 基于突变级数法的地铁站施工风险预测模型研究［J］. 安全与环境学报，2020，20（3）：832－839.
JIANG Anmin，DONG Yanchen，LIU Ji.Probe into the risk prediction modelfor the metro station construction based on the catastrophe series
method［J］. Journal of Safety and Environment，2020，20（3）：832－839.（in Chinese）
［19］中国土木工程学会，同济大学，上海城建集团，等. GB 50652－2011 城市轨道交通地下工程建设风险管理规范［S］. 中华人民共和国国
家标准，2011.
China Society of Civil Engineering，Tongji University，Shanghai Construction Group.Code for Risk Management of Underground Works in Urban
Rail Transit［S］. National Standards of the People′s Republic of China，2011.（in Chinese）
［20］陈楠. 基于IOWA算子的地铁车站深基坑施工安全综合评价［J］. 隧道建设（中英文），2020，40（2）：202－208.
CHEN Nan.Comprehensive evaluation of construction safety of deep foundation pit of metro station based on IOWA operator［J］. Tunnel Construc‐
tion，2020，40（2）：202－208.（in Chinese）
> ［21］吴丹红，张美霞，张汉斌，等. 基于可拓学的地铁车站深基坑施工安全评价［J］. 安全与环境学报，2019，19（3）：761－766.公众号：数学建模老哥
WU Danhong，ZHANG Meixia，ZHANG Hanbin，et al.On the safety evaluation for the deep foundation pit of the subway stations based on the
theory of extenics［J］. Journal of Safety and Environment，2019，19（3）：761－766.（in Chinese）
［22］宋博. DEA‐BP神经网络下地铁车站深基坑施工安全评价［J］. 中国安全科学学报，2019，29（5）：91－96.
SONG Bo. Safety evaluation for deep foundation pit construction inmetro station based on DEA‐BP neural network［J］. China Safety Science Jour‐
nal，2019，29（5）：91－96.（in Chinese）
［23］何花. 地铁施工安全事故致因研究［D］. 兰州：兰州大学，2018.
HE Hua. Research on Safety Accidents Caused by Subway Construction［D］.Lanzhou：Lanzhou University，2018.（in Chinese）
［24］郭健，钱劲斗，陈健，等. 地铁车站深基坑施工风险识别与评价［J］. 土木工程与管理学报，2017，34（5）：32－38.
GUO Jian，QIAN Jindou，CHEN Jian，et al.Risk identification and evaluation for foundation pit construction of subway station［J］. Journal of
Civil Engineering and Management，2017，34（5）：32－38.（in Chinese）
［25］GB 50652－2011城市轨道交通地下工程建设风险管理规范［S］. 中华人民共和国住房和城乡建设部.中华人民共和国国家标准，2011.
GB 50652－2011 Code for Risk Management of Underground Works in Urban Rail Transit［S］. Ministry of Housing and Urban‐Rural Develop‐
ment of the People′s Republic of China. National Standards of the People′s Republic of China，2011.（in Chinese）
［26］GB 50715－2011 地铁工程施工安全评价标准［S］.华中科技大学，武汉市市政建设集团有限公司，中铁第四勘察设计院集团有限公司，
等. 中华人民共和国国家标准，2011.
GB 50715－2011 Standard for Construction Safety Assessment of Metro Engineering［S］. Huazhong University of Science and Technology，Wu‐
han Municipal Construction Group Co.，Ltd，China Railway Fourth Survey and Design Institute Group Co.，Ltd，et al. National Standards of the
People′s Republic of China，2011.（in Chinese）
［27］胡众，朱大勇. 复杂环境下地铁基坑施工风险研究［J］. 合肥工业大学学报（自然科学版），2020，43（4）：522－529.
HU Zhong，ZHU Dayong. Research on construction risk of subway foundation pit under complicated environment［J］. Journal of Hefei University
of Technology（Natural Science），2020，43（4）：522－529.（in Chinese）
［28］许硕，唐作其，王鑫. 基于D‐AHP与灰色理论的信息安全风险评估［J］. 计算机工程，2019，45（7）：194－202.
XU Shuo，TANG Zuoqi，WANG Xin.Information security risk assessment based on D‐AHP and grey theory［J］. Computer Engineering，2019，45

#### （7）：194－202.（in Chinese）
［29］安进，徐廷学，曾翔，等. 组合赋权下的装备质量状态信息融合评估方法［J］. 控制与决策，2018，33（9）：1693－1698.
AN Jin，XU Yanxue，ZENG Xiang，et al.Equipment quality condition assessment under fusion information based on combination weighting［J］.
Control and Decision，2018，33（9）：1693－1698.（in Chinese）
［30］张玉，魏华波. 基于CRITIC的多属性决策组合赋权方法［J］. 统计与决策，2012（16）：75－77.
ZHANG Yu，WEI Huabo. Multi‐attribute decision combination weighting method based on CRITIC［J］. Statistics & Decision，2012（16）：75－

### 77.（in Chinese）

［31］ALI A T M M，ERFAN A. Role of public participation in sustainability of historical city：Usage of TOPSIS method［J］. Indian Journal of Science
and Technology，2012：2289－2294.
［32］K. PAUL Y，CHING‐LAI H. Multiple Attribute Decision Making：An Introduction［M］. California：SAGE Publicationgs，1995.
［33］Zavadskas E K，Zakarevicius A，Antucheviciene J. Evaluation of ranking accuracy in multi‐criteria decisions［J］. Informatica，2006，17（4）：
601－618.
