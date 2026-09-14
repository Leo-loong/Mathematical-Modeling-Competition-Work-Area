SVM&#31070;&#32463;&#32593;&#32476;&#30340;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;---&#19978;&#35777;&#25351;&#25968;&#24320;&#30424;&#25351;&#25968;&#39044;&#27979;
# SVM&#31070;&#32463;&#32593;&#32476;&#30340;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;---&#19978;&#35777;&#25351;&#25968;&#24320;&#30424;&#25351;&#25968;&#39044;&#27979;

			该案例作者申明：				1：本人长期驻扎在此板块里，对该案例提问，做到有问必答。	2：此案例有配套的教学视频，配套的完整可运行Matlab程序。						3：以下内容为该案例的部分内容（约占该案例完整内容的1/10）。							4：此案例为原创案例，转载请注明出处（Matlab中文论坛，《Matlab神经网络30个案例分析》）。							5：若此案例碰巧与您的研究有关联，我们欢迎您提意见，要求等，我们考虑后可以加在案例里。							6：您看到的以下内容为初稿，书籍的实际内容可能有少许出入，以书籍实际发行内容为准。					7：此书其他常见问题、预定方式等，请点击这里。

## Contents

- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25968;&#25454;&#30340;&#25552;&#21462;&#21644;&#39044;&#22788;&#29702;
- &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
- &#21033;&#29992;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
- SVM&#32593;&#32476;&#22238;&#24402;&#39044;&#27979;
- &#32467;&#26524;&#20998;&#26512;
- &#23376;&#20989;&#25968; SVMcgForRegress.m
## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter14
tic;
close all;
clear;
clc;
format compact;

## &#25968;&#25454;&#30340;&#25552;&#21462;&#21644;&#39044;&#22788;&#29702;
% &#36733;&#20837;&#27979;&#35797;&#25968;&#25454;&#19978;&#35777;&#25351;&#25968;(1990.12.19-2009.08.19)
% &#25968;&#25454;&#26159;&#19968;&#20010;4579*6&#30340;double&#22411;&#30340;&#30697;&#38453;,&#27599;&#19968;&#34892;&#34920;&#31034;&#27599;&#19968;&#22825;&#30340;&#19978;&#35777;&#25351;&#25968;
% 6&#21015;&#20998;&#21035;&#34920;&#31034;&#24403;&#22825;&#19978;&#35777;&#25351;&#25968;&#30340;&#24320;&#30424;&#25351;&#25968;,&#25351;&#25968;&#26368;&#39640;&#20540;,&#25351;&#25968;&#26368;&#20302;&#20540;,&#25910;&#30424;&#25351;&#25968;,&#24403;&#26085;&#20132;&#26131;&#37327;,&#24403;&#26085;&#20132;&#26131;&#39069;.
load chapter14_sh.mat;

% &#25552;&#21462;&#25968;&#25454;
[m,n] = size(sh);
ts = sh(2:m,1);
tsx = sh(1:m-1,:);

% &#30011;&#20986;&#21407;&#22987;&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;
figure;
plot(ts,'LineWidth',2);
title('&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;(1990.12.20-2009.08.19)','FontSize',12);
grid on;
% print -dtiff -r600 original;

% &#25968;&#25454;&#39044;&#22788;&#29702;,&#23558;&#21407;&#22987;&#25968;&#25454;&#36827;&#34892;&#24402;&#19968;&#21270;
ts = ts';
tsx = tsx';

% mapminmax&#20026;matlab&#33258;&#24102;&#30340;&#26144;&#23556;&#20989;&#25968;
% &#23545;ts&#36827;&#34892;&#24402;&#19968;&#21270;
[TS,TSps] = mapminmax(ts,1,2);

% &#30011;&#20986;&#21407;&#22987;&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;
figure;
plot(TS,'LineWidth',2);
title('&#21407;&#22987;&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;','FontSize',12);
grid on;
% print -dtiff -r600 scale;
% &#23545;TS&#36827;&#34892;&#36716;&#32622;,&#20197;&#31526;&#21512;libsvm&#24037;&#20855;&#31665;&#30340;&#25968;&#25454;&#26684;&#24335;&#35201;&#27714;
TS = TS';

