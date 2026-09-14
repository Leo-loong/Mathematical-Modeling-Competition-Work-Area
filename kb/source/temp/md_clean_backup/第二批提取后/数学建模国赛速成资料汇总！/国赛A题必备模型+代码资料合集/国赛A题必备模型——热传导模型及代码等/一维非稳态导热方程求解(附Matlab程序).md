<!-- 第 1 页 -->
使用差分方法求解下面的热传导方程

# T x t( , )  a T2 ( , )x t (0  x 1, 0 t 0.2,a 1)
t xx

#### 初值条件： T x( ,0)  4x  4x2 ；

#### T (0, )t  0
边值条件： ；

#### T (1, )t  0
使用差分公式

#### T x(  h t, )  2 ( , )T x t  T x(  h t, ) T  2T T

#### T ( , )x t  i j i j i j  O h( 2)  i1, j i j, i1, j

#### xx i j h2 h2

#### T x t( ,  k) T x t( , ) T T

#### T x t( , )  i j i j  O k( )  i j, 1 i j,

#### t i j k k
上面两式带入原热传导方程

#### T T T  2T T

#### i j, 1 i j,  i1, j i j, i1, j

#### k h2

#### 4 k2

#### 令 r  ，化简上式的

#### h2

# T  (1 2 ) r T  r T( T )
i j, 1 i j, i1, j i1, j
如下图：

### T
i j, 1

## rT  (1 2 ) i j r T rT 
i 1, j , i 1, j

#### jt

#### ix

<!-- 第 2 页 -->
编程MATLAB 程序，运行结果如下

1

### 0.8

### 0.6

T

### 0.4

### 0.2

0

### 0.2

## 0.15 1

### 0.8

### 0.1

### 0.6

## 0.05 0.4

### 0.2

# 0 0
t
x

function mypdesolution
c=1;
xspan=[0 1];
tspan=[0 0.2];
ngrid=[100 10];
f=@(x)4*x-4*x.^2;
g1=@(t)0;
g2=@(t)0;
[T,x,t]=rechuandao(c,f,g1,g2,xspan,tspan,ngrid);
[x,t]=meshgrid(x,t);
mesh(x,t,T);
xlabel('x')
ylabel('t')
zlabel('T')

function [U,x,t]=rechuandao(c,f,g1,g2,xspan,tspan,ngrid)
% 热传导方程：
% Ut(x,t)=c^2*Uxx(x,t)  a<x<b  ts<t<tf
% 初值条件：
% u(x,0)=f(x)

<!-- 第 3 页 -->
% 边值条件：
% u(a,t)=g1(t)
% u(b,t)=g2(t)
%
% 参数说明
% c：方程中的系数
% f：初值条件
% g1,g2：边值条件
% xspan=[a,b]：x 的取值范围
% tspan=[ts,tf]：t 的取值范围
% ngrid=[n,m]：网格数量，m 为x 网格点数量，n 为t 的网格点数量
% U：方程的数值解
% x,t：x 和t 的网格点
n=ngrid(1);
m=ngrid(2);
h=range(xspan)/(m-1);
x=linspace(xspan(1),xspan(2),m);
k=range(tspan)/(n-1);
t=linspace(tspan(1),tspan(2),n);

r=c^2*k/h^2;
if r>0.5
error('为了保证算法的收敛，请增大步长h 或减小步长k!')
end
s=1-2*r;

U=zeros(ngrid);

% 边界条件
U(:,1)=g1(t);
U(:,m)=g2(t);

% 初值条件
U(1,:)=f(x);

% 差分计算
for j=2:n
for i=2:m-1
U(j,i)=s*U(j-1,i)+r*(U(j-1,i-1)+U(j-1,i+1));
end
end

%%%%%%本文来自互联网%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
