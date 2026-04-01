import re
import json
import urllib.parse
import urllib.request
import time
import ssl
from pathlib import Path

src = Path("/Users/wangzerui/Documents/papers_agent/EAGLE Speculative Sampling Requires Rethinking Feature Uncertainty/example_paper.tex")
dst = src.with_name("example_paper_zh.tex")
text = src.read_text(encoding="utf-8")

if "\\usepackage{xeCJK}" not in text:
    text = text.replace(
        "\\usepackage{hyperref}\n",
        "\\usepackage{hyperref}\n\\usepackage{fontspec}\n\\usepackage{xeCJK}\n\\setCJKmainfont{PingFang SC}\n",
        1,
    )

text = text.replace(
    "\\icmltitlerunning{EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty}",
    "\\icmltitlerunning{EAGLE：推测采样需要重新思考特征不确定性}",
)
text = text.replace(
    "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty",
    "EAGLE：推测采样需要重新思考特征不确定性",
    1,
)

def gtranslate(s: str) -> str:
    s_strip = s.strip()
    if not s_strip:
        return s
    if not re.search(r"[A-Za-z]", s_strip):
        return s
    q = urllib.parse.quote(s_strip)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q={q}"
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(url, timeout=12, context=ctx) as r:
            data = r.read().decode("utf-8")
        arr = json.loads(data)
        trans = "".join(x[0] for x in arr[0])
        if s.startswith(" "):
            trans = " " + trans
        if s.endswith(" "):
            trans = trans + " "
        return trans
    except Exception:
        return s


def trans_brace_arg(cmd, src_text):
    pat = re.compile(rf"(\\{cmd}(?:\[[^\]]*\])?\{{)([^{{}}]*)(\}})")
    def r(m):
        return m.group(1) + gtranslate(m.group(2)) + m.group(3)
    return pat.sub(r, src_text)

for c in ["section", "subsection", "subsubsection", "paragraph", "caption", "textbf", "emph"]:
    text = trans_brace_arg(c, text)

PROTECT_PATTERNS = [
    r"\$[^$]*\$",
    r"\\cite\{[^{}]*\}",
    r"\\citet\{[^{}]*\}",
    r"\\citep\{[^{}]*\}",
    r"\\ref\{[^{}]*\}",
    r"\\label\{[^{}]*\}",
    r"\\url\{[^{}]*\}",
    r"\\texttt\{[^{}]*\}",
    r"\\\w+\*?(?:\[[^\]]*\])?\{[^{}]*\}",
    r"\\\w+\*?(?:\[[^\]]*\])?",
]


def protect_line(s: str):
    slots = []

    def repl(m):
        slots.append(m.group(0))
        return f"⟪{len(slots)-1}⟫"

    tmp = s
    for pat in PROTECT_PATTERNS:
        tmp = re.sub(pat, repl, tmp)
    return tmp, slots


def restore_line(s: str, slots):
    out = s
    for i, v in enumerate(slots):
        out = out.replace(f"⟪{i}⟫", v)
    return out

out_lines = []
for line in text.splitlines():
    st = line.strip()
    if not st or st.startswith("%"):
        out_lines.append(line)
        continue

    # 跳过表格行与纯命令行
    if "&" in line and "\\\\" in line:
        out_lines.append(line)
        continue
    if st.startswith("\\") and " " not in st:
        out_lines.append(line)
        continue

    protected, slots = protect_line(line)
    if re.search(r"[A-Za-z]{3,}", protected):
        translated = gtranslate(protected)
        out_lines.append(restore_line(translated, slots))
    else:
        out_lines.append(line)
    time.sleep(0.02)

res = "\n".join(out_lines) + "\n"
res = res.replace("\\end{document}", "% 中文翻译版\n\\end{document}")
dst.write_text(res, encoding="utf-8")
print(f"written: {dst}")
