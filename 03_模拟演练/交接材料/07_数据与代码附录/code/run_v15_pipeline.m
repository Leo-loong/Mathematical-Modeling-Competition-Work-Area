%% run_v15_pipeline.m — v1.5 完整反演管线 + 验证闭环 (V-3/V-4, 第3块)
% 流程: 实测三域估计 -> 合成闭环(D3: 10/30/100μm×30次, 估计器误差模型)
%       -> 偏差校正 + 逆方差融合 + X²两级检验(D1) -> 联合E3 + 残差诊断(D2)
%       -> bootstrap(N=200, 残差重采样, 诚实条款)
% Input : 附件1/2.xlsx
% Output: 实验包-1/work/out/V4_report.txt (UTF-8), V4_验证闭环.png
% Run   : matlab -batch "addpath('src/model'); addpath('src/validation'); run_v15_pipeline"
% 对应  : docs/01 D1-D4; 模型设计/02 规格; 实验包-1/03_实现块与验证.md

function run_v15_pipeline()
rootDir = mfilename('fullpath');
for i = 1:3, rootDir = fileparts(rootDir); end
outDir = fullfile(rootDir,'模型设计','实验包-1','work','out');
fid = fopen(fullfile(outDir,'V4_report.txt'),'w','n','UTF-8');
fprintf(fid,'v1.5 管线与验证闭环  %s\n==================================================\n\n', ...
    char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')));

angles = [10 15]; sig0 = 1100; sigCm = 2550; nref = 2.55;
opts = optimoptions('lsqnonlin','Display','off','MaxIterations',1500,...
    'FunctionTolerance',1e-13,'StepTolerance',1e-13);

% ---------- 数据准备 ----------
Dcell = cell(1,2); Fcell = cell(1,2); sigN = zeros(1,2); bgCell = cell(1,2);
for k = 1:2
    raw = readmatrix(fullfile(rootDir,'附件',sprintf('附件%d.xlsx',k)));
    D = raw(:,1); R = raw(:,2);
    in = D >= sig0; Df = D(in); Rf = R(in);
    xn = (Df-mean(Df))/(max(Df)-min(Df));
    pf = polyfit(xn, Rf, 7);
    bgCell{k} = @(sg) polyval(pf, (sg-mean(Df))/(max(Df)-min(Df)));
    Fcell{k} = Rf - polyval(pf, xn);
    Dcell{k} = Df;
    sigN(k) = 1.4826*mad(diff(Rf),1)/sqrt(2);
end

% ---------- 1) 实测三域估计 ----------
dRaw = zeros(2,3); sStat = zeros(2,3); diagI = cell(1,2); estAll = cell(1,2);
for k = 1:2
    [est, di] = sic_e1_e2_e3(Dcell{k}, Fcell{k}, sigN(k), angles(k), nref, opts);
    estAll{k} = est; diagI{k} = di;
    dRaw(k,:) = [est.e1.d, est.e2.d, est.e3.d];
    sStat(k,:) = [est.e1.sd, est.e2.sd, est.e3.sd];
    fprintf(fid,'[实测 附件%d(%d°)] E1=%.3f±%.3f | E2=%.3f±%.3f | E3=%.3f±%.3f um\n', ...
        k, angles(k), dRaw(k,1), sStat(k,1), dRaw(k,2), sStat(k,2), dRaw(k,3), sStat(k,3));
    resd = di.e3res;
    fprintf(fid,'  [D2 E3残差] std=%.4f%%(噪声%.4f%%) lag1自相关=%.3f runs-z=%.2f\n', ...
        std(resd), sigN(k), autocorr1(resd), runs_test(resd));
end