% mapminmax&#20026;matlab&#33258;&#24102;&#30340;&#26144;&#23556;&#20989;&#25968;
% &#23545;tsx&#36827;&#34892;&#24402;&#19968;&#21270;
[TSX,TSXps] = mapminmax(tsx,1,2);
% &#23545;TSX&#36827;&#34892;&#36716;&#32622;,&#20197;&#31526;&#21512;libsvm&#24037;&#20855;&#31665;&#30340;&#25968;&#25454;&#26684;&#24335;&#35201;&#27714;
TSX = TSX';

## &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% &#39318;&#20808;&#36827;&#34892;&#31895;&#30053;&#36873;&#25321;:
[bestmse,bestc,bestg] = SVMcgForRegress(TS,TSX,-8,8,-8,8);

% &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#26681;&#25454;&#31895;&#30053;&#36873;&#25321;&#30340;&#32467;&#26524;&#22270;&#20877;&#36827;&#34892;&#31934;&#32454;&#36873;&#25321;:
[bestmse,bestc,bestg] = SVMcgForRegress(TS,TSX,-4,4,-4,4,3,0.5,0.5,0.05);

% &#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);
&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation MSE = 0.000961388 Best c = 0.25 Best g = 2
&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
Best Cross Validation MSE = 0.000961388 Best c = 0.25 Best g = 2

## &#21033;&#29992;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
cmd = ['-c ', num2str(bestc), ' -g ', num2str(bestg) , ' -s 3 -p 0.01'];
model = svmtrain(TS,TSX,cmd);

