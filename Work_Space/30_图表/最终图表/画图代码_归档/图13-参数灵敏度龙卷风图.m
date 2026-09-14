%% 图13-参数灵敏度龙卷风图
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_tornado_data.csv'), 'PreserveVariableNames', true);
outs = {'C_center','C_surface','T_center','T_surface'};
sub_titles = {'水分浓度 中心','水分浓度 表面','温度 中心','温度 表面'};
figure('Position', [100 100 720 480]);
for k = 1:4
    subplot(2,2,k);
    sel = d(strcmp(d.output, outs{k}), :);
    [~, ord] = sort(abs(sel.S_norm));
    barh(sel.S_norm(ord), 'FaceColor', BLUE);
    set(gca, 'YTickLabel', sel.parameter(ord));
    xline(0, '--', 'Color', GRAY);
    title(sub_titles{k}); xlabel('归一化灵敏度 S');
    grid on;
end
sgtitle('Q1 参数灵敏度龙卷风图（OAT±20%）');
