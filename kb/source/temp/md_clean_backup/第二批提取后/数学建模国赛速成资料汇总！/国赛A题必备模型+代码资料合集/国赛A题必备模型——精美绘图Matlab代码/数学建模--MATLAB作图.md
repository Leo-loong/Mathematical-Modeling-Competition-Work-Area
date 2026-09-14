<!-- 第 1 页 -->
数学建模与数学实验
MATLAB作图

<!-- 第 2 页 -->
MATLAB作图
二维图形
三维图形
图形处理
实例
作业
特殊二、三维图形

<!-- 第 3 页 -->
MATLAB作图是通过描点、连线来实现的，故在画一个曲线图形之前，必须先取得该图形上的一系列的点的坐标（即横坐标和纵坐标），然后将该点集的坐标传给MATLAB函数画图.
命令为：
plot(X,Y,S)
plot(X,Y)— 画实线
plot(X,Y1,S1,X,Y2,S2,……,X,Yn,Sn)
— 将多条线画在一起
X,Y是向量,分别表示点集的横坐标和纵坐标
线型
y  黄色   . 点   -  连线
m  洋红   o 圈   :  短虚线
c  蓝绿色     x  x-符号       -.  长短线     r  红色        +   加号      --  长虚线
1.曲线图

<!-- 第 4 页 -->
## 例 在[0,2  ]用红线画sin x,用绿圈画cos x.
例 在[0,2  ]用红线画sin x,用绿圈画cos x.
x=linspace(0,2*pi,30);
y=sin(x);
z=cos(x);
plot(x,y,'r',x,z, 'g0')
解
MATLAB  liti1

<!-- 第 5 页 -->
2.符号函数(显函数、隐函数和参数方程)画图
(1) ezplot
ezplot(‘x(t)’,’y(t)’,[tmin,tmax])
表示在区间tmin<t<tmax绘制参数方程                                                x=x(t),y=y(t)的函数图.
ezplot(‘f(x)’,[a,b])
表示在a<x<b绘制显函数f=f(x)的函数图.
ezplot(‘f(x,y)’,[xmin,xmax,ymin,ymax])
表示在区间xmin<x<xmax和 ymin<y<ymax绘制
隐函数f(x,y)=0的函数图.

<!-- 第 6 页 -->
例   在[0,   ]上画y=cos x 的图形.
解 输入命令     ezplot(‘sin(x)’,[0,pi])
MATLAB liti25
解 输入命令
ezplot(‘cos(t)^3’,’sin(t)^3’,[0.2*pi])
MATLAB liti41
解  输入命令
ezplot('exp(x)+sin(x*y)',[-2,0.5,0,2])
MATLAB liti40

<!-- 第 7 页 -->
(2) fplot
注意：
[1] fun必须是M文件的函数名或是独立变量为x的字符串.
[2] fplot函数不能画参数方程和隐函数图形，但在一个图上可以画多个图形.
fplot(‘fun’,lims)
表示绘制字符串fun指定的函数在lims=[xmin,xmax]的图形.

<!-- 第 8 页 -->
解  先建M文件myfun1.m：
function Y=myfun1(x)
Y=exp(2*x)+sin(3*x.^2)
再输入命令：
fplot(‘myfun1’,[-1,2])
MATLAB liti43
MATLAB liti28
解 输入命令:
fplot(‘[tanh(x),sin(x),cos(x)]’,2*pi*[-1 1 –1 1])
例  在[-2,2]范围内绘制函数tanh的图形.
解   fplot(‘tanh’,[-2,2])
MATLAB liti42

<!-- 第 9 页 -->
3. 对数坐标图
在很多工程问题中,通过对数据进行对数转换可以更清晰地看出数据的某些特征,在对数坐标系中描绘数据点的曲线,可以直接地表现对数转换.对数转换有双对数坐标转换和单轴对数坐标转换两种.用loglog函数可以实现双对数坐标转换,用semilogx和semilogy函数可以实现单轴对数坐标转换.
loglog(Y)        表示 x、y坐标都是对数坐标系
semilogx(Y)   表示 x坐标轴是对数坐标系
semilogy(…)    表示y坐标轴是对数坐标系
plotyy 有两个y坐标轴，一个在左边，一个在右边

