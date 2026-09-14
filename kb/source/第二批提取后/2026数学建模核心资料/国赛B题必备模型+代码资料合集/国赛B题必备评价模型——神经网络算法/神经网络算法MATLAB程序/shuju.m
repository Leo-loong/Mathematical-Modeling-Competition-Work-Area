%%
clc
clear
close all
tic
%% 提取已有分类数据?
load data1 c1
load data2 c2
load data3 c3
load data4 c4
kd=4;
c=cell(1,kd);
% for i=1:kd
%     c{i}=xlsread(['data',num2str(i),'.xlsx']);
% end
c{1}=c1;c{2}=c2;c{3}=c3;c{4}=c4;
test0=c{2}(3:4,2:end);

%% 四个特征值矩阵合成一个矩阵
[rows,lines]=size(c{1});
data=[];
for i=1:kd
 data=[data;c{i}(1:rows,:)];
end
[output_fore0,modelrightridio,MCC]=shenjingnet1(data,kd,test0)
toc