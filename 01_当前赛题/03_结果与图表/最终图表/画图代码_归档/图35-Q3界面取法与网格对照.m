%% 图39-Q3界面取法与网格对照
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q3_iface_grid.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 520 320]);
b = bar(d.t_dry_h, 0.5);
b.FaceColor = 'flat';
clrs = {BLUE, BLUE, GREEN, GREEN, RED, GOLD};
for i = 1:min(6, height(d))
    r = [hex2dec(clrs{i}(2:3)) hex2dec(clrs{i}(4:5)) hex2dec(clrs{i}(6:7))]/255;
    b.CData(i,:) = r;
end
set(gca, 'XTickLabel', d.case);
ylabel('t_{dry} / h');
title('Q3 界面取法×网格分辨率对照');
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
