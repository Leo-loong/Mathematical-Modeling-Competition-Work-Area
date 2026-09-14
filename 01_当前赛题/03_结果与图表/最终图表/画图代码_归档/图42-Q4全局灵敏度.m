%% 图46-Q4全局灵敏度
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q4_INV3_morris.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 450 320]);
scatter(d.mu_star, d.sigma, 40, INK, 'filled'); hold on;
for i = 1:height(d)
    text(d.mu_star(i)+max(d.mu_star)*0.04, d.sigma(i), d.param{i}, 'FontSize', 7);
end
xlabel('\mu^* (均值影响)'); ylabel('\sigma (非线性/交互)');
title('Q4 全局灵敏度 Morris (6参数)'); grid on;

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
