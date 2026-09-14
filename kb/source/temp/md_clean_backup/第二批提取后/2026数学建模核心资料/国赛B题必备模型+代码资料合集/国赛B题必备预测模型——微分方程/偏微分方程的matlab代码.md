《 瞓 偏 微 分 方 程 数 值 解 法 的 MATLAB 吗 〖 史 新 毕
说 咖 山 千 偏 微 分 的 程 序 都 比 较 长 ， 比 其 他 的 算 泓 稍 复 杂 一 些 ， 所 以 另 开 一 貼 ， 专 门 上 传 偏 微 分 程 序
谢 谢 大 家 的 支 持 ！
其 他 的 数 值 算 法 见 ：
.]/Announce/Announce asp?BoardID=209&id=8245004
1 、 古 典 显 式 格 式 求 解 抛 物 型 偏 微 分 方 程 （ 一 维 热 传 导 方 程 ）
functlon IU x tl—PDEParabohcClassicalExplicit(uX.uT,phi,psi I,psi2,M,NC)
％ 古 典 显 式 格 式 求 解 抛 物 型 偏 微 分 方 程
%[U x 刂 一 PDEP 訂 ab 湖 记 0 然 0 正 xp 雇 it 在 X T ， 种 1 ， p 1 ， p 《 2 ， M ， N ℃ ）
％ 方 程 ． u 忤 C 0 x uX,0 t ． ； 。 uT
％ 初 值 条 件 ： 虱 x 两 唧 地 对
％ 边 值 条 件 ； u(0 t)-psi 1@， uftlX,0=psi2(t)
％ 输 出 参 数 ： U ． 解 詎 阵 ， 第 一 行 表 示 初 值 ， 第 一 列 和 最 后 一 列 表 示 边 值 ， 第 二 行 表 示 第 2 层 一
x 一 空 闷 变 量
t ． 时 间 变 量
％ 输 八 参 数 ； ux 一 司 变 量 x 的 取 上 限
uT ． 时 间 变 量 1 取 值 上 限
phJ 0J0 条 件 ， 定 义 为 内 联 函 数
的 1 ， 边 值 条 件 ， 定 为 内 联 函 数
一 2 值 条 0 定 义 为 内 联 数
M 一 沿 x 轴 的 等 分 区 间 数
N ． 沿 〔 轴 的 等 分 区 河 數
c 、 系 数 ， 默 认 情 况 下 01
％ 应 用 举 例 ！
%uX=l ； uT 以 0 ． M 一 巧 ； N 二 1D0 C 二 1 ，
0
%phi=unlineCsin(pi*x));psil=unhne(t)');psi2=1nline(W);
％@ x t]—PDEParaboIicCIassicaIExpIic1t(uX,uT,phi,psiI,psi2,M,N,C);
％ 设 置 参 数 c 的 默 认 值
if nargin==7
end
％ 计 算 步 长
dx=uXLM;%x 的 步 长
dt=uTfN;%t 的 步 长
1 一 C*dt•' 血 ， 巛 ； ％ 步 长 比
rl— 不 2 竹 ；
if > 0 ， 5
山 ． r ． > 05 不 稳 定 ： ）
end
‰ 计 算 初 仙 和 边 值
U=zeros(M+l,N+l);
for i=l'M+l
00 j-phi 《 x0月；
end
U(I ， j)=p $ il@0
M + 1 出 ： 2 的 旌
end
％ 逐 层 求 解
for i ： 2
U(i,j + 10 产 U （ i-l\j 》 0U00 “ * U （ i00
end
U=V;
％ 作 出 图 形
亩 圄 咕 典 显 式 格 式 ， 一 维 热 传 导 方 程 的 解 的 图 像 》
xla 空 间 变 量 对
ylabelClbTti] 变 量 0
小 & 圹 一 热 传 导 方 程 的 解
re.turtti
乜 古 典 显 式 恪 式 不 稳 定 情 况
0
． 1 的
0 地
乜 出 ． 典 显 式 恪 式 稳 定 情 况
、 一 适 攥 礱 的 的 壓 0
0 地 ．
了 i 豇 《 思 ，
2 、 古 典 隐 式 格 式 求 解 抛 物 型 偏 微 分 方 程 （ 一 维 热 传 导 方 程 ）
function IU x tl=PDEParabolicClassicalImp1icit(uX,uT phi,psi l,ps12,M N,C)
％ 古 共 隐 式 格 式 求 解 抛 物 里 偏 微 分 方 程
%[U x t]=PDEParab01icClassicallmplici1(uX,uT,phi,psil ， PS12*M ， N,C.)
％ 方 程 ； u t=C 与 0 二 x ． uX 0 < 二 t < 二 uT
％ 初 值 条 件 ： ， 的 ： 种 i
％ 边 值 条 件 ； u00 一 l(t) ， u()X ， 0-psi2(0
％ 输 出 参 做 ； U ． 解 矩 阵 ， 第 一 行 表 示 初 值 ， 第 一 列 和 最 后 一 列 表 示 边 值 ， 第 过 行 表 示 ． 第 2 层 一
x 一 空 间 变 量
t ． 时 间 变 量
％ 输 入 参 数 ： ux “ 空 间 变 量 x 的 取 值 上 限
uT 、 时 间 变 量 t 的 取 有 上 限
phi ， 初 值 条 件 ， 定 义 为 内 联 函 数
画 1 迪 值 条 件 ` 定 义 为 内 联 数
2 一 边 值 条 件 ， 定 义 为 内 ． 联 函 数
M ． 沿 轴 等 分 区 间 数
N ． 沿 t 轴 的 等 分 区 间 數
C ． 系 ． 数 ， 默 认 情 一 卜 C=I
％ 应 用 举 例 ：
%uX—I ； uT 《 M 50 ； N 50 ℃ 1 ． ；
%phi—inline('sin(pl*x)f);psi l—in il 淵 》 ； p $ i2 到 nlin 以 ' 0 生
％ 〔 0 x t]=PDEParab01icClassicallmplicit(uX,uT,phi,psil psi2,M,N,C);
％ 设 置 参 数 c 的 默 认 值
if nargin—•l
end
‰ 计 算 步 长
dx-uX.•M ， ％、 的 步 长
山 ： uT ； ％ 1 的 步 长
x—(0M)*dx;
t=(ON)*dt;
1 一 0 ／ ； ％ 步 长 比
D ros(l ， M 一 0 矩 阵 的 对 鱼 线 元 素
L 灬 一 灬 （ 1 ， M ． 2 } ， ％ 阵 的 下 对 角 线 元 素
U 灬 （ 1 ． M ． 2 ） ； ％ 矩 的 上 对 角 线 元 素
for i=l:M.2
Diag(i)—1+2*r;
end
Diag(M•l)=l+2*r•
％ 计 算 初 值 和 边 值
U ： 娌 ro $ （ M 斗 1 ， N + 0
for 种 上 M 到
cnd
fcjr j=I:N+l
0
0
U(lJj-psil(t(ij);
LJ { M + 0 ： 2 的
end
％ 逐 层 求 解 ， 需 要 使 川 追 赶 泓 （ 调 用 函 数 EqtsForwardAndBackward)
for j—I:N
bI=zeros(M-I, 性
bl(M-lj-r*U(M+Ri+l),
b—U(2 (j) 十 bl ，
U(2:Mj+1)•EqtsForwardAndBackward(Low.Diag,Up,b),
end
％ 作 出 图 形
mesh(x LU);
titl 虻 古 典 隐 式 格 式 ， 一 维 热 传 导 方 程 的 解 的 图 像 〕
b巛@阃 变 量 的
abcl （ ' 时 间 变 量 0
zlabe （ 冖 维 热 传 导 方 程 的 解 U)
压 山 r 瞓
此 算 法 需 呶 使 用 追 赶 法 求 解 三 对 角 线 性 方 程 组 ， 这 个 算 法 在 上 一 篇 軲 子 中 已 经 给 出 ， 为 了 方 便 ， 再 给 出 来
追 赶 法 解 0 对 角 线 性 方 程 组
function x—EqtsForward 、 AndBackward(L D,Utb)
％ 追 赶 法 求 解 三 对 角 线 性 方 程 组 Ax-b
%x=EqtsForwardAndBackward(L,D,U,b)
%x 过 对 角 线 性 方 程 组 的 解
％ L 三 对 知 阵 的 下 对 角 线 ， 行 向 量
％ D 对 角 詎 阵 的 对 角 线 ， ． 行 向 量
%U 三 对 角 矩 阵 的 上 对 角 线 ， 行 向 量
％ 线 性 方 程 组 Ax=b 中 的 b ， 列 向 量
％ 应 用 举 例 ．
%L-[•I ． 2 司 ， 上 〔 2 3 4 5 上 U ： 卜 I ． 2 ． 30 6 1 ． 2
%x—FAtsF0twardAndBaekward(L,D,U b)
％ 检 查 参 数 的 输 人 是 否 正 确
n=length(l)),m=length(b);
的 二 》 “ gth （ 0000 “ g 山 （ U } ：
if 0n1 ～ 冖
disp( 输 人 参 数 有 误 ！ 》
returlv
end
％ 追 的 过 程
订 i=2:n
L00 ： L00 以 i 、 0 ，
以 i) 一 L(i 一 1 尸@一
end
zero $ 0 ， 0
for i=2.-n
cnd
％ 赶 的 过 程
x 回 。 对 nV 0
对 i) ：0@．U （ 旷 种 到 0 耱
end
return;
占 典 隐 式 格 式
0
0
遜 咩 能 性 一 一 禹 0 導 0 鼕 ，
0
0 ；
在 以 后 的 程 序 中 ， 我 们 都 取 c=l ， 不 再 作 为 一 个 输 入 参 数 处 理
隐 式 格 式 求 解 鼬 物 型 偏 微 分 方 程
3 、 C n N 记 視 需 咖
需 要 调 用 追 赶 法 的 程 序
åünction IU x tl=PDEParaboIicCN(uX,uT phi,psiI,psi2,M,N)
%Ctank-NieoIson 隐 式 格 式 求 的 抛 物 型 偏 微 分 方 程
%[U x t]=PDEParab01ieCN(uX*11T,ph1,PSll p 2 M,N)
％ 方 和 ： u xx < uX ， 0 《 1 uT
％ 初 值 条 件 0 ： 种 i
％ 边 1 直 条 件 ： u@的 二@1@， u № 》 p (0
0
0
0
0
％ 输 出 参 数 ： U 矩 阼 ， 第 一 行 表 示 初 值 ， 第 一 列 和 最 后 一 列 表 示 边 直 ， 第 过 行 表 示 第 2 层 一
x ． 空 司 变 量
t ． 时 间 变 量
％ 输 入 参 数 ； ux 一 啊 司 变 量 x 的 取 值 上 限
uT ． 时 间 变 量 t 的 取 上 限
phl J 值 条 件 ， 定 义 为 内 联 函 数
0i1 ． 边 值 条 件 》 定 义 为 内 联 函 数
伊 i2 ． 边 值 条 件 ， 定 义 为 内 联 函 数
M 一 沿 轴 的 等 分 区 间 数
N ． 沿 t 轴 的 等 分 区 间 数
％ 应 用 举 例 ：
， ， X ： 丨 ； uT ： 2 ， M 干 50 ； N ： 50
%pht=inlineCsin(pi*xY),psi 1 ， psi2=inline(O);
%[U x t]=PDEParab01ieCN(uX,LIT ， ph10》 1 ， 2
％ 计 算 步 ． 长
dx=uX/M,%x 的 步 长
dt=uT 叭 ： ％ 1 的 步 长
1 ： ()N 了 山 ；
r=dt/d 对 dx ； ％ 步 长 比
Diag-zerosCl ， M ． 的 ； ％ 矩 阵 的 刈 的 线 元 素
l-ow=zeros(l ， M ． 以 ％ 庫 阵 的 下 对 角 线 元 素
Up “ 灬 出 M ． 2 ） ； ％ 矩 阵 的 上 对 角 线 元 素
for 《 ： M 一 2
Diag(i)=I+r,
Low(i)--rf2;
跏@一 02 ；
end
Diag(M-I)* +r;
％ 汁 算 初 值 和 边 值
U=zemos(M+I,N+I);
for 0 的 M 十 ]
cnd
for j••l :N+I
1J(1,j 、)—p巛@班
U@十 1 ， j 厂 的 2@0
end
B “ “ 对 M 一 1 ， M 一 0
for i=l:M.2
B(i,ij—l-r;
， i + 0 ： 在 2 ；
B （ i + 1 ， 0002 ；
end
B(M•I,M•I)=I 寸 ；
0
0
％ 逐 层 求 解 ， 需 要 雙 川 追 赶 泫 （ 调 用 数 EqtsFormrdAndBackward)
bI=zeros(M-1, 地
bl(l)=r*(U(lj+l)+U(l,j)Y2;
bl （ M 刁 0 气 以 M 到 ， j 到 ） 十 IJ （ M 十 1 出 V2 ；
U(2:M,j+l )—EqtsForwardAndBackward(Low Diag,Up,b);
end
％ 作 出 图 形
me 訃 1 ， 0 ；
title(Crank 、 Nicolson 式 格 式 ， 一 维 热 传 导 方 程 的 解 的 图 像 》
对 圹 空 阊 变 量 对
訃 el （ 时 间 变 量 0
zlabe 〔 一 维 热 传 导 方 程 的 解
压 山 rn ；
@CranA7icoIson 隐 式 格 式
． 上 0 一 丆 [ 《 00 、 「 上 剂 就 00
0 上 ，
0 ；
4 、 iE 方 形 区 域 卪 a “ 方 穆 Diriclet 同 题 的 求 解
需 要 调 用 Jacobi 迭 代 法 和 Guass-SeideI 迭 代 法 求 解 线 性 方 程 组
0
0
function IU x y]—PDEEIIipseSquareLaplaceDinch1et(ub,ph11,phi2,psil 卧 i2 ， M ， 0r0
％ 方 形 区 域 凵 卪 “ 方 程 的 mriclet 边 佰 同 题 的 差 分 求 解
％ 此 程 序 需 要 调 用 Jacobi 送 代 法 或 者 Guass-Seidel 迭 代 泫 求 解 线 骨 方 程 组
％@ x yJ=PDEEllipseSquarcLapIaceDirichlct(ub,phiI phi2,psiI ， i2 ， M 0
‰ 方 程 ． + 巧 厂 0 0 《 ， ：
％ 边 值 条 件 ； uLy)-phi l(y)
uCub,yj-phi2(y)
u （ & 过 bF1 “ i2 （ 对
％ 输 出 参 数 ： U ． 解 矩 阵 ， 第 一 行 表 示 厂 0 时 的 值 ． ， 第 行 表 示 厂 h 时 值 一
x 、 横 坐 标
Y 一 纵 标
％ 输 入 参 数 ： ub ． 变 量 边 界 值 的 上 限
phil,phi2,psil ,psi2 一 边 界 函 数 ， 定 ． 义 为 内 联 函 数
M ． 横 纵 坐 标 的 等 分 区 间 数
巧 ． 求 解 差 分 方 程 的 迭 代 格 式 ， 若 采 Jacobi 迭 代 格 式
若 type=GS', 采 用 Guass-Se1del 送 代 格 式 。 畎 认 情 况 下 ， 0 世 一 ℃ S '
％ 应 用 举 ：
0/oub—4;M=20;
%phiI—mIine(Y*(4-y)mphi2—inIineCO%),psi —inlin ' $ i 以 pi* 对 40 尹 $ i2—inIi 以 0 〕 ' } ；
%[U x yl=PDEEIIipseSquareLaplaceDirichlet(ub,phil p11i2 ， psiLpsi2 M,GS');
0 nargin==6
巧 世 。 GS ' ，
end
％ 步 长
h=ub!M
％ 横 纵 坐 标
％ 差 分 格 式 的 矩 阵 形 式 AU=K
％ 构 造 的 A
M2 ： （ M 山 0
A 一 z 亠 》 寸 M
for i=1:M2
A( 河 ： 4 ；
end
(c)f i=l:M2-
if mod 在 M 、 I) 一 、 。 0
A （ i01 产 ；
AO+I ， i01 '
end
end
for i— 上 M M 十 1
A(i i 十 M 司 》 刁 ；
0
0
AO+M 、 1 0 七
end
U=zeros()4 0
％ 边 值 条 曾
for 0 的 M 十 1
U 在 0邗巛@一 炉
U(i,M+lFpsi2((i- 炉
U(I ， i)=phil@一 1 严 0
U(M 十 0）一ph]2@．《产h）；
end
‰ 构 造 K
K “ 吓 （ M2 ， 0 ；
for i=l'M•l
K00U0 + 1 山
K012 与 + 0 ： U(i 到 ， M 刊
end
K （ M2 一 M12 》 K { M2 一 M ． 0 U 卩 ， ，
for 02 ： M 、 2
@（M山 气 i 山 + 0 一 卩 計 0 ；
坷 （ M ． l)*i) ： U01 + 1 0
end
x0 删 ne M2 ， 0 ；
switch 巧
0
0
％ 调 用 Guass-SeideI 选 代 法 求 解 线 且 方 程 组 AU K
“ 虻 tJacobl'
X—EqtsJacobi(A,K,x0),
％ 调 用 Guass-Setdel 迭 代 泫 求 解 线 性 方 程 组 AU=K
X=EqtsGS(A,K,x0);
， Ot 五 到 se
dis 的 差 分 格 式 类 型 输 人 错 误 〕
re.tur•n;
end
％ 把 求 解 结 果 化 成 短 阵 型 式
for i—2:M
for j=2:M
U { J ， i ） 一 X01 气 M 、 1 ， )*(i ． 2
end
U—U,
％ 作 出 图 形
me 訃 掣 0 ；
血 鳳 点 差 分 格 式 Laplace 方 程 DJriclet 问 题 的 解 的 图 ． 像 》
对 a 沅 IC 的
a 巧 e 旷 的
zlabel('Laplace 方 程 Diriclet 问 题 的 解 0
压 山 rn ；
乜 讵 方 形 区 域 Laplace 方 程 五 点 差 分 格 式
5 、 一 阶 双 的 型 方 程 的 差 分 方 法
function [U x tl"PDEHyperboIic(uX,uT,M,N,C,phi,psi 1,psi2,type)
％ 一 阶 双 曲 型 方 程 的 差 分 格 式
%[U x t]—PDEHyperboIic(uX,uT,M,N,C,phi,psil,psi2,typej
％ 方 程 ： u t+C*u x=0 0 < = t < ： uT, 0 < =
％ 初 值 条 件 ． u 区 0 } 叩 hi （ 对
％ 输 出 参 ， U 、 解 矩 阵 ， 第 一 行 表 示 初 值 ， 第 二 行 表 示 第 2 个 时 间 层 一
x 罪 坐 标
t 一 纵 坐 标 ， 时 阃
％ 输 入 参 数 ： ux 、 变 量 x 的 上 界
uT 一 变 量 《 的 上 界
M ． 变 量 x 的 等 分 区 间 数
N ． 变 量 t 的 等 分 区 间 数
c 孫
phi ． 初 值 条 付 函 数 ， 定 义 为 内 联 函 数
psil ,psi2 一 边 1 直 条 件 函 数 ， 定 义 为 内 联 函 数
帅 《 ． 差 分 格 式 ， 从 下 列 值 中 选 取
的 世 0 寸 ' 飛 d 彘 h 采 用 Lax-Friedrichs 差 分 格 式 求 解
以 卵 e 一 00t10n 小 翮 onR 就 采 用 Courant-Isaacson-Rees
． 巧 ： ' 上 “ pF “ g ' ， 采 用 Leap•Frog （ 鲢 跳 〕 差 分 格 式 求
-ope=LaxWendroff, 采 用 Lax W “ d 阉 差 分 ． 格 式 求 解
差 分 格 式 求 解
： 0 “ kN 5 耐 ， 采 用 差 分 格 式 求 解 ， 此 格 式 需 调 用 追 赶 法
求 解 三 对 角 线 骨 方 程 组
删 X,•M ， ％ 变 量 x 的 步 长
炉 u 的 N ； ‰ 变 量 的 步 长
。 k 山 ． ％ 步 长 比
U••zeros(M+1 ， N+0；
％ 初 值 条 件
for 汾 上 M 十 1
cnd
％ 边 值 条 件
fcjr j ： 上 N 斗 1
LJ(I ，jj-p司@毖
U01 + 1 ， j 片 卩 s 《 2@li));
%U(l,j)—NaN;
％ U01 + 1 ,j)=NaN,
end
1 师 e
%Lax-Friedrichs 差 分 格 式
case iLaxFriedrichsi
if 訃 s(C 孬 0 ： 刁
d 这 凶 001 ， Lax 丰 飛 d 小 h $ 差 分 格 式 不 稳 定 ！ 》
0
％ 逐 层 求 解
for i=2:M
U(i ， j + 1 ） 以 U(i + 10 还 （ 0 河 门 一 C 新 气 I-J （ i 到 0U0 一 1 ， 0 》 2 ；
end
%Courant-Isaacson-Rees 差 分 格 式
case CourantlsaacsonRees•
山 'C ， 采 用 前 差 公 式 〕
if C*r<-l
end
％ 逐 层 求 解
0 「 i=2:M
U(i,j + 10000 * U （ 卜 0 产 U(i + 10 ；
cnd
else
d 这 0 ． 0 采 用 后 差 公 式 〕
if C 寧 01
d 这 的 c 灬 an 《 小 皿 吓 “ 还 “ s 差 分 格 式 不 稳 定 ！ 》
LJ0,j + 100 产 00 地 ． 00m （ ijj;
cnd
％ 逐 层 求 解
for j= I:N
for 02M
cnd
end
0
0
0
%Leap-Frog 〔 蛙 跳 》 差 分 格 式
“ “ 'LeapFrog'
冲 i2 艹 甲 ut （ ' 请 输 人 第 过 层 到 值 条 件 函 数 ； pst2 刁 ；
if 訃 s(C 》 刁
d 这 凶 001 ， Leap-Frog 差 分 格 式 不 稳 定 1 〕
end
％ 第 过 层 ． 初 值 条 件
for 01 ： M + 1
U 在 2)=phi2 骁
end
％ 逐 层 求 解
for j—2N
for i=2:M
1J(i,j+l)=U0j-l)-C*r*(U(i+l,j)-l 丿 （0j就
end
end
%Lax-Wendrofi 、 差 分 格 式
凵 'LaxWendroff
评 abs(C•r)>1
d 这 的 001 ， 0 ～ w 《 ndr 。 0 差 分 格 式 不 稳 定 ！ 》
end
％ 逐 层 求 解
for i=2:M
U(i ， 010 00i 到 ． U （ 凵 j02 十 02 ． 0 （ U （ 汾 l,j 戽 U(l,j ） 十 U()- ,J 力 过 ；
end
end
%Crank-NicoIson 隐 式 差 分 恪 式 ， 需 调 用 追 赶 法 求 解 三 对 角 线 性 方 程 组 的 算 法
“ CrankNicolson
Diag- “ 灬 0 ． M 一 0 ‰ 矩 的 对 的 线 元
l-ow—zeros(l ， M ． 与 酆 阵 的 下 对 角 线 元 素
Up 一 ze 灬 卩 ， M ． 2 ） ； ％ 矩 阵 的 上 对 角 线 元 素
for 1 ： M ， 2
Diag(i)=4;
end
Diag(M-l)—4;
B=zeros(M-1 ， M 一 0
for i=lM.2
B(i ， i尸4；
B(i+l ， 00 产 C ；
end
B(M I ， M 山 到 ，
0
0
％ 逐 层 求 解 ， 需 要 使 川 追 赶 法 （ 调 川 所 E 下 。 ru dA " 戕 旧
」 ： 上 N
bl=zeros(M 1 ， 以
bl(l) “ ℃ 气 U(1,j + 0 + U(I 山 贮 ；
bl （ M 刁 0 的 0 （ U （ M+I ， j 十 10U （ M 到 0 理 ；
b=B*U(2:M,j)+bI;
U(2:M,j+l)—EqtsForwardAndBackward(Low,Diag,Up,b),
end
． ． 然 孥 诔 e
d 这 p 《 差 分 格 式 头 型 输 入 有 误 ！ 》
return;
end
％ 作 出 图 形
1 ， 0 ；
血 0 赆 ' 格 式 求 解 一 阶 双 曲 型 方 程 的 解 的 图 像 肛
对 ab 0 阎 变 量 妁 ，
y 《 訃 cl （ 时 间 变 量 0
zlabe 〔 一 阶 双 曲 是 方 程 的 解 蚴 ，
压 山 rn ；
0
0
