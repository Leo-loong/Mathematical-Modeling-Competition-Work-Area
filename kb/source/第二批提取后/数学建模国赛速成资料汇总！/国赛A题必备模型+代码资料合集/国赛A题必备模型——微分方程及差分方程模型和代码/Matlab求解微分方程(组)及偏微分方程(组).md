第四讲 Matlab求解微分方程（组）
理论介绍:Matlab求解微分方程（组）命令
求解实例：Matlab求解微分方程（组）实例
实际应用问题通过数学建模所归纳得到的方程，绝大多数都是微分方程，真正能得到代数方程的机会很少。另一方面，能够求解的微分方程也是十分有限的，特别是高阶方程和偏微分方程(组）。这就要求我们必须研究微分方程（组）的解法：解析解法和数值解法.
一．相关函数、命令及简介
1。在Matlab中，用大写字母D表示导数,Dy表示y关于自变量的一阶导数，D2y表示y关于自变量的二阶导数，依此类推。函数dsolve用来解决常微分方程（组）的求解问题，调用格式为：
X=dsolve（‘eqn1’,’eqn2'，…）
函数dsolve用来解符号常微分方程、方程组，如果没有初始条件，则求出通解，如果有初始条件,则求出特解.
注意，系统缺省的自变量为t
2.函数dsolve求解的是常微分方程的精确解法，也称为常微分方程的符号解。但是，有大量的常微分方程虽然从理论上讲,其解是存在的,但我们却无法求出其解析解，此时,我们需要寻求方程的数值解，在求常微分方程数值解方面，MATLAB具有丰富的函数，我们将其统称为solver，其一般格式为：
[T,Y]=solver(odefun，tspan,y0)
说明:（1）solver为命令ode45、ode23、ode113、ode15s、ode23s、ode23t、ode23tb、ode15i之一。
（2）odefun是显示微分方程 EMBED Equation.DSMT4 在积分区间tspan EMBED Equation.DSMT4 上从 EMBED Equation.DSMT4 到 EMBED Equation.DSMT4 用初始条件 EMBED Equation.DSMT4 求解。
(3)如果要获得微分方程问题在其他指定时间点 EMBED Equation.DSMT4 上的解，则令tspan EMBED Equation.DSMT4 (要求是单调的）。
(4)因为没有一种算法可以有效的解决所有的ODE问题，为此，Matlab提供了多种求解器solver，对于不同的ODE问题，采用不同的solver。
表1 Matlab中文本文件读写函数
求解器	ODE类型特点说明		ode45	非刚性单步算法：4、5阶Runge-Kutta方程;累计截断误差 EMBED Equation.DSMT4 	大部分场合的首选算法		ode23	非刚性单步算法：2、3阶Runge-Kutta方程;累计截断误差 EMBED Equation.DSMT4 	使用于精度较低的情形		ode113	非刚性多步法：Adams算法；高低精度可达 EMBED Equation.DSMT4 	计算时间比ode45短		ode23t	适度刚性采用梯形算法适度刚性情形		ode15s	刚性多步法：Gear’s反向数值微分；精度中等若ode45失效时，可尝试使用		ode23s	刚性单步法：2阶Rosebrock算法;低精度当精度较低时，计算时间比ode15s短		ode23tb	刚性梯形算法;低精度当精度较低时，计算时间比ode15s短说明：ode23、ode45是极其常用的用来求解非刚性的标准形式的一阶微分方程（组）的初值问题的解的Matlab常用程序,其中：
ode23采用龙格-库塔2阶算法,用3阶公式作误差估计来调节步长，具有低等的精度.
ode45则采用龙格—库塔4阶算法，用5阶公式作误差估计来调节步长，具有中等的精度.
3．在matlab命令窗口、程序或函数中创建局部函数时，可用内联函数inline，inline函数形式相当于编写M函数文件，但不需编写M-文件就可以描述出某种数学关系.调用inline函数，只能由一个matlab表达式组成，并且只能返回一个变量,不允许[u，v]这种向量形式.因而，任何要求逻辑运算或乘法运算以求得最终结果的场合，都不能应用inline函数,inline函数的一般形式为：
FunctionName=inline（‘函数内容'， ‘所有自变量列表’)
例如：（求解F（x)=x^2*cos(a*x）—b ,a，b是标量；x是向量 )在命令窗口输入:
Fofx=inline(‘x .^2＊cos（a*x)-b' , ‘x'，'a’,’b’）；
g= Fofx（[pi/3 pi/3。5],4，1)
系统输出为：g=—1.5483 —1.7259
注意：由于使用内联对象函数inline不需要另外建立m文件，所有使用比较方便，另外在使用ode45函数的时候,定义函数往往需要编辑一个m文件来单独定义，这样不便于管理文件，这里可以使用inline来定义函数。
二．实例介绍
1。几个可以直接用Matlab求微分方程精确解的实例
例1 求解微分方程 EMBED Equation.DSMT4
程序：syms x y; y=dsolve（‘Dy+2*x＊y=x＊exp(-x^2)’,’x’)
例2 求微分方程 EMBED Equation.DSMT4 在初始条件 EMBED Equation.DSMT4 下的特解并画出解函数的图形。
程序：syms x y; y=dsolve(‘x*Dy+y—exp（1)=0’,’y(1）=2*exp（1）'，’x’）；ezplot(y）
例 3 求解微分方程组 EMBED Equation.DSMT4 在初始条件 EMBED Equation.DSMT4 下的特解并画出解函数的图形.
程序：syms x y t
［x，y]=dsolve(’Dx+5＊x+y=exp(t）'，'Dy-x-3＊y=0','x（0）=1’,'y（0）=0'，'t’）
simple（x）；
simple(y)
ezplot(x,y，[0,1.3］）；axis auto
2。用ode23、ode45等求解非刚性标准形式的一阶微分方程（组）的初值问题的数值解（近似解）
例 4 求解微分方程初值问题 EMBED Equation.DSMT4 的数值解，求解范围为区间[0,0。5］.
程序：fun=inline(’-2＊y+2＊x^2+2＊x'，’x’，'y’);
[x,y］=ode23(fun,[0,0。5]，1);
plot(x，y，'o-’）
例 5 求解微分方程 EMBED Equation.DSMT4 的解，并画出解的图形。
分析：这是一个二阶非线性方程，我们可以通过变换，将二阶方程化为一阶方程组求解。令 EMBED Equation.DSMT4 ，则
 EMBED Equation.DSMT4
编写M—文件vdp。m
function fy=vdp(t，x)
fy=[x（2）；7＊(1—x(1）^2)*x（2)—x(1)];
end
在Matlab命令窗口编写程序
y0=［1；0］
［t，x］=ode45(@vdp，[0,40],y0);或［t,x]=ode45（'vdp’,［0,40］,y0）;
y=x（：，1);dy=x(:，2）;
plot(t,y,t,dy)
练习与思考：M—文件vdp.m改写成inline函数程序？
3.用Euler折线法求解
Euler折线法求解的基本思想是将微分方程初值问题
 EMBED Equation.DSMT4
化成一个代数(差分）方程,主要步骤是用差商 EMBED Equation.DSMT4 替代微商 EMBED Equation.DSMT4 ,于是
 EMBED Equation.DSMT4
记 EMBED Equation.DSMT4 从而 EMBED Equation.DSMT4 于是
 EMBED Equation.DSMT4
例 6 用Euler折线法求解微分方程初值问题
 EMBED Equation.DSMT4
的数值解（步长 EMBED Equation.DSMT4 取0。4），求解范围为区间［0，2]。
分析：本问题的差分方程为
 EMBED Equation.DSMT4
程序：〉〉 clear
>> f=sym（’y+2*x/y^2’)；
〉〉 a=0;
〉〉 b=2；
>> h=0.4；
>〉 n=(b—a）/h+1;
>> x=0；
>〉 y=1；
〉> szj=［x，y］；%数值解
>> for i=1:n—1
     y=y+h*subs（f，｛'x','y'｝,{x,y｝）；%subs，替换函数
     x=x+h；
     szj=［szj；x,y]；
 end
>>szj
>> plot（szj(：,1),szj（：，2））
说明：替换函数subs例如：输入subs(a+b,a,4）意思就是把a用4替换掉，返回 4+b,也可以替换多个变量，例如:subs(cos(a)+sin(b）,{a，b｝,[sym（'alpha')，2］）分别用字符alpha替换a和2替换b，返回 cos（alpha）+sin（2）
特别说明：本问题可进一步利用四阶Runge—Kutta法求解，Euler折线法实际上就是一阶Runge-Kutta法,Runge—Kutta法的迭代公式为
 EMBED Equation.DSMT4
相应的Matlab程序为：〉> clear
〉〉 f=sym（'y+2＊x/y^2’）;
>> a=0；
〉> b=2;
〉> h=0。4；
〉〉 n=(b-a)/h+1;
>> x=0;
〉〉 y=1;
>〉 szj=［x，y］;%数值解
〉> for i=1：n-1
     l1=subs（f, {’x’,’y’｝,{x,y｝）;替换函数
     l2=subs（f， {’x’，’y’｝，{x+h/2,y+l1*h/2});
     l3=subs（f，｛’x',’y’},｛x+h/2,y+l2＊h/2｝)；
     l4=subs（f, ｛’x’，’y'},｛x+h,y+l3*h｝);
     y=y+h*(l1+2*l2+2＊l3+l4)/6；
     x=x+h;
     szj=［szj；x，y］;
 end
〉>szj
>〉 plot（szj(:，1）,szj(：,2)）
练习与思考：(1）ode45求解问题并比较差异。
（2)利用Matlab求微分方程 EMBED Equation.DSMT4 的解.
(3）求解微分方程 EMBED Equation.DSMT4 的特解。
(4）利用Matlab求微分方程初值问题 EMBED Equation.DSMT4 的解。
提醒：尽可能多的考虑解法
三．微分方程转换为一阶显式微分方程组
    Matlab微分方程解算器只能求解标准形式的一阶显式微分方程（组）问题,因此在使用ODE解算器之前,我们需要做的第一步，也是最重要的一步就是借助状态变量将微分方程（组)化成Matlab可接受的标准形式。当然，如果ODEs由一个或多个高阶微分方程给出,则我们应先将它变换成一阶显式常微分方程组.下面我们以两个高阶微分方程组构成的ODEs为例介绍如何将它变换成一个一阶显式微分方程组.
Step 1 将微分方程的最高阶变量移到等式左边，其它移到右边，并按阶次从低到高排列.形式为：
 EMBED Equation.DSMT4
Step 2 为每一阶微分式选择状态变量，最高阶除外
 EMBED Equation.DSMT4
注意：ODEs中所有是因变量的最高阶次之和就是需要的状态变量的个数,最高阶的微分式不需要给它状态变量。
Step 3 根据选用的状态变量，写出所有状态变量的一阶微分表达式
 EMBED Equation.DSMT4
练习与思考：（1)求解微分方程组
 EMBED Equation.DSMT4
其中 EMBED Equation.DSMT4  EMBED Equation.DSMT4  EMBED Equation.DSMT4  EMBED Equation.DSMT4  EMBED Equation.DSMT4
 EMBED Equation.DSMT4  EMBED Equation.DSMT4  EMBED Equation.DSMT4
（2）求解隐式微分方程组
 EMBED Equation.DSMT4
提示：使用符号计算函数solve求 EMBED Equation.DSMT4 ，然后利用求解微分方程的方法
四．偏微分方程解法
Matlab提供了两种方法解决PDE问题，一是使用pdepe函数,它可以求解一般的PDEs,具有较大的通用性,但只支持命令形式调用；二是使用PDE工具箱，可以求解特殊PDE问题，PDEtoll有较大的局限性，比如只能求解二阶PDE问题，并且不能解决片微分方程组，但是它提供了GUI界面,从复杂的编程中解脱出来，同时还可以通过File-〉Save As直接生成M代码.
1。一般偏微分方程（组)的求解
(1）Matlab提供的pdepe函数，可以直接求解一般偏微分方程（组），它的调用格式为：sol=pdepe(m，@pdefun，@pdeic,＠pdebc，x,t）
＠pdefun是PDE的问题描述函数，它必须换成标准形式：
 EMBED Equation.DSMT4
这样,PDE就可以编写入口函数：[c,f，s]=pdefun(x，t,u,du),m,x，t对应于式中相关参数，du是u的一阶导数,由给定的输入变量可表示出c，f,s这三个函数。
＠pdebc是PDE的边界条件描述函数,它必须化为形式：
 EMBED Equation.DSMT4
于是边值条件可以编写函数描述为:[pa,qa,pb，qb]=pdebc(x,t,u,du）,其中a表示下边界，b表示上边界.
＠pdeic是PDE的初值条件，必须化为形式： EMBED Equation.DSMT4 ,故可以使用函数描述为:u0=pdeic（x）
sol是一个三维数组，sol（:,:,i)表示 EMBED Equation.DSMT4 的解,换句话说， EMBED Equation.DSMT4 对应x（i)和t(j)时的解为sol（i,j,k)，通过sol，我们可以使用pdeval函数直接计算某个点的函数值.
（2）实例说明
求解偏微分
 EMBED Equation.DSMT4
其中， EMBED Equation.DSMT4 且满足初始条件 EMBED Equation.DSMT4 及边界条件 EMBED Equation.DSMT4  EMBED Equation.DSMT4
解:（1）对照给出的偏微分方程和pdepe函数求解的标准形式，原方程改写为
 EMBED Equation.DSMT4
可见 EMBED Equation.DSMT4
%目标PDE函数
function [c,f，s]=pdefun(x，t，u,du）
c=[1;1］；
f=[0。024*du(1)；0。17*du（2）］；
temp=u（1）-u（2）；
s=[—1；1]。*(exp(5。73*temp)—exp(—11。46＊temp）)
end
（2)边界条件改写为：
下边界 EMBED Equation.DSMT4 上边界 EMBED Equation.DSMT4
%边界条件函数
function [pa,qa,pb,qb］=pdebc(xa,ua,xb，ub,t）
pa=［0;ua(2)］;
qa=[1;0］;
pb=[ub(1)—1;0];
qb=[0;1］；
end
（3）初值条件改写为： EMBED Equation.DSMT4
％初值条件函数
function u0=pdeic(x）
u0=[1；0］;
end
（4）编写主调函数
clc
x=0：0.05：1；
t=0:0.05：2;
m=0;
sol=pdepe（m,＠pdefun，＠pdeic,@pdebc,x,t）；
subplot(2,1，1)  surf(x,t，sol（：,:，1））
subplot(2，1，2)  surf(x，t,sol（:，:，2））
练习与思考： This example illustrates the straightforward formulation， computation, and plotting of the solution of a single PDE.
 EMBED Equation.DSMT4
This equation holds on an interval  EMBED Equation.DSMT4  for times  EMBED Equation.DSMT4 . The PDE satisfies the initial condition EMBED Equation.DSMT4  and boundary conditions
 EMBED Equation.DSMT4
2.PDEtool求解偏微分方程
(1）PDEtool（GUI）求解偏微分方程的一般步骤
在Matlab命令窗口输入pdetool，回车，PDE工具箱的图形用户界面（GUI）系统就启动了.从定义一个偏微分方程问题到完成解偏微分方程的定解,整个过程大致可以分为六个阶段
Step 1 “Draw模式”绘制平面有界区域 EMBED Equation.DSMT4 ，通过公式把Matlab系统提供的实体模型：矩形、圆、椭圆和多边形,组合起来,生成需要的平面区域.
Step 2 “Boundary模式”定义边界，声明不同边界段的边界条件.
Step 3 “PDE模式”定义偏微分方程，确定方程类型和方程系数c,a,f,d，根据具体情况,还可以在不同子区域声明不同系数。
Step 4 “Mesh模式”网格化区域 EMBED Equation.DSMT4 ，可以控制自动生成网格的参数，对生成的网格进行多次细化,使网格分割更细更合理.
Step 5 “Solve模式"解偏微分方程,对于椭圆型方程可以激活并控制非线性自适应解题器来处理非线性方程；对于抛物线型方程和双曲型方程，设置初始边界条件后可以求出给定时刻t的解；对于特征值问题,可以求出给定区间上的特征值.求解完成后,可以返回到Step 4，对网格进一步细化,进行再次求解.
Step 6 “View模式"计算结果的可视化,可以通过设置系统提供的对话框，显示所求的解的表面图、网格图、等高线图和箭头梯形图.对于抛物线型和双曲线型问题的解还可以进行动画演示.
(2)实例说明用法
求解一个正方形区域上的特征值问题：
 EMBED Equation.DSMT4
正方形区域为： EMBED Equation.DSMT4
(1）使用PDE工具箱打开GUI求解方程
（2）进入Draw模式，绘制一个矩形，然后双击矩形，在弹出的对话框中设置Left=-1，Bottom=-1，Width=2，Height=2,确认并关闭对话框
(3)进入Boundary模式，边界条件采用Dirichlet条件的默认值
(4)进入PDE模式,单击工具栏PDE按钮，在弹出的对话框中方程类型选择Eigenmodes，参数设置c=1,a=-1/2，d=1,确认后关闭对话框
(5）单击工具栏的 EMBED Equation.DSMT4 按钮，对正方形区域进行初始网格剖分，然后再对网格进一步细化剖分一次
（6)点开solve菜单，单击Parameters选项，在弹出的对话框中设置特征值区域为[-20，20］
（7)单击Plot菜单的Parameters项，在弹出的对话框中选中Color、Height（3-D plot)和show mesh项，然后单击Done确认
（8）单击工具栏的“="按钮，开始求解

PAGE

PAGE  12
