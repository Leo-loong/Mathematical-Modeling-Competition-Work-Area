%% 图41a-Q4低C端外推UQ-a
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

df = readtable(fullfile(DATA, 'fig_q4_INV2_uq_family.csv'));
figure('Position', [100 100 500 360]);
plot(df.C_fr, df.t_dry_h, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE, 'LineWidth', 1.5);
xlabel('C_{fr}'); ylabel('t_{dry} / h');
title('Q4 低C端外推不确定度 — 截断族曲线'); grid on;

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
