%% 图30-Q2精度效率帕累托图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_pareto.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 480 320]);
loglog(d.wall_s, d.rel_err, 'o', 'Color', BLUE, 'MarkerSize', 10, 'MarkerFaceColor', BLUE);
xlabel('计算耗时 / s'); ylabel('相对误差');
title('Q2 精度-效率帕累托图');
for i = 1:height(d)
    text(d.wall_s(i)*1.1, d.rel_err(i), d.scheme{i}, 'FontSize', 7);
end
grid on;
