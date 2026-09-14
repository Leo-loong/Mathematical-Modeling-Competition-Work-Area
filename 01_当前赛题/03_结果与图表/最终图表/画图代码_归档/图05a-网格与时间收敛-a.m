%% 图05a-网格与时间收敛-a
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
        plot(s.delta, s.Tc, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
        plot(s.delta, s.Ts, 's-', 'Color', GOLD, 'MarkerFaceColor', GOLD);
    else
        plot(s.delta, s.Tc, '^-', 'Color', GREEN, 'MarkerFaceColor', GREEN);
    end
end
set(gca, 'XScale', 'log');
xlabel('步长'); ylabel('终态温度 / ℃');
title('网格与时间收敛 — 终态值随步长');
legend({'空间 T(0)','空间 T(R)','时间 T(0)'}, 'Location', 'southeast');
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
