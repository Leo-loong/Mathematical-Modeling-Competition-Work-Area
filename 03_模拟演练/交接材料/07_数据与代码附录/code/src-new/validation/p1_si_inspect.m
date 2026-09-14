function p1_si_inspect()
%% P1_SI_INSPECT — 第3块块首：Si 数据（附件3/4）体检（00 总纲风险预案：异常即停止上报）
% 输入 : 附件/附件3.xlsx (10°), 附件/附件4.xlsx (15°)
% 输出 : 实验包-2/work/out/P1_Si报告.txt (UTF-8), P1_Si_overview.png
% Run  : matlab -batch "addpath('src-new/validation'); p1_si_inspect"
% 对应 : 实验包-2/03_第3块 P1

outDir = fullfile('模型设计','实验包-2','work','out');
if ~exist(outDir,'dir'), mkdir(outDir); end
fid = fopen(fullfile(outDir,'P1_Si报告.txt'),'w','n','UTF-8');
fprintf(fid,'P1 Si 数据体检报告（附件3/4）  %s\n==================================================\n\n', ...
    char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')));

files  = {fullfile('附件','附件3.xlsx'), fullfile('附件','附件4.xlsx')};
angles = [10 15];
data   = cell(1,2);

for k = 1:2
    raw = readmatrix(files{k});
    D = raw(:,1); R = raw(:,2);
    dS = diff(D);
    fprintf(fid,'附件%d (Si, %.0f°)\n--------------------------------------------------\n', k+2, angles(k));
    fprintf(fid,'[波数轴] 点数 %d, 范围 %.2f~%.2f cm⁻¹; 单调递增 %d; 间隔中位 %.4f (CV %.4f)\n', ...
        numel(D), min(D), max(D), all(dS>0), median(dS), std(dS)/median(dS));
    fprintf(fid,'  NaN: 波数 %d / 反射率 %d; 重复点 %d\n', sum(isnan(D)), sum(isnan(R)), sum(dS==0));
    fprintf(fid,'[反射率] 范围 %.3f~%.3f %%; 均值 %.3f %%\n', min(R), max(R), mean(R));
    d2 = [0; diff(diff(R)); 0];
    z = (d2 - median(d2))/(1.4826*mad(d2,1)+eps);
    fprintf(fid,'  尖峰候选(|二阶差分|robust-z>8): %d 处; 负值 %d; >100%% %d\n', ...
        sum(abs(z)>8), sum(R<0), sum(R>100));
    % 条纹区识别: Si 谱的显著极值跨度（去除 <500 的源/边缘伪迹与谱端效应）
    % 判据: 极值相对滚动中位的幅度 > 4×robust噪声; 下限 500 cm⁻¹ (Si 剩余射线带/等离子体反射区)
    bg = movmedian(R, 401);
    sigL = 1.4826*mad(diff(R),1)/sqrt(2);
    [~, iex] = local_ext(R, 'both', 15);
    sigExt = abs(R(iex) - bg(iex)) > 4*sigL & D(iex) >= 500;
    iex = iex(sigExt);
    frLo = D(iex(1)); frHi = D(iex(end));
    fprintf(fid,'[条纹区识别] 显著极值跨度: %.1f ~ %.1f cm⁻¹ (%d 个显著极值, 噪声阈 4σ)\n', ...
        frLo, frHi, numel(iex));
    in = D >= frLo & D <= frHi;
    Df = D(in); Rf = R(in);
    [pmx, imx] = local_ext(Rf, 'max', 5);
    [pmn, imn] = local_ext(Rf, 'min', 5);
    fprintf(fid,'[条纹观察] 区内极大 %d / 极小 %d\n', numel(imx), numel(imn));
    if numel(imx) >= 2
        pper = diff(Df(imx));
        fprintf(fid,'  条纹周期(极大间距): 中位 %.2f, 范围 %.2f~%.2f cm⁻¹\n', median(pper), min(pper), max(pper));
        % Si 厚度粗估 (n=3.42)
        nref = 3.42; th = angles(k)*pi/180; ct = cos(asin(sin(th)/nref));
        p_est = 1/median(pper);   % OPD cm
        d_est = p_est/(2*nref*ct)*1e4;
        fprintf(fid,'  粗估厚度(以条纹周期中位): %.2f um (n=3.42)\n', d_est);
        % FFT 粗估
        F0 = detrend(Rf - movmedian(Rf,201)); Nf = numel(F0);
        Y = abs(fft(F0.*hann_win(Nf), Nf*8)); Yh = Y(1:floor(Nf/2));
        fs = 1/median(diff(Df)); fh = (0:numel(Yh)-1)'/(numel(Y))*fs;
        [~,ip] = max(Yh);
        fprintf(fid,'  FFT 主频 %.6f cyc/cm⁻¹ -> d ≈ %.2f um\n', fh(ip), fh(ip)/(2*nref*ct)*1e4);
        % 可见度
        fprintf(fid,'  可见度素材: 极大中位 %.3f%%, 极小中位 %.3f%%\n', median(pmx), median(pmn));
    end
    sigN = 1.4826*mad(diff(Rf),1)/sqrt(2);
    fprintf(fid,'[噪声粗估] 区内相邻差分 robust σ = %.4f %%\n\n', sigN);
    data{k} = [D R];
end
fclose(fid);

fig = figure('Position',[60 60 1200 700],'Visible','off');
for k = 1:2
    subplot(2,1,k); D = data{k}(:,1); R = data{k}(:,2);
    plot(D,R,'b-'); grid on;
    xlabel('Wavenumber (cm^{-1})'); ylabel('Reflectance (%)');
    title(sprintf('Attachment %d (%d deg) — Si full spectrum', k, angles(k)));
end
saveas(fig, fullfile(outDir,'P1_Si_overview.png'));
disp('P1SI_DONE');
end

function [vals, idx] = local_ext(x, type, wmin)
n = numel(x); idx = []; i = 2;
while i <= n-1
    if strcmp(type,'both')
        isExt = (x(i)>=x(i-1) && x(i)>=x(i+1)) || (x(i)<=x(i-1) && x(i)<=x(i+1));
    elseif strcmp(type,'max'), isExt = x(i)>=x(i-1) && x(i)>=x(i+1);
    else,                      isExt = x(i)<=x(i-1) && x(i)<=x(i+1);
    end
    if isExt
        j = i;
        while j < n && x(j+1)==x(j), j = j+1; end
        ci = floor((i+j)/2);
        if ci>wmin && ci<=n-wmin
            left = x(ci-wmin:ci-1); right = x(ci+1:ci+wmin);
            if strcmp(type,'max')
                ok = all(left<=x(ci)) && all(right<=x(ci));
            else
                ok = all(left>=x(ci)) && all(right>=x(ci));
            end
            if ok, idx(end+1) = ci; end %#ok<AGROW>
        end
        i = j + 1;
    else
        i = i + 1;
    end
end
vals = x(idx);
end

function w = hann_win(N)
w = 0.5*(1 - cos(2*pi*(0:N-1)'/(N-1)));
end
