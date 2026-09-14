%% 图41b-Q4低C端外推UQ-b
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dl = readtable(fullfile(DATA, 'fig_q4_INV2_uq_lhs.csv'));
figure('Position', [100 100 500 360]);
scatter(dl.C_fr, dl.t_dry_h, 25, [0.30 0.69 0.31], 'filled');
xlabel('C_{fr}'); ylabel('t_{dry} / h');
title(sprintf('Q4 低C端外推不确定度 — LHS分位 (n=%d)', height(dl))); grid on;

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