<!-- 第 10 页 -->
例   用方形标记创建一个简单的loglog.
解   输入命令:
x=logspace(-1,2);
loglog(x,exp(x),’-s’)
grid on     %标注格栅
MATLAB liti37
例  创建一个简单的半对数坐标图.
解  输入命令:
x=0:.1:10;
semilogy(x,10.^x)
MATLAB liti38
例  绘制y=x3的函数图、对数坐标图、半对数坐标图.
MATLAB liti22
返回

<!-- 第 11 页 -->
三维图形
1. 空间曲线
2. 空间曲面
返回

<!-- 第 12 页 -->
plot3(x,y,z,s)
空  间  曲  线
1. 一条曲线
例  在区间[0，10π]画出参数曲线 x=sint,y=cost,
z=t.
MATLAB liti8
解  t=0:pi/50:10*pi;
plot3(sin(t),cos(t),t)
rotate3d  %旋转

<!-- 第 13 页 -->
plot3(x,y,z)
2. 多条曲线
例 画多条曲线观察函数Z=(X+Y)2.
（这里meshgrid(x,y)的作用是产生一个以向量x为行、向量y为列的矩阵）
MATLAB liti9
其中x，y，z是都是m×n矩阵，其对应的每一列表示一条曲线.
解  x=-3:0.1:3;y=1:0.1:5;
[X,Y]=meshgrid(x,y);
Z=(X+Y).^2;
plot3(X,Y,Z)
返回

<!-- 第 14 页 -->
## 空  间  曲  面
空  间  曲  面
例  画函数Z=(X+Y)2 的图形.
解  x=-3:0.1:3;
y=1:0.1:5;
[X,Y]=meshgrid(x,y);
Z=(X+Y).^2;
surf(X,Y,Z)
shading  flat    %将当前图形变得平滑
MATLAB liti11
(1)  surf(x,y,z)
画出数据点（x，y，z）表示的曲面

<!-- 第 15 页 -->
（2）  mesh(x,y,z)
解 x=-3:0.1:3;   y=1:0.1:5;
[X,Y]=meshgrid(x,y);
Z=(X+Y).^2;
mesh(X,Y,Z)
MATLAB liti24
例  画出曲面Z=(X+Y)2在不同视角的网格图.
画网格曲面

<!-- 第 16 页 -->
(3)meshz(X,Y,Z) 在网格周围画一个curtain图(如,参考平面)
解 输入命令:
[X,Y]=meshgrid(-3:.125:3);
Z=peaks(X,Y);
meshz(X,Y,Z)
例  绘peaks的网格图
MATLAB liti36
返回

<!-- 第 17 页 -->
在图形上加格栅、图例和标注
定制坐标
图形保持
分割窗口
缩放图形
改变视角
图形处理
返回
动       画

<!-- 第 18 页 -->
## 1. 在图形上加格栅、图例和标注
1. 在图形上加格栅、图例和标注
（1）GRID ON: 加格栅在当前图上
GRID OFF: 删除格栅
处理图形
（2）hh = xlabel(string):在当前图形的x轴上加图例string
hh = ylabel(string): 在当前图形的y轴上加图例string
hh = title(string): 在当前图形的顶端上加图例string
hh = zlabel(string): 在当前图形的z轴上加图例string

<!-- 第 19 页 -->
例 在区间[0,2π]画sin(x)的图形，并加注图例“自变量
X”、“函数Y”、“示意图”, 并加格栅.
解  x=linspace(0,2*pi,30);
y=sin(x);
plot(x,y)
xlabel('自变量X')
ylabel('函数Y')
title('示意图')
grid on
MATLAB liti2

