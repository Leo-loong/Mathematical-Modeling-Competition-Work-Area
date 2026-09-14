chapter_PSO
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
- &#23376;&#20989;&#25968; psoSVMcgForClass.m
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% SVM&#30340;&#21442;&#25968;&#20248;&#21270;&#8212;&#8212;&#22914;&#20309;&#26356;&#22909;&#30340;&#25552;&#21319;&#20998;&#31867;&#22120;&#30340;&#24615;&#33021;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter_PSO
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
[bestacc,bestc,bestg] = psoSVMcgForClass(train_wine_labels,train_wine);

% &#25171;&#21360;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation Accuracy = %g%% Best c = %g Best g = %g',bestacc,bestc,bestg);
disp(str);
&#25171;&#21360;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation Accuracy = 98.8764% Best c = 33.0915 Best g = 4.10411
 
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
Accuracy = 97.7528% (87/89) (classification)
&#25171;&#21360;&#27979;&#35797;&#38598;&#20998;&#31867;&#20934;&#30830;&#29575;
Accuracy = 97.7528% (87/89)

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
 
## &#23376;&#20989;&#25968; psoSVMcgForClass.m
function [bestCVaccuarcy,bestc,bestg,pso_option] = psoSVMcgForClass(train_label,train,pso_option)
% psoSVMcgForClass

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
    pso_option = struct('c1',1.5,'c2',1.7,'maxgen',200,'sizepop',20, ...
        'k',0.6,'wV',1,'wP',1,'v',5, ...
        'popcmax',10^2,'popcmin',10^(-1),'popgmax',10^3,'popgmin',10^(-2));
end
% c1:&#21021;&#22987;&#20026;1.5,pso&#21442;&#25968;&#23616;&#37096;&#25628;&#32034;&#33021;&#21147;
% c2:&#21021;&#22987;&#20026;1.7,pso&#21442;&#25968;&#20840;&#23616;&#25628;&#32034;&#33021;&#21147;
% maxgen:&#21021;&#22987;&#20026;200,&#26368;&#22823;&#36827;&#21270;&#25968;&#37327;
% sizepop:&#21021;&#22987;&#20026;20,&#31181;&#32676;&#26368;&#22823;&#25968;&#37327;
% k:&#21021;&#22987;&#20026;0.6(k belongs to [0.1,1.0]),&#36895;&#29575;&#21644;x&#30340;&#20851;&#31995;(V = kX)
% wV:&#21021;&#22987;&#20026;1(wV best belongs to [0.8,1.2]),&#36895;&#29575;&#26356;&#26032;&#20844;&#24335;&#20013;&#36895;&#24230;&#21069;&#38754;&#30340;&#24377;&#24615;&#31995;&#25968;
% wP:&#21021;&#22987;&#20026;1,&#31181;&#32676;&#26356;&#26032;&#20844;&#24335;&#20013;&#36895;&#24230;&#21069;&#38754;&#30340;&#24377;&#24615;&#31995;&#25968;
% v:&#21021;&#22987;&#20026;3,SVM Cross Validation&#21442;&#25968;
% popcmax:&#21021;&#22987;&#20026;100,SVM &#21442;&#25968;c&#30340;&#21464;&#21270;&#30340;&#26368;&#22823;&#20540;.
% popcmin:&#21021;&#22987;&#20026;0.1,SVM &#21442;&#25968;c&#30340;&#21464;&#21270;&#30340;&#26368;&#23567;&#20540;.
% popgmax:&#21021;&#22987;&#20026;1000,SVM &#21442;&#25968;g&#30340;&#21464;&#21270;&#30340;&#26368;&#22823;&#20540;.
% popgmin:&#21021;&#22987;&#20026;0.01,SVM &#21442;&#25968;c&#30340;&#21464;&#21270;&#30340;&#26368;&#23567;&#20540;.

Vcmax = pso_option.k*pso_option.popcmax;
Vcmin = -Vcmax ;
Vgmax = pso_option.k*pso_option.popgmax;
Vgmin = -Vgmax ;

eps = 10^(-3);

% &#20135;&#29983;&#21021;&#22987;&#31890;&#23376;&#21644;&#36895;&#24230;
for i=1:pso_option.sizepop

    % &#38543;&#26426;&#20135;&#29983;&#31181;&#32676;&#21644;&#36895;&#24230;
    pop(i,1) = (pso_option.popcmax-pso_option.popcmin)*rand+pso_option.popcmin;
    pop(i,2) = (pso_option.popgmax-pso_option.popgmin)*rand+pso_option.popgmin;
    V(i,1)=Vcmax*rands(1,1);
    V(i,2)=Vgmax*rands(1,1);

    % &#35745;&#31639;&#21021;&#22987;&#36866;&#24212;&#24230;
    cmd = ['-v ',num2str(pso_option.v),' -c ',num2str( pop(i,1) ),' -g ',num2str( pop(i,2) )];
    fitness(i) = svmtrain(train_label, train, cmd);
    fitness(i) = -fitness(i);
end

% &#25214;&#26497;&#20540;&#21644;&#26497;&#20540;&#28857;
[global_fitness bestindex]=min(fitness); % &#20840;&#23616;&#26497;&#20540;
local_fitness=fitness;   % &#20010;&#20307;&#26497;&#20540;&#21021;&#22987;&#21270;

global_x=pop(bestindex,:);   % &#20840;&#23616;&#26497;&#20540;&#28857;
local_x=pop;    % &#20010;&#20307;&#26497;&#20540;&#28857;&#21021;&#22987;&#21270;

% &#27599;&#19968;&#20195;&#31181;&#32676;&#30340;&#24179;&#22343;&#36866;&#24212;&#24230;
avgfitness_gen = zeros(1,pso_option.maxgen);

