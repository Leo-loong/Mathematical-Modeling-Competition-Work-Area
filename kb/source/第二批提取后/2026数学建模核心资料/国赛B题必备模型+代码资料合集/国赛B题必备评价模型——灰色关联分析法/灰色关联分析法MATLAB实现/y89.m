high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');
%对两种模型进行回测检验
P_S=cell(1,2);
R_S=cell(1,2);
r=cell(1,2);
cumr=cell(1,2);
benchmark=cell(1,2);
x=cell(1,2);
ret=cell(1,2);
Maxdrawdown=cell(1,2);
dd=cell(1,2);
for i=1:2
    %交易信号确认
    [P_S{i},decvalues]=SVMforecast(Label,Train{i},bestc{i},bestg{i},window{i});
    %P_S为算法预测信号
    R_S{i}=Label(1+window{i}:end-1,:);%R_S为真实交易信号
    title(['以价量信息为样本属性集合构建的SVM模型']);
    
    %预测信号与实际信号对比
    Signal=[P_S{i} R_S{i}];
    Signalforcast(P_S{i},R_S{i})
    %每笔盈利及累计收益计算
    r{i}=[0;P_S{i}.*(close(window{i}+2:end-1,1)-close(window{i}+1:end-2,1));];
    %每笔收益
    title(['以技术指标为样本属性集合构建的SVM模型']);
end
