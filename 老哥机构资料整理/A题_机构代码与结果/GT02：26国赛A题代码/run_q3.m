%% A题第 3 问：以“各径向位置含水率均低于 0.15”为停止条件
% 附件 1 只给到 4 h；4 h 后程序按其末时刻空气状态保持不变。
clear; clc;

root = fileparts(mfilename('fullpath'));

cfg = drying_common('config',3);
air = drying_common('load_air',fullfile(root,'data','附件1.xlsx'));

[t,T,C,meta] = drying_common('solve_fixed',cfg,air);

drying_common('write_result',cfg,root,t,T,C,meta);
drying_common('make_plots',cfg,root,t,T,C,meta);

if meta.reachedTarget
    fprintf('第3问完成：所有径向位置均满足 C<0.15，干燥时间为 %.2f h。\n', ...
        meta.endTime/3600);
else
    fprintf('第3问在 %.0f h 的安全上限内仍未满足 C<0.15。\n', ...
        cfg.tMax/3600);
end