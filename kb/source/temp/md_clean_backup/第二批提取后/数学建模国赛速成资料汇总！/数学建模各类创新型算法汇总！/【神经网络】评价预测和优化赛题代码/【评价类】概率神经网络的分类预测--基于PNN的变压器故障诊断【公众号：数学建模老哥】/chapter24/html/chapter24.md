chapter24
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#25968;&#25454;&#36733;&#20837;
- &#36873;&#21462;&#35757;&#32451;&#25968;&#25454;&#21644;&#27979;&#35797;&#25968;&#25454;
- &#23558;&#26399;&#26395;&#31867;&#21035;&#36716;&#25442;&#20026;&#21521;&#37327;
- &#20351;&#29992;newpnn&#20989;&#25968;&#24314;&#31435;PNN SPREAD&#36873;&#21462;&#20026;1.5
- &#35757;&#32451;&#25968;&#25454;&#22238;&#20195; &#26597;&#30475;&#32593;&#32476;&#30340;&#20998;&#31867;&#25928;&#26524;
- &#36890;&#36807;&#20316;&#22270; &#35266;&#23519;&#32593;&#32476;&#23545;&#35757;&#32451;&#25968;&#25454;&#20998;&#31867;&#25928;&#26524;
- &#32593;&#32476;&#39044;&#27979;&#26410;&#30693;&#25968;&#25454;&#25928;&#26524;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#27010;&#29575;&#31070;&#32463;&#32593;&#32476;&#30340;&#20998;&#31867;&#39044;&#27979;--&#22522;&#20110;PNN&#30340;&#21464;&#21387;&#22120;&#25925;&#38556;&#35786;&#26029;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clc;
clear all
close all
nntwarn off;
warning off;

## &#25968;&#25454;&#36733;&#20837;
load data

## &#36873;&#21462;&#35757;&#32451;&#25968;&#25454;&#21644;&#27979;&#35797;&#25968;&#25454;
Train=data(1:23,:);
Test=data(24:end,:);
p_train=Train(:,1:3)';
t_train=Train(:,4)';
p_test=Test(:,1:3)';
t_test=Test(:,4)';

## &#23558;&#26399;&#26395;&#31867;&#21035;&#36716;&#25442;&#20026;&#21521;&#37327;
t_train=ind2vec(t_train);
t_train_temp=Train(:,4)';

## &#20351;&#29992;newpnn&#20989;&#25968;&#24314;&#31435;PNN SPREAD&#36873;&#21462;&#20026;1.5
Spread=1.5;
net=newpnn(p_train,t_train,Spread)

net =

    Neural Network
 
              name: 'Probabilistic Neural Network'
        efficiency: .cacheDelayedInputs, .flattenTime,
                    .memoryReduction
          userdata: (your custom info)
 
    dimensions:
 
         numInputs: 1
         numLayers: 2
        numOutputs: 1
    numInputDelays: 0
    numLayerDelays: 0
 numFeedbackDelays: 0
 numWeightElements: 207
        sampleTime: 1
 
    connections:
 
       biasConnect: [1; 0]
      inputConnect: [1; 0]
      layerConnect: [0 0; 1 0]
     outputConnect: [0 1]
 
    subobjects:
 
            inputs: {1x1 cell array of 1 input}
            layers: {2x1 cell array of 2 layers}
           outputs: {1x2 cell array of 1 output}
            biases: {2x1 cell array of 1 bias}
      inputWeights: {2x1 cell array of 1 weight}
      layerWeights: {2x2 cell array of 1 weight}
 
    functions:
 
          adaptFcn: (none)
        adaptParam: (none)
          derivFcn: 'defaultderiv'
         divideFcn: (none)
       divideParam: (none)
        divideMode: 'sample'
           initFcn: 'initlay'
        performFcn: 'mse'
      performParam: .regularization, .normalization
          plotFcns: {}
        plotParams: {1x0 cell array of 0 params}
          trainFcn: (none)
        trainParam: (none)
 
    weight and bias values:
 
                IW: {2x1 cell} containing 1 input weight matrix
                LW: {2x2 cell} containing 1 layer weight matrix
                 b: {2x1 cell} containing 1 bias vector
 
    methods:
 
             adapt: Learn while in continuous use
         configure: Configure inputs & outputs
            gensim: Generate Simulink model
              init: Initialize weights & biases
           perform: Calculate performance
               sim: Evaluate network outputs given inputs
             train: Train network with examples
              view: View diagram
       unconfigure: Unconfigure inputs & outputs
 

## &#35757;&#32451;&#25968;&#25454;&#22238;&#20195; &#26597;&#30475;&#32593;&#32476;&#30340;&#20998;&#31867;&#25928;&#26524;
% Sim&#20989;&#25968;&#36827;&#34892;&#32593;&#32476;&#39044;&#27979;
Y=sim(net,p_train);
% &#23558;&#32593;&#32476;&#36755;&#20986;&#21521;&#37327;&#36716;&#25442;&#20026;&#25351;&#38024;
Yc=vec2ind(Y);

## &#36890;&#36807;&#20316;&#22270; &#35266;&#23519;&#32593;&#32476;&#23545;&#35757;&#32451;&#25968;&#25454;&#20998;&#31867;&#25928;&#26524;
figure(1)
subplot(1,2,1)
stem(1:length(Yc),Yc,'bo')
hold on
stem(1:length(Yc),t_train_temp,'r*')
title('PNN &#32593;&#32476;&#35757;&#32451;&#21518;&#30340;&#25928;&#26524;')
xlabel('&#26679;&#26412;&#32534;&#21495;')
ylabel('&#20998;&#31867;&#32467;&#26524;')
set(gca,'Ytick',[1:5])
subplot(1,2,2)
H=Yc-t_train_temp;
stem(H)
title('PNN &#32593;&#32476;&#35757;&#32451;&#21518;&#30340;&#35823;&#24046;&#22270;')
xlabel('&#26679;&#26412;&#32534;&#21495;')
 
## &#32593;&#32476;&#39044;&#27979;&#26410;&#30693;&#25968;&#25454;&#25928;&#26524;
Y2=sim(net,p_test);
Y2c=vec2ind(Y2);
figure(2)
stem(1:length(Y2c),Y2c,'b^')
hold on
stem(1:length(Y2c),t_test,'r*')
title('PNN &#32593;&#32476;&#30340;&#39044;&#27979;&#25928;&#26524;')
xlabel('&#39044;&#27979;&#26679;&#26412;&#32534;&#21495;')
ylabel('&#20998;&#31867;&#32467;&#26524;')
set(gca,'Ytick',[1:5])
 
Published with MATLAB&reg; R2012b
