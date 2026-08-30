# CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM

> 中文 PDF · `chime/main_zh.pdf`

## 阅读入口

- [全屏打开 Viewer（推荐）](https://mozilla.github.io/pdf.js/web/viewer.html?file=https%3A%2F%2Fraw.githubusercontent.com%2Fwang-zerui%2Fpaper_zhs%2Fmain%2Fchime%2Fmain_zh.pdf)
- [直接打开 PDF](https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/chime/main_zh.pdf)
- [查看 GitHub 源文件](https://github.com/wang-zerui/paper_zhs/blob/main/chime/main_zh.pdf)
- 原文：[arXiv:2504.17584](https://arxiv.org/abs/2504.17584)

中文题目：CHIME：基于 DIMM-PIM 的高效长上下文 Attention-FC 分离式推理研究。

## 内容说明

本文提出面向 Attention-FC 分离式 LLM 推理的分离式屋顶线模型 DRM，并据此说明系统吞吐量受加速器内存容量或带宽中较弱一方约束。作者进一步给出集成 DIMM-PIM 的软硬件协同系统 CHIME，通过无气泡流水线、混合粒度重布局、秩组粒度通信--计算重叠和对齐预测调度减少同步开销；在作者的模拟评估中，CHIME 相对最先进 HBM-PIM 方案最高获得 5.15 倍加速。

中文稿完整翻译摘要及全部主文章节，包括相关工作、结论与致谢；原稿没有附录。公式、图表、实验数值、引用、限定条件及作者主张边界均予以保留，参考文献沿用原文。

## 备用文件块

{% file src="https://raw.githubusercontent.com/wang-zerui/paper_zhs/main/chime/main_zh.pdf" %}
CHIME 中文 PDF
{% endfile %}
