%% 清空环境变量
clc;
clear all
close all
nntwarn off;
%% 数据载入
aa=xlsread('test.xls','sheet3','a1:a41');
lag=4;    % 自回归阶数
iinput=aa; % x为原始序列（行向量）
n=length(iinput);
%准备输入和输出数据
inputs=zeros(lag,n-lag);%产生log行n-log列的元素为0的矩阵,因为是两阶的。所以是两个数据预测第三个数据。
for i=1:n-lag
    inputs(:,i)=iinput(i:i+lag-1)';
end
targets=aa(lag+1:end);
targets=targets';%将目标矩阵转置，与inputs矩阵对应使两个矩阵列数相等(与原始数据是横还是列数据有关)
%创建网络
hiddenLayerSize = 10; %隐藏层神经元个数
net = fitnet(hiddenLayerSize);%以隐藏层神经元的个数来建立网络
% 避免过拟合，划分训练，测试和验证数据的比例
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

%训练网络
[net,tr] = train(net,inputs,targets);%trian训练函数，trian（网络结构，输入数据，对应的目标数据）
%% 根据图表判断拟合好坏
yn=net(inputs);
errors=targets-yn;
figure, ploterrcorr(errors)                      %绘制误差的自相关情况（20lags）
figure, parcorr(errors)                          %绘制偏相关情况
%[h,pValue,stat,cValue]= lbqtest(errors)         %Ljung－Box Q检验（20lags）
figure,plotresponse(con2seq(targets),con2seq(yn)) %看预测的趋势与原趋势
%figure, ploterrhist(errors)                      %误差直方图
%figure, plotperform(tr)                          %误差下降线
%% 下面预测往后预测几个时间段
fn=10;  %比如预测步数为fn。
f_in=iinput(n-lag+1:end);%原来给出的数据末尾几个数据作为预测的开始输入，具体是几个数据与自回归阶数log有关，log是几就以多少个末尾数据作为预测的输入。f_in=iinput(n-lag+1:end)';加不加转置与所给的数据是横还是列有关
f_out=zeros(1,fn);  %预测输出
% 多步预测时，用下面的循环将网络输出重新输入

for i=1:fn
    f_out(i)=net(f_in);
    f_in=[f_in(2:end);f_out(i)];
end
% 画出预测图
figure,plot(1:n,iinput,'b-s',n:n+fn,[iinput(end),f_out],'r-d')