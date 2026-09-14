<!-- 第 1 页 -->

#### ·80 · 计算机应用研究 2001 年

# 用MATLAB 实现遗传算法程序3

#### 刘国华, 包宏, 李文超

#### (北京科技大学, 北京100083)
摘要: 简要阐述了遗传算法的基本原理,探讨了在MATLAB 环境中实现遗传算法各算子的编程方法,
并以一个简单的实例说明所编程序在函数全局寻优中的应用。
关键词: 遗传算法( GA) ; MATLAB
中图分类号: TP301. 6       文献标识码: A       文章编号: 100123695(2001) 0820080203

## A Genetic Algorithm in MATLAB
LIU Guo2hua , BAO Hong , LI Wen2chao
( Beijing University of Science & Technology , Beijing 100083 , China)
Abstract : The principle of genetic algorithm has been presented and its realization in MATLAB has been discussed. A function opti2
mization problem has been given to demonstrate the global optimization functionality of the MATLAB program.
Key words : Genetic algorithm( GA) ;MATLAB

### 1   遗传算法概述遗传算法的基本步骤[3]如下:
遗传算法( Genetic Algorithm , GA) 是借鉴生物界自 1) 在一定编码方案下,随机产生一个初始种群;
然选择和群体进化机制形成的一种全局寻优算法。与 2) 用相应的解码方法,将编码后的个体转换成问
传统的优化算法相比,遗传算法具有如下优点[1] :1) 不题空间的决策变量,并求得个体的适应值;
是从单个点,而是从多个点构成的群体开始搜索;2) 在 3) 按照个体适应值的大小,从种群中选出适应值
搜索最优解过程中,只需要由目标函数值转换得来的较大的一些个体构成交配池;
适应值信息,而不需要导数等其它辅助信息;3) 搜索过 4) 由交叉和变异这两个遗传算子对交配池中的个
程不易陷入局部最优点。目前,该算法已渗透到许多体进行操作,并形成新一代的种群;
领域,并成为解决各领域复杂问题的有力工具[2] 。 5) 反复执行步骤2～4 ,直至满足收敛判据为止。
在遗传算法中,将问题空间中的决策变量通过一使用遗传算法需要决定的运行参数有:编码串长
度、种群大小、交叉和变异概率[4] 。编码串长度由优化
定编码方法表示成遗传空间的一个个体,它是一个基
因型串结构数据;同时,将目标函数值转换成适应值, 问题所要求的求解精度决定。种群大小表示种群中所
它用来评价个体的优劣,并作为遗传操作的依据。遗含个体的数量,种群较小时,可提高遗传算法的运算速
传操作包括三个算子:选择、交叉和变异。选择用来实度,但却降低了群体的多样性,可能找不出最优解;种群
施适者生存的原则,即把当前群体中的个体按与适应较大时,又会增加计算量,使遗传算法的运行效率降低。
值成比例的概率复制到新的群体中,构成交配池(当前一般取种群数目为20～100。交叉概率控制着交叉操作
代与下一代之间的中间群体) 。选择算子的作用效果的频率,由于交叉操作是遗传算法中产生新个体的主要
是提高了群体的平均适应值。由于选择算子没有产生方法,所以交叉概率通常应取较大值;但若过大的话,又
新个体,所以群体中最好个体的适应值不会因选择操可能破坏群体的优良模式。一般取0. 4～0. 99。变异概
作而有所改进。交叉算子可以产生新的个体,它首先率也是影响新个体产生的一个因素,变异概率小,产生
使从交配池中的个体随机配对,然后将两两配对的个新个体少;变异概率太大,又会使遗传算法变成随机搜
体按某种方式相互交换部分基因。变异是对个体的某索。一般取变异概率为0. 0001～0. 1。遗传算法常采用
一个或某一些基因值按某一较小概率进行改变。从产的收敛判据有:规定遗传代数;连续几次得到的最优个
体的适应值没有变化或变化很小等[5] 。
生新个体的能力方面来说,交叉算子是产生新个体的

### 主要方法,它决定了遗传算法的全局搜索能力;而变异 2   用MATLAB 实现遗传算法
算子只是产生新个体的辅助方法,但也必不可少,因为 MATLAB 是Matwork 公司的产品,是一个功能强大
它决定了遗传算法的局部搜索能力。交叉和变异相配的数学软件,其优秀的数值计算能力使其在工业界和
合,共同完成对搜索空间的全局和局部搜索。学术界的使用率都非常高。MATLAB 还十分便于使用,
它以直观、简洁并符合人们思维习惯的代码给用户提
供了一个非常友好的开发环境[6] 。利用MATLAB 处理
收稿日期: 2000212226 矩阵运算的强大功能来编写遗传算法程序有着巨大的
基金项目: 国家自然科学基金资助项目(59874006 ; 优势。
59872002)

<!-- 第 2 页 -->

#### 第8 期刘国华等:用MATLAB 实现遗传算法程序 ·81 ·
size ,1) 3 r ) + 1 ;

