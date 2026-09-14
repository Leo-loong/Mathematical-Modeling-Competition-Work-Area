chapter40
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#21152;&#36733;&#25968;&#25454;
- &#24314;&#31435;&#38750;&#32447;&#24615;&#33258;&#22238;&#24402;&#27169;&#22411;
- &#32593;&#32476;&#25968;&#25454;&#39044;&#22788;&#29702;&#20989;&#25968;&#23450;&#20041;
- &#26102;&#38388;&#24207;&#21015;&#25968;&#25454;&#20934;&#22791;&#24037;&#20316;
- &#35757;&#32451;&#25968;&#25454;&#12289;&#39564;&#35777;&#25968;&#25454;&#12289;&#27979;&#35797;&#25968;&#25454;&#21010;&#20998;
- &#32593;&#32476;&#35757;&#32451;&#20989;&#25968;&#35774;&#23450;
- &#35823;&#24046;&#20989;&#25968;&#35774;&#23450;
- &#32472;&#22270;&#20989;&#25968;&#35774;&#23450;
- &#32593;&#32476;&#35757;&#32451;
- &#32593;&#32476;&#27979;&#35797;
- &#35745;&#31639;&#35757;&#32451;&#38598;&#12289;&#39564;&#35777;&#38598;&#12289;&#27979;&#35797;&#38598;&#35823;&#24046;
- &#32593;&#32476;&#35757;&#32451;&#25928;&#26524;&#21487;&#35270;&#21270;
- close loop&#27169;&#24335;&#30340;&#23454;&#29616;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#21160;&#24577;&#31070;&#32463;&#32593;&#32476;&#26102;&#38388;&#24207;&#21015;&#39044;&#27979;&#30740;&#31350;-&#22522;&#20110;MATLAB&#30340;NARX&#23454;&#29616;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clear
clc

## &#21152;&#36733;&#25968;&#25454;
load phdata
inputSeries = phInputs;
targetSeries = phTargets;

## &#24314;&#31435;&#38750;&#32447;&#24615;&#33258;&#22238;&#24402;&#27169;&#22411;
inputDelays = 1:2;
feedbackDelays = 1:2;
hiddenLayerSize = 10;
net = narxnet(inputDelays,feedbackDelays,hiddenLayerSize);

## &#32593;&#32476;&#25968;&#25454;&#39044;&#22788;&#29702;&#20989;&#25968;&#23450;&#20041;
net.inputs{1}.processFcns = {'removeconstantrows','mapminmax'};
net.inputs{2}.processFcns = {'removeconstantrows','mapminmax'};

## &#26102;&#38388;&#24207;&#21015;&#25968;&#25454;&#20934;&#22791;&#24037;&#20316;
[inputs,inputStates,layerStates,targets] = preparets(net,inputSeries,{},targetSeries);

## &#35757;&#32451;&#25968;&#25454;&#12289;&#39564;&#35777;&#25968;&#25454;&#12289;&#27979;&#35797;&#25968;&#25454;&#21010;&#20998;
net.divideFcn = 'dividerand';
net.divideMode = 'value';
net.divideParam.trainRatio = 70/100;
net.divideParam.valRatio = 15/100;
net.divideParam.testRatio = 15/100;

## &#32593;&#32476;&#35757;&#32451;&#20989;&#25968;&#35774;&#23450;
net.trainFcn = 'trainlm';  % Levenberg-Marquardt

## &#35823;&#24046;&#20989;&#25968;&#35774;&#23450;
net.performFcn = 'mse';  % Mean squared error

## &#32472;&#22270;&#20989;&#25968;&#35774;&#23450;
net.plotFcns = {'plotperform','plottrainstate','plotresponse', ...
  'ploterrcorr', 'plotinerrcorr'};

## &#32593;&#32476;&#35757;&#32451;
[net,tr] = train(net,inputs,targets,inputStates,layerStates);

## &#32593;&#32476;&#27979;&#35797;
outputs = net(inputs,inputStates,layerStates);
errors = gsubtract(targets,outputs);
performance = perform(net,targets,outputs)

performance =

    0.0091

## &#35745;&#31639;&#35757;&#32451;&#38598;&#12289;&#39564;&#35777;&#38598;&#12289;&#27979;&#35797;&#38598;&#35823;&#24046;
trainTargets = gmultiply(targets,tr.trainMask);
valTargets = gmultiply(targets,tr.valMask);
testTargets = gmultiply(targets,tr.testMask);
trainPerformance = perform(net,trainTargets,outputs)
valPerformance = perform(net,valTargets,outputs)
testPerformance = perform(net,testTargets,outputs)

trainPerformance =

    0.0091

valPerformance =

    0.0076

testPerformance =

    0.0111

## &#32593;&#32476;&#35757;&#32451;&#25928;&#26524;&#21487;&#35270;&#21270;
figure, plotperform(tr)
figure, plottrainstate(tr)
figure, plotregression(targets,outputs)
figure, plotresponse(targets,outputs)
figure, ploterrcorr(errors)
figure, plotinerrcorr(inputs,errors)
      
## close loop&#27169;&#24335;&#30340;&#23454;&#29616;
&#26356;&#25913;NARX&#31070;&#32463;&#32593;&#32476;&#27169;&#24335;

narx_net_closed = closeloop(net);
view(net)
view(narx_net_closed)

% &#35745;&#31639;1500-2000&#20010;&#28857;&#30340;&#25311;&#21512;&#25928;&#26524;
phInputs_c=phInputs(1500:2000);
PhTargets_c=phTargets(1500:2000);

[p1,Pi1,Ai1,t1] = preparets(narx_net_closed,phInputs_c,{},PhTargets_c);
% &#32593;&#32476;&#20223;&#30495;
yp1 = narx_net_closed(p1,Pi1,Ai1);
plot([cell2mat(yp1)' cell2mat(t1)'])
   
Published with MATLAB&reg; R2012b
