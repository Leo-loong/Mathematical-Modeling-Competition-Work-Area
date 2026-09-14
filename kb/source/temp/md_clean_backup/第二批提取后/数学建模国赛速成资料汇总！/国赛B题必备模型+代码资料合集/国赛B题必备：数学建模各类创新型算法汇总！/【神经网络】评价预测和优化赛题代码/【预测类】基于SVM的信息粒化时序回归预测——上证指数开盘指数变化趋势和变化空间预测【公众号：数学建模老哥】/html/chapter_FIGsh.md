chapter_FIGsh
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#21407;&#22987;&#25968;&#25454;&#30340;&#25552;&#21462;
- &#23545;&#21407;&#22987;&#25968;&#25454;&#36827;&#34892;&#27169;&#31946;&#20449;&#24687;&#31890;&#21270;
- &#21033;&#29992;SVM&#23545;Low&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
- &#23545;&#20110;Low&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
- &#21033;&#29992;SVM&#23545;R&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
- &#23545;&#20110;R&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
- &#21033;&#29992;SVM&#23545;Up&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
- &#23545;&#20110;Up&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
- &#23376;&#20989;&#25968; SVMcgForRegress.m
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#22522;&#20110;SVM&#30340;&#20449;&#24687;&#31890;&#21270;&#26102;&#24207;&#22238;&#24402;&#39044;&#27979;&#8212;&#8212;&#19978;&#35777;&#25351;&#25968;&#24320;&#30424;&#25351;&#25968;&#21464;&#21270;&#36235;&#21183;&#21644;&#21464;&#21270;&#31354;&#38388;&#39044;&#27979;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
function chapter_FIGsh
tic;
close all;
clear;
clc;
format compact;

## &#21407;&#22987;&#25968;&#25454;&#30340;&#25552;&#21462;
% &#36733;&#20837;&#27979;&#35797;&#25968;&#25454;&#19978;&#35777;&#25351;&#25968;(1990.12.19-2009.08.19)
% &#25968;&#25454;&#26159;&#19968;&#20010;4579*6&#30340;double&#22411;&#30340;&#30697;&#38453;,&#27599;&#19968;&#34892;&#34920;&#31034;&#27599;&#19968;&#22825;&#30340;&#19978;&#35777;&#25351;&#25968;
% 6&#21015;&#20998;&#21035;&#34920;&#31034;&#24403;&#22825;&#19978;&#35777;&#25351;&#25968;&#30340;&#24320;&#30424;&#25351;&#25968;,&#25351;&#25968;&#26368;&#39640;&#20540;,&#25351;&#25968;&#26368;&#20302;&#20540;,&#25910;&#30424;&#25351;&#25968;,&#24403;&#26085;&#20132;&#26131;&#37327;,&#24403;&#26085;&#20132;&#26131;&#39069;.
load chapter_sh.mat;

% &#25552;&#21462;&#25968;&#25454;
ts = sh_open;
time = length(ts);

% &#30011;&#20986;&#21407;&#22987;&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;
figure;
plot(ts,'LineWidth',2);
title('&#19978;&#35777;&#25351;&#25968;&#30340;&#27599;&#26085;&#24320;&#30424;&#25968;(1990.12.20-2009.08.19)','FontSize',12);
xlabel('&#20132;&#26131;&#26085;&#22825;&#25968;(1990.12.19-2009.08.19)','FontSize',12);
ylabel('&#24320;&#30424;&#25968;','FontSize',12);
grid on;
print -dtiff -r600 original;

snapnow;
 
