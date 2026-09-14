%% 图23-Q2三维演化曲面
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dT = readmatrix(fullfile(DATA, 'fig_q2_field_T.csv'));
dC = readmatrix(fullfile(DATA, 'fig_q2_field_C.csv'));
t_all = dT(:,1); ZT = dT(:,2:end); ZC = dC(:,2:end);
r = linspace(0, 2, size(ZT,2));
skip = max(1, round(length(t_all)/200));
idx = 1:skip:length(t_all);
figure('Position', [100 100 600 450]); hold on;
for k = idx
    col = max(0, min(1, t_all(k)/t_all(end)));
    plot3(r, ZC(k,:), ZT(k,:), 'Color', [col 0.5*(1-col) 1-col], 'LineWidth', 0.5);
end
plot3(r, ZC(1,:), ZT(1,:), 'Color', RED, 'LineWidth', 2.5);
plot3(r, ZC(end,:), ZT(end,:), 'Color', BLUE, 'LineWidth', 2.5);
xlabel('r / cm'); ylabel('C / (kg/kg)'); zlabel('T / ℃');
title('Q2 三维演化曲面 T-C-t');
legend({'t=0','t=3 h'}, 'Location', 'best');
view(22, -58); grid on;
