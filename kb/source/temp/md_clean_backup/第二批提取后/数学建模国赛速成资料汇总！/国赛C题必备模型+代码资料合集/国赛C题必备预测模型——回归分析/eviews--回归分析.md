<!-- 第 1 页 -->
计量经济软件Eviews 上机指导及演示示例

### 第一部分 Eviews 简介

Eviews 是Econometrics Views 的缩写，直译为计量经济学观察，通常称为计量经济学
软件包。它的本意是对社会经济关系与经济活动的数量规律，采用计量经济学方法与技术进
行“观察”。计量经济学研究的核心是设计模型、收集资料、估计模型、检验模型、应用模
型（结构分析、经济预测、政策评价）。Eviews 是完成上述任务比较得力的必不可少的工具。
正是由于Eviews 等计量经济学软件包的出现，使计量经济学取得了长足的进步，发展成为
一门较为实用与严谨的经济学科。

#### 1、Eviews 是什么

Eviews 是美国QMS 公司研制的在Windows 下专门从事数据分析、回归分析和预测的工
具。使用Eviews 可以迅速地从数据中寻找出统计关系，并用得到的关系去预测数据的未来
值。Eviews 的应用范围包括：科学实验数据分析与评估、金融分析、宏观经济预测、仿真、
销售预测和成本分析等。
Eviews 是专门为大型机开发的、用以处理时间序列数据的时间序列软件包的新版本。
Eviews 的前身是1981 年第1 版的Micro TSP。目前最新的版本是Eviews4.0。我们以
Eviews3.1 版本为例，介绍经济计量学软件包使用的基本方法和技巧。虽然Eviews 是经济
学家开发的，而且主要用于经济学领域，但是从软件包的设计来看，Eviews 的运用领域并
不局限于处理经济时间序列。即使是跨部门的大型项目，也可以采用Eviews 进行处理。
Eviews 处理的基本数据对象是时间序列，每个序列有一个名称，只要提及序列的名称
就可以对序列中所有的观察值进行操作，Eviews 允许用户以简便的可视化的方式从键盘或
磁盘文件中输入数据，根据已有的序列生成新的序列，在屏幕上显示序列或打印机上打印输
出序列，对序列之间存在的关系进行统计分析。Eviews 具有操作简便且可视化的操作风格，
体现在从键盘或从键盘输入数据序列、依据已有序列生成新序列、显示和打印序列以及对序
列之间存在的关系进行统计分析等方面。
Eviews 具有现代Windows 软件可视化操作的优良性。可以使用鼠标对标准的Windows
菜单和对话框进行操作。操作结果出现在窗口中并能采用标准的Windows 技术对操作结果进
行处理。此外，Eviews 还拥有强大的命令功能和批处理语言功能。在Eviews 的命令行中输
入、编辑和执行命令。在程序文件中建立和存储命令，以便在后续的研究项目中使用这些程
序。

#### 2、运行Eviews

在Windows 2000 中运行Eviews 的方法有：

#### （1）单击任务栏上的“开始”→“程序”→“Eviews”程序组→“Eviews”图标。
（2）使用Windows 浏览器或从桌面上“我的电脑”定位Eviews 目录，双击“Eviews”
程序图标。

#### （3）双击Eviews 的工作文件和数据文件。

#### 3、Eviews 的窗口

Eviews 的窗口分为几个部分：标题栏、主菜单栏、命令窗口、状态行和工作区（如图
1-1 所示）。

<!-- 第 2 页 -->
计量经济软件Eviews 上机指导及演示示例

图1-1 Eviews 窗口

#### （1）标题栏
标题栏位于主窗口的顶部，标记有Eviews 字样。当Eviews 窗口处于激活时，标题栏颜
色加深，否则变暗。单击Eviews 窗口的任意区域将使它处于激活状态。标题栏的右端有三
个按钮：最小化、最大化（或复原）和关闭。标题栏左边是控制框，控制框也有上述三个按
钮的功能且双击它关闭该窗口。

#### （2）主菜单
主菜单位于标题栏之下。将指针移至主菜单上的某个项目并用鼠标左键单击，打开一个
下拉式菜单，通过单击下拉菜单中的项目，就可以对它们进行访问。菜单中黑色的是可执行
的，灰色的是不可执行的无效项目。
主菜单栏上共有7 个选项：“File”, “Edit”, “Objects”, “View”,“Procs”,
“Quick”,“Options”,“Windows”,“Help”。

#### （3）命令窗口
主菜单下的区域称作命令窗口。在命令窗口输入命令，按“ENTER”后命令立即执行。
命令窗口中的竖条称为插入点（或提示符），它指示键盘输入字符的位置。允许用户在提示
符后通过键盘输入Eviews（TSP 风格）命令。如果熟悉Micro TSP(DOS)版的命令，可以直
接在此输入，如同DOS 版一样使用Eviews。按F1 键（或移动箭头），输入的历史命令将重
新显示出来，供用户选用。
将插入点移至从前已经执行过的命令行，编辑已经存在的命令，按ENTER，立即执行原
命令的编辑版本。
命令窗口支持cut-and-paste 功能，命令窗口、其他Eviews 文本窗口和其他Windows
程序窗口间可方便地进行文本的移动。命令窗口的内容可以直接保存到文本文件中备用，为
此必须保持命令窗口处于激活状态，并从主菜单上选择“File”→“Save as”。
若输入的命令超过了命令窗口显示的大小，窗口中就自动出现滚动条，通过上下或左右

<!-- 第 3 页 -->
计量经济软件Eviews 上机指导及演示示例

调节，可浏览已执行命令的各个部分。将指针移至命令窗口下部，按着鼠标左键向下向上拖
动，来调整默认命令窗口的大小。

#### （4）状态栏
窗口最底部是状态行。状态行分为4 栏。左栏有时给出Eviews 送出的状态信息，单击
状态行左端的边框可以清楚这些信息。第二栏是Eviews 默认的读取数据和程序的路径。最
后两栏分别显示默认的数据库和默认的工作文件。

#### （5）工作区（或主显示窗口）
命令窗口下是Eviews 的工作区或主显示窗口，以后操作产生的窗口（称为子窗口）均
在此范围之内，不能移出主窗口之外。Eviews 在此显示它建立的各种对象的窗口。工作区
中的这些窗口类似于用户在办公桌上使用的各种纸张。出现在最上面的窗口正处于焦点，即
处于激活状态。状态栏颜色加深的窗口是激活窗口。单击部分处于下面窗口的标题栏或任何
可见部分，都可以使该窗口移至顶部。也可以按压F6 或CTRL-TAB，循环地激活各个窗口。
此外，单击窗口中菜单项目，选择关注的文件名，可直接选择某个窗口。还可以移动窗
口、改变窗口的大小等。

#### 4、Eviews 的主要功能

#### （1）输入、扩大和修改时间序列数据。

#### （2）依据已有序列按照任意复杂的公式生成新的序列。

#### （3）在屏幕上和用打字机输出序列的趋势图、散点图、柱形图和饼图。

#### （4）执行普通最小二乘法（多元回归），带有自回归校正的最小二乘法，两阶段最小二
乘法和三阶段最小二乘法。

#### （5）执行非线性最小二乘法。

#### （6）对二择一决策模型进行Probit 和Logit 估计。

#### （7）对联立方程进行线性和非线性的估计。

#### （8）估计和分析向量自回归系统。

#### （9）计算描述统计量：相关系数、斜方差、自相关系数、互相关函数和直方图

#### （10）残差自回归和移动平均过程。

#### （11）多项式分布滞后。

#### （12）基于回归方程的预测。

#### （13）求解（模拟）模型。

#### （14）管理时间序列数据库。

#### （15）与外部软件（如Excel 和Lotus 软件）进行数据交换。

#### 5、关闭Eviews

关闭Eviews 的方法很多：选择主菜单上的“File”→“Close”;按ALT-F4 键；单击
Eviews 窗口右上角的关闭按钮；双击Eviews 窗口左上角等。
Eviews 关闭总是警告和给予机会将那些还没有保存的工作保存到磁盘文件中。

### 第二部分  单方程计量经济模型Eviews 操作

#### 案例：

建立我国最终消费支出与国内生产总值（单位：亿元）之间的回归模型，并进行变量和

<!-- 第 4 页 -->
计量经济软件Eviews 上机指导及演示示例

方程整体的显著性检验。当显著性水平为0.05， 2004 年国内生产总值为38000 亿元时，对

# 2004 年我国最终消费支出和平均最终消费支出进行点预测和区间预测。

|年份|GDP|最终消<br>费|年份|GDP|最终消费|
|---|---|---|---|---|---|
|1978|3624.10|2239.10|1991|11147.73|6151.57|
|1979|3899.53|2568.04|1992|12735.09|7083.53|
|1980|4203.96|2753.10|1993|14452.91|7917.65|
|1981|4425.03|2989.25|1994|16283.08|8638.30|
|1982|4823.68|3225.09|1995|17993.66|9445.38|
|1983|5349.17|3511.35|1996|19718.73|10588.64|
|1984|6160.97|3988.53|1997|21461.92|11444.17|
|1985|6990.89|4506.64|1998|23139.88|12511.70|
|1986|7610.61|4817.38|1999|24792.47|13819.54|
|1987|8491.27|5114.07|2000|26774.85|15406.57|
|1988|9448.03|5419.86|2001|28782.60|16759.78|
|1989|9832.18|5190.02|2002|31170.88|18097.55|
|1990|10209.09|5471.93|2003|34070.16|19452.70|

#### 一、创建工作文件

建立工作文件的方法有以下几种。
1．菜单方式
在主菜单上依次单击File→New→Workfile（见图2-1）， 选择数据类型和起止日期。
时间序列提供起止日期（年、季度、月度、周、日），非时间序列提供最大观察个数。本例
中在Start Data 里输入1978，在End data 里输入2003，见图2-3。单击OK 后屏幕出现
Workfile 工作框，如图2-4 所示。
2．命令方式
在命令窗口直接输入建立工作文件的命令CREATE，
命令格式：CREATE 数据频率 起始期 终止期
其中，数据频率类型分别为A（年）、Q（季）、M（月）、U（非时间序列数据）。输入Eviews
命令时，命令字与命令参数之间只能用空格分隔。如本例可输入命令：
CREATE A 1978 2003
工作文件创立后，需将工作文件保存到磁盘，单击工具条中Save→输入文件名、路径
→保存，或单击菜单兰中File→Save 或Save as→输入文件名、路径→保存。

<!-- 第 5 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-1

这时屏幕上出现Workfile Range 对话框，如图2-2 所示。

图2-2

<!-- 第 6 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-3

图2-4

<!-- 第 7 页 -->
计量经济软件Eviews 上机指导及演示示例

#### 二、输入和编辑数据

建立或调入工作文件以后，可以输入和编辑数据。输入数据有两种基本方法：命令方式
和菜单方式。
1．命令方式
命令格式：data 〈序列名1〉 〈序列名2〉 … 〈序列名n〉
功能：输入新变量的数据，或编辑工作文件中现有变量的数据。
在本例中，在命令窗口直接输入：
Data  Y  X
2．菜单方式
在主菜单上单击Objects→New object，在New object 对话框里，选Group 并在Name for
Object 上定义变量名（如变量X、Y），单击OK，屏幕出现数据编辑框。
另一种菜单方式是在主菜单上依次单击Quick→Group（见图2-5），

图2-5

建立一个空组（见图2-6）， 再用方向键将光标移到每一列的顶部之后，输入各个变量
名，回车后输入数据（见图2-7）。另外数据还可以从Excel 中直接复制到空组。
然后为每个时间序列取序列名。单击数据表中的SER01（见图2-8），在数据组对话框中
的命令窗口输入该序列名称，如本例中输入X（见图2-9），回车后Yes。采用同样的步骤修
改序列名Y（见图2-10）。数据输入操作完成。

<!-- 第 8 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-6

图2-7  修改序列名

<!-- 第 9 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-8    修改序列名

图2-9    修改序列名

<!-- 第 10 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-10  数据输入

数据输入完毕，单击工作文件窗口工具条的Save 或单击菜单兰的File→Save 将数据存
入磁盘。

#### 三、图形分析

在估计计量经济模型之前，借助图形分析可以直观地观察经济变量的变动规律和相关关
系，以便合理的确定模型的数学形式。图形分析中最常用的是趋势图和相关图。
1．菜单方式
在数组窗口工具条上Views 的下拉菜单中选择Graph。（见图2-11）
2．命令方式
趋势图：Plot  Y  X
功能：

