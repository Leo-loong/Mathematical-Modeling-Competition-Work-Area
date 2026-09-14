data=rand(100,1);
t=length(data);
[b,bint,r,~,stats] = regress(data,[ones(t,1),data([1,1:(end-1)])]);
% temp=[1,data(end)]*b;
temp=b(1)+b(2)*data(end)
