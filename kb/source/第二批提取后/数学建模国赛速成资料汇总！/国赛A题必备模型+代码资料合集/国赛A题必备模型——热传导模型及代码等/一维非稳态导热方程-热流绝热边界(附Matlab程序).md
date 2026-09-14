<!-- 第 1 页 -->
function oned
% 根据网上一维算例改了下边界条件，边界条件为绝热和恒定热流
% by hxg
clear all;clc;
%%%%%%%%%%%%%
%需要输入的物性参数
Lambda=10;%导热系数
cp=440;%热容
rou=7800;%密度
qw=500000;%壁面热流
%%%%%%%%%%%%%
a=Lambda/rou/cp;%定义中间系数
c=qw/Lambda;%定义中间系数
xspan=[0 0.012];%轴向坐标起止位置
tspan=[0 10];%仿真时间起止
ngrid=[1000 20];%空间网格数和时间网格数
%%%%%%%%%%%%%
%调用子函数
[T,x,t]=rechuandao(a,c,xspan,tspan,ngrid);
%画图
[x,t]=meshgrid(x,t);
figure(1)
mesh(x,t,T);
xlabel('x')
ylabel('t')
zlabel('T')

function [U,x,t]=rechuandao(a,c,xspan,tspan,ngrid)
% 热传导方程：
% Ut(x,t)=c^2*Uxx(x,t)  a<x<b  ts<t<tf
%一维非稳态导热方程
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

<!-- 第 2 页 -->
k=range(tspan)/(n-1);
t=linspace(tspan(1),tspan(2),n);

r=a*k/h^2;%%
if r>0.5
error('为了保证算法的收敛，请增大步长h 或减小步长k!')
end

%两个中间系数
s=1-2*r;
s2=c*h;
U=zeros(ngrid);%初步赋初值

% 初值条件，给了一个均温场
U(1,:)=20;

% 差分计算
for j=2:n
for i=2:m-1
U(j,i)=s*U(j-1,i)+r*(U(j-1,i-1)+U(j-1,i+1));
end
%%%%%%%下面是边界条件
U(j,1)=s2+U(j-1,2);%定热流边界条件
U(j,m)=U(j,m-1);%绝热边界条件
end