#### （1）分析经济变量的发展变化趋势；

#### （2）观察经济变量是否存在异常值。
图给出了最终消费支出与国内生产总值的趋势图。
相关图：Scat  Y  X   （见图2-13）
功能：

#### （1）观察经济变量之间的相关程度；

#### （2）观察经济变量之间的相关类型，判断是线性相关，还是曲线相关；曲线相关时，
大致是哪种类型的曲线。

<!-- 第 11 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-11  数组窗口趋势图

40000

30000

20000

10000

0

# 78 80 82 84 86 88 90 92 94 96 98 00 02
X Y

图2-12  最终消费支出与国内生产总值的趋势图

<!-- 第 12 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-13  数组窗口相关图

20000

15000

Y 10000

5000

0

# 0 10000 20000 30000 40000

X

图2-14  最终消费支出与国内生产总值的相关图

#### 四、OLS 估计参数

1．命令方式
在主菜单命令行键入
LS  Y  C  X   （如图2-15）

<!-- 第 13 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-15

2．菜单方式
在主菜单上选Quick 菜单，单击Estimate Equation 项，屏幕出现Equation
Specification 估计对话框，在Estimation Settings 中选OLS 估计，即Least Squares，
输入：Y  C  X（其中C 为Eviews 固定的截距项系数）。然后OK，出现方程窗口（见图2-16），
输出结果如表2-1 所示。

图2-16  方程窗口

<!-- 第 14 页 -->
计量经济软件Eviews 上机指导及演示示例

表2-1  回归结果

Dependent Variable: Y

Method: Least Squares

Sample: 1978 2003

Included observations: 26

Variable  Coefficient Std.  t-Statistic  Prob.
Error

C  245.3522 153.9605 1.593605  0.1241

X  0.551514 0.009135 60.37623  0.0000

R-squared  0.993459     Mean dependent var  8042.748

Adjusted R-squared  0.993187     S.D. dependent var  5177.609

S.E. of regression  427.3742     Akaike info  15.02700
criterion

Sum squared resid  4383569.     Schwarz criterion  15.12378

Log likelihood  -193.3510     F-statistic  3645.290

Durbin-Watson stat  0.244011     Prob(F-statistic)  0.000000

方程窗口的上半部分为参数估计结果如表2-2 所示，其中第1 列分别为解释变量名（包
括常数项），第2 列为相应的参数估计值，第3 列为参数的标准误差，第4 列为t 统计值，
第5 列为t 检验的双侧概率值p，即P（| t |> ti）= p。

表2-2  参数估计结果

#### 常数和解释变 参数估 参数标准 t 统计 双侧

#### 量  计值  误差  量  概率

#### C  245.3522 153.9605  1.593605  0.1241

#### X  0.551514 0.009135  60.37623  0.0000

方程窗口的下半部分主要是一些统计检验值，其中各统计量的含义如表2-3 所示。
表2-3  统计检验值

#### 可决系数  0.993459 被解释变量均值  8042.748

#### 调整的可决系数  0.993187 被解释变量标准差  5177.609

#### 回归方程标准差ˆ  427.3742 赤池信息准则  15.02700

#### 残差平方和  ie2 4383569. 施瓦兹信息准则  15.12378

<!-- 第 15 页 -->
计量经济软件Eviews 上机指导及演示示例

#### 似然函数的对数  -193.3510 F 统计量  3645.290

#### DW 统计量  0.244011 F 统计量的概率  0.000000

单击Equation 窗口中的Resid 按钮，将显示模型的拟合图和残差图。
20000
15000
10000
1000
5000
500
0
0
-500
-1000

# 78 80 82 84 86 88 90 92 94 96 98 00 02
Residual Actual Fitted

图2-17  拟合图和残差图

单击Equation 窗口中的View → Actual, Fitted, Resid → Table 按钮，可以得到
拟合直线和残差的有关结果。

图2-18

#### 五、预测

在Equation 框中选Forecast 项后，弹出Forecast 对话框，Eviews 自动计算出样本
估计期内的被解释变量的拟合值，拟合变量记为YF，其拟合值与实际值的对比图如图2-19
所示。

<!-- 第 16 页 -->
计量经济软件Eviews 上机指导及演示示例

25000

|0|Col2|
|---|---|
|||
|||
|||
|||
|||

Forecast: YF
Actual: Y

# 20000 Forecast sample: 1978 2003
Included observations: 26

# 15000 Root Mean Squared Error 410.6078
Mean Absolute Error     363.4227
Mean Abs. Percent Error 5.438789

# 10000 Theil Inequality Coefficient 0.021596
Bias Proportion       0.000000
Variance Proportion 0.001641

# 5000       Covariance Proportion 0.998359

0

# 78 80 82 84 86 88 90 92 94 96 98 00 02
YF ?2 S.E.

图2-19

下面预测2004 年我国最终消费支出。
1．首先将样本期范围从1978-2003 年扩展为1978-2004 年。即单击工作文件框中Pros
中的Change workfile range，如图2-20 所示，并将1978-2003 改为1978-2004，如图2-21
所示。

图2-20

<!-- 第 17 页 -->
计量经济软件Eviews 上机指导及演示示例

图2-21

2．然后编辑解释变量X。在Group 数据框中输入变量X 的2004 年数据38000.00。（见
图2-22）

图2-22

<!-- 第 18 页 -->
计量经济软件Eviews 上机指导及演示示例

3．点预测。在前面Equation 对话框中选Forecast，将时间Sample 定义在1978-2004，

#### ˆY
如图2-23 所示，这时Eviews 自动计算出 2004 =21202.8727955，如图2-24 所示。

图2-23

图2-24

<!-- 第 19 页 -->
计量经济软件Eviews 上机指导及演示示例

4．区间预测。在Group 数据框中单击View，选Descriptive Stats 里的Common Sample
Eviews，计算出有关X 和Y 的描述统计结果，如图2-25 所示。

图2-25

图2-26  X 和Y 的描述统计结果

根据图2-26 可计算出如下结果：

<!-- 第 20 页 -->
计量经济软件Eviews 上机指导及演示示例

####  x2  (n )12  (26 )1  (9357.245)2  2188950850
X

#### ( X  X )2  (38000 14138.17)2  569386930.9
2004

#### 给定显著性水平 0.05，查表得 t (24)  .2056 ，由
.0025

#### 1 ( X  X )2

#### Y  Yˆ  t (n  2)ˆ 1   0

#### 0 0 .0025 n  x2

#### 可得Y 的预测区间为：
2004

#### 1 5693869309.

#### 21202.8727955 2.056427.3742 1    21202.8727955 100

#### 26 2188950850

### 1.30364

#### 即Y 的95%预测区间为（20201.56915，22204.17643）。
2004

#### 六、非线性回归模型的估计

#### 1

#### 1．倒数模型：Y      

#### 0 1 X
在命令窗口直接依次键入
GENR  X1=1/X
LS  Y  C  X1

#### 2．多项式模型：Y     X   X 2  

# 0 1 2
在命令窗口直接依次键入
GENR  X1=X
GENR  X2=X^2
LS  Y  C  X1  X2

#### 3．准对数模型：Y     ln X  

# 0 1
在命令窗口直接依次键入
GENR  lnX=LOG(X)
LS  Y  C  lnX

#### 4．双对数模型： lnY     ln X  

# 0 1
在命令窗口直接依次键入
GENR  lnX=LOG(X)
GENR  lnY=LOG(Y)
LS  lnY  C  lnX

<!-- 第 21 页 -->
计量经济软件Eviews 上机指导及演示示例

#### 七、异方差检验与解决办法

#### 1． e 2 X 相关图检验法
LS  Y  C  X                 对模型进行参数估计
GENR  E=RESID               求出残差序列
GENR  E2=E^2                求出残差的平方序列
SORT  X                     对解释变量X 排序
SCAT  X  E2                 画出残差平方与解释变量X 的相关图
2．戈德菲尔德——匡特检验
已知样本容量n=26，去掉中间6 个样本点（即约n/4），形成两个样本容量均为10 的
子样本。
SORT  X                     将样本数据关于X 排序
SMPL  1 10                  确定子样本1
LS  Y  C  X                 求出子样本1 的回归平方和RSS1
SMPL  17  26                确定子样本2
LS  Y  C  X                 求出子样本2 的回归平方和RSS2
计算F 统计量并做出判断。
3．加权最小二乘法
LS  Y  C  X                 最小二乘法估计，得到残差序列
GRNR  E1=ABS(RESID)         生成残差绝对值序列
LS(W=1/E1)  Y  C  X         以E1 为权数进行加权最小二成估计

#### 八、自相关检验与解决办法

1．图示法检验
LS  Y  C  X                 最小二乘法估计，得到残差序列
GENR  E=RESID              生成残差序列
SCAT  E(-1)  E             et—et-1的散点图
PLOT  E                    还可绘制et的趋势图
2．广义差分法
LS  Y  C  X  AR(1)  AR(2)

### 第三部分  联立方程计量经济模型Eviews 操作

#### 案例：

1978—2003 年全国居民消费CSt、国民生产总值Yt、投资It、政府消费Gt数据，如下表
所示。

|年<br>份|CS<br>t|Y<br>t|I<br>t|G<br>t|
|---|---|---|---|---|
|1978|1759.100|3605.600|1377.900|468.6000|
|1979|1966.078|3994.118|1445.294|582.7451|

<!-- 第 22 页 -->
计量经济软件Eviews 上机指导及演示示例

|1980|2143.478|4210.268|1470.860|595.9297|
|---|---|---|---|---|
|1981|2352.394|4427.642|1428.184|647.0641|
|1982|2542.465|4866.312|1560.461|763.3865|
|1983|2779.476|5306.812|1751.092|776.2445|
|1984|3121.920|6087.001|2097.366|867.7145|
|1985|3582.358|6863.466|2643.247|637.8610|
|1986|3810.751|7461.561|2832.106|818.7040|
|1987|4091.421|8088.332|2966.369|1030.5422|
|1988|4419.861|8514.186|3181.818|912.5072|
|1989|4190.511|8095.379|2996.559|908.3088|
|1990|4387.675|8820.173|3102.552|1329.9470|
|1991|4827.281|9958.072|3517.548|1613.2429|
|1992|5532.771|11484.769|4278.863|1673.1350|
|1993|6152.373|13534.994|5883.876|1498.7446|
|1994|6708.511|15051.805|6209.091|2134.2037|
|1995|7566.554|16430.918|6705.139|2159.2249|
|1996|8510.402|18086.395|7111.488|2464.5050|
|1997|9152.994|19667.595|7473.109|3041.4916|
|1998|9954.462|21300.431|7966.002|3379.9676|
|1999|10932.296|22977.515|8532.963|3512.2568|
|2000|12103.725|25209.058|9170.372|3934.9605|
|2001|13054.067|28041.212|10654.380|4332.7645|
|2002|14086.916|31094.409|12191.614|4815.8790|
|2003|15194.260|35047.995|14820.508|5033.2276|

建立如下宏观经济模型：
消费函数： CS  Y  CS  
t 0 1 t 2 t1 1t

投资函数： I    Y  
t 0 1 t 2t

收入方程： Y  I  CS  G
t t t t

<!-- 第 23 页 -->
计量经济软件Eviews 上机指导及演示示例

容易判断该联立方程模型中投资方程是过渡识别，消费方程是恰好识别，模型是可识别
的。
下面用四种方法进行二阶段最小二乘法估计参数。这四种方法的输出结果是一样的。

#### 方法一：
第一阶段：LS CS C G CS(-1)          估计消费的简化式方程
GENR ECS=CS-RESID         计算消费的估计值
LS Y C G CS(-1)           估计收入的简化式方程
GENR EY=Y-RESID           计算收入的估计值
第二阶段：LS CS C EY CS(-1)         估计替代后的消费结构式方程
LS I C EY                 估计替代后的投资结构式方程
Dependent Variable: CS

Method: Least Squares

Sample(adjusted): 1979 2003

Included observations: 25 after adjusting endpoints

Variable  Coefficient Std.  t-Statistic  Prob.
Error

C  273.3999 188.4340 1.450905  0.1609

EY  0.265184 0.185426 1.430131  0.1667

CS(-1)  0.433729 0.456004 0.951151  0.3519

R-squared  0.998058     Mean dependent var  6526.600

Adjusted  0.997881     S.D. dependent var  4023.411
R-squared

