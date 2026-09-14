function varargout = drying_common(action, varargin)
%DRYING_COMMON  A题四问共用的圆柱药材耦合传热传质求解函数。
%   本文件采用守恒有限体积离散和 Picard 迭代处理物性随含水率、温度
%   变化的非线性；所有主程序均通过本函数读取数据、求解、导出及绘图。
%
%   例：cfg = drying_common('config', 1);
%       air = drying_common('load_air', 'data/附件1.xlsx');
%       [t,T,C,meta] = drying_common('solve_fixed', cfg, air);

switch lower(action)
    case 'config'
        varargout{1} = make_config(varargin{1});
    case 'load_air'
        varargout{1} = load_air_data(varargin{1});
    case 'load_radius'
        varargout{1} = load_radius_data(varargin{1});
    case 'solve_fixed'
        [varargout{1:nargout}] = solve_fixed(varargin{1}, varargin{2});
    case 'solve_shrink'
        [varargout{1:nargout}] = solve_shrink(varargin{1}, varargin{2}, varargin{3});
    case 'write_result'
        write_result(varargin{1}, varargin{2}, varargin{3}, varargin{4}, varargin{5}, varargin{6});
    case 'make_plots'
        make_plots(varargin{1}, varargin{2}, varargin{3}, varargin{4}, varargin{5}, varargin{6});
    otherwise
        error('drying_common:UnknownAction', '不支持的动作：%s', action);
end
end

function cfg = make_config(q)
% 统一单位：长度 m，时间 s，温度 ℃（扩散系数的绝对温度在 props 中转换）。
cfg.id = q;
cfg.R0 = 0.02;
cfg.N = 20;                       % r=0,0.1,...,2.0 cm，共 21 个节点
cfg.T0 = 28;
cfg.C0 = 2.55;
cfg.h = 25;                       % W/(m^2·℃)
cfg.km = 8e-7;                    % m/s
cfg.dt = 1;                       % 内部时间步；隐式格式下数值稳定
cfg.picardIter = 3;
cfg.picardTol = 1e-7;
cfg.relax = 0.85;
cfg.stopC = false;
cfg.targetC = 0.15;

switch q
    case 1
        cfg.propertyCase = 1;
        cfg.tMax = 1800;
        cfg.outEvery = 1;
        cfg.figureTimes = [100, 300, 600, 1200, 1800];
    case 2
        cfg.propertyCase = 2;
        cfg.tMax = 3*3600;
        cfg.outEvery = 1;
        cfg.figureTimes = [0, 1800, 3600, 7200, 10800];
    case 3
        cfg.propertyCase = 2;
        cfg.tMax = 600*3600;
        cfg.dt = 30;
        cfg.outEvery = 60;
        cfg.stopC = true;
        cfg.targetC = 0.15;
        cfg.figureTimes = [0, 6, 12, 24, 72, 168, 360, 558]*3600;
    case 4
        cfg.propertyCase = 4;
        cfg.tMax = 72*3600;
        cfg.dt = 30;
        cfg.outEvery = 60;
        cfg.figureTimes = [0, 6, 12, 24, 48, 72]*3600;
    otherwise
        error('题号只能为 1、2、3 或 4。');
end
end

function air = load_air_data(filename)
data = readmatrix(filename);
data = data(all(isfinite(data),2),:);
if size(data,2) < 3
    error('附件 1 应至少包含“时间、温度、水分浓度”三列。');
end
air.t = data(:,1);
air.T = data(:,2);
air.C = data(:,3);
end

function radius = load_radius_data(filename)
data = readmatrix(filename);
data = data(all(isfinite(data),2),:);
if size(data,2) < 2
    error('附件 2 应至少包含“时间、半径”两列。');
end
radius.t = data(:,1);
radius.R = data(:,2)/100;         % 附件半径单位为 cm，内部统一换为 m
radius.Rdot = gradient(radius.R, radius.t);
end

