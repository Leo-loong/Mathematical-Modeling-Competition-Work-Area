chapter_GA
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25968;&#25454;&#25552;&#21462;
- &#25968;&#25454;&#39044;&#22788;&#29702;
- &#36873;&#25321;GA&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
- &#21033;&#29992;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
- SVM&#32593;&#32476;&#39044;&#27979;
- &#32467;&#26524;&#20998;&#26512;
- &#23376;&#20989;&#25968; gaSVMcgForClass.m
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% SVM&#30340;&#21442;&#25968;&#20248;&#21270;&#8212;&#8212;&#22914;&#20309;&#26356;&#22909;&#30340;&#25552;&#21319;&#20998;&#31867;&#22120;&#30340;&#24615;&#33021;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter_GA
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

## &#36873;&#25321;GA&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% GA&#30340;&#21442;&#25968;&#36873;&#39033;&#21021;&#22987;&#21270;
ga_option.maxgen = 200;
ga_option.sizepop = 20;
ga_option.cbound = [0,100];
ga_option.gbound = [0,100];
ga_option.v = 5;
ga_option.ggap = 0.9;

[bestacc,bestc,bestg] = gaSVMcgForClass(train_wine_labels,train_wine,ga_option);

% &#25171;&#21360;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation Accuracy = %g%% Best c = %g Best g = %g',bestacc,bestc,bestg);
disp(str);
&#25171;&#21360;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation Accuracy = 98.8764% Best c = 4.05092 Best g = 3.0839
 
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
 
## &#23376;&#20989;&#25968; gaSVMcgForClass.m
function [BestCVaccuracy,Bestc,Bestg,ga_option] = gaSVMcgForClass(train_label,train_data,ga_option)
% gaSVMcgForClass

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

% &#21442;&#25968;&#21021;&#22987;&#21270;
if nargin == 2
    ga_option = struct('maxgen',200,'sizepop',20,'ggap',0.9,...
        'cbound',[0,100],'gbound',[0,1000],'v',5);
end
% maxgen:&#26368;&#22823;&#30340;&#36827;&#21270;&#20195;&#25968;,&#40664;&#35748;&#20026;200,&#19968;&#33324;&#21462;&#20540;&#33539;&#22260;&#20026;[100,500]
% sizepop:&#31181;&#32676;&#26368;&#22823;&#25968;&#37327;,&#40664;&#35748;&#20026;20,&#19968;&#33324;&#21462;&#20540;&#33539;&#22260;&#20026;[20,100]
% cbound = [cmin,cmax],&#21442;&#25968;c&#30340;&#21464;&#21270;&#33539;&#22260;,&#40664;&#35748;&#20026;(0,100]
% gbound = [gmin,gmax],&#21442;&#25968;g&#30340;&#21464;&#21270;&#33539;&#22260;,&#40664;&#35748;&#20026;[0,1000]
% v:SVM Cross Validation&#21442;&#25968;,&#40664;&#35748;&#20026;5

%
MAXGEN = ga_option.maxgen;
NIND = ga_option.sizepop;
NVAR = 2;
PRECI = 20;
GGAP = ga_option.ggap;
trace = zeros(MAXGEN,2);

FieldID = ...
[rep([PRECI],[1,NVAR]);[ga_option.cbound(1),ga_option.gbound(1);ga_option.cbound(2),ga_option.gbound(2)]; ...
 [1,1;0,0;0,1;1,1]];

Chrom = crtbp(NIND,NVAR*PRECI);

gen = 1;
v = ga_option.v;
BestCVaccuracy = 0;
Bestc = 0;
Bestg = 0;
%
cg = bs2rv(Chrom,FieldID);

for nind = 1:NIND
    cmd = ['-v ',num2str(v),' -c ',num2str(cg(nind,1)),' -g ',num2str(cg(nind,2))];
    ObjV(nind,1) = svmtrain(train_label,train_data,cmd);
end
[BestCVaccuracy,I] = max(ObjV);
Bestc = cg(I,1);
Bestg = cg(I,2);

for gen = 1:MAXGEN
    FitnV = ranking(-ObjV);

    SelCh = select('sus',Chrom,FitnV,GGAP);
    SelCh = recombin('xovsp',SelCh,0.7);
    SelCh = mut(SelCh);

    cg = bs2rv(SelCh,FieldID);
    for nind = 1:size(SelCh,1)
        cmd = ['-v ',num2str(v),' -c ',num2str(cg(nind,1)),' -g ',num2str(cg(nind,2))];
        ObjVSel(nind,1) = svmtrain(train_label,train_data,cmd);
    end

    [Chrom,ObjV] = reins(Chrom,SelCh,1,1,ObjV,ObjVSel);

    if max(ObjV) <= 50
        continue;
    end

    [NewBestCVaccuracy,I] = max(ObjV);
    cg_temp = bs2rv(Chrom,FieldID);
    temp_NewBestCVaccuracy = NewBestCVaccuracy;

    if NewBestCVaccuracy > BestCVaccuracy
       BestCVaccuracy = NewBestCVaccuracy;
       Bestc = cg_temp(I,1);
       Bestg = cg_temp(I,2);
    end

    if abs( NewBestCVaccuracy-BestCVaccuracy ) <= 10^(-2) && ...
        cg_temp(I,1) < Bestc
       BestCVaccuracy = NewBestCVaccuracy;
       Bestc = cg_temp(I,1);
       Bestg = cg_temp(I,2);
    end

    trace(gen,1) = max(ObjV);
    trace(gen,2) = sum(ObjV)/length(ObjV);

end
%
figure;
hold on;
trace = round(trace*10000)/10000;
plot(trace(1:gen,1),'r*-','LineWidth',1.5);
plot(trace(1:gen,2),'o-','LineWidth',1.5);
legend('&#26368;&#20339;&#36866;&#24212;&#24230;','&#24179;&#22343;&#36866;&#24212;&#24230;',3);
xlabel('&#36827;&#21270;&#20195;&#25968;','FontSize',12);
ylabel('&#36866;&#24212;&#24230;','FontSize',12);
axis([0 gen 0 100]);
grid on;
axis auto;

line1 = '&#36866;&#24212;&#24230;&#26354;&#32447;Accuracy[GAmethod]';
line2 = ['(&#32456;&#27490;&#20195;&#25968;=', ...
    num2str(gen),',&#31181;&#32676;&#25968;&#37327;pop=', ...
    num2str(NIND),')'];
line3 = ['Best c=',num2str(Bestc),' g=',num2str(Bestg), ...
    ' CVAccuracy=',num2str(BestCVaccuracy),'%'];
title({line1;line2;line3},'FontSize',12);

      Published with MATLAB&reg; 7.14

 BestCVaccuracy
       BestCVaccuracy = NewBestCVaccuracy;
       Bestc = cg_temp(I,1);
       Bestg = cg_temp(I,2);
    end
    
    if abs( NewBestCVaccuracy-BestCVaccuracy )
