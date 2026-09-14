function paperfig_style(hfig)
%PAPERFIG_STYLE 统一论文图风格(双路线共用): 字体/线宽/边框/刻度/配色
%   paperfig_style(hfig)  在绘图完成后、导出前调用
% 全局编码纪律: 本文件已自审; 修改后需 checkcode + 小样本干跑
if isempty(hfig) || ~ishandle(hfig), return; end
set(hfig, 'Color', 'w', 'Position', [100 100 900 620]);   % 白底(论文标准; 透明在矢量/位图导出会回退黑底)
ax = findall(hfig, 'Type', 'axes');
set(ax, 'FontName', 'Arial', 'FontSize', 10, 'LineWidth', 0.8, ...
    'TickDir', 'out', 'Box', 'on', 'XMinorTick', 'on', 'YMinorTick', 'on');
lg = findall(hfig, 'Type', 'legend');
set(lg, 'FontName', 'Arial', 'FontSize', 9);
set(findall(hfig, '-property', 'LineWidth'), 'LineWidth', 1.2);
% 固定配色(黑白打印可辨: 线型/标记区分, 颜色仅辅助)
c = struct('c1', [0 0 0], 'c2', [0 0.447 0.741], 'c3', [0.851 0.325 0.098], ...
    'g1', [0.30 0.30 0.30], 'g2', [0.60 0.60 0.60], 'band', [0.85 0.85 0.85]);
setappdata(hfig, 'paperfig_colors', c);
end
