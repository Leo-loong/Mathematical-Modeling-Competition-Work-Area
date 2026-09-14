function paths = paperfig_export(hfig, name, outDir)
%PAPERFIG_EXPORT 双路线导出: MATLAB原生留档 + 透明矢量(LaTeX直接可用)
%   paths = paperfig_export(hfig, 'fig2_spectrum', outDir)
%   产物: name.fig(MATLAB原生,核验/再编辑) + name.png(300dpi预览)
%         name.pdf(透明矢量,LaTeX includegraphics首选) + name.svg(备选矢量)
%   注意: exportgraphics 需 R2020a+; SVG 由 print -dsvg 生成(背景为白)
if nargin < 3, outDir = pwd; end
if ~exist(outDir, 'dir'), mkdir(outDir); end
paths = struct();
% 1) MATLAB 原生留档 (保存全部句柄/数据, 供后续核验与再编辑)
savefig(hfig, fullfile(outDir, [name '.fig']));
paths.fig = fullfile(outDir, [name '.fig']);
% 2) PNG 位图预览 (300 dpi, 透明背景)
exportgraphics(hfig, fullfile(outDir, [name '.png']), ...
    'Resolution', 300, 'BackgroundColor', 'none');
paths.png = fullfile(outDir, [name '.png']);
% 3) PDF 矢量 (矢量 ContentType; 矢量导出不支持透明, 用白底——LaTeX 白纸无缝)
exportgraphics(hfig, fullfile(outDir, [name '.pdf']), ...
    'ContentType', 'vector', 'BackgroundColor', 'white');
paths.pdf = fullfile(outDir, [name '.pdf']);
% 4) SVG 矢量备选
print(hfig, fullfile(outDir, [name '.svg']), '-dsvg', '-vector');
paths.svg = fullfile(outDir, [name '.svg']);
fprintf('EXPORTED %s -> fig/png/pdf/svg\n', name);
end
