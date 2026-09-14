%% 图19-Q1Q2重叠段差异归因
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q1q2_overlap.csv'));
dT = d.T_surface_q2 - d.T_surface_q1;
dC = d.C_surface_q2 - d.C_surface_q1;
figure('Position', [100 100 640 480]);
subplot(2,1,1);
plot(d.t, d.T_surface_q1, '--', 'Color', GOLD); hold on
plot(d.t, d.T_surface_q2, '-', 'Color', GOLD, 'LineWidth', 2);
ylabel('温度 / ℃');
title('Q1与Q2重叠段(0-1800s)差异归因');
legend({'T_R Q1(常物性)','T_R Q2(变物性)'}, 'Location', 'southeast');
subplot(2,1,2);
plot(d.t, dT, 'Color', RED); hold on
plot(d.t, dC, '-.', 'Color', GREEN);
yline(0, '--', 'Color', GRAY);
xlabel('时间 t / s'); ylabel('偏差');
legend({'\DeltaT_R(Q2-Q1)', '\DeltaC_R(Q2-Q1)'}, 'Location', 'best');
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