S.E. of  185.1869     Akaike info  13.39277
regression  criterion

Sum squared  754472.1     Schwarz criterion  13.53904
resid

Log likelihood  -164.4097     F-statistic  5653.343

Durbin-Watson  1.456439     Prob(F-statistic)  0.000000
stat

Dependent Variable: I

Method: Least Squares

Sample(adjusted): 1979 2003

Included observations: 25 after adjusting endpoints

<!-- 第 24 页 -->
计量经济软件Eviews 上机指导及演示示例

Variable  Coefficient Std.  t-Statistic  Prob.
Error

C  -258.6251 219.8342 -1.176455  0.2514

EY  0.401765 0.013389 30.00704  0.0000

R-squared  0.975093     Mean dependent var  5279.634

Adjusted  0.974010     S.D. dependent var  3703.951
R-squared

S.E. of  597.1325     Akaike info  15.69877
regression  criterion

Sum squared  8201047.     Schwarz criterion  15.79628
resid

Log likelihood  -194.2347     F-statistic  900.4222

Durbin-Watson  0.751407     Prob(F-statistic)  0.000000
stat

#### 方法二：

实际上在Eviews 软件中，可以利用命令直接进行二阶段最小二乘估计，命令格式为：
TSLS Yi C 解释变量名 @ C 先决变量名
其中符号@前面是该结构式方程的所有解释变量名，包括内生变量和先决变量；符号@
后面是联立方程模型中的所有前定变量。
因此本例可用TSLS 命令直接写成：
TSLS CS C Y CS(-1)@ C G CS(-1)
TSLS I C Y @ C G CS(-1)
Dependent Variable: CS

Method: Two-Stage Least Squares

Sample(adjusted): 1979 2003

Included observations: 25 after adjusting endpoints

Instrument list:  C G CS(-1)

Variable  Coefficient Std.  t-Statistic  Prob.
Error

C  273.3999 177.3501 1.541583  0.1374

Y  0.265184 0.174519 1.519510  0.1429

CS(-1)  0.433729 0.429181 1.010595  0.3232

<!-- 第 25 页 -->
计量经济软件Eviews 上机指导及演示示例

R-squared  0.998280     Mean dependent var  6526.600

Adjusted  0.998123     S.D. dependent var  4023.411
R-squared

S.E. of regression  174.2940     Sum squared resid  668324.6

F-statistic  6382.063     Durbin-Watson stat  1.003405

Prob(F-statistic)  0.000000

Dependent Variable: I

Method: Two-Stage Least Squares

Sample(adjusted): 1979 2003

Included observations: 25 after adjusting endpoints

Instrument list:  C G CS(-1)

Variable  Coefficient Std.  t-Statistic  Prob.
Error

C  -258.6251 131.6564 -1.964394  0.0617

Y  0.401765 0.008019 50.10444  0.0000

R-squared  0.991067     Mean dependent var  5279.634

Adjusted  0.990678     S.D. dependent var  3703.951
R-squared

S.E. of regression  357.6166     Sum squared resid  2941461.

F-statistic  2510.455     Durbin-Watson stat  0.814465

Prob(F-statistic)  0.000000

#### 方法三：

还可以在方程说明窗口中，选择估计方法为TLSL，并在工具变量兰（Instrument List）
输入模型中的所有先决变量。

#### 方法四：

借助于Eviews 中的System 命令，可以直接进行TSLS 估计。
（1）创建系统：在主菜单上单击Objects → New Object，并在弹出的对象列表框中
选择System；然后在打开的系统窗口输入结构式模型的随机方程
CS=C(1)+C(2)*Y+C(3)*CS(-1)
I=C(4)+C(5)*Y

<!-- 第 26 页 -->
计量经济软件Eviews 上机指导及演示示例

INST G CS(-1)

#### （2）估计模型：在系统窗口单击Estimate，在弹出估计方法选择窗口中选择TSLS 方
法后，单击OK。
System: UNTITLED

Estimation Method: Two-Stage Least Squares

Sample: 1979 2003

Included observations: 25

Total system (balanced) observations 50

Instruments: G CS(-1) C

Coefficient Std.  t-Statistic  Prob.
Error

C(1)  273.3999 177.3501 1.541583  0.1302

C(2)  0.265184 0.174519 1.519510  0.1356

C(3)  0.433729 0.429181 1.010595  0.3176

C(4)  -258.6251 131.6564 -1.964394  0.0557

C(5)  0.401765 0.008019 50.10444  0.0000

Determinant residual covariance 1.35E+09

Equation: CS=C(1)+C(2)*Y+C(3)*CS(-1)

Observations: 25

R-squared  0.998280     Mean dependent var  6526.600

Adjusted  0.998123     S.D. dependent var  4023.411
R-squared

S.E. of  174.2940     Sum squared resid  668324.6
regression

Durbin-Watson  1.003405
stat

Equation: I=C(4)+C(5)*Y

Observations: 25

R-squared  0.991067     Mean dependent var  5279.634

Adjusted  0.990678     S.D. dependent var  3703.951
R-squared

<!-- 第 27 页 -->
计量经济软件Eviews 上机指导及演示示例

S.E. of  357.6166     Sum squared resid  2941461.
regression

Durbin-Watson  0.814465
stat

### 第四部分  演示示例

#### EVIEWS 在计量经济学教学过程中的演示示例（一）

练习一（习题集P17 第8 题）

### 一、按题意在EVIEWS 中输入数据；

二、在主窗口QUICK 菜单下选择estimate equation，在弹出对话框中输入Y C X，进行最
小二乘估计参数。
三、在equantion 窗口viiew 菜单下选择representations 选项，可得回归方程。
Y = 49.82200092 + 0.7944335972*X
四、选择equantion窗口viiew菜单下estimation output或stats按钮，可得回归结果输出：
Dependent Variable: Y
Method: Least Squares
Date: 10/13/05   Time: 19:47
Sample: 1 30
Included observations: 30
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  49.82200 143.7013 0.346705 0.7314
X  0.794434 0.025719 30.88857 0.0000
R-squared  0.971490    Mean dependent var 4342.317
Adjusted R-squared  0.970472    S.D. dependent var 1166.015
S.E. of regression  200.3663    Akaike info  13.50251
criterion
Sum squared resid  1124106.    Schwarz criterion  13.59592
Log likelihood  -200.5377    F-statistic  954.1039
Durbin-Watson stat  1.607925    Prob(F-statistic)  0.000000

### 五、标准报告形式

#### Y = 49.82200092 + 0.7944335972*X

#### （0.346705）    （30.88857）
R-squared＝0.971490  S.E. of regression＝200.3663      F-statistic＝
954.103925503

### 六、点预测

#### Y0 = 49.82200092 + 0.7944335972*1000=844.222(元)

### 七、区间预测

<!-- 第 28 页 -->
计量经济软件Eviews 上机指导及演示示例

##  

####  2

####  1 X X

#### Y  Y  t (n  2) 1   F ，

# F 0  

#### n x2

# 2 i

# 其中      

#### x2 ( X X )2 2 (n )1
i i X
代入相应数据计算即可得区间估计值。
X  Y
Mean   5403.214   4342.317
Median   4926.830   3862.585
Maximum   8839.680   7054.090
Minimum   4009.610   3099.360
Std. Dev.   1446.658   1166.015

#### EVIEWS 在计量经济学教学过程中的演示示例（二）

练习二（习题集P18第10题）

### 一、按题意在EVIEWS 中输入数据；

二、在group 窗口view—graph—scatter—simple scatter，绘制散点图。
选择view—graph—scatter—scatter with regression，绘制回归直线

Y vs. X

# 6 7

6
5
5
4
Y Y 4
3
3
2
2

# 1 1

# 4 6 8 10 12 14 4 6 8 10 12 14
X X

三、在主窗口QUICK 菜单下选择estimate equation，在弹出对话框中输入Y C X，进行最
小二乘估计参数。
四、在equantion 窗口viiew 菜单下选择representations 选项，可得回归方程。
Y = 0.009777361481 + 0.4851934577*X
五、选择equantion窗口viiew菜单下estimation output或stats按钮，可得回归结果输出：
Dependent Variable: Y
Method: Least Squares
Date: 10/13/05   Time: 21:18
Sample: 1985 1996
Included observations: 12
Variable  Coefficien Std. Error t-Statistic Prob.

<!-- 第 29 页 -->
计量经济软件Eviews 上机指导及演示示例

t
C  0.009777 0.284926 0.034315 0.9733
X  0.485193 0.033344 14.55127 0.0000
R-squared  0.954902    Mean dependent var 4.016667
Adjusted R-squared  0.950392    S.D. dependent var 1.138447
S.E. of regression  0.253564    Akaike info  0.244611
criterion
Sum squared resid  0.642947    Schwarz criterion  0.325428
Log likelihood  0.532337    F-statistic  211.7394
Durbin-Watson stat  1.321761    Prob(F-statistic)  0.000000

### 六、点预测

Y = 0.009777361481 + 0.4851934577*X＝0.009777361481 + 0.4851934577*15＝7.2876

#### EVIEWS 在计量经济学教学过程中的演示示例（三）

#### 目的：1、正确使用EVIEWS

#### 2、会使用OLS 和WLS，Goldfeld-Quandt 检验

#### 3、能根据计算结果进行异方差分析和出现异方差性后的补救。

#### 3、数据为demo data1

#### 实例：某市人均储蓄与人均收入的关系分析（异方差性检验及补救）

#### 根据某市1978－1998 年人均储蓄与人均收入的数据资料（见下表），其中X

#### 为人均收入（元），Y 为人均储蓄（元），经分析人均储蓄受人均收入的线性影响，

#### 可建立一元线性回归模型进行分析。

|obs|X|Y|
|---|---|---|
|1978|590.2000|107.0000|
|1979|664.9400|123.0000|
|1980|809.5000|159.0000|
|1981|875.5400|189.0000|
|1982|991.2500|233.0000|
|1983|1109.950|312.0000|
|1984|1357.870|401.0000|
|1985|1682.800|522.0000|
|1986|1890.580|664.0000|
|1987|2098.250|871.0000|
|1988|2499.580|1033.000|
|1989|2827.730|1589.000|
|1990|3084.170|2209.000|
|1991|3462.710|2878.000|
|1992|3932.520|3722.000|

<!-- 第 30 页 -->
计量经济软件Eviews 上机指导及演示示例

|1993|5150.790|5350.000|
|---|---|---|
|1994|7153.350|8080.000|
|1995|9076.850|11758.00|
|1996|10448.21|15839.00|
|1997|11575.48|18196.00|
|1998|12500.84|20954.00|

#### 1、用OLS 估计法估计参数

#### 设模型为：

#### Y     X  

# 1 2

#### 运行EVIEWS 软件，并输入数据，得计算结果如下：

Dependent Variable: Y
Method: Least Squares
Date: 10/11/05   Time: 23:10
Sample: 1978 1998
Included observations: 21
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -2185.998 339.9020 -6.431262 0.0000
X  1.684158 0.062166 27.09150 0.0000
R-squared  0.974766    Mean dependent var 4533.238
Adjusted R-squared  0.973438    S.D. dependent var 6535.103
S.E. of regression  1065.086    Akaike info  16.86989
criterion
Sum squared resid  21553736    Schwarz criterion  16.96937
Log likelihood  -175.1338    F-statistic  733.9495
Durbin-Watson stat  0.293421    Prob(F-statistic)  0.000000

#### 2、异方差检验

#### （1）Goldfeld-Quandt 检验

#### 在Procs 菜单项选Sort series 项，出现排序对话框，输入X，OK。

#### 在Sample 菜单里，将时间定义为1978－1985，用OLS 方法计算得如下结果：

#### Y = -145.441495 + 0.3971185479*X

#### （-8.730234）   （25.42693）

#### R-squared＝0.990805        Sum squared resid1＝15.12284

Dependent Variable: Y
Method: Least Squares
Date: 10/11/05   Time: 23:25
Sample: 1978 1985
Included observations: 8

<!-- 第 31 页 -->
计量经济软件Eviews 上机指导及演示示例

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -145.4415 16.65952 -8.730234 0.0001
X  0.397119 0.015618 25.42693 0.0000
R-squared  0.990805    Mean dependent var 255.7500
Adjusted R-squared  0.989273    S.D. dependent var 146.0105
S.E. of regression  15.12284    Akaike info  8.482607
criterion
Sum squared resid  1372.202    Schwarz criterion  8.502468
Log likelihood  -31.93043    F-statistic  646.5287
Durbin-Watson stat  1.335534    Prob(F-statistic)  0.000000

