%0-1规划  p313
%整数线性规划matlab指令及参考程序
%x=bintprog(f,A,b):求解0-1整数线性规划，用法类似于linprog
%x=bintprog(f,A,b,Aeq,beq):求解下面线性规划：min z=f^T,Ax<=b,Aeq*x=beq,x分量取值0或1
%x=bintprog(f,A,b,Aeq,beq，x0):指定迭代初值x0,如果没有不等式约束，可用[]替代A和b表示默认，如果没有等式约束，可用[]代替Aeq和
%beq表示默认；用[x,Fval]代替上述各个命令行中左边的x，则可以得到最优解处的函数值Fval。
%de2bi转换十进制为二进制
function b=de2bi(d,n,p)
d=d(:);
len_d=length(d);
if min(d)<0,error('Cannot convert a negative number');
elseif ~isempty(find(d==inf))
    error('Inpur must be an integer.');
end
if nargin<2
    tmp=max(d);b1=[];
    while tmp>0
        b1=[b1 rem(tmp,2)];
        tmp=floor(tmp/2);
    end
    n=length(b1);
end
if nargin<3, p=2;end
b=zeros(len_d,n);
for i=1:len_d
    j=1;
    tmp=d(i);
    while(j<=n)&(tmp>0)
        b(i,j)=rem(tmp,p);
        tmp=floor(tmp/p);
        j=j+1;
    end
end
end

