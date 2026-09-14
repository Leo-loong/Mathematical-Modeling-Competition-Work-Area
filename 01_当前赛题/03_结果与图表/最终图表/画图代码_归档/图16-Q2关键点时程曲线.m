%% 图18-Q2关键点时程曲线
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_curves.csv'));
figure;
yyaxis left
plot(d.time_s, d.T_center, 'Color', BLUE); hold on
plot(d.time_s, d.T_surface, 'Color', GOLD);
ylabel('温度 / ℃');
yyaxis right
plot(d.time_s, d.C_center, 'Color', GREEN);
plot(d.time_s, d.C_surface, 'Color', RED);
ylabel('水分浓度 / (kg/kg)');
xline(1800, ':', 'Color', GRAY);
xlabel('时间 t / s'); title('Q2 中心与表面温度、水分浓度时程（0-3 h）');
legend({'T中心','T表面','C中心','C表面'}, 'Location', 'northwest');
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
