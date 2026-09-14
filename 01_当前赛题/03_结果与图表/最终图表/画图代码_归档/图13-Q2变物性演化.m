%% 图15-Q2变物性演化
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesFontName', 'Source Han Sans SC');
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_props.csv'));
figure;
plot(d.C, d.rho_rel,   'Color', BLUE);  hold on
plot(d.C, d.cp_rel,    'Color', GOLD);
plot(d.C, d.k_rel,     'Color', GREEN);
plot(d.C, d.D_rel_T28, 'Color', RED);
plot(d.C, d.D_rel_T50, '--', 'Color', RED);
xline(d.C(1), ':', 'Color', GRAY);
xline(d.C(end), ':', 'Color', GRAY);
xlabel('水分浓度 C / (kg/kg)'); ylabel('相对初值（C_0=2.55处=1）');
title('Q2 物性参数随水分浓度的演化');
legend({'\rho/\rho_0','c_p/c_{p,0}','k/k_0','D/D_0(T=28℃)','D/D_0(T=50℃)'}, 'Location', 'northeast', 'FontSize', 7);
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