% ---------- 2) 合成闭环 D3 (估计器误差模型, 用附件1实拟形状做发生器) ----------
rng(20260909);
d0list = [10 30 100]; M = 30;
bias = zeros(3,3); spread = zeros(3,3);
parGen = diagI{1}.e3par;      % 附件1 E3 拟合形状 [phi12, c0, p, amp, a1]
for di = 1:3
    d0 = d0list(di);
    rec = zeros(M,3);
    for m = 1:M
        Df = Dcell{1};
        pTrue = 2*nref*cos(asin(sind(angles(1))/nref))*d0*1e-4;
        Ftrue = parGen(4)*2*abs((1 - nref*cos(asin(sind(angles(1))/nref)))/(1 + nref*cos(asin(sind(angles(1))/nref)))) ...
                .*cos(2*pi*pTrue.*Df + parGen(1)*pi) + parGen(2) + parGen(5).*(Df-sigCm)/1000;
        Rsyn = bgCell{1}(Df) + Ftrue + sigN(1)*randn(size(Df));
        Fsyn = Rsyn - bgCell{1}(Df);     % 管线同款背景扣除
        est = sic_e1_e2_e3(Df, Fsyn, sigN(1), angles(1), nref, opts);
        rec(m,:) = [est.e1.d, est.e2.d, est.e3.d];
    end
    bias(:,di) = median(rec) - d0;
    spread(:,di) = 1.4826*mad(rec);
    fprintf(fid,'[D3 合成 d0=%3d um] E1 bias=%+.3f spread=%.3f | E2 %+.3f/%.3f | E3 %+.3f/%.3f\n', ...
        d0, bias(1,di), spread(1,di), bias(2,di), spread(2,di), bias(3,di), spread(3,di));
end
fprintf(fid,'[D3 小结] spread 即各估计器算法自身精度上限的稳健估计; 分布图见 work/out/V4_验证闭环.png\n\n');

% ---------- 3) 偏差校正 + 融合 + X² 两级 ----------
sigmaTotal = cell(1,2);
dHat = zeros(2,3); sHat = zeros(2,3);
for k = 1:2
    dMean = mean(dRaw(k,:));
    st = zeros(1,3);
    for mi = 1:3
        sp = interp1(d0list, squeeze(spread(mi,:)), dMean, 'linear','extrap');
        sp = max(sp, spread(mi,1));          % 不低于 d0=10 的 spread
        st(mi) = sqrt(sStat(k,mi)^2 + sp^2);
    end
    sigmaTotal{k} = st;
    bNow = arrayfun(@(mi) interp1(d0list, bias(mi,:), dMean, 'linear','extrap'), 1:3);
    dHat(k,:) = dRaw(k,:) - bNow;
    sHat(k,:) = st;
end
chiCrit = chi2inv(0.95, 2);
fusedA = zeros(1,2); sFusedA = zeros(1,2); x2a = zeros(1,2);
for k = 1:2
    w = 1./sHat(k,:).^2;
    fusedA(k) = sum(w.*dHat(k,:))/sum(w);
    sFusedA(k) = 1/sqrt(sum(w));
    x2a(k) = sum(w.*(dHat(k,:)-fusedA(k)).^2);
    fprintf(fid,'[X² L1 附件%d] 三估计器(校正后)=%.3f/%.3f/%.3f; 融合=%.3f±%.3f um, X²=%.2f (95%%临界=%.2f, dof=2) -> %s\n', ...
        k, dHat(k,:), fusedA(k), sFusedA(k), x2a(k), chiCrit, passfail(x2a(k)<=chiCrit));
end
w2 = 1./sFusedA.^2;
dFinal = sum(w2.*fusedA)/sum(w2);
sFinal = 1/sqrt(sum(w2));
x2b = sum(w2.*(fusedA-dFinal).^2);
chiCrit2 = chi2inv(0.95, 1);
fprintf(fid,'[X² L2 双角度] 最终融合=%.3f±%.3f um, X²=%.2f (95%%临界=%.2f, dof=1) -> %s\n', ...
    dFinal, sFinal, x2b, chiCrit2, passfail(x2b<=chiCrit2));

% ---------- 4) 联合 E3 (双角度共享 d) ----------
Dj = [Dcell{1}; Dcell{2}]; Fj = [Fcell{1}; Fcell{2}];
wj = [1/sigN(1)^2*ones(size(Dcell{1})); 1/sigN(2)^2*ones(size(Dcell{2}))];
angId = [ones(size(Dcell{1})); 2*ones(size(Dcell{2}))];
sin_t = sind(angles);
mdlJ = @(par) mdl_joint(par, Dj, angId, sin_t, nref, sigCm);
lbJ = [3, -1, 0, 0, -2, -1]; ubJ = [20, 1, 10, 10, 2, 1];
bestJ = inf; pj = [];
for ph0 = [-0.3, 0.7]
    x0 = [dFinal, ph0, 0.35, 0.35, 0, -0.5];
    [pk,~,rr] = lsqnonlin(@(p)((mdlJ(p)-Fj).*sqrt(wj)), x0, lbJ, ubJ, opts);
    if sum(rr.^2) < bestJ, bestJ = sum(rr.^2); pj = pk; rj = rr; end
