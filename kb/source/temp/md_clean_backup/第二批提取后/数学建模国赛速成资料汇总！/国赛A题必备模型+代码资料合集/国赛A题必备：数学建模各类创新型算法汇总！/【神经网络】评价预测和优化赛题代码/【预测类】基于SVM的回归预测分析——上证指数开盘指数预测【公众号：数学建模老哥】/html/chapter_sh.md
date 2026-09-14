chapter_sh
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25968;&#25454;&#30340;&#25552;&#21462;&#21644;&#39044;&#22788;&#29702;
- &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
- &#21033;&#29992;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#26368;&#20339;&#30340;&#21442;&#25968;&#36827;&#34892;SVM&#32593;&#32476;&#35757;&#32451;
- SVM&#32593;&#32476;&#22238;&#24402;&#39044;&#27979;
- &#32467;&#26524;&#20998;&#26512;
- &#23376;&#20989;&#25968; SVMcgForRegress.m
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#22522;&#20110;SVM&#30340;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#8212;&#8212;&#19978;&#35777;&#25351;&#25968;&#24320;&#30424;&#25351;&#25968;&#39044;&#27979;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter_sh
tic;
close all;
clear;
clc;
format compact;

## &#25968;&#25454;&#30340;&#25552;&#21462;&#21644;&#39044;&#22788;&#29702;
% &#36733;&#20837;&#27979;&#35797;&#25968;&#25454;&#19978;&#35777;&#25351;&#25968;(1990.12.19-2009.08.19)
% &#25968;&#25454;&#26159;&#19968;&#20010;4579*6&#30340;double&#22411;&#30340;&#30697;&#38453;,&#27599;&#19968;&#34892;&#34920;&#31034;&#27599;&#19968;&#22825;&#30340;&#19978;&#35777;&#25351;&#25968;
% 6&#21015;&#20998;&#21035;&#34920;&#31034;&#24403;&#22825;&#19978;&#35777;&#25351;&#25968;&#30340;&#24320;&#30424;&#25351;&#25968;,&#25351;&#25968;&#26368;&#39640;&#20540;,&#25351;&#25968;&#26368;&#20302;&#20540;,&#25910;&#30424;&#25351;&#25968;,&#24403;&#26085;&#20132;&#26131;&#37327;,&#24403;&#26085;&#20132;&#26131;&#39069;.
load chapter_sh.mat;

% &#25552;&#21462;&#25968;&#25454;
[m,n] = size(sh);
ts = sh(2:m,1);
tsx = sh(1:m-1,:);

% &#30011;&#20986;&#21407;&#22987;&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;
figure;
plot(ts,'LineWidth',2);
title('&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;(1990.12.20-2009.08.19)','FontSize',12);
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#24320;&#30424;&#25968;','FontSize',12);
grid on;

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
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#24402;&#19968;&#21270;&#21518;&#30340;&#24320;&#30424;&#25968;','FontSize',12);
grid on;
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
Best Cross Validation MSE = 0.000916702 Best c = 0.329877 Best g = 1.7411
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
Mean squared error = 2.35705e-05 (regression)
Squared correlation coefficient = 0.999195 (regression)
&#22343;&#26041;&#35823;&#24046; MSE = 2.35705e-05 &#30456;&#20851;&#31995;&#25968; R = 99.9195%

## &#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(ts,'-o');
plot(predict,'r-^');
legend('&#21407;&#22987;&#25968;&#25454;','&#22238;&#24402;&#39044;&#27979;&#25968;&#25454;');
hold off;
title('&#21407;&#22987;&#25968;&#25454;&#21644;&#22238;&#24402;&#39044;&#27979;&#25968;&#25454;&#23545;&#27604;','FontSize',12);
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#24320;&#30424;&#25968;','FontSize',12);
grid on;

figure;
error = predict - ts';
plot(error,'rd');
title('&#35823;&#24046;&#22270;(predicted data - original data)','FontSize',12);
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#35823;&#24046;&#37327;','FontSize',12);
grid on;

figure;
error = (predict - ts')./ts';
plot(error,'rd');
title('&#30456;&#23545;&#35823;&#24046;&#22270;(predicted data - original data)/original data','FontSize',12);
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#30456;&#23545;&#35823;&#24046;&#37327;','FontSize',12);
grid on;
snapnow;
toc;
   Elapsed time is 128.622808 seconds.

## &#23376;&#20989;&#25968; SVMcgForRegress.m
function [mse,bestc,bestg] = SVMcgForRegress(train_label,train,cmin,cmax,gmin,gmax,v,cstep,gstep,msestep)
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
    msestep = 0.06;
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
% X:c Y:g cg:acc
[X,Y] = meshgrid(cmin:cstep:cmax,gmin:gstep:gmax);
[m,n] = size(X);
cg = zeros(m,n);

eps = 10^(-4);

bestc = 0;
bestg = 0;
mse = Inf;
basenum = 2;
for i = 1:m
    for j = 1:n
        cmd = ['-v ',num2str(v),' -c ',num2str( basenum^X(i,j) ),' -g ',num2str( basenum^Y(i,j) ),' -s 3 -p 0.1'];
        cg(i,j) = svmtrain(train_label, train, cmd);

        if cg(i,j) < mse
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

        if abs( cg(i,j)-mse )<=eps && bestc > basenum^X(i,j)
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end

    end
end
% to draw the acc with different c & g
[cg,ps] = mapminmax(cg,0,1);
figure;
[C,h] = contour(X,Y,cg,0:msestep:0.5);
clabel(C,h,'FontSize',10,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
firstline = 'SVR&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(&#31561;&#39640;&#32447;&#22270;)[GridSearchMethod]';
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVmse=',num2str(mse)];
title({firstline;secondline},'Fontsize',12);
grid on;

figure;
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,0,1]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('MSE','FontSize',12);
firstline = 'SVR&#21442;&#25968;&#36873;&#25321;&#32467;&#26524;&#22270;(3D&#35270;&#22270;)[GridSearchMethod]';
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVmse=',num2str(mse)];
title({firstline;secondline},'Fontsize',12);

      Published with MATLAB&reg; 7.14

 basenum^X(i,j)
            mse = cg(i,j);
            bestc = basenum^X(i,j);
            bestg = basenum^Y(i,j);
        end
        
    end
end
% to draw the acc with different c & g
[cg,ps] = mapminmax(cg,0,1);
figure;
[C,h] = contour(X,Y,cg,0:msestep:0.5);
clabel(C,h,'FontSize',10,'Color','r');
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
firstline = 'SVR参数选择结果图(等高线图)[GridSearchMethod]'; 
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVmse=',num2str(mse)];
title({firstline;secondline},'Fontsize',12);
grid on;

figure;
meshc(X,Y,cg);
% mesh(X,Y,cg);
% surf(X,Y,cg);
axis([cmin,cmax,gmin,gmax,0,1]);
xlabel('log2c','FontSize',12);
ylabel('log2g','FontSize',12);
zlabel('MSE','FontSize',12);
firstline = 'SVR参数选择结果图(3D视图)[GridSearchMethod]'; 
secondline = ['Best c=',num2str(bestc),' g=',num2str(bestg), ...
    ' CVmse=',num2str(mse)];
title({firstline;secondline},'Fontsize',12);
##### SOURCE END #####
-->
