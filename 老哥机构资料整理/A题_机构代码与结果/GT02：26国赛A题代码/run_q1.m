%% A题第 1 问：常物性圆柱药材的耦合传热传质模拟
% 运行本文件后，result/result1.xlsx 以及两张 PNG 图自动生成。
clear; clc;
root = fileparts(mfilename('fullpath'));
cfg = drying_common('config',1);
air = drying_common('load_air',fullfile(root,'data','附件1.xlsx'));
[t,T,C,meta] = drying_common('solve_fixed',cfg,air);
drying_common('write_result',cfg,root,t,T,C,meta);
drying_common('make_plots',cfg,root,t,T,C,meta);
fprintf('第1问完成：结果保存至 %s\n',fullfile(root,'result'));
