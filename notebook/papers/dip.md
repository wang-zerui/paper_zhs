# DIP: Efficient Large Multimodal Model Training with Dynamic Interleaved Pipeline

> 中文 PDF · `dip/main_zh.pdf`

- [全屏打开 Viewer](https://mozilla.github.io/pdf.js/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2Fwang-zerui%2Fpaper_zhs%2Fmain%2Fdip%2Fmain_zh.pdf)
- [直接打开 PDF](https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/dip/main_zh.pdf)
- [查看 GitHub 源文件](https://github.com/wang-zerui/paper_zhs/blob/main/dip/main_zh.pdf)
- 原文：[arXiv:2504.14145](https://arxiv.org/abs/2504.14145)

中文题目：DIP：面向高效大多模态模型训练的动态交错流水线。

内容简介：本文提出面向大多模态模型训练的动态模态感知流水线调度框架 DIP，通过分离不同模态的流水线段、动态构造特定于模态的子微批次，以及异步的分解式调度搜索，缓解异构模型结构与动态多模态数据共同造成的流水线不均衡；作者在五种 12B--94B 模型上报告了最高 97.3% 的训练吞吐量提升。
