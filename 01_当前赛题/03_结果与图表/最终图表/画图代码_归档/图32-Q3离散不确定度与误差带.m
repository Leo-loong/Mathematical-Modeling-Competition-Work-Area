%% 图36-Q3离散不确定度与误差带
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q3_gci.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 700 280]);
subplot(1,2,1); hold on;
s_space = d(contains(d.kind, 'space'), :);
s_time  = d(contains(d.kind, 'time'), :);
plot(s_space.dr_mm, s_space.t_end_h, 'o-', 'Color', BLUE);
plot(s_time.h_in_s, s_time.t_end_h, '^-', 'Color', GOLD);
xlabel('步长 (mm或s)'); ylabel('t_{end} / h');
title('(a) 终态值'); legend({'空间','时间'}, 'Location', 'best');
subplot(1,2,2); hold on;
rc_s = abs(diff(s_space.t_end_h))/abs(s_space.t_end_h(end));
plot(s_space.dr_mm(2:end), rc_s, 'o-', 'Color', BLUE);
rc_t = abs(diff(s_time.t_end_h))/abs(s_time.t_end_h(end));
plot(s_time.h_in_s(2:end), rc_t, '^-', 'Color', GOLD);
set(gca, 'YScale', 'log');
xlabel('步长'); ylabel('相对偏差');
title('(b) 收敛趋势'); grid on;

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
