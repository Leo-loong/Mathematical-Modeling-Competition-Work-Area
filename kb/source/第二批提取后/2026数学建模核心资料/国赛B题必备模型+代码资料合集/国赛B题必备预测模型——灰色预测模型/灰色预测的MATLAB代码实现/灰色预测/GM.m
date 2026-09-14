% 灰色预测步骤
% 判断数据是否适合灰色预测
% 求累积和（后面的均值序列求的是累积和的均值）
% 求均值序列
% 利用原始数据和均值序列，求参数a和u
% 对累积和的结果进行预测，得到预测累积和
% 累减得到实际的预测值

clc
clear

x0=[174 179 183 189 207 234 220.5 255 270 285];
%输入原序列

n=length(x0);
rank_ratio=zeros(1,n-1);

for i=2:n
    rank_ratio(i-1)=x0(i)/x0(i-1);
end

% 使用灰色预测的前提条件，待研究
if (all(rank_ratio>=exp(-2/(n+1)))&&all((rank_ratio<=exp(2/(n+1)))))
    fprintf('\n')
    disp('此序列适合GN（1，1）模型')
    fprintf('\n')
else
    disp('此序列不适合GN（1，1）模型')
end

x=cumsum(x0); %原序列做累加处理
B=zeros(1,n-1);

%产生均值序列
for i=1:n-1
    B(1,i)=(x(1,i)+x(1,i+1))/2;
end

B=[-B;ones(1,n-1)];
B=B';
Y=x0;
Y(1)=[];
Y=Y';

%最小二乘法求参数
a=inv(B'*B)*B'*Y;   % inv  矩阵求逆，此处求的a即为原理介绍里的U
F=zeros(1,20);
F(1)=x0(1);

for i=2:n+10
    F(i)=(F(1)-a(2,1)/a(1,1))*exp(-a(1,1)*(i-1))+a(2,1)/a(1,1);
end                  %计算预测后累加序列

G=zeros(1,20);
G(1,1)=x0(1,1);

for i=2:n+10
    G(i)=F(i)-F(i-1);
end                 %计算预测值

disp('输出预测值');
G

%相对误差检验
D=G(1,1:10);
res=abs(D-x0);%相对误差序列
rel_rate=res./x0;
rel_rate=mean(rel_rate);%计算相对误差

if rel_rate<=0.01
    disp('相对误差检验结果很好');
elseif rel_rate<=0.05
    disp('相对误差检验结果合格');
elseif rel_rate<=0.1
    disp('相对误差检验结果勉强合格');
end

fprintf('\n相对误差rel_rate=%4f\n\n',rel_rate);

%后验差检验
x0_mean=mean(x0);%原始序列均值
x0_std=std2(x0);%原始序列均方差
res_mean=mean(res);%残差序列均值
res_std=std2(res);%残差序列均方差
c=res_std/x0_std;%计算后验差比
s0=0.6745*x0_std;
e=abs(res-res_mean);
P=length(find(e<s0))/length(e);%计算小误差概率

if (c<=0.35&&P>=0.95)
    disp('后验差检验结果好');
end

if(c>0.35&&c<=0.5&&P>=0.8&&P<=0.95)
    disp('后验差检验合格');
end

if(c>0.5&&c<=0.65&&P>=0.7&&P<0.8)
    disp('后验差检验勉强合格');
end

fprintf('\n后验差比c=%4f\n',c);
fprintf('\n小误差概率P=%4f\n\n',P);

%关联度检验
abs_ss=D-x0;%绝对误差序列
k=(min(abs_ss)+0.5*max(abs_ss))./(abs_ss+0.5*max(abs_ss));

%计算关联系数
kk=mean(k);%计算平均 关联系数
if (abs(kk)>0.6)
    disp('关联度检验结果良好');
else
    disp('关联度检验不合格');
end

fprintf('\n关联度为%f\n\n',kk);

%残差检验
f=abs(D-x0)./x0;%残差序列
if (all(f<0.1))
    disp('残差检验结果好');
elseif(all(f<0.2))
    disp('残差检验结果合格');
end

P0=1-sum(f)/(n-1);
fprintf('\n本次建模精度P0=%f\n',P0);


