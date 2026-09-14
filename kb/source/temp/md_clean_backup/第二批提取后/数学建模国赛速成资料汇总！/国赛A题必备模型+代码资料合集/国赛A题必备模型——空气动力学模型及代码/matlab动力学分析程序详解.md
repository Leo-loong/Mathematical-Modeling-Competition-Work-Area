I. 微 分 方 程 的 定 义
对 于 dufftng 方 程 + 无
． = 攴 2
攴
= 0 ， 先 将 方 程 写 作
X
2
3
—CD 一 无 1
func t ion dy=duffing(), x)
omega= 1 ； ％ 定 义 参 数
f 1 = x （ 2 ） ；
f2=-omega 2*x(l)-x (l) 一 3 ；
dy±[fl ； f2] ；
2 ． 微 分 方 程 的 求 解
funct i on 50h ℃ (tstop)
tst 。 p 一 500 ， ％ 定 义 时 间 长 度
y0= [ 0 ． 01 ； 0 ] ； ％ 定 义 初 始 条 件
Ct, 到 一 0de45 (' duffing' ， tstopt 、 0 [ ] ） ：
funct i on solve (tstop)
$ tep=0. 01 ， ％ 定 义 步 长
y0=rand 0 ， 2 ） ： ％ 随 机 初 始 条 件
tspan=C0:step•500] ： ％ 定 义 时 间 范 围
Ct, 到 ： 0de45 (' dufflng' ， t (0) ；
3 ` 时 间 历 程 的 绘 制
时 间 历 程 横 轴 为 t ， 纵 轴 为 Y ， 绘 制 时 只 取 稳 态 部 分 。
plot(), y （ ： ， I)) 绘 制 的 时 间 历 程
xlabel （ ' t' ） ％ 横 轴 为 t
ylabel （ ， yt 纵 轴 为 Y
gri 山 ％ 显 示 网 格 线
axis(C460 500 一 1 n f lr 的 ） ％ 图 形 显 示 范 围 设 置
4 ． 相 图 的 绘 制
相 图 的 横 轴 为 Y ， 纵 轴 为 dy/dt ， 绘 制 时 也 只 取 稳 态 部 分 。 红 色 部 分
表 示 只 取 最 后 10m 个 点 。
plot (y(end-1000 l) ， y (end-1000:end, 2 月 ； ％ 绘 制 Y 的 时 间 历
程
xlabel (' y' ） ％ 横 轴 为 Y
ylabel （ ' dy/dt' 纵 轴 为 dy/dt
gri 山 ％ 显 示 网 格 线
5 .Poincare 映 射 的 绘 制
对 于 不 同 的 系 统 ， Poincare 截 面 的 选 取 方 法 也 不 同
对 于 自 治 系 统 一 般 每 过 其 对 应 线 性 系 统 的 固 有 周 期 ， 截 取 一 次
对 于 非 自 治 系 统 ， 一 般 每 过 其 激 励 的 周 期 ， 截 取 一 次
例 程 duffing 方 程 十 攴 十 x 一 0 的 poincare 映 射
func t i on poincare (tstop)
global omega ；
omega= 1 ，
T ： 2 * pi / 。 mega ； ％ 线 性 系 统 的 周 期 或 激 励 的 周 期
step 一 T / 1 佣 ， ％ 定 义 步 长 为 T ／ 100
y0 一 [ 0 ， 01 ； 0 ] ； ％ 初 始 条 件
tspan=C0:step: 1 開 * T ] ； ％ 定 义 时 间 范 围
[t, yl =ode45C duffing' ， tspan, yO ） ，
for i = 5000 ： 100 ： 1 佣 00 ％ 稳 态 过 程 每 个 周 期 取 一 个 点
hold on ； ％ 保 留 上 一 次 的 图 形
end
xlabel （ ， y' ） ;ylabel （ ， dy/dt ' ）
Poincare 映 射 也 可 以 通 过 取 极 值 点 得 到
funct 1 on PO 1 ncare (tstop)
y0 ： [ 0 ． 01 ;0)
tspan=CO:0 、 01 “ 500 ] ：
Ct, 到 =od e45 C duffing' ， t spant (0) 和
count=find(t>100) ； ％ 截 取 稳 态 过 程
YZY (coun t ， ： ） ；
n=length (y(:, D ） ； ％ 计 算 点 的 总 数
for i 2 .n—l
if y(i-l, l)+eps<y(i, l) & & y(), l)>y(i+l, l)+eps ％ 简 单 的 取 出
局 部 最 人 值
plot(y(l, y 0 ， 2), '
h01 d on
end
end
xlabel C y' ） ;ylabel C dy/dt' ） ；
6 ． 频 谱
yy=fft (y （ end 一 1000 end, I)) ：
N=Iength (yy) ；
power=ab s (yy) ，
freq= .N—l)*l/step/N,
plot (freq （ 1.N/2), power （ 1 :N/2)) ；
xlabel （ ' f(y) ' ）
yl 楠 el （ ' y' ）
7 ． 算 例
duff i ng 方 程 、 + 攴 +
= 0 的 时 间 历 程 ，
相 图 ，
频 谱 和 poincare
映 射 。
function dy=duffing(), x)
omega=l ； ％ 定 义 参 数
f2=—omega 一 2*x (l)-x (l) 一 3 ；
dy= Cfl ； f2] ；
funct i on duffsim （ tsto
s tep=O 、 1
tspan=CO ： step ： 500
Ct, 到 二 0de45 (' duffing' ， tspan, (0) ；
subpl ot （ 2 ， 2 ， l)
plot(), y （
， l)) ： ％ 绘 制 Y 的 时 间 历 程
xlabel C t' 横 轴 为 t
ylabel （ ' y' 纵 轴 为 Y
gT 、 id ； ％ 显 示 网 格 线
“ is （ [ 460 500 -lnf lnf 的 ％ 显 示 范 围 设 置
subplot （ 2 ， 2 ， 2 ）
plot (y(end-1000 l), y (end-1000:end, 2 月 ； ％ 绘 制 Y 的 时 间 历
xlabel （ ' y' ） ％ 横 轴 为 Y
ylabel （ ' dy/dt' ） ％ 纵 轴 为 dy/dt
grid ： ％ 显 示 网 格 线
subpl ot （ 2 ， 2 ， 3 ）
yy=fft (y （ end 一 1000 end, I)) ；
N=Iength (yy) ；
power=ab s (yy) ；
fT 、 eq= 0 :N"I) 1 /st ep/N ，
plot (freq 〔 1 、 N/2 ） ， （ 1 .N/2)) ：
对 a № 1 （ ， f (y) ' ）
ylabel C y' ）
subpl ot （ 2 ， 2 ， 4 ）
count=find(t>100) ， ％ 截 取 稳 态 过 程
y=y (count, ： ） ；
n=length (Y(•
。 1)) ； ％ 计 算 点 的 总 数
for i 二 2 :n—l
讠 f y(i 一 1 ， l) ps 〈 y （ 1 ， l) & & y(), l) 〉 y （ 01 ， D 斗 eps ％ 简 单 的 取 出
局 部 最 大 佰
0 山 01d on ，
end
end
xlabel （ ' y' ,ylabel （ ' dy/dt' ） ，
刁 、 05
1
470
40
0
& 分 岔 图 的 绘 制
•O.OS
0 《 0
0 ． 05 ．
0 ． 15
0 2
+ 0 ． 3 戈 一 + x 一 丆 cosl.2t 随 丆 变 化 的 分 岔 图 。
func t ion dy=duffing(), x)
g ] ℃ ba 1 0
omega= 1 ； ％ 定 义 参 数
fl=x （ 2 ） ，
f2=omega 、 2 * x (I) -x (l) 一 3 一 0 、 3*x （ 2 ） +c*co s (). 2*t) ；
dy=[fl ； f2] ；
clear;
g 1 obal c ； ％ 定 义 个 局 变 量
range= [ 0 ． 1 ： 0 ． 002 ： 0 ． 9 ] ； ％ 定 义 参 数 变 化 范 围
YY= [ ] ； ％ 定 义 空 数 组
for c=range
y0 ： [ 0 ． 1 ； 0 ] 初 始 条 件
k=k+ I ，
tspan=CO:0 、 01 400 ] ；
Ct, 到 ： 0de45 (' duffing' ， t span, (0) 和
count=f1nd(t>200) ；
Y=Y ount ， ： ） ；
n=length (Y 0 ， l) ） ；
for i=2 ． n—l
l)+eps ％ 简 单 的 取 出
， 局 部 最 大 值 。
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
随 F 变 化 的 分 岔 图
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
