%% 图38-Q3低C端外推不确定度
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dg = readtable(fullfile(DATA, 'fig_q3_uq_grid.csv'));
dl = readtable(fullfile(DATA, 'fig_q3_uq_lhs.csv'));
figure('Position', [100 100 700 320]);
subplot(1,2,1);
plot(dg.C_fr, dg.t_end_h, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
xlabel('C_{fr}'); ylabel('t_{end} / h');
title('(a) 截断族曲线'); grid on;
subplot(1,2,2);
scatter(dl.C_fr, dl.t_end_h, 20, [0.30 0.69 0.31], 'filled');
xlabel('C_{fr}'); ylabel('t_{end} / h');
title(sprintf('(b) LHS (n=%d)', height(dl))); grid on;

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
