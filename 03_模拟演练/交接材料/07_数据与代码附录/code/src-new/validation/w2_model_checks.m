function w2_model_checks()
%% W2_MODEL_CHECKS — 第2块验收：退化测试（W-1）+ TMM 交叉校验（W-2）+ Drude 带外边缘复核
% 输入 : 无（确定性计算）
% 输出 : 实验包-2/work/out/W2_report.txt (UTF-8), W2_checks.png
% Run  : matlab -batch "addpath('src-new/model'); addpath('src-new/validation'); w2_model_checks"
% 对应 : 实验包-2/02_第2块_v2.0模型块.md 验收门; 00 总纲第2块验收门

outDir = fullfile('模型设计','实验包-2','work','out');
if ~exist(outDir,'dir'), mkdir(outDir); end
fid = fopen(fullfile(outDir,'W2_report.txt'),'w','n','UTF-8');
fprintf(fid,'W-1/W-2 模型校验报告  %s\n==================================================\n\n', ...
    char(datetime('now','Format','yyyy-MM-dd HH:mm:ss')));

sig = (1100:0.482:4000)';          % SiC 条纹带（与实测轴同栅格）
angle = 10;
d = 8.026;                          % v1.5 交付值（口径统一的代表厚度）

%% ---------- 1) Drude 带外边缘复核（T1.9 W-1 注意事项） ----------
fprintf(fid,'[1] Drude 等离子体边缘复核（选择规则：边缘 < 条纹带下界）\n');
for mat = {'SiC','Si'}
    p = drude_params(mat{1});
    fprintf(fid,'  %s: σp=%.0f, γ=%.0f, ε∞=%.2f -> 边缘 %.0f cm⁻¹ vs 条纹带 [%.0f,%.0f] -> %s\n', ...
        p.matname, p.sigma_p, p.gamma, p.epsinf, p.edge, p.band(1), p.band(2), ...
        ternary(p.edge < p.band(1),'带外 OK','带内 !!'));
end
fprintf(fid,'  敏感性扫描档位: σp ∈ [%s]; γ ∈ [%s]（不拟合, 仅扫描）\n\n', ...
    num2str(p.scan_sigma_p,'%g '), num2str(p.scan_gamma,'%g '));

%% ---------- 2) 退化测试（W-1）：v2.0 ⊃ v1.5 ----------
fprintf(fid,'[2] 退化测试：Airy关(双光束) + Drude关(常数r12) → 必须逐点回到 v1.5 双光束式\n');
pC = drude_params('SiC');
rho12 = 0.204; phi12 = -0.28*pi;    % 由 v1.5 拟合换算（T1.4: |r12|=ρ̂/(1-r01²)）
opt2 = struct('airy',false,'drude',false,'r12const',rho12*exp(1i*phi12));
R_deg = v20_airy_forward(sig, d, angle, pC, opt2);
% v1.5 闭式（01号文档 S-5.3）: R = r01² + ρ̂² + 2·r01·ρ̂·cos(Δ+φ12), ρ̂=(1-r01²)ρ12
cost1 = sqrt(1 - sind(angle)^2/pC.n1^2);
r01 = (cosd(angle) - pC.n1*cost1)/(cosd(angle) + pC.n1*cost1);
rho_hat = (1-r01^2)*rho12;
Delta = 4*pi*sig*(d*1e-4)*pC.n1*cost1;
R_v15 = r01^2 + rho_hat^2 + 2*r01*rho_hat*cos(Delta + phi12);
maxDev = max(abs(R_deg - R_v15));
relDev = maxDev/max(R_v15);
fprintf(fid,'  max|R_deg − R_v15| = %.3e (相对 %.3e) -> %s\n', maxDev, relDev, ...
    ternary(relDev < 1e-12,'PASS（机器精度）','FAIL'));
fprintf(fid,'  r01=%.4f, ρ̂=(1-r01²)ρ12=%.4f\n\n', r01, rho_hat);

