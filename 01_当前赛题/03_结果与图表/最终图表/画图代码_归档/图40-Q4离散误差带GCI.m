%% 图44-Q4离散误差带GCI
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_INV1_gci.csv'), 'PreserveVariableNames', true);
t_h = d.t_dry_s / 3600;
labels_str = strings(height(d), 1);
for i = 1:height(d)
    labels_str(i) = sprintf('%s N=%d sub=%d', d.kind{i}, d.N(i), d.n_sub(i));
end
figure('Position', [100 100 480 250]);
barh(t_h, 0.5, 'FaceColor', BLUE);
set(gca, 'YTickLabel', labels_str);
xlabel('t_{dry} / h');
title('Q4 离散误差带 (GCI)');
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
