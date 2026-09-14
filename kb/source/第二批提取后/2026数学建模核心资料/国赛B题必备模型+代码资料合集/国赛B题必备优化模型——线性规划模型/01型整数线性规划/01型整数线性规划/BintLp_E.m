%mÃ¶¾Ù·¨³ÌÐò BintLp_E.m
function [x,f]=BintLp_E(c,A,b,N)
if nargin<4,N=0;end
c=c(:);
b=b(:);
[m,n]=size(A);
x=[];
f=abs(c')*ones(n,1);
i=1;
while i<=2^n
    B=de2bi(i-1,n)';
    t=A*B-b;
    t11=find(t(1:N,:)~=0);
    t12=find(t(N+1:m,:)>0);
    t1=[t11;t12];
    if isempty(t1)
        f=min([f,c'*B]);
        if c'*B==f,x=B;end
    end
    i=i+1;
end