function [tOut, Tout, Cout, meta] = solve_fixed(cfg, air)
% 固定半径的一维径向有限体积求解器，适用于第 1、2、3 问。
r = linspace(0, cfg.R0, cfg.N+1)';
T = cfg.T0*ones(cfg.N+1,1);
C = cfg.C0*ones(cfg.N+1,1);
nSteps = round(cfg.tMax/cfg.dt);
nMax = floor(cfg.tMax/cfg.outEvery)+2;
tOut = zeros(nMax,1);
Tout = zeros(nMax,cfg.N+1);
Cout = zeros(nMax,cfg.N+1);
nOut = 0;
reached = false;
endTime = cfg.tMax;

for step = 0:nSteps
    t = step*cfg.dt;
    if mod(round(t), cfg.outEvery) == 0
        nOut = nOut + 1;
        tOut(nOut) = t;
        Tout(nOut,:) = T';
        Cout(nOut,:) = C';
    end

    if cfg.stopC && max(C) < cfg.targetC
        reached = true;
        endTime = t;
        break;
    end
    if step == nSteps
        break;
    end

    [Ta, Ca] = air_at(air, t);
    [T,C] = nonlinear_fixed_step(T, C, r, cfg, Ta, Ca);
end

% 若达到阈值的时刻不是整分钟，也保留最终一行，便于直接给出干燥时长。
if tOut(nOut) ~= endTime
    nOut = nOut + 1;
    tOut(nOut) = endTime;
    Tout(nOut,:) = T';
    Cout(nOut,:) = C';
end
tOut = tOut(1:nOut);
Tout = Tout(1:nOut,:);
Cout = Cout(1:nOut,:);
meta.r = r;
meta.endTime = endTime;
meta.reachedTarget = reached;
meta.description = '固定半径圆柱；守恒有限体积 + Picard 非线性迭代';
end

function [tOut, Tout, Cout, meta] = solve_shrink(cfg, air, radiusData)
% 第 4 问：在 x=r/R(t) 坐标中求解，显式加入收缩诱导的对流项。
x = linspace(0,1,cfg.N+1)';
T = cfg.T0*ones(cfg.N+1,1);
C = cfg.C0*ones(cfg.N+1,1);
nSteps = round(cfg.tMax/cfg.dt);
nMax = floor(cfg.tMax/cfg.outEvery)+2;
tOut = zeros(nMax,1);
Tout = zeros(nMax,cfg.N+1);
Cout = zeros(nMax,cfg.N+1);
Rout = zeros(nMax,1);
nOut = 0;

for step = 0:nSteps
    t = step*cfg.dt;
    [R,~] = radius_at(radiusData,t);
    if mod(round(t), cfg.outEvery) == 0
        nOut = nOut + 1;
        tOut(nOut) = t;
        Tout(nOut,:) = T';
        Cout(nOut,:) = C';
        Rout(nOut) = R;
    end
    if step == nSteps
        break;
    end

    [Ta,Ca] = air_at(air,t);
    [R,Rdot] = radius_at(radiusData,t);
    r = R*x;
    [T,C] = nonlinear_shrink_step(T,C,r,x,Rdot/R,cfg,Ta,Ca);
end

tOut = tOut(1:nOut);
Tout = Tout(1:nOut,:);
Cout = Cout(1:nOut,:);
Rout = Rout(1:nOut);
meta.x = x;
meta.Rout = Rout;
meta.endTime = tOut(end);
meta.description = 'x=r/R(t) 坐标；有限体积 + Picard 迭代 + 收缩对流项';
end

function [T,C] = nonlinear_fixed_step(Told, Cold, r, cfg, Ta, Ca)
Ti = Told;
Ci = Cold;
for it = 1:cfg.picardIter
    [rho,cp,k,~] = material_props(cfg.propertyCase,Ci,Ti);
    Tnew = diffuse_radial(Told,r,k,rho.*cp,cfg.dt,cfg.h,Ta,zeros(size(Ti)));
    [~,~,~,D] = material_props(cfg.propertyCase,max(Ci,1e-10),Tnew);
    Cnew = diffuse_radial(Cold,r,D,ones(size(Ci)),cfg.dt,cfg.km,Ca,zeros(size(Ci)));
    if max(abs(Tnew-Ti)) < cfg.picardTol && max(abs(Cnew-Ci)) < cfg.picardTol
        Ti = Tnew;
        Ci = Cnew;
        break;
    end
    Ti = cfg.relax*Tnew + (1-cfg.relax)*Ti;
    Ci = max(cfg.relax*Cnew + (1-cfg.relax)*Ci,1e-10);
