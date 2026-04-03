# papers_agent

这是一个论文源码 / 翻译工作区，现在它的主输出形态已经可以作为一个**随处访问的静态 PDF 阅读器**来使用：

- 每个顶层论文目录会自动挑选候选主 PDF
- 生成 `site/` 静态站点，可直接部署到 GitHub Pages
- 首页支持搜索 / 过滤 / 随机打开
- 单篇阅读页支持移动端目录、上一页 / 下一页、直接打开 PDF、跳 GitHub 源文件

仓库里仍然保留：

- 多个单篇论文目录（源码、翻译稿、编译产物、原始 `source.tar`）
- `notebook/`：旧的 HonKit / GitBook 版本阅读站
- `scripts/`：生成索引、旧 notebook、以及新的静态 PDF 阅读器
- `pdf/`：聚合导出的 PDF 目录

## 主要入口

- `REPO_INDEX.md`：本地工作区总览，扫描所有论文目录
- `repo_index.json`：对应的机器可读索引
- `scripts/build_pdf_reader_site.py`：生成新阅读器站点
- `site/`：新的静态阅读器构建产物
- `.github/workflows/deploy-paper-notebook.yml`：推送到 `main` 后自动发布 GitHub Pages

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

### 2. 阅读器站点与本地索引的区别

- `REPO_INDEX.md` 会扫描**所有本地目录**
- `site/` / `notebook/` 会优先使用每个目录里的**候选主 PDF**

这样可以同时满足：

- 本地整理时能看到完整工作区
- 本地预览和提交后的 GitHub Pages 构建都走同一套目录扫描逻辑

### 3. `00README.json`

带 `00README.json` 的目录会被识别为“已标准化”的论文目录；脚本会从中提取：

- 主入口 tex
- 编译器信息

## 常用命令

```bash
# 刷新本地仓库索引
python3 scripts/build_repo_index.py

# 生成新的静态 PDF 阅读器
python3 scripts/build_pdf_reader_site.py

# 本地预览新的阅读器
python3 -m http.server 8000 --directory site

# 也可以用 npm scripts
npm run build:reader
npm run serve:reader

# 刷新 notebook 源文件
python3 scripts/build_paper_notebook.py

# 构建 GitHub Pages / HonKit 站点
npm run build:notebook

# 本地预览 notebook
npm run serve:notebook
```

## 部署方式

默认工作流已经改成发布新的静态阅读器：

1. push 到 `main`
2. GitHub Actions 执行 `python3 scripts/build_pdf_reader_site.py`
3. 将 `site/` 作为 GitHub Pages artifact 发布

这样部署后，你就能通过 GitHub Pages 从任意设备直接访问整套 PDF 阅读站。

## 补充说明

- `notebook/` 还保留着，方便继续使用原来的 HonKit 结构
- 新的 `site/` 不依赖 Node / HonKit，纯静态 HTML + CSS + JS，更适合直接发布
- 没有删除现有论文源码/翻译文件，只是在此基础上新增了阅读器生成链路
