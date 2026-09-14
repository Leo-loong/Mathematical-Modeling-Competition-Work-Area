function exp6_w3_si()
%% EXP6_W3_SI — EXP-6 Si 多光束判定（任务C）+ W-3 Si 反演（任务D/E）+ Si 形态合成闭环
% 判据（冻结, 00 总纲）:
%   四条件核对表; 数据证据三选二: ①双光束式拟合残差 lag-1/std 显著超噪声
%   ②可见度随σ变化偏离双光束预测 ③v2.0与双光束反演厚度差>双光束系统区间
% 设计: 双光束Si式(常数n=3.42,常数ρ) 5参数拟合（证据①/③口径）;
%       v2.0 = σp 敏感性扫描(不拟合,风险预案) + d 轮廓(内层线性[amp,c0,a1], 无盆地)。
%       附件3 选型, 附件4 验证（选择与验证分离）。
% 输入 : 附件3/4.xlsx
% 输出 : 实验包-2/work/out/EXP6_W3_report.txt (UTF-8), EXP6_W3_fits.png
% Run  : matlab -batch "addpath('src-new/model'); addpath('src-new/validation'); exp6_w3_si"

outDir = fullfile('模型设计','实验包-2','work','out');
if ~exist(outDir,'dir'), mkdir(outDir); end
fid = fopen(fullfile(outDir,'EXP6_W3_report.txt'),'w','n','UTF-8');
fprintf(fid,'EXP-6 + W-3 · Si 判定与反演  %s\n==================================================\n\n', ...
    char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')));

angles = [10 15];
band = [500 2800]; sigCm = 1650; nSi = 3.42;
opts = optimoptions('lsqnonlin','Display','off','MaxIterations',2000,...
    'FunctionTolerance',1e-13,'StepTolerance',1e-13);

% ---------- 数据准备 ----------
Dcell = cell(1,2); Fcell = cell(1,2); sigN = zeros(1,2);
for k = 1:2
    raw = readmatrix(fullfile('附件',sprintf('附件%d.xlsx',k+2)));
    D = raw(:,1); R = raw(:,2);
    in = D >= band(1) & D <= band(2);
    Df = D(in); Rf = R(in);
    xn = (Df-mean(Df))/(max(Df)-min(Df));
    Fcell{k} = Rf - polyval(polyfit(xn, Rf, 7), xn);
    Dcell{k} = Df;
    sigN(k) = 1.4826*mad(diff(Rf),1)/sqrt(2);
    fprintf(fid,'附件%d(Si, %d°): 条纹带 %d 点, σnoise=%.4f%%\n', k+2, angles(k), numel(Df), sigN(k));
end
fprintf(fid,'\n');

% ---------- PART A: 证据① 双光束 Si 式拟合 ----------
dDb = zeros(1,2); sDb = zeros(1,2); resDb = cell(1,2);
for k = 1:2
    Df = Dcell{k}; F = Fcell{k};
    mdl = @(par) par(1) + (par(2)+par(3).*(Df-sigCm)/1000).*cos(2*pi*par(4).*Df + par(5)*pi);
    cost = cos(asin(sind(angles(k)))/nSi);
    x0 = [0, 0.5, 0, 2*pi*cost*4.4e-4, -0.3];
    lb = [-5, 0, -1, 2*pi*cost*1.0e-4, -1];
    ub = [ 10, 10, 1, 2*pi*cost*50e-4, 1];
    [pk,~,rr] = lsqnonlin(@(q)(mdl(q)-F)/sigN(k), x0, lb, ub, opts);
    dDb(k) = pk(4)/(2*nSi*cost)*1e4;
    J = numjac_local(@(q)mdl(q), pk, Df);
    covB = pinv(J'*J)*(sum(rr.^2)*sigN(k)^2)/numel(F);
    sDb(k) = sqrt(covB(4,4))/(2*nSi*cost)*1e4;
    resDb{k} = rr*sigN(k);
    fprintf(fid,'[证据① 双光束Si式 附件%d] d_app=%.3f±%.3f um; 残差std=%.4f%%(噪声%.4f%%, 比=%.1f×); lag-1=%.3f; runs-z=%.1f\n', ...
        k+2, dDb(k), sDb(k), std(resDb{k}), sigN(k), std(resDb{k})/sigN(k), ...
        autocorr1(resDb{k}), runs_test(resDb{k}));
end
fprintf(fid,'\n');

% ---------- PART B: 证据② 分波段可见度 ----------
bands = [500 950; 950 1400; 1400 1850; 1850 2300; 2300 2800];
ampB = zeros(2, size(bands,1));
for k = 1:2
    Df = Dcell{k};
    for b = 1:size(bands,1)
        sel = Df >= bands(b,1) & Df < bands(b,2);
        ampB(k,b) = max(detrend(Fcell{k}(sel))) - min(detrend(Fcell{k}(sel)));
    end
end
fprintf(fid,'[证据② 分波段条纹幅度(%%), 双光束式预测为常数]\n  波段:      ');
fprintf(fid,'[%4.0f-%4.0f]  ', bands.');
fprintf(fid,'\n  附件3: '); fprintf(fid,'%.3f  ', ampB(1,:));
fprintf(fid,'\n  附件4: '); fprintf(fid,'%.3f  ', ampB(2,:));
fprintf(fid,'\n  首末衰减比: 附件3=%.1f×, 附件4=%.1f× (双光束预测≈1×)\n\n', ...
    ampB(1,1)/ampB(1,end), ampB(2,1)/ampB(2,end));

% ---------- PART C: v2.0 反演（附件3 选型 → 附件4 验证） ----------
spList = [1000 1500 1859 2500 3200 4157 6000 8000];
dGrid = 1.0:0.02:30;
% 附件3: σp 扫描
fprintf(fid,'[W-3 v2.0 附件3 选型] σp 扫描（γ=360; 不拟合; RMSE 为非加权 %%）\n');
res3 = struct('rmse',inf,'sp',NaN,'g',NaN,'d',NaN,'sd',NaN);
scanRMSE = nan(size(spList)); scanD = nan(size(spList));
siIdx = 0;
for sp = spList
    siIdx = siIdx + 1;
    pm = drude_params('Si'); pm.sigma_p = sp; pm.gamma = 360;
    [chi2g, dGf] = profile_d_v20(Dcell{1}, Fcell{1}, angles(1), pm, sigN(1), sigCm, dGrid);
    [cm, im] = min(chi2g);
    dd = refine_d(dGf, im, chi2g);
    sd = sigma_from_curve(dGf, chi2g, im);
    scanRMSE(siIdx) = 100*sqrt(cm/numel(Fcell{1}))*sigN(1);
    scanD(siIdx) = dd;
    fprintf(fid,'  σp=%4d: d=%.3f±%.3f um, RMSE=%.4f%%\n', sp, dd, sd, scanRMSE(siIdx));
    if cm < res3.rmse
        res3 = struct('rmse',cm,'sp',sp,'g',360,'d',dd,'sd',sd);
    end
end
% 附件3: γ 扫描（最优 σp 处）
fprintf(fid,'  γ 扫描（σp=%d）:\n', res3.sp);
for g = [150 360 900]
    pm = drude_params('Si'); pm.sigma_p = res3.sp; pm.gamma = g;
    [chi2g, dGf] = profile_d_v20(Dcell{1}, Fcell{1}, angles(1), pm, sigN(1), sigCm, dGrid);
    [cm, im] = min(chi2g);
    dd = refine_d(dGf, im, chi2g);
    sd = sigma_from_curve(dGf, chi2g, im);
    fprintf(fid,'  γ=%4d: d=%.3f±%.3f um, RMSE=%.4f%%\n', g, dd, sd, 100*sqrt(cm/numel(Fcell{1}))*sigN(1));
    if cm < res3.rmse
        res3 = struct('rmse',cm,'sp',res3.sp,'g',g,'d',dd,'sd',sd);
    end
end
fprintf(fid,'  选型(附件3): σp=%d, γ=%d, d=%.3f±%.3f um\n\n', res3.sp, res3.g, res3.d, res3.sd);

% 附件4: 验证（同组合）
pmV = drude_params('Si'); pmV.sigma_p = res3.sp; pmV.gamma = res3.g;
dV = zeros(1,2); sdV = zeros(1,2); rmseV = zeros(1,2);
for k = 1:2
    [chi2g, dGf] = profile_d_v20(Dcell{k}, Fcell{k}, angles(k), pmV, sigN(k), sigCm, dGrid);
    [cm, im] = min(chi2g);
    dV(k) = refine_d(dGf, im, chi2g);
    sdV(k) = sigma_from_curve(dGf, chi2g, im);
    rmseV(k) = sqrt(cm/numel(Fcell{k}))*sigN(k);
    fprintf(fid,'[W-3 v2.0 附件%d] σp=%d γ=%d: d=%.3f±%.3f um, RMSE=%.4f%%\n', ...
        k+2, res3.sp, res3.g, dV(k), sdV(k), 100*rmseV(k)*sigN(k));
end
fprintf(fid,'\n');

% ---------- PART D: 证据③ ----------
fprintf(fid,'[证据③] 双光束 d_app = %.3f / %.3f um; v2.0 d = %.3f / %.3f um\n', ...
    dDb(1), dDb(2), dV(1), dV(2));
fprintf(fid,'  差值 = %.3f / %.3f um; 双光束统计σ = %.3f / %.3f um; 差/σ = %.1f / %.1f\n', ...
    dDb(1)-dV(1), dDb(2)-dV(2), sDb(1), sDb(2), ...
    abs(dDb(1)-dV(1))/sDb(1), abs(dDb(2)-dV(2))/sDb(2));
fprintf(fid,'\n');

% ---------- PART E: Si 形态合成闭环 ----------
rng(20260909);
d0list = [3 5 10 30]; M = 20;
biasD = zeros(1,4); spreadD = zeros(1,4); biasA = zeros(1,4); spreadA = zeros(1,4);
raw = readmatrix(fullfile('附件','附件3.xlsx'));
D = raw(:,1); R = raw(:,2);
in = D >= band(1) & D <= band(2); Df = D(in); Rf = R(in);
xn = (Df-mean(Df))/(max(Df)-min(Df));
pf = polyfit(xn, Rf, 7);
bgFun = @(sg) polyval(pf, (sg-mean(Df))/(max(Df)-min(Df)));
pmG = drude_params('Si');
cosG = cos(asin(sind(angles(1)))/nSi);
sigN3 = sigN(1);
for di = 1:4
    d0 = d0list(di);
    recD = zeros(M,1); recA = zeros(M,1);
    for m = 1:M
        Rtrue = v20_airy_forward(Df, d0, angles(1), pmG, struct());
        Rsyn = bgFun(Df) + Rtrue + sigN3*randn(size(Df));
        Fsyn = Rsyn - polyval(pf, xn);
        mdl = @(par) par(1) + (par(2)+par(3).*(Df-sigCm)/1000).*cos(2*pi*par(4).*Df + par(5)*pi);
        x0 = [0, 0.5, 0, 2*pi*cosG*d0*1e-4, -0.3];
        lb = [-5, 0, -1, 2*pi*cosG*1e-4, -1]; ub = [10, 10, 1, 2*pi*cosG*50e-4, 1];
        pk = lsqnonlin(@(q)(mdl(q)-Fsyn)/sigN3, x0, lb, ub, opts);
        recD(m) = pk(4)/(2*nSi*cosG)*1e4;
        [chi2g, dGf] = profile_d_v20(Df, Fsyn, angles(1), pmG, sigN3, sigCm, dGrid);
        [~,im] = min(chi2g);
        recA(m) = refine_d(dGf, im, chi2g);
    end
    biasD(di) = median(recD)-d0;  spreadD(di) = 1.4826*mad(recD);
    biasA(di) = median(recA)-d0;  spreadA(di) = 1.4826*mad(recA);
    fprintf(fid,'[闭环Si d0=%3d um] 双光束 bias=%+.3f spread=%.3f | v2.0 bias=%+.3f spread=%.3f\n', ...
        d0, biasD(di), spreadD(di), biasA(di), spreadA(di));
end
fprintf(fid,'[D4 预览] 偏差方向与量级——EXP-8 将扩展为 q 关系曲线\n');
fclose(fid);

% ---------- 图 ----------
fig = figure('Position',[60 60 1400 800],'Visible','off');
subplot(2,2,1);
plot(Dcell{1}, Fcell{1},'b', Dcell{1}, resDb{1}+mean(Fcell{1}),'r-'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('Fringe (%)');
legend('data','dual-beam fit','Location','best'); title('Att3: dual-beam (Si) fit');
subplot(2,2,2);
plot(Dcell{1}, resDb{1},'r-'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('Residual (%)'); title('Dual-beam residual (structured)');
subplot(2,2,3);
semilogx(spList, scanRMSE,'o-'); grid on;
xlabel('\sigma_p (cm^{-1})'); ylabel('RMSE (%)'); title('\sigma_p sensitivity scan (att3)');
subplot(2,2,4);
errorbar(1:4, biasA, spreadA,'o'); hold on;
errorbar(1:4, biasD, spreadD,'s'); grid on;
set(gca,'XTickLabel',{'3um','5um','10um','30um'});
legend('v2.0','dual-beam','Location','best'); ylabel('recovery bias (um)');
title('Si closed loop: recovery bias');
saveas(fig, fullfile(outDir,'EXP6_W3_fits.png'));
disp('EXP6W3_DONE');
end

% ---------------- 辅助 ----------------
function [chi2g, dGridF] = profile_d_v20(Df, F, angle, pm, sigN, sigCm, dGrid)
chi2g = zeros(size(dGrid)); dGridF = dGrid;
Lin = [ones(size(Df)), (Df-sigCm)/1000];
for gi = 1:numel(dGrid)
    Ra = v20_airy_forward(Df, dGrid(gi), angle, pm, struct());
    xn = (Df-mean(Df))/(max(Df)-min(Df));
    Fr = Ra - polyval(polyfit(xn, Ra, 7), xn);
    M = [Fr, Lin];
    coef = M\F;
    r = F - M*coef;
    chi2g(gi) = sum((r/sigN).^2);
end
end

function d = refine_d(dGrid, im, chi2g)
d = dGrid(im);
if im>1 && im<numel(dGrid)
    y1=chi2g(im-1); y2=chi2g(im); y3=chi2g(im+1); den=y1-2*y2+y3;
    if den>0, d = d + 0.5*(y1-y3)/den*(dGrid(2)-dGrid(1)); end
end
end

function sd = sigma_from_curve(dGrid, chi2g, im)
% Δchi²=1 曲率法
if im>1 && im<numel(dGrid)
    y1=chi2g(im-1); y2=chi2g(im); y3=chi2g(im+1); den=y1-2*y2+y3;
    if den>0, sd = sqrt(1/den)*(dGrid(2)-dGrid(1))/2; else, sd = (dGrid(2)-dGrid(1)); end
else
    sd = (dGrid(2)-dGrid(1));
end
sd = max(sd, 0.005);
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

function J = numjac_local(fun, par, Dall)
np = numel(par); J = zeros(numel(Dall), np);
for j = 1:np
    dp = max(1e-8, abs(par(j))*1e-6);
    pp = par; pp(j)=pp(j)+dp; pm = par; pm(j)=pm(j)-dp;
    J(:,j) = (fun(pp)-fun(pm))/(2*dp);
end
end
