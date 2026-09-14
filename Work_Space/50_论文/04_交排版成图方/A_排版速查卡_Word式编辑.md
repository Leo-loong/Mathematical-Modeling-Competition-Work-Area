# A 排版速查卡（**像用 Word 一样改这份 LaTeX**）

> **适用**：`50_论文/04_交排版成图方/交付排版方论文/`（本机已装 TeX Live 2026，含 `xelatex`／`latexmk`／`texworks`）
> **一句话**：源码在左、PDF 在右，**保存即重编译**（1–3 秒），点 PDF 能跳回源码 —— 这就是这份论文能做到的"Word 体验"。

---

## 一、先做一次（一次性配置）

| 方式 | 怎么做 | 体验 |
|---|---|---|
| **A（最省事，已配置好）** | 双击交付目录里的 **`编译预览.bat`**（窗口留着）；再用任意编辑器改 `main.tex`／`sections\*.tex` 并保存 | **保存即自动重编译**，1–3 秒后 PDF 更新 |
| **B（推荐给长期编辑）** | 装了 VS Code：`code --install-extension James-Yu.latex-workshop`，打开交付目录，点左侧 TeX 图标 → Build | 保存即编译 ＋ 内嵌 PDF ＋ 点击跳源码 |
| **C（TeX Live 自带，已装）** | 运行 `C:\texlive\2026\bin\windows\texworks.exe`，打开 `main.tex`（魔术注释已写，会自动用 **XeLaTeX**），按 ▶ | 左源码／右 PDF，**Ctrl+点击 PDF 跳源码**；内嵌预览**不锁文件**，最稳 |
| 只需编译一次 | 双击 **`编译一次.bat`**（等价于 `xelatex main.tex` 跑两遍） | 出 `main.pdf` |

> ⚠ **不要用 WPS／Acrobat 一直开着 `main.pdf`** —— 它们会**锁住文件**导致编译失败（这正是此前"编译卡住"的根因）。要看 PDF 请用 **TeXworks 内嵌预览**，或看完就关。

---

## 二、Word 操作 ↔ 这里怎么改（**只改"数字与参数"，不动宏** ⟹ 版式不会崩）

| 你想做的（Word 里） | 在 tex 里改什么 | 注意 |
|---|---|---|
| 改文字 | 直接在 `sections/01…10_*.tex` 里改中文；改完保存 | 数值**不要动**（本论文数值口径已锁定） |
| 改图大小 | `\includegraphics[width=0.66\linewidth]{…}` 里的 **0.66** | 太大会顶到版心（编译日志会出现 `Overfull \hbox`） |
| 图居中／换位置 | `\begin{figure}[htbp]` 的 `[htbp]` 改成 `[ht]`；或加 `!` 变 `[!ht]` | 强制位置可能把文字挤开 |
| 表格列宽 | `m{\dimexpr 0.62\tblw\relax}` 里的 **0.62** | 各列比例之和 ≈ 1 |
| 表格加一行 | 复制一整行 `xxx & yyy & zzz \\` 改内容 | 列数必须与表头一致（否则报错） |
| 改字号 | 局部：`{\small …}`／`{\footnotesize …}`／`{\zihao{5} …}` | 改全局字号要动 `preamble.tex`，会影响页数 |
| 改行距 | `preamble.tex` 的 `\linespread{…}`（现为 1.0） | **行距一动，页数就变** ⟹ 每次核页数 |
| 加粗／斜体 | `\textbf{…}`／`\emph{…}` | 中文字体只有黑体有粗，见下 |
| 上下标、希腊字母 | `$t_{\rm dry}$`、`$\alpha$`、`$\pm10\%$` | 数字与单位放数学模式里更规范 |
| 不首行缩进 | 段首加 `\noindent` | — |
| 插入公式 | 复制附近的 `\begin{equation}…\end{equation}` 改内容；**要引用就写 `\eqref{eq:标签}`** | 编号会自动排，别手写 `(5-x)` |

---

## 三、三条"保命"提醒（这份论文特有的坑）

1. **不要再跑 `python gen_latex.py --apply`** —— 它会用 Markdown 稿**重新生成** `sections/*.tex`，**覆盖你现在的手改** ✗。从现在起，`sections/*.tex` 与 `preamble.tex` 就是**唯一真源**。
2. **每次改完看一眼两个数**：正文 **30 页**（红线 ≤30，超了就删内容或收版式）＋ 日志里 `Overfull \hbox = 0`、`Missing character = 0`。
3. **别用 LyX／Overleaf 视觉模式／Word 转换**来改这份稿 —— 自定义宏（`\srcfile` 按路径嵌代码）、`longtable` 的 `m{}` 列、`wrapfig` 环绕图、`fancyhdr` 页眉、CJK 字体路由，任何"导入导出"都可能破坏版式。

---

## 四、本目录已为你准备好的文件

| 文件 | 用途 |
|---|---|
| `main.tex` 顶部三行 `% !TEX …` | 魔术注释：TeXworks／TeXstudio 自动用 XeLaTeX ＋ UTF-8 |
| `编译预览.bat` ＋ `编译预览.ps1` | **双击＝保存即编译预览**（相当于 Word 实时预览） |
| `编译一次.bat` | 双击＝编译一次出 PDF（`xelatex` 跑两遍） |
| `fonts/Kingsoft_Cloud_Font.ttf` | 页眉字体（金山云技术体·商免）；删掉它会自动回退主字体，不影响编译 |

> ⚠ **为什么不用 `latexmk -pvc`**（已实测弃用）：本论文的图件路径含中文（`../../05_成品图/图35-…pdf`），
> `latexmk` 在 Windows 代码页下转 PDF 那步会报 `runscript.tlu … exit code 12`（xelatex 本身正常），
> 故**改为直接调 `xelatex` 两遍**（本会话已验证上百次，稳定出 191 页）。
