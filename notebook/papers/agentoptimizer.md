# Offline Training of Language Model Agents with Functions as Learnable Weights

> 中文 PDF · `agentoptimizer/main_zh.pdf`

## 阅读入口

- [全屏打开 Viewer（推荐）](https://mozilla.github.io/pdf.js/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2Fwang-zerui%2Fpaper_zhs%2Fmain%2Fagentoptimizer%2Fmain_zh.pdf)
- [直接打开 PDF](https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/agentoptimizer/main_zh.pdf)
- [查看 GitHub 源文件](https://github.com/wang-zerui/paper_zhs/blob/main/agentoptimizer/main_zh.tex)
- 原文：[arXiv:2402.11359](https://arxiv.org/abs/2402.11359)

中文题目：以可学习函数为权重的语言模型智能体离线训练。

本文提出 AgentOptimizer，把智能体可调用的函数视为可学习参数，在不修改底层 LLM 权重的前提下，依据训练任务的执行历史渐进添加、修改或删除函数，并以回滚和早停约束优化过程。中文稿完整翻译摘要与全部正文主章节，保留公式、算法、图表、实验数值、引用、局限性与影响声明；官方英文附录及其资产保留在源码与 `source.tar` 中。
