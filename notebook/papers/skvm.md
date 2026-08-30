# SkVM: Revisiting Language VM for Skills across Heterogenous LLMs and Harnesses

> 中文 PDF · `skvm/main_zh.pdf`

## 阅读入口

- [全屏打开 Viewer（推荐）](https://mozilla.github.io/pdf.js/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2Fwang-zerui%2Fpaper_zhs%2Fmain%2Fskvm%2Fmain_zh.pdf)
- [直接打开 PDF](https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/skvm/main_zh.pdf)
- [查看 GitHub 源文件](https://github.com/wang-zerui/paper_zhs/blob/main/skvm/main_zh.pdf)
- [原文 arXiv:2604.03088](https://arxiv.org/abs/2604.03088)

中文题目：SkVM：重访跨异构 LLM 与代理框架的技能语言虚拟机。

## 内容说明

本文把技能视为代码、把 LLM 视为异构处理器，提出面向技能可移植执行的编译与运行时系统 SkVM。系统通过基于 26 项原语能力的 AOT 编译、环境绑定和并发性提取来适配模型、代理框架与主机环境，并在运行时采用自适应重编译、代码固化和资源感知调度。作者在八个 LLM、三个代理框架与 118 个代表性任务上报告平均任务完成率提升 15.3\%、token 消耗最多降低 40\%、并行化最高加速 3.2 倍，以及代码固化带来的 19--50 倍延迟降低；论文同时讨论了自然语言编译的非确定性、能力目录覆盖范围与编译成本。
