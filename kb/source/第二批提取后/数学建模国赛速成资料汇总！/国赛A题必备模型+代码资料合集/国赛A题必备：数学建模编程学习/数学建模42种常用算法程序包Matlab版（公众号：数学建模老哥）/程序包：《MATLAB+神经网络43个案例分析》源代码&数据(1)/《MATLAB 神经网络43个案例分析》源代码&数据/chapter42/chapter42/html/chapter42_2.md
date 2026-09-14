chapter42_2
-
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25171;&#24320;matlabpool
- &#21152;&#36733;&#25968;&#25454;
- &#21019;&#24314;&#19968;&#20010;&#25311;&#21512;&#31070;&#32463;&#32593;&#32476;
- &#25351;&#23450;&#36755;&#20837;&#19982;&#36755;&#20986;&#22788;&#29702;&#20989;&#25968;(&#26412;&#25805;&#20316;&#24182;&#38750;&#24517;&#39035;)
- &#35774;&#32622;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#12289;&#39564;&#35777;&#12289;&#27979;&#35797;&#25968;&#25454;&#38598;&#21010;&#20998;
- &#35774;&#32622;&#32593;&#32476;&#30340;&#35757;&#32451;&#20989;&#25968;
- &#35774;&#32622;&#32593;&#32476;&#30340;&#35823;&#24046;&#20989;&#25968;
- &#35774;&#32622;&#32593;&#32476;&#21487;&#35270;&#21270;&#20989;&#25968;
- &#21333;&#32447;&#31243;&#32593;&#32476;&#35757;&#32451;
- &#24182;&#34892;&#32593;&#32476;&#35757;&#32451;
- &#32593;&#32476;&#25928;&#26524;&#39564;&#35777;
- &#31070;&#32463;&#32593;&#32476;&#21487;&#35270;&#21270;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#24182;&#34892;&#36816;&#31639;&#19982;&#31070;&#32463;&#32593;&#32476;-&#22522;&#20110;CPU/GPU&#30340;&#24182;&#34892;&#31070;&#32463;&#32593;&#32476;&#36816;&#31639;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003
% &#26412;&#20195;&#30721;&#20026;&#26696;&#20363;&#20195;&#30721;

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clear all
clc
warning off

## &#25171;&#24320;matlabpool
matlabpool open
poolsize=matlabpool('size');
Starting matlabpool using the 'local' profile ... connected to 2 workers.

## &#21152;&#36733;&#25968;&#25454;
load bodyfat_dataset
inputs = bodyfatInputs;
targets = bodyfatTargets;

## &#21019;&#24314;&#19968;&#20010;&#25311;&#21512;&#31070;&#32463;&#32593;&#32476;
hiddenLayerSize = 10;   % &#38544;&#34255;&#23618;&#31070;&#32463;&#20803;&#20010;&#25968;&#20026;10
net = fitnet(hiddenLayerSize);  % &#21019;&#24314;&#32593;&#32476;

## &#>
net = fitnet(hiddenLayerSize);  % &#21019;&#24314;&#32593;&#32476;

## &#>
net = fitnet(hiddenLayerSize);
net.inputs{1}.processFcns = {'removeconstantrows','mapminmax'};
net.outputs{2}.processFcns = {'removeconstantrows','mapminmax'};

## &#35774;&#32622;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#12289;&#39564;&#35777;&#12289;&#27979;&#35797;&#25968;&#25454;&#38598;&#21010;&#20998;
net.divideFcn = 'dividerand';  % &#38543;&#26426;&#21010;&#20998;&#25968;&#25454;&#38598;
net.divideMode = 'sample';  %  &#21010;&#20998;&#21333;&#20301;&#20026;&#27599;&#19968;&#20010;&#25968;&#25454;
net.divideParam.trainRatio = 70/100; %&#35757;&#32451;&#38598;&#27604;&#20363;
net.divideParam.valRatio = 15/100; %&#39564;&#35777;&#38598;&#27604;&#20363;
net.divideParam.testRatio = 15/100; %&#27979;&#35797;&#38598;&#27604;&#20363;

## &#35774;&#32622;&#32593;&#32476;&#30340;&#35757;&#32451;&#20989;&#25968;
net.trainFcn = 'trainlm';  % Levenberg-Marquardt

## &#35774;&#32622;&#32593;&#32476;&#30340;&#35823;&#24046;&#20989;&#25968;
net.performFcn = 'mse';  % Mean squared error

## &#35774;&#32622;&#32593;&#32476;&#21487;&#35270;&#21270;&#20989;&#25968;
net.plotFcns = {'plotperform','plottrainstate','ploterrhist', ...
  'plotregression', 'plotfit'};

## &#21333;&#32447;&#31243;&#32593;&#32476;&#35757;&#32451;
tic
[net1,tr1] = train(net,inputs,targets);
t1=toc;
disp(['&#21333;&#32447;&#31243;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#26102;&#38388;&#20026;',num2str(t1),'&#31186;']);
&#21333;&#32447;&#31243;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#26102;&#38388;&#20026;0.93209&#31186;

## &#24182;&#34892;&#32593;&#32476;&#35757;&#32451;
tic
[net2,tr2] = train(net,inputs,targets,'useParallel','yes','showResources','yes');
t2=toc;
disp(['&#24182;&#34892;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#26102;&#38388;&#20026;',num2str(t2),'&#31186;']);

Computing Resources:
Parallel Workers:
  Worker 1 on Wang_Matlab, MEX on PCWIN
  Worker 2 on Wang_Matlab, MEX on PCWIN

Lab 1:

  Training with TRAINLM.
  Epoch 0/1000, Time 0.096, Performance 7115.2407/0, Gradient 12833.5776/1e-07, Mu 0.001/10000000000, Validation Checks 0/6
  Epoch 12/1000, Time 0.397, Performance 5.1658/0, Gradient 3.4342/1e-07, Mu 0.01/10000000000, Validation Checks 6/6
  Training with TRAINLM completed: Validation stop.

&#24182;&#34892;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#26102;&#38388;&#20026;2.2013&#31186;

## &#32593;&#32476;&#25928;&#26524;&#39564;&#35777;
outputs1 = sim(net1,inputs);
outputs2 = sim(net2,inputs);
errors1 = gsubtract(targets,outputs1);
errors2 = gsubtract(targets,outputs2);
performance1 = perform(net1,targets,outputs1)
performance2 = perform(net2,targets,outputs2)

performance1 =

   19.6247

performance2 =

   14.5379

## &#31070;&#32463;&#32593;&#32476;&#21487;&#35270;&#21270;
figure, plotperform(tr1);
figure, plotperform(tr2);
figure, plottrainstate(tr1);
figure, plottrainstate(tr2);
figure,plotregression(targets,outputs1);
figure,plotregression(targets,outputs2);
figure,ploterrhist(errors1);
figure,ploterrhist(errors2);

matlabpool close
Sending a stop signal to all the workers ... stopped.

Published with MATLAB&reg; R2012b
