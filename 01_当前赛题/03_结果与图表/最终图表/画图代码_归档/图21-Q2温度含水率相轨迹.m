%% 图24-Q2温度含水率相轨迹
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_curves.csv'));
figure('Position', [100 100 450 450]);
plot(d.C_center, d.T_center, 'Color', BLUE, 'LineWidth', 1.8); hold on;
plot(d.C_surface, d.T_surface, 'Color', RED, 'LineWidth', 1.8);
marks_t = [1800, 5400, 10800];
for j = 1:3
    [~, idxi] = min(abs(d.time_s - marks_t(j)));
    plot(d.C_center(idxi), d.T_center(idxi), 'o', 'Color', GRAY, 'MarkerSize', 6, 'MarkerFaceColor', GRAY);
    plot(d.C_surface(idxi), d.T_surface(idxi), 's', 'Color', GRAY, 'MarkerSize', 6, 'MarkerFaceColor', GRAY);
    text(d.C_center(idxi)+0.02, d.T_center(idxi)+0.5, sprintf('t=%ds', marks_t(j)), 'FontSize', 7);
end
xlabel('水分浓度 C / (kg/kg)'); ylabel('温度 T / ℃');
title('Q2 温度-水分浓度相轨迹');
legend({'中心 r=0','表面 r=R_0'}, 'Location', 'best');
set(gca, 'XDir', 'reverse'); grid on;

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
