from pathlib import Path
import translate_tex

root = Path('.')
chunks_dir = root / 'chunks'
preface = (chunks_dir / 'preface.tex').read_text(encoding='utf-8')
out = [translate_tex.build_preface(preface), r'\begin{document}', '\n']
for path in sorted(chunks_dir.glob('chunk_*_zh.tex')):
    out.append(path.read_text(encoding='utf-8'))
out_path = root / 'main_zh.tex'
out_path.write_text(''.join(out), encoding='utf-8')
print(out_path)
