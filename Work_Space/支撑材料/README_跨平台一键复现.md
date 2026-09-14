# 跨平台一键复现说明（Windows / macOS / Linux）

> **用途**：说明如何在他人的设备、其他操作系统上**一键复现** A 题全部结果，并给出逐项可行性核查结论。
> **结论速览**：**主链路（`run_all.py` ＋ `code/` 全部脚本）在三平台可直接一键运行**；
> 3 个辅助链式启动器（`run_chain.py`、`run_innov_chain.py`、`run_innov_chain2.py`）的
> `python` 命令硬编码与日志目录假设**已完成跨平台适配**（见 §四）；
> 仅 `rerun_chain.ps1` 保留为 Windows 便捷脚本（跨平台请用等价的 `run_chain.py`）。
> **核查方式**：静态代码审计（依赖／路径／平台 API／并行启动方式）＋ 平台启动机制等价性推理；
> **未在 macOS／Linux 实机运行**，故下表中凡推断项均已注明依据。

---

## 一、一键运行（最短路径）

```bash
# 1) 准备 Python 3.9+（开发环境实测 3.14.7；3.11–3.14 均可）
python --version

# 2) 安装依赖（在本目录：20_交付包/09_代码与复现/）
pip install -r requirements.txt

# 3) 查看复现计划（不执行任何计算，仅打印脚本清单）
python run_all.py

# 4) 实际执行（按序运行求解与检验脚本，并把 --go 透传给各脚本）
python run_all.py --go
```

> **macOS / Linux 提示**：若系统没有 `python` 命令（新版发行版常只提供 `python3`），
> 请把上述命令中的 `python` 换成 `python3`。`run_all.py` 自身通过 `sys.executable`
> 调用子脚本，因此**只要能用同一条命令启动它，内部调用就不会出错**。

> **覆盖范围（全题一键）**：`run_all.py` 按目录扫描收集 **求解（4）＋ 检验/诊断（68）＋ 创新（14）**，
> **递归包含 `code/innov/`**；公共库／非入口模块（`*_lib`／`*_par`／`*core*`／`*exact*` 等）自动排除。
> 工作区内另有一个全量入口 `tools/rerun_all.py`（覆盖 102 个程序：主求解＋检验＋创新＋参考图渲染，
> 副本隔离运行并**自动生成复现结论**）：无参数运行时会**交互询问执行模式**，
> Agent／脚本化调用可直接传参 `--go --groups solver,check,innov,fig`。

---

## 二、目录要求（必须保持，勿只拷 `code/`）

```
<工作区根>/
├── 10_赛题/A题/附件/附件1.xlsx          ← 题目输入（必需）
├── 10_赛题/A题/附件/附件2.xlsx          ← 第四问输入（必需）
├── 11_建模/...                           ← 工作区脚本位置（可选，与交付副本同源）
├── 20_交付包/09_代码与复现/
│   ├── run_all.py                        ← 一键入口
│   ├── code/                             ← 全部源程序
│   ├── results/                          ← result1–4.xlsx 输出位置
│   └── requirements.txt
└── 30_图表/03_图数据准备/                ← 图数据 CSV 输出位置
```

**原因**：所有脚本以**自身位置**为基准，用 `_find_root()` 向上探测含 `10_赛题` 的目录来定位工作区根，
因此**不能硬编码绝对路径，也不能把 `code/` 单独拷走**（否则找不到 `10_赛题`，无法读取附件）。
同一份代码在工作区（`11_建模/11-3_算法与管线/Q*/code/`）与交付副本（`09_代码与复现/code/`）
两种深度下均可直接运行，无需修改。

---

## 三、跨平台可行性核查（逐项）

