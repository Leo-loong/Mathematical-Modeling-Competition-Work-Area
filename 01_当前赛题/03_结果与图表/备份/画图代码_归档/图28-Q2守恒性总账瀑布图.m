%% 图28-Q2守恒性总账瀑布图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_conservation.csv'), 'PreserveVariableNames', true);
dm = d(strcmp(d.kind, 'mass'), :);
de = d(strcmp(d.kind, 'energy'), :);
labels = {'初始储量','终值储量','变化量','边界流出','物性项','残差'};
figure('Position', [100 100 700 300]);
subplot(1,2,1);
b = bar(dm.value, 'FaceColor', BLUE);
set(gca, 'XTickLabel', labels);
ylabel('水分储变量'); title('质量守恒'); grid on;
subplot(1,2,2);
b = bar(de.value, 'FaceColor', GOLD);
set(gca, 'XTickLabel', labels);
ylabel('能量储变量'); title('能量守恒'); grid on;
sgtitle('Q2 守恒性总账');
