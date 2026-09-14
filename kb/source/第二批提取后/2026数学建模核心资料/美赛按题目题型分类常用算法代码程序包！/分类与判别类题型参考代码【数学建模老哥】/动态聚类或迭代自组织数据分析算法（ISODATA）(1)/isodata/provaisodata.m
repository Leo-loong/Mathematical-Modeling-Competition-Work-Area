clear all
close all
clc
load('\dades.mat')
ON=15;  %一个聚类中最少样本 
OC=7;   %两聚类中心之间的最小距离.
OS=12;  %一个聚类域中样本距离分布的标准差.
k=8;    %期望得到的聚类数.
L=2;    %一次迭代运算中可以合并的聚类中心的最多对数.
I=60;   %允许迭代的次数.
NO=1;   
min=50;  
 
[centro, Xcluster, Ycluster, A, clustering]=isodata(X, Y, k, L, I, ON, OC, OS, NO, min);
clc;
fprintf('Numero de agrupaciones: %d',A);

 

%  颜色
colr=zeros(A,3);
for i=1:A
    colr(i,:)=rand(1,3);
end;
%显示
 
figure;
hold on;
for i=1:A,
    n=find(clustering==i);
    p=plot(X(n), Y(n),'.');set(p,'Color',colr(i,:));title(A)
end;

 
clc;
fprintf('Numero de agrupaciones: %d',A);
 
clear n;clear i;clear p;clear colr;clear NO;