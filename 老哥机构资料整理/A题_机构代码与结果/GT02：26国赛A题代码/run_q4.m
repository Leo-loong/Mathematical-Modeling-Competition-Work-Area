%% A题第 4 问：考虑半径收缩的耦合传热传质模拟
% 使用 x=r/R(t) 变换。固定输出点自动限于全过程最小半径内，另列给出实际表面值。
clear; clc;
root = fileparts(mfilename('fullpath'));
cfg = drying_common('config',4);
air = drying_common('load_air',fullfile(root,'data','附件1.xlsx'));
radius = drying_common('load_radius',fullfile(root,'data','附件2.xlsx'));
[t,T,C,meta] = drying_common('solve_shrink',cfg,air,radius);
drying_common('write_result',cfg,root,t,T,C,meta);
drying_common('make_plots',cfg,root,t,T,C,meta);
fprintf('第4问完成：结果保存至 %s\n',fullfile(root,'result'));