#### 在Sample 菜单里，将时间定义为1991－1998，用OLS 方法计算得如下结果：

#### Y = -4602.367144 + 1.952519317*X

#### （-5.065962）      （18.40942）

#### R-squared＝0.982604     Sum squared resid2＝5811189.

Dependent Variable: Y
Method: Least Squares
Date: 10/11/05   Time: 23:29
Sample: 1991 1998
Included observations: 8
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -4602.367 908.4882 -5.065962 0.0023
X  1.952519 0.106061 18.40942 0.0000
R-squared  0.982604    Mean dependent var 10847.12
Adjusted R-squared  0.979705    S.D. dependent var 6908.102
S.E. of regression  984.1400    Akaike info  16.83373
criterion
Sum squared resid  5811189.    Schwarz criterion  16.85359
Log likelihood  -65.33492    F-statistic  338.9068
Durbin-Watson stat  0.837367    Prob(F-statistic)  0.000002

# 

#### e2 5811189

# 求F 统计量： F  2   4334.9370 ，查F 分布表，给定显著性

#### e2 1372.202
1

水平 .005 ，得临界值 F (6,6)  .428 ，比较 F  4334.9370 > F (6,6)  .428 ，
.005 .005

#### 拒绝原假设 H 0 :2  2 ，表明随机误差项显著的存在异方差。

# 1 2

#### 3、异方差的修正

<!-- 第 32 页 -->
计量经济软件Eviews 上机指导及演示示例

#### （1）WLS 估计法。

#### 1

#### 首先生成权函数W  ,然后用OLS 估计参数，

#### abs(resid)

#### Y = -2262.639946 + 1.566910934*X
Dependent Variable: Y
Method: Least Squares
Date: 10/12/05   Time: 08:07
Sample: 1978 1998
Included observations: 21
Weighting series: W
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -2262.640 131.2507 -17.23907 0.0000
X  1.566911 0.057637 27.18590 0.0000
Weighted Statistics
R-squared  0.961501    Mean dependent var 2183.201
Adjusted R-squared  0.959475    S.D. dependent var 2104.209
S.E. of regression  423.5951    Akaike info  15.02583
criterion
Sum squared resid  3409224.    Schwarz criterion  15.12530
Log likelihood  -155.7712    F-statistic  474.5211
Durbin-Watson stat  0.354490    Prob(F-statistic)  0.000000
Unweighted
Statistics
R-squared  0.962755    Mean dependent var 4533.238
Adjusted R-squared  0.960794    S.D. dependent var 6535.103
S.E. of regression  1293.978    Sum squared resid  31813191
Durbin-Watson stat  0.224165

#### （2）对数变换法。
用GENR 生成LY 和LX 序列，用OLS 方法求LY 对LX 的回归，结果如下：

#### LY = -6.839135503 + 1.787148637*LX
Dependent Variable: LY
Method: Least Squares
Date: 10/12/05   Time: 00:05
Sample: 1978 1998
Included observations: 21
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -6.839136 0.237565 -28.78845 0.0000
LX  1.787149 0.030033 59.50680 0.0000

<!-- 第 33 页 -->
计量经济软件Eviews 上机指导及演示示例

R-squared  0.994663    Mean dependent var 7.195082
Adjusted R-squared  0.994382    S.D. dependent var 1.746173
S.E. of regression  0.130880    Akaike info  -1.138677
criterion
Sum squared resid  0.325463    Schwarz criterion  -1.039199
Log likelihood  13.95611    F-statistic  3541.059
Durbin-Watson stat  0.642916    Prob(F-statistic)  0.000000

比较方法（1）和（2），可以看出X 与Y 在对数线性回归下拟合效果较好。原因是Y 的曲线
呈对数型图形有关。

25000

20000

15000

10000

5000

0

# 78 80 82 84 86 88 90 92 94 96 98
Y

#### EVIEWS 在计量经济学教学过程中的演示示例（四）

#### 目的：1、正确使用EVIEWS

#### 2、能根据计算结果进行多重共线性检验和出现多重共线性时的补救。

#### 3、数据为demo data2

#### 实例：我国钢材供应量分析（多重共线性检验及补救）

通过分析我国改革开放以来（1978－1997）钢材供应量的历史资料，可以建立一个单一
方程模型。根据理论及对现实情况的认识，影响我国钢材供应量Y（万吨）的主要因素有：
原油产量X1（万吨），生铁产量X2（万吨），原煤产量X3（万吨），电力产量X4（亿千瓦小
时），固定资产投资X5(亿元)，国内生产总值X6(亿元)，铁路运输量X7（万吨）。

|obs|X1|X2|X3|X4|X5|X6|X7|Y|
|---|---|---|---|---|---|---|---|---|
|1978|10405|3479.00|6.81|2566|668.72|3624.1|110119|2208|
|1979|10615|3673|6.35|2820|699.36|4038.2|111893|2497|
|1980|10595|3802|6.2|3006|746.9|4517.8|111279|2716|
|1981|10122|3417|6.22|3093|638.21|4862.4|107673|2670|
|1982|10212|3551|6.66|3277|805.9|5294.7|113495|2920|
|1983|10607|3738|7.15|3514|885.26|5934.5|118784|3072|
|1984|11461|4001|7.89|3770|1052.43|7171|124074|3372|
|1985|12490|4834|8.72|4107|1523.51|8964.4|130709|3693|
|1986|13069|5064|8.94|4495|1795.32|10202.2|135635|4058|

<!-- 第 34 页 -->
计量经济软件Eviews 上机指导及演示示例

|1987|13414|5503|9.28|4973|2101.69|11962.5|140653|4386|
|---|---|---|---|---|---|---|---|---|
|1988|13705|5704|9.8|5452|2554.86|14928.3|144948|4689|
|1989|13764|5820|10.54|5848|2340.52|16909.2|151489|4859|
|1990|13831|6238|10.8|6212|2534|18547.9|150681|5153|
|1991|14099|6765|10.87|6775|3139.03|21617.8|152893|5638|
|1992|14210|7589|11.16|7539|4473.76|26638.1|157627|6697|
|1993|14524|8956|11.5|8395|6811.35|34634.4|162663|7716|
|1994|14608|9741|12.4|9281|9355.35|46759.4|163093|8428|
|1995|15004.95|10529.27|13.61|10070.3|10702.97|58478.1|165855|8979|
|1996|15733.39|10722.5|13.97|10813.1|12185.79|67884.6|168803|9338|
|1997|16074.14|11511.41|13.73|11355.53|13838.96|74772.4|169734|9978|

设模型的函数形式为：

#### Y    X   X   X   X   X   X   X  

# 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7

### 一、运用OLS 估计法对上式中参数进行估计，EVIEWS 操作步骤为：

# 1、 在FILE 菜单中选择NEW－WORKFILE，输入起止时间。

# 2、 在主窗口菜单选QUICK－EMPTY GROUP，在编辑数据区输入Y  X1 X2 X3 X4 X5 X6 X7
所对应的数据。

# 3、 在主窗口菜单选在QUICK－ESTIMATE EQUATION，对参数做OSL 估计，输出结果见下
表：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  139.2362 718.2493 0.193855 0.8495
X1  -0.051954 0.090753 -0.572483 0.5776
X2  0.127532 0.132466 0.962751 0.3547
X3  -24.29427 97.48792 -0.249203 0.8074
X4  0.863283 0.186798 4.621475 0.0006
X5  0.330914 0.105592 3.133889 0.0086
X6  -0.070015 0.025490 -2.746755 0.0177
X7  0.002305 0.019087 0.120780 0.9059
R-squared  0.999222    Mean dependent var 5153.350
Adjusted R-squared  0.998768    S.D. dependent var 2511.950
S.E. of regression  88.17626    Akaike info  12.08573
criterion
Sum squared resid  93300.63    Schwarz criterion  12.48402
Log likelihood  -112.8573    F-statistic  2201.081
Durbin-Watson stat  1.703427    Prob(F-statistic)  0.000000
Y = 139.2361608 - 0.05195439459*X1 + 0.1275320853*X2 - 24.294272*X3 +
0.8632825292*X4 + 0.330913843*X5 - 0.07001518918*X6 + 0.002305379405*X7

### 二、分析

由F=2201.081>F0.05(7,12)=2.91（显著性水平a=0.05），表明模型从整体上看钢材供应

<!-- 第 35 页 -->
计量经济软件Eviews 上机指导及演示示例

量与解释变量之间线性关系显著。

### 三、检验

计算解释变量之间的简单相关系数。EVIEWS 过程如下：
1、 主菜单QUICK－GROUP STATISTICS－CORRRELATION，在对话框中输入X1 X2 X3 X4 X5
X6 X7，结果如下：
X1  X2  X3  X4  X5  X6  X7

X1   1.000000   0.921956   0.975474   0.931882   0.826401   0.845837   0.986815
X2   0.921956   1.000000   0.964400   0.994921   0.969686   0.972530   0.931689
X3   0.975474   0.964400   1.000000   0.974809   0.894963   0.913344   0.982943
X4   0.931882   0.994921   0.974809   1.000000   0.959613   0.969105   0.945444
X5   0.826401   0.969686   0.894963   0.959613   1.000000   0.996169   0.827643
X6   0.845837   0.972530   0.913344   0.969105   0.996169   1.000000   0.846079
X7   0.986815   0.931689   0.982943   0.945444   0.827643   0.846079   1.000000

# 2、由上表可以看出，解释变量之间存在高度线性相关性。尽管方程整体线性回归拟合
较好，但X1 X2 X3 X7 变量的参数t 值并不显著， X3 X6 系数的符号与经济意义相悖。表
明模型确实存在严重的多重共线性。

### 四、修正

# 1、运用OLS 方法逐一求Y 对各个解释变量的回归。结合经济意义和统计检验选出拟合效果
最好的一元线性回归方程。

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -10123.78 1528.060 -6.625250 0.0000
X1  1.181784 0.116936 10.10629 0.0000
R-squared  0.850171    Mean dependent var 5153.350
Adjusted R-squared  0.841847    S.D. dependent var 2511.950
S.E. of regression  998.9623    Akaike info  16.74595
criterion
Sum squared resid  17962663    Schwarz criterion  16.84552
Log likelihood  -165.4595    F-statistic  102.1371
Durbin-Watson stat  0.217842    Prob(F-statistic)  0.000000

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -618.7199 108.3930 -5.708116 0.0000
X2  0.926212 0.016019 57.82017 0.0000
R-squared  0.994645    Mean dependent var 5153.350
Adjusted R-squared  0.994347    S.D. dependent var 2511.950
S.E. of regression  188.8610    Akaike info  13.41454
criterion
Sum squared resid  642032.9    Schwarz criterion  13.51411
Log likelihood  -132.1454    F-statistic  3343.172

<!-- 第 36 页 -->
计量经济软件Eviews 上机指导及演示示例

Durbin-Watson stat  0.962290    Prob(F-statistic)  0.000000

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -3770.942 581.6642 -6.483023 0.0000
X3  926.7178 58.38537 15.87243 0.0000
R-squared  0.933317    Mean dependent var 5153.350
Adjusted R-squared  0.929612    S.D. dependent var 2511.950
S.E. of regression  666.4367    Akaike info  15.93641
criterion
Sum squared resid  7994483.    Schwarz criterion  16.03598
Log likelihood  -157.3641    F-statistic  251.9341
Durbin-Watson stat  0.477559    Prob(F-statistic)  0.000000

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -34.32474 91.75324 -0.374098 0.7127
X4  0.884047 0.014146 62.49381 0.0000
R-squared  0.995412    Mean dependent var 5153.350
Adjusted R-squared  0.995157    S.D. dependent var 2511.950
S.E. of regression  174.8044    Akaike info  13.25985
criterion
Sum squared resid  550018.2    Schwarz criterion  13.35942
Log likelihood  -130.5985    F-statistic  3905.476
Durbin-Watson stat  0.824221    Prob(F-statistic)  0.000000
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  2896.350 211.0245 13.72518 0.0000
X5  0.572451 0.036983 15.47892 0.0000
R-squared  0.930123    Mean dependent var 5153.350
Adjusted R-squared  0.926241    S.D. dependent var 2511.950
S.E. of regression  682.2088    Akaike info  15.98319
criterion
Sum squared resid  8377359.    Schwarz criterion  16.08276
Log likelihood  -157.8319    F-statistic  239.5971
Durbin-Watson stat  0.181794    Prob(F-statistic)  0.000000

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  2720.664 205.3405 13.24952 0.0000
X6  0.108665 0.006568 16.54535 0.0000

