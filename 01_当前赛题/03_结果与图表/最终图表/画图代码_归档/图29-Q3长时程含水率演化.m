%% 图33-Q3长时程含水率演化
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q3_history.csv'));
figure;
plot(d.t_h, d.C_center,  'Color', BLUE); hold on
plot(d.t_h, d.C_surface, 'Color', RED);
yline(0.15, '--', 'Color', GRAY);
xline(d.t_h(end), ':', 'Color', RED);
xlabel('时间 t / h'); ylabel('水分浓度 / (kg/kg)');
title('Q3 中心与表面水分浓度长时程演化');
legend({'C_0 中心','C_R 表面'}, 'Location', 'northeast');
grid on

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
