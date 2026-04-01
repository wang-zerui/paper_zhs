# papers_agent

这是一个论文源码/翻译工作区，当前仓库里同时包含：

- 多个单篇论文目录（源码、翻译稿、编译产物、原始 `source.tar`）
- `notebook/`：面向 GitHub Pages / HonKit 的 PDF 阅读站
- `scripts/`：生成 notebook 和仓库索引的脚本
- `pdf/`：聚合导出的 PDF 目录

## 这次整理后的入口

- `REPO_INDEX.md`：本地工作区总览，扫描所有论文目录
- `repo_index.json`：和上面对应的机器可读索引
- `notebook/README.md`：GitBook 首页
- `notebook/catalog.json`：进入 notebook 的论文清单

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

### 2. notebook 与本地索引的区别

- `REPO_INDEX.md` 会扫描**所有本地目录**
- `notebook/` 会优先使用每个目录里的**候选主 PDF**

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

# 刷新 notebook 源文件
python3 scripts/build_paper_notebook.py

# 构建 GitHub Pages / HonKit 站点
npm run build:notebook

# 本地预览 notebook
npm run serve:notebook
```

## 说明

当前已经完成两轮整理：

- 第一轮：补齐索引、说明文档、脚本和 ignore 规则
- 第二轮：统一顶层论文目录命名
- 仍然没有删除现有源码/翻译文件，只做目录重命名和索引刷新

如果你下一步想继续，我可以再帮你做下一轮，例如：

1. 把顶层 `source.tar` 收拢到单独目录  
2. 补全缺失的 `00README.json`  
3. 自动生成每篇论文的状态表（原文 / 翻译 / PDF / notebook）  
4. 给新论文增加一键规范化脚本