#### 211   编码
evo2gen = evo2gen(selected , :) ;
遗传算法不对优化问题的实际决策变量进行操在该算子中,采用了最优保存策略和比例选择法
作,所以应用遗传算法首要的问题是通过编码将决策相结合的思路,即首先找出当前群体中适应值最高和
变量表示成串结构数据。本文中我们采用最常用的二最低的个体,将最佳个体best2indiv 保留并用其替换掉
进制编码方案,即用二进制数构成的符号串来表示一最差个体。为保证当前最佳个体不被交叉、变异操作
个个体,用下面的encoding 函数来实现编码并产生初始所被坏,允许其不参与交叉和变异而直接进入下一代。
种群: 然后将剩下的个体evo2gen 按比例选择法进行操作。所
function [bin2gen ,bits] =encoding(min2var ,max2var ,scale2var ,popsize) 谓比例选择法,也叫赌轮算法[4] ,是指个体被选中的概
bits = ceil (log2( (max2var2min2var) . / scale2var) ) ;
率与该个体的适应值大小成正比。将这两种方法相结
bin2gen = randint (popsize ,sum(bits) ) ;
合的目的是:在遗传操作中,不仅能不断提高群体的平
在上面的代码中,首先根据各决策变量的下界
均适应值,而且能保证最佳个体的适应值不减小。
(min2var) 、上界(max2var) 及其搜索精度scale2var 来确定

#### 214   交叉
表示各决策变量的二进制串的长度bits ,然后随机产生
一个种群大小为popsize 的初始种群bin2gen。编码后的下面采用单点交叉的方法来实现交叉算子,即按
实际搜索精度为scale2dec = (max2var2min2var) / (2^bits2 选择概率PC 在两两配对的个体编码串cpairs 中随机设
1) ,该精度会在解码时用到。置一个交叉点cpoints ,然后在该点相互交换两个配对个
体的部分基因,从而形成两个新的个体。交叉算子的

