%% 图48-Q4潜热中段温降曲线
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_INV4_latent_dT.csv'));
figure;
plot(d.t_h, d.dT_K, 'Color', RED);
yline(0, '--', 'Color', GRAY);
xlabel('时间 t / h'); ylabel('\DeltaT / K');
title('Q4 潜热中段温降曲线');
grid on
