clear all;
clc

load 'b.txt';
X=b(:,1:7);

disp('第一步，进行标准化处理');
MX=mean(X);
[n,m]=size(X);
for ii=1:m
    SX(:,ii)=(X(:,ii)/MX(ii));
end
SX
disp('第二步，对标准化后的数据矩阵进行对应变换处理');
for ii=1:n;
    SXLineAdd(ii)=sum(SX(ii,:));%按行求和
end
for jj=1:m;
    SXColumAdd(jj)=sum(SX(:,jj));%按列求和
end
SXTotal=(sum(SXLineAdd)+sum(SXColumAdd)/2);%%求总和

for ii=1:n
    for jj=1:m
        ZX(ii,jj)=(SX(ii,jj)-(SXLineAdd(ii)*SXColumAdd(jj))/SXTotal)/sqrt(SXLineAdd(ii)*SXColumAdd(jj));
    end
end
ZX
disp('第三步，计算协方差矩阵');
RX=ZX'*ZX
disp('第四步，确定矩阵R的特征值及对应的特征向量，并按照由大到小顺序排列');
[e,lamda]=eig(cov(RX));
for ii=1:m
    lamd(ii)=lamda(ii,ii);
end
[lamd,kk]=sort(lamd,2);
for ii=1:m;
    lam(ii)=lamd(m+1-ii);
end
yjj=m+1-kk;
for k=1:m
    ee(:,k)=e(:,yjj(k));
end
lam
ee
EXPLAINED(1:m)=0;
for ii=1:m
    explained(ii)=100*lam(ii)/sum(lam);
end
disp('主分量累积贡献率');
EXPLAINED=cumsum(explained)
xi=1;
while xi<=m
    if EXPLAINED(xi)>=85
        ['选择前面',num2str(xi),'个主分量即可大于85%']
        break;
    end
    xi=xi+1;
end
disp('第五步，计算R型、Q型因子载荷矩阵A、B');
for ii=1:m
    A(:,ii)=ee(:,ii)*sqrt(lam(ii));vv(:,ii)=ZX*ee(:,ii);
    B(:,ii)=vv(:,ii)*sqrt(lam(ii));
end
A,B
for iii=1:xi
    for ii=1:n;
        PJ(iii,ii)=SX(ii,:)*A(:,xi);end
end
disp('样本排序评价');
for iii=1:xi
    ['样本按照第',num2str(iii),'个综合因子排序']
    gc=1:n;[YPJ,K]=sort(PJ(iii,:),2);K
end
disp('第六步，作图分类');
figure(1);plot(A(:,1),A(:,2),'*');grid on;
xlabel('第一综合因子');ylabel('第二综合因子');title('二维指标分类图');
for ii=1:m;
    text(A(ii,1),A(ii,2),['指标',num2str(ii)]);end
figure(2);plot(B(:,1),B(:,2),'*');grid on;
xlabel('第一综合因子');ylabel('第二综合因子');title('二维样本分类图');
for ii=1:n;
    text(B(ii,1),B(ii,2),['月份',num2str(ii)]);end
figure(3);plot3(A(:,1),A(:,2),A(:,3),'*');grid on;
xlabel('第一综合因子');ylabel('第二综合因子');zlabel('第三综合因子');title('三维指标分类图');
for ii=1:m;
    text(A(ii,1),A(ii,2),A(ii,3),['指标',num2str(ii)]);end
figure(4);plot3(B(:,1),B(:,2),B(:,3),'*');grid on;
xlabel('第一综合因子');ylabel('第二综合因子');zlabel('第三综合因子');title('三维样本分类图');
for ii=1:n;
    text(B(ii,1),B(ii,2),B(ii,3),['月份',num2str(ii)]);end
