%% 图50-Q4界面取法与网格对照
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_INV4_iface_grid.csv'), 'PreserveVariableNames', true);
labels_str = strcat(string(d.iface), {' N='}, string(d.N));
figure('Position', [100 100 450 250]);
b = bar(d.t_dry_h, 0.5); b.FaceColor = 'flat';
b.CData(1:2,:) = repmat([0.13 0.40 0.67], 2, 1);
b.CData(3:4,:) = repmat([0.84 0.40 0.18], 2, 1);
set(gca, 'XTickLabel', cellstr(labels_str));
ylabel('t_{dry} / h'); title('Q4 界面取法 x 网格对照');
yline(d.t_dry_h(1), '--', 'Color', GRAY); grid on;

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
