%% 图35-Q3参数灵敏度
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

data = readmatrix(fullfile(DATA, 'fig_q3_sensitivity.csv'));
params_labels = {'T_\infty','T_\infty','C_\infty','C_\infty','h','h','k_m','k_m','D_0','D_0'};
S = max(abs(data(1:2:end, 5)), abs(data(2:2:end, 5)));
param_names = {'T_\infty','C_\infty','h','k_m','D_0'};
figure('Position', [100 100 420 300]);
[~, ord] = sort(S);
barh(S(ord), 'FaceColor', BLUE);
set(gca, 'YTickLabel', param_names(ord));
xlabel('灵敏度系数 S'); title('Q3 参数灵敏度');
xline(0, '--', 'Color', GRAY); grid on;