end
Jj = numjac_local(@(p)mdlJ(p), pj, Dj);
covJ = pinv(Jj'*Jj)*(sum(rj.^2))/(numel(Fj)-numel(pj));
sdJoint = sqrt(covJ(1,1));
fprintf(fid,'[联合E3] d_joint=%.4f±%.4f um (共享d; phi12=%.3f; amp10=%.3f amp15=%.3f) red-chi2=%.1f\n', ...
    pj(1), sdJoint, pj(2), pj(3), pj(4), sum(rj.^2)/(numel(Fj)-6));
resJ = (Fj - mdlJ(pj)).*sqrt(wj);
fprintf(fid,'  [D2 联合残差] lag1自相关=%.3f runs-z=%.2f\n', autocorr1(resJ), runs_test(resJ));

% ---------- 5) bootstrap (N=200, 分块残差重采样, 块长=1条纹周期, 保留相关结构) ----------
Nboot = 200;
fusedBoot = zeros(2, Nboot); e1Boot = zeros(2,Nboot); e3Boot = zeros(2,Nboot);
rng(42);
for k = 1:2
    resid0 = diagI{k}.e3res;
    model0 = diagI{k}.e3model;
    nPts = numel(resid0);
    Lblk = 500;
    per = diagI{k}.period; per = per(find(isfinite(per),1));
    if ~isempty(per) && per > 0
        Lblk = round(per/(Dcell{k}(2)-Dcell{k}(1)));
    end
    Lblk = min(max(Lblk,50), floor(nPts/2));
    if ~isfinite(Lblk) || Lblk < 10 || Lblk >= nPts, Lblk = 500; end
    nBlk = ceil(nPts/Lblk);
    for b = 1:Nboot
        starts = randi(nPts-Lblk, nBlk,1);
        idx = cell2mat(arrayfun(@(s) s:(s+Lblk-1), starts, 'UniformOutput', false));
        idx = idx(1:nPts);
        Fb = model0 + resid0(idx);
        % 与管线带宽一致: 高通去除重采样引入的平滑伪分量(|f|<f0/2)
        Nb = numel(Fb); Yb = fft(Fb - mean(Fb));
        fsb = 1/median(diff(Dcell{k}));
        faxb = (0:Nb-1)'/Nb*fsb;
        cutb = 1/(2*229);
        Yb(faxb < cutb | faxb > fsb-cutb) = 0;
        Fb = real(ifft(Yb));
        estb = sic_e1_e2_e3(Dcell{k}, Fb, sigN(k), angles(k), nref, opts);
        dRall = [estb.e1.d, estb.e2.d, estb.e3.d];
        ok = isfinite(dRall);
        if ~any(ok), fusedBoot(k,b)=NaN; e1Boot(k,b)=estb.e1.d; e3Boot(k,b)=estb.e3.d; continue; end
        dR = dRall(ok);
        dMean = median(dR);
        bVec = arrayfun(@(mi) interp1(d0list, bias(mi,:), dMean, 'linear','extrap'), find(ok));
        dR = dR - bVec;
        fusedBoot(k,b) = median(dR);   % 稳健聚合: 单方法离群不污染
        e1Boot(k,b) = estb.e1.d; e3Boot(k,b) = estb.e3.d;
    end
    fb = fusedBoot(k,:); fb = fb(isfinite(fb));
    e1v = e1Boot(k,:); e1v = e1v(isfinite(e1v));
    e3v = e3Boot(k,:); e3v = e3v(isfinite(e3v));
    fprintf(fid,'[分块bootstrap 附件%d] E1中位=%.3f E3中位=%.3f; 融合分布: median=%.3f, robustσ=%.3f, 2.5/97.5%%=[%.3f, %.3f]\n', ...
        k, median(e1v), median(e3v), median(fb), ...
        1.4826*mad(fb), prctile(fb,2.5), prctile(fb,97.5));
