%% 图09-Q1水分浓度场时空分布
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

data = readmatrix(fullfile(DATA, 'fig_q1_field_C.csv'));
t = data(:, 1); Z = data(:, 2:end);
r = linspace(0, 2, size(Z, 2));
figure('Position', [100 100 500 500]);
pcolor(r, t, Z); shading interp; colormap(parula);
c = colorbar; c.Label.String = '水分浓度 / (kg/kg)';
xlabel('到药材中心的距离 r / cm'); ylabel('时间 t / s');
title('Q1水分浓度场时空分布');
caxis([1.5 2.55]);
