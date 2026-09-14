%% 图30a-Q3收敛性与网格裁决-a
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dc = readtable(fullfile(DATA, 'fig_q3_conv.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 450 340]); hold on;
s = dc(strcmp(dc.kind, 'space'), :);
plot(s.dr_mm, s.C0, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
plot(s.dr_mm, s.CR, 's-', 'Color', RED, 'MarkerFaceColor', RED);
set(gca, 'XScale', 'log'); xlabel('Δr / mm'); ylabel('水分浓度 / (kg/kg)');
title('Q3 收敛性 — 终态值随步长');
legend({'C_0 中心','C_R 表面'}, 'Location', 'southeast'); grid on;

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
