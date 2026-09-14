clear;close all;clc

data = rand(100,1);% must be a column vector
t = length(data);
L = 10;
lag = [];
for i = 1:L
    lag = [lag,[ones(i,1);(1:(t-i))']];
end

[b,bint,r,~,stats] = regress(data,[ones(t,1),data(lag)]);

newdata = rand(20,1);
t2 = length(newdata);
newdatalag = [];
for i = 1:L
    newdatalag = [newdatalag,[data((end-i+1):end);newdata(1:(t2-i))]];
end
predValue = [ones(t2,1),newdatalag]*b;


%% analysis

ACF = [];
PACF = [];
ts0 = data;
ts = data(lag);
for j = 1:L
    u = mean(ts0,'omitnan');
    ACF(j) = sum((ts0-u).*(ts(:,j)-u),'omitnan')/...
        sum((ts0-u).*(ts0-u),'omitnan');
end

r = [ACF((end-1):-1:1),1,fliplr(ACF(end:-1:1))];
temp = reshape(repmat(r,1,2*L-1),2*L-1,2*L);
R = temp(L:(2*L-1),1:L);
PACF = R\ACF(:);

figure
subplot(2,1,1)
hold on
% stem(1:k,ACF(id,:),'linewidth',2)
bar(1:L,ACF(:),'BarWidth',0.2)
plot(0:L,ones(1,L+1)*2/sqrt(t),'r',0:L,-ones(1,L+1)*2/sqrt(t),'r')
set(gcf,'position',[300,0,1440,1440])
set(gca,'fontsize',20,'xgrid','on','ygrid','on','xlim',[0,L],'ylim',[-1,1])
title([num2str(L),' ACF'])

subplot(2,1,2)
hold on
bar(1:L,PACF,'BarWidth',0.2)
plot(0:L,ones(1,L+1)*2/sqrt(t),'r',0:L,-ones(1,L+1)*2/sqrt(t),'r')
set(gcf,'position',[300,0,1440,1440])
set(gca,'fontsize',20,'xgrid','on','ygrid','on','xlim',[0,L],'ylim',[-1,1])
title([num2str(L),' PACF'])