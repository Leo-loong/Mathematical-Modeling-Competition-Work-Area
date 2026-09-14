# kb/engine — 本地搜索引擎

对 `kb/source/` 全部语料建立统一词法检索库（含新增文件夹自动发现、PDF 等文献原件文件名级注册），源文件除 P2 规则化精修（仅"提取后"目录 md，已备份）外零改动。**全部路径动态推导，kb 整体移动到正式工作目录无需改代码。**

## 一键增量更新（最常用）

```powershell
# 新内容拖进 kb\source（任意新文件夹/散文件），然后：
python kb\engine\update.py
```

## Agent 检索方式

```powershell
# 1) 常规查询：文件级命中 + 最佳段落定位（自动别名扩展 + 重复组折叠）
python kb\engine\p5_search.py 蒙特卡洛

# 2) 段落级深挖：给出所有命中的 文件:行号（供 read_file 定位精读）
python kb\engine\p5_search.py 建模方法 --deep

# 3) 只搜代码 / JSON 输出
python kb\engine\p5_search.py wavelet --type code
python kb\engine\p5_search.py 小波 --json
```

- 命中结果带 `[低信息量]` 标注（<500 字符的清单页，参考价值低）。
- OCR 件正文可能含形近字误差，引用数字前回查原始文件。

## 重建流程（语料变更后按序重跑，全部幂等）

```powershell
python kb\engine\p1_scan.py        # 只读扫描建档（重复组、质量标签）
python kb\engine\p2_refine.py      # 规则化精修提取后 md（自动备份到 data\p2_backup）
python kb\engine\p3_meta.py        # 元数据/关键词抽取 -> data\files.json
python kb\engine\p4_build_index.py # 构建 data\catalog.db（FTS5 trigram）
python kb\engine\p5_report.py      # 重建 kb\index\MOC.md 与 覆盖与缺口.md
```

## 维护要点

- **增量接入**：扫描区为 `source/` 根目录下**所有**子目录的动态发现（`temp` 除外，`_无效内容` 跳过）——网盘新资料放 `source/` 下任意新目录（如 `第三批/`）重跑 p3→p5 即可。精修（p2）只处理名字含"提取后"的目录，原始区永不修改。
- **别名词表**：`p3_meta.py` 顶部 `ALIAS` 字典是检索质量的核心杠杆，发现"搜不到但库里有"的同义叫法就补进去，然后重跑 p3→p5。
- **索引重建**：p4 用库内 `DROP TABLE` 幂等重建，不做文件系统删除（会触发环境安全删除保护）。
- **验证**：`t1_incremental_test.py`（增量更新）、`t2_recall_test.py`（召回率+账实核对），报告在 `data/`。T2 实测：正文特征片段召回率 88.4%，未命中全部为 `function/figure` 类全局高频通用标识符（排序截断，非索引缺失）。
- **已知检索边界**：扫描件 PDF/CAJ/PPT/VSS 仅文件名可检索；OCR 错字需按错字或别名查询；语义改述不召回（词法引擎设计边界）。
- 语义检索（embedding）设计上已预留 `chunks.cid` 映射，如需后补不需重构。

## 产物

| 文件 | 说明 |
|---|---|
| `data/catalog.db` | SQLite 检索库（files + chunks + FTS5） |
| `data/files.json` | 文件元数据（标题/摘要/关键词/函数名） |
| `data/p1_*.csv` | 全源清单、重复组 |
| `data/p2_backup/` | P2 精修前备份（可整目录回滚） |
| `kb/index/MOC.md` | 全库文件地图（自动生成） |
| `kb/index/覆盖与缺口.md` | 方法覆盖统计 + 缺口清单 + 网盘补料建议 |
