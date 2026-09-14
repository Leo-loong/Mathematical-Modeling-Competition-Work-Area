function [w1,b1,w2,b2,inputps]=mynet(kd,input_train,output_train)
%输入数据归一化?
[inputn,inputps]=mapminmax(input_train);
[lines,kr]=size(input_train);

%网络结构初始化
innum=lines;
midnum=lines+1;
outnum=kd;
 

%权值初始化
w1=rands(midnum,innum);
b1=rands(midnum,1);
w2=rands(midnum,outnum);
b2=rands(outnum,1);

w1_1=w1;
w2_1=w2;
b1_1=b1;
b2_1=b2;

%学习率
xite=0.1;
alfa=0.01;

% 网络训练
for ii=1:20
%    E(ii)=0;
    for i=1:1:kr
       % 网络预测输出
        x=inputn(:,i);
        % 隐含层输出?        
        for j=1:1:midnum
            I(j)=inputn(:,i)'*w1(j,:)'+b1(j);
            Iout(j)=1/(1+exp(-I(j)));
        end
        % 输出层输出
        yn=w2'*Iout'+b2;
        
       % 权值阀值修正
        %计算误差        
        e=output_train(:,i)-yn;     
       % E(ii)=E(ii)+sum(abs(e));
        
        %计算权值变化率
        dw2=e*Iout;
        db2=e';
        
        for j=1:1:midnum
            S=1/(1+exp(-I(j)));
            FI(j)=S*(1-S);
        end      
        for k=1:1:innum
            for j=1:1:midnum
                ew=0;
                for i=1:outnum
                    ew=e(i)*w2(j,i)+ew;
                end
                dw1(k,j)=FI(j)*x(k)*ew;
                db1(j)=FI(j)*ew;
            end
        end
           
        w1=w1_1+xite*dw1';
        b1=b1_1+xite*db1';
        w2=w2_1+xite*dw2';
        b2=b2_1+xite*db2';
        
       w1_1=w1;
       w2_1=w2;
        b1_1=b1;
        b2_1=b2;
    end
end
 