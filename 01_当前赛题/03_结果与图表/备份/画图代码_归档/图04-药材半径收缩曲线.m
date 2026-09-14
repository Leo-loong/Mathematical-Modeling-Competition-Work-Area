%% 图04-药材半径收缩曲线
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_shrinkage.csv'));
figure;
plot(d.t_h, d.R_cm, 'Color', BLUE, 'LineWidth', 1.8);
xlabel('时间 t / h'); ylabel('药材半径 R / cm');
title('药材半径随干燥时间收缩（附件2）');
grid on