<!-- 第 37 页 -->
计量经济软件Eviews 上机指导及演示示例

R-squared  0.938303    Mean dependent var 5153.350
Adjusted R-squared  0.934875    S.D. dependent var 2511.950
S.E. of regression  641.0376    Akaike info  15.85869
criterion
Sum squared resid  7396725.    Schwarz criterion  15.95827
Log likelihood  -156.5869    F-statistic  273.7485
Durbin-Watson stat  0.259927    Prob(F-statistic)  0.000000

Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -9760.099 1317.227 -7.409582 0.0000
X7  0.106826 0.009326 11.45524 0.0000
R-squared  0.879375    Mean dependent var 5153.350
Adjusted R-squared  0.872673    S.D. dependent var 2511.950
S.E. of regression  896.3356    Akaike info  16.52915
criterion
Sum squared resid  14461517    Schwarz criterion  16.62872
Log likelihood  -163.2915    F-statistic  131.2225
Durbin-Watson stat  0.183657    Prob(F-statistic)  0.000000

经分析在7 个一元回归模型中钢材供应量Y 对电力产量X4 的线性关系强，拟合度好，
即：

#### Y = -34.32474492 + 0.8840472792*X4

#### （-0.374098）    （62.49381）
R2= 0.995412   S.E.=174.8044，F=3905.476
截距项不显著，去掉，重新估计：

#### Y = 0.8792594492*X4

# 2、逐步回归。
将其余解释变量逐一代入上式，得如下模型：

#### Y = -0.005935225118*X1 + 0.8906555628*X4

#### （-0.604681）    （45.03888）
R2= 0.995469   S.E.=173.7270，    F=3954.290
式中X1 不显著，删去，继续：

#### Y = 0.1741981867*X2 + 0.6978252624*X4

#### （1.879546）    （7.217200）
R2= 0.996135   S.E.=160.4431，    F=4639.290

#### Y = 0.2753793175*X2 + 0.5595511241*X4 + 0.04060861466*X5
（3.082485）        （5.637333）         （2.615818）
R2= 0.997244   S.E.=139.4060，    F=3075.985

Y = 0.466836912*X2 + 0.5219953469*X4 - 0.03080496295*X5 - 0.004998894793*X7
（3.245804）      （5.366654）       （-0.674009）       （-1.651391）

<!-- 第 38 页 -->
计量经济软件Eviews 上机指导及演示示例

R2= 0.997646   S.E.=132.8222，    F=2259.899
X7 不符合经济意义，应去掉。

所以：

#### Y = 0.2753793175*X2 + 0.5595511241*X4 + 0.04060861466*X5
（3.082485）        （5.637333）         （2.615818）
R2= 0.997244   S.E.=139.4060，    F=3075.985
即为最优模型。
Dependent Variable: Y
Method: Least Squares
Date: 10/17/05   Time: 22:53
Sample: 1978 1997
Included observations: 20
Variable  Coefficien Std. Error t-Statistic Prob.
t
X2  0.275379 0.089337 3.082485 0.0068
X4  0.559551 0.099258 5.637333 0.0000
X5  0.040609 0.015524 2.615818 0.0181
R-squared  0.997244    Mean dependent var 5153.350
Adjusted R-squared  0.996920    S.D. dependent var 2511.950
S.E. of regression  139.4060    Akaike info  12.85014
criterion
Sum squared resid  330378.5    Schwarz criterion  12.99950
Log likelihood  -125.5014    F-statistic  3075.985
Durbin-Watson stat  0.790639    Prob(F-statistic)  0.000000

#### EVIEWS 在计量经济学教学过程中的演示示例（五）

#### 目的：1、正确使用EVIEWS

#### 2、能根据计算结果进行序列相关性检验和补救。

#### 3、数据为demo data3

#### 实例：国内生产总值和出口总额之间的关系分析（序列相关性检验及补救）

根据某地区1978－1998 年国内生产总值与出口总额的数据资料，其中X 表示国内生产
总值（人民币亿元），Y 表示出口总额（人民币亿元）。试建立一元线性回归函数。设模型函
数形式为：

#### Y     X  
t 1 2 t t
obs  X  Y

# 1978   3624.100   134.8000

# 1979   4038.200   139.7000

# 1980   4517.800   167.6000

<!-- 第 39 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1981   4860.300   211.7000

# 1982   5301.800   271.2000

# 1983   5957.400   367.6000

# 1984   7206.700   413.8000

# 1985   8989.100   438.3000

# 1986   10201.40   580.5000

# 1987   11954.50   808.9000

# 1988   14922.30   1082.100

# 1989   16917.80   1470.000

# 1990   18598.40   1766.700

# 1991   21622.50   1956.000

# 1992   26651.90   2985.800

# 1993   34560.50   3827.100

# 1994   46670.00   4676.300

# 1995   57494.90   5284.800

# 1996   66850.50   10421.80

# 1997   73142.70   12451.80

# 1998   78017.80   15231.70

# 1、用OLS 估计方法求模型的参数估计值
点击NEW－WORKFILE，输入X,Y 的数据。
点击QUICK－ESITMATE EQUATION，在对话框中输入Y  C  X，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -1147.443 396.1630 -2.896390 0.0093
X  0.170052 0.011451 14.84990 0.0000
R-squared  0.920675    Mean dependent var 3080.390
Adjusted R-squared  0.916500    S.D. dependent var 4368.710
S.E. of regression  1262.402    Akaike info  17.20981
criterion
Sum squared resid  30279518    Schwarz criterion  17.30929
Log likelihood  -178.7030    F-statistic  220.5196
Durbin-Watson stat  0.688670    Prob(F-statistic)  0.000000

# 2、自相关检验

#### （1）图示法
由上述OLS 计算，可直接得到残差RESID，运用GENR 命令生成序列E，则在QUICK 菜
单中选GRAPH，在图形对话框中输入：E  E(-1)，再点击SCATTER DIOGRAM。得结果如下，
从图中可以看出残差et呈线性自回归，表明随机误差ut存在自相关。

<!-- 第 40 页 -->
计量经济软件Eviews 上机指导及演示示例

4000

2000

0
E

-2000

-4000
-4000 -3000 -2000 -1000 0 1000 2000

E(-1)

#### （2）、DW 检验
根据OLS 计算结果，由：Durbin-Watson stat＝0.688670，给定显著性水平a=0.05，
查D-W 表，n=21，k'（解释变量个数）＝1，得下限临界值dL=1.22，上限临界值dU=1.42，
因为DW 统计量为0.688670<dL=1.22。根据判定区域知，此时随机误差项存在一阶自相关。

# 3、自相关的修正

####  DW 

#### （1）由DW＝0.688670，根据  1  ，计算得 ＝0.6556。

#### 2
用GENR 分别对X 和Y 做广义差分。在WORKFILE 窗口选择GENR 或直接在主窗口输入：
GENR DY=Y-0.6556*Y(-1)
GENR DX=X-0.6556*X(-1)
然后再用OLS 估计参数。结果为：

#### DY = -585.3252045 + 0.192825853*DX

#### （-1.752142）     （8.851754）

#### R2= 0.813188  DW=1.345597，    F=78.35354
这时可以看出使用广义差分法后，DW 值有所提高，但仍然存在自相关。

#### （2）Cochrane-Orcutt 迭代法
在QUICK－ESTIMATE EQUATION 项，在对话框中输入：Y  C  X  AR(1),OK 后得如下结
果：
Dependent Variable: Y
Method: Least Squares
Date: 10/31/05   Time: 18:07
Sample(adjusted): 1979 1998
Included observations: 20 after adjusting endpoints
Convergence achieved after 14 iterations
Variable  Coefficien Std. Error t-Statistic Prob.
t

<!-- 第 41 页 -->
计量经济软件Eviews 上机指导及演示示例

C  -1876.253 1975.932 -0.949554 0.3556
X  0.198637 0.049973 3.974859 0.0010
AR(1)  0.740777 0.310956 2.382259 0.0292
R-squared  0.951955    Mean dependent var 3227.670
Adjusted R-squared  0.946303    S.D. dependent var 4428.390
S.E. of regression  1026.178    Akaike info  16.84255
criterion
Sum squared resid  17901699    Schwarz criterion  16.99191
Log likelihood  -165.4255    F-statistic  168.4172
Durbin-Watson stat  1.451436    Prob(F-statistic)  0.000000
Inverted AR Roots         .74

此时DW=1.451436>dU=1.42，认为此时无自相关性。
（3）利用对数线性回归修正自相关。用GENR 分别对X 和Y 生成LogX 和LogY，命令为：
GENR LY=LOG(Y)
GENR LX=LOG(X)
在OLS 估计对话框输入： LY  C  LX 计算结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -7.083917 0.337892 -20.96504 0.0000
LX  1.466088 0.034876 42.03750 0.0000
R-squared  0.989363    Mean dependent var 7.043795
Adjusted R-squared  0.988803    S.D. dependent var 1.515819
S.E. of regression  0.160400    Akaike info  -0.731905
criterion
Sum squared resid  0.488832    Schwarz criterion  -0.632427
Log likelihood  9.685003    F-statistic  1767.151
Durbin-Watson stat  1.140571    Prob(F-statistic)  0.000000

同时考虑Cochrane-Orcutt 迭代法。在估计对话框里输入： LY  C  LX  AR(1)
计算结果如下：
Dependent Variable: LY
Method: Least Squares
Date: 10/31/05   Time: 18:19
Sample(adjusted): 1979 1998
Included observations: 20 after adjusting endpoints
Convergence achieved after 5 iterations
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -7.088071 0.604260 -11.73016 0.0000
LX  1.467507 0.061299 23.94022 0.0000
AR(1)  0.425084 0.232705 1.826708 0.0854

<!-- 第 42 页 -->
计量经济软件Eviews 上机指导及演示示例

R-squared  0.990102    Mean dependent var 7.150795
Adjusted R-squared  0.988937    S.D. dependent var 1.471582
S.E. of regression  0.154782    Akaike info  -0.756115
criterion
Sum squared resid  0.407278    Schwarz criterion  -0.606756
Log likelihood  10.56115    F-statistic  850.2191
Durbin-Watson stat  1.537282    Prob(F-statistic)  0.000000
Inverted AR Roots         .43

此时DW=1.537282>dU=1.42，可以认为此时已消除自相关性。

#### EVIEWS 在计量经济学教学过程中的演示示例（六）

#### 目的：1、正确使用EVIEWS

#### 2、对分布滞后模型能进行析和计算，会使用经验加权法、阿尔蒙法、自

#### 回归模型的估计和检验等方法。

#### 3、数据为demo data4 demo data5、demo data6

#### 方法1：（经验加权法）
已知某地区制造业部门1955－1974 年期间的资本存量Y 和销售额X 的统计资料如下表
（金额单位：百万元）。设定有限分布滞后模型为：

#### Y    X  X   X   X  
t 0 t 1 t1 2 t2 3 t3 t
运用经验加权法，选择下列三组权数：

#### （1）1、1/2、1/4、1/8

#### （2）1/4、1/2、2/3、1/4

#### （3）1/4、1/4、1/4、1/4、
分别估计上述模型，并从中选择最佳的方程。
obs  SER01  SER02

# 1955   450.6900   264.8000

# 1956   506.4200   277.4000

# 1957   518.7000   287.3600

# 1958   500.7000   272.8000

# 1959   527.0700   302.1900

# 1960   538.1400   307.9600

# 1961   549.3900   308.9600

# 1962   582.1300   331.1300

# 1963   600.4300   350.3200

# 1964   633.8300   373.3500

# 1965   682.2100   410.0300

# 1966   779.6500   448.6900

# 1967   846.6500   464.4900

<!-- 第 43 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1968   908.7500   502.8200

# 1969   970.7400   535.5500

# 1970   1016.450   528.5900

# 1971   1024.450   559.1700

# 1972   1077.190   620.1700

# 1973   1208.700   713.9800

# 1974   1471.350   820.9800
记新的线性组合变量分别为：

#### 1 1 1

#### Z  X  X  X  X

#### 1 t 2 t1 4 t2 8 t3

#### 1 1 2 1

#### Z  X  X  X  X

