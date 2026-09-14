%% 图47-Q4收缩物性双效应分解
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

base = 57.53; prop = 71.9; shrink = -78.8; actual = 50.78;
net = base + prop + shrink;
figure('Position', [100 100 500 380]); hold on;
bar(1, base, 0.45, 'FaceColor', [0.13 0.40 0.67]);
bar(2, prop, 0.45, 'FaceColor', [0.84 0.40 0.18], 'BaseValue', base);
bar(3, shrink, 0.45, 'FaceColor', [0.30 0.69 0.31], 'BaseValue', base+prop+shrink);
bar(4, actual, 0.45, 'FaceColor', [0.13 0.40 0.67]);
y0 = base; y1 = base+prop; y2 = base+prop+shrink;
plot([0.8 1.2], [y0 y0], 'k', 'LineWidth', 1.2);
plot([1.8 2.2], [y1 y1], 'k', 'LineWidth', 1.2);
plot([2.8 3.2], [y2 y2], 'k', 'LineWidth', 1.2);
plot([3.2 3.8], [actual actual], 'k', 'LineWidth', 1.2);
text(1, base+5, sprintf('%.1f h', base), 'HorizontalAlignment', 'center', 'FontSize', 9);
text(2, y1+5, sprintf('+%.1f h', prop), 'HorizontalAlignment', 'center', 'Color', RED, 'FontSize', 9);
text(3, y2-10, sprintf('%.1f h', shrink), 'HorizontalAlignment', 'center', 'Color', GREEN, 'FontSize', 9);
text(4, actual+5, sprintf('%.1f h', actual), 'HorizontalAlignment', 'center', 'FontSize', 9);
text(0.98, 0.9, sprintf('净= %+.1f h', net), 'Units', 'normalized', 'HorizontalAlignment', 'right', 'FontSize', 10, 'FontWeight', 'bold', 'BackgroundColor', 'w');
set(gca, 'XTickLabel', {'Q3基准','物性+71.9','收缩-78.8','Q4实际'}, 'XTickLabelRotation', 30);
ylabel('烘干时间 / h'); title('Q4 收缩-物性双效应分解'); grid on;

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
