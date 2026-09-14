%% 图06-网格与时间收敛
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_gci_data.csv'), 'PreserveVariableNames', true);

figure('Position', [100 100 800 360]);

% (a) 终态值随步长
subplot(1,2,1); hold on;
g_list = unique(d.group);
for g = g_list'
    s = d(strcmp(d.group, g), :);
    s = sortrows(s, 'delta');
    if strcmp(g{1}, 'spatial')
        plot(s.delta, s.Tc, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
        plot(s.delta, s.Ts, 's-', 'Color', GOLD, 'MarkerFaceColor', GOLD);
    else
        plot(s.delta, s.Tc, '^-', 'Color', GREEN, 'MarkerFaceColor', GREEN);
    end
end
set(gca, 'XScale', 'log');
xlabel('步长（Δr / mm 或 Δt / s）');
ylabel('终态温度 / ℃');
title('(a) 终态值随步长');
legend({'空间 T(0)','空间 T(R)','时间 T(0)'}, 'Location', 'best');

% (b) 收敛阶
subplot(1,2,2); hold on;
for g = g_list'
    s = d(strcmp(d.group, g), :);
    s = sortrows(s, 'delta');
    if strcmp(g{1}, 'spatial')
        y = s.Tc; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, 'o-', 'Color', BLUE);
        y = s.Cs; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, 's-', 'Color', GOLD);
    elseif strcmp(g{1}, 'temporal_T')
        y = s.Tc; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, '^-', 'Color', GREEN);
    else
        y = s.Cs; rc = abs(diff(y))/abs(y(end));
        plot(s.delta(2:end), rc, 'D-', 'Color', RED);
    end
end
set(gca, 'XScale', 'log', 'YScale', 'log');
xlabel('步长（Δr / mm 或 Δt / s）');
ylabel('相对偏差');
title('(b) 收敛阶与理论参考线');
% 参考线
xr = [0.1 1.25];
plot(xr, 3e-5*xr, '--', 'Color', GRAY);
plot(xr, 3e-6*xr.^2, '-.', 'Color', GRAY);
text(1.1, 3e-5*1.1, 'O(h)', 'Color', GRAY, 'FontSize', 7);
text(1.05, 2.2e-6, 'O(h^2)', 'Color', GRAY, 'FontSize', 7);
legend({'空间 T(0)','空间 C(R)','时间 T(0)','时间 C(R)'}, 'Location', 'best');

sgtitle('网格与时间收敛性');