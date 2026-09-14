function R = v20_tmm(sig, d, angle, p)
%% V20_TMM — M-B 传输矩阵法校验器（特征矩阵法，与 M-A 逐束求和互相独立）
% 单层(外延层) + 半空间衬底; 标量 s 偏振导纳口径（与审核定稿 T1.2 一致）。
% 特征矩阵: M = [cosδ, i·sinδ/Y1 ; i·Y1·sinδ, cosδ],  δ = 2π·σ·d·cosθ1 (单程相位)
% 输入导纳 Y = (M21 + M22·Y2)/(M11 + M12·Y2);  R = |(Y0 − Y)/(Y0 + Y)|²
% 校验目标: 与 v20_airy_forward（M-A）的 R(σ) 逐点相对偏差 < 0.1%（W-2 验收）。

sig = sig(:);
theta = angle*pi/180;
Y0 = cos(theta);                                    % 空气导纳 (n0=1)
cos1 = sqrt(1 - sin(theta)^2/p.n1^2);
Y1 = p.n1*cos1;                                     % 外延层导纳
N2 = drude_N2(sig, p.sigma_p, p.gamma, p.epsinf);
cos2 = sqrt(1 - (sin(theta)./N2).^2);
Y2 = N2.*cos2;                                      % 衬底导纳 (复)

delta = 2*pi*sig*(d*1e-4)*p.n1*cos1;                % 单程相位 (rad): 2π·σ·n1·d·cosθ1
% 时间约定 e^{+iωt}（与 M-A 的 e^{+iΔ} 传播因子一致）→ 特征矩阵取共轭形式:
M11 = cos(delta); M12 = -1i*sin(delta)./Y1;
M21 = -1i*Y1*sin(delta); M22 = M11;

Yin = (M21 + M22.*Y2)./(M11 + M12.*Y2);
R = abs((Y0 - Yin)./(Y0 + Yin)).^2;
end

function N2 = drude_N2(sig, sigma_p, gamma, epsinf)
epsc = epsinf - sigma_p^2./(sig.*(sig + 1i*gamma));
N2 = sqrt(epsc);
end