## &#23545;&#21407;&#22987;&#25968;&#25454;&#36827;&#34892;&#27169;&#31946;&#20449;&#24687;&#31890;&#21270;
win_num = floor(time/5);
tsx = 1:win_num;
tsx = tsx';
[Low,R,Up]=FIG_D(ts','triangle',win_num);

% &#27169;&#31946;&#20449;&#24687;&#31890;&#21270;&#21487;&#35270;&#21270;&#22270;
figure;
hold on;
plot(Low,'b+');
plot(R,'r*');
plot(Up,'gx');
hold off;
legend('Low','R','Up',2);
title('&#27169;&#31946;&#20449;&#24687;&#31890;&#21270;&#21487;&#35270;&#21270;&#22270;','FontSize',12);
xlabel('&#31890;&#21270;&#31383;&#21475;&#25968;&#30446;','FontSize',12);
ylabel('&#31890;&#21270;&#20540;','FontSize',12);
grid on;
print -dtiff -r600 FIGpic;

snapnow;
 
## &#21033;&#29992;SVM&#23545;Low&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
% &#25968;&#25454;&#39044;&#22788;&#29702;,&#23558;Low&#36827;&#34892;&#24402;&#19968;&#21270;&#22788;&#29702;
% mapminmax&#20026;matlab&#33258;&#24102;&#30340;&#26144;&#23556;&#20989;&#25968;
[low,low_ps] = mapminmax(Low);
low_ps.ymin = 100;
low_ps.ymax = 500;
% &#23545;Low&#36827;&#34892;&#24402;&#19968;&#21270;
[low,low_ps] = mapminmax(Low,low_ps);
% &#30011;&#20986;Low&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;
figure;
plot(low,'b+');
title('Low&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;','FontSize',12);
xlabel('&#31890;&#21270;&#31383;&#21475;&#25968;&#30446;','FontSize',12);
ylabel('&#24402;&#19968;&#21270;&#21518;&#30340;&#31890;&#21270;&#20540;','FontSize',12);
grid on;
print -dtiff -r600 lowscale;
% &#23545;low&#36827;&#34892;&#36716;&#32622;,&#20197;&#31526;&#21512;libsvm&#24037;&#20855;&#31665;&#30340;&#25968;&#25454;&#26684;&#24335;&#35201;&#27714;
low = low';
snapnow;

% &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#20013;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% &#39318;&#20808;&#36827;&#34892;&#31895;&#30053;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(low,tsx,-10,10,-10,10,3,1,1,0.1,1);

% &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for Low:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#26681;&#25454;&#31895;&#30053;&#36873;&#25321;&#30340;&#32467;&#26524;&#22270;&#20877;&#36827;&#34892;&#31934;&#32454;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(low,tsx,-4,8,-10,10,3,0.5,0.5,0.05,1);

% &#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for Low:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#35757;&#32451;SVM
cmd = ['-c ', num2str(bestc), ' -g ', num2str(bestg) , ' -s 3 -p 0.1'];
low_model = svmtrain(low, tsx, cmd);

% &#39044;&#27979;
[low_predict,low_mse] = svmpredict(low,tsx,low_model);
low_predict = mapminmax('reverse',low_predict,low_ps);
predict_low = svmpredict(1,win_num+1,low_model);
predict_low = mapminmax('reverse',predict_low,low_ps);
predict_low
 &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
SVM parameters for Low:Best Cross Validation MSE = 35.0883 Best c = 256 Best g = 0.03125
&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
SVM parameters for Low:Best Cross Validation MSE = 35.0178 Best c = 256 Best g = 0.0220971
Mean squared error = 22.0053 (regression)
Squared correlation coefficient = 0.995366 (regression)
Mean squared error = 85135.8 (regression)
Squared correlation coefficient = -1.#IND (regression)
predict_low =
   2.7968e+03
  
## &#23545;&#20110;Low&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(Low,'b+');
plot(low_predict,'r*');
legend('original low','predict low',2);
title('original vs predict','FontSize',12);
xlabel('&#31890;&#21270;&#31383;&#21475;&#25968;&#30446;','FontSize',12);
ylabel('&#31890;&#21270;&#20540;','FontSize',12);
grid on;
print -dtiff -r600 lowresult;

figure;
error = low_predict - Low';
plot(error,'ro');
title('&#35823;&#24046;(predicted data-original data)','FontSize',12);
xlabel('&#31890;&#21270;&#31383;&#21475;&#25968;&#30446;','FontSize',12);
ylabel('&#35823;&#24046;&#37327;','FontSize',12);
grid on;
print -dtiff -r600 lowresulterror;

snapnow;
  
## &#21033;&#29992;SVM&#23545;R&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
% &#25968;&#25454;&#39044;&#22788;&#29702;,&#23558;R&#36827;&#34892;&#24402;&#19968;&#21270;&#22788;&#29702;
% mapminmax&#20026;matlab&#33258;&#24102;&#30340;&#26144;&#23556;&#20989;&#25968;
[r,r_ps] = mapminmax(R);
r_ps.ymin = 100;
r_ps.ymax = 500;
% &#23545;R&#36827;&#34892;&#24402;&#19968;&#21270;
[r,r_ps] = mapminmax(R,r_ps);
% &#30011;&#20986;R&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;
figure;
plot(r,'r*');
title('r&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;','FontSize',12);
grid on;
% &#23545;R&#36827;&#34892;&#36716;&#32622;,&#20197;&#31526;&#21512;libsvm&#24037;&#20855;&#31665;&#30340;&#25968;&#25454;&#26684;&#24335;&#35201;&#27714;
r = r';
snapnow;

% &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#20013;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% &#39318;&#20808;&#36827;&#34892;&#31895;&#30053;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(r,tsx,-10,10,-10,10,3,1,1,0.1);

% &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for R:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#26681;&#25454;&#31895;&#30053;&#36873;&#25321;&#30340;&#32467;&#26524;&#22270;&#20877;&#36827;&#34892;&#31934;&#32454;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(r,tsx,-4,8,-10,10,3,0.5,0.5,0.05);

% &#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for R:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#35757;&#32451;SVM
cmd = ['-c ', num2str(bestc), ' -g ', num2str(bestg) , ' -s 3 -p 0.1'];
r_model = svmtrain(r, tsx, cmd);

% &#39044;&#27979;
[r_predict,r_mse] = svmpredict(r,tsx,low_model);
r_predict = mapminmax('reverse',r_predict,r_ps);
predict_r = svmpredict(1,win_num+1,r_model);
predict_r = mapminmax('reverse',predict_r,r_ps);
predict_r
 &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
SVM parameters for R:Best Cross Validation MSE = 22.7821 Best c = 256 Best g = 0.03125
&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
SVM parameters for R:Best Cross Validation MSE = 22.7821 Best c = 256 Best g = 0.03125
Mean squared error = 26.2002 (regression)
Squared correlation coefficient = 0.995899 (regression)
Mean squared error = 84653.5 (regression)
Squared correlation coefficient = -1.#IND (regression)
predict_r =
   2.9500e+03
  
## &#23545;&#20110;R&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(R,'b+');
plot(r_predict,'r*');
legend('original r','predict r',2);
title('original vs predict','FontSize',12);
grid on;
figure;
error = r_predict - R';
plot(error,'ro');
title('&#35823;&#24046;(predicted data-original data)','FontSize',12);
grid on;
snapnow;
  
## &#21033;&#29992;SVM&#23545;Up&#36827;&#34892;&#22238;&#24402;&#39044;&#27979;
% &#25968;&#25454;&#39044;&#22788;&#29702;,&#23558;up&#36827;&#34892;&#24402;&#19968;&#21270;&#22788;&#29702;
% mapminmax&#20026;matlab&#33258;&#24102;&#30340;&#26144;&#23556;&#20989;&#25968;
[up,up_ps] = mapminmax(Up);
up_ps.ymin = 100;
up_ps.ymax = 500;
% &#23545;Up&#36827;&#34892;&#24402;&#19968;&#21270;
[up,up_ps] = mapminmax(Up,up_ps);
% &#30011;&#20986;Up&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;
figure;
plot(up,'gx');
title('Up&#24402;&#19968;&#21270;&#21518;&#30340;&#22270;&#20687;','FontSize',12);
grid on;
% &#23545;up&#36827;&#34892;&#36716;&#32622;,&#20197;&#31526;&#21512;libsvm&#24037;&#20855;&#31665;&#30340;&#25968;&#25454;&#26684;&#24335;&#35201;&#27714;
up = up';
snapnow;

% &#36873;&#25321;&#22238;&#24402;&#39044;&#27979;&#20998;&#26512;&#20013;&#26368;&#20339;&#30340;SVM&#21442;&#25968;c&g
% &#39318;&#20808;&#36827;&#34892;&#31895;&#30053;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(up,tsx,-10,10,-10,10,3,1,1,0.5);

% &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for Up:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#26681;&#25454;&#31895;&#30053;&#36873;&#25321;&#30340;&#32467;&#26524;&#22270;&#20877;&#36827;&#34892;&#31934;&#32454;&#36873;&#25321;
[bestmse,bestc,bestg] = SVMcgForRegress(up,tsx,-4,8,-10,10,3,0.5,0.5,0.2);

% &#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
disp('&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;');
str = sprintf( 'SVM parameters for Up:Best Cross Validation MSE = %g Best c = %g Best g = %g',bestmse,bestc,bestg);
disp(str);

% &#35757;&#32451;SVM
cmd = ['-c ', num2str(bestc), ' -g ', num2str(bestg) , ' -s 3 -p 0.1'];
up_model = svmtrain(up, tsx, cmd);

% &#39044;&#27979;
[up_predict,up_mse] = svmpredict(up,tsx,up_model);
up_predict = mapminmax('reverse',up_predict,up_ps);
predict_up = svmpredict(1,win_num+1,up_model);
predict_up = mapminmax('reverse',predict_up,up_ps);
predict_up
 &#25171;&#21360;&#31895;&#30053;&#36873;&#25321;&#32467;&#26524;
SVM parameters for Up:Best Cross Validation MSE = 23.8759 Best c = 512 Best g = 0.0625
&#25171;&#21360;&#31934;&#32454;&#36873;&#25321;&#32467;&#26524;
SVM parameters for Up:Best Cross Validation MSE = 23.8957 Best c = 256 Best g = 0.0220971
Mean squared error = 11.1079 (regression)
Squared correlation coefficient = 0.997625 (regression)
Mean squared error = 96798.9 (regression)
Squared correlation coefficient = -1.#IND (regression)
predict_up =
   3.2673e+03
  
## &#23545;&#20110;Up&#30340;&#22238;&#24402;&#39044;&#27979;&#32467;&#26524;&#20998;&#26512;
figure;
hold on;
plot(Up,'b+');
plot(up_predict,'r*');
legend('original up','predict up',2);
title('original vs predict','FontSize',12);
grid on;
figure;
error = up_predict - Up';
plot(error,'ro');
title('&#35823;&#24046;(predicted data-original data)','FontSize',12);
grid on;
toc;
snapnow;
Elapsed time is 1171.865134 seconds.
  
## &#23376;&#20989;&#25968; SVMcgForRegress.m
function [mse,bestc,bestg] = SVMcgForRegress(train_label,train,cmin,cmax,gmin,gmax,v,cstep,gstep,msestep,flag)
% SVMcgForClass
% &#36755;&#20837;:
% train_label:&#35757;&#32451;&#38598;&#26631;&#31614;.&#35201;&#27714;&#19982;libsvm&#24037;&#20855;&#31665;&#20013;&#35201;&#27714;&#19968;&#33268;.
% train:&#35757;&#32451;&#38598;.&#35201;&#27714;&#19982;libsvm&#24037;&#20855;&#31665;&#20013;&#35201;&#27714;&#19968;&#33268;.
% cmin:&#24809;&#32602;&#21442;&#25968;c&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; c_min = 2^(cmin).&#40664;&#35748;&#20026; -5
% cmax:&#24809;&#32602;&#21442;&#25968;c&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#22823;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; c_max = 2^(cmax).&#40664;&#35748;&#20026; 5
% gmin:&#21442;&#25968;g&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; g_min = 2^(gmin).&#40664;&#35748;&#20026; -5
% gmax:&#21442;&#25968;g&#30340;&#21464;&#21270;&#33539;&#22260;&#30340;&#26368;&#23567;&#20540;(&#21462;&#20197;2&#20026;&#24213;&#30340;&#23545;&#25968;&#21518;),&#21363; g_min = 2^(gmax).&#40664;&#35748;&#20026; 5
% v:cross validation&#30340;&#21442;&#25968;,&#21363;&#32473;&#27979;&#35797;&#38598;&#20998;&#20026;&#20960;&#37096;&#20998;&#36827;&#34892;cross validation.&#40664;&#35748;&#20026; 3
% cstep:&#21442;&#25968;c&#27493;&#36827;&#30340;&#22823;&#23567;.&#40664;&#35748;&#20026; 1
% gstep:&#21442;&#25968;g&#27493;&#36827;&#30340;&#22823;&#23567;.&#40664;&#35748;&#20026; 1
% msestep:&#26368;&#21518;&#26174;&#31034;MSE&#22270;&#26102;&#30340;&#27493;&#36827;&#22823;&#23567;.&#40664;&#35748;&#20026; 20
% &#36755;&#20986;:
% bestacc:Cross Validation &#36807;&#31243;&#20013;&#30340;&#26368;&#39640;&#20998;&#31867;&#20934;&#30830;&#29575;
% bestc:&#26368;&#20339;&#30340;&#21442;&#25968;c
% bestg:&#26368;&#20339;&#30340;&#21442;&#25968;g

% about the parameters of SVMcgForRegress
if nargin < 11
    flag = 0;
end
if nargin < 10
    msestep = 0.1;
end
if nargin < 7
    msestep = 0.1;
    v = 3;
    cstep = 1;
    gstep = 1;
end
if nargin < 6
    msestep = 0.1;
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
end
if nargin < 5
    msestep = 0.1;
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
    gmin = -5;
end
if nargin < 4
    msestep = 0.1;
    v = 3;
    cstep = 1;
    gstep = 1;
    gmax = 5;
    gmin = -5;
    cmax = 5;
end
if nargin < 3
    msestep = 0.1;
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

filename = ['c',num2str(bestc),'g',num2str(bestg),num2str(msestep),'.tif'];
if flag == 1;
    print('-dtiff','-r600',filename);
end

      Published with MATLAB&reg; 7.14

 basenum^X(i,j) )
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

filename = ['c',num2str(bestc),'g',num2str(bestg),num2str(msestep),'.tif'];
if flag == 1;
    print('-dtiff','-r600',filename);
end

##### SOURCE END #####
-->
