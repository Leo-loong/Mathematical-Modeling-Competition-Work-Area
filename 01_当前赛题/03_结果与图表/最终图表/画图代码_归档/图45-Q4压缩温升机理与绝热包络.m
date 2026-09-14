%% 图49-Q4压缩温升机理与绝热包络
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_INV5_compression.csv'));
figure;
plot(d.t_h, d.TR,         'Color', BLUE);  hold on
plot(d.t_h, d.T_ad,       '--', 'Color', RED);
plot(d.t_h, d.theta_meas, 'Color', GREEN);
plot(d.t_h, d.theta_qs,   '-.', 'Color', GOLD);
xlabel('时间 t / h'); ylabel('温度 / ℃');
title('Q4 压缩温升机理与绝热包络');
legend({'T_R表面','T_{ad}绝热包络','\theta_{meas}实测','\theta_{qs}准稳态'}, 'Location', 'best', 'FontSize', 7);
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
