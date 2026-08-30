# KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider

> 中文 PDF · `kvcache-cache-in-the-wild/main_zh.pdf`

- [全屏打开 Viewer](https://mozilla.github.io/pdf.js/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2Fwang-zerui%2Fpaper_zhs%2Fmain%2Fkvcache-cache-in-the-wild%2Fmain_zh.pdf)
- [直接打开 PDF](https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/kvcache-cache-in-the-wild/main_zh.pdf)
- [查看 GitHub 源文件](https://github.com/wang-zerui/paper_zhs/blob/main/kvcache-cache-in-the-wild/main_zh.pdf)
- 原文：[arXiv:2506.02634](https://arxiv.org/abs/2506.02634)

中文题目：真实世界中的 KVCache 缓存：某大型云服务商的特征刻画与优化。

内容简介：本文基于一家大型云服务商的两类生产轨迹，系统刻画单轮与多轮请求的 KVCache 复用、时间与空间局部性以及容量需求，并提出按请求类别拟合复用概率分布的工作负载感知淘汰策略。作者报告该策略相对其他基线将命中率提高 1.5--3.9\%，并将排队首 token 时间降低 28.3--41.9\%；同时明确说明轨迹只覆盖一家服务商的一周工作负载，新型推理工作负载与全局调度扩展仍留作未来工作。
