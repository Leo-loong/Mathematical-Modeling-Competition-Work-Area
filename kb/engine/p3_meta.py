# -*- coding: utf-8 -*-
"""P3 元数据抽取：为所有可索引文件生成 title/summary/keywords/funcs -> data/files.json。
覆盖：kb/source 根下动态发现的所有语料区（temp 除外，_无效内容 跳过），含根级散文件。
  - 全部路径由脚本位置动态推导，kb 文件夹整体移动无需改代码；
  - 文本文件全文索引；PDF/CAJ/DOC 等二进制按"文件名级"注册为 kind=doc（转 md 前也能搜到）；
  - 所有 path 相对【kb 的上级目录】（如 kb/source/xxx），统一正斜杠。
keywords 来源：内置别名词典命中 + 英文缩写 + 文件名分词。
⚠ 约束：本引擎任何脚本禁止用 os.remove / shutil.rmtree 删除语料或索引文件
  （会触发环境安全删除保护导致进程异常）；需要清理时一律移动到 source/temp 隔离目录。
"""
import os
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))          # kb/engine
KB = os.path.dirname(HERE)                                  # kb
WORKSPACE = os.path.dirname(KB)                             # kb 的上级（工作区根）
SOURCE_ROOT = os.path.join(KB, "source")
DATA = os.path.join(HERE, "data")
# 可选：source 之外的额外语料根（相对工作区）。默认空——文献请直接放 kb/source 内。
EXTRA_ROOTS = []
EXCLUDE = {"_无效内容"}
NON_CORPUS = {"temp"}  # source 下非语料目录（工具/报告），永不入索引


def discover_areas():
    """动态发现语料区：source 子目录 + 额外语料根。返回 [(area_name, base_dir)]。"""
    areas = []
    for name in sorted(os.listdir(SOURCE_ROOT)):
        p = os.path.join(SOURCE_ROOT, name)
        if os.path.isdir(p) and name not in NON_CORPUS:
            areas.append((name, p))
    for extra in EXTRA_ROOTS:
        p = os.path.join(WORKSPACE, extra) if not os.path.isabs(extra) else extra
        if os.path.isdir(p):
            areas.append((os.path.basename(p), p))
    return areas


