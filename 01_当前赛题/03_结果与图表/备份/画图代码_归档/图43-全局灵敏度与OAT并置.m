%% 图43-全局灵敏度与OAT并置
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q1_gs.csv'), 'PreserveVariableNames', true);
sel = d(strcmp(d.output, 'CR'), :);
figure('Position', [100 100 450 300]);
b = bar([sel.S1, sel.ST], 'grouped');
b(1).FaceColor = BLUE; b(2).FaceColor = GOLD;
set(gca, 'XTickLabel', sel.param);
ylabel('灵敏度指数'); title('Q1 全局灵敏度 Sobol（C_R）');
legend({'S_1','S_T'}, 'Location', 'best'); grid on;
