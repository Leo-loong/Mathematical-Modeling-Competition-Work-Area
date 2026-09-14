function p = drude_params(material, override)
%% DRUDE_PARAMS — v2.0 固定文献 Drude 参数（DI-1：零自由参数，禁止与 d 联合拟合）
% p = drude_params('SiC') / ('Si')；override 可覆盖单字段（敏感性扫描用，须在记录中留痕）
%
% 换算式（成文可审计）：
%   等离子体波数 σp = ωp/(2πc)，ωp² = N·e²/(ε₀·m*)
%   => σp[cm⁻¹] = 299.5 · sqrt( (N/10¹⁸cm⁻³) · (m₀/m*) )
%      (常数: e=1.602e-19 C, ε₀=8.854e-12 F/m, c=2.998e10 cm/s, m₀=9.109e-31 kg)
%   阻尼 γ = 1/(2πc·τ)，τ = μ·m*/e （μ=迁移率）
%   等离子体边缘 σ_edge = σp/√ε∞ （|r₁₂|→1 金属性起点）
%
% W-1 注意事项（T1.9）：边缘必须落在条纹带外，否则低波数段 |r₁₂|→1 金属性，
%   条纹带内出现非条纹结构——选择规则：baseline 取边缘在带外的最低合理掺杂档，
%   其余档位进敏感性扫描（00 总纲风险预案：扫描替代单值，不拟合）。

switch upper(material)
    case 'SIC'
        % 外延 4H-SiC，条纹带 1100~4000 cm⁻¹（实验包-1 P1b）
        p.matname   = 'SiC';
        p.n1        = 2.55;      % 外延层（S06, EXP-2 定稿）
        p.epsinf    = 6.52;      % S06 (⊥c, Goldberg 2001)
        p.mstar     = 0.35;      % 4H-SiC 电子电导有效质量 (文献区间 0.29~0.42, 取中值)
        % 掺杂档 → σp（换算式见上）；GB/T 42905: 衬底 N > 1e18 cm⁻³
        % baseline 修正（W-2, 2026-09-09）：由实测条纹幅度反演——
        %   |r12|(σ) = 条纹幅度 / (2|r01|(1-r01²))：1100→~0.030, 2500→~0.009, 4000→~0.0023
        %   严格符合 Drude |r12|∝σp²/σ² 衰减 → 反推 σp≈700 cm⁻¹ (N≈1.9e18, m*=0.35)。
        %   注意：EXP-4 的 ρ12=0.165 与 amp=2.6 为简并参数积（记录_EXP-4），T1.6 灰区预判
        %   误将该积当纯 ρ12 —— 修正后 q≈0.004，落在"可忽略"档；EXP-7 数据仲裁最终裁定。
        p.sigma_p   = 700;       % baseline: N≈1.9e18 cm⁻³（幅度反演）; 边缘 275 cm⁻¹ 远离条纹带
        p.gamma     = 300;       % baseline: μ=100 cm²/Vs → τ=2.0e-14 s → γ=267；取整 300
        p.band      = [1100 4000];
        p.scan_sigma_p = [500 700 1100 1600 3100 4600 6000 8000 12000];  % 含幅度反演值/EXP-4 区间/高掺杂外延
        p.scan_gamma   = [100 300 900];              % μ≈900/100/30 cm²/Vs
        p.scan_sigma_p_notes = {'N=2.8e18','幅度反演 baseline N≈1.9e18','N=1.1e19','N=1e19+EXP4下缘','EXP-4 拟合区间上缘'};
        p.edge = p.sigma_p/sqrt(p.epsinf);           % baseline 边缘 ≈274 cm⁻¹ < 1100 → 带外
    case 'SI'
        % 外延 Si（高阻）/ 重掺 Si 衬底；条纹带待第3块 P1 确认（预期 ≥1400 cm⁻¹）
        p.matname   = 'Si';
        p.n1        = 3.42;      % Si 红外折射率（00 总纲锁定值）
        p.epsinf    = 11.7;      % Si 高频介电常数（教科书值）
        p.mstar     = 0.26;      % Si 电子电导有效质量（教科书值）
        % 典型重掺 Si 衬底 N≈1e19 cm⁻³（As/P, 0.005~0.02 Ω·cm）
        p.sigma_p   = 1859;      % baseline: N=1e19 → 299.5·sqrt(10/0.26)
        p.gamma     = 360;       % baseline: μ=100 cm²/Vs → γ=360
        p.band      = [1400 4000];  % 预期条纹带（第3块 P1 实测确认）
        p.scan_sigma_p = [1859 4157 5874];           % N=1e19/5e19/1e20
        p.scan_gamma   = [150 360 900];
        p.scan_sigma_p_notes = {'N=1e19 baseline','N=5e19','N=1e20'};
        p.edge = p.sigma_p/sqrt(p.epsinf);           % baseline 边缘 ≈543 cm⁻¹ < 1400 → 带外
    otherwise
        error('drude_params: unknown material %s', material);
end

% override 敏感性覆盖
if nargin > 1
    f = fieldnames(override);
    for i = 1:numel(f)
        p.(f{i}) = override.(f{i});
    end
    p.edge = p.sigma_p/sqrt(p.epsinf);   % 覆盖后重算边缘
end

% 选择规则复核（T1.9 W-1 注意事项）
if p.edge >= p.band(1)
    warning('drude_params: 等离子体边缘 %.0f cm⁻¹ 落入条纹带 [%.0f,%.0f]（材料 %s）— 低波数段 |r12|→1 金属性, 需显式建模或换档', ...
        p.edge, p.band(1), p.band(2), p.matname);
end
end
