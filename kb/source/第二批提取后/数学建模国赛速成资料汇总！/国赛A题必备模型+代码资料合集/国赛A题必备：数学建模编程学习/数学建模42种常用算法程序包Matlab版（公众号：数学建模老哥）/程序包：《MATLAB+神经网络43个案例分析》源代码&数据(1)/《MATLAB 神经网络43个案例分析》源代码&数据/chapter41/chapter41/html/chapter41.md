chapter41
-
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#24314;&#31435;&#19968;&#20010;&#8220;&#31354;&#8221;&#31070;&#32463;&#32593;&#32476;
- &#36755;&#20837;&#19982;&#32593;&#32476;&#23618;&#25968;&#23450;&#20041;
- &#20351;&#29992;view(net)&#35266;&#23519;&#31070;&#32463;&#32593;&#32476;&#32467;&#26500;&#12290;
- &#38408;&#20540;&#36830;&#25509;&#23450;&#20041;
- &#36755;&#20837;&#19982;&#23618;&#36830;&#25509;&#23450;&#20041;
- &#36755;&#20986;&#36830;&#25509;&#35774;&#32622;
- &#36755;&#20837;&#35774;&#32622;
- &#23618;&#35774;&#32622;
- &#36755;&#20986;&#35774;&#32622;
- &#38408;&#20540;&#65292;&#36755;&#20837;&#26435;&#20540;&#19982;&#23618;&#26435;&#20540;&#35774;&#32622;
- &#23558;&#31070;&#32463;&#32593;&#32476;&#30340;&#26576;&#20123;&#26435;&#20540;&#30340;&#24310;&#36831;&#36827;&#34892;&#35774;&#32622;
- &#32593;&#32476;&#20989;&#25968;&#35774;&#32622;
- &#26435;&#20540;&#38408;&#20540;&#22823;&#23567;&#35774;&#32622;
- &#31070;&#32463;&#32593;&#32476;&#21021;&#22987;&#21270;
- &#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;
- &#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#21442;&#25968;
- &#35757;&#32451;&#32593;&#32476;
- &#20223;&#30495;&#26469;&#26816;&#26597;&#31070;&#32463;&#32593;&#32476;&#26159;&#21542;&#30456;&#24212;&#27491;&#24120;&#12290;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#23450;&#21046;&#31070;&#32463;&#32593;&#32476;&#30340;&#23454;&#29616;-&#31070;&#32463;&#32593;&#32476;&#30340;&#20010;&#24615;&#21270;&#24314;&#27169;&#19982;&#20223;&#30495;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clear all
clc
warning off

## &#24314;&#31435;&#19968;&#20010;&#8220;&#31354;&#8221;&#31070;&#32463;&#32593;&#32476;
net = network

net =

    Neural Network

              name: 'Custom Neural Network'
        efficiency: .cacheDelayedInputs, .flattenTime,
                    .memoryReduction
          userdata: (your custom info)

    dimensions:

         numInputs: 0
         numLayers: 0
        numOutputs: 0
    numInputDelays: 0
    numLayerDelays: 0
 numFeedbackDelays: 0
 numWeightElements: 0
        sampleTime: 1

    connections:

       biasConnect: []
      inputConnect: []
      layerConnect: []
     outputConnect: []

    subobjects:

            inputs: {0x1 cell array of 0 inputs}
            layers: {0x1 cell array of 0 layers}
           outputs: {1x0 cell array of 0 outputs}
            biases: {0x1 cell array of 0 biases}
      inputWeights: {0x0 cell array of 0 weights}
      layerWeights: {0x0 cell array of 0 weights}

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

                IW: {0x0 cell} containing 0 input weight matrices
                LW: {0x0 cell} containing 0 layer weight matrices
                 b: {0x1 cell} containing 0 bias vectors

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

## &#36755;&#20837;&#19982;&#32593;&#32476;&#23618;&#25968;&#23450;&#20041;
net.numInputs = 2;
net.numLayers = 3;

## &#20351;&#29992;view(net)&#35266;&#23519;&#31070;&#32463;&#32593;&#32476;&#32467;&#26500;&#12290;
view(net)
% &#27492;&#26102;&#31070;&#32463;&#32593;&#32476;&#26377;&#20004;&#20010;&#36755;&#20837;&#65292;&#19977;&#20010;&#31070;&#32463;&#20803;&#23618;&#12290;&#20294;&#35831;&#27880;&#24847;&#65306;net.numInputs&#35774;&#32622;&#30340;&#26159;
% &#31070;&#32463;&#32593;&#32476;&#30340;&#36755;&#20837;&#20010;&#25968;&#65292;&#27599;&#20010;&#36755;&#20837;&#30340;&#32500;&#25968;&#26159;&#30001;net.inputs{i}.size&#25511;&#21046;&#12290;

