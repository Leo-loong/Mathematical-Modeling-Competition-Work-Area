%% 图31-Q2全局灵敏度热力图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_gs_sobol.csv'), 'PreserveVariableNames', true);
outputs = unique(d.output); params = unique(d.parameter);
n_o = length(outputs); n_p = length(params);
M = zeros(n_p, n_o);
for i = 1:height(d)
    ri = find(strcmp(params, d.parameter{i}));
    ci = find(strcmp(outputs, d.output{i}));
    M(ri, ci) = d.ST(i);
end
figure('Position', [100 100 420 380]);
imagesc(M); colormap(flipud(jet)); colorbar;
caxis([0 max(M(:))*1.1]);
set(gca, 'XTick', 1:n_o, 'XTickLabel', outputs, 'XTickLabelRotation', 30);
set(gca, 'YTick', 1:n_p, 'YTickLabel', params);
for i = 1:n_p
    for j = 1:n_o
        text(j, i, sprintf('%.3f', M(i,j)), 'HorizontalAlignment', 'center', 'FontSize', 7);
    end
end
title('Q2 全局灵敏度 Sobol S_T 热力图');

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
