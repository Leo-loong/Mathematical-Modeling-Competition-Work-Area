%% 图27-Q2耦合强度分解图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q2_coupling.csv'), 'PreserveVariableNames', true);
modes = {'强耦合(基准)','解耦(T=C固定)','冻结(物性常数)'};
figure('Position', [100 100 480 320]);
b = bar(d.rel_CR_vs_strong, 'FaceColor', 'flat');
b.CData(1,:) = [0.13 0.40 0.67];
b.CData(2,:) = [0.84 0.40 0.18];
b.CData(3,:) = [0.30 0.69 0.31];
set(gca, 'XTickLabel', modes);
ylabel('相对偏差（以强耦合C_R为基准）');
title('Q2 耦合强度分解（3 h末C_R偏差）');
yline(0, '-', 'Color', INK);
grid on;
