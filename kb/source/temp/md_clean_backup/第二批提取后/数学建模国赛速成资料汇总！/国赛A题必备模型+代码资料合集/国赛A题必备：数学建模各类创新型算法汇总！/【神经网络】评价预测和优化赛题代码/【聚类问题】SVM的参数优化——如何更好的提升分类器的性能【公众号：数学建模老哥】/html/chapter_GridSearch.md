chapter_GridSearch
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25968;&#25454;&#25552;&#21462;
- &#25968;&#25454;&#39044;&#22788;&#29702;
- &#36873;&#25321;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
- &#21033;&#29992;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
- SVM&#32593;&#32476;&#39044;&#27979;
- &#32467;&#26524;&#20998;&#26512;
- &#23376;&#20989;&#25968; SVMcgForClass.m
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% SVM&#30340;&#21442;&#25968;&#20248;&#21270;&#8212;&#8212;&#22914;&#20309;&#26356;&#22909;&#30340;&#25552;&#21319;&#20998;&#31867;&#22120;&#30340;&#24615;&#33021;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter_GridSearch
close all;
clear;
clc;
format compact;

## &#25968;&#25454;&#25552;&#21462;
% &#36733;&#20837;&#27979;&#35797;&#25968;&#25454;wine,&#20854;&#20013;&#21253;&#21547;&#30340;&#25968;&#25454;&#20026;classnumber = 3,wine:178*13&#30340;&#30697;&#38453;,wine_labes:178*1&#30340;&#21015;&#21521;&#37327;
load wine.mat;

% &#30011;&#20986;&#27979;&#35797;&#25968;&#25454;&#30340;box&#21487;&#35270;&#21270;&#22270;
figure;
boxplot(wine,'orientation','horizontal','labels',categories);
title('wine&#25968;&#25454;&#30340;box&#21487;&#35270;&#21270;&#22270;','FontSize',12);
xlabel('&#23646;&#24615;&#20540;','FontSize',12);
grid on;

% &#30011;&#20986;&#27979;&#35797;&#25968;&#25454;&#30340;&#20998;&#32500;&#21487;&#35270;&#21270;&#22270;
figure
subplot(3,5,1);
hold on
for run = 1:178
    plot(run,wine_labels(run),'*');
end
xlabel('&#26679;&#26412;','FontSize',10);
ylabel('&#31867;&#21035;&#26631;&#31614;','FontSize',10);
title('class','FontSize',10);
for run = 2:14
    subplot(3,5,run);
    hold on;
    str = ['attrib ',num2str(run-1)];
    for i = 1:178
        plot(i,wine(i,run-1),'*');
    end
    xlabel('&#26679;&#26412;','FontSize',10);
    ylabel('&#23646;&#24615;&#20540;','FontSize',10);
    title(str,'FontSize',10);
end

% &#36873;&#23450;&#35757;&#32451;&#38598;&#21644;&#27979;&#35797;&#38598;

% &#23558;&#31532;&#19968;&#31867;&#30340;1-30,&#31532;&#20108;&#31867;&#30340;60-95,&#31532;&#19977;&#31867;&#30340;131-153&#20570;&#20026;&#35757;&#32451;&#38598;
train_wine = [wine(1:30,:);wine(60:95,:);wine(131:153,:)];
% &#30456;&#24212;&#30340;&#35757;&#32451;&#38598;&#30340;&#26631;&#31614;&#20063;&#35201;&#20998;&#31163;&#20986;&#26469;
train_wine_labels = [wine_labels(1:30);wine_labels(60:95);wine_labels(131:153)];
% &#23558;&#31532;&#19968;&#31867;&#30340;31-59,&#31532;&#20108;&#31867;&#30340;96-130,&#31532;&#19977;&#31867;&#30340;154-178&#20570;&#20026;&#27979;&#35797;&#38598;
test_wine = [wine(31:59,:);wine(96:130,:);wine(154:178,:)];
% &#30456;&#24212;&#30340;&#27979;&#35797;&#38598;&#30340;&#26631;&#31614;&#20063;&#35201;&#20998;&#31163;&#20986;&#26469;
test_wine_labels = [wine_labels(31:59);wine_labels(96:130);wine_labels(154:178)];
  
