% ============================================================
% 第1批折线图 — 9张 MATLAB 一键生成
% 数据源：Work_Space/20_交付包/04_图表包/data/*.csv
% 输出：矢量PDF
% ============================================================
clear; close all; clc;

DATA_DIR = fullfile(fileparts(mfilename('fullpath')), ...
    '../../../..', 'Work_Space', '20_交付包', '04_图表包', 'data');

% ---------- 全局样式 ----------
set(0, 'DefaultAxesFontName', 'PingFang SC');       % macOS 中文
set(0, 'DefaultTextFontName', 'PingFang SC');
set(0, 'DefaultAxesFontSize', 9);
set(0, 'DefaultLineLineWidth', 1.5);
set(0, 'DefaultAxesLineWidth', 0.8);
set(0, 'DefaultAxesBox', 'off');

BLUE  = '#2166AC';
GOLD  = '#D6604D';
GREEN = '#4DAF4A';
RED   = '#B2182B';
GRAY  = [0.62 0.62 0.62];
INK   = [0.2  0.2  0.2];

% ============================================================
% F-03 烘房环境时序（双Y轴）
% ============================================================
fprintf('F-03 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_env_timeseries.csv'));
figure('Position', [100 100 480 340]);

yyaxis left
plot(d.t_s, d.T_env_C, 'Color', GOLD, 'LineWidth', 1.5); hold on;
ylabel('烘房温度 / ℃');
set(gca, 'YColor', GOLD);

yyaxis right
plot(d.t_s, d.C_env_kgkg, '--', 'Color', GREEN, 'LineWidth', 1.5);
ylabel('烘房水分浓度 / (kg/kg)');
set(gca, 'YColor', GREEN);

xlabel('时间 t / s');
title('烘房环境条件时序（附件1）');
xline(8160, ':', 'Color', GRAY);
text(8300, 29.5, '进入平台段', 'Color', GRAY, 'FontSize', 8);
text(900, 44, '升温段(Q1)', 'Color', INK, 'FontSize', 8);
grid on;

exportgraphics(gcf, '图_F03_烘房环境时序.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-10: Q1 中心/表面 T、C 时程（双Y轴）
% ============================================================
fprintf('F-10 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q1_curves.csv'));
figure('Position', [100 100 480 360]);

yyaxis left
plot(d.time_s, d.T_center, '-', 'Color', BLUE, 'LineWidth', 1.5); hold on;
plot(d.time_s, d.T_surface, '-', 'Color', GOLD, 'LineWidth', 1.5);
ylabel('温度 / ℃');
ylim([27.4 39.4]);

yyaxis right
plot(d.time_s, d.C_center, '-', 'Color', GREEN, 'LineWidth', 1.5);
plot(d.time_s, d.C_surface, '-', 'Color', RED, 'LineWidth', 1.5);
ylabel('水分浓度 / (kg/kg)');
ylim([1.38 2.80]);

xlabel('时间 t / s');
title('Q1 中心与表面温度、水分浓度时程曲线');
legend({'T中心','T表面','C中心','C表面'}, 'Location', 'northwest', 'FontSize', 7);

% 关键数值
t_end = d.time_s(end);
txt = sprintf('T_0=%5.2f ℃', d.T_center(end));
text(0.33, 0.96, txt, 'Units', 'normalized', 'Color', BLUE, 'FontSize', 7);
txt = sprintf('T_R=%5.2f ℃', d.T_surface(end));
text(0.33, 0.89, txt, 'Units', 'normalized', 'Color', GOLD, 'FontSize', 7);
txt = sprintf('C_0=%.4f', d.C_center(end));
text(0.75, 0.10, txt, 'Units', 'normalized', 'Color', GREEN, 'FontSize', 7);
txt = sprintf('C_R=%.4f', d.C_surface(end));
text(0.75, 0.05, txt, 'Units', 'normalized', 'Color', RED, 'FontSize', 7);

grid on;
exportgraphics(gcf, '图_F10_Q1关键点时程曲线.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-18: Q2 关键点时程（0-3 h，双Y轴）
% ============================================================
fprintf('F-18 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q2_curves.csv'));
figure('Position', [100 100 480 360]);

yyaxis left
plot(d.time_s, d.T_center, '-', 'Color', BLUE, 'LineWidth', 1.5); hold on;
plot(d.time_s, d.T_surface, '-', 'Color', GOLD, 'LineWidth', 1.5);
ylabel('温度 / ℃');

yyaxis right
plot(d.time_s, d.C_center, '-', 'Color', GREEN, 'LineWidth', 1.5);
plot(d.time_s, d.C_surface, '-', 'Color', RED, 'LineWidth', 1.5);
ylabel('水分浓度 / (kg/kg)');

% Q1 结束线
xline(1800, ':', 'Color', GRAY);
text(2000, 30, 'Q1结束', 'Color', GRAY, 'FontSize', 8);

xlabel('时间 t / s');
title('Q2 中心与表面温度、水分浓度时程（0-3 h）');
legend({'T中心','T表面','C中心','C表面'}, 'Location', 'northwest', 'FontSize', 7);

% 数值
txt = sprintf('T_0=%.1f ℃', d.T_center(end));
text(0.60, 0.80, txt, 'Units', 'normalized', 'Color', BLUE, 'FontSize', 7);
txt = sprintf('T_R=%.1f ℃', d.T_surface(end));
text(0.60, 0.73, txt, 'Units', 'normalized', 'Color', GOLD, 'FontSize', 7);
txt = sprintf('C_0=%.4f', d.C_center(end));
text(0.60, 0.15, txt, 'Units', 'normalized', 'Color', GREEN, 'FontSize', 7);
txt = sprintf('C_R=%.4f', d.C_surface(end));
text(0.60, 0.08, txt, 'Units', 'normalized', 'Color', RED, 'FontSize', 7);

grid on;
exportgraphics(gcf, '图_F18_Q2关键点时程曲线.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-15: Q2 变物性随含水率演化（多线归一化）
% ============================================================
fprintf('F-15 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q2_props.csv'));
figure('Position', [100 100 500 360]);

plot(d.C, d.rho_rel, '-',  'Color', BLUE,  'LineWidth', 1.5); hold on;
plot(d.C, d.cp_rel,  '-',  'Color', GOLD,  'LineWidth', 1.5);
plot(d.C, d.k_rel,   '-',  'Color', GREEN, 'LineWidth', 1.5);
plot(d.C, d.D_rel_T28, '-', 'Color', RED,   'LineWidth', 1.5);
plot(d.C, d.D_rel_T50, '--','Color', RED,   'LineWidth', 1.2);

xline(d.C(1), ':', 'Color', GRAY);
xline(d.C(end), ':', 'Color', GRAY);

xlabel('水分浓度 C / (kg/kg)');
ylabel('相对初值（C_0=2.55）');
title('Q2 物性参数随水分浓度的演化');
legend({'\rho/\rho_0','c_p/c_{p,0}', 'k/k_0', 'D/D_0(T=28℃)', 'D/D_0(T=50℃)'}, ...
    'Location', 'northeast', 'FontSize', 7);
grid on;
exportgraphics(gcf, '图_F15_Q2变物性演化.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-33: Q3 长时程含水率演化
% ============================================================
fprintf('F-33 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q3_history.csv'));
figure('Position', [100 100 550 360]);

plot(d.t_h, d.C_center,  '-', 'Color', BLUE,  'LineWidth', 1.5); hold on;
plot(d.t_h, d.C_surface, '-', 'Color', RED,   'LineWidth', 1.5);
yline(0.15, '--', 'Color', GRAY, 'LineWidth', 1);
text(2, 0.155, '达标阈值 C=0.15', 'Color', GRAY, 'FontSize', 8);

% 达标时刻
t_end = d.t_h(end);
xline(t_end, ':', 'Color', RED);
txt = sprintf('t=%.2f h\nC_0=%.4f\nC_R=%.4f', t_end, d.C_center(end), d.C_surface(end));
text(t_end-15, 1.0, txt, 'Color', RED, 'FontSize', 8, 'HorizontalAlignment', 'right');

xlabel('时间 t / h');
ylabel('水分浓度 / (kg/kg)');
title('Q3 中心与表面水分浓度长时程演化');
legend({'C_0 中心','C_R 表面'}, 'Location', 'northeast', 'FontSize', 8);
grid on;
exportgraphics(gcf, '图_F33_Q3长时程含水率演化.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-40: Q3 干燥速率曲线
% ============================================================
fprintf('F-40 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q3_drying_rate.csv'));
figure('Position', [100 100 550 360]);

plot(d.t_h, d.u_kg_per_kg_h, '-', 'Color', BLUE, 'LineWidth', 1.5);

% 峰值
[~, imax] = max(d.u_kg_per_kg_h(1:round(length(d.u_kg_per_kg_h)*0.3)));
txt = sprintf('峰值 %.4f', d.u_kg_per_kg_h(imax));
x_peak = d.t_h(imax);
text(x_peak+5, d.u_kg_per_kg_h(imax)*1.5, txt, 'Color', RED, 'FontSize', 8);

xlabel('时间 t / h');
ylabel('干燥速率 / (kg·kg^{-1}·h^{-1})');
title('Q3 干燥速率曲线');
grid on;
exportgraphics(gcf, '图_F40_Q3干燥速率曲线.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-04: 药材半径随干燥时间收缩
% ============================================================
fprintf('F-04 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q4_shrinkage.csv'));
figure('Position', [100 100 500 320]);

plot(d.t_h, d.R_cm, '-', 'Color', BLUE, 'LineWidth', 1.8);

xlabel('时间 t / h');
ylabel('药材半径 R / cm');
title('药材半径随干燥时间收缩（附件2）');

% 标注
text(1, d.R_cm(1)-0.05, sprintf('R_0=%.2f cm', d.R_cm(1)), 'FontSize', 8);
text(d.t_h(end)*0.6, d.R_cm(end)+0.06, sprintf('R=%.4f cm\n收缩比 %.3f', ...
    d.R_cm(end), d.R_cm(end)/d.R_cm(1)), 'Color', RED, 'FontSize', 8);

grid on;
exportgraphics(gcf, '图_F04_药材半径收缩曲线.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-48: Q4 潜热中段温降曲线
% ============================================================
fprintf('F-48 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q4_INV4_latent_dT.csv'));
figure('Position', [100 100 480 300]);

plot(d.t_h, d.dT_K, '-', 'Color', RED, 'LineWidth', 1.5);
yline(0, '--', 'Color', GRAY);

[~, imax] = max(d.dT_K);
txt = sprintf('峰值 %.4f K @ %.2f h', d.dT_K(imax), d.t_h(imax));
text(d.t_h(imax)+1.5, d.dT_K(imax)+max(d.dT_K)*0.3, txt, 'FontSize', 8);

xlabel('时间 t / h');
ylabel('\DeltaT / K');
title('Q4 潜热中段温降曲线');
grid on;
exportgraphics(gcf, '图_F48_Q4潜热中段温降曲线.pdf', 'ContentType', 'vector');
close;

% ============================================================
% F-49: Q4 压缩温升机理与绝热包络
% ============================================================
fprintf('F-49 ...\n');
d = readtable(fullfile(DATA_DIR, 'fig_q4_INV5_compression.csv'));
figure('Position', [100 100 520 350]);

plot(d.t_h, d.TR,         '-',  'Color', BLUE,  'LineWidth', 1.5); hold on;
plot(d.t_h, d.T_ad,       '--', 'Color', RED,   'LineWidth', 1.2);
plot(d.t_h, d.theta_meas, '-',  'Color', GREEN, 'LineWidth', 1.2);
plot(d.t_h, d.theta_qs,   '-.', 'Color', GOLD,  'LineWidth', 1.2);

xlabel('时间 t / h');
ylabel('温度 / ℃');
title('Q4 压缩温升机理与绝热包络');
legend({'T_R 表面','T_{ad} 绝热包络','\theta_{meas} 实测','\theta_{qs} 准稳态'}, ...
    'Location', 'best', 'FontSize', 7);
grid on;
exportgraphics(gcf, '图_F49_Q4压缩温升机理与绝热包络.pdf', 'ContentType', 'vector');
close;

fprintf('第1批折线图全部完成！\n');
fprintf('输出目录: %s\n', pwd);