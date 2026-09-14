Chapter_CharacterRecognitionUsingLibsvm
- 
## Contents

- Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
- A Little Clean Work
- &#36733;&#20837;&#35757;&#32451;&#25968;&#25454;
- &#24314;&#31435;&#25903;&#25345;&#21521;&#37327;&#26426;
- &#36733;&#20837;&#27979;&#35797;&#26679;&#26412;
- &#23545;&#27979;&#35797;&#26679;&#26412;&#36827;&#34892;&#20998;&#31867;
- sub function of pre-processing picfunction Chapter_CharacterRecognitionUsingLibsvm

## Matlab&#31070;&#32463;&#32593;&#32476;43&#20010;&#26696;&#20363;&#20998;&#26512;
% &#22522;&#20110;SVM&#30340;&#25163;&#20889;&#23383;&#20307;&#35782;&#21035;
% by &#26446;&#27915;(faruto)
% http://www.matlabsky.com
% Email:faruto@163.com
% http://weibo.com/faruto
% http://blog.sina.com.cn/faruto
% 2013.01.01

## A Little Clean Work
close all;
clear;
clc;
format compact;

## &#36733;&#20837;&#35757;&#32451;&#25968;&#25454;
% &#21033;&#29992;uigetfile&#20989;&#25968;&#20132;&#20114;&#24335;&#36873;&#21462;&#35757;&#32451;&#26679;&#26412;
[FileName,PathName,FilterIndex] = uigetfile( ...
    {'*.jpg';'*.bmp'},'&#35831;&#23548;&#20837;&#35757;&#32451;&#22270;&#29255;','*.jpg','MultiSelect','on');
if ~FilterIndex
    return;
end
num_train = length(FileName);
TrainData = zeros(num_train,16*16);
TrainLabel = zeros(num_train,1);
for k = 1:num_train
    pic = imread([PathName,FileName{k}]);
    pic = pic_preprocess(pic);

    % &#23558;&#26631;&#20934;&#21270;&#22270;&#20687;&#25353;&#21015;&#25289;&#25104;&#19968;&#20010;&#21521;&#37327;&#24182;&#36716;&#32622;&#65292;&#29983;&#25104;50*256&#30340;&#35757;&#32451;&#26679;&#26412;&#30697;&#38453;
    TrainData(k,:) = double(pic(:)');
    % &#26679;&#26412;&#26631;&#31614;&#20026;&#26679;&#26412;&#25152;&#23545;&#24212;&#30340;&#25968;&#23383;
    TrainLabel(k) = str2double(FileName{k}(4));
end

## &#24314;&#31435;&#25903;&#25345;&#21521;&#37327;&#26426;
[bestCVaccuracy,bestc,bestg] = ...     SVMcgForClass(TrainLabel,TrainData,-8,8,-8,8,10,0.8,0.8,4.5)

% &#35774;&#32622;GA&#30456;&#20851;&#21442;&#25968;
    ga_option.maxgen = 100;
    ga_option.sizepop = 20;
    ga_option.cbound = [0,100];
    ga_option.gbound = [0,100];
    ga_option.v = 10;
    ga_option.ggap = 0.9;
    [bestCVaccuracy,bestc,bestg] = ...
    gaSVMcgForClass(TrainLabel,TrainData,ga_option)

% &#35757;&#32451;
cmd = ['-c ',num2str(bestc),' -g ',num2str(bestg)];
model = svmtrain(TrainLabel, TrainData, cmd);
% &#22312;&#35757;&#32451;&#38598;&#19978;&#26597;&#30475;&#35782;&#21035;&#33021;&#21147;
preTrainLabel = svmpredict(TrainLabel, TrainData, model);
bestCVaccuracy =
    98
bestc =
    0.6168
bestg =
    4.0916
Accuracy = 100% (50/50) (classification)
 
## &#36733;&#20837;&#27979;&#35797;&#26679;&#26412;
[FileName,PathName,FilterIndex] = uigetfile( ...
    {'*.jpg';'*.bmp'},'&#35831;&#23548;&#20837;&#27979;&#35797;&#22270;&#29255;','*.bmp','MultiSelect','on');
if ~FilterIndex
    return;
end
num_train = length(FileName);
TestData = zeros(num_train,16*16);
TestLabel = zeros(num_train,1);
for k = 1:num_train
    pic = imread([PathName,FileName{k}]);
    pic = pic_preprocess(pic);

    TestData(k,:) = double(pic(:)');
    TestLabel(k) = str2double(FileName{k}(4));
end

## &#23545;&#27979;&#35797;&#26679;&#26412;&#36827;&#34892;&#20998;&#31867;
preTestLabel = svmpredict(TestLabel, TestData, model);
assignin('base','TestLabel',TestLabel);
assignin('base','preTestLabel',preTestLabel);
TestLabel'
preTestLabel'
Accuracy = 93.3333% (28/30) (classification)
ans =
  Columns 1 through 13
     0     0     0     1     1     1     2     2     2     3     3     3     4
  Columns 14 through 26
     4     4     5     5     5     6     6     6     7     7     7     8     8
  Columns 27 through 30
     8     9     9     9
ans =
  Columns 1 through 13
     0     0     0     1     1     7     2     2     2     3     3     3     4
  Columns 14 through 26
     4     4     5     5     5     6     6     6     7     7     7     8     8
  Columns 27 through 30
     8     7     9     9

## sub function of pre-processing pic
function pic_preprocess = pic_preprocess(pic)
% &#22270;&#29255;&#39044;&#22788;&#29702;&#23376;&#20989;&#25968;
% &#22270;&#20687;&#21453;&#33394;&#22788;&#29702;
pic = 255-pic;
% &#35774;&#23450;&#38408;&#20540;&#65292;&#23558;&#21453;&#33394;&#22270;&#20687;&#36716;&#25104;&#20108;&#20540;&#22270;&#20687;
pic = im2bw(pic,0.4);
% &#26597;&#25214;&#25968;&#23383;&#19978;&#25152;&#26377;&#20687;&#32032;&#28857;&#30340;&#34892;&#26631;y&#21644;&#21015;&#26631;x
[y,x] = find(pic == 1);
% &#25130;&#21462;&#21253;&#21547;&#23436;&#25972;&#25968;&#23383;&#30340;&#26368;&#23567;&#21306;&#22495;
pic_preprocess = pic(min(y):max(y), min(x):max(x));
% &#23558;&#25130;&#21462;&#30340;&#21253;&#21547;&#23436;&#25972;&#25968;&#23383;&#30340;&#26368;&#23567;&#21306;&#22495;&#22270;&#20687;&#36716;&#25104;16*16&#30340;&#26631;&#20934;&#21270;&#22270;&#20687;
pic_preprocess = imresize(pic_preprocess,[16,16]);

      Published with MATLAB&reg; 7.14
