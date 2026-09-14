Chapter_ModelDecryption
-
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- A Little Clean Work
- &#20998;&#31867;&#27169;&#22411;model&#35299;&#23494;
- &#39564;&#35777;&#33258;&#24049;&#36890;&#36807;&#20915;&#31574;&#20989;&#25968;&#39044;&#27979;&#30340;&#26631;&#31614;&#21644;svmpredict&#32473;&#20986;&#30340;&#26631;&#31614;&#30456;&#21516;
- DecisionFunctionfunction Chapter_ModelDecryption

## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% LIBSVM&#21442;&#25968;&#23454;&#20363;&#35814;&#35299;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## A Little Clean Work
clear;
clc;
close all;
format compact;
&#39318;&#20808;&#36733;&#20837;&#25968;&#25454;

load heart_scale;
data = heart_scale_inst;
label = heart_scale_label;
% &#24314;&#31435;&#20998;&#31867;&#27169;&#22411;
model = svmtrain(label,data,'-s 0 -t 2 -c 1.2 -g 2.8');
% &#21033;&#29992;&#24314;&#31435;&#30340;&#27169;&#22411;&#30475;&#20854;&#22312;&#35757;&#32451;&#38598;&#21512;&#19978;&#30340;&#20998;&#31867;&#25928;&#26524;
[PredictLabel,accuracy] = svmpredict(label,data,model);
accuracy
Accuracy = 99.6296% (269/270) (classification)
accuracy =
   99.6296
    0.0148
    0.9851

## &#20998;&#31867;&#27169;&#22411;model&#35299;&#23494;
model
Parameters = model.Parameters
Label = model.Label
nr_class = model.nr_class
totalSV = model.totalSV
nSV = model.nSV
model =
    Parameters: [5x1 double]
      nr_class: 2
       totalSV: 259
           rho: 0.0514
         Label: [2x1 double]
         ProbA: []
         ProbB: []
           nSV: [2x1 double]
       sv_coef: [259x1 double]
           SVs: [259x13 double]
Parameters =
         0
    2.0000
    3.0000
    2.8000
         0
Label =
     1
    -1
nr_class =
     2
totalSV =
   259
nSV =
   118
   141
plable = zeros(270,1);
for i = 1:270
    x = data(i,:);
    plabel(i,1) = DecisionFunction(x,model);
end

## &#39564;&#35777;&#33258;&#24049;&#36890;&#36807;&#20915;&#31574;&#20989;&#25968;&#39044;&#27979;&#30340;&#26631;&#31614;&#21644;svmpredict&#32473;&#20986;&#30340;&#26631;&#31614;&#30456;&#21516;
flag = sum(plabel == PredictLabel)
flag =
   270

## DecisionFunction
function plabel = DecisionFunction(x,model)

gamma = model.Parameters(4);
RBF = @(u,v)( exp(-gamma.*sum( (u-v).^2) ) );

len = length(model.sv_coef);
y = 0;

for i = 1:len
    u = model.SVs(i,:);
    y = y + model.sv_coef(i)*RBF(u,x);
end
b = -model.rho;
y = y + b;

if y >= 0
    plabel = 1;
else
    plabel = -1;
end

      Published with MATLAB&reg; 7.14

= 0

    plabel = 1;

else

    plabel = -1;

end
##### SOURCE END #####
-->
