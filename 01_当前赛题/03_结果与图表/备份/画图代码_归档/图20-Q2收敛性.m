%% 图20-Q2收敛性
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_gci.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 700 360]);
subplot(1,2,1); hold on
for g = unique(d.group)'
    s = d(strcmp(d.group, g), :);
    s = sortrows(s, 'delta');
    if strcmp(g{1}, 'spatial')
        plot(s.delta, s.TR, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
    else
        plot(s.delta, s.T0, '^-', 'Color', GREEN, 'MarkerFaceColor', GREEN);
    end
end
set(gca, 'XScale', 'log');
xlabel('步长'); ylabel('终态值');
title('(a) 收敛趋势'); legend({'空间Δr','时间Δt'}, 'Location', 'best');
subplot(1,2,2); hold on
for g = unique(d.group)'
    s = d(strcmp(d.group, g), :);
    s = sortrows(s, 'delta');
    if strcmp(g{1}, 'spatial')
        y = s.TR; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, 'o-', 'Color', BLUE);
    else
        y = s.T0; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, '^-', 'Color', GREEN);
    end
end
set(gca, 'XScale', 'log', 'YScale', 'log');
xlabel('步长'); ylabel('相对偏差');
title('(b) 收敛阶');
yline(5e-5, '--', 'Color', GRAY);
grid on
