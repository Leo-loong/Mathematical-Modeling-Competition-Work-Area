%% 图30c-Q3收敛性与网格裁决-c
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dp = readtable(fullfile(DATA, 'fig_q3_conv_pos.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 500 320]);
[~, ord] = sort(dp.rel_change); barh(dp.rel_change(ord), 'FaceColor', BLUE);
short_names = cell(height(dp), 1);
for i = 1:height(dp)
    short_names{i} = dp.pair{i}(1:min(15, length(dp.pair{i})));
end
set(gca, 'YTickLabel', short_names(ord), 'FontSize', 7);
xlabel('相对变化'); title('Q3 收敛性 — 各位置收敛情况'); grid on;

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