## &#38408;&#20540;&#36830;&#25509;&#23450;&#20041;
net.biasConnect(1) = 1;
net.biasConnect(3) = 1;
% &#25110;&#32773;&#20351;&#29992;net.biasConnect = [1; 0; 1];
view(net)

## &#36755;&#20837;&#19982;&#23618;&#36830;&#25509;&#23450;&#20041;
net.inputConnect(1,1) = 1;
net.inputConnect(2,1) = 1;
net.inputConnect(2,2) = 1;
% &#25110;&#32773;&#20351;&#29992;net.inputConnect = [1 0; 1 1; 0 0];
view(net)
net.layerConnect = [0 0 0; 0 0 0; 1 1 1];
view(net)

## &#36755;&#20986;&#36830;&#25509;&#35774;&#32622;
net.outputConnect = [0 1 1];
view(net)

## &#36755;&#20837;&#35774;&#32622;
net.inputs
net.inputs{1}
net.inputs{1}.processFcns = {'removeconstantrows','mapminmax'};
net.inputs{2}.size = 5;
net.inputs{1}.exampleInput = [0 10 5; 0 3 10];
view(net)

ans =

    [1x1 nnetInput]
    [1x1 nnetInput]

ans =

    Neural Network Input

              name: 'Input'
    feedbackOutput: []
       processFcns: {}
     processParams: {1x0 cell array of 0 params}
   processSettings: {0x0 cell array of 0 settings}
    processedRange: []
     processedSize: 0
             range: []
              size: 0
          userdata: (your custom info)

## &#23618;&#35774;&#32622;
net.layers{1}
% &#23558;&#31070;&#32463;&#32593;&#32476;&#31532;&#19968;&#23618;&#30340;&#31070;&#32463;&#20803;&#20010;&#25968;&#35774;&#32622;&#20026;4&#20010;&#65292;&#20854;&#20256;&#36882;&#20989;&#25968;&#35774;&#32622;&#20026;&#8220;tansig&#8221;&#24182;
% &#23558;&#20854;&#21021;&#22987;&#21270;&#20989;&#25968;&#35774;&#32622;&#20026;Nguyen-Widrow&#20989;&#25968;&#12290;
net.layers{1}.size = 4;
net.layers{1}.transferFcn = 'tansig';
net.layers{1}.initFcn = 'initnw';
% &#23558;&#31532;&#20108;&#23618;&#31070;&#32463;&#20803;&#20010;&#25968;&#35774;&#32622;&#20026;3&#20010;&#65292;&#20854;&#20256;&#36882;&#20989;&#25968;&#35774;&#32622;&#20026;&#8220;logsig&#8221;&#65292;&#24182;&#20351;&#29992;&#8220;initnw&#8221;&#21021;&#22987;&#21270;&#12290;
net.layers{2}.size = 3;
net.layers{2}.transferFcn = 'logsig';
net.layers{2}.initFcn = 'initnw';
% &#23558;&#31532;&#19977;&#23618;&#21021;&#22987;&#21270;&#20989;&#25968;&#35774;&#32622;&#20026;&#8220;initnw&#8221;
net.layers{3}.initFcn = 'initnw';
view(net)

ans =

    Neural Network Layer

              name: 'Layer'
        dimensions: 0
       distanceFcn: (none)
     distanceParam: (none)
         distances: []
           initFcn: 'initwb'
       netInputFcn: 'netsum'
     netInputParam: (none)
         positions: []
             range: []
              size: 0
       topologyFcn: (none)
       transferFcn: 'purelin'
     transferParam: (none)
          userdata: (your custom info)

## &#36755;&#20986;&#35774;&#32622;
net.outputs
net.outputs{2}

ans =

    []    [1x1 nnetOutput]    [1x1 nnetOutput]

ans =

    Neural Network Output

              name: 'Output'
     feedbackInput: []
     feedbackDelay: 0
      feedbackMode: 'none'
       processFcns: {}
     processParams: {1x0 cell array of 0 params}
   processSettings: {0x0 cell array of 0 settings}
    processedRange: [3x2 double]
     processedSize: 3
             range: [3x2 double]
              size: 3
          userdata: (your custom info)

## &#38408;&#20540;&#65292;&#36755;&#20837;&#26435;&#20540;&#19982;&#23618;&#26435;&#20540;&#35774;&#32622;
net.biases
net.biases{1}
net.inputWeights
net.layerWeights

ans =

    [1x1 nnetBias]
    []
    [1x1 nnetBias]

ans =

    Neural Network Bias

           initFcn: (none)
             learn: true
          learnFcn: (none)
        learnParam: (none)
              size: 4
          userdata: (your custom info)

ans =

    [1x1 nnetWeight]                  []
    [1x1 nnetWeight]    [1x1 nnetWeight]
                  []                  []

ans =

                  []                  []                  []
                  []                  []                  []
    [1x1 nnetWeight]    [1x1 nnetWeight]    [1x1 nnetWeight]

