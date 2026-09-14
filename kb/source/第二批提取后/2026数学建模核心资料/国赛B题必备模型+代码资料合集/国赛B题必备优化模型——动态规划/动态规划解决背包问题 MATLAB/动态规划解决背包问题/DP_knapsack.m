clear all;
clc;
%% 初值设置
v=[90 75 83 32 56 31 21 43 14 65 12 24 42 17 60];
w=[30 27 23 24 21 18 16 14 12 10 9 8 6 5 3];
C=120;        %背包容量

%% 动态规划
if length(v)~=length(w)
    disp('输入的向量v与w长度不等');
end
n=length(v);  %物品数量
m=zeros(n,C+1);%建立二维数组
sum_W=0;
product_N=[];
%i指第i个物体，j指背包容量
for j=0:C
    if j>=w(1)
        m(1,j+1)=v(1);
    end
end  %初始化第一行，数组编码从1开始，因此下标要加1
for i=2:n
    for j=1:C
        if j>=w(i)  %背包可以装下当前物体
            m(i,j+1)=max(m(i-1,j+1),m(i-1,j-w(i)+1)+v(i));%1.不装 2.空出刚好可以放进去的容量
        else
            m(i,j+1)=m(i-1,j+1);%容量不够不能装
        end
    end
end
sum_V=m(n,C+1);%数组最后一行最后一列即为最大价值

%% 记录前面动态规划计算所得到的结果    即：哪些物品被装入了背包
x=zeros(1,15);%布尔数组记录当前物体是否被装入
x(1)=1;
j=C;%从最后一个数开始回溯
for i=n:-1:2
        if j>=w(i)&m(i,j+1)==m(i-1,j-w(i)+1)+v(i)
            x(i)=1;
            j=j-w(i);   %列要进行更新才能找到路线
        else
            x(i)=0;
        end
end;
for i=1:n
    if x(i)==1
        sum_W=sum_W+w(i);
        product_N=[product_N,i];
    end
end

%% 最终结果输出显示
disp(['装入背包的物品索引号为: ',num2str(product_N)]);
disp(['  已占用的背包容量为:  ',num2str(sum_W)]);
disp(['     物品总价值为:    ',num2str(sum_V)]);
