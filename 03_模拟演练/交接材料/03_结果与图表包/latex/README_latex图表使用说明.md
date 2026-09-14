# LaTeX 图表模板（可选礼品 + 复核参照）

> **定位（2026-09-09 图表交接再设计后）**：图表渲染由写作者负责（风格归写作者）。本文件夹与 `figures/` 基准图均为**可选参照**：
> - `data/*.csv` 才是交付主体（写作者自绘的唯一数据依据）；
> - `figures/` 基准图用于与写作者成品做比对复核（规程见 03-4 §二）；
> - 本 LaTeX 模板：写作者若用 pgfplots 可直接取用，不用无妨。

## 一、原双路线体系（保留供参考）

| 路线 | 产物 | 位置 | 用途 |
|---|---|---|---|
| **MATLAB 基准** | `.fig`（原生留档核验）+ `.png`（预览）+ `.pdf`/`.svg`（矢量） | `figures/` | 复核基准 + 快速嵌入 `\includegraphics` |
| **LaTeX 模板** | `latex/*.tex`（pgfplots 源码）+ `data/*.csv`（图数据） | 本文件夹 | 与正文字体/版式无缝一致，风格统一 |

两条路线**共用同一份数据**（`data/*.csv` 由 `src/figures/make_paper_figures.m` 从与管线同源的计算中导出），保证数字口径唯一。

## 二、LaTeX 路线使用步骤

1. 导言区：
   ```latex
   \usepackage{pgfplots}
   \pgfplotsset{compat=1.17}
   \input{latex/pgfplots_style.tex}   % 或复制内容到导言区
   ```
2. 正文需要插图处 `\input{latex/fig2_spectrum.tex}` 等；
3. 编译：**xelatex**（含中文；`latex/` 内模板的相对路径基于 `交接材料/03_结果与图表包/`，主 tex 若在别处请调整 `\def` 路径或用 `--output-directory` 组织）；
4. 数据与图同步：CSV 更新后 LaTeX 重编译即自动更新，**不需要改模板**。

## 三、各图文件对应

| 模板 | 数据 | 内容 |
|---|---|---|
| `fig2_spectrum.tex` | `data/fig2_data.csv` | 实测谱 + poly7 背景 + 条纹区下界 |
| `fig3_fitresidual.tex` | `data/fig3_data.csv` | 联合拟合（上）+ 残差（下）groupplot |
| `fig4_crosscomparison.tex` | `data/fig4_data.csv` | 多算法交叉误差棒 + 系统区间带 [8.0, 8.9] μm |

## 四、风格一致性守则（修改图表必须遵守）

1. 尺寸/字号/线宽只改 `pgfplots_style.tex` 一处（对应 MATLAB 侧 `paperfig_style.m`）；
2. 配色固定四色（黑/蓝/橙/灰），黑白打印靠线型+标记区分；
3. 误差棒只允许用 03-1 数值口径总表登记的值；
4. 修改后 MATLAB 路线与 LaTeX 路线必须重新对表核对（同一数据源天然一致，防手滑）。

## 五、遗留事项（挂起，见 03-4 §状态）

- 图5（合成闭环/bootstrap 分布）：待管线落盘 `V4_results.mat` 后扩展；
- MATLAB 导出的"背景透明度不支持"警告需核验 PNG/PDF 实际底色（白/黑），必要时统一白底；
- `make_paper_figures.m` 中图4 数据写出（addprop）改由"权威源复制"替代——已用 `data/fig4_data.csv` 落地，脚本内该段待清理。
