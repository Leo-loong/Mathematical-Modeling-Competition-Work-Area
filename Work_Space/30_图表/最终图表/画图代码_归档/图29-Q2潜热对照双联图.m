%% 图29-Q2潜热对照双联图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_latent.csv'));
figure('Position', [100 100 640 420]);
subplot(2,1,1);
plot(d.t_h, d.dT_center, 'Color', BLUE); hold on
plot(d.t_h, d.dT_surface, 'Color', GOLD);
yline(0, '--', 'Color', GRAY);
ylabel('温度偏差 / ℃');
title('潜热效应对照（计入潜热 - 忽略潜热）');
legend({'\DeltaT_0','\DeltaT_R'}, 'Location', 'best');
subplot(2,1,2);
plot(d.t_h, d.dC_center, 'Color', GREEN); hold on
plot(d.t_h, d.dC_surface, 'Color', RED);
yline(0, '--', 'Color', GRAY);
xlabel('时间 t / h'); ylabel('水分浓度偏差 / (kg/kg)');
legend({'\DeltaC_0','\DeltaC_R'}, 'Location', 'best');
grid on
