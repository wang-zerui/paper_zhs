from pathlib import Path

path = Path('main_zh.tex')
text = path.read_text(encoding='utf-8')
replacements = [
    ('具有威震天核心的混合专家模型的可扩展训练', 'Megatron Core 上混合专家模型的可扩展训练'),
    ('威震天核心', 'Megatron Core'),
    ('Megatron-核心', 'Megatron-Core'),
    ('威震天桥', 'Megatron-Bridge'),
    ('威震天-LM', 'Megatron-LM'),
    ('威震天-MoE-ModelZoo', 'Megatron-MoE-ModelZoo'),
    ('专家荟萃', '混合专家'),
    ('教育部', 'MoE'),
    ('密集变压器', '稠密 Transformer'),
    ('变压器', 'Transformer'),
    ('变形金刚', 'Transformer'),
    ('代币', '令牌'),
    ('通讯', '通信'),
    ('沟通', '通信'),
    ('记忆墙', '内存墙'),
    ('乙状结肠', 'sigmoid'),
    ('全对所有', 'all-to-all'),
]
for old, new in replacements:
    text = text.replace(old, new)

# Normalize a few common machine-translation artifacts in technical text.
text = text.replace('all-to-all', 'all-to-all')
text = text.replace('英伟达。版权所有。', 'NVIDIA。保留所有权利。')
text = text.replace('英伟达', 'NVIDIA')
text = text.replace(r'\section{介绍}', r'\section{引言}')
text = text.replace('顶部-$k$', 'top-$k$')
text = text.replace('顶部-$K$', 'top-$K$')
text = text.replace('威震天-核心', 'Megatron-Core')
text = text.replace('MoE培训', 'MoE 训练')
text = text.replace('MoE 培训', 'MoE 训练')
text = text.replace('MoE训练', 'MoE 训练')
text = text.replace('MoE层', 'MoE 层')
text = text.replace('MoE模型', 'MoE 模型')
text = text.replace('MoE架构', 'MoE 架构')
text = text.replace('MoE并行', 'MoE 并行')

path.write_text(text, encoding='utf-8')
print(path)
