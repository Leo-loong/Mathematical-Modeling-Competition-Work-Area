I. 微分方程的定义
对于 dufftng 方程 + 无
． = 攴 2
攴
= 0 ，先将方程写作
X
2
3
—CD 一无 1
func t ion dy=duffing(), x)
omega= 1 ；％定义参数
f 1 = x （ 2 ）；
f2=-omega 2*x(l)-x (l) 一 3 ；
dy±[fl ； f2] ；
2 ．微分方程的求解
funct i on 50h ℃ (tstop)
tst 。 p 一 500 ，％定义时间长度
y0= [ 0 ． 01 ； 0 ] ；％定义初始条件
Ct, 到一 0de45 (' duffing' ， tstopt 、 0 [ ] ）：
funct i on solve (tstop)
$ tep=0. 01 ，％定义步长
y0=rand 0 ， 2 ）：％随机初始条件
tspan=C0:step•500] ：％定义时间范围
Ct, 到： 0de45 (' dufflng' ， t (0) ；
3 ` 时 间 历 程 的 绘 制
时间历程横轴为 t ，纵轴为 Y ，绘制时只取稳态部分。
plot(), y （：， I)) 绘制的时间历程
xlabel （ ' t' ）％横轴为 t
ylabel （， yt 纵轴为 Y
gri 山％显示网格线
axis(C460 500 一 1 n f lr 的）％图形显示范围设置
4 ．相图的绘制
相图的横轴为 Y ，纵轴为 dy/dt ，绘制时也只取稳态部分。红色部分
表示只取最后 10m 个点。
plot (y(end-1000 l) ， y (end-1000:end, 2 月；％绘制 Y 的时间历
程
xlabel (' y' ）％横轴为 Y
ylabel （ ' dy/dt' 纵轴为 dy/dt
gri 山％显示网格线
5 .Poincare 映射的绘制
对于不同的系统， Poincare 截面的选取方法也不同
对于自治系统一般每过其对应线性系统的固有周期，截取一次
对于非自治系统，一般每过其激励的周期，截取一次
例程 duffing 方程十攴十 x 一 0 的 poincare 映射
func t i on poincare (tstop)
global omega ；
omega= 1 ，
T ： 2 * pi / 。 mega ；％线性系统的周期或激励的周期
step 一 T / 1 佣，％定义步长为 T ／ 100
y0 一 [ 0 ， 01 ； 0 ] ；％初始条件
tspan=C0:step: 1 開 * T ] ；％定义时间范围
[t, yl =ode45C duffing' ， tspan, yO ），
for i = 5000 ： 100 ： 1 佣 00 ％稳态过程每个周期取一个点
hold on ；％保留上一次的图形
end
xlabel （， y' ） ;ylabel （， dy/dt ' ）
Poincare 映射也可以通过取极值点得到
funct 1 on PO 1 ncare (tstop)
y0 ： [ 0 ． 01 ;0)
tspan=CO:0 、 01 “ 500 ] ：
Ct, 到 =od e45 C duffing' ， t spant (0) 和
count=find(t>100) ；％截取稳态过程
YZY (coun t ，：）；
n=length (y(:, D ）；％计算点的总数
for i 2 .n—l
if y(i-l, l)+eps<y(i, l) & & y(), l)>y(i+l, l)+eps ％简单的取出
局部最人值
plot(y(l, y 0 ， 2), '
h01 d on
end
end
xlabel C y' ） ;ylabel C dy/dt' ）；
6 ．频谱
yy=fft (y （ end 一 1000 end, I)) ：
N=Iength (yy) ；
power=ab s (yy) ，
freq= .N—l)*l/step/N,
plot (freq （ 1.N/2), power （ 1 :N/2)) ；
xlabel （ ' f(y) ' ）
yl 楠 el （ ' y' ）
7 ．算例
duff i ng 方程、 + 攴 +
= 0 的时间历程，
相图，
频谱和 poincare
映射。
function dy=duffing(), x)
omega=l ；％定义参数
f2=—omega 一 2*x (l)-x (l) 一 3 ；
dy= Cfl ； f2] ；
funct i on duffsim （ tsto
s tep=O 、 1
tspan=CO ： step ： 500
Ct, 到二 0de45 (' duffing' ， tspan, (0) ；
subpl ot （ 2 ， 2 ， l)
plot(), y （
， l)) ：％绘制 Y 的时间历程
xlabel C t' 横轴为 t
ylabel （ ' y' 纵轴为 Y
gT 、 id ；％显示网格线
“ is （ [ 460 500 -lnf lnf 的％显示范围设置
subplot （ 2 ， 2 ， 2 ）
plot (y(end-1000 l), y (end-1000:end, 2 月；％绘制 Y 的时间历
xlabel （ ' y' ）％横轴为 Y
ylabel （ ' dy/dt' ）％纵轴为 dy/dt
grid ：％显示网格线
subpl ot （ 2 ， 2 ， 3 ）
yy=fft (y （ end 一 1000 end, I)) ；
N=Iength (yy) ；
power=ab s (yy) ；
fT 、 eq= 0 :N"I) 1 /st ep/N ，
plot (freq 〔 1 、 N/2 ），（ 1 .N/2)) ：
对 a № 1 （， f (y) ' ）
ylabel C y' ）
subpl ot （ 2 ， 2 ， 4 ）
count=find(t>100) ，％截取稳态过程
y=y (count, ：）；
n=length (Y(•
。 1)) ；％计算点的总数
for i 二 2 :n—l
讠 f y(i 一 1 ， l) ps 〈 y （ 1 ， l) & & y(), l) 〉 y （ 01 ， D 斗 eps ％简单的取出
局部最大佰
0 山 01d on ，
end
end
xlabel （ ' y' ,ylabel （ ' dy/dt' ），
刁、 05
1
470
40
0
& 分岔图的绘制
•O.OS
0 《 0
0 ． 05 ．
0 ． 15
0 2
+ 0 ． 3 戈一 + x 一丆 cosl.2t 随丆变化的分岔图。
func t ion dy=duffing(), x)
g ] ℃ ba 1 0
omega= 1 ；％定义参数
fl=x （ 2 ），
f2=omega 、 2 * x (I) -x (l) 一 3 一 0 、 3*x （ 2 ） +c*co s (). 2*t) ；
dy=[fl ； f2] ；
clear;
g 1 obal c ；％定义个局变量
range= [ 0 ． 1 ： 0 ． 002 ： 0 ． 9 ] ；％定义参数变化范围
YY= [ ] ；％定义空数组
for c=range
y0 ： [ 0 ． 1 ； 0 ] 初始条件
k=k+ I ，
tspan=CO:0 、 01 400 ] ；
Ct, 到： 0de45 (' duffing' ， t span, (0) 和
count=f1nd(t>200) ；
Y=Y ount ，：）；
n=length (Y 0 ， l) ）；
for i=2 ． n—l
l)+eps ％简单的取出
，局部最大值。
end
end
讠 f j > 1
plot(), YY (), [ 1
end
hold on ；
index (k) =j-l ，
end
xlabel （ ' c' )i
ylabel （ ' y' 》
markersize
25
0 ． 5
02
0 5
随 F 变化的分岔图
F=0.20
0 ． 8
0 、 9
F = 仇 27
F = 275
F = 仇 2875
0
0
F = 32
0
F = 仇 36
F =
400
F=O. 652
F = 仇 8
