chapter21
-
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
- &#24405;&#20837;&#36755;&#20837;&#25968;&#25454;
- &#32593;&#32476;&#24314;&#31435;&#21644;&#35757;&#32451;
- &#32593;&#32476;&#30340;&#25928;&#26524;&#39564;&#35777;
- &#32593;&#32476;&#20316;&#20998;&#31867;&#30340;&#39044;&#27979;
## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#21333;&#23618;&#31454;&#20105;&#31070;&#32463;&#32593;&#32476;&#30340;&#25968;&#25454;&#20998;&#31867;&#8212;&#24739;&#32773;&#30284;&#30151;&#21457;&#30149;&#39044;&#27979;
% by &#29579;&#23567;&#24029;(@&#29579;&#23567;&#24029;_matlab)
% http://www.matlabsky.com
% Email:sina363@163.com
% http://weibo.com/hgsz2003

## &#28165;&#31354;&#29615;&#22659;&#21464;&#37327;
clc
clear

## &#24405;&#20837;&#36755;&#20837;&#25968;&#25454;
&#36733;&#20837;&#25968;&#25454;&#24182;&#23558;&#25968;&#25454;&#20998;&#25104;&#35757;&#32451;&#21644;&#39044;&#27979;&#20004;&#31867;

load gene.mat;
data=gene;
P=data(1:40,:);
T=data(41:60,:);

% &#36716;&#32622;&#21518;&#31526;&#21512;&#31070;&#32463;&#32593;&#32476;&#30340;&#36755;&#20837;&#26684;&#24335;
P=P';
T=T';
% &#21462;&#36755;&#20837;&#20803;&#32032;&#30340;&#26368;&#22823;&#20540;&#21644;&#26368;&#23567;&#20540;Q&#65306;
Q=minmax(P);

## &#32593;&#32476;&#24314;&#31435;&#21644;&#35757;&#32451;
&#21033;&#29992;newc( )&#21629;&#20196;&#24314;&#31435;&#31454;&#20105;&#32593;&#32476;&#65306;2&#20195;&#34920;&#31454;&#20105;&#23618;&#30340;&#31070;&#32463;&#20803;&#20010;&#25968;&#65292;&#20063;&#23601;&#26159;&#35201;&#20998;&#31867;&#30340;&#20010;&#25968;&#12290;0.1&#20195;&#34920;&#23398;&#20064;&#36895;&#29575;&#12290;

net=newc(Q,2,0.1)

% &#21021;&#22987;&#21270;&#32593;&#32476;&#21450;&#35774;&#23450;&#32593;&#32476;&#21442;&#25968;&#65306;
net=init(net);
net.trainparam.epochs=20;
% &#35757;&#32451;&#32593;&#32476;&#65306;
net=train(net,P);

net =

    Neural Network

              name: 'Custom Neural Network'
        efficiency: .cacheDelayedInputs, .flattenTime,
                    .memoryReduction
          userdata: (your custom info)

    dimensions:

         numInputs: 1
         numLayers: 1
        numOutputs: 1
    numInputDelays: 0
    numLayerDelays: 0
 numFeedbackDelays: 0
 numWeightElements: 230
        sampleTime: 1

    connections:

       biasConnect: true
      inputConnect: true
      layerConnect: false
     outputConnect: true

    subobjects:

            inputs: {1x1 cell array of 1 input}
            layers: {1x1 cell array of 1 layer}
           outputs: {1x1 cell array of 1 output}
            biases: {1x1 cell array of 1 bias}
      inputWeights: {1x1 cell array of 1 weight}
      layerWeights: {1x1 cell array of 0 weights}

    functions:

          adaptFcn: 'adaptwb'
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
          trainFcn: 'trainru'
        trainParam: .showWindow, .showCommandLine, .show, .epochs,
                    .time

    weight and bias values:

                IW: {1x1 cell} containing 1 input weight matrix
                LW: {1x1 cell} containing 0 layer weight matrices
                 b: {1x1 cell} containing 1 bias vector

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
% &#23558;&#21407;&#25968;&#25454;&#22238;&#24102;&#65292;&#27979;&#35797;&#32593;&#32476;&#25928;&#26524;&#65306;
a=sim(net,P);
ac=vec2ind(a)

% &#36825;&#37324;&#20351;&#29992;&#20102;&#21464;&#25442;&#20989;&#25968;vec2ind()&#65292;&#29992;&#20110;&#23558;&#21333;&#20540;&#21521;&#37327;&#32452;&#21464;&#25442;&#25104;&#19979;&#26631;&#21521;&#37327;&#12290;&#20854;&#35843;&#29992;&#30340;&#26684;&#24335;&#20026;&#65306;
%  ind=vec2ind(vec)
% &#20854;&#20013;&#65292;
% vec&#65306;&#20026;m&#34892;n&#21015;&#30340;&#21521;&#37327;&#30697;&#38453;x&#65292;x&#20013;&#30340;&#27599;&#20010;&#21015;&#21521;&#37327;i&#65292;&#38500;&#21253;&#21547;&#19968;&#20010;1&#22806;&#65292;&#20854;&#20313;&#20803;&#32032;&#22343;&#20026;0&#12290;
% ind&#65306;&#20026;n&#20010;&#20803;&#32032;&#20540;&#20026;1&#25152;&#22312;&#30340;&#34892;&#19979;&#26631;&#20540;&#26500;&#25104;&#30340;&#19968;&#20010;&#34892;&#21521;&#37327;&#12290;

ac =

  Columns 1 through 13

     2     2     2     2     2     2     2     2     2     2     2     2     1

  Columns 14 through 26

     2     2     2     1     2     2     1     1     1     1     1     1     1

  Columns 27 through 39

     1     2     2     1     1     2     2     1     1     1     1     2     1

  Column 40

     2

## &#32593;&#32476;&#20316;&#20998;&#31867;&#30340;&#39044;&#27979;
&#19979;&#38754;&#23558;&#21518;20&#20010;&#25968;&#25454;&#24102;&#20837;&#31070;&#32463;&#32593;&#32476;&#27169;&#22411;&#20013;&#65292;&#35266;&#23519;&#32593;&#32476;&#36755;&#20986;&#65306; sim( )&#26469;&#20570;&#32593;&#32476;&#20223;&#30495;

Y=sim(net,T)
yc=vec2ind(Y)

Y =

  Columns 1 through 13

     1     1     0     0     0     0     0     0     0     0     0     0     0
     0     0     1     1     1     1     1     1     1     1     1     1     1

  Columns 14 through 20

     0     0     0     1     0     0     0
     1     1     1     0     1     1     1

yc =

  Columns 1 through 13

     1     1     2     2     2     2     2     2     2     2     2     2     2

  Columns 14 through 20

     2     2     2     1     2     2     2

Published with MATLAB&reg; R2012b