#### 212   解码
程序如下:
编码后的个体构成的种群bin2gen 必须经过解码, function new2gen = crossover(old2gen ,pc)
以转换成原问题空间的决策变量构成的种群var2gen ,   [nouse ,mating] = sort (rand(size(old2gen ,1) ,1) ) ;
mat2gen = old2gen(mating , :) ;
方能计算相应的适应值。我们用下面的代码实现。
pairs = size(mat2gen ,1) / 2 ;
function [ var2gen ,fitness] = decoding (funname ,bin2gen ,bits ,min2
bits = size(mat2gen ,2) ;
var ,max2var)
cpairs = rand(pairs ,1) < pc ;
num2var = length(bits) ;
cpoints = randint (pairs ,1 ,[1 ,bits]) ;
popsize = size(bin2gen ,1) ;   cpoints = cpairs. 3 cpoints ;
scale2dec = (max2var2min2var) . / (2.^bits21) ;
for i = 1 :pairs
bits = cumsum(bits) ; = [mat2gen([2 3 i21   2 3 i ] ,1 :
new2gen([2 3i21   2 3i ] , :)
bits = [0 bits] ;
cpoints(i) ) mat2gen([2 3i   2 3i21] ,cpoints(i) + 1 :bits) ] ;
for i = 1 :num2var
bin2var{i} = bin2gen( : ,bits(i) + 1 :bits(i + 1) ) ; end
var{i} = sum(ones(popsize ,1) 3 2.^(size(bin2var{i} ,2)21 :2 215   变异

# 1 :0) . 3 bin2var{i} ,2) . 3 scale2dec(i) + min2var(i) ;
end 对于二进制的基因串而言,变异操作就是按照变
var2gen = [var{1 , :} ] ; 异概率pm 随机选择变异点mpoints ,在变异点处将其位
for i = 1 :popsize
取反即可。变异算子的实现过程如下:
fitness(i) = eval ([funname ,’(var2gen(i , :) ) ’]) ;
end function new2gen = mutation (old2gen ,pm)
解码函数的关键在于先由二进制数求得对应的十   mpoints = find(rand(size(old2gen) ) < pm) ;
new2gen = old2gen ;
进制数D ,并根据下式求得实际决策变量值X:
new2gen(mpoints) = 12old2gen(mpoints) ;

### X = D ×scale2dec + min2var 3   应用实例

#### 213   选择上述程序已经考虑了多参数编码问题,可以用于
搜索多变量函数的最优解。为简单起见,下面仅以一
选择过程是利用解码后求得的各个体适应值大
小,淘汰一些较差的个体而选出一些比较优良的个体, 个单变量函数为例,来验证所编遗传算法程序的全局
寻优能力。设函数为:y = cos (5x)2sin(3x) + 10 ,x ∈[1
以进行下一步的交叉和变异操作。选择算子的程序如
下: 7] ,函数特性如图1 所示。
function [ evo2gen ,best2indiv ,max2fitness] = selection ( old2gen ,fit2
ness)
popsize = length(fitness) ;
[ max2fitness ,index1 ] = max (fitness) ; [ min2fitness ,index2 ] =
min(fitness) ;
best2indiv = old2gen(index1 , :) ;
index = [1 :popsize] ; index(index1) = 0 ; index(index2) = 0 ;
index = nonzeros(index) ;
evo2gen = old2gen(index , :) ;
evo2fitness = fitness(index , :) ;
evo2popsize = popsize22 ;
图1   函数特性示意图
ps = evo2fitness/ sum(evo2fitness) ;
pscum = cumsum(ps) ; 取种群大小popsize = 20 ,搜索精度scale2var = 0.0001 ,
r = rand(1 ,evo2popsize) ; 交叉概率pc = 0. 6 ,变异概率pm = 0. 1。图2 和图3 是
selected = sum( pscum 3 ones (1 ,evo2popsize) < ones (evo2pop2

<!-- 第 3 页 -->

#### ·82 · 计算机应用研究 2001 年

某一次运算遗传20 代后最佳个体的适应值增长情况种群中适应值最大的个体解码后的值为1. 1944 ,落在
和最佳个体的变化情况。函数的一个局部极值处。但是搜索并没有在此处停
滞,很快就跃到了另一个更大的极值点3. 7 附近。在该
点附近搜索多次后,我们发现连续几次得到的最优个
体的适应值变化很小,可以认为找到全局最大值,全局
最大值点为3. 7414 ,最大值为11. 9638。

### 4   结束语
我们用MATLAB 编写了遗传算法程序,并给出完
整代码,程序在MATLAB 5. 3 中调试通过。最后,通过
一个实例说明其在函数优化中的应用。
参考文献:
[1]   刘勇,康立山,陈毓屏. 非数值并行算法(第二册) ———遗
图2   最佳个体适应值的增长情况传算法[M]. 北京:科学出版社,1997.
[2]   席裕庚,柴天佑,恽为民. 遗传算法综述[J ]. 控制理论与
应用,1996 ,13 (6) : 6972708.
[3]   韩祯祥,文福拴. 模拟进化优化方法及其应用———遗传
算法[J ]. 计算机科学,1995 ,22 (2) : 47256.
[4]   周明,孙树栋. 遗传算法原理及其应用[M]. 北京:国防
工业出版社,1999.
[5]   梁吉业. 遗传算法应用中的一些共性问题研究[J ]. 计算
机应用研究,1999 ,16 (7) : 20221.
[6 ]   张宜华. 精通MATLAB 5[M]. 北京:清华大学出版社,
1999.
作者简介:
图3   最佳个体的变化情况
刘国华(19742) ,男,博士生,研究方向为人工智能及其在计算
由于采用了最优保存策略,所以在图2 中未看到
机辅助材料设计中的应用;包宏,副教授;李文超,教授,博导。
最佳个体适应值减少的现象。由图3 可见:在前三代

(上接第79 页) 的可保护性和维护性在性能上有很大的提高,但在应
END IF 用程序中也必要加上状态标志和缓冲,否则将使得其
Ids - datastore = CREATE datastore
性能适得其反。在应用中当大量客户端同时访问数据
Ids - datastore. dataobject =″d - emplist″
Ids - datastore. setTransobject (SQLCA) 库的情况下,可以通过组件事务服务器定义一个数据
RetrieveData 函数实现检索功能。其函数原形为: 库连接缓冲池,各客户端可以共享这个缓冲池,使得数
RetrieveDate(reference blob able - data) return Long
Long ll - rr 据库服务器所需管理和维护的连接数大大减少,从而
Ids - datastore. Retrieve()
提高系统的性能。
ll - rr = ids - datastore. GetFullState(ablb - data)
Txnsrv. Setcomplete() 参考文献:
Return ll - rr
UpdateDate 函数实现代码如下: [1]   温为民. PowerBuilder 7. 0 实例应用进阶[M]. 北京:机械
Long ll - rr 工业出版社122222531
If ids - datastore. SetChanges(ablb - data) = 1 then
[2]   PowerBuilder 6. 0 用户参考手册[M]. 北京:希望电子出版
ll - rr = ids - datastore. Update()
社134425001
end if
if ll-rr = 1 then [3]   郭迅华1Sybase 组件事务服务器Jaguar CTS[M]1 北京:电
txnsrv. Setcomplete()
子工业出版社120022451
else
txnsrv. SetAbort () [4 ]   McFall C . An Object Infrastrusture for Internet Middleware
end if IBM on Component Broker [ J ]. IEEE Internet Computing ,
return ll - rr

# 1998 ,422501
在组件关闭事件中必须回收存储过程资源并断开
连接。 [5]   Anne I. Jaguar CTS ,Jaguar CTS white paper [M]1Emery ville
DESTROY ids- datastore Sybase cop 1999.
DISCONNECT USING SQLCA ;
作者简介:

### 5   结束语
本例主要讲述的是基于组件事务服务器中数据库杨书凡(19752) ,女,湖南大学计算机系硕士生,助教,研究方向
的操作。由于组件三层/ 多层模式的结构特点对数据为分布式计算、网络技术。
