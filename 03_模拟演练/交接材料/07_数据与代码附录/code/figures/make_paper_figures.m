%% make_paper_figures.m — 论文图双路线生成主脚本 (问题1/2 范围: 图2~4)
% 数据路线: 与 run_v15_pipeline 逐行同源的数据准备/模型 (确定性部分, 无随机数)
% 产物   : 交接材料/03_结果与图表包/figures/{fig,png,pdf,svg} + data/*.csv (pgfplots 用)
% Input  : 附件1/2.xlsx; results/final/多算法交叉对照表.csv (图4 权威源)
% Output : 图2 实测谱+背景 | 图3 联合拟合+残差 | 图4 多算法交叉+系统区间
% 图5(合成闭环/bootstrap)依赖管线随机结果 — 待 V4_results.mat 落地后由同脚本扩展
% Run    : matlab -batch "addpath('src/figures');addpath('src/model');make_paper_figures"
% 对应   : 交接材料/03-4 论文用图需求清单; 03-1 数值口径总表

function make_paper_figures()
rootDir = mfilename('fullpath');
for i = 1:3, rootDir = fileparts(rootDir); end   % src/figures -> src -> B题根
figDir = fullfile(rootDir, '交接材料', '03_结果与图表包', 'figures');
dataDir = fullfile(rootDir, '交接材料', '03_结果与图表包', 'data');
if ~exist(dataDir, 'dir'), mkdir(dataDir); end

angles = [10 15]; sig0 = 1100; nref = 2.55;
opts = optimoptions('lsqnonlin', 'Display', 'off', 'MaxIterations', 1500, ...
    'FunctionTolerance', 1e-13, 'StepTolerance', 1e-13);

% ---------- 数据准备 (与 run_v15_pipeline 逐行同源) ----------
Dcell = cell(1,2); Fcell = cell(1,2); Rcell = cell(1,2); bgCell = cell(1,2);
sigN = zeros(1,2);
for k = 1:2
    raw = readmatrix(fullfile(rootDir, '附件', sprintf('附件%d.xlsx', k)));
    D = raw(:,1); R = raw(:,2);
    in = D >= sig0; Df = D(in); Rf = R(in);
    xn = (Df - mean(Df))/(max(Df) - min(Df));
    pf = polyfit(xn, Rf, 7);
    bgCell{k} = @(sg) polyval(pf, (sg - mean(Df))/(max(Df) - min(Df)));
    Fcell{k} = Rf - polyval(pf, xn);
    Dcell{k} = Df; Rcell{k} = Rf;
    sigN(k) = 1.4826*mad(diff(Rf), 1)/sqrt(2);
end

% ---------- 三域估计 (确定性地复现管线实测段) ----------
estAll = cell(1,2); diagI = cell(1,2);
for k = 1:2
    [est, di] = sic_e1_e2_e3(Dcell{k}, Fcell{k}, sigN(k), angles(k), nref, opts);
    estAll{k} = est; diagI{k} = di;
    fprintf('ANGLE %d: E1=%.3f E2=%.3f E3=%.3f\n', angles(k), est.e1.d, est.e2.d, est.e3.d);
end

% ---------- 联合 E3 (与 run_v15_pipeline 同源, 双起点防假分支) ----------
Dj = [Dcell{1}; Dcell{2}]; Fj = [Fcell{1}; Fcell{2}];
wj = [1/sigN(1)^2*ones(size(Dcell{1})); 1/sigN(2)^2*ones(size(Dcell{2}))];
angId = [ones(size(Dcell{1})); 2*ones(size(Dcell{2}))];
sin_t = sind(angles); sigCm = 2550;
lbJ = [3, -1, 0, 0, -2, -1]; ubJ = [20, 1, 10, 10, 2, 1];
bestSse = inf; pj = [];
for ph0 = [-0.3, 0.7]
    x0 = [8.0, ph0, 0.35, 0.35, 0, -0.5];
    [pk, ~, rr] = lsqnonlin(@(p)((mdl_joint(p, Dj, angId, sin_t, nref, sigCm) - Fj).*sqrt(wj)), ...
        x0, lbJ, ubJ, opts);
    if sum(rr.^2) < bestSse, bestSse = sum(rr.^2); pj = pk; end
end
fprintf('JOINT: d=%.4f phi12=%.3f\n', pj(1), pj(2));

% ================= 图2: 实测谱 + 背景 + 条纹区 =================
h = figure('Visible', 'off');
plot(Dcell{1}, Rcell{1}, '-', 'Color', [0 0 0], 'LineWidth', 1.0); hold on;
plot(Dcell{2}, Rcell{2}, '-', 'Color', [0 0.447 0.741], 'LineWidth', 1.0);
plot(Dcell{1}, bgCell{1}(Dcell{1}), '--', 'Color', [0.6 0.6 0.6], 'LineWidth', 1.0);
xline(sig0, ':', 'Color', [0.3 0.3 0.3], 'LineWidth', 1.0);
xlabel('Wavenumber \sigma (cm^{-1})'); ylabel('Reflectance (%)');
legend({'10° 实测', '15° 实测', 'poly7 背景', ...
    sprintf('条纹区下界 %d cm^{-1}', sig0)}, 'Location', 'best');
title('实测反射率谱与背景估计');
paperfig_style(h); paperfig_export(h, 'fig2_spectrum', figDir);
T2 = table(Dcell{1}, Rcell{1}, bgCell{1}(Dcell{1}), Dcell{2}, Rcell{2}, bgCell{2}(Dcell{2}), ...
    'VariableNames', {'sigma10', 'R10', 'bg10', 'sigma15', 'R15', 'bg15'});
writetable(T2, fullfile(dataDir, 'fig2_data.csv'));

% ================= 图3: 联合拟合 + 残差 (10°, 双纵轴) =================
h = figure('Visible', 'off');
yyaxis left
sel1 = angId == 1;
hM = plot(Dj(sel1), Fj(sel1), 'k.', 'MarkerSize', 4); hold on;
yJ = mdl_joint(pj, Dj, angId, sin_t, nref, sigCm);
hF = plot(Dj(sel1), yJ(sel1), '-', 'Color', [0 0.447 0.741], 'LineWidth', 1.0);
ylabel('条纹分量 (%)');
yyaxis right
hR = plot(Dj(sel1), Fj(sel1) - yJ(sel1), '-', 'Color', [0.851 0.325 0.098], 'LineWidth', 0.9);
ylabel('残差 (%)');
xlabel('Wavenumber \sigma (cm^{-1})');
legend([hM, hF, hR], {'实测条纹分量(10°)', '联合 E3 拟合', '残差'}, 'Location', 'best');
title(sprintf('联合拟合与残差 (10°, 残差 std=%.2f%%)', std(Fj(sel1) - yJ(sel1))));
paperfig_style(h); paperfig_export(h, 'fig3_fitresidual', figDir);
T3 = table(Dj(sel1), Fj(sel1), yJ(sel1), Fj(sel1) - yJ(sel1), ...
    'VariableNames', {'sigma', 'F_meas', 'F_fit', 'residual'});
writetable(T3, fullfile(dataDir, 'fig3_data.csv'));

% ================= 图4: 多算法交叉 + 系统区间 (权威源=results/final CSV) =================
csv = fullfile(rootDir, 'results', 'final', '多算法交叉对照表.csv');
T4 = readtable(csv, 'TextType', 'string', 'VariableNamingRule', 'preserve');
T4 = T4(~any(ismissing(T4), 2), :);          % 剔除CSV尾部空行等全缺失行
labels = string(T4.method) + " @" + string(T4.angle) + "°";
h = figure('Visible', 'off');
fill([0.4, height(T4)+0.6, height(T4)+0.6, 0.4], [8.0 8.0 8.9 8.9], ...
    [0.85 0.85 0.85], 'EdgeColor', 'none'); hold on;
yline(8.03, 'k-', 'LineWidth', 1.0);
errorbar(1:height(T4), T4.d_hat_um, T4.sigma_stat_um, 'ko', 'LineWidth', 1.1, ...
    'MarkerFaceColor', 'k', 'CapSize', 6);
set(gca, 'XTick', 1:height(T4), 'XTickLabel', labels, 'XTickLabelRotation', 40, ...
    'FontSize', 8);
ylabel('d (\mum)'); xlim([0.4, height(T4)+0.6]);
legend({'模型系统区间 [8.0, 8.9] \mum', '融合中心 8.03 \mum', '各算法/角度估计'}, ...
    'Location', 'northwest');
title('多算法/双角度交叉对照与系统不确定度区间');
paperfig_style(h); paperfig_export(h, 'fig4_crosscomparison', figDir);
T4out = [T4, table(labels, 'VariableNames', {'method_angle'})];   % pgfplots xticklabels 可用
writetable(T4out, fullfile(dataDir, 'fig4_data.csv'));

fprintf('MAKE_PAPER_FIGURES_DONE\n');
end

% ---------------- 联合模型 (与 run_v15_pipeline mdl_joint 逐行同源) ----------------
function y = mdl_joint(par, Dj, angId, sin_t, nref, sigCm)
% [d, phi12, amp10, amp15, c0, a1]
dcm = par(1)*1e-4;
y = zeros(size(Dj));
for k = 1:2
    sel = angId == k; sg = Dj(sel);
    cost = sqrt(1 - sin_t(k)^2/nref^2);
    r01 = (1 - nref*cost)/(1 + nref*cost);
    Phi = 4*pi*sg.*dcm*nref*cost + par(2)*pi;
    y(sel) = par(2+k)*2*abs(r01).*cos(Phi) + par(5) + par(6).*(sg - sigCm)/1000;
end
end
