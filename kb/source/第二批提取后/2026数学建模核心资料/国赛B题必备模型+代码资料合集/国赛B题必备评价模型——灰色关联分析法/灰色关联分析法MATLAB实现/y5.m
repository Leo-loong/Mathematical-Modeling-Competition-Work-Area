data=xlsread('yumi.xlsx','Sheet1','A2:H727');
high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');
Train=data';
[Train,Train_ps]=mapminmax(Train);%归一化
train=Train';
Train1=train(2:end,:);
%模型预测

[predict_label1,accuracy1,dec_values1]=svmpredict(Label,Train1,model,'-b 1');
roc_label1(Label>=0)=1;
Train_Signal=cell(1,5);
for i=1:5
    Train_Signal{i}(lead{i}>=lag{i})=1;%买(多头)
    Train_Signal{i}(lead{i}<lag{i})=-1;%卖(空头)
end

Train2=cell2mat(Train_Signal);
Train2=reshape(Train2,726,5);
%模型预测
[predict_label2,accuracy2,dec_values2]=svmpredict(Label,Train2(2:end,:),model,'-b 1');
roc_label2(Label>=0)=1;
%ROC曲线对比
roc_label=[roc_label1;roc_label2];
dec_values=[dec_values1(:,1)'; dec_values2(:,1)'];
scrsz=get(0,'ScreenSize');
figure('Position',[scrsz(3)*1/4 scrsz(4)*1/6 scrsz(3)*4/5 scrsz(4)]*3/4);
plotroc(roc_label1,dec_values);