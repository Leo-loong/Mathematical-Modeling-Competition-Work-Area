%% data
clear
cd('F:\ÄªÀ¼µÙ')
% ¶«É½ Áúº£ ÉÏ´¨ ÍòÉ½  ÉÇÎ²
% DoSA LoHi ShCH WaSH SnWE
% Á÷ ÀË ·ç
namelist = [repmat('DoSA',2,1);...
            repmat('LoHI',2,1);...
            repmat('ShCH',4,1);...
            repmat('WaSH',4,1);...
            repmat('SnWE',10,1)];
datelist = [repmat(['160914';'160915'],2,1);...
            repmat(['181029';'181030';'181031';'181101'],2,1);...
            strcat('2006',num2str((10:19)'))];
typelist = [ones(12,1);ones(10,1)];
alldata = [];
% load('alldata.mat')
for i = 13%1:length(namelist)
   cd('F:\ÄªÀ¼µÙ')
   [alldata(i).name,...
    alldata(i).data,...
    alldata(i).data1,...
    alldata(i).n,...
    alldata(i).m,...
    alldata(i).n1,...
    alldata(i).t,...
    alldata(i).coo,...
    alldata(i).kmat,...
    alldata(i).pairid,...
    alldata(i).nearid]= read(namelist(i,:),datelist(i,:),'F:\ÄªÀ¼µÙ\data',typelist(i,:));
end
cd('F:\ÄªÀ¼µÙ')
% save('alldata.mat','alldata')

clear
cd('F:\ÄªÀ¼µÙ')
load('alldata.mat')
ind = 5;
data = alldata(ind).data;
data1 = alldata(ind).data1;
n = alldata(ind).n;
m = alldata(ind).m;
n1 = alldata(ind).n1;
t = alldata(ind).t;
coo = alldata(ind).coo;
kmat = alldata(ind).kmat;
pairid = alldata(ind).pairid;
nearid = alldata(ind).nearid;

%% descriptional statistics
% overall animation
close all
figure
plotid = 1:n1;
y1 = min(min(data1(plotid,:,1)));y2 = max(max(data1(plotid,:,1)));
x1 = min(min(data1(plotid,:,2)));x2 = max(max(data1(plotid,:,2)));
z1 = min(min(data1(plotid,:,4)));z2 = max(max(data1(plotid,:,4)));
z = max(-z1,z2)/2;
for i = 1:t
    scatter([data1(plotid,i,2);0;0],...
            [data1(plotid,i,1);0;0],...
            100,...
            [data1(plotid,i,4);-z;z],'filled')
    colormap(jet)
    set(gcf,'position',[0,0,2050,1150])
    set(gca,'FontSize',20,'xlim',[x1,x2],'ylim',[y1,y2])
    colorbar
    title(i);
    pause(0.5)
    axis equal
end

% overall 3d animation
close all
figure
plotid = 1:n1;%nearid(1000,1:100);
y1 = min(min(data1(plotid,:,1)));y2 = max(max(data1(plotid,:,1)));
x1 = min(min(data1(plotid,:,2)));x2 = max(max(data1(plotid,:,2)));
z1 = min(min(data1(plotid,:,4)));z2 = max(max(data1(plotid,:,4)));
z = max(-z1,z2);
for i = 1:t
    scatter3([data1(plotid,i,2);0;0],...
            [data1(plotid,i,1);0;0],...
            [data1(plotid,i,4);0;0],...
            100,...
            [data1(plotid,i,4);-z;z],'filled')
%     view(0,3)
    colormap(jet)
    set(gcf,'position',[0,0,2000,1400])
    set(gca,'FontSize',20,'xlim',[x1,x2],'ylim',[y1,y2],'zlim',[-z,z])
    colorbar
    title(i);
    pause(0.2)
end

% valid data count
figure
histogram(m,t)
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20)

% overall ts
figure
plot(1:t,data1(:,:,4))
set(gca,'FontSize',20,'XTick',linspace(1,t,9),'XTickLabel',{'0','3','6','9','12','15','18','21','24'})
set(gcf,'position',[0,0,2560,1440])

% physical distribution and missing values count
plotid = 1:n1;
y1 = min(min(data1(plotid,:,1)));y2 = max(max(data1(plotid,:,1)));
x1 = min(min(data1(plotid,:,2)));x2 = max(max(data1(plotid,:,2)));
figure
scatter(coo(plotid,1),coo(plotid,2),[],m,'filled')
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20,'xlim',[x1,x2],'ylim',[y1,y2])
colorbar
axis equal
% valid area
threhold = 120;
figure
plotid = find(m>threhold);
scatter([coo(plotid,1);0],[coo(plotid,2);0],[],[m(plotid);0],'filled')
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20,'xlim',[x1,x2],'ylim',[y1,y2])
colorbar
title(threhold)
axis equal

temp = nan(t,1);
for i = 1:t
    temp(i) = sum((m>i));
end