#### 2 4 t 2 t1 3 t2 4 t3

#### 1 1 1 1

#### Z  X  X  X  X

#### 3 4 t 4 t1 4 t2 4 t3
分别估计如下经验加权模型：

#### Y    Z   k  3,2,1
t kt t
具体步骤为：

# 1、 打开EVIEWS，输入X，Y 的数据，生成线性组合变量Z1,Z2,Z3的数据；

#### genr z1=xt+(1/2)*xt(-1)+(1/4)*xt(-2)+(1/8)*xt(-3)

#### genr z2=(1/4)*xt+(1/2)*xt(-1)+(2/3)*xt(-2)+(1/4)*xt(-3)

#### genr z3=(1/4)*xt+(1/4)*xt(-1)+(1/4)*xt(-2)+(1/4)*xt(-3)

# 2、 回归分析。在EQUATION SPECIFICATION 对话框中，输入 Y C Z1，在ESTIMAYIONS
栏中选择OLS，点击OK，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -66.52295 18.16484 -3.662182 0.0023
Z1  1.071395 0.021024 50.96149 0.0000
R-squared  0.994257    Mean dependent var 818.6959
Adjusted R-squared  0.993875    S.D. dependent var 279.9181
S.E. of regression  21.90777    Akaike info  9.121691
criterion
Sum squared resid  7199.257    Schwarz criterion  9.219716
Log likelihood  -75.53437    F-statistic  2597.074
Durbin-Watson stat  1.439440    Prob(F-statistic)  0.000000
用Z2,Z3分别进行回归估计，结果整理如下：

#### YT = -66.52294932 + 1.071395456*Z1

#### （-3.662182）     （50.96149）

#### R-squared＝0.994257  DW＝1.439440   F＝2597.074

#### YT = -133.1722303 + 1.366668187*Z2

#### （-5.029746）     （37.37033）

<!-- 第 44 页 -->
计量经济软件Eviews 上机指导及演示示例

#### R-squared＝0.989373  DW＝1.042713   F＝1396.542

#### YT = -121.7394467 + 2.237930494*Z3

#### （-4.813143）     （38.68578）

#### R-squared＝0.990077  DW＝1.158530   F＝1496.590
从上述回归分析结果可以看出，模型一的扰动项无一阶自相关，模型二和模型三扰动
项存在一阶正相关；在综合判断可决系数、F－检验值，t 检验值，可以认为：最佳的方程
式模型一，即权数为1、1/2、1/4、1/8 的分布滞后模型。

#### 方法2：（阿尔蒙法）
下表给出某行业1955－1974 年的库存额Y 和销售额X 的资料。假定库存额取决于本年
销售额和前三年的销售额，估计如下分布滞后模型：
obs  XT  YT

# 1955   26.48000   45.06900

# 1956   27.74000   50.64200

# 1957   28.23600   51.87100

# 1958   27.28000   52.07000

# 1959   30.21900   52.70900

# 1960   30.79600   53.81400

# 1961   30.89600   54.93900

# 1962   33.11300   58.12300

# 1963   35.03200   60.04300

# 1964   37.33500   63.38300

# 1965   41.00300   68.22100

# 1966   44.86900   77.96500

# 1967   46.44900   84.65500

# 1968   50.28200   90.81500

# 1969   53.55500   97.07400

# 1970   52.85900   101.6400

# 1971   55.91700   102.4400

# 1972   62.01700   107.7100

# 1973   71.39800   120.8700

# 1974   82.07800   147.1300

#### Y   X  X   X   X  
t 0 t 1 t1 2 t2 3 t3 t
假定系数β可以用二次多项式近似，即

####   

# 0 0

####     

# 1 0 1 2

####     2  4

# 2 0 1 2

####     3  9

# 2 0 1 2
则模型可变为：

<!-- 第 45 页 -->
计量经济软件Eviews 上机指导及演示示例

#### Y   Z Z  Z  
t 0 0t 1 1t 2 2t t
其中

#### Z  X  X  X  X
0t t t1 t2 t3

#### Z  X  2X  3X
1t t1 t2 t3

#### Z  X  4X  9X
2t t1 t2 t3
在EVIEWS 中输入XT 和YT 的数据，然后在工作文件的工具条上选择生成新数据序列的
GENR 命令，在打开的EQUATION 对话框中依次键入生成Z0t，Z1t，Z2t 的公式。

#### GENR Z0T=XT+XT(-1)+XT(-2)+XT(-3)

#### GENR Z1T=XT(-1)+2*XT(-2)+3*XT(-3)

#### GENR Z2T=XT(-1)+4*XT(-2)+9*XT(-3)

#### 打开EQUATION SPECIFICATION对话框，键入回归方程形式：

#### Y  C  Z0T  Z1T  Z2T

#### 点击OK，结果如下表：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -6.419601 2.130157 -3.013675 0.0100
Z0T  0.630281 0.179160 3.517969 0.0038
Z1T  0.987410 0.525307 1.879682 0.0827
Z2T  -0.460829 0.181199 -2.543216 0.0245
R-squared  0.996230    Mean dependent var 81.97653
Adjusted R-squared  0.995360    S.D. dependent var 27.85539
S.E. of regression  1.897384    Akaike info  4.321154
criterion
Sum squared resid  46.80087    Schwarz criterion  4.517204
Log likelihood  -32.72981    F-statistic  1145.160
Durbin-Watson stat  1.513212    Prob(F-statistic)  0.000000
  

#### 表中，Z0t，Z1t，Z2t 对应的系数分别为 ,, 的估计值 , , 。将它们代入分布

# 0 1 2 0 1 2
   

#### 滞后阿尔蒙多项式中，可以计算出 , , , 的估计值为：

# 0 1 2 3

 

####     .0630281,

# 0 0
   

####       .1157

# 1 0 1 2
   

####     2  4  .0762

# 2 0 1 2
   

####     3  9  .0555

# 3 0 1 2
从而，分布滞后模型的最终估计形式为：


#### Y  .64196  .0631X  .1157 X  .0762X  .0555X
t t t1 t2 t3
在实际应用中，EVIEWS 提供了多项式分布滞后指令“PDL”用于估计分布滞后模型。下

<!-- 第 46 页 -->
计量经济软件Eviews 上机指导及演示示例

面给出本例的操作过程。

#### 在EVIEWS 中输入XT,YT 的数据，进入EQUATION SPECIFICATION 对话框，输入方

#### 程形式：

#### Y  C  PDL(X,3,2)

#### 其中，“PDL”指令表示进行阿尔蒙多项式分布滞后模型的估计，括号中的3 表示X 的分布
滞后长度，2 表示阿尔蒙多项式的阶数。在ESTIMATION SETTING 中选择OLS，点击OK，结
果如下：
Variable  Coefficient Std. Error t-Statistic  Prob.
C  -6.419601 2.130157 -3.013675  0.0100
PDL01  1.156862 0.195928 5.904516  0.0001
PDL02  0.065752 0.176055 0.373472  0.7148
PDL03  -0.460829 0.181199 -2.543216  0.0245
R-squared  0.996230 Mean dependent var  81.97653
Adjusted R-squared  0.995360 S.D. dependent var  27.85539
S.E. of regression  1.897384 Akaike info criterion  4.321154
Sum squared resid  46.80087 Schwarz criterion  4.517204
Log likelihood  -32.72981 F-statistic  1145.160
Durbin-Watson stat  1.513212 Prob(F-statistic)  0.000000
Lag Distribution of XT  i  Coefficient Std. Error T-Statisti
c
.     *     |  0   0.63028   0.17916   3.51797
.          *|  1   1.15686   0.19593   5.90452
.      *    |  2   0.76178   0.17820   4.27495
*    .           |  3  -0.55495   0.25562  -2.17104
Sum of Lags  1.99398   0.06785   29.3877
注意：用“PDL”估计分布滞后模型时，EVIEWS 所采用的滞后系数多项式变换不是上面的形
式，而是阿尔蒙多项式的派生形式。因此结果中PDL01，PDL02，PDL03 对应的估计系数不是

#### 阿尔蒙多项式系数 ,, 的估计。但同前面分步计算的结果比较，最终的分布滞后估计

# 0 1 2

   

#### 系数 , , , 是相同的。

# 0 1 2 3

#### 方法3：（自回归模型的估计和检验）

下表给出了没地区消费总额Y（亿元）和货币收入总额X（亿元）的年度资料，分析消
费和收入的关系。
obs  X  Y

# 1966   103.1690   91.15800

# 1967   115.0700   109.1000

# 1968   132.2100   119.1870

# 1969   156.5740   143.9080

<!-- 第 47 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1970   166.0910   155.1920

# 1971   155.0990   148.6730

# 1972   138.1750   151.2880

# 1973   146.9360   148.1000

# 1974   157.7000   156.7770

# 1975   179.7970   168.4750

# 1976   195.7790   174.7370

# 1977   194.8580   182.8020

# 1978   189.1790   180.1300

# 1979   199.9630   190.4440

# 1980   250.7170   196.9000

# 1981   215.5390   204.7500

# 1982   220.3910   218.6660

# 1983   235.4830   227.4250

# 1984   280.9750   229.8600

# 1985   292.3390   244.2300

# 1986   278.1160   258.3630

# 1987   292.6540   275.2480

# 1988   341.4420   299.2770

# 1989   401.1410   345.4700

# 1990   458.5670   406.1190

# 1991   500.9150   462.2230

# 1992   450.9390   492.6620

# 1993   626.7090   539.0460

# 1994   783.9530   617.5680

# 1995   890.6370   727.3970
为了考察收入对消费的影响，首先做Y 关于X 的回归，即建立如下的回归模型

#### Y    X  
t 0 t t
得结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  26.12309 8.246128 3.167922 0.0037
X  0.809209 0.023638 34.23312 0.0000
R-squared  0.976665    Mean dependent var 262.1725
Adjusted R-squared  0.975831    S.D. dependent var 159.3349
S.E. of regression  24.77059    Akaike info  9.321532
criterion
Sum squared resid  17180.30    Schwarz criterion  9.414945
Log likelihood  -137.8230    F-statistic  1171.906
Durbin-Watson stat  1.352981    Prob(F-statistic)  0.000000
从回归结果看，在判断可决系数、F－检验值，t 检验值都显著，但在显著性水平a=0.05
上。DW＝1.35>dl=1.3 不能判断。对模型进行改进。事实上，当年消费不仅受当年收入得影

<!-- 第 48 页 -->
计量经济软件Eviews 上机指导及演示示例

响，而且还受过去各年收入水平的影响，因此，对上述模型中添加货币收入总额X 的滞后变
量进行分析。如前所述，对分布滞后模型直接进行估计会存在自由度损失和多重共线性等问
题。在此，选择库伊克模型进行回归估计，即估计如下模型：

#### Y     X  Y  
t 0 t 1 t1 t
利用所给数据得回归结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -8.140848 4.281553 -1.901378 0.0684
X  0.240752 0.045060 5.342898 0.0000
Y(-1)  0.830523 0.064854 12.80598 0.0000
R-squared  0.996740    Mean dependent var 268.0696
Adjusted R-squared  0.996490    S.D. dependent var 158.7886
S.E. of regression  9.407876    Akaike info  7.418669
criterion
Sum squared resid  2301.211    Schwarz criterion  7.560113
Log likelihood  -104.5707    F-statistic  3975.259
Durbin-Watson stat  1.238470    Prob(F-statistic)  0.000000

从回归结果看，在判断可决系数、F－检验值，t 检验值都显著，但

#### dw n 1 29

#### h  1(  )  1(  .123847)

#### 2  2 1  29  0.0648542

#### 1  nVar( )
1

####  .224

#### 在显著性水平 a ＝0.05 上，查标准正态分布临界值 h  .196 ，由于

2

#### h  .224  h  .196 ，拒绝原假设  0 ，说明回归模型存在一阶自相关，需要对模型做

2
进一步修改。

下面换一个角度进行分析。消费者得消费是一个复杂得过程。一方面，预期收入得大小
可能会影响消费，即消费者会按照收入预期决定自己得消费计划；另一方面，实际消费往往
与预计得消费之间存在偏差，消费者会对预期得消费计划进行调整。因此，可以考虑采用局
部调整——自适应期望综合模型进行分析。
如前所述，在局部调整假设和自适应假设下，局部调整——自适应期望综合模型可转化
为如下形式得自回归模型：