end
fb1 = fusedBoot(1,:); fb1 = fb1(isfinite(fb1));
fb2 = fusedBoot(2,:); fb2 = fb2(isfinite(fb2));
sEmp = [1.4826*mad(fb1), 1.4826*mad(fb2)];
sEmp = max(sEmp, 0.05);   % 下限保护: 经验σ不低于 0.05um(分块重采样分辨率极限)
w3 = 1./sEmp.^2;
dFinalEmp = sum(w3.*fusedA)/sum(w3);
x2Emp = sum(w3.*(fusedA-dFinalEmp).^2);
fprintf(fid,'[X² L2 (经验σ)] X²=%.2f (95%%临界=%.2f, dof=1) -> %s\n', x2Emp, chiCrit2, passfail(x2Emp<=chiCrit2));
fprintf(fid,'\n==================================================\n[第3块验收指标]\n');
fprintf(fid,'D1 双角度: 融合 %.3f / %.3f um (经验σ %.3f/%.3f); 统计σ下 X²L2=%.2f (%s; 若FAIL, 角度间系统差已并入经验σ)\n', ...
    fusedA(1), fusedA(2), sEmp(1), sEmp(2), x2b, passfail(x2b<=chiCrit2));
fprintf(fid,'D3 合成闭环: E3 spread(10/30/100um)=%.3f/%.3f/%.3f um (算法自身精度上限)\n', ...
    spread(3,1), spread(3,2), spread(3,3));
fprintf(fid,'bootstrap(诚实条款): 经验误差棒 %.3f/%.3f um (分块重采样, 保留系统误差相关结构)\n', sEmp);
fprintf(fid,'[转第4块] 融合值 d = %.3f um; 统计σ=%.3f; 经验σ=%.3f/%.3f(角度); 模型系统差见预算\n', ...
    dFinalEmp, sFinal, sEmp(1), sEmp(2));
fclose(fid);

% ---------- 图 ----------
fig = figure('Position',[60 60 1400 800],'Visible','off');
subplot(2,2,1);
bar(spread'); legend('E1','E2','E3'); grid on;
set(gca,'XTickLabel',{'10um','30um','100um'}); ylabel('robust spread (um)');
title('D3: synthetic recovery spread');
subplot(2,2,2);
for k=1:2
    errorbar(angles(k), fusedA(k), sFusedA(k),'o','LineWidth',1.5); hold on;
end
errorbar(mean([10 15]), dFinal, sFinal,'ks','LineWidth',1.5); grid on;
xlim([5 20]); xlabel('incidence angle (deg)'); ylabel('d (um)');
title('D1: two-angle cross validation');
subplot(2,2,3);
sel1 = angId==1;
yJ = mdlJ(pj);
plot(Dj(sel1), Fj(sel1)-yJ(sel1),'r-'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('Residual (%)'); title('D2: joint E3 residual (10°)');
subplot(2,2,4);
histogram(fusedBoot(1,:),20,'FaceAlpha',0.6); hold on;
histogram(fusedBoot(2,:),20,'FaceAlpha',0.6); grid on;
legend('10°','15°'); xlabel('fused d (um)'); title('bootstrap fusion distribution');
saveas(fig, fullfile(outDir,'V4_验证闭环.png'));
disp('PIPELINE_DONE');
end

% ---------------- 辅助 ----------------
function y = mdl_joint(par, Dj, angId, sin_t, nref, sigCm)
% [d, phi12, amp10, amp15, c0, a1]
dcm = par(1)*1e-4;
y = zeros(size(Dj));
for k = 1:2
    sel = angId==k; sg = Dj(sel);
    cost = sqrt(1 - sin_t(k)^2/nref^2);
    r01 = (1 - nref*cost)/(1 + nref*cost);
    Phi = 4*pi*sg.*dcm*nref*cost + par(2)*pi;
    y(sel) = par(2+k)*2*abs(r01).*cos(Phi) + par(5) + par(6).*(sg-sigCm)/1000;
end
end

function a = autocorr1(x)
x = x(:); x = x(isfinite(x));
x = x - mean(x);
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

function s = passfail(tf)
if tf, s='PASS'; else, s='FAIL'; end
end

function J = numjac_local(fun, par, Dall)
np = numel(par); J = zeros(numel(Dall), np);
for j = 1:np
    dp = max(1e-8, abs(par(j))*1e-6);
    pp = par; pp(j)=pp(j)+dp; pm = par; pm(j)=pm(j)-dp;
    J(:,j) = (fun(pp)-fun(pm))/(2*dp);
end
end
