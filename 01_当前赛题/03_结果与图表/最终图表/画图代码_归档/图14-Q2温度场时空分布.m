%% 图16-Q2温度场时空分布
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

data = readmatrix(fullfile(DATA, 'fig_q2_field_T.csv'), 'NumHeaderLines', 1);
t = data(:, 1); Z = data(:, 2:end);
r = linspace(0, 2, size(Z, 2));

r_fine = linspace(0, 2, 200);
t_fine = linspace(t(1), t(end), size(Z, 1))';
Z_fine = interp2(r, t, Z, r_fine, t_fine, 'spline');

figure('Position', [100 100 500 500]);
imagesc(r_fine, t_fine, Z_fine); axis xy;
colormap(parula); c = colorbar; c.Label.String = '温度 / ℃';
xlabel('到药材中心的距离 r / cm'); ylabel('时间 t / s');
title('Q2 温度场 T(r,t) 时空分布（0-3 h）');
caxis([28 55]);
yline(1800, 'w--', 'LineWidth', 0.8);
text(0.05, 1700, 'Q1结束', 'Color', 'w', 'FontSize', 7);

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
