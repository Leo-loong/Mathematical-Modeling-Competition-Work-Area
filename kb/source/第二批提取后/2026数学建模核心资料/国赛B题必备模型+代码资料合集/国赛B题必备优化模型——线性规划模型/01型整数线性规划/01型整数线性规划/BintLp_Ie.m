%ÒþÃ¶¾Ù·¨³ÌÐò BintLp_Ie:
function [x,f]=BintLp_Ie(c,A,b,N)
if nargin<4,N=0;end
c=c(:);
b=b(:);
A=[-A(1:N,:);A];
b=[-b(1:N);b];
[m,n]=size(A);
x=[];
f=abs(c')*ones(n,1);
A=[c';A];
b=[f;b];
i=1;
while i<=2^n
    B=de2bi(i-1,n)';
    j=1;
    t1=A(j,:)*B-b(j);
    while(t1<=0&j<m+1)
        j=j+1;
        t1=A(j,:)*B-b(j);
        if t1>0,j=1;
        end;
    end
    if j==m+1
        x=B;f=c'*B;
        b(1)=min([b(1),f]);
    end
    i=i+1;
end