%% 图45-Q4低C端外推UQ
%% 数据源: Work_Space/20_交付包/04_图表包/data/
set(0, 'DefaultAxesFontSize', 9); set(0, 'DefaultLineLineWidth', 1.5);
BLUE='#2166AC'; GOLD='#D6604D'; GREEN='#4DAF4A'; RED='#B2182B'; GRAY=[0.62 0.62 0.62]; INK=[0.2 0.2 0.2];
DATA='/Users/kuangping/Desktop/数学建模/Mathematical-Modeling-Competition-Work-Area/Work_Space/20_交付包/04_图表包/data';

df = readtable(fullfile(DATA, 'fig_q4_INV2_uq_family.csv'));
dl = readtable(fullfile(DATA, 'fig_q4_INV2_uq_lhs.csv'));
figure('Position', [100 100 700 320]);
subplot(1,2,1);
plot(df.C_fr, df.t_dry_h, 'o-', 'Color', BLUE, 'MarkerFaceColor', BLUE);
xlabel('C_{fr}'); ylabel('t_{dry} / h');
title('(a) 截断族曲线'); grid on;
subplot(1,2,2);
scatter(dl.C_fr, dl.t_dry_h, 20, [0.30 0.69 0.31], 'filled');
xlabel('C_{fr}'); ylabel('t_{dry} / h');
title(sprintf('(b) LHS (n=%d)', height(dl))); grid on;
