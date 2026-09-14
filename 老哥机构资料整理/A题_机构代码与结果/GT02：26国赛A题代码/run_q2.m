%% A题第 2 问：物性随温湿状态变化的非线性传热传质模拟
% 运行本文件后，result/result2.xlsx 以及两张 PNG 图自动生成。
clear; clc;
root = fileparts(mfilename('fullpath'));
cfg = drying_common('config',2);
air = drying_common('load_air',fullfile(root,'data','附件1.xlsx'));
[t,T,C,meta] = drying_common('solve_fixed',cfg,air);
drying_common('write_result',cfg,root,t,T,C,meta);
drying_common('make_plots',cfg,root,t,T,C,meta);
fprintf('第2问完成：结果保存至 %s\n',fullfile(root,'result'));
