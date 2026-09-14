
%%3周预测一周
addpath farutoUltimateVersion2[1].0;

%% 清空环境变量
clear all
clc
close all

load data.mat;
i=2;
rain1=data(1:645,i);
rain2=data(2:646,i);
rain3=data(3:647,i);
rain4=data(4:648,i);

train1=[rain1,rain2,rain3];
test1=rain4;

p_train=train1(1:585,:);
t_train=test1(1:585,:);

p_test=train1(586:645,:);
t_test=test1(586:645,:);


%% 数据归一化

% 训练集
[pn_train,inputps] = mapminmax(p_train');
pn_train = pn_train';
pn_test = mapminmax('apply',p_test',inputps);
pn_test = pn_test';
% 测试集
[tn_train,outputps] = mapminmax(t_train');
tn_train = tn_train';
tn_test = mapminmax('apply',t_test',outputps);
tn_test = tn_test';

%% SVM模型创建/训练


bestc = 10;
bestg = 2;

% 创建/训练SVM  
cmd = [' -t 2',' -c ',num2str(bestc),' -g ',num2str(bestg),' -s 3 -p 0.01'];
model = svmtrain(tn_train,pn_train,cmd);

%% SVM仿真预测
[Predict_1,error_1] = svmpredict(tn_train,pn_train,model);
[Predict_2,error_2] = svmpredict(tn_test,pn_test,model);
% 反归一化
predict_1 = mapminmax('reverse',Predict_1,outputps);
predict_2 = mapminmax('reverse',Predict_2,outputps);
% 结果对比
result_1 = [t_train predict_1];
result_2 = [t_test predict_2];

% %% 绘图
% figure(1)
% plot(1:length(t_train),t_train,'r-*',1:length(t_train),predict_1,'b:o')
% grid on
% legend('真实值','预测值')
% xlabel('样本编号')
% ylabel('耐压强度')
% string_1 = {'训练集预测结果对比';
%            ['mse = ' num2str(error_1(2)) ' R^2 = ' num2str(error_1(3))]};
% title(string_1)
% figure(2)
% plot(1:length(t_test),t_test,'r-*',1:length(t_test),predict_2,'b:o')
% grid on
% legend('真实值','预测值')
% xlabel('样本编号')
% ylabel('耐压强度')
% string_2 = {'测试集预测结果对比';
%            ['mse = ' num2str(error_2(2)) ' R^2 = ' num2str(error_2(3))]};
% title(string_2)

%% BP 神经网络

% 数据转置
pn_train = pn_train';
tn_train = tn_train';
pn_test = pn_test';
tn_test = tn_test';
% 创建BP神经网络
net = newff(pn_train,tn_train,10);
% 设置训练参数
net.trainParam.epcohs = 1000;
net.trainParam.goal = 1e-3;
net.trainParam.show = 10;
net.trainParam.lr = 0.1;
% 训练网络
net = train(net,pn_train,tn_train);
% 仿真测试
tn_sim = sim(net,pn_test);
% 均方误差
E = mse(tn_sim - tn_test);
% 决定系数
N = size(t_test,1);
R2=(N*sum(tn_sim.*tn_test)-sum(tn_sim)*sum(tn_test))^2/((N*sum((tn_sim).^2)-(sum(tn_sim))^2)*(N*sum((tn_test).^2)-(sum(tn_test))^2)); 
% 反归一化
t_sim = mapminmax('reverse',tn_sim,outputps);
% 绘图
figure(3)
plot(1:length(t_test),t_test,'r-*',1:length(t_test),t_sim,'b:o',1:length(predict_2),predict_2,'g:+')
grid on
legend('真实值','BP预测值','svm')

% string_3 = {'测试集预测结果对比(BP神经网络)';
%            ['mse = ' num2str(E) ' R^2 = ' num2str(R2)]};
% title(string_3)