end
T = Ti;
C = Ci;
end

function [T,C] = nonlinear_shrink_step(Told,Cold,r,x,beta,cfg,Ta,Ca)
% 从 C_t-beta*x*C_x=扩散项 得到 C_t=beta*x*C_x+扩散项。
Ti = Told;
Ci = Cold;
for it = 1:cfg.picardIter
    [rho,cp,k,~] = material_props(cfg.propertyCase,Ci,Ti);
    motionT = beta*x.*upwind_dx(Ti,x,beta);
    Tnew = diffuse_radial(Told,r,k,rho.*cp,cfg.dt,cfg.h,Ta,motionT);
    [~,~,~,D] = material_props(cfg.propertyCase,max(Ci,1e-10),Tnew);
    motionC = beta*x.*upwind_dx(Ci,x,beta);
    Cnew = diffuse_radial(Cold,r,D,ones(size(Ci)),cfg.dt,cfg.km,Ca,motionC);
    if max(abs(Tnew-Ti)) < cfg.picardTol && max(abs(Cnew-Ci)) < cfg.picardTol
        Ti = Tnew;
        Ci = Cnew;
        break;
    end
    Ti = cfg.relax*Tnew + (1-cfg.relax)*Ti;
    Ci = max(cfg.relax*Cnew + (1-cfg.relax)*Ci,1e-10);
end
T = Ti;
C = Ci;
end

function unew = diffuse_radial(uold,r,coef,capacity,dt,bc,ambient,extraRate)
% 径向守恒有限体积：capacity*du/dt = div(coef*grad u)+capacity*extraRate。
% 边界条件：-coef*du/dr = bc*(u-u_inf)。中心自动满足对称无通量条件。
n = numel(r);
vol = radial_volume(r);
faceR = 0.5*(r(1:end-1)+r(2:end));
dr = diff(r);
coefFace = harmonic_mean(coef(1:end-1),coef(2:end));
g = faceR.*coefFace./dr;

K = spalloc(n,n,3*n);
K(1,1) = -g(1);
K(1,2) =  g(1);
for i = 2:n-1
    K(i,i-1) = g(i-1);
    K(i,i) = -(g(i-1)+g(i));
    K(i,i+1) = g(i);
end
K(n,n-1) = g(end);
K(n,n) = -g(end) - r(end)*bc;
source = zeros(n,1);
source(n) = r(end)*bc*ambient;

mass = capacity.*vol/dt;
A = spdiags(mass,0,n,n) - K;
rhs = mass.*uold + source + capacity.*vol.*extraRate;
unew = A\rhs;
end

function vol = radial_volume(r)
edge = [0; 0.5*(r(1:end-1)+r(2:end)); r(end)];
vol = 0.5*(edge(2:end).^2-edge(1:end-1).^2);
end

function hm = harmonic_mean(a,b)
hm = 2*a.*b./max(a+b,eps);
end

function gradU = upwind_dx(u,x,beta)
% 迁移速度为 -beta*x。半径收缩 beta<0 时取从中心向表面的迎风差分。
gradU = zeros(size(u));
dx = x(2)-x(1);
if beta <= 0
    gradU(2:end) = (u(2:end)-u(1:end-1))/dx;
else
    gradU(1:end-1) = (u(2:end)-u(1:end-1))/dx;
    gradU(end) = gradU(end-1);
end
end

function [rho,cp,k,D] = material_props(propertyCase,C,Tc)
C = max(C,1e-10);
Tk = Tc + 273.15;
switch propertyCase
    case 1
        rho = 820*ones(size(C));
        cp = 2600*ones(size(C));
        k = 0.36*ones(size(C));
        D = 7e-9*exp(-0.89./C);
    case 2
        rho = 650 + 128*C;
        cp = 1450 + 2736*C./(C+1);
        k = 0.21 + 0.38*C./(C+1);
        D = 2.4e-3*exp(-0.45./C).*exp(-3850./Tk);
    case 4
        rho = 760 + 90*C;
        cp = 1850 + 2150*C./(C+1);
        k = 0.12 + 0.20*C./(C+1);
        D = 4.2e-4*exp(-0.30./C).*exp(-3850./Tk);
    otherwise
        error('未知物性参数组。');
