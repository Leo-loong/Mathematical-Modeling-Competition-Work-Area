chapter7_1
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#20135;&#29983;&#36755;&#20837; &#36755;&#20986;&#25968;&#25454;
- &#32593;&#32476;&#24314;&#31435;&#21644;&#35757;&#32451;
- &#32593;&#32476;&#30340;&#25928;&#26524;&#39564;&#35777;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% RBF&#32593;&#32476;&#30340;&#22238;&#24402;--&#38750;&#32447;&#24615;&#20989;&#25968;&#22238;&#24402;&#30340;&#23454;&#29616;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clc
clear

## &#20135;&#29983;&#36755;&#20837; &#36755;&#20986;&#25968;&#25454;
&#35774;&#32622;&#27493;&#38271;

interval=0.01;

% &#20135;&#29983;x1 x2
x1=-1.5:interval:1.5;
x2=-1.5:interval:1.5;

% &#25353;&#29031;&#20989;&#25968;&#20808;&#27714;&#24471;&#30456;&#24212;&#30340;&#20989;&#25968;&#20540;&#65292;&#20316;&#20026;&#32593;&#32476;&#30340;&#36755;&#20986;&#12290;
F =20+x1.^2-10*cos(2*pi*x1)+x2.^2-10*cos(2*pi*x2);

## &#32593;&#32476;&#24314;&#31435;&#21644;&#35757;&#32451;
&#32593;&#32476;&#24314;&#31435; &#36755;&#20837;&#20026;[x1;x2],&#36755;&#20986;&#20026;F&#12290;Spread&#20351;&#29992;&#40664;&#35748;&#12290;

net=newrbe([x1;x2],F)
Warning: Rank deficient, rank = 21, tol =  6.683543e-14. 

net =

    Neural Network
 
              name: 'Radial Basis Network, Exact'
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
 numWeightElements: 1205
        sampleTime: 1
 
    connections:
 
       biasConnect: [1; 1]
      inputConnect: [1; 0]
      layerConnect: [0 0; 1 0]
     outputConnect: [0 1]
 
    subobjects:
 
            inputs: {1x1 cell array of 1 input}
            layers: {2x1 cell array of 2 layers}
           outputs: {1x2 cell array of 1 output}
            biases: {2x1 cell array of 2 biases}
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
                 b: {2x1 cell} containing 2 bias vectors
 
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
 

## &#32593;&#32476;&#30340;&#25928;&#26524;&#39564;&#35777;
% &#25105;&#20204;&#23558;&#21407;&#25968;&#25454;&#22238;&#24102;&#65292;&#27979;&#35797;&#32593;&#32476;&#25928;&#26524;&#65306;
ty=sim(net,[x1;x2]);

% &#25105;&#20204;&#20351;&#29992;&#22270;&#20687;&#26469;&#30475;&#32593;&#32476;&#23545;&#38750;&#32447;&#24615;&#20989;&#25968;&#30340;&#25311;&#21512;&#25928;&#26524;
figure
plot3(x1,x2,F,'rd');
hold on;
plot3(x1,x2,ty,'b-.');
view(113,36)
title('&#21487;&#35270;&#21270;&#30340;&#26041;&#27861;&#35266;&#23519;&#20934;&#30830;RBF&#31070;&#32463;&#32593;&#32476;&#30340;&#25311;&#21512;&#25928;&#26524;')
xlabel('x1')
ylabel('x2')
zlabel('F')
grid on
 
Published with MATLAB&reg; R2012b
