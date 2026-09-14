%% 图42-边界不确定度散布区间
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

fid = fopen(fullfile(DATA, 'fig_q1_uq.csv'));
raw = textscan(fid, '%s%f%f%f%f%f%f', 'Delimiter', ',', 'HeaderLines', 5, 'CommentStyle', '#');
fclose(fid);
names = raw{1}; base = raw{2}; lo = raw{3}; hi = raw{6};
figure('Position', [100 100 500 300]); hold on;
for i = 1:4
    plot([lo(i) hi(i)], [i i], '-', 'LineWidth', 8, 'Color', [BLUE 0.25]);
    plot(base(i), i, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k');
end
set(gca, 'YTick', 1:4, 'YTickLabel', names);
xlabel('数值'); title('Q1 边界不确定度传播区间');
grid on;

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