end
end

function [Ta,Ca] = air_at(air,t)
tq = min(max(t,air.t(1)),air.t(end));
Ta = interp1(air.t,air.T,tq,'pchip');
Ca = interp1(air.t,air.C,tq,'pchip');
end

function [R,Rdot] = radius_at(radius,t)
tq = min(max(t,radius.t(1)),radius.t(end));
R = interp1(radius.t,radius.R,tq,'pchip');
Rdot = interp1(radius.t,radius.Rdot,tq,'pchip');
end

function write_result(cfg,root,tOut,Tout,Cout,meta)
resultDir = fullfile(root,'result');
if ~exist(resultDir,'dir')
    mkdir(resultDir);
end
template = fullfile(root,'data',sprintf('result%d_template.xlsx',cfg.id));
output = fullfile(resultDir,sprintf('result%d.xlsx',cfg.id));
copyfile(template,output,'f');
keep = tOut > 0;                  % 与题目给出的模板一致，结果从 1 s / 60 s 开始
t = tOut(keep);

if cfg.id <= 3
    r = meta.r*100;
    header = [{'时间\到药材中心的距离'}, num2cell(r')];
    if cfg.id <= 2
        writecell(header,output,'Sheet','温度','Range','A1');
        writematrix([t,Tout(keep,:)],output,'Sheet','温度','Range','A2');
        writecell(header,output,'Sheet','水分浓度','Range','A1');
        writematrix([t,Cout(keep,:)],output,'Sheet','水分浓度','Range','A2');
    else
        writecell(header,output,'Sheet','Sheet1','Range','A1');
        writematrix([t,Cout(keep,:)],output,'Sheet','Sheet1','Range','A2');
        write_q3_summary(resultDir,tOut,Cout,meta.r);
    end
else
    % 收缩过程中固定点只能取全过程最小半径以内；最后一列单列给出实际表面。
    Rkeep = meta.Rout(keep);
    maxFixed = floor((min(Rkeep)*100)/0.1)*0.1;  % cm，向下取整至 0.1 cm
    rFixedCm = 0:0.1:maxFixed;
    rFixed = rFixedCm/100;
    Cfixed = zeros(sum(keep),numel(rFixed));
    Csurface = Cout(keep,end);
    row = 0;
    for i = find(keep)'
        row = row+1;
        ri = meta.Rout(i)*linspace(0,1,cfg.N+1)';
        Cfixed(row,:) = interp1(ri,Cout(i,:),rFixed,'pchip');
    end
    header = [{'时间\到药材中心的距离'}, num2cell(rFixedCm), {'药材表面'}];
    writecell(header,output,'Sheet','Sheet1','Range','A1');
    writematrix([t,Cfixed,Csurface],output,'Sheet','Sheet1','Range','A2');
    write_q4_radius_history(resultDir,t, Rkeep);
end
end

function write_q3_summary(resultDir,t,C,r)
idx = find(t > 0 & mod(t,6*3600) == 0);
if isempty(idx), return; end
pick = [0,0.005,0.010,0.015,0.020];
M = zeros(numel(idx),numel(pick));
for j = 1:numel(idx)
    M(j,:) = interp1(r,C(idx(j),:),pick,'pchip');
end
filename = fullfile(resultDir,'q3_每6小时含水率汇总.xlsx');
writecell([{'时间(s)'},num2cell(pick*100)],filename,'Sheet','Sheet1','Range','A1');
writematrix([t(idx),M],filename,'Sheet','Sheet1','Range','A2');
end

function write_q4_radius_history(resultDir,t,R)
filename = fullfile(resultDir,'q4_半径历史.xlsx');
writecell({'时间(s)','半径(cm)'},filename,'Sheet','Sheet1','Range','A1');
writematrix([t,R*100],filename,'Sheet','Sheet1','Range','A2');
end

function make_plots(cfg,root,t,T,C,meta)
resultDir = fullfile(root,'result');
if ~exist(resultDir,'dir'), mkdir(resultDir); end
if cfg.id <= 3
    rcm = meta.r*100;
    selected = nearest_indices(t,cfg.figureTimes);
    selected = unique(selected);
    f = figure('Visible','off','Color','w','Position',[100 100 1040 420]);
    subplot(1,2,1); hold on; grid on; box on;
    for j=1:numel(selected)
        plot(rcm,T(selected(j),:),'LineWidth',1.4,'DisplayName',sprintf('t=%.1f h',t(selected(j))/3600));
    end
    xlabel('距中心距离 / cm'); ylabel('温度 / ℃'); title(sprintf('第%d问径向温度分布',cfg.id)); legend('Location','best');
    subplot(1,2,2); hold on; grid on; box on;
    for j=1:numel(selected)
        plot(rcm,C(selected(j),:),'LineWidth',1.4,'DisplayName',sprintf('t=%.1f h',t(selected(j))/3600));
    end
    xlabel('距中心距离 / cm'); ylabel('干基含水率 / kg·kg^{-1}'); title(sprintf('第%d问径向含水率分布',cfg.id)); legend('Location','best');
    save_png(f,fullfile(resultDir,sprintf('q%d_径向剖面.png',cfg.id)));

    f = figure('Visible','off','Color','w','Position',[100 100 900 420]);
    yyaxis left; plot(t/3600,T(:,1),'r-','LineWidth',1.5); hold on; plot(t/3600,T(:,end),'r--','LineWidth',1.5);
    ylabel('温度 / ℃');
    yyaxis right; plot(t/3600,C(:,1),'b-','LineWidth',1.5); hold on; plot(t/3600,C(:,end),'b--','LineWidth',1.5);
    ylabel('干基含水率 / kg·kg^{-1}'); grid on; box on;
    xlabel('时间 / h'); title(sprintf('第%d问中心与表面状态演化',cfg.id));
    legend('中心温度','表面温度','中心含水率','表面含水率','Location','best');
    save_png(f,fullfile(resultDir,sprintf('q%d_中心表面演化.png',cfg.id)));
else
    x = meta.x;
    selected = nearest_indices(t,cfg.figureTimes);
    selected = unique(selected);
    f = figure('Visible','off','Color','w','Position',[100 100 1040 420]);
    subplot(1,2,1); hold on; grid on; box on;
    for j=1:numel(selected)
        plot(x,C(selected(j),:),'LineWidth',1.4,'DisplayName',sprintf('t=%.1f h',t(selected(j))/3600));
    end
    xlabel('归一化半径 x=r/R(t)'); ylabel('干基含水率 / kg·kg^{-1}'); title('第4问：收缩坐标下的含水率分布'); legend('Location','best');
    subplot(1,2,2); plot(t/3600,meta.Rout*100,'k-','LineWidth',1.8); grid on; box on;
    xlabel('时间 / h'); ylabel('半径 / cm'); title('第4问：药材半径收缩过程');
    save_png(f,fullfile(resultDir,'q4_含水率与半径.png'));

    f = figure('Visible','off','Color','w','Position',[100 100 900 420]);
    plot(t/3600,C(:,1),'b-','LineWidth',1.5); hold on; plot(t/3600,C(:,end),'b--','LineWidth',1.5);
    grid on; box on; xlabel('时间 / h'); ylabel('干基含水率 / kg·kg^{-1}');
    title('第4问：中心与实际表面含水率'); legend('中心','实际表面','Location','best');
    save_png(f,fullfile(resultDir,'q4_中心表面含水率.png'));
end
end

function idx = nearest_indices(t,target)
idx = zeros(size(target));
for i=1:numel(target)
    [~,idx(i)] = min(abs(t-target(i)));
end
end

function save_png(fig,filename)
set(fig,'PaperPositionMode','auto');
print(fig,filename,'-dpng','-r300');
close(fig);
end
