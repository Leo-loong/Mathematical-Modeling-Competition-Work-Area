
%获取样本数据

%获取样本数据
high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');

Train_Signal=cell(1,5);
for i=1:5
    Train_Signal{i}(lead{i}>=lag{i})=1;%买(多头)
    Train_Signal{i}(lead{i}<lag{i})=-1;%卖(空头)
end

Train2=cell2mat(Train_Signal);
Train2=reshape(Train2,726,5);
%g,c参数寻优
[bestmse2,bestc2,bestg2]=SVMcgForClass(Label,Train2(2:end,:),-10,10,-10,10,5,0.5,0.5,0.5);
cmd2=['-c',num2str(bestc2),'-g',num2str(bestg2) '-b',num2str(1)];
cmd2
%模型建设，训练SVM网络
model=svmtrain(Label,Train2(2:end,:),cmd2);
%模型预测
[predict_label2,accuracy2,dec_values2]=svmpredict(Label,Train2(2:end,:),model,'-b 1');
roc_label2(Label>=0)=1;
