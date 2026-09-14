%% 图10-Q1关键点时程曲线
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

d = readtable(fullfile(DATA, 'fig_q1_curves.csv'));
figure;
yyaxis left
plot(d.time_s, d.T_center, 'Color', BLUE); hold on
plot(d.time_s, d.T_surface, 'Color', GOLD);
ylabel('温度 / ℃'); ylim([27.4 39.4]);
yyaxis right
plot(d.time_s, d.C_center, 'Color', GREEN);
plot(d.time_s, d.C_surface, 'Color', RED);
ylabel('水分浓度 / (kg/kg)'); ylim([1.38 2.80]);
xlabel('时间 t / s'); title('Q1 中心与表面温度、水分浓度时程曲线');
legend({'T中心','T表面','C中心','C表面'}, 'Location', 'northwest');
grid on
