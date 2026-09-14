function [est, diagInfo] = sic_e1_e2_e3(Df, F, sigN, angle, nref, opts)
%% 单角度三域估计器 (v1.5 规格: 模型设计/02)
% E1 极值回归: robust极值+交替约束+亚像素抛物线细化 -> m=k·σ+c, d=k/(4·n·cosθ₁)
% E2 谱域: 去趋势+Hann+零填充FFT, 峰位=d̂₂, 半高宽->σ₂
% E3 全谱拟合: v1.0定稿正演 [phi12, c0, p(OPD), amp, a1], lsqnonlin, p->d
% est 字段: e1/e2/e3 各含 d, sd; diagInfo: 极值/残差诊断
cost = cos(asin(sind(angle)/nref));
fs = 1/median(diff(Df));

% ---------- E1 (多假设周期竞争) ----------
sigCm = mean(Df);
Fd = detrend(F);
ZP = 8;
Yp = abs(fft(Fd.*hann_win(numel(Fd)), numel(Fd)*ZP));
Yh = Yp(1:floor(numel(Yp)/2));
fh = (0:numel(Yh)-1)'/(numel(Yp))*fs;
% GB/T 物理窗内的候选周期: top-5 局部峰
fDmin = 2*nref*cost*2*1e-4;    % d=2um -> 低频
fDmax = 2*nref*cost*250*1e-4;  % d=250um -> 高频
candMask = fh >= fDmin & fh <= fDmax;
Ym = Yh; Ym(~candMask) = 0;
[pkv, pkidx] = local_extrema_vec(Ym);
[~,ord] = sort(pkv,'descend');
if isempty(ord)
    candPeriod = 1/((fDmin+fDmax)/2);
else
    candPeriod = 1./fh(pkidx(ord(min(1:5,end))));
end
best = struct('rmse', inf, 'd', NaN, 'sd', NaN, 'phi0', NaN, 'nExt', 0, 'period', NaN, 'chi2model', inf);
extSigBest = []; extValBest = []; extTypeBest = [];
for pc = candPeriod
    [e1t, extS, extV, extT] = try_e1(Df, F, pc, sigN, nref, cost);
    if ~(e1t.nExt >= 8 && isfinite(e1t.d)), continue; end
    % 全谱模型裁决: 固定 d=d_c, 线性拟合 [cos, sin, 1, slope], chi2 最小者胜
    pC = 2*nref*cost*e1t.d*1e-4;
    PhC = 2*pi*pC.*Df;
    M = [cos(PhC), sin(PhC), ones(size(PhC)), (Df-sigCm)/1000];
    coef = M\F;
    chi2m = sum((F - M*coef).^2);
    if chi2m < best.chi2model
        best = e1t; best.chi2model = chi2m; best.period = pc;
        extSigBest = extS; extValBest = extV; extTypeBest = extT;
    end
end
est.e1 = best;
diagInfo.extSig = extSigBest; diagInfo.extVal = extValBest; diagInfo.extType = extTypeBest;
period = best.period;

% ---------- E2 ----------
% 峰搜索: E1 可用时取 E1 厚度 ±50% 窗, 否则 GB/T 3~200um 物理窗
if isfinite(est.e1.d)
    fLo = 2*nref*cost*max(est.e1.d*0.5,1)*1e-4;
    fHi = 2*nref*cost*est.e1.d*1.5*1e-4;
else
    fLo = 2*nref*cost*2*1e-4;
    fHi = 2*nref*cost*250*1e-4;
end
band2 = fh >= fLo & fh <= fHi;
[~,ipE2] = max(Yh.*band2);
est.e2 = struct('d', fh(ipE2)/(2*nref*cost)*1e4, 'sd', NaN);
halfPower = Yh(ipE2)/sqrt(2);
iL = ipE2; while iL>1 && Yh(iL)>halfPower, iL=iL-1; end
iR = ipE2; while iR<numel(Yh) && Yh(iR)>halfPower, iR=iR+1; end
fwhm = (iR-iL)*(fh(2)-fh(1));
est.e2.sd = (fwhm/2.355)/(2*nref*cost)*1e4;