#### Y     X  Y  Y  
t 0 t 1 t1 2 t2 t
利用所给数据进行估计，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -3.038540 4.018267 -0.756182 0.4569
X  0.225020 0.035669 6.308632 0.0000

<!-- 第 49 页 -->
计量经济软件Eviews 上机指导及演示示例

Y(-1)  1.305370 0.128310 10.17359 0.0000
Y(-2)  -0.516627 0.134074 -3.853306 0.0008
R-squared  0.998104    Mean dependent var 273.7470
Adjusted R-squared  0.997867    S.D. dependent var 158.6766
S.E. of regression  7.328427    Akaike info  6.952962
criterion
Sum squared resid  1288.940    Schwarz criterion  7.143277
Log likelihood  -93.34147    F-statistic  4211.360
Durbin-Watson stat  2.332370    Prob(F-statistic)  0.000000

从回归结果看，在判断可决系数、F－检验值，t 检验值都显著，且

#### dw n 1 28

#### h  1(  )  1(   .2233)

#### 2  2 1  28  0.128312

#### 1  nVar( )
1

####  .0786

#### 在显著性水平 a ＝0.05 上，查标准正态分布临界值 h  .196 ，由于

2

#### h  .0786  h  .196 ，接受原假设  0 ，说明回归模型扰动项不存存在一阶自相关，

2
最终的估计模型为：

#### Y = -3.0386 + 0.2250*X + 1.3054*Y(-1) - 0.5166*Y(-2)

#### （-0.7562）（6.309）  （10.174）     （-3.853）

#### R-squared＝0.998104  DW＝2.332370   F＝4211.360

#### 该模型较好的解释了所考察地区居民消费和收入之间的关系。

#### EVIEWS 在计量经济学教学过程中的演示示例（七）

#### 目的：1、正确使用EVIEWS

#### 2、对联立方程模型能进行析和计算，会使用两阶段最小二乘法法

#### 3、数据为demo data7

#### 实例1：（两阶段最小二乘法法）

下表为1978－1998 年度我国国内生产总值（GDP）、货币供应量（M2）、政府支出（GCE）
和投资支出（INV）的数据，我们将利用此数据，运用EVIEWS，建立我国的收入——货币供
应模型。
obs  GDP  M2  INV  GCE

# 1978   3624.100   1159.100   1377.900   480.0000

# 1979   4038.200   1458.100   1474.200   614.0000

# 1980   4517.800   1842.900   1590.000   659.0000

# 1981   4862.400   2234.500   1581.000   705.0000

<!-- 第 50 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1982   5294.700   2589.800   1760.200   770.0000

# 1983   5934.500   3075.000   2005.000   838.0000

# 1984   7171.000   4146.300   2468.600   1021.000

# 1985   8964.400   5198.900   3386.000   1184.000

# 1986   10202.20   6720.900   3846.000   1367.000

# 1987   11962.50   8330.900   4322.000   1490.000

# 1988   14928.30   10099.80   5492.000   1727.000

# 1989   16909.20   11949.60   6095.000   2033.000

# 1990   18547.90   15290.40   6444.000   2252.000

# 1991   21617.80   19349.90   7517.000   2830.000

# 1992   26638.10   25402.20   9636.000   3492.300

# 1993   34634.40   34879.80   14998.00   4499.700

# 1994   46759.40   46923.50   19260.60   5982.000

# 1995   58478.10   60750.50   23877.00   6690.500

# 1996   67884.60   76094.90   26867.20   7851.600

# 1997   74462.60   90995.30   28457.60   8724.800

# 1998   79395.70   102297.0   30396.00   9484.800

设定模型为：

#### 收入方程： GDP     M  INV  GCE  
t 10 12 2t 11 t 12 t 1t

#### 货币供应方程： M     GDP  
2t 20 21 t 2t
根据分析，可以判定货币供应方程为过度识别。
在EVIEWS 中输入数据，点击Quick—Estimat Equation,在对话框的上部输入过度识别
方程表达式：
M2  C  GDP
在对话框下部选择估计方法TSLS，此时屏幕弹出Instrument list 对话框，在此对话
框中输入联立方程的全部先决变量：
C  INV  GCE
样本时间（Sample）选择1978  1998 后，OK，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -6035.171 1108.036 -5.446728 0.0000
GDP  1.248089 0.031623 39.46831 0.0000
R-squared  0.988010    Mean dependent var 25275.68
Adjusted R-squared  0.987379    S.D. dependent var 31554.19
S.E. of regression  3544.893    Sum squared resid  2.39E+08
F-statistic  1557.748    Durbin-Watson stat 0.430376
Prob(F-statistic)  0.000000
即货币供应方程为：

#### M2 = -6035.171232 + 1.248088599*GDP
（1108.036）     （0.031623）

<!-- 第 51 页 -->
计量经济软件Eviews 上机指导及演示示例

（-5.446728）     （39.46831）
R2＝0.988010   Adjusted R-squared＝0.987379  F-statistic＝1557.748  DW＝0.430376

下面分两步进行过度识别方程的估计。

# 1、对内生变量GDP 的精确部分进行估计，即对简化式方程1：

#### GDP    INV  GCE  v
t 10 11 t 12 t t
进行OLS 估计。
点击Quick—Estimate Equantion，在弹出对话框上部，输入内生解释变量的简化式方
程：
GDP  C   INV  GCE
接着OK，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -413.5196 476.1544 -0.868457 0.3966
INV  1.100051 0.356854 3.082640 0.0064
GCE  4.828218 1.216720 3.968226 0.0009
R-squared  0.998032    Mean dependent var 25087.04
Adjusted R-squared  0.997814    S.D. dependent var 25091.06
S.E. of regression  1173.247    Akaike info  17.10450
criterion
Sum squared resid  24777169    Schwarz criterion  17.25372
Log likelihood  -176.5973    F-statistic  4564.607
Durbin-Watson stat  0.868802    Prob(F-statistic)  0.000000
即

#### GDP = -413.5196197 + 1.100051492*INV + 4.828217899*GCE
（476.1544）      （0.356854）         （1.216720）
（-0.868457）     （3.082640）         （3.968226）
R2＝0.998032   Adjusted R-squared＝0.997814  F＝4564.607  DW＝0.868802
上述结果表明第一阶段的拟合状态良好。

# 2、为了求得内生解释变量GDP 的精确不分，点击Equation 窗口的Forecast 按钮，OK，
得到预测结果。
在主窗口，点击Quick——Estimate Equation，输入过度识别方程，此时的内生变量
用其精确部分替代：
M2  C  GDPF
OK 后，结果如下：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -6035.171 1318.862 -4.576043 0.0002
GDPF  1.248089 0.037639 33.15912 0.0000
R-squared  0.983013    Mean dependent var 25275.68
Adjusted R-squared  0.982119    S.D. dependent var 31554.19
S.E. of regression  4219.380    Akaike info  19.62316

<!-- 第 52 页 -->
计量经济软件Eviews 上机指导及演示示例

criterion
Sum squared resid  3.38E+08    Schwarz criterion  19.72264
Log likelihood  -204.0431    F-statistic  1099.527
Durbin-Watson stat  0.391075    Prob(F-statistic)  0.000000

说明：（1）这里主要讨论TSLS 在EVIEWS 中的实现，因而没有把注意力放在检验各变量平稳
性、因果性以及是否产生伪回归现象上，有兴趣的同学可以进行相应检验；

#### （2）当直接进行OSL 估计货币供应方程时，结果为：
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -6083.785 1107.368 -5.493917 0.0000
GDP  1.250026 0.031588 39.57246 0.0000
R-squared  0.988012    Mean dependent var 25275.68
Adjusted R-squared  0.987382    S.D. dependent var 31554.19
S.E. of regression  3544.542    Akaike info  19.27460
criterion
Sum squared resid  2.39E+08    Schwarz criterion  19.37408
Log likelihood  -200.3833    F-statistic  1565.980
Durbin-Watson stat  0.429772    Prob(F-statistic)  0.000000
与TSLS 结果比较，可以看出二者回归结果非常接近。因为在TSLS 的第一阶段回归结果中，
R2＝0.998032 已经非常高，是的GDPF 和GDP 几乎相同，因而在第二阶段回归中用GDPF 或
GDP 作为解释变量结果不会有太大差异。
但是，在实证分析中，并不能保证都是上述情况，当第一阶段中R2 不是非常大时，情
况就会不同。
提示：对于过度识别方程，在没有检验TSLS 的第二阶段结果之前不宜接受OLS 的回归结果。

#### EVIEWS 在计量经济学教学过程中的演示示例（八）

#### 目的：1、正确使用EVIEWS

#### 2、对联立方程模型能进行析和计算，会使用两阶段最小二乘法法

#### 3、数据为demo data8

下面给出Klein 于1950 年建立的旨在分析美国在两次世界大战之间的经济发展的小型
宏观计量经济学模型：

#### 消费： C       (W  W )  
t 0 1 t 2 t1 3 pt Gt 1t

#### 投资： I          K  
t 0 1 t 2 t1 3 t1 2t

#### 工资：W    (Y  T  W )  (Y  T  W )  t  
pt 0 1 t t Gt 2 t1 t1 Gt1 3 3t

#### 收入：Y  C  I  G  T
t t t t t

<!-- 第 53 页 -->
计量经济软件Eviews 上机指导及演示示例

#### 利润：   Y  W  W
t t pt Gt

#### 资本存量： K  I  K
t t t1
其中，Y,C,I,WP,WG,Π,K,G,T,t 分别表示收入、消费、投资、私人工资、政府工资、利润、
年末资本存量、政府支出、税收与时间。

#### （1）指出该模型的内生变量、外生变量与先决变量；

#### （2）对模型进行识别；

#### （3）利用下表给出的数据，对模型进行OLS 估计，然后估计模型中出现的内生解释变量的
简化式，并以此为基础进行TSLS 估计。

obs  CT  Π  WP  I  KT-1  Y  WG  G  T

# 1920  28.80000  2.700000
39.80000  12.70000  180.1000 44.90000 2.200000  2.400000  3.400000

# 1921  25.50000 -0.200000
41.90000  12.40000  182.8000 45.60000 2.700000  3.900000  7.700000

# 1922  29.30000  1.900000
45.00000  16.90000  182.6000 50.10000 2.900000  3.200000  3.900000

# 1923  34.10000  5.200000
49.20000  18.40000  184.5000 57.20000 2.900000  2.800000  4.700000

# 1924  33.90000  3.000000
50.60000  19.40000  189.7000 57.10000 3.100000  3.500000  3.800000

# 1925  35.40000  5.100000
52.60000  20.10000  192.7000 61.00000 3.200000  3.300000  5.500000

# 1926  37.40000  5.600000
55.10000  19.60000  197.8000 64.00000 3.300000  3.300000  7.000000

# 1927  37.90000  4.200000
56.20000  19.80000  203.4000 64.40000 3.600000  4.000000  6.700000

# 1928  39.20000  3.000000
57.30000  21.10000  207.6000 64.50000 3.700000  4.200000  4.200000

# 1929  41.30000  5.100000
57.80000  21.70000  210.6000 67.00000 4.000000  4.100000  4.000000

# 1930  37.90000  1.000000
55.00000  15.60000  215.7000 61.20000 4.200000  5.200000  7.700000

# 1931  34.50000 -3.400000
50.90000  11.40000  216.7000 53.40000 4.800000  5.900000  7.500000

# 1932  29.00000 -6.200000
45.60000  7.000000  213.3000 44.30000 5.300000  4.900000  8.300000

# 1933  28.50000 -5.100000
46.50000  11.20000  207.1000 45.10000 5.600000  3.700000  5.400000

# 1934  30.60000 -3.000000
48.70000  12.30000  202.0000 49.70000 6.000000  4.000000  6.800000

# 1935  33.20000 -1.300000
51.30000  14.00000  199.0000 54.40000 6.100000  4.400000  7.200000

<!-- 第 54 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1936  36.80000  2.100000
57.70000  17.60000  197.7000 62.70000 7.400000  2.900000  8.300000

# 1937  41.00000  2.000000
58.70000  17.30000  199.8000 65.00000 6.700000  4.300000  6.700000

# 1938  38.20000 -1.900000
57.50000  15.30000  201.8000 60.90000 7.700000  5.300000  7.400000

# 1939  41.60000  1.300000
61.60000  19.00000  199.9000 69.50000 7.800000  6.600000  8.900000

# 1940  45.00000  3.300000
65.00000  21.10000  201.2000 75.70000 8.000000  7.400000  9.600000

