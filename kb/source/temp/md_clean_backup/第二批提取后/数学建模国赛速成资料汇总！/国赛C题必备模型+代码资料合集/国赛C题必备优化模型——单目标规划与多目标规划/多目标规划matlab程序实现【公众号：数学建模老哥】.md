优化与决策
——多目标线性规划的若干解法及MATLAB实现
摘要：求解多目标线性规划的基本思想大都是将多目标问题转化为单目标规划，本文介绍了理想点法、线性加权和法、最大最小法、目标规划法，然后给出多目标线性规划的模糊数学解法，最后举例进行说明，并用Matlab软件加以实现。
关键词：多目标线性规划 Matlab 模糊数学。
注：本文仅供参考，如有疑问，还望指正。
一．引言
多目标线性规划是多目标最优化理论的重要组成部分，由于多个目标之间的矛盾性和不可公度性,要求使所有目标均达到最优解是不可能的,因此多目标规划问题往往只是求其有效解(非劣解)。目前求解多目标线性规划问题有效解的方法,有理想点法、线性加权和法、最大最小法、目标规划法。本文也给出多目标线性规划的模糊数学解法。
二．多目标线性规划模型
　   多目标线性规划有着两个和两个以上的目标函数,且目标函数和约束条件全是线性函数,其数学模型表示为：
 EMBED Equation.DSMT4               （1）
约束条件为：
       EMBED Equation.DSMT4               （2）
若（1）式中只有一个 EMBED Equation.DSMT4  ，则该问题为典型的单目标线性规划。我们记: EMBED Equation.DSMT4  , EMBED Equation.DSMT4  , EMBED Equation.DSMT4  , EMBED Equation.DSMT4  ， EMBED Equation.DSMT4  .
则上述多目标线性规划可用矩阵形式表示为:
 EMBED Equation.DSMT4
   约束条件： EMBED Equation.DSMT4                              （3）