AREAS = discover_areas()
CODE_EXTS = {".m", ".M", ".py", ".c", ".h", ".cpp"}
MD_EXTS = {".md"}
TEXT_EXTS = MD_EXTS | CODE_EXTS | {".txt", ".html", ".cls", ".bst", ".bib", ".dat", ".sty", ".csv", ".json"}
# 仅在额外语料根（refs 等）注册文件名级索引的二进制文档类型
DOC_EXTS = {".pdf", ".caj", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
PAGE_MARK = re.compile(r"<!--\s*第\s*\d+\s*页\s*-->")
WS = re.compile(r"\s+")
ABBR = re.compile(r"\b[A-Z]{2,8}\b")
FUNC_M = re.compile(r"^\s*(?:function\s+[\w\s,=~]*=\s*([A-Za-z_]\w*)|def\s+([A-Za-z_]\w*)|([A-Za-z_]\w*)\s*\(\s*[A-Za-z_]\w*\s*\)\s*\{)", re.M)

# 受控别名词典：标准词 -> 别名列表（检索时双向扩展）。人工增量维护入口。
ALIAS = {
    "线性规划": ["LP", "Linear Programming", "linprog"],
    "整数规划": ["MILP", "混合整数规划", "intlinprog"],
    "非线性规划": ["NLP", "fmincon"],
    "多目标规划": ["多目标优化", "Pareto", "NSGA", "帕累托"],
    "动态规划": ["DP", "Dynamic Programming"],
    "层次分析法": ["AHP", "Analytic Hierarchy"],
    "TOPSIS": ["逼近理想解", "理想解法"],
    "熵权法": ["熵值法", "Entropy Weight"],
    "灰色关联分析": ["GRA", "灰色关联度"],
    "灰色预测": ["GM(1,1)", "GM11"],
    "模糊综合评价": ["模糊评价", "Fuzzy"],
    "主成分分析": ["PCA", "Principal Component"],
    "因子分析": ["Factor Analysis"],
    "聚类分析": ["K-means", "K均值", "聚类", "Cluster"],
    "判别分析": ["判别"],
    "典型相关分析": ["典型相关"],
    "回归分析": ["回归", "Regression", "最小二乘", "OLS"],
    "逻辑回归": ["Logistic Regression"],
    "时间序列": ["ARIMA", "指数平滑", "预测模型"],
    "蒙特卡洛": ["Monte Carlo", "MC模拟", "随机模拟"],
    "模拟退火": ["Simulated Annealing", "SA算法"],
    "遗传算法": ["GA", "Genetic Algorithm"],
    "粒子群优化": ["PSO", "粒子群算法"],
    "蚁群算法": ["ACO", "蚁群"],
    "神经网络": ["BP神经网络", "ANN", "BP网络", "RBF", "GRNN"],
    "支持向量机": ["SVM", "SVR"],
    "随机森林": ["Random Forest"],
    "决策树": ["Decision Tree"],
    "微分方程模型": ["常微分方程", "ODE", "微分方程", "差分方程"],
    "偏微分方程": ["PDE", "热传导", "扩散方程"],
    "有限元": ["FEM", "Finite Element"],
    "图论": ["最短路径", "Dijkstra", "Floyd", "最小生成树"],
    "网络流": ["最大流", "最小费用流"],
    "排队论": ["排队模型", "M/M/1"],
    "博弈论": ["纳什均衡", "Game Theory"],
    "插值与拟合": ["插值", "拟合", "Interpolation", "三次样条", "Lagrange"],
    "小波分析": ["小波变换", "小波降噪", "小波去噪", "Wavelet"],
    "傅里叶变换": ["FFT", "Fourier", "傅里叶"],
    "滤波": ["卡尔曼滤波", "Kalman", "滤波器"],
    "灵敏度分析": ["敏感性分析", "Sensitivity"],
    "稳健性检验": ["鲁棒性", "Robustness", "稳健性"],
    "误差分析": ["不确定度", "残差分析", "误差"],
    "参数反演": ["反问题", "参数估计", "反演", "厚度反演"],
    "数据包络分析": ["DEA"],
    "秩和比": ["RSR"],
    "熵权TOPSIS": ["熵权topsis"],
    "薄膜干涉": ["光程差", "干涉条纹", "等厚干涉", "双光束干涉"],
    "多光束干涉": ["Fabry-Pérot", "Fabry-Perot", "F-P腔", "法布里珀罗", "Airy"],
    "折射率色散": ["Cauchy", "Sellmeier", "柯西", "色散模型"],
    "Drude模型": ["Drude", "载流子浓度"],
    "红外测厚": ["红外干涉", "膜厚测量", "外延层厚度"],
    "碳化硅": ["SiC", "4H-SiC", "6H-SiC", "外延层"],
    "论文写作": ["论文模板", "写作规范", "摘要写作", "三线表"],
    "AI合规": ["AIGC检测", "AI自查", "AI红线", "AI痕迹"],
    "提示词": ["Prompt", "提示词模板"],
    "流程图": ["Visio", "技术路线图"],
}

ENC_ABBR = {"AHP", "TOPSIS", "PCA", "GRA", "GA", "PSO", "ACO", "SVM", "ODE", "PDE",
            "FFT", "ARIMA", "MILP", "DEA", "RSR", "SiC", "NLP", "LP", "ANN", "MC"}


def read_text_best(path):
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8", "gbk"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def md_fields(text):
    text = PAGE_MARK.sub("", text)
    lines = text.split("\n")
    title, heads = "", []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", s)
        if m:
            if not title:
                title = m.group(2).strip()
            if len(heads) < 40:
                heads.append(m.group(2).strip())
    # summary：第一个非标题、非空、非表格分隔的段落行
    summary = ""
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith(("#", "|", "---", "> ", "<!--", "```")):
            continue
        summary = re.sub(r"[*_`\[\]]", "", s)[:160]
        break
    if not summary and title:
        summary = title
    return title, summary, heads


def keywords_for(title, heads, fname, text_head):
    kws = set()
    hay = title + " \n " + " \n ".join(heads) + " \n " + fname
    for std, aliases in ALIAS.items():
        terms = [std] + aliases
        if any(t.lower() in hay.lower() for t in terms):
            kws.add(std)
            for a in aliases:
                if a.lower() in hay.lower():
                    kws.add(a)
    for a in ABBR.findall(text_head)[:10]:
        kws.add(a)
    stem = os.path.splitext(os.path.basename(fname))[0]
    for tok in re.findall(r"[A-Za-z]{3,}", stem):
        kws.add(tok)
    return sorted(kws)[:24]


def main():
    os.makedirs(DATA, exist_ok=True)
    records, seen = [], set()

    def add_record(area, full, fn):
        ext = os.path.splitext(fn)[1].lower()
        rel = os.path.relpath(full, WORKSPACE).replace("\\", "/")
        if rel in seen:
            return
        if ext in TEXT_EXTS:
            kind = "md" if ext in MD_EXTS else ("code" if ext in CODE_EXTS else "text")
            try:
                text = read_text_best(full)
            except OSError:
                return
            nchars = len(text)
            if kind == "md":
                title, summary, heads = md_fields(text)
            elif kind == "code":
                title, summary, heads = fn, "", []
                m = re.search(r"^\s*(?:%|//|#)\s*(\S.{4,80})", text, re.M)
                if m:
                    summary = m.group(1).strip()
            else:
                title = fn
                first = next((l.strip() for l in text.split("\n") if l.strip()), "")
                summary, heads = first[:160], []
            funcs = [a or b or c for a, b, c in FUNC_M.findall(text)][:30] if kind == "code" else []
            kws = keywords_for(title, heads, fn, text[:4000])
        elif ext in DOC_EXTS:  # 二进制文献：仅文件名级注册
            kind, nchars, summary, heads, funcs = "doc", 0, "", [], []
            title = fn
            kws = keywords_for(title, [], fn, "")
        else:
            return
        seen.add(rel)
        records.append({
            "path": rel, "area": area, "kind": kind, "ext": ext,
            "title": title or fn, "summary": summary,
            "nchars": nchars, "keywords": kws, "funcs": funcs,
        })

    for area, base in discover_areas():
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE]
            for fn in filenames:
                add_record(area, os.path.join(dirpath, fn), fn)
    # source 根级散文件（用户直接拖进 source 的文件）
    for fn in os.listdir(SOURCE_ROOT):
        full = os.path.join(SOURCE_ROOT, fn)
        if os.path.isfile(full):
            add_record("_root", full, fn)

    with open(os.path.join(DATA, "files.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)
    n_kw = len(set(k for r in records for k in r["keywords"]))
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print("P3 done. files=%d (%s) unique_keywords=%d"
          % (len(records), ", ".join("%s=%d" % kv for kv in sorted(kinds.items())), n_kw))


if __name__ == "__main__":
    main()
