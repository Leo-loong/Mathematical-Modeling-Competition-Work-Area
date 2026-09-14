%% 图32-Q2自适应步长轨迹图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_adaptive.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 480 300]);
stairs(d.t_s, d.h_from_s, 'Color', BLUE, 'LineWidth', 1.8); hold on;
plot(d.t_s, d.rel_change*max(d.h_from_s), 'o-', 'Color', RED, 'LineWidth', 1.2);
xlabel('时间 t / s'); ylabel('步长 h / s');
title('Q2 自适应步长轨迹');
legend({'步长h','相对变化'}, 'Location', 'best');
grid on;
