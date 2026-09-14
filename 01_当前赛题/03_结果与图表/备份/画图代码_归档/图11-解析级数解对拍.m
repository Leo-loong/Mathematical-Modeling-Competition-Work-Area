%% 图11-解析级数解对拍
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_series_check.csv'), 'PreserveVariableNames', true);
sel = d(strcmp(d.case, 'E2a_dr0.25mm'), :);
t = sel.t; yn = sel.Tc_num; ya = sel.Tc_ana;
dev = yn - ya;
figure('Position', [100 100 640 420]);
subplot(2,1,1);
plot(t, yn, 'Color', BLUE); hold on
plot(t, ya, '--', 'Color', GOLD);
ylabel('温度 / ℃');
title('Q1 温度解析对拍（解析级数解 vs 数值解，r=0）');
legend({'数值解(0.25mm)','解析级数解'}, 'Location', 'best');
subplot(2,1,2);
plot(t, dev, 'Color', RED);
yline(0, '--', 'Color', GRAY);
xlabel('时间 t / s'); ylabel('偏差 Δ / ℃');
ylim([-6e-3 6e-3]);
grid on