# 1941  53.30000  4.900000
69.70000  23.50000  204.5000 88.40000 8.500000  13.80000  11.60000

解：

#### （1）从单个变量看，内生变量分别为：收入Y，消费C、投资I、私人工资WP、利润Π、
资本存量K；
外生变量分别为：政府工资WG、政府支出G、税收T 与时间t；
先决变量分别为：Yt-1，Πt-1，Kt-1，WG，G，T，t，WGt-1，Tt-1。由于模型中有两个组合变
量：WPt+WG 与Yt+Tt-WGt，它们都是内生变量与外生变量的组合，因此 在模型中也是内生变
量。但Yt－1+Tt－1－WGt－1也是先决变量。

#### （2）结构参数矩阵包括了16 个变量，其中6 个为内生变量，9 个为先决变量和一个常
数项：

#### C , I ,W ,Y ,  , K ,Y , , K ,W ,T ,W ,G ,T ,t,常数项
t t pt t t t t 1 t1 t1 Gt1 t1 Gt t t
对于消费方程，其中未包含的变量在其他方程中对应系数所组成的矩阵为：

#### I Y K K W G T T Y t
t t t t1 Gt1 t t t1 t1

#### 1 0 0   0 0 0 0 0 0 
3

####  

#### 0  0 0  0    

####  1 2 1 1 1 1 

#### (B  )  1 1 0 0 0 1 1 0 0 0 

#### 0 0  

#### 0 1 0 0 0 0 0 0 0 0

####  

####   

####  1 0 1 1 0 0 0 0 0 0 
可知该矩阵的秩为5，与整个模型系统的内生变量g-1=5 相等，从而该方程可以识别；又
k-ki=10-3=7>gi-1=3-1=2，所以消费方程为过度识别。
对于投资方程，其中未包含的变量在其他方程中对应系数所组成的矩阵为：

#### C W Y K W W G T T Y t
t pt t t Gt1 Gt t t t1 t1

#### 1  0 0 0  0 0 0 0 0 

# 3 3

####  

#### 0 0  0   0    

####  1 2 1 1 2 2 3 

#### (B  )  1 0 1 0 0 0 1 1 0 0 0 

#### 0 0  

#### 0 1 1 0 0 1 0 0 0 0 0

####  

####  

#### 0 0 0 1 0 0 0 0 0 0 0 

<!-- 第 55 页 -->
计量经济软件Eviews 上机指导及演示示例

可知该矩阵的秩为5，与整个模型系统的内生变量g-1=5 相等，从而该方程可以识别；又
k-ki=10-3=7>gi-1=2-1=1，所以投资方程为过度识别。
对于工资方程，其中未包含的变量在其他方程中对应系数所组成的矩阵为：

#### C I  K  K G
t t t t t1 t1 t1

#### 1 0  0  0 0 

# 1 2

####  

#### 0 1   0     0

####  1 2 3 

#### (B  )  1 1 0 0 0 0 1

#### 0 0  

#### 0 0 1 0 0 0 0 

####    

#### 0 1 0 1 0 1 0 
可知该矩阵的秩为5，与整个模型系统的内生变量g-1=5 相等，从而该方程可以识别；又
k-ki=10-7=3>gi-1=2-1=1，所以工资方程为过度识别。
其他方程不需要识别。整个联立方程是可以识别的。

#### （3）消费、投资、工资方程的OLS 估计结果如下：
消费
Dependent Variable: CT
Method: Least Squares
Date: 10/28/05   Time: 23:20
Sample(adjusted): 1921 1941
Included observations: 21 after adjusting endpoints
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  16.23660 1.302698 12.46382 0.0000
PI  0.192934 0.091210 2.115273 0.0495
PI(-1)  0.089885 0.090648 0.991582 0.3353
WP+WG  0.796219 0.039944 19.93342 0.0000
R-squared  0.981008    Mean dependent var 53.99524
Adjusted R-squared  0.977657    S.D. dependent var 6.860866
S.E. of regression  1.025540    Akaike info  3.057959
criterion
Sum squared resid  17.87945    Schwarz criterion  3.256916
Log likelihood  -28.10857    F-statistic  292.7076
Durbin-Watson stat  1.367474    Prob(F-statistic)  0.000000

投资
Dependent Variable: I
Method: Least Squares
Date: 10/28/05   Time: 23:22
Sample(adjusted): 1921 1941
Included observations: 21 after adjusting endpoints
Variable  Coefficien Std. Error t-Statistic Prob.
t

<!-- 第 56 页 -->
计量经济软件Eviews 上机指导及演示示例

C  10.12579 5.465547 1.852658 0.0814
PI  0.479636 0.097115 4.938864 0.0001
PI(-1)  0.333039 0.100859 3.302015 0.0042
KT  -0.111795 0.026728 -4.182749 0.0006
R-squared  0.931348    Mean dependent var 1.266667
Adjusted R-squared  0.919233    S.D. dependent var 3.551948
S.E. of regression  1.009447    Akaike info  3.026325
criterion
Sum squared resid  17.32270    Schwarz criterion  3.225281
Log likelihood  -27.77641    F-statistic  76.87537
Durbin-Watson stat  1.810184    Prob(F-statistic)  0.000000

工资
Dependent Variable: WP
Method: Least Squares
Date: 10/28/05   Time: 23:27
Sample(adjusted): 1921 1941
Included observations: 21 after adjusting endpoints
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  -1.219803 2.594698 -0.470114 0.6442
Y+T-WG  0.465920 0.068718 6.780182 0.0000
Y(-1)+T(-1)-WG(-1)  0.151552 0.077766 1.948827 0.0680
TT  -0.031620 0.215348 -0.146830 0.8850
R-squared  0.939443    Mean dependent var 36.36190
Adjusted R-squared  0.928756    S.D. dependent var 6.304401
S.E. of regression  1.682744    Akaike info  4.048371
criterion
Sum squared resid  48.13764    Schwarz criterion  4.247328
Log likelihood  -38.50790    F-statistic  87.90849
Durbin-Watson stat  0.816530    Prob(F-statistic)  0.000000

估计模型中出现的内生解释变量的简化式，即估计所有内生解释变量关于所有先决变
量的函数。
模型中出现的内生解释变量为利润PI,私人工资与政府工资的组合WP+WG，国民收入组
合Y+T-WG,这时，先决变量可看成P(-1),KT,T,t,以及组合性先决变量Y(-1)+T(-1)-WG(-1)。
上述三个内生解释变量与这里指出的先决变量的OLS 回归估计结果如下：
Dependent Variable: PI
Method: Least Squares
Date: 10/28/05   Time: 23:44
Sample(adjusted): 1921 1941

<!-- 第 57 页 -->
计量经济软件Eviews 上机指导及演示示例

Included observations: 21 after adjusting endpoints
Variable  Coefficien Std. Error t-Statistic Prob.
t
C  37.67528 11.39995 3.304863 0.0042
PI(-1)  0.500961 0.254405 1.969150 0.0655
KT  -0.208531 0.067921 -3.070193 0.0069
Y(-1)+T(-1)-WG(-1)  0.215183 0.130931 1.643483 0.1186
R-squared  0.738262    Mean dependent var 16.89048
Adjusted R-squared  0.692073    S.D. dependent var 4.220178
S.E. of regression  2.341825    Akaike info  4.709381
criterion
Sum squared resid  93.23046    Schwarz criterion  4.908338
Log likelihood  -45.44851    F-statistic  15.98351
Durbin-Watson stat  1.671408    Prob(F-statistic)  0.000034

### 第五部分  综合练习

#### 计量经济学综合练习一

下表是我国1978－1997 年的财政收入Y 和国民生产总值X 的数据资料，试根据资料完
成下列问题：

# 1、 建立财政收入对国民生产总值的一元线性回归方程，并解释斜率系数的经济意义；

# 2、 对所建立的 回归方程进行检验；

# 3、 若1998 年国民生产总值为78017.8 亿元，求1998 年财政收入预测值及预测区间（α＝
0.05）。

obs  X Y

# 1978  3624.100 1132.260

# 1979  4038.200 1146.380

# 1980  4517.800 1159.930

# 1981  4860.300 1175.790

# 1982  5301.800 1212.330

# 1983  5957.400 1366.950

# 1984  7206.700 1642.860

# 1985  8989.100 2004.820

# 1986  10201.40 2122.010

# 1987  11954.50 2199.350

# 1988  14922.30 2357.240

# 1989  16917.80 2664.900

# 1990  18598.40 2937.100

<!-- 第 58 页 -->
计量经济软件Eviews 上机指导及演示示例

# 1991  21662.50 3149.480

# 1992  26651.90 3483.370

# 1993  34560.50 4348.950

# 1994  46670.00 5218.100

# 1995  57494.90 6242.200

# 1996  66850.50 7407.990

# 1997  73452.50 8651.140

#### 计量经济学综合练习二

下表给出某国铜工业的有关数据。
obs  CT  G  I  L  H  A
1951  21.89000  330.2000   45.10000   220.4000   1491.000  19.00000
1952  22.29000  347.2000   50.90000   259.5000   1504.000  19.41000
1953  19.63000  366.1000   53.30000   256.3000   1438.000     20.9300
1954  22.85000  366.3000   53.60000   249.3000   1551.000  21.78000
1955  33.77000  399.3000   54.60000   352.3000   1646.000  23.68000
1956  39.18000  420.7000   61.10000   329.1000   1349.000  26.01000
1957  30.58000  442.0000   61.90000   219.6000   1224.000  27.52000
1958  26.30000  447.0000   57.90000   234.8000   1382.000  26.89000
1959  30.70000  483.0000   64.80000   237.4000   1553.700  26.85000
1960  32.10000  506.0000   66.20000   245.8000   1296.100  27.23000
1961  30.00000  523.3000   66.70000   229.2000   1365.000  25.46000
1962  30.80000  563.8000   72.20000   233.9000   1492.500  23.88000
1963  30.80000  594.7000   76.50000   234.2000   1634.900  22.62000
1964  32.60000  635.7000   81.70000   347.0000   1561.000  23.72000
1965  35.40000  688.1000   89.80000   468.1000   1509.700  24.50000
1966  36.60000  753.0000   97.80000   555.0000   1195.800  24.50000
1967  38.60000  796.3000   100.0000   418.0000   1321.900  24.98000
1968  42.20000  868.5000   106.3000   525.2000   1545.400  25.58000
1969  47.90000  935.5000   111.1000   620.7000   1499.500  27.18000
1970  58.20000  982.4000   107.8000   588.6000   1469.000  28.72000
1971  52.00000  1063.400   109.6000   444.4000   2084.500  29.00000
1972  51.20000  1171.100   119.7000   427.8000   2378.500  26.67000
1973  59.50000  1306.600   129.8000   727.1000   2057.500  25.33000
1974  77.30000  1412.900   129.3000   877.6000   1352.500  34.06000
1975  64.20000  1528.800   117.8000   556.6000   1171.400  39.79000
1976  69.60000  1700.100   129.8000   780.6000   1547.600  44.49000
1977  66.80000  1887.200   137.1000   750.7000   1989.800  51.23000
1978  66.50000  2127.600   145.2000   709.8000   2023.300  54.42000
1979  98.30000  2628.800   152.5000   935.7000   1759.200  61.01000
1980  101.4000  2633.100   147.1000   940.9000   1298.500  70.87000

# 1、根据这些数据，估计以下回归模型：

<!-- 第 59 页 -->
计量经济软件Eviews 上机指导及演示示例

#### ln C    ln I   ln L   ln H   ln A  
t 1 t 2 t 3 t 4 t t
并解释所得结果；
其中，CT 为12 个月的平均国内铜价（每磅美分）
G 国民总产值（10 亿美元）
I 为12 个月的平均工业生产指数
L 为12 个月的平均伦敦金属交易所铜价（20 英镑）
H 为每年新房动工数（千单位）
A 为12 个月的平均铝价（每磅美分）

# 2、求出上述回归的残差，你能对这些残差中是否有自回归做些什么解释？

# 3、求DW 统计量，并对数据中可能出现的自相关性质做出评价；

# 4、试用广义差分回归估计方法修正自相关；

# 5、试用Cochrane-Orcutt 迭代法估计模型；

# 6、对4、5 所用方法作出评价。

#### 综合练习三（关于异方差性）

#### 习题集P42 页第7 题。

#### 综合练习四（关于多重共线性）

#### 习题集P60 页第3 题。