figure
plot(1:t,temp/n1,'linewidth',3)
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20)
xlabel('¾ö¶ÏãÐÖµ')
ylabel('Êý¾Ý¿ÉÓÃÂÊ')
axis tight

% missing values count by range



% radial = nan(n1,1);
% rn = [];
% rid = 1;
% while sum(isnan(radial))
%     id = find(isnan(radial));
%     temp = id(1);
%     while sum(sum(~ismember(pairid(temp,1:2),temp)))
%         add = unique(pairid(temp,1:2));
%         add = add(:);
%         temp = [temp;add];
%         temp = unique(temp);
%         temp = temp(:);
%     end
%     temp(ismember(temp,find(~isnan(radial))))=[];
%     if length(temp)>2
%         radial(temp) = rid;
%         rid = rid+1;
%         rn = [rn;length(temp)];
%     else
%         radial(temp) = 0;
%     end
% end
% rid = rid-1;
% unique(rn)
% sum(radial==0)

% figure
% for id = 1:n1
%     hold off
%     scatter(coo(:,1),coo(:,2))
%     hold on
%     scatter(coo(pairid(id,1:2),1),coo(pairid(id,1:2),2),100,'g','fill')
%     scatter(coo(id,1),coo(id,2),100,'k','fill')
%     set(gcf,'position',[0,0,2560,1440])
%     set(gca,'FontSize',20)
%     axis equal
%     title(id)
%     pause(0.3)
% end
% 
% figure
% for i = 1:rid
%     scatter(coo(:,1),coo(:,2))
%     axis equal
%     hold on
%     scatter(coo(radial==i,1),coo(radial==i,2),'g','fill')
%     hold off
%     set(gcf,'position',[0,0,2560,1440])
%     set(gca,'FontSize',20)
%     title(i)
%     pause(0.5)
% end

%% time series analysis
% lag series
id = 100;
k = 20;
ts0 = data1(id,:,4);
ts = [];
for i = 1:k
    ts = [ts;data1(id,[ones(1,i),1:(end-i)],4)];
end

% scatter
figure
l = 2;
scatter(ts0,ts(1,:),100)
title([num2str(id),' lag_',num2str(l)],'fontsize',30)
set(gcf,'position',[300,0,1440,1440])
set(gca,'FontSize',20)

% ACF and PACF
k = 80;
ACF = nan(n1,k);
PACF = nan(n1,k);
for id = 1:n1
    ts0 = data1(id,:,4);
    ts = [];
    for i = 1:k
        ts = [ts;data1(id,[ones(1,i),1:(end-i)],4)];
    end
    for j = 1:k
        u = mean(ts0,'omitnan');
        ACF(id,j) = sum((ts0-u).*(ts(j,:)-u),'omitnan')/...
            sum((ts0-u).*(ts0-u),'omitnan');
    end
    r = [ACF(id,(end-1):-1:1),1,fliplr(ACF(id,end:-1:1))];
    temp = reshape(repmat(r,1,2*k-1),2*k-1,2*k);
    R = temp(k:(2*k-1),1:k);
    PACF(id,:) = R\ACF(id,:)';
end

id = 2400;
figure
subplot(2,1,1)
hold on
% stem(1:k,ACF(id,:),'linewidth',2)
bar(1:k,ACF(id,:),'BarWidth',0.2)
plot(0:k,ones(1,k+1)*2/sqrt(t),'r',0:k,-ones(1,k+1)*2/sqrt(t),'r')
set(gcf,'position',[300,0,1440,1440])
set(gca,'fontsize',20,'xgrid','on','ygrid','on','xlim',[0,k],'ylim',[-1,1])
title([num2str(id),' ACF'])

subplot(2,1,2)
hold on
bar(1:k,PACF(id,:),'BarWidth',0.2)
plot(0:k,ones(1,k+1)*2/sqrt(t),'r',0:k,-ones(1,k+1)*2/sqrt(t),'r')
set(gcf,'position',[300,0,1440,1440])
set(gca,'fontsize',20,'xgrid','on','ygrid','on','xlim',[0,k],'ylim',[-1,1])
title([num2str(id),' PACF'])

%% prediction
% identification
% data1(:,:,4) = data1(:,:,4)-data1(:,[1,1:(end-1)],4);
[dev1,dev2,dev3,R1,R2,sigma1,sigma2] = model(data1,pairid,nearid,m);

out1 = find(sum(dev1>0,2));
out2 = find(sum(dev2>0,2));
out3 = find(sum(dev3>0,2));
for i = 1:5
    id = out2(i);
    tsfigure(id,data1,pairid,nearid,dev1,dev2,dev3,R1,R2,sigma1,sigma2,0)
    if mod(i,50) == 0
        close all
        pause(4)
    end
    pause(5)
end

% position presentation
mnear = 1:4;
mpair = 1:2;
figure
hold on
scatter(coo(:,1),coo(:,2))
% scatter(coo(nearid(id,mnear),1),coo(nearid(id,mnear),2),'r','fill')
scatter(coo(pairid(id,mpair),1),coo(pairid(id,mpair),2),'g','fill')
scatter(coo(id,1),coo(id,2),'k','fill')
axis equal
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20)
title(id)

