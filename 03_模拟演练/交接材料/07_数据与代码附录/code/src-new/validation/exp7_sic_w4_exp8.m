function exp7_sic_w4_exp8()
%% EXP7/W-4/EXP-8 — 第4块：SiC 效应分离、修正重算、精度影响量化
% EXP-7（判据冻结）: {Airy 开/关} × {固定Drude 开/关} 四模型拟合附件1(10°);
%   归因: 引入某开关使残差 lag-1 相对下降 ≥50% → 该效应主导;
%   修正判据: 胜出模型 d̂ 是否超出 v1.5 系统区间 [8.0, 8.9] μm; 附件2 独立验证。
% W-4: 胜出模型重算附件1/2 → v1.5/v2.0 对比表。
% EXP-8: d0∈{5,8,30} Airy真值谱(固定Drude, σp 扫描) → 双光束 vs v2.0 反演 → 偏差-q 关系。
% 输出 : 实验包-2/work/out/EXP7_W4_EXP8_report.txt (UTF-8), EXP7_models.png
% Run  : matlab -batch "addpath('src-new/model'); addpath('src-new/validation'); exp7_sic_w4_exp8"

outDir = fullfile('模型设计','实验包-2','work','out');
if ~exist(outDir,'dir'), mkdir(outDir); end
fid = fopen(fullfile(outDir,'EXP7_W4_EXP8_report.txt'),'w','n','UTF-8');
fprintf(fid,'EXP-7 / W-4 / EXP-8 · SiC 效应分离与量化  %s\n==================================================\n\n', ...
    char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')));

angles = [10 15]; band = [1100 4000]; sigCm = 2550; nSiC = 2.55;
opts = optimoptions('lsqnonlin','Display','off','MaxIterations',2000,...
    'FunctionTolerance',1e-13,'StepTolerance',1e-13);

Dcell = cell(1,2); Fcell = cell(1,2); sigN = zeros(1,2); XN = cell(1,2);
for k = 1:2
    raw = readmatrix(fullfile('附件',sprintf('附件%d.xlsx',k)));
    D = raw(:,1); R = raw(:,2);
    in = D >= band(1) & D <= band(2); Df = D(in); Rf = R(in);
    xn = (Df-mean(Df))/(max(Df)-min(Df));
    Fcell{k} = Rf - polyval(polyfit(xn, Rf, 7), xn);
    Dcell{k} = Df; XN{k} = xn;
    sigN(k) = 1.4826*mad(diff(Rf),1)/sqrt(2);
end
pSiC = drude_params('SiC');

% ---------- EXP-7: 四模型（d 轮廓 + 内参数拟合） ----------
dGrid = 6.0:0.02:12.0;
names4 = {'M00 双光束+常数r12','M01 Airy+常数r12','M10 双光束+Drude','M11 Airy+Drude'};
res7 = struct('d',{},'sd',{},'rmse',{},'lag1',{},'runs',{},'redchi2',{},'np',{});
for m = 1:4
    [chi2g, dGf] = prof7(Dcell{1}, XN{1}, Fcell{1}, angles(1), pSiC, sigN(1), sigCm, dGrid, m, opts);
    [cm, im] = min(chi2g);
    dd = refine7(dGf, im, chi2g);
    sd = sig_from_curve(dGf, chi2g, im);
    rmse = 100*sqrt(cm/numel(Fcell{1}))*sigN(1);
    [r, ~, np] = resid7(dd, Dcell{1}, XN{1}, Fcell{1}, angles(1), pSiC, sigN(1), sigCm, m, opts);
    res7(m) = struct('d',dd,'sd',sd,'rmse',rmse,'lag1',autocorr1(r),'runs',runs_test(r), ...
        'redchi2',cm/(numel(Fcell{1})-np),'np',np);
    fprintf(fid,'[EXP-7 %s] d=%.4f±%.4f um, RMSE=%.4f%%, red-chi2=%.1f, lag-1=%.4f, runs-z=%.1f\n', ...
        names4{m}, dd, sd, rmse, res7(m).redchi2, res7(m).lag1, res7(m).runs);
end

fprintf(fid,'\n[EXP-7 归因判据（冻结: lag-1 相对下降 ≥50%% → 主导）]\n');
base = max(res7(1).lag1, eps);
redDrude = 100*(1 - res7(3).lag1/base);
redAiry  = 100*(1 - res7(2).lag1/base);
redBoth  = 100*(1 - res7(4).lag1/base);
fprintf(fid,'  加 Drude (M00→M10): %+.1f%% ; 加 Airy (M00→M01): %+.1f%% ; 都加: %+.1f%%\n', ...
    redDrude, redAiry, redBoth);
if redDrude >= 50 && redAiry >= 50
    dom = '两者可分离（均主导量级）';
elseif redDrude >= 50
    dom = 'Drude 相位频变主导';
elseif redAiry >= 50
    dom = 'Airy 多光束主导';
else
    dom = '均未达 50%（残差另有来源）';
end
fprintf(fid,'  → 归因: %s\n', dom);
fprintf(fid,'  过拟合核对(red-chi2): M00=%.1f M01=%.1f M10=%.1f M11=%.1f\n', ...
    [res7.redchi2]);
[~, ibest] = min([res7.redchi2]);
fprintf(fid,'  修正判据: 胜出 %s d̂=%.4f±%.4f; 区间[8.0,8.9] -> %s\n', ...
    names4{ibest}, res7(ibest).d, res7(ibest).sd, ...
    tern7(res7(ibest).d >= 8.0 && res7(ibest).d <= 8.9,'区间内（修正不显著）','超出区间（修正显著）'));

k = 2;
[chi2g, dGf] = prof7(Dcell{k}, XN{k}, Fcell{k}, angles(k), pSiC, sigN(k), sigCm, dGrid, ibest, opts);
[cm, im] = min(chi2g);
dV2 = refine7(dGf, im, chi2g);
sdV2 = sig_from_curve(dGf, chi2g, im);
rmseV2 = 100*sqrt(cm/numel(Fcell{k}))*sigN(k);
[rv, ~, ~] = resid7(dV2, Dcell{k}, XN{k}, Fcell{k}, angles(k), pSiC, sigN(k), sigCm, ibest, opts);
fprintf(fid,'  附件2 验证（%s）: d=%.4f±%.4f um, RMSE=%.4f%%, lag-1=%.4f\n', ...
    names4{ibest}, dV2, sdV2, rmseV2, autocorr1(rv));

% W-4 σp 扫描（风险预案: 扫描替代单值; 目标=残差最小+跨角度一致）
fprintf(fid,'\n[W-4 M10 σp 扫描（附件1/2 同参拟合）]\n');
scanW4 = zeros(numel(pSiC.scan_sigma_p), 5);   % [sp, d1, d2, gap, rmse_avg]
for si = 1:numel(pSiC.scan_sigma_p)
    pmS = drude_params('SiC'); pmS.sigma_p = pSiC.scan_sigma_p(si); pmS.gamma = pSiC.gamma;
    dds = zeros(1,2); rs = zeros(1,2); lgs = zeros(1,2);
    for k = 1:2
        [chi2g, dGf] = prof7(Dcell{k}, XN{k}, Fcell{k}, angles(k), pmS, sigN(k), sigCm, dGrid, 3, opts);
        [cm, im] = min(chi2g);
        dds(k) = refine7(dGf, im, chi2g);
        rs(k) = 100*sqrt(cm/numel(Fcell{k}))*sigN(k);
        [rv, ~, ~] = resid7(dds(k), Dcell{k}, XN{k}, Fcell{k}, angles(k), pmS, sigN(k), sigCm, 3, opts);
        lgs(k) = autocorr1(rv);
    end
    scanW4(si,:) = [pSiC.scan_sigma_p(si), dds(1), dds(2), abs(dds(1)-dds(2)), mean(rs)];
    fprintf(fid,'  σp=%4d: d10=%.3f d15=%.3f |Δ|=%.3f, RMSE=%.2f/%.2f%%, lag-1=%.3f/%.3f\n', ...
        pSiC.scan_sigma_p(si), dds(1), dds(2), abs(dds(1)-dds(2)), rs(1), rs(2), lgs(1), lgs(2));
end
% 选型（数据驱动规则）: 跨角度一致性优先——在 |Δ| < 0.1 μm 的档中取 RMSE 最小;
% 若无档满足 |Δ|<0.1, 则取 |Δ| 最小者并声明不一致。
okGap = scanW4(:,4) < 0.1;
if any(okGap)
    cand = find(okGap);
    [~, ib] = min(scanW4(cand,5)); ib = cand(ib);
    selNote = sprintf('跨角度一致档中 RMSE 最小（%d 档满足 |Δ|<0.1）', nnz(okGap));
else
    [~, ib] = min(scanW4(:,4));
    selNote = '无档满足 |Δ|<0.1（跨角度不一致, 需上报）';
end
spBest = scanW4(ib,1);
fprintf(fid,'  选型(%s): σp=%d (d10=%.3f, d15=%.3f, |Δ|=%.3f)\n', selNote, spBest, scanW4(ib,2), scanW4(ib,3), scanW4(ib,4));

fprintf(fid,'\n[W-4 修正对比表（SiC, 胜出 %s @σp=%d）]\n', names4{ibest}, spBest);
fprintf(fid,'  口径      | v1.5(μm) | v2.0(μm) | 差值(μm)\n');
fprintf(fid,'  10°       | 8.042    | %.4f | %+.4f\n', scanW4(ib,2), scanW4(ib,2)-8.042);
fprintf(fid,'  15°       | 8.011    | %.4f | %+.4f\n', scanW4(ib,3), scanW4(ib,3)-8.011);
fprintf(fid,'  融合基准  | 8.026    | 参考     | 修正量 %+.4f（超出 v1.5 系统区间则显著）\n', ...
    (scanW4(ib,2)+scanW4(ib,3))/2-8.026);

%% ---------- EXP-8: 精度影响量化（偏差-q 关系） ----------
fprintf(fid,'\n==================================================\n[EXP-8 精度影响量化]\n');
rng(20260909);
d0list = [5 8 30];
spSweep = [700 1500 4000];
raw = readmatrix(fullfile('附件','附件1.xlsx'));
D = raw(:,1); R = raw(:,2);
in = D >= band(1) & D <= band(2); Df = D(in); Rf = R(in);
xn = (Df-mean(Df))/(max(Df)-min(Df));
pf = polyfit(xn, Rf, 7);
bgF = @(sg) polyval(pf, (sg-mean(Df))/(max(Df)-min(Df)));
cost10 = cos(asin(sind(10))/nSiC);
sigN1 = sigN(1);
dGrid8 = 1.0:0.02:40;
fprintf(fid,'设计: SiC 形态, σp 扫描(改变 q), d0∈{5,8,30}×15次; 反演: 双光束(v1.5式) vs v2.0\n');
fprintf(fid,'  σp   | q̄      | d0  | 双光束bias | v2.0 bias\n');
for si = 1:numel(spSweep)
    pg = drude_params('SiC'); pg.sigma_p = spSweep(si); pg.gamma = 300;
    qAvg = mean(abs(aux_r12(Df, 10, pg)))*abs(aux_r01(10, nSiC));
    for di = 1:3
        d0 = d0list(di);
        bD = zeros(15,1); bA = zeros(15,1);
        for m = 1:15
            Rtrue = v20_airy_forward(Df, d0, 10, pg, struct());
            Rsyn = bgF(Df) + Rtrue + sigN1*randn(size(Df));
            Fsyn = Rsyn - bgF(Df);
            mdl = @(par) par(1) + (par(2)+par(3).*(Df-sigCm)/1000).*cos(2*pi*par(4).*Df + par(5)*pi);
            x0 = [0, 0.4, 0, 2*pi*cost10*d0*1e-4, -0.3];
            lb = [-5, 0, -1, 2*pi*cost10*2e-4, -1]; ub = [10, 10, 1, 2*pi*cost10*60e-4, 1];
            pk = lsqnonlin(@(q2)(mdl(q2)-Fsyn)/sigN1, x0, lb, ub, opts);
            bD(m) = pk(4)/(2*nSiC*cost10)*1e4 - d0;
            [chi2g, dGf] = profile_d_v20(Df, Fsyn, 10, pg, sigN1, sigCm, dGrid8);
            [~,im] = min(chi2g);
            bA(m) = refine7(dGf, im, chi2g) - d0;
        end
        fprintf(fid,'  %4d | %.4f | %3d | %+7.3f    | %+7.3f\n', ...
            spSweep(si), qAvg, d0, median(bD), median(bA));
    end
end
fclose(fid);

fig = figure('Position',[60 60 1400 600],'Visible','off');
rmV = arrayfun(@(s)s.rmse, res7);
lgV = arrayfun(@(s)s.lag1, res7);
subplot(1,2,1);
bar([rmV; lgV*100]'); grid on;
set(gca,'XTickLabel',{'M00','M01','M10','M11'});
legend('RMSE (%)','lag-1 (\times100)'); title('EXP-7: four-model comparison (att1)');
subplot(1,2,2);
[~, Fm11, ~] = resid7(res7(4).d, Dcell{1}, XN{1}, Fcell{1}, 10, pSiC, sigN(1), sigCm, 4, opts);
plot(Dcell{1}, Fcell{1},'b'); hold on;
plot(Dcell{1}, Fm11,'r-'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('Fringe (%)');
legend('data','M11 Airy+Drude','Location','best'); title('Att1: best model fit');
saveas(fig, fullfile(outDir,'EXP7_models.png'));
disp('EXP7_DONE');
end

% ---------------- 辅助 ----------------
function r01 = aux_r01(angle, n1)
theta = angle*pi/180;
c1 = sqrt(1 - sin(theta)^2/n1^2);
r01 = (cos(theta) - n1*c1)/(cos(theta) + n1*c1);
end

function r12 = aux_r12(sig, angle, p)
theta = angle*pi/180;
c1 = sqrt(1 - sin(theta)^2/p.n1^2);
N2 = sqrt(p.epsinf - p.sigma_p^2./(sig.*(sig + 1i*p.gamma)));
c2 = sqrt(1 - (sin(theta)./N2).^2);
r12 = (p.n1*c1 - N2.*c2)./(p.n1*c1 + N2.*c2);
end

function [chi2g, dGf] = prof7(Df, xn, F, angle, pm, sigN, sigCm, dGrid, midx, opts)
chi2g = zeros(size(dGrid)); dGf = dGrid;
for gi = 1:numel(dGrid)
    [r, ~, ~] = resid7(dGrid(gi), Df, xn, F, angle, pm, sigN, sigCm, midx, opts);
    chi2g(gi) = sum((r/sigN).^2);
end
end

function [r, Fmod, np] = resid7(d, Df, xn, F, angle, pm, sigN, sigCm, midx, opts)
cost = cos(asin(sind(angle)/pm.n1));
Delta = 4*pi*Df*(d*1e-4)*pm.n1*cost;
Lin = [ones(size(Df)), (Df-sigCm)/1000];
switch midx
    case 1  % M00: 双光束+常数r12 → 线性 [A, B, c0, a1]
        M = [cos(Delta), sin(Delta), Lin];
        coef = M\F; Fmod = M*coef; np = 4;
    case 3  % M10: 双光束+Drude → 线性 [amp, c0, a1]
        Rd = dual_R(Df, d, angle, pm);
        M = [fringe_of(Rd, xn), Lin];
        coef = M\F; Fmod = M*coef; np = 3;
    case 4  % M11: Airy+Drude → 线性 [amp, c0, a1]
        Ra = v20_airy_forward(Df, d, angle, pm, struct());
        M = [fringe_of(Ra, xn), Lin];
        coef = M\F; Fmod = M*coef; np = 3;
    case 2  % M01: Airy+常数r12 → lsqnonlin [phi12, rho12, amp, c0, a1]
        mdl = @(q) q(3)*fringe_of(v20_airy_forward(Df, d, angle, pm, ...
            struct('airy',true,'drude',false,'r12const',q(2)*exp(1i*q(1)*pi))), xn) ...
            + q(4) + q(5).*(Df-sigCm)/1000;
        x0 = [-0.3, 0.25, 1, 0, -0.5]; lb = [-1, 0, 0, -2, -1]; ub = [1, 0.6, 10, 2, 1];
        [pk, ~, rr] = lsqnonlin(@(q)(mdl(q)-F)/sigN, x0, lb, ub, opts);
        r = rr*sigN; Fmod = mdl(pk); np = 5;
        return;
end
r = F - Fmod;
end

function Fr = fringe_of(R, xn)
Fr = R - polyval(polyfit(xn, R, 7), xn);
end

function R = dual_R(sig, d, angle, pm)
theta = angle*pi/180;
c1 = sqrt(1 - sin(theta)^2/pm.n1^2);
r01 = (cos(theta) - pm.n1*c1)/(cos(theta) + pm.n1*c1);
N2 = sqrt(pm.epsinf - pm.sigma_p^2./(sig(:).*(sig(:) + 1i*pm.gamma)));
c2 = sqrt(1 - (sin(theta)./N2).^2);
r12 = (pm.n1*c1 - N2.*c2)./(pm.n1*c1 + N2.*c2);
Delta = 4*pi*sig(:)*(d*1e-4)*pm.n1*c1;
R = abs(r01 + (1-r01^2).*r12.*exp(1i*Delta)).^2;
end

function [chi2g, dGridF] = profile_d_v20(Df, F, angle, pm, sigN, sigCm, dGrid)
chi2g = zeros(size(dGrid)); dGridF = dGrid;
Lin = [ones(size(Df)), (Df-sigCm)/1000];
xn = (Df-mean(Df))/(max(Df)-min(Df));
for gi = 1:numel(dGrid)
    Ra = v20_airy_forward(Df, dGrid(gi), angle, pm, struct());
    Fr = Ra - polyval(polyfit(xn, Ra, 7), xn);
    M = [Fr, Lin];
    coef = M\F;
    r = F - M*coef;
    chi2g(gi) = sum((r/sigN).^2);
end
end

function d = refine7(dGrid, im, chi2g)
d = dGrid(im);
if im>1 && im<numel(dGrid)
    y1=chi2g(im-1); y2=chi2g(im); y3=chi2g(im+1); den=y1-2*y2+y3;
    if den>0, d = d + 0.5*(y1-y3)/den*(dGrid(2)-dGrid(1)); end
end
end

function sd = sig_from_curve(dGrid, chi2g, im)
if im>1 && im<numel(dGrid)
    y1=chi2g(im-1); y2=chi2g(im); y3=chi2g(im+1); den=y1-2*y2+y3;
    if den>0, sd = sqrt(1/den)*(dGrid(2)-dGrid(1))/2; else, sd = (dGrid(2)-dGrid(1)); end
else
    sd = (dGrid(2)-dGrid(1));
end
sd = max(sd, 0.005);
end

function s = tern7(tf, a, b)
if tf, s = a; else, s = b; end
end

function a = autocorr1(x)
x = x(:); x = x(isfinite(x)); x = x - mean(x);
a = sum(x(1:end-1).*x(2:end))/sum(x.^2);
end

function z = runs_test(x)
med = median(x); s = x > med;
n1 = sum(s); n2 = numel(s)-n1;
if n1<10 || n2<10, z = NaN; return; end
r = 1 + sum(s(2:end) ~= s(1:end-1));
mu = 2*n1*n2/(n1+n2) + 1;
va = 2*n1*n2*(2*n1*n2-n1-n2)/((n1+n2)^2*(n1+n2-1));
z = (r-mu)/sqrt(va);
end
