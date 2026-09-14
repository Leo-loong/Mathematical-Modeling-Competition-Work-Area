%% 图25-Q2全断面失水瀑布图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

data = readmatrix(fullfile(DATA, 'fig_q2_field_C.csv'));
t_all = data(:,1); Z = data(:,2:end);
r = linspace(0, 2, size(Z,2));
skip = max(1, round(length(t_all)/30));
idx = 1:skip:length(t_all);
figure('Position', [100 100 500 350]); hold on;
for j = 1:length(idx)
    col = j/length(idx);
    plot(r, Z(idx(j),:), 'Color', [col 0.5*(1-col) 0.8*(1-col)], 'LineWidth', 1);
end
plot(r, Z(1,:), '--', 'Color', GRAY, 'LineWidth', 1.5);
plot(r, Z(end,:), 'Color', RED, 'LineWidth', 2.5);
xlabel('到药材中心的距离 r / cm'); ylabel('水分浓度 / (kg/kg)');
title('Q2 全断面失水演化（浅->深=时间推进）');
legend({'t=0','t=3 h'}, 'Location', 'best'); grid on;

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
