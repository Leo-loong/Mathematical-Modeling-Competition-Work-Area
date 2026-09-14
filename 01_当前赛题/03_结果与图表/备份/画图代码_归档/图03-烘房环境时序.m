%% 图03-烘房环境时序
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_env_timeseries.csv'));
figure;
yyaxis left
plot(d.t_s, d.T_env_C, 'Color', GOLD); hold on
ylabel('烘房温度 / ℃');
yyaxis right
plot(d.t_s, d.C_env_kgkg, '--', 'Color', GREEN);
ylabel('烘房水分浓度 / (kg/kg)');
xlabel('时间 t / s'); title('烘房环境条件时序（附件1）');
xline(8160, ':', 'Color', GRAY);
grid on
