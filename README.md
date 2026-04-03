# papers_agent

这是一个论文源码 / 翻译工作区。为了避免继续折腾 GitHub Pages 自动部署，现在仓库的**主接入方式改成 GitBook Sync**：

- 继续扫描每个顶层论文目录里的候选主 PDF
- 自动生成 `notebook/` 下的 GitBook 目录页和单篇论文页
- 通过 `.gitbook.yaml` 让 GitBook 直接把 `notebook/` 当作文档根目录
- 每篇论文页提供 PDF 文件块、PDF 直链、GitHub 源文件链接

## 主要入口

- `REPO_INDEX.md`：本地工作区总览，扫描所有论文目录
- `repo_index.json`：对应的机器可读索引
- `.gitbook.yaml`：GitBook 配置，指定文档根目录为 `notebook/`
- `notebook/README.md`：GitBook 首页
- `notebook/SUMMARY.md`：GitBook 左侧目录
- `scripts/build_paper_notebook.py`：生成 GitBook-friendly 页面

## 当前约定

### 1. 论文目录

默认每个顶层论文目录视为一个独立条目，例如：

- `blitzscale/`
- `td-pipe/`
- `glm-5/`

当前统一规则：

- 顶层论文目录统一为 **lowercase kebab-case**
- 能从论文主 `tex` 提取到标题时，优先使用**标题 / 系统名 slug**
- 项目名/论文名目录统一写成 `flashinfer`、`byte-checkpoint`、`workload-router-pool` 这种形式
- 只有在标题还不明确时，才临时保留编号风格目录名

### 2. GitBook 目录与本地索引的区别

- `REPO_INDEX.md` 会扫描**所有本地目录**
- `notebook/` 会优先使用每个目录里的**候选主 PDF**

这样可以同时满足：

- 本地整理时能看到完整工作区
- GitBook 展示时只暴露适合阅读的 PDF 入口

### 3. `00README.json`

带 `00README.json` 的目录会被识别为“已标准化”的论文目录；脚本会从中提取：

- 主入口 tex
- 编译器信息

## 常用命令

```bash
# 刷新本地仓库索引
python3 scripts/build_repo_index.py

# 生成 GitBook 页面
python3 scripts/build_paper_notebook.py

# 如果还想本地看旧的 HonKit 版本
npm run build:notebook
npm run serve:notebook
```

## GitBook 接入方式

1. 在 GitBook 新建一个 space。
2. 连接这个 GitHub 仓库。
3. 让 GitBook 使用仓库根目录下的 `.gitbook.yaml`。
4. GitBook 会读取 `notebook/README.md` 和 `notebook/SUMMARY.md` 作为文档入口。

## 说明

- 当前主路线是 **GitBook Sync**，不是 GitHub Pages 自动发布
- `.github/workflows/deploy-paper-notebook.yml` 已改为仅手动触发，避免每次 push 都报错
- `site/` 静态阅读器脚本还保留着，但不再作为默认方案
- GitBook 更适合作为“论文索引 + PDF 打开入口”；如果未来要追求站内内嵌 PDF 阅读体验，再回到静态站方案会更合适
