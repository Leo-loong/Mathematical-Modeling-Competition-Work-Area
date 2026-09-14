%% 图14-数据预处理对照
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_smooth_check.csv'), 'PreserveVariableNames', true);
data = readmatrix(fullfile(DATA, 'fig_smooth_check.csv'));
vals = abs(data(1:2, 2:6));
vals(vals==0) = 1e-12;
labels = {'ΔT_0 / ℃','ΔT_R / ℃','ΔC_0','ΔC_R','全场T偏差 / ℃'};
figure('Position', [100 100 480 320]);
b = bar(vals');
b(1).FaceColor = BLUE; b(2).FaceColor = GOLD;
set(gca, 'XTickLabel', labels, 'YScale', 'log');
ylabel('偏差绝对值（对数轴）');
title('Q1 边界平滑 vs 不平滑对比');
legend({'MA-3平滑','MA-5平滑'}, 'Location', 'northwest');
yline(1e-2, '--', 'Color', GRAY);
grid on;