## &#23558;&#31070;&#32463;&#32593;&#32476;&#30340;&#26576;&#20123;&#26435;&#20540;&#30340;&#24310;&#36831;&#36827;&#34892;&#35774;&#32622;
net.inputWeights{2,1}.delays = [0 1];
net.inputWeights{2,2}.delays = 1;
net.layerWeights{3,3}.delays = 1;

## &#32593;&#32476;&#20989;&#25968;&#35774;&#32622;
&#23558;&#31070;&#32463;&#32593;&#32476;&#21021;&#22987;&#21270;&#35774;&#32622;&#20026;&#8220;initlay&#8221;&#65292;&#36825;&#26679;&#31070;&#32463;&#32593;&#32476;&#23601;&#21487;&#20197;&#25353;&#29031; &#25105;&#20204;&#35774;&#32622;&#30340;&#23618;&#21021;&#22987;&#21270;&#20989;&#25968;&#8220; initnw&#8221;&#21363;Nguyen-Widrow&#36827;&#34892;&#21021;&#22987;&#21270;&#12290;

net.initFcn = 'initlay';
% &#23558;&#31070;&#32463;&#32593;&#32476;&#30340;&#35823;&#24046;&#35774;&#32622;&#20026;&#8220;mse&#8221;&#65288;mean squared error&#65289;&#65292;&#21516;&#26102;&#23558;&#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#20989;&#25968;
% &#35774;&#32622;&#20026;&#8220;trainlm&#8221;Levenberg-Marquardt backpropagation)&#12290;
net.performFcn = 'mse';
net.trainFcn = 'trainlm';
% &#20026;&#20102;&#20351;&#31070;&#32463;&#32593;&#32476;&#21487;&#20197;&#38543;&#26426;&#21010;&#20998;&#35757;&#32451;&#25968;&#25454;&#38598;&#65292;&#25105;&#20204;&#21487;&#20197;&#23558;divideFcn&#35774;&#32622;&#20026;&#8220;dividerand&#8221;&#12290;
net.divideFcn = 'dividerand';
% &#23558; plot functions&#35774;&#32622;&#20026;&#65306;&#8220;plotperform&#8221;,&#8220;plottrainstate&#8221;
net.plotFcns = {'plotperform','plottrainstate'};

## &#26435;&#20540;&#38408;&#20540;&#22823;&#23567;&#35774;&#32622;
net.IW{1,1}, net.IW{2,1}, net.IW{2,2}
net.LW{3,1}, net.LW{3,2}, net.LW{3,3}
net.b{1}, net.b{3}

ans =

     0     0
     0     0
     0     0
     0     0

ans =

     0     0     0     0
     0     0     0     0
     0     0     0     0

ans =

     0     0     0     0     0
     0     0     0     0     0
     0     0     0     0     0

ans =

   Empty matrix: 0-by-4

ans =

   Empty matrix: 0-by-3

ans =

     []

ans =

     0
     0
     0
     0

ans =

   Empty matrix: 0-by-1

## &#31070;&#32463;&#32593;&#32476;&#21021;&#22987;&#21270;
net = init(net);
net.IW{1,1}

ans =

   -2.7851    0.2880
    2.1169   -1.8327
    0.6403   -2.7258
   -1.8147    2.1323

## &#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;
X = {[0; 0] [2; 0.5]; [2; -2; 1; 0; 1] [-1; -1; 1; 0; 1]};
T = {[1; 1; 1] [0; 0; 0]; 1 -1};
Y = sim(net,X)

Y =

    [3x1 double]    [3x1 double]
    [0x1 double]    [0x1 double]

## &#31070;&#32463;&#32593;&#32476;&#30340;&#35757;&#32451;&#21442;&#25968;
net.trainParam

ans =

    Function Parameters for 'trainlm'

    Show Training Window Feedback   showWindow: true
    Show Command Line Feedback showCommandLine: false
    Command Line Frequency                show: 25
    Maximum Epochs                      epochs: 1000
    Maximum Training Time                 time: Inf
    Performance Goal                      goal: 0
    Minimum Gradient                  min_grad: 1e-07
    Maximum Validation Checks         max_fail: 6
    Mu                                      mu: 0.001
    Mu Decrease Ratio                   mu_dec: 0.1
    Mu Increase Ratio                   mu_inc: 10
    Maximum mu                          mu_max: 10000000000

## &#35757;&#32451;&#32593;&#32476;
net = train(net,X,T);

## &#20223;&#30495;&#26469;&#26816;&#26597;&#31070;&#32463;&#32593;&#32476;&#26159;&#21542;&#30456;&#24212;&#27491;&#24120;&#12290;
Y = sim(net,X)

Y =

    [3x1 double]    [3x1 double]
    [    1.0000]    [   -1.0000]

Published with MATLAB&reg; R2012b