% choice of range threhold variable
v1 = std(data1(:,:,4),0,2,'omitnan');% std
v2 = std(data1(:,:,4)-data1(:,[1,1:(end-1)],4),0,2,'omitnan');% lag1 std
v3 = sum(dev2>0,2);% anomaly count
plotid = find(sigma1);
figure
hold on
scatter(coo(plotid,1),coo(plotid,2),[],sigma1(plotid),'filled')
set(gcf,'position',[0,0,2560,1440])
set(gca,'FontSize',20)
axis equal
colorbar

%% calibration
datapre1 = data1;
dev2p = dev2;
R2p = R2;
remain = 0;
tic
for times = 1:30
    dev2num = sum(dev2p>0,2);
    for i = 1:n1
        for j = dev2p(i,1:dev2num(i))
            datapre1(i,j,4) = datapre1(i,j,4)-R2p(i,j);
        end
    end
    [devp,dev2p,dev3p,R1p,R2p,sigma1p,sigma2p] = model(datapre1,pairid,nearid,m);
    tsfigure(id,datapre1,pairid,nearid,devp,dev2p,R1p,R2p,sigma1p,sigma2p)
    remain = [remain;sum(sum(dev2p,2)>0)];
end
remain(1) = [];
toc
save('pre3-30.mat',datapre1)

%% compose
clear;clc;close all
cd('F:\ÄªÀ¼µÙ')

figure 
for zoom = 10:100
key_l = round(coo_l(:,1)*zoom)/zoom+round(coo_l(:,2)*zoom)/zoom*1i;
key_d = round(coo_d(:,1)*zoom)/zoom+round(coo_d(:,2)*zoom)/zoom*1i;
hold on
xlim([10,100])
scatter(zoom,length(key_l)+length(key_d)-length(unique([key_l;key_d])))
end

va = 10;vb = 23;vc = 39;
thetaa = 40;thetab = 20;thetac = 24;

theta1 = atan((vb*cos(thetaa)-va*cos(thetab))/(va*sin(thetab)-vb*sin(thetab)));
v1 = va/cos(theta1-thetaa);

theta2 = atan((vc*cos(theta1)-v1*cos(thetac))/(v1*sin(thetac)-vc*sin(theta1)));
v2 = v1/cos(theta2-theta1);

%% others

% 3-d mesh
[x,y] = meshgrid(1:t,1:100);
figure
meshz(y,x,data1(nearid(id,1:100),:,4))
xlabel('t')

%% iforest
rand('state',1)
tic

itree = 32;
phi = 128;
t0 = 15;

seq = permute(data1(:,t0,[1,2,4]),[1,3,2]);
seq = [seq,repmat(data1(:,t0,4),1,5)];
nearbar = [];
for i = 1:4
    nearbar = [nearbar,permute(data1(nearid(:,i),t0,4),[1,3,2])];
end
nearbar = mean(nearbar,2,'omitnan');
seq(:,3) = seq(:,3)-nearbar;
seq(:,4) = seq(:,3)-nearbar;
seq(:,5) = seq(:,3)-nearbar;
seq(:,6) = seq(:,3)-nearbar;
nind = find(sum(~isnan(seq),2));
seq = seq(nind,:);
[n2,~] = size(seq);

trees = struct([]);
for i = 1:itree
    r = ceil(rand(phi,1)*n2);
    seqi = seq(r,:);
    trees(i).nodes = myiforest(seqi);
end

H = nan(n2,itree);
for i = 1:n2
    for j = 1:itree
        h = 0;
        point = seq(i,:);
        tree = trees(j).nodes;
        while size(tree,1)~=1
            fea = tree{1,2}(1+h);
            cut = tree{1,3}(1+h);
            ind = tree{1,1}(1+h);
            flag = (point(fea)>=cut);
            left = tree{1,4}(1,h+1);
            right = tree{1,4}(2,h+1);
            tree = tree((1+left*flag):(left+right*flag),:);
            h = h+1;
        end
        H(i,j) = h;
    end
end
Hbar = mean(H,2);
toc

figure
p1 = subplot(1,2,1);
plotid = 1:n1;
scatter(data1(plotid,t0,2),...
        data1(plotid,t0,1),...
        100,...
        data1(plotid,t0,4),'filled')
colormap(p1,jet)
set(gcf,'position',[0,0,2050,1150])
set(gca,'FontSize',20)
colorbar
title(t0);
axis equal

p2 = subplot(1,2,2);
plotid = nind;
scatter(data1(plotid,t0,2),...
        data1(plotid,t0,1),...
        100,...
        Hbar,'filled')
colormap(p2,hot)
set(gcf,'position',[0,0,2050,1150])
set(gca,'FontSize',20)
colorbar
title(t0);
axis equal