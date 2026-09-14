
%获取样本数据

%获取样本数据
data=xlsread('yumi.xlsx','Sheet1','A2:H727');
high=xlsread('yumi.xlsx','Sheet1','B2:B727');
low=xlsread('yumi.xlsx','Sheet1','C2:C727');
close=xlsread('yumi.xlsx','Sheet1','D2:D727');
open=xlsread('yumi.xlsx','Sheet1','E2:E727');
average=xlsread('yumi.xlsx','Sheet1','F2:F727');
volume=xlsread('yumi.xlsx','Sheet1','G2:G727');
positions=xlsread('yumi.xlsx','Sheet1','H2:H727');
date=xlsread('yumi.xlsx','Sheet1','A2:A727');
lead=cell(1,5);
lag=cell(1,5);
scrsz=get(0,'ScreenSize');
figure('Position',[scrsz(3)*1/4 scrsz(4)*1/6 scrsz(3)*4/5 scrsz(4)]*3/4);
MT_candle(high,low,close,open,'r',date);
xlim([1 length(date)]);
hold on;
for i=1:5
    [lead{i},lag{i}]=movavg(close,i*3-2,i*9-6,'e');
    plot(lead{i},'Color',[i/5,0,0]);
    plot(lag{i},'Color',[0,0,i/5]);
    grid on
end
title('5组不同时间长度的移动平均线展示','FontWeight','Bold');