<!-- 第 20 页 -->
## （3）  hh = gtext(‘string’)
（3）  hh = gtext(‘string’)
命令gtext(‘string’)用鼠标放置标注在现有的图上.
运行命令gtext(‘string’)时，屏幕上出现当前图形，在
图形上出现一个交叉的十字，该十字随鼠标的移动移动，
当按下鼠标左键时，该标注string放在当前十交叉的位
置.
例 在区间[0,2π]画sin(x)，并分别标注“sin(x)”
”cos(x)”.
解  x=linspace(0,2*pi,30);
y=sin(x);
z=cos(x);
plot(x,y,x,z)
gtext(‘sin(x)’);gtext(’cos(x)’)
MATLAB liti3
返回

<!-- 第 21 页 -->
2. 定制坐标
Axis([xmin xmax ymin ymax zmin zmax])
例 在区间[0.005,0.01]显示sin(1/x)的图形.
解  x=linspace(0.0001,0.01,1000);
y=sin(1./x);
plot(x,y)
axis([0.005 0.01 –1 1])
MATLAB liti4
返回
定制图形坐标
将坐标轴返回到自动缺省值
Axis auto

<!-- 第 22 页 -->
3. 图形保持
(1)  hold  on
hold  of
例 将y=sin(x)、y=cos(x)分别用点和线画出在同一屏幕上.
解  x=linspace(0,2*pi,30);
y=sin(x);
z=cos(x)
plot(x,z,:)
hold on
Plot(x,y)
MATLAB liti5
保持当前图形, 以便继续画图到当前图上
释放当前图形窗口

<!-- 第 23 页 -->
(2)    figure(h)
例  区间[0,2 ]新建两个窗口分别画出y=sin(x)；
z=cos(x).
解  x=linspace(0,2*pi,100);
y=sin(x);z=cos(x);
plot(x,y);
title('sin(x)');
pause
figure(2);
plot(x,z);
title('cos(x)');
MATLAB liti6
返回
新建h窗口，激活图形使其可见，并把它置于其它图形之上

<!-- 第 24 页 -->
4. 割窗口
h=subplot(mrows,ncols,thisplot)
划分整个作图区域为mrows*ncols块（逐行对块访问）并激活第thisplot块，其后的作图语句将图形画在该块上.
激活已划分为mrows*ncols块的屏幕中的第thisplot块，其后的作图语句将图形画在该块上.
命令Subplot(1,1,1)返回非分割状态.
subplot(mrows,ncols,thisplot)
subplot(1,1,1)

<!-- 第 25 页 -->
解x=linspace(0,2*pi,100);
y=sin(x); z=cos(x);
a=sin(x).*cos(x);b=sin(x)./(cos(x)+eps)
subplot(2,2,1);plot(x,y),title(‘sin(x)’)
subplot(2,2,2);plot(x,z),title(‘cos(x)’)
subplot(2,2,3);plot(x,a),title(‘sin(x)cos(x)’)
subplot(2,2,4);plot(x,b),title(‘sin(x)/cos(x)’)
例 将屏幕分割为四块，并分别画出y=sin(x)，z=cos(x)，a=sin(x)×cos(x),b=sin(x)/cos(x).
MATLAB liti7
返回

<!-- 第 26 页 -->
5. 缩放图形
zoom  on
单击鼠标左键，则在当前图形窗口中，以鼠标点中的点为中心的图形放大2倍；单击鼠标右键，则缩小2倍.
解  x=linspace(0,2*pi,30);
y=sin(x);
Plot(x,y)
zoom on
MATLAB liti13
例 缩放y=sin(x)的图形.
zoom  off
为当前图形打开缩放模式
关闭缩放模式
返回

<!-- 第 27 页 -->
6. 改变视角view
（1）view(a,b)
命令view(a,b)改变视角到(a,b),a是方位角,b为仰角.缺省视角为（-37.5，30）.
解 x=-3:0.1:3;   y=1:0.1:5;
[X,Y]=meshgrid(x,y);
Z=(X+Y).^2;
subplot(2,2,1)， mesh(X,Y,Z)
subplot(2,2,2)， mesh(X,Y,Z)，view(50,-34)
subplot(2,2,3)， mesh(X,Y,Z)，view(-60,70)
subplot(2,2,4)， mesh(X,Y,Z)，view(0，1，1)
MATLAB liti10
例   画出曲面Z=(X+Y)2在不同视角的网格图.
view用空间向量表示的，三个量只关心它们的比例，与数值的大小无关，x轴view（[1，0，0]），y轴view（[0，1，0]），z 轴view（[0，0 ，1]）.
（2）view（[x，y，z]）
返回

