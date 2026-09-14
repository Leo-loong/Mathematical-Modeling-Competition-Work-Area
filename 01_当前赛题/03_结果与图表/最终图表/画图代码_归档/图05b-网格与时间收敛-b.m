%% 图05b-网格与时间收敛-b
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_gci_data.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 500 360]); hold on;
g_list = unique(d.group);
for g = g_list'
    s = d(strcmp(d.group, g), :); s = sortrows(s, 'delta');
    if strcmp(g{1}, 'spatial')
        y = s.Tc; rc = abs(diff(y))/abs(y(end)); plot(s.delta(2:end), rc, 'o-', 'Color', BLUE);
        y = s.Cs; rc = abs(diff(y))/abs(y(end)); plot(s.delta(2:end), rc, 's-', 'Color', GOLD);
    elseif strcmp(g{1}, 'temporal_T')
        y = s.Tc; rc = abs(diff(y))/abs(y(end)); plot(s.delta(2:end), rc, '^-', 'Color', GREEN);
    else
        y = s.Cs; rc = abs(diff(y))/abs(y(end)); plot(s.delta(2:end), rc, 'D-', 'Color', RED);
    end
end
set(gca, 'XScale', 'log', 'YScale', 'log');
xr = [0.1 1.25]; plot(xr, 3e-5*xr, '--', 'Color', GRAY); plot(xr, 3e-6*xr.^2, '-.', 'Color', GRAY);
text(1.1, 3e-5*1.1, 'O(h)', 'Color', GRAY, 'FontSize', 7);
text(1.05, 2.2e-6, 'O(h^2)', 'Color', GRAY, 'FontSize', 7);
xlabel('步长'); ylabel('相对偏差');
title('网格与时间收敛 — 收敛阶');
legend({'空间 T(0)','空间 C(R)','时间 T(0)','时间 C(R)'}, 'Location', 'northwest');
grid on;

% 导出矢量PDF
drawnow
[~, scriptName] = fileparts(mfilename('fullpath'));
outPath = fullfile('..', [scriptName '.pdf']);
try
    exportgraphics(gcf, outPath, 'ContentType', 'vector');
    fprintf('exportgraphics OK: %s\n', outPath);
catch
    try
        print(gcf, outPath, '-dpdf', '-painters');
        fprintf('print OK (fallback): %s\n', outPath);
    catch
        fprintf('BOTH FAILED: %s\n', outPath);
    end
end