## SVM&#32593;&#32476;&#22238;&#24402;&#39044;&#27979;
[predict,mse] = svmpredict(TS,TSX,model);
predict = mapminmax('reverse',predict',TSps);
predict = predict';

% &#25171;&#21360;&#22238;&#24402;&#32467;&#26524;
str = sprintf( '&#22343;&#26041;&#35823;&#24046; MSE = %g &#30456;&#20851;&#31995;&#25968; R = %g%%',mse(2),mse(3)*100);
disp(str);
Mean squared error = 2.35705e-005 (regression)
Squared correlation coefficient = 0.999195 (regression)
&#22343;&#26041;&#35823;&#24046; MSE = 2.35705e-005 &#30456;&#20851;&#31995;&#25968; R = 99.9195%

## &#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(ts,'o-','LineWidth',1);
plot(predict,'r*-','LineWidth',1);
legend('&#21407;&#22987;&#25968;&#25454;','&#22238;&#24402;&#39044;&#27979;&#25968;&#25454;');
hold off;
grid on;
print -dtiff -r600 result;

figure;
error = predict - ts';
plot(error,'r*');
title('&#35823;&#24046;(predicted data - original data)','FontSize',12);
grid on;
% print -dtiff -r600 resulterror;
snapnow;
toc;
  Elapsed time is 110.417548 seconds.

## &#23376;&#20989;&#25968; SVMcgForRegress.m
function [mse,bestc,bestg] = SVMcgForRegress(train_label,train,cmin,cmax,gmin,gmax,v,cstep,gstep,msestep)
% SVMcgForClass
% &#36755;&#20837;:
% train_label:&#35757;&#32451;&#38598;&#26631;&#31614;(&#24453;&#22238;&#24402;&#30340;&#21464;&#37327;).&#35201;&#27714;&#19982;libsvm&#24037;&#20855;&#31665;&#20013;&#35201;&#27714;&#19968;&#33268;.
% train:&#35757;&#32451;&#38598;(&#22240;&#21464;&#37327;).&#35201;&#27714;&#19982;libsvm&#24037;&#20855;&#31665;&#20013;&#35201;&#27714;&#19968;&#33268;.
% cmin:&#24809;&#32602;&#21442;&#25968;c&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; c_min = 2^(cmin).&#40664;&#35748;&#20026; -5
% cmax:&#24809;&#32602;&#21442;&#25968;c&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#22823;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; c_max = 2^(cmax).&#40664;&#35748;&#20026; 5
% gmin:&#21442;&#25968;g&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; g_min = 2^(gmin).&#40664;&#35748;&#20026; -5
% gmax:&#21442;&#25968;g&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; g_min = 2^(gmax).&#40664;&#35748;&#20026; 5
% v:cross validation&#30340;&#21442;&#25968;,&#21363;&#32473;&#27979;&#35797;&#38598;&#20998;&#20026;&#20960;&#37096;&#20998;&#36827;&#34892;cross validation.&#40664;&#35748;&#20026; 3
% cstep:&#21442;&#25968;c&#27493;&#36827;&#30340;&#22823;&#23567;.&#40664;&#35748;&#20026; 1
% gstep:&#21442;&#25968;g&#27493;&#36827;&#30340;&#22823;&#23567;.&#40664;&#35748;&#20026; 1
% msestep:&#26368;&#21518;&#26174;&#31034;MSE&#22270;&#26102;&#30340;&#27493;&#36827;&#22823;&#23567;.&#40664;&#35748;&#20026; 0.1
% &#36755;&#20986;:
% mse:Cross Validation &#36807;&#31243;&#20013;&#30340;&#26368;&#20302;&#30340;&#22343;&#26041;&#35823;&#24046;
% bestc:&#26368;&#20339;&#30340;&#21442;&#25968;c
% bestg:&#26368;&#20339;&#30340;&#21442;&#25968;g

% about the parameters of SVMcgForRegress
if nargin < 10
    msestep = 0.1;
end
if nargin < 7
    v = 3;
    cstep = 1;
    gstep = 1;
end
if nargin < 6
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
end
if nargin < 5
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
    gmin = -5;
end
if nargin < 4
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
    gmin = -5;
    cmax = 5;
end
if nargin < 3
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
    gmin = -5;
    cmax = 5;
    cmin = -5;
end
% X:c Y:g cg:mse
[X,Y] = meshgrid(cmin:cstep:cmax,gmin:gstep:gmax);
[m,n] = size(X);
cg = zeros(m,n);
% record accuracy with different c & g,and find the best mse with the smallest c
bestc = 0;
bestg = 0;
mse = 10^10;
basenum = 2;
for i = 1:m
    for j = 1:n
        cmd = ['-v ',num2str(v),' -c ',num2str( basenum^X(i,j) ),' -g ',num2str( basenum^Y(i,j) ),' -s 3'];
        cg(i,j) = svmtrain(train_label, train, cmd);

        if cg(i,j) < mse
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end
        if ( cg(i,j) == mse && bestc > basenum^X(i,j) )
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

    end
end
% draw the accuracy with different c & g
[cg,ps] = mapminmax(cg,0,1);
figure;
subplot(1,2,1);
[C,h] = contour(X,Y,cg,0:msestep:0.5);
clabel(C,h,'FontSize',10,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
title('&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(&#31561;&#39640;&#32447;&#22270;)','FontSize',12);
grid on;

subplot(1,2,2);
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,0,1]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('MSE','FontSize',12);
title('&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(3D&#35270;&#22270;)','FontSize',12);
% filename = ['c',num2str(bestc),'g',num2str(bestg),num2str(msestep),'.tif'];
% print('-dtiff','-r600',filename);

			版权所有：Matlab中文论坛

      Published with MATLAB&reg; 7.9

% 			该案例作者申明：				1：本人长期驻扎在此板块里，对该案例提问，做到有问必答。	2：此案例有配套的教学视频，配套的完整可运行Matlab程序。						3：以下内容为该案例的部分内容（约占该案例完整内容的1/10）。							4：此案例为原创案例，转载请注明出处（Matlab中文论坛，《Matlab神经网络30个案例分析》）。							5：若此案例碰巧与您的研究有关联，我们欢迎您提意见，要求等，我们考虑后可以加在案例里。							6：您看到的以下内容为初稿，书籍的实际内容可能有少许出入，以书籍实际发行内容为准。					7：此书其他常见问题、预定方式等，请点击这里。
%
%

%% 清空环境变量
function chapter14
tic;
close all;
clear;
clc;
format compact;
%% 数据的提取和预处理

% 载入测试数据上证指数(1990.12.19-2009.08.19)
% 数据是一个4579*6的double型的矩阵,每一行表示每一天的上证指数
% 6列分别表示当天上证指数的开盘指数,指数最高值,指数最低值,收盘指数,当日交易量,当日交易额.
load chapter14_sh.mat;

% 提取数据
[m,n] = size(sh);
ts = sh(2:m,1);
tsx = sh(1:m-1,:);

% 画出原始上证指数的每日开盘数
figure;
plot(ts,'LineWidth',2);
title('上证指数的每日开盘数(1990.12.20-2009.08.19)','FontSize',12);
grid on;
% print -dtiff -r600 original;

% 数据预处理,将原始数据进行归一化
ts = ts';
tsx = tsx';

% mapminmax为matlab自带的映射函数
% 对ts进行归一化
[TS,TSps] = mapminmax(ts,1,2);

% 画出原始上证指数的每日开盘数归一化后的图像
figure;
plot(TS,'LineWidth',2);
title('原始上证指数的每日开盘数归一化后的图像','FontSize',12);
grid on;
% print -dtiff -r600 scale;
% 对TS进行转置,以符合libsvm工具箱的数据格式要求
TS = TS';

% mapminmax为matlab自带的映射函数
% 对tsx进行归一化
[TSX,TSXps] = mapminmax(tsx,1,2);
% 对TSX进行转置,以符合libsvm工具箱的数据格式要求
TSX = TSX';

%% 选择回归预测分析最佳的SVM参数c&g

% 首先进行粗略选择:
[bestmse,bestc,bestg] = SVMcgForRegress(TS,TSX,-8,8,-8,8);

% 打印粗略选择结果
disp('打印粗略选择结果');
str = sprintf( 'Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% 根据粗略选择的结果图再进行精细选择:
[bestmse,bestc,bestg] = SVMcgForRegress(TS,TSX,-4,4,-4,4,3,0.5,0.5,0.05);

% 打印精细选择结果
disp('打印精细选择结果');
str = sprintf( 'Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

%% 利用回归预测分析最佳的参数进行SVM网络训练
cmd = ['-c ', num2str(bestc), ' -g ', num2str(bestg) , ' -s 3 -p 0.01'];
model = svmtrain(TS,TSX,cmd);

%% SVM网络回归预测
[predict,mse] = svmpredict(TS,TSX,model);
predict = mapminmax('reverse',predict',TSps);
predict = predict';

% 打印回归结果
str = sprintf( '均方误差 MSE = %g 相关系数 R = %g%%',mse(2),mse(3)*100);
disp(str);

%% 结果分析
figure;
hold on;
plot(ts,'o-','LineWidth',1);
plot(predict,'r*-','LineWidth',1);
legend('原始数据','回归预测数据');
hold off;
grid on;
print -dtiff -r600 result;

figure;
error = predict - ts';
plot(error,'r*');
title('误差(predicted data - original data)','FontSize',12);
grid on;
% print -dtiff -r600 resulterror;
snapnow;
toc;

%% 子函数 SVMcgForRegress.m
function [mse,bestc,bestg] = SVMcgForRegress(train_label,train,cmin,cmax,gmin,gmax,v,cstep,gstep,msestep)
% SVMcgForClass
% 输入:
% train_label:训练集标签(待回归的变量).要求与libsvm工具箱中要求一致.
% train:训练集(因变量).要求与libsvm工具箱中要求一致.
% cmin:惩罚参数c的变化范围的最小值(取以2为底的对数后),即 c_min = 2^(cmin).默认为 -5
% cmax:惩罚参数c的变化范围的最大值(取以2为底的对数后),即 c_max = 2^(cmax).默认为 5
% gmin:参数g的变化范围的最小值(取以2为底的对数后),即 g_min = 2^(gmin).默认为 -5
% gmax:参数g的变化范围的最小值(取以2为底的对数后),即 g_min = 2^(gmax).默认为 5
% v:cross validation的参数,即给测试集分为几部分进行cross validation.默认为 3
% cstep:参数c步进的大小.默认为 1
% gstep:参数g步进的大小.默认为 1
% msestep:最后显示MSE图时的步进大小.默认为 0.1
% 输出:
% mse:Cross Validation 过程中的最低的均方误差
% bestc:最佳的参数c
% bestg:最佳的参数g

% about the parameters of SVMcgForRegress
if nargin  basenum^X(i,j) )
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

    end
end
% draw the accuracy with different c & g
[cg,ps] = mapminmax(cg,0,1);
figure;
subplot(1,2,1);
[C,h] = contour(X,Y,cg,0:msestep:0.5);
clabel(C,h,'FontSize',10,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
title('参数选择结果图(等高线图)','FontSize',12);
grid on;

subplot(1,2,2);
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,0,1]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('MSE','FontSize',12);
title('参数选择结果图(3D视图)','FontSize',12);
% filename = ['c',num2str(bestc),'g',num2str(bestg),num2str(msestep),'.tif'];
% print('-dtiff','-r600',filename);

%%%
%
%
% 			版权所有：Matlab中文论坛
%
%

##### SOURCE END #####
-->