## &#25968;&#25454;&#39044;&#22788;&#29702;
&#25968;&#25454;&#39044;&#22788;&#29702;,&#23558;&#35757;&#32451;&#38598;&#21644;&#27979;&#35797;&#38598;&#24402;&#19968;&#21270;&#21040;[0,1]&#21306;&#38388;

[mtrain,ntrain] = size(train_wine);
[mtest,ntest] = size(test_wine);

dataset = [train_wine;test_wine];
% mapminmax&#20026;MATLAB&#33258;&#24102;&#30340;&#24402;&#19968;&#21270;&#20989;&#25968;
[dataset_scale,ps] = mapminmax(dataset',0,1);
dataset_scale = dataset_scale';

train_wine = dataset_scale(1:mtrain,:);
test_wine = dataset_scale( (mtrain+1):(mtrain+mtest),: );

## &#36873;&#25321;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% &#39318;&#20808;&#36827;&#34892;&#31895;&#30053;&#36873;&#25321;: c&g &#30340;&#21464;&#21270;&#33539;&#22260;&#26159; 2^(-10),2^(-9),...,2^(10)
[bestacc,bestc,bestg] = SVMcgForClass(train_wine_labels,train_wine,-10,10,-10,10);

% &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation Accuracy = %g%% Best c = %g Best g = %g',bestacc,bestc,bestg);
disp(str);

% &#26681;&#25454;&#31895;&#30053;&#36873;&#25321;&#30340;&#32467;&#26524;&#22270;&#20877;&#36827;&#34892;&#31934;&#32454;&#36873;&#25321;: c &#30340;&#21464;&#21270;&#33539;&#22260;&#26159; 2^(-2),2^(-1.5),...,2^(4), g &#30340;&#21464;&#21270;&#33539;&#22260;&#26159; 2^(-4),2^(-3.5),...,2^(4),
[bestacc,bestc,bestg] = SVMcgForClass(train_wine_labels,train_wine,-2,4,-4,4,3,0.5,0.5,0.9);
% &#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation Accuracy = %g%% Best c = %g Best g = %g',bestacc,bestc,bestg);
disp(str);
&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation Accuracy = 98.8764% Best c = 2.2974 Best g = 4
&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation Accuracy = 98.8764% Best c = 1.41421 Best g = 1
    
## &#21033;&#29992;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
cmd = ['-c ',num2str(bestc),' -g ',num2str(bestg)];
model = svmtrain(train_wine_labels,train_wine,cmd);

## SVM&#32593;&#32476;&#39044;&#27979;
[predict_label,accuracy] = svmpredict(test_wine_labels,test_wine,model);

% &#25171;&#21360;&#27979;&#35797;&#38598;&#20998;&#31867;&#20934;&#30830;&#29575;
total = length(test_wine_labels);
right = sum(predict_label == test_wine_labels);
disp('&#25171;&#21360;&#27979;&#35797;&#38598;&#20998;&#31867;&#20934;&#30830;&#29575;');
str = sprintf( 'Accuracy = %g%% (%d/%d)',accuracy(1),right,total);
disp(str);
Accuracy = 98.8764% (88/89) (classification)
&#25171;&#21360;&#27979;&#35797;&#38598;&#20998;&#31867;&#20934;&#30830;&#29575;
Accuracy = 98.8764% (88/89)

## &#32467;&#26524;&#20998;&#26512;
% &#27979;&#35797;&#38598;&#30340;&#23454;&#38469;&#20998;&#31867;&#21644;&#39044;&#27979;&#20998;&#31867;&#22270;
% &#36890;&#36807;&#22270;&#21487;&#20197;&#30475;&#20986;&#21482;&#26377;&#19977;&#20010;&#27979;&#35797;&#26679;&#26412;&#26159;&#34987;&#38169;&#20998;&#30340;
figure;
hold on;
plot(test_wine_labels,'o');
plot(predict_label,'r*');
xlabel('&#27979;&#35797;&#38598;&#26679;&#26412;','FontSize',12);
ylabel('&#31867;&#21035;&#26631;&#31614;','FontSize',12);
legend('&#23454;&#38469;&#27979;&#35797;&#38598;&#20998;&#31867;','&#39044;&#27979;&#27979;&#35797;&#38598;&#20998;&#31867;');
title('&#27979;&#35797;&#38598;&#30340;&#23454;&#38469;&#20998;&#31867;&#21644;&#39044;&#27979;&#20998;&#31867;&#22270;','FontSize',12);
grid on;
snapnow;
 
## &#23376;&#20989;&#25968; SVMcgForClass.m
function [bestacc,bestc,bestg] = SVMcgForClass(train_label,train,cmin,cmax,gmin,gmax,v,cstep,gstep,accstep)
%SVMcg cross validation by faruto

%
% by faruto
%Email:patrick.lee@foxmail.com QQ:516667408 http://blog.sina.com.cn/faruto BNU
%last modified 2010.01.17
%Super Moderator @ www.ilovematlab.cn

% &#33509;&#36716;&#36733;&#35831;&#27880;&#26126;&#65306;
% faruto and liyang , LIBSVM-farutoUltimateVersion
% a toolbox with implements for support vector machines based on libsvm, 2009.
% Software available at http://www.ilovematlab.cn
%
% Chih-Chung Chang and Chih-Jen Lin, LIBSVM : a library for
% support vector machines, 2001. Software available at
% http://www.csie.ntu.edu.tw/~cjlin/libsvm

% about the parameters of SVMcg
if nargin < 10
    accstep = 4.5;
end
if nargin < 8
    cstep = 0.8;
    gstep = 0.8;
end
if nargin < 7
    v = 5;
end
if nargin < 5
    gmax = 8;
    gmin = -8;
end
if nargin < 3
    cmax = 8;
    cmin = -8;
end
% X:c Y:g cg:CVaccuracy
[X,Y] = meshgrid(cmin:cstep:cmax,gmin:gstep:gmax);
[m,n] = size(X);
cg = zeros(m,n);

eps = 10^(-4);

% record acc with different c & g,and find the bestacc with the smallest c
bestc = 1;
bestg = 0.1;
bestacc = 0;
basenum = 2;
for i = 1:m
    for j = 1:n
        cmd = ['-v ',num2str(v),' -c ',num2str( basenum^X(i,j) ),' -g ',num2str( basenum^Y(i,j) )];
        cg(i,j) = svmtrain(train_label, train, cmd);

        if cg(i,j) <= 55
            continue;
        end

        if cg(i,j) > bestacc
            bestacc = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

        if abs( cg(i,j)-bestacc )<=eps && bestc > basenum^X(i,j)
            bestacc = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

    end
end
% to draw the acc with different c & g
figure;
[C,h] = contour(X,Y,cg,70:accstep:100);
clabel(C,h,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
firstline = 'SVC&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(&#31561;&#39640;&#32447;&#22270;)[GridSearchMethod]';
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVAccuracy=',num2str(bestacc),'%'];
title({firstline;secondline},'Fontsize',12);
grid on;

figure;
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,30,100]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('Accuracy(%)','FontSize',12);
firstline = 'SVC&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(3D&#35270;&#22270;)[GridSearchMethod]';
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVAccuracy=',num2str(bestacc),'%'];
title({firstline;secondline},'Fontsize',12);

      Published with MATLAB&reg; 7.14

 bestacc
            bestacc = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end        
        
        if abs( cg(i,j)-bestacc ) basenum^X(i,j) 
            bestacc = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end        
        
    end
end
% to draw the acc with different c & g
figure;
[C,h] = contour(X,Y,cg,70:accstep:100);
clabel(C,h,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
firstline = 'SVC参数选择结果图(等高线图)[GridSearchMethod]'; 
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVAccuracy=',num2str(bestacc),'%'];
title({firstline;secondline},'Fontsize',12);
grid on; 

figure;
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,30,100]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('Accuracy(%)','FontSize',12);
firstline = 'SVC参数选择结果图(3D视图)[GridSearchMethod]'; 
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVAccuracy=',num2str(bestacc),'%'];
title({firstline;secondline},'Fontsize',12);

##### SOURCE END #####
-->
