%% 图34-Q3收敛性与网格裁决
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

dc = readtable(fullfile(DATA, 'fig_q3_conv.csv'), 'PreserveVariableNames', true);
dp = readtable(fullfile(DATA, 'fig_q3_conv_pos.csv'), 'PreserveVariableNames', true);
figure('Position', [100 100 900 280]);
subplot(1,3,1); hold on;
s = dc(strcmp(dc.kind, 'space'), :);
plot(s.dr_mm, s.C0, 'o-', 'Color', BLUE);
plot(s.dr_mm, s.CR, 's-', 'Color', RED);
set(gca, 'XScale', 'log'); xlabel('\Deltar / mm'); ylabel('水分浓度');
title('(a) 终态值'); legend({'C_0','C_R'}, 'Location', 'best');
subplot(1,3,2);
plot(s.dr_mm(2:end), s.rel_change(2:end), 'o-', 'Color', INK);
set(gca, 'XScale', 'log', 'YScale', 'log');
xlabel('\Deltar / mm'); ylabel('相对变化');
title('(b) 收敛阶'); yline(1e-5, '--', 'Color', GRAY);
subplot(1,3,3);
[~, ord] = sort(dp.rel_change);
barh(dp.rel_change(ord), 'FaceColor', BLUE);
short_names = cell(height(dp), 1);
for i = 1:height(dp)
    short_names{i} = dp.pair{i}(1:min(12, length(dp.pair{i})));
end
set(gca, 'YTickLabel', short_names(ord), 'FontSize', 6);
xlabel('相对变化'); title('(c) 按位置');