三．MATLAB优化工具箱常用函数 EMBED Equation.DSMT4
在MATLAB软件中，有几个专门求解最优化问题的函数，如求线性规划问题的linprog、求有约束非线性函数的fmincon、求最大最小化问题的fminimax、求多目标达到问题的fgoalattain等,它们的调用形式分别为：
①.[x,fval]=linprog(f,A,b,Aeq,beq,lb,ub)
f为目标函数系数,A,b为不等式约束的系数, Aeq,beq为等式约束系数, lb,ub为x的下限和上限, fval求解的x所对应的值。
算法原理：单纯形法的改进方法投影法。
②.[x,fval ]=fmincon(fun,x0,A,b,Aeq,beq,lb,ub）
fun为目标函数的M函数, x0为初值,A,b为不等式约束的系数, Aeq,beq为等式约束系数, lb,ub为x的下限和上限, fval求解的x所对应的值。
算法原理：基于K-T（Kuhn-Tucker）方程解的方法。
③.[x,fval ]=fminimax(fun,x0,A,b,Aeq,beq,lb,ub)
fun为目标函数的M函数, x0为初值,A,b为不等式约束的系数, Aeq,beq为等式约束系数, lb,ub为x的下限和上限, fval求解的x所对应的值。
算法原理：序列二次规划法。
④.[x,fval ]=fgoalattain(fun,x0,goal,weight,A,b,Aeq,beq,lb,ub)
fun为目标函数的M函数, x0为初值,goal变量为目标函数希望达到的向量值, wight 参数指定目标函数间的权重,A,b为不等式约束的系数, Aeq,beq为等式约束系数, lb,ub为x的下限和上限, fval求解的x所对应的值。
算法原理：目标达到法。

四．多目标线性规划的求解方法及MATLAB实现
4.1理想点法
在（3）中，先求解 EMBED Equation.DSMT4  个单目标问题： EMBED Equation.DSMT4  ，设其最优值为 EMBED Equation.DSMT4  ，称 EMBED Equation.DSMT4  为值域中的一个理想点，因为一般很难达到。于是，在期望的某种度量之下，寻求距离 EMBED Equation.DSMT4  最近的 EMBED Equation.DSMT4  作为近似值。一种最直接的方法是最短距离理想点法，构造评价函数
 EMBED Equation.DSMT4  ，
然后极小化 EMBED Equation.DSMT4  ，即求解
 EMBED Equation.DSMT4  ，
并将它的最优解 EMBED Equation.DSMT4  作为（3）在这种意义下的“最优解”。
例1：利用理想点法求解
 EMBED Equation.DSMT4
解：先分别对单目标求解：
①求解 EMBED Equation.DSMT4  最优解的MATLAB程序为
>> f=[3;-2]; A=[2,3;2,1]; b=[18;10]; lb=[0;0];
>> [x,fval]=linprog(f,A,b,[],[],lb)
结果输出为：x = 0.0000   6.0000
fval = -12.0000
即最优解为12.
②求解 EMBED Equation.DSMT4  最优解的MATLAB程序为
>> f=[-4;-3]; A=[2,3;2,1]; b=[18;10]; lb=[0;0];
>> [x,fval]=linprog(f,A,b,[],[],lb)
结果输出为：x =3.0000  4.0000
fval =-24.0000
即最优解为24.
于是得到理想点：（12，24）.
然后求如下模型的最优解
 EMBED Equation.DSMT4
MATLAB程序如下：
>> A=[2,3;2,1]; b=[18;10]; x0=[1;1]; lb=[0;0];
>> x=fmincon('((-3*x(1)+2*x(2)-12)^2+(4*x(1)+3*x(2)-24)^2)^(1/2)',x0,A,b,[],[],lb,[])
结果输出为：x = 0.5268  5.6488
则对应的目标值分别为 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  .
4.2线性加权和法
在具有多个指标的问题中，人们总希望对那些相对重要的指标给予较大的权系数，因而将多目标向量问题转化为所有目标的加权求和的标量问题，基于这个现实，构造如下评价函数，即
 EMBED Equation.DSMT4
将它的最优解 EMBED Equation.DSMT4  作为（3）在线性加权和意义下的“最优解”。（ EMBED Equation.DSMT4  为加权因子，其选取的方法很多，有专家打分法、容限法和加权因子分解法等）.

例2：对例1进行线性加权和法求解。（权系数分别取 EMBED Equation.DSMT4  ， EMBED Equation.DSMT4  ）
解：构造如下评价函数，即求如下模型的最优解。
 EMBED Equation.DSMT4
MATLAB程序如下：
>> f=[-0.5;-2.5; A=[2,3;2,1]; b=[18;10]; lb=[0;0];
>> x=linprog(f,A,b,[],[],lb)
结果输出为：x =0.0000  6.0000
则对应的目标值分别为 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  .
4.3最大最小法
在决策的时候，采取保守策略是稳妥的，即在最坏的情况下，寻求最好的结果，按照此想法，可以构造如下评价函数，即
 EMBED Equation.DSMT4
然后求解：                    EMBED Equation.DSMT4
并将它的最优解 EMBED Equation.DSMT4  作为（3）在最大最小意义下的“最优解”。
例3：对例1进行最大最小法求解：
解：MATLAB程序如下，首先编写目标函数的M文件：
function f=myfun12(x)
f(1)=3*x(1)-2*x(2);
f(2)=-4*x(1)-3*x(2);
>> x0=[1;1];A=[2,3;2,1];b=[18;10];lb=zeros(2,1);
>> [x,fval]=fminimax('myfun12',x0,A,b,[],[],lb,[])
结果输出为：x =0.0000   6.0000
fval = -12    -18
则对应的目标值分别为 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  .

4.4目标规划法
    EMBED Equation.DSMT4                    （4）
并把原多目标线性规划（3） EMBED Equation.DSMT4  称为和目标规划（4）相对应的多目标线性规划。
为了用数量来描述（4），我们在目标空间 EMBED Equation.DSMT4  中引进点 EMBED Equation.DSMT4  之间的某种“距离”
 EMBED Equation.DSMT4
这样（4）便可以用单目标 EMBED Equation.DSMT4  来描述了。

例4：对例1对进行目标规划法求解：
解：MATLAB程序如下，首先编写目标函数的M文件：
function f=myfun3(x)
f(1)=3*x(1)-2*x(2);
f(2)=-4*x(1)-3*x(2);
>> goal=[18,10]; weight=[18,10]; x0=[1,1]; A=[2,3;2,1]; b=[18,10]; lb=zeros(2,1);
>> [x,fval]=fgoalattain('myfun3',x0,goal,weight,A,b,[],[],lb,[])
结果输出为：x =    0.0000    6.0000
fval =   -12      -18
则对应的目标值分别为 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  .

4.5模糊数学求解方法
　  由于多目标线性规划的目标函数不止一个,要想求得某一个点作 EMBED Equation.DSMT4  ,使得所有的目标函数都达到各自的最大值,这样的绝对最优解通常是不存在的。因此,在具体求解时,需要采取折衷的方案,使各目标函数都尽可能的大。模糊数学规划方法可对其各目标函数进行模糊化处理,将多目标问题转化为单目标,从而求该问题的模糊最优解。
    具体的方法为：先求在约束条件： EMBED Equation.DSMT4   下各个单目标 EMBED Equation.DSMT4  的最大值 EMBED Equation.DSMT4  和最小值 EMBED Equation.DSMT4  ，伸缩因子为 EMBED Equation.DSMT4
得到 EMBED Equation.DSMT4                （5）
式（5）是一个简单的单目标线性规划问题。
最后求得模糊最优解为： EMBED Equation.DSMT4  .
利用(5)式来求解的关键是对伸缩指标的 EMBED Equation.DSMT4  确定, EMBED Equation.DSMT4  是我们选择的一些常数,由于在多目标线性规划中,各子目标难以同时达到最大值 EMBED Equation.DSMT4  ，但是可以确定的是各子目标的取值范围，它满足： EMBED Equation.DSMT4  ，所以，伸缩因子为 EMBED Equation.DSMT4  可以按如下取值： EMBED Equation.DSMT4  .
例5：对例1进行模糊数学方法求解：
解：①分别求得 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  在约束条件下的最大值为： EMBED Equation.DSMT4  .
②分别求得 EMBED Equation.DSMT4  , EMBED Equation.DSMT4  在约束条件下的最小值为： EMBED Equation.DSMT4  .
伸缩因子为 EMBED Equation.DSMT4
然后求如下模型的最优解：
 EMBED Equation.DSMT4
MATLAB程序如下：
>>f=[0;0;-1]; A=[3,-2,27;-4,-3,24;2,3,0;2,1,0]; b=[15;0;18;10]; lb=[0;0;0]
>> [x,fval]=linprog(f,A,b,[],[],lb)
结果输出为：x = 1.0253   5.3165  0.8354
fval =-0.8354
于是原多目标规划问题的模糊最优值为 EMBED Equation.DSMT4  .

五．结论
多目线性标规划是优化问题的一种,由于其存在多个目标,要求各目标同时取得较优的值,使得求解的方法与过程都相对复杂. 通过将目标函数进行模糊化处理,可将多目标问题转化为单目标,借助工具软件,从而达到较易求解的目标。
