%% 图37-Q3全局灵敏度
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

m = readtable(fullfile(DATA, 'fig_q3_gs_morris.csv'), 'PreserveVariableNames', true);
s = readtable(fullfile(DATA, 'fig_q3_gs_sobol.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 700 280]);
subplot(1,2,1);
scatter(m.mu_star, m.sigma, 40, INK, 'filled'); hold on;
for i = 1:height(m)
    text(m.mu_star(i)+max(m.mu_star)*0.03, m.sigma(i), m.param{i}, 'FontSize', 7);
end
xlabel('\mu^*'); ylabel('\sigma'); title('Morris \mu^*-\sigma'); grid on;
subplot(1,2,2);
b = bar([s.S1, s.ST], 'grouped');
b(1).FaceColor = BLUE; b(2).FaceColor = GOLD;
set(gca, 'XTickLabel', s.param);
ylabel('灵敏度指数'); title('Sobol S_1 vs S_T');
legend({'S_1','S_T'}, 'Location', 'best'); grid on;

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
