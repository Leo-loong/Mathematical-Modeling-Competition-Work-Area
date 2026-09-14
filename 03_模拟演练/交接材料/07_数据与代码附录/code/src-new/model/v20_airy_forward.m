function [R, aux] = v20_airy_forward(sig, d, angle, p, opt)
%% V20_AIRY_FORWARD — v2.0 M-A 解析 Airy 三介质正演模型（实验包-2 W-1）
% R(σ) = | r01 + (1-r01²)·r12·e^{iΔ} / (1 + r01·r12·e^{iΔ}) |²    （记录_T1_推导.md T1.3）
% 输入:
%   sig   — 波数向量 (cm⁻¹, 列向量)
%   d     — 外延层厚度 (μm)
%   angle — 入射角 (deg)
%   p     — drude_params(material) 结构
%   opt   — 退化开关（W-1 退化测试与 EXP-7 2×2 对照用）:
%           opt.airy  (true=完整 Airy 级数 | false=双光束一阶截断)      默认 true
%           opt.drude (true=固定 Drude 复 r12 | false=常数 r12)         默认 true
%           opt.r12const — drude=false 时的常数 r12 (复标量)，如 0.204·e^{-i0.28π}
% 输出:
%   R   — 反射率 (0~1, 列向量)
%   aux — 诊断: r12, r01, cos_t, Delta
% 退化一致性（T1.4）: airy=false & drude=false 且 opt.r12const=ρ12·e^{iφ12} 时，
%   R ≡ r01² + ρ̂² + 2·r01·ρ̂·cos(Δ+φ12)，ρ̂=(1-r01²)·|r12| —— 与 v1.5 双光束式逐项相等。

if nargin < 5, opt = struct(); end
if ~isfield(opt,'airy'),  opt.airy  = true;  end
if ~isfield(opt,'drude'), opt.drude = true;  end

sig = sig(:);
theta = angle*pi/180;
cos_t = sqrt(1 - sin(theta)^2/p.n1^2);        % 层内 cosθ₁
% r01: s 偏振标量（审核定稿 T1.2 修正式）
r01 = (cos(theta) - p.n1*cos_t)/(cos(theta) + p.n1*cos_t);

% 衬底界面 r12(σ): 固定 Drude（DI-1）或常数
if opt.drude
    N2 = drude_N2(sig, p.sigma_p, p.gamma, p.epsinf);
    sin2 = sin(theta)./N2;
    cos2 = sqrt(1 - sin2.^2);
    r12 = (p.n1*cos_t - N2.*cos2)./(p.n1*cos_t + N2.*cos2);
else
    if ~isfield(opt,'r12const')
        error('v20_airy_forward: drude=false 需提供 opt.r12const');
    end
    r12 = opt.r12const * ones(size(sig));
end

Delta = 4*pi*sig*(d*1e-4)*p.n1*cos_t;         % 往返相位

if opt.airy
    Er = r01 + (1-r01^2).*r12.*exp(1i*Delta) ./ (1 + r01.*r12.*exp(1i*Delta));
else
    Er = r01 + (1-r01^2).*r12.*exp(1i*Delta); % 一阶截断 = 双光束（v1.5 对应式, T1.4）
end
R = abs(Er).^2;

aux.r01 = r01; aux.r12 = r12; aux.cos_t = cos_t; aux.Delta = Delta;
end

function N2 = drude_N2(sig, sigma_p, gamma, epsinf)
% 固定 Drude 介电函数: ε(σ) = ε∞ − σp²/(σ(σ+iγ)), σ/σp/γ 同为 cm⁻¹
epsc = epsinf - sigma_p^2./(sig.*(sig + 1i*gamma));
N2 = sqrt(epsc);
end
