%% 图30b-Q3收敛性与网格裁决-b
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dc = readtable(fullfile(DATA, 'fig_q3_conv.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 450 340]);
s = dc(strcmp(dc.kind, 'space'), :);
plot(s.dr_mm(2:end), s.rel_change(2:end), 'o-', 'Color', INK);
set(gca, 'XScale', 'log', 'YScale', 'log');
xlabel('Δr / mm'); ylabel('相对变化');
title('Q3 收敛性 — 收敛阶'); yline(1e-5, '--', 'Color', GRAY); grid on;

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
