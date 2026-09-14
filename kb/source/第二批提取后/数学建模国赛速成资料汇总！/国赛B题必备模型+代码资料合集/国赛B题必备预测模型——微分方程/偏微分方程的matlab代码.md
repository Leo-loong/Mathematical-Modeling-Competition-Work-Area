《瞓偏微分方程数值解法的 MATLAB 吗〖史新毕
说咖山千偏微分的程序都比较长，比其他的算泓稍复杂一些，所以另开一貼，专门上传偏微分程序
谢谢大家的支持！
其他的数值算法见：
.]/Announce/Announce asp?BoardID=209&id=8245004
1 、古典显式格式求解抛物型偏微分方程（一维热传导方程）
functlon IU x tl—PDEParabohcClassicalExplicit(uX.uT,phi,psi I,psi2,M,NC)
％古典显式格式求解抛物型偏微分方程
%[U x 刂一 PDEP 訂 ab 湖记 0 然 0 正 xp 雇 it 在 X T ，种 1 ， p 1 ， p 《 2 ， M ， N ℃ ）
％方程． u 忤 C 0 x uX,0 t ．；。 uT
％初值条件：虱 x 两唧地对
％边值条件； u(0 t)-psi 1@， uftlX,0=psi2(t)
％输出参数： U ．解詎阵，第一行表示初值，第一列和最后一列表示边值，第二行表示第 2 层一
x 一空闷变量
t ．时间变量
％输八参数； ux 一司变量 x 的取上限
uT ．时间变量 1 取值上限
phJ 0J0 条件，定义为内联函数
的 1 ，边值条件，定为内联函数
一 2 值条 0 定义为内联数
M 一沿 x 轴的等分区间数
N ．沿〔轴的等分区河數
c 、系数，默认情况下 01
％应用举例！
%uX=l ； uT 以 0 ． M 一巧； N 二 1D0 C 二 1 ，
0
%phi=unlineCsin(pi*x));psil=unhne(t)');psi2=1nline(W);
％@ x t]—PDEParaboIicCIassicaIExpIic1t(uX,uT,phi,psiI,psi2,M,N,C);
％设置参数 c 的默认值
if nargin==7
end
％计算步长
dx=uXLM;%x 的步长
dt=uTfN;%t 的步长
1 一 C*dt•' 血，巛；％步长比
rl— 不 2 竹；
if > 0 ， 5
山． r ． > 05 不稳定：）
end
‰ 计算初仙和边值
U=zeros(M+l,N+l);
for i=l'M+l
00 j-phi 《 x0月；
end
U(I ， j)=p $ il@0
M + 1 出： 2 的旌
end
％逐层求解
for i ： 2
U(i,j + 10 产 U （ i-l\j 》 0U00 “ * U （ i00
end
U=V;
％作出图形
亩圄咕典显式格式，一维热传导方程的解的图像》
xla 空间变量对
ylabelClbTti] 变量 0
小 & 圹一热传导方程的解
re.turtti
乜古典显式恪式不稳定情况
0
． 1 的
0 地
乜出．典显式恪式稳定情况
、一适攥礱的的壓 0
0 地．
了 i 豇《思，
2 、古典隐式格式求解抛物型偏微分方程（一维热传导方程）
function IU x tl=PDEParabolicClassicalImp1icit(uX,uT phi,psi l,ps12,M N,C)
％古共隐式格式求解抛物里偏微分方程
%[U x t]=PDEParab01icClassicallmplici1(uX,uT,phi,psil ， PS12*M ， N,C.)
％方程； u t=C 与 0 二 x ． uX 0 < 二 t < 二 uT
％初值条件：，的：种 i
％边值条件； u00 一 l(t) ， u()X ， 0-psi2(0
％输出参做； U ．解矩阵，第一行表示初值，第一列和最后一列表示边值，第过行表示．第 2 层一
x 一空间变量
t ．时间变量
％输入参数： ux “ 空间变量 x 的取值上限
uT 、时间变量 t 的取有上限
phi ，初值条件，定义为内联函数
画 1 迪 值 条 件 ` 定 义 为 内 联 数
2 一边值条件，定义为内．联函数
M ．沿轴等分区间数
N ．沿 t 轴的等分区间數
C ．系．数，默认情一卜 C=I
％应用举例：
%uX—I ； uT 《 M 50 ； N 50 ℃ 1 ．；
%phi—inline('sin(pl*x)f);psi l—in il 淵》； p $ i2 到 nlin 以 ' 0 生
％〔 0 x t]=PDEParab01icClassicallmplicit(uX,uT,phi,psil psi2,M,N,C);
％设置参数 c 的默认值
if nargin—•l
end
‰ 计算步长
dx-uX.•M ，％、的步长
山： uT ；％ 1 的步长
x—(0M)*dx;
t=(ON)*dt;
1 一 0 ／；％步长比
D ros(l ， M 一 0 矩阵的对鱼线元素
L 灬一灬（ 1 ， M ． 2 } ，％阵的下对角线元素
U 灬（ 1 ． M ． 2 ）；％矩的上对角线元素
for i=l:M.2
Diag(i)—1+2*r;
end
Diag(M•l)=l+2*r•
％计算初值和边值
U ：娌 ro $ （ M 斗 1 ， N + 0
for 种上 M 到
cnd
fcjr j=I:N+l
0
0
U(lJj-psil(t(ij);
LJ { M + 0 ： 2 的
end
％逐层求解，需要使川追赶泓（调用函数 EqtsForwardAndBackward)
for j—I:N
bI=zeros(M-I, 性
bl(M-lj-r*U(M+Ri+l),
b—U(2 (j) 十 bl ，
U(2:Mj+1)•EqtsForwardAndBackward(Low.Diag,Up,b),
end
％作出图形
mesh(x LU);
titl 虻古典隐式格式，一维热传导方程的解的图像〕
b巛@阃变量的
abcl （ ' 时间变量 0
zlabe （冖维热传导方程的解 U)
压山 r 瞓
此算法需呶使用追赶法求解三对角线性方程组，这个算法在上一篇軲子中已经给出，为了方便，再给出来
追赶法解 0 对角线性方程组
function x—EqtsForward 、 AndBackward(L D,Utb)
％追赶法求解三对角线性方程组 Ax-b
%x=EqtsForwardAndBackward(L,D,U,b)
%x 过对角线性方程组的解
％ L 三对知阵的下对角线，行向量
％ D 对角詎阵的对角线，．行向量
%U 三对角矩阵的上对角线，行向量
％线性方程组 Ax=b 中的 b ，列向量
％应用举例．
%L-[•I ． 2 司，上〔 2 3 4 5 上 U ：卜 I ． 2 ． 30 6 1 ． 2
%x—FAtsF0twardAndBaekward(L,D,U b)
％检查参数的输人是否正确
n=length(l)),m=length(b);
的二》 “ gth （ 0000 “ g 山（ U } ：
if 0n1 ～冖
disp( 输人参数有误！》
returlv
end
％追的过程
订 i=2:n
L00 ： L00 以 i 、 0 ，
以 i) 一 L(i 一 1 尸@一
end
zero $ 0 ， 0
for i=2.-n
cnd
％赶的过程
x 回。对 nV 0
对 i) ：0@．U （旷种到 0 耱
end
return;
占典隐式格式
0
0
遜咩能性一一禹 0 導 0 鼕，
0
0 ；
在以后的程序中，我们都取 c=l ，不再作为一个输入参数处理
隐式格式求解鼬物型偏微分方程
3 、 C n N 记視需咖
需要调用追赶法的程序
åünction IU x tl=PDEParaboIicCN(uX,uT phi,psiI,psi2,M,N)
%Ctank-NieoIson 隐式格式求的抛物型偏微分方程
%[U x t]=PDEParab01ieCN(uX*11T,ph1,PSll p 2 M,N)
％方和： u xx < uX ， 0 《 1 uT
％初值条件 0 ：种 i
％边 1 直条件： u@的二@1@， u № 》 p (0
0
0
0
0
％输出参数： U 矩阼，第一行表示初值，第一列和最后一列表示边直，第过行表示第 2 层一
x ．空司变量
t ．时间变量
％输入参数； ux 一啊司变量 x 的取值上限
uT ．时间变量 t 的取上限
phl J 值条件，定义为内联函数
0i1 ．边值条件》定义为内联函数
伊 i2 ．边值条件，定义为内联函数
M 一沿轴的等分区间数
N ．沿 t 轴的等分区间数
％应用举例：
，， X ：丨； uT ： 2 ， M 干 50 ； N ： 50
%pht=inlineCsin(pi*xY),psi 1 ， psi2=inline(O);
%[U x t]=PDEParab01ieCN(uX,LIT ， ph10》 1 ， 2
％计算步．长
dx=uX/M,%x 的步长
dt=uT 叭：％ 1 的步长
1 ： ()N 了山；
r=dt/d 对 dx ；％步长比
Diag-zerosCl ， M ．的；％矩阵的刈的线元素
l-ow=zeros(l ， M ．以％庫阵的下对角线元素
Up “ 灬出 M ． 2 ）；％矩阵的上对角线元素
for 《： M 一 2
Diag(i)=I+r,
Low(i)--rf2;
跏@一 02 ；
end
Diag(M-I)* +r;
％汁算初值和边值
U=zemos(M+I,N+I);
for 0 的 M 十 ]
cnd
for j••l :N+I
1J(1,j 、)—p巛@班
U@十 1 ， j 厂的 2@0
end
B “ “ 对 M 一 1 ， M 一 0
for i=l:M.2
B(i,ij—l-r;
， i + 0 ：在 2 ；
B （ i + 1 ， 0002 ；
end
B(M•I,M•I)=I 寸；
0
0
％逐层求解，需要雙川追赶泫（调用数 EqtsFormrdAndBackward)
bI=zeros(M-1, 地
bl(l)=r*(U(lj+l)+U(l,j)Y2;
bl （ M 刁 0 气以 M 到， j 到）十 IJ （ M 十 1 出 V2 ；
U(2:M,j+l )—EqtsForwardAndBackward(Low Diag,Up,b);
end
％作出图形
me 訃 1 ， 0 ；
title(Crank 、 Nicolson 式格式，一维热传导方程的解的图像》
对圹空阊变量对
訃 el （时间变量 0
zlabe 〔一维热传导方程的解
压山 rn ；
@CranA7icoIson 隐式格式
．上 0 一丆 [ 《 00 、「上剂就 00
0 上，
0 ；
4 、 iE 方形区域卪 a “ 方穆 Diriclet 同题的求解
需要调用 Jacobi 迭代法和 Guass-SeideI 迭代法求解线性方程组
0
0
function IU x y]—PDEEIIipseSquareLaplaceDinch1et(ub,ph11,phi2,psil 卧 i2 ， M ， 0r0
％方形区域凵卪 “ 方程的 mriclet 边佰同题的差分求解
％此程序需要调用 Jacobi 送代法或者 Guass-Seidel 迭代泫求解线骨方程组
％@ x yJ=PDEEllipseSquarcLapIaceDirichlct(ub,phiI phi2,psiI ， i2 ， M 0
‰ 方程． + 巧厂 0 0 《，：
％边值条件； uLy)-phi l(y)
uCub,yj-phi2(y)
u （ & 过 bF1 “ i2 （对
％输出参数： U ．解矩阵，第一行表示厂 0 时的值．，第行表示厂 h 时值一
x 、横坐标
Y 一纵标
％输入参数： ub ．变量边界值的上限
phil,phi2,psil ,psi2 一边界函数，定．义为内联函数
M ．横纵坐标的等分区间数
巧．求解差分方程的迭代格式，若采 Jacobi 迭代格式
若 type=GS', 采用 Guass-Se1del 送代格式。畎认情况下， 0 世一 ℃ S '
％应用举：
0/oub—4;M=20;
%phiI—mIine(Y*(4-y)mphi2—inIineCO%),psi —inlin ' $ i 以 pi* 对 40 尹 $ i2—inIi 以 0 〕 ' } ；
%[U x yl=PDEEIIipseSquareLaplaceDirichlet(ub,phil p11i2 ， psiLpsi2 M,GS');
0 nargin==6
巧世。 GS ' ，
end
％步长
h=ub!M
％横纵坐标
％差分格式的矩阵形式 AU=K
％构造的 A
M2 ：（ M 山 0
A 一 z 亠》寸 M
for i=1:M2
A( 河： 4 ；
end
(c)f i=l:M2-
if mod 在 M 、 I) 一、。 0
A （ i01 产；
AO+I ， i01 '
end
end
for i— 上 M M 十 1
A(i i 十 M 司》刁；
0
0
AO+M 、 1 0 七
end
U=zeros()4 0
％边值条曾
for 0 的 M 十 1
U 在 0邗巛@一炉
U(i,M+lFpsi2((i- 炉
U(I ， i)=phil@一 1 严 0
U(M 十 0）一ph]2@．《产h）；
end
‰ 构造 K
K “ 吓（ M2 ， 0 ；
for i=l'M•l
K00U0 + 1 山
K012 与 + 0 ： U(i 到， M 刊
end
K （ M2 一 M12 》 K { M2 一 M ． 0 U 卩，，
for 02 ： M 、 2
@（M山气 i 山 + 0 一卩計 0 ；
坷（ M ． l)*i) ： U01 + 1 0
end
x0 删 ne M2 ， 0 ；
switch 巧
0
0
％调用 Guass-SeideI 选代法求解线且方程组 AU K
“ 虻 tJacobl'
X—EqtsJacobi(A,K,x0),
％调用 Guass-Setdel 迭代泫求解线性方程组 AU=K
X=EqtsGS(A,K,x0);
， Ot 五到 se
dis 的差分格式类型输人错误〕
re.tur•n;
end
％把求解结果化成短阵型式
for i—2:M
for j=2:M
U { J ， i ）一 X01 气 M 、 1 ， )*(i ． 2
end
U—U,
％作出图形
me 訃掣 0 ；
血鳳点差分格式 Laplace 方程 DJriclet 问题的解的图．像》
对 a 沅 IC 的
a 巧 e 旷的
zlabel('Laplace 方程 Diriclet 问题的解 0
压山 rn ；
乜讵方形区域 Laplace 方程五点差分格式
5 、一阶双的型方程的差分方法
function [U x tl"PDEHyperboIic(uX,uT,M,N,C,phi,psi 1,psi2,type)
％一阶双曲型方程的差分格式
%[U x t]—PDEHyperboIic(uX,uT,M,N,C,phi,psil,psi2,typej
％方程： u t+C*u x=0 0 < = t < ： uT, 0 < =
％初值条件． u 区 0 } 叩 hi （对
％输出参， U 、解矩阵，第一行表示初值，第二行表示第 2 个时间层一
x 罪坐标
t 一纵坐标，时阃
％输入参数： ux 、变量 x 的上界
uT 一变量《的上界
M ．变量 x 的等分区间数
N ．变量 t 的等分区间数
c 孫
phi ．初值条付函数，定义为内联函数
psil ,psi2 一边 1 直条件函数，定义为内联函数
帅《．差分格式，从下列值中选取
的世 0 寸 ' 飛 d 彘 h 采用 Lax-Friedrichs 差分格式求解
以卵 e 一 00t10n 小翮 onR 就采用 Courant-Isaacson-Rees
．巧： ' 上 “ pF “ g ' ，采用 Leap•Frog （鲢跳〕差分格式求
-ope=LaxWendroff, 采用 Lax W “ d 阉差分．格式求解
差分格式求解
： 0 “ kN 5 耐，采用差分格式求解，此格式需调用追赶法
求解三对角线骨方程组
删 X,•M ，％变量 x 的步长
炉 u 的 N ； ‰ 变量的步长
。 k 山．％步长比
U••zeros(M+1 ， N+0；
％初值条件
for 汾上 M 十 1
cnd
％边值条件
fcjr j ：上 N 斗 1
LJ(I ，jj-p司@毖
U01 + 1 ， j 片卩 s 《 2@li));
%U(l,j)—NaN;
％ U01 + 1 ,j)=NaN,
end
1 师 e
%Lax-Friedrichs 差分格式
case iLaxFriedrichsi
if 訃 s(C 孬 0 ：刁
d 这凶 001 ， Lax 丰飛 d 小 h $ 差分格式不稳定！》
0
％逐层求解
for i=2:M
U(i ， j + 1 ）以 U(i + 10 还（ 0 河门一 C 新气 I-J （ i 到 0U0 一 1 ， 0 》 2 ；
end
%Courant-Isaacson-Rees 差分格式
case CourantlsaacsonRees•
山 'C ，采用前差公式〕
if C*r<-l
end
％逐层求解
0 「 i=2:M
U(i,j + 10000 * U （卜 0 产 U(i + 10 ；
cnd
else
d 这 0 ． 0 采用后差公式〕
if C 寧 01
d 这的 c 灬 an 《小皿吓 “ 还 “ s 差分格式不稳定！》
LJ0,j + 100 产 00 地． 00m （ ijj;
cnd
％逐层求解
for j= I:N
for 02M
cnd
end
0
0
0
%Leap-Frog 〔蛙跳》差分格式
“ “ 'LeapFrog'
冲 i2 艹甲 ut （ ' 请输人第过层到值条件函数； pst2 刁；
if 訃 s(C 》刁
d 这凶 001 ， Leap-Frog 差分格式不稳定 1 〕
end
％第过层．初值条件
for 01 ： M + 1
U 在 2)=phi2 骁
end
％逐层求解
for j—2N
for i=2:M
1J(i,j+l)=U0j-l)-C*r*(U(i+l,j)-l 丿（0j就
end
end
%Lax-Wendrofi 、差分格式
凵 'LaxWendroff
评 abs(C•r)>1
d 这的 001 ， 0 ～ w 《 ndr 。 0 差分格式不稳定！》
end
％逐层求解
for i=2:M
U(i ， 010 00i 到． U （凵 j02 十 02 ． 0 （ U （汾 l,j 戽 U(l,j ）十 U()- ,J 力过；
end
end
%Crank-NicoIson 隐式差分恪式，需调用追赶法求解三对角线性方程组的算法
“ CrankNicolson
Diag- “ 灬 0 ． M 一 0 ‰ 矩的对的线元
l-ow—zeros(l ， M ．与酆阵的下对角线元素
Up 一 ze 灬卩， M ． 2 ）；％矩阵的上对角线元素
for 1 ： M ， 2
Diag(i)=4;
end
Diag(M-l)—4;
B=zeros(M-1 ， M 一 0
for i=lM.2
B(i ， i尸4；
B(i+l ， 00 产 C ；
end
B(M I ， M 山到，
0
0
％逐层求解，需要使川追赶法（调川所 E 下。 ru dA " 戕旧
」：上 N
bl=zeros(M 1 ，以
bl(l) “ ℃ 气 U(1,j + 0 + U(I 山贮；
bl （ M 刁 0 的 0 （ U （ M+I ， j 十 10U （ M 到 0 理；
b=B*U(2:M,j)+bI;
U(2:M,j+l)—EqtsForwardAndBackward(Low,Diag,Up,b),
end
．．然孥诔 e
d 这 p 《差分格式头型输入有误！》
return;
end
％作出图形
1 ， 0 ；
血 0 赆 ' 格式求解一阶双曲型方程的解的图像肛
对 ab 0 阎变量妁，
y 《訃 cl （时间变量 0
zlabe 〔一阶双曲是方程的解蚴，
压山 rn ；
0
0