%% ---------- 3) TMM 交叉校验（W-2）：三组参数, <0.1% ----------
fprintf(fid,'[3] TMM（M-B 特征矩阵法） vs Airy（M-A 逐束求和）: 相对偏差 < 0.1%%\n');
cases = { ...
    struct('mat','SiC','d',8.026,'angle',10), ...
    struct('mat','Si','d',12.0,'angle',10), ...
    struct('mat','Si','d',3.5,'angle',15)};
for c = 1:numel(cases)
    cs = cases{c};
    pm = drude_params(cs.mat);
    Ra = v20_airy_forward(sig, cs.d, cs.angle, pm, struct());
    Rb = v20_tmm(sig, cs.d, cs.angle, pm);
    rel = max(abs(Ra-Rb)./max(Rb, 1e-12));
    fprintf(fid,'  组%d (%s, d=%.3f um, %d°): max rel-dev = %.3e -> %s\n', ...
        c, pm.matname, cs.d, cs.angle, rel, ternary(rel < 1e-3,'PASS','FAIL'));
end
% 注: 退化态（常数 r12）无法用特征矩阵 TMM 独立表达（TMM 需真实层参数）,
% 退化态的独立校验由第 2 节承担: R_deg vs v1.5 闭式（docs/01 文档式）逐点机器精度一致。

%% ---------- 4) Airy vs 双光束 差异量级（q 证据, 供 EXP-6/8 预览） ----------
fprintf(fid,'\n[4] 完整 Airy vs 双光束 的谱差异量级（q 证据）\n');
for mat = {'SiC','Si'}
    pm = drude_params(mat{1});
    Ra = v20_airy_forward(sig, d, angle, pm, struct());
    Rd = v20_airy_forward(sig, d, angle, pm, struct('airy',false));
    r01m = abs((cosd(angle) - pm.n1*sqrt(1-sind(angle)^2/pm.n1^2))/(cosd(angle) + pm.n1*sqrt(1-sind(angle)^2/pm.n1^2)));
    r12m = mean(abs(aux_get_r12(sig, angle, pm)));
    fprintf(fid,'  %s: |r01|=%.3f, <|r12|>=%.3f, q≈%.3f; max|R_A−R_D|=%.4f (相对 %.2f%%)\n', ...
        pm.matname, r01m, r12m, r01m*r12m, max(abs(Ra-Rd)), 100*max(abs(Ra-Rd))/max(Ra));
end
fclose(fid);

%% ---------- 图 ----------
pC2 = drude_params('SiC');
Ra = v20_airy_forward(sig, d, angle, pC2, struct());
Rd = v20_airy_forward(sig, d, angle, pC2, struct('airy',false));
Rt = v20_tmm(sig, d, angle, pC2);
fig = figure('Position',[60 60 1400 600],'Visible','off');
subplot(1,2,1);
plot(sig, Ra,'b', sig, Rd,'r--'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('R'); legend('Airy (v2.0)','Dual-beam','Location','best');
title('SiC: v2.0 vs v1.5 forward (d=8.026 \mum)');
subplot(1,2,2);
plot(sig, Ra-Rt,'k.'); grid on;
xlabel('Wavenumber (cm^{-1})'); ylabel('R_{Airy} - R_{TMM}');
title('W-2: Airy vs TMM residual');
saveas(fig, fullfile(outDir,'W2_checks.png'));
disp('W2_DONE');
end

function s = ternary(tf, a, b)
if tf, s = a; else, s = b; end
end

function r12 = aux_get_r12(sig, angle, p)
theta = angle*pi/180;
cos_t = sqrt(1 - sin(theta)^2/p.n1^2);
N2 = p.epsinf - p.sigma_p^2./(sig.*(sig + 1i*p.gamma)); N2 = sqrt(N2);
cos2 = sqrt(1 - (sin(theta)./N2).^2);
r12 = (p.n1*cos_t - N2.*cos2)./(p.n1*cos_t + N2.*cos2);
end

% （占位结束：退化态不适用 TMM，见第 3 节注释）