| 检查项 | 结论 | 依据 |
|---|---|---|
| 第三方依赖 | ✅ 三平台可用 | 仅 `numpy`／`scipy`／`openpyxl`（`numba`／`SALib` 可选，缺失自动降级），均为纯 Python 或提供三平台预编译 wheel |
| 平台专属 API | ✅ 无 | 全仓检索 `sys.platform`／`os.name`／`win32`／`winsound`／`winreg`／`.dll`／`.exe` → **0 命中** |
| 绝对路径 | ✅ 无 | 检索 `C:\`／`D:\`／`/Users/`／`/home/` → **0 命中**；全部为脚本自身位置相对定位 |
| shell 调用 | ✅ 无 | 检索 `os.system`／`shell=True`／`powershell`／`cmd /c` → **0 命中**；仅用 `subprocess` 列表式调用 |
| 文本编码 | ✅ 显式 | 文件读写显式 `encoding='utf-8'`（含日志、CSV、JSON）；JSON 输出 `ensure_ascii=False` |
| 子进程解释器 | ✅ 正确 | `run_all.py` 使用 `sys.executable`（随当前解释器，跨平台正确） |
| **并行计算（17 个脚本）** | ✅ 安全 | 使用 `concurrent.futures.ProcessPoolExecutor`／`multiprocessing.Pool`，且相关入口**均含 `if __name__ == '__main__'` 保护**；macOS 与 Windows 同为 **spawn** 启动方式，Windows 已实测通过 ⟹ 同机制在 macOS 上成立（Linux 的 fork 更宽松） |
| 文件换行／路径分隔 | ✅ 兼容 | 路径拼接一律 `os.path.join`；不依赖平台分隔符 |
| 中文路径 | ✅ 兼容 | 三平台均支持 UTF-8 路径；脚本不假设 ASCII 路径 |

---

## 四、可迁移适配情况

**已完成的适配**（主工作区 `11_建模/11-3_算法与管线/Q4/` 与交付副本 `09_代码与复现/code/` 同步修改）

| # | 位置 | 原问题 | 处理 |
|---|---|---|---|
| L1 | `run_chain.py`、`run_innov_chain.py`、`run_innov_chain2.py` | 硬编码命令名 `'python'`；macOS／Linux 常无该命令 → `FileNotFoundError` | 改为 `sys.executable`（随当前解释器，跨平台正确） |
| L2 | `run_chain.py` | 日志目录取 `../logs`；交付副本 `09_代码与复现/` 下无 `logs/` 目录 → `FileNotFoundError` | 增加存在性判断：不存在则回退到上级目录本身（与 `rerun_chain.ps1` 语义一致），并 `os.makedirs(..., exist_ok=True)` |
| L3 | `run_innov_chain.py`、`run_innov_chain2.py` | 日志目录取 `code/logs`；交付副本内该目录不存在 | `os.makedirs(..., exist_ok=True)` 兜底 |
| L5 | `requirements.txt` 注释 | 注明"实测 Python 3.14.7 / Windows"，易被误读为平台限制 | 补注"所列依赖均为跨平台包（Windows／macOS／Linux 同源），无平台限制" |

**保留项（不修改）**

| # | 位置 | 说明 |
|---|---|---|
| L4 | `code/rerun_chain.ps1` | PowerShell 脚本，Windows 专属 → macOS／Linux 不可执行。**保留作溯源留痕**；跨平台用户请使用已适配的等价脚本 `run_chain.py`，无需理会该文件 |

**适配后校验**（静态，未触发任何求解）：6 个启动器语法解析通过、无 `'python'` 硬编码、
均使用 `sys.executable`；日志目录在两种目录深度下解析结果均存在（主工作区 `Q4/logs`、
交付副本 `09_代码与复现/`）。

> 以上脚本均为**辅助驱动**，不在主复现链路上：`run_all.py` 按目录扫描自动收集
> 求解与检验脚本并逐个以 `sys.executable` 调用，不依赖这些 chain 脚本。

---

## 五、复现核对清单

运行完成后，按下表核对（详细期望值见同目录 `A_代码复现.md` 与
`20_交付包/05_数值口径总表/A_数值口径总表.md`）：

| 产物 | 核对要点 |
|---|---|
| `results/result1.xlsx` | 两个工作表各 1801 行 × 22 列；`T(0,1800)=33.5753 ℃`、`T(R,1800)=36.7855 ℃`、`C(R,1800)=1.5104` |
| `results/result2.xlsx` | 3 h 时程；`T(0,3h)=49.8495 ℃`、`C(0)=1.7662`、`C(R)=1.0081` |
| `results/result3.xlsx` | `t_end=57.5314 h`；末行时间列与二分定位值一致 |
| `results/result4.xlsx` | 3041 行 × 22 列（含表头）；`t_dry=182348.109 s`；`R(t_dry)=1.200 cm`；`r>R(t)` 留空 |
| 日志 | 各脚本自建日志中的断言项应全部 PASS |

**浮点末位差异**：不同 `numpy` 版本下可能出现 1 ULP 级差异，**不影响 4 位小数结果**。

---

## 六、常见问题

**Q1：macOS 上 `pip install numba` 失败怎么办？**
`numba` 为**可选加速项**：缺失时求解核自动降级为纯 NumPy 实现，**数值结果不变**，仅耗时增加。

**Q2：可以用 `python3` 吗？**
可以。只要用同一条命令启动 `run_all.py`，其内部通过 `sys.executable` 调用子脚本，不会串环境。

**Q3：为什么必须保留 `10_赛题` 目录？**
脚本用 `_find_root()` 向上探测该目录来定位工作区根；缺失时只能回退到固定层数，可能定位错误。

**Q4：`code/` 下的 `*_orig.py`／`*prebug*`／`*preM6*` 等脚本要跑吗？**
不必。它们是**历史对照／溯源**脚本（基线与缺陷前版本），不产生交付数值。
