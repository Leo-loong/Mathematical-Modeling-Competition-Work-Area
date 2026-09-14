high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');
%寻找模型中最优的滑窗window的大小
Train=cell(1,2);
Train{1}=train(1:end-1,:);
Train{2}=Train2(1:end-1,:);

bestc=cell(1,2);
bestc{1}=bestc1;
bestc{2}=bestc2;
bestg=cell(1,2);
bestg{1}=bestg1;
bestg{2}=bestg2;
window=cell(1,2);
bestaccurate=cell(1,2);
strtemp={'{以价量信息为样本属性集合}','{以技术指标为样本属性集合}'};


%窗口设定的范围为:x-y 天
for i=1:2
    [bestaccurate{i},window{i},Accurate,xlab]=Bestwindow(Label,Train{i},bestc1,bestg1,15,65);
    [bestaccurate{i},window{i},Accurate,xlab]=Bestwindow(Label,Train{i},bestc{i},bestg{i},15,65);
 scrsz=get(0,'ScreenSize');
 figure('Position',[scrsz(3)*1/4 scrsz(4)*1/6 scrsz(3)*4/5 scrsz(4)]*3/4);
 plot(xlab,Accurate,'-*');
 xlabel('滑窗的长度');
 ylabel('准确度');
 title(['最优的滑窗长度=',num2str(window{i}),',最佳准确率=',num2str(bestaccurate{i}),strtemp{i}],'FontWeight','Bold');
 grid on
 hold on
 scatter(window{i},bestaccurate{i},'MarkerFaceColor',[1 0 0],'Marker','Square');
 hold off
end