% ---------- E3 ----------
sigCm = mean(Df);
r01c = (1 - nref*cost)/(1 + nref*cost);
mdl3 = @(par) par(4)*2*abs(r01c).*cos(2*pi*par(3).*Df + par(1)*pi) ...
             + par(2) + par(5).*(Df-sigCm)/1000;
cand = [est.e1.d, est.e2.d];
cand = cand(isfinite(cand));
if isempty(cand), d0 = 8.0; else, d0 = median(cand); end
p0 = 2*nref*cost*d0*1e-4;
lb = [-1, -2, p0/2, 0, -1]; ub = [1, 2, p0*2, 10, 1];
bestSse = inf; pk = [];
for ph0 = [-0.3, 0.7]
    [pkk,~,rrk] = lsqnonlin(@(p)(mdl3(p)-F)/sigN, [ph0, 0, p0, 1, 0], lb, ub, opts);
    if sum(rrk.^2) < bestSse, bestSse = sum(rrk.^2); pk = pkk; rr = rrk; end
end
J = numjac_local(@(p)mdl3(p), pk, Df);
n = numel(F);
covB = pinv(J'*J)*(sum(rr.^2)*sigN^2)/n;
sd3 = sqrt(covB(3,3))/(2*nref*cost)*1e4;
est.e3 = struct('d', pk(3)/(2*nref*cost)*1e4, 'sd', sd3, 'phi0', pk(1), ...
    'amp', pk(4), 'p', pk(3));
diagInfo.e3par = pk; diagInfo.e3res = rr*sigN; diagInfo.e3model = mdl3(pk);
diagInfo.sigN = sigN;
diagInfo.period = period;
end

function [e1, extS, extV, extT] = try_e1(Df, F, period, sigN, nref, cost)
% 给定周期假设, 完整执行 检测->交替约束->亚像素->robust回归
period = period(1);
if ~isfinite(period) || period <= 0
    e1 = struct('d', NaN, 'sd', NaN, 'phi0', NaN, 'nExt', 0, 'rmse', inf);
    extS = []; extV = []; extT = {}; return;
end
[extSig, extVal, extType] = robust_extrema(Df, F, period, sigN);
[extSig, extVal, extType] = enforce_alternating(extSig, extVal, extType, period);
extSigRef = extSig;
for ii = 1:numel(extSig)
    [~,ci] = min(abs(Df - extSig(ii)));
    if ci>2 && ci<numel(Df)-2
        y1=F(ci-2); y2=F(ci); y3=F(ci+2);
        den = y1 - 2*y2 + y3;
        if abs(den)>eps && ((strcmp(extType{ii},'max') && y2>y1 && y2>y3) || (strcmp(extType{ii},'min') && y2<y1 && y2<y3))
            dsig = (Df(ci+2)-Df(ci-2))/4;
            delta = (y1-y3)/den*dsig;
            if abs(delta)<dsig, extSigRef(ii) = extSig(ii) + delta; end
        end
    end
end
nExt = numel(extSigRef);
mIdx = (0:nExt-1)';
e1 = struct('d', NaN, 'sd', NaN, 'phi0', NaN, 'nExt', nExt, 'rmse', inf);
if nExt >= 4
    keep = true(nExt,1);
    pm = [0 0]; residAll = mIdx;
    for it = 1:4
        pm = polyfit(extSigRef(keep), mIdx(keep), 1);
        residAll = mIdx - polyval(pm, extSigRef);
        sR = 1.4826*mad(residAll(keep));
        if sR < eps, break; end
        keepNew = abs(residAll) < 3*sR;
        if ~isequal(keepNew, keep) && sum(keepNew) >= 4
            keep = keepNew;
        else
            break;
        end
    end
    resid = residAll(keep);
    kEst = pm(1); cEst = pm(2);
    Sxx = sum((extSigRef(keep)-mean(extSigRef(keep))).^2);
    sigK = sqrt(sum(resid.^2)/(sum(keep)-2)/Sxx);
    e1 = struct('d', kEst/(4*nref*cost)*1e4, 'sd', sigK/(4*nref*cost)*1e4, ...
        'phi0', mod(cEst,1), 'nExt', sum(keep), 'rmse', sqrt(mean(resid.^2)));
    extS = extSigRef; extV = extVal; extT = extType;
else
    extS = extSig; extV = extVal; extT = extType;
end
end

function [pkv, pkidx] = local_extrema_vec(x)
n = numel(x); pkidx = []; pkv = [];
for i = 2:n-1
    if x(i)>x(i-1) && x(i)>=x(i+1) || x(i)>=x(i-1) && x(i)>x(i+1)
        pkidx(end+1)=i; pkv(end+1)=x(i); %#ok<AGROW>
    end
end
end

function J = numjac_local(fun, par, Dall)
np = numel(par); J = zeros(numel(Dall), np);
for j = 1:np
    dp = max(1e-8, abs(par(j))*1e-6);
    pp = par; pp(j)=pp(j)+dp; pm = par; pm(j)=pm(j)-dp;
    J(:,j) = (fun(pp)-fun(pm))/(2*dp);
end
end

function [extSig, extVal, extType] = robust_extrema(D, F, period, sigN)
w = max(3, round(period/4));
[cand, ctype] = raw_extrema(F);
keep = false(numel(cand),1);
for i = 1:numel(cand)
    ci = cand(i);
    lo = max(1, ci-w); hi = min(numel(F), ci+w);
    seg = F(lo:hi);
    if strcmp(ctype{i},'max')
        keep(i) = F(ci) >= max(seg)-1e-12 && (F(ci)-min(seg)) > 4*sigN;
    else
        keep(i) = F(ci) <= min(seg)+1e-12 && (max(seg)-F(ci)) > 4*sigN;
    end
end
cand = cand(keep); ctype = ctype(keep);
extSig = D(cand); extVal = F(cand); extType = ctype;
end

function [S, V, T] = enforce_alternating(S, V, T, period)
halfp = period/2;
i = 2;
while i <= numel(S)
    if strcmp(T{i}, T{i-1})
        if strcmp(T{i},'max'), rm = i - 1*(V(i-1) >= V(i));
        else,                  rm = i - 1*(V(i-1) <= V(i));
        end
        S(rm)=[]; V(rm)=[]; T(rm)=[];
        i = max(2, i-1);
    else
        i = i + 1;
    end
end
guard = 0;
while guard < 10
    guard = guard + 1;
    dsp = diff(S);
    if isempty(dsp) || numel(S) < 3, break; end
    bad = find(dsp < 0.5*halfp);
    if isempty(bad), break; end
    b = bad(1);
    if b+1 > numel(S), break; end
    promA = V(b) - min(V(max(1,b-2)):V(b));
    promB = V(b+1) - min(V(b+1):V(min(numel(S),b+3)));
    if abs(promA) >= abs(promB), rm = b+1; else, rm = b; end
    S(rm)=[]; V(rm)=[]; T(rm)=[];
end
end

function [cand, ctype] = raw_extrema(x)
n = numel(x); cand = []; ctype = {};
for i = 2:n-1
    if x(i)>=x(i-1) && x(i)>=x(i+1) && (x(i)>x(i-1) || x(i)>x(i+1))
        cand(end+1)=i; ctype{end+1}='max'; %#ok<AGROW>
    elseif x(i)<=x(i-1) && x(i)<=x(i+1) && (x(i)<x(i-1) || x(i)<x(i+1))
        cand(end+1)=i; ctype{end+1}='min'; %#ok<AGROW>
    end
end
end

function w = hann_win(N)
w = 0.5*(1 - cos(2*pi*(0:N-1)'/(N-1)));
end