<!-- 第 28 页 -->
7. 动画
Moviein(),getframe,movie()
函数Moviein()产生一个帧矩阵来存放动画中的帧；函数getframe对当前的图像进行快照；函数movie()按顺序回放各帧.
MATLAB liti14
返回
例 将曲面peaks做成动画.
解 [x,y,z]=peaks(30);
surf(x,y,z)
axis([-3 3 -3 3 -10 10])
m=moviein(15);
for i=1:15
view(-37.5+24*(i-1),30)
m(:,i)=getframe;
end
movie(m)

<!-- 第 29 页 -->
特殊二、三维图形
1. 特殊的二维图形函数
2. 特殊的三维图形函数
返回

<!-- 第 30 页 -->
特殊的二维图形函数
1. 极坐标图：polar (theta,rho,s)
用角度theta（弧度表示）和极半径rho作极坐标图，用s指定线型.
解：theta=linspace(0,2*pi),
rho=sin(2*theta).*cos(2*theta);
polar(theta,rho,’g’)
title(‘Polar plot of sin(2*theta).*cos(2*theta)’);
MATLAB liti15

<!-- 第 31 页 -->
2. 散点图:  scatter（X,Y,S,C）
在向量X和Y的指定位置显示彩色圈．X和Y必须大小相同．
解  输入命令：
load seamount
scatter(x,y,5,z)
MATLAB liti29
3. 平面等值线图: contour(x,y,z,n) 绘制n个等值线的二维
等值线图
解   输入命令：
［X,Y］=meshgeid(-2:.2:2,-2:.2:3);
Z=X.*exp(-X.^2-Y.^2);
[C,h]=contour(X,Y,Z);
clabel(C,h)
colormap cool
MATLAB liti34
例  绘制seamount散点图
返回

<!-- 第 32 页 -->
特殊的三维图形函数
1. 空间等值线图： contour 3(x,y,z,n)
其中n表示等值线数.
例 山峰的三维和二维等值线图.
解 [x,y,z]=peaks;
subplot(1,2,1)
contour3(x,y,z,16,'s')
grid,   xlabel('x-axis'),ylabel('y-axis')
zlabel('z-axis')
title('contour3 of peaks');
subplot(1,2,2)
contour(x,y,z,16,'s')
grid,  xlabel('x-axis'), ylabel('y-axis')
title('contour of peaks');
MATLAB liti18

<!-- 第 33 页 -->
2. 三维散点图 scatter3（X,Y,Z,S,C）
在向量X,Y和Z指定的位置上显示彩色圆圈.
向量X,Y和Z的大小必须相同.
解 输入命令:
[x,y,z]=sphere(16);
X=[x(:)*.5 x(:)*.75 x(:)];
Y=[y(:)*.5 y(:)*.75 y(:)];
Z=[z(:)*.5 z(:)*.75 z(:)];
S=repmat([1 .75 .5]*10,prod(size(x)),1);
C=repmat([1 2 3],prod(size(x)),1);
scatter3(X(:),Y(:),Z(:),S(:),C(:),'filled'),view(-60,60)
例  绘制三维散点图.
MATLAB liti32
返回

<!-- 第 34 页 -->
绘制山区地貌图
要在某山区方圆大约27km2范围内修建一条公路，从山脚出发经过一个居民区，再到达一个矿区.横向纵向分别每隔400m测量一次，得到一些地点的高程：(平面区域0≤x≤ 5600,0≤y≤4800)，需作出该山区的地貌图和等高线图.
MATLAB shanqu
返回

<!-- 第 35 页 -->
返回
实验作业
1. 在同一平面中的两个窗口分别画出心形线和马鞍面.
要求：
1)在图形上加格栅、图例和标注
2)定制坐标
3)以不同角度观察马鞍面

<!-- 第 36 页 -->
谢谢！
