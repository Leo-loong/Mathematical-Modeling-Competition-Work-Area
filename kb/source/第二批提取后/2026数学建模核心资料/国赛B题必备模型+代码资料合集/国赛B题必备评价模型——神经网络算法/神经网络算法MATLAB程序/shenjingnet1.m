function [output_fore0,modelrightridio,MCC]=shenjingnet1(data,kd,test0)
%%
[rows,lines]=size(data);
rows=rows/kd;
k=randperm(kd*rows);
[~,n]=sort(k);

input=data(:,2:lines);
output1 =data(:,1);

ey=eye(kd);
for i=1:kd*rows
    for j=1:kd
        if (output1(i)==j)
            output(i,:)=ey(j,:);
        end
    end
end

%% 
tic
% input_train=input(n(1:(kd-1)*rows),:)';
% output_train=output(n(1:(kd-1)*rows),:)';
input_train=input(n,:)';
output_train=output(n,:)';

input_test=input(n((kd-1)*rows+1:kd*rows),:)';
output_test=output(n((kd-1)*rows+1:kd*rows),:)';

[w1,b1,w2,b2,inputps]=mynet(kd,input_train,output_train);
[output_fore]=forecast(w1,w2,b1,b2,input_test,inputps);
[output_fore0]=forecast(w1,w2,b1,b2,test0',inputps);

%BP网络预测误差
error=output_fore-output1(n((kd-1)*rows+1:kd*rows))';

%画出预测种类和实际种类的分类图图
figure(1)
plot(output_fore,'or')
hold on
plot(output1(n((kd-1)*rows+1:kd*rows))','*b')
legend('预测类别','实际类别')

%画出误差图?
figure(2)
plot(error)
title('BP网络分类误差','fontsize',12)
xlabel('样本值','fontsize',12)
ylabel('分类误差','fontsize',12)
toc
%%
j=20
for i=1:j
    tic
    i
    input_test1=input_train(:,1:j);output_test1=output_train(:,1:j);
    a_intest=input_test1(:,i);
    b_outtest(i)=find(output_test1(:,i)>0);
    input_test1(:,i)=[];output_test1(:,i)=[];
    [w11,b11,w21,b21,inputps1]=mynet(kd,input_test1,output_test1);
    [output_fore1]=forecast(w11,w21,b11,b21,a_intest,inputps1);
    error1(i)=output_fore1-b_outtest(i);
    outf(i)=output_fore1;
    toc
end
errlv=sum(error1==0)/j;

figure(3)
plot(error1)
figure(4)
plot(outf,'or')
hold on
plot(b_outtest,'*b')

for i=1:kd
    TP(i)=sum(outf==i&b_outtest==i)/j;    
    FN(i)=sum(outf==i&b_outtest~=i)/j;   
    FP(i)=sum(outf~=i&b_outtest==i)/j;
    TN(i)=sum(outf~=i&b_outtest~=i)/j;
    MCC(i)=(TP(i)*TN(i)-FP(i)*FN(i))/sqrt((TP(i)+FN(i))*(TP(i)+FP(i))*(TN(i)+FP(i))*(TN(i)+FN(i)));
end

%%
k=zeros(1,kd);  
%找出判断错误的分类属于哪一类?
for i=1:rows
    if error(i)~=0
        [~,c]=max(output_test(:,i));
        switch c
            case 1 
                k(1)=k(1)+1;
            case 2 
                k(2)=k(2)+1;
            case 3 
                k(3)=k(3)+1;
            case 4 
                k(4)=k(4)+1;
        end
    end
end

%找出每类的个体和
kk=zeros(1,kd);
for i=1:rows
    [~,c]=max(output_test(:,i));
    switch c
        case 1
            kk(1)=kk(1)+1;
        case 2
            kk(2)=kk(2)+1;
        case 3
            kk(3)=kk(3)+1;
        case 4
            kk(4)=kk(4)+1;
    end
end

%正确率
modelrightridio=(kk-k)./kk;