% &#36845;&#20195;&#23547;&#20248;
for i=1:pso_option.maxgen

    for j=1:pso_option.sizepop

        %&#36895;&#24230;&#26356;&#26032;
        V(j,:) = pso_option.wV*V(j,:) + pso_option.c1*rand*(local_x(j,:) - pop(j,:)) + pso_option.c2*rand*(global_x - pop(j,:));
        if V(j,1) > Vcmax
            V(j,1) = Vcmax;
        end
        if V(j,1) < Vcmin
            V(j,1) = Vcmin;
        end
        if V(j,2) > Vgmax
            V(j,2) = Vgmax;
        end
        if V(j,2) < Vgmin
            V(j,2) = Vgmin;
        end

        %&#31181;&#32676;&#26356;&#26032;
        pop(j,:)=pop(j,:) + pso_option.wP*V(j,:);
        if pop(j,1) > pso_option.popcmax
            pop(j,1) = pso_option.popcmax;
        end
        if pop(j,1) < pso_option.popcmin
            pop(j,1) = pso_option.popcmin;
        end
        if pop(j,2) > pso_option.popgmax
            pop(j,2) = pso_option.popgmax;
        end
        if pop(j,2) < pso_option.popgmin
            pop(j,2) = pso_option.popgmin;
        end

        % &#33258;&#36866;&#24212;&#31890;&#23376;&#21464;&#24322;
        if rand>0.5
            k=ceil(2*rand);
            if k == 1
                pop(j,k) = (20-1)*rand+1;
            end
            if k == 2
                pop(j,k) = (pso_option.popgmax-pso_option.popgmin)*rand + pso_option.popgmin;
            end
        end

        %&#36866;&#24212;&#24230;&#20540;
        cmd = ['-v ',num2str(pso_option.v),' -c ',num2str( pop(j,1) ),' -g ',num2str( pop(j,2) )];
        fitness(j) = svmtrain(train_label, train, cmd);
        fitness(j) = -fitness(j);

        cmd_temp = ['-c ',num2str( pop(j,1) ),' -g ',num2str( pop(j,2) )];
        model = svmtrain(train_label, train, cmd_temp);

        if fitness(j) >= -65
            continue;
        end

        %&#20010;&#20307;&#26368;&#20248;&#26356;&#26032;
        if fitness(j) < local_fitness(j)
            local_x(j,:) = pop(j,:);
            local_fitness(j) = fitness(j);
        end

        if abs( fitness(j)-local_fitness(j) )<=eps && pop(j,1) < local_x(j,1)
            local_x(j,:) = pop(j,:);
            local_fitness(j) = fitness(j);
        end

        %&#32676;&#20307;&#26368;&#20248;&#26356;&#26032;
        if fitness(j) < global_fitness
            global_x = pop(j,:);
            global_fitness = fitness(j);
        end

        if abs( fitness(j)-global_fitness )<=eps && pop(j,1) < global_x(1)
            global_x = pop(j,:);
            global_fitness = fitness(j);
        end

    end

    fit_gen(i) = global_fitness;
    avgfitness_gen(i) = sum(fitness)/pso_option.sizepop;
end

% &#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(-fit_gen,'r*-','LineWidth',1.5);
plot(-avgfitness_gen,'o-','LineWidth',1.5);
legend('&#26368;&#20339;&#36866;&#24212;&#24230;','&#24179;&#22343;&#36866;&#24212;&#24230;',3);
xlabel('&#36827;&#21270;&#20195;&#25968;','FontSize',12);
ylabel('&#36866;&#24212;&#24230;','FontSize',12);
grid on;

bestc = global_x(1);
bestg = global_x(2);
bestCVaccuarcy = -fit_gen(pso_option.maxgen);

line1 = '&#36866;&#24212;&#24230;&#26354;&#32447;Accuracy[PSOmethod]';
line2 = ['(&#21442;&#25968;c1=',num2str(pso_option.c1), ...
    ',c2=',num2str(pso_option.c2),',&#32456;&#27490;&#20195;&#25968;=', ...
    num2str(pso_option.maxgen),',&#31181;&#32676;&#25968;&#37327;pop=', ...
    num2str(pso_option.sizepop),')'];
line3 = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVAccuracy=',num2str(bestCVaccuarcy),'%'];
title({line1;line2;line3},'FontSize',12);

      Published with MATLAB&reg; 7.14

 Vcmax
            V(j,1) = Vcmax;
        end
        if V(j,1)  Vgmax
            V(j,2) = Vgmax;
        end
        if V(j,2)  pso_option.popcmax
            pop(j,1) = pso_option.popcmax;
        end
        if pop(j,1)  pso_option.popgmax
            pop(j,2) = pso_option.popgmax;
        end
        if pop(j,2) 0.5
            k=ceil(2*rand);
            if k == 1
                pop(j,k) = (20-1)*rand+1;
            end
            if k == 2
                pop(j,k) = (pso_option.popgmax-pso_option.popgmin)*rand + pso_option.popgmin;
            end
        end
        
        %适应度值
        cmd = ['-v ',num2str(pso_option.v),' -c ',num2str( pop(j,1) ),' -g ',num2str( pop(j,2) )];
        fitness(j) = svmtrain(train_label, train, cmd);
        fitness(j) = -fitness(j);
        
        cmd_temp = ['-c ',num2str( pop(j,1) ),' -g ',num2str( pop(j,2) )];
        model = svmtrain(train_label, train, cmd_temp);
        
        if fitness(j) >= -65
            continue;
        end
        
        %个体最优更新
        if fitness(j)
