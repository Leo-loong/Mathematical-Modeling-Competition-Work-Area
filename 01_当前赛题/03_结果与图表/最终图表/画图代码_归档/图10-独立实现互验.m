%% 图12-独立实现互验
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_e3_check.csv'));
dev = d.Ts_main - d.Ts_expl;
figure('Position', [100 100 640 420]);
subplot(2,1,1);
plot(d.t, d.Ts_main, 'Color', BLUE); hold on
plot(d.t, d.Ts_expl, '--', 'Color', GOLD);
ylabel('温度 / ℃');
title('Q1 独立实现互验（表面温度，t≤3h）');
legend({'主力解(全隐式)','独立实现(FTCS)'}, 'Location', 'best');
subplot(2,1,2);
plot(d.t, dev, 'Color', RED);
yline(0, '--', 'Color', GRAY);
xlabel('时间 t / s'); ylabel('偏差 ΔT / ℃');
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
