import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/Users/wangzerui/Documents/papers_agent/2512.22219")
FILES = [
    "abstract.tex",
    "intro.tex",
    "background.tex",
    "graph.tex",
    "compiler.tex",
    "runtime.tex",
    "eval.tex",
    "related.tex",
]

SKIP_LINE_PATTERNS = [
    re.compile(r"^\s*%"),
    re.compile(r"^\s*$"),
]

PROTECT_PATTERNS = [
    r"\$[^$]*\$",
    r"\\\[[^\]]*\\\]",
    r"\\cite\{[^{}]*\}",
    r"\\citet\{[^{}]*\}",
    r"\\citep\{[^{}]*\}",
    r"\\cref\{[^{}]*\}",
    r"\\Cref\{[^{}]*\}",
    r"\\ref\{[^{}]*\}",
    r"\\eqref\{[^{}]*\}",
    r"\\label\{[^{}]*\}",
    r"\\url\{[^{}]*\}",
    r"\\href\{[^{}]*\}\{[^{}]*\}",
    r"\\texttt\{[^{}]*\}",
    r"\\verb.\S.*?\S.",
    r"\\\w+\*?(?:\[[^\]]*\])?\{[^{}]*\}",
    r"\\\w+\*?(?:\[[^\]]*\])?",
]

COMMANDS_TO_TRANSLATE = [
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "caption",
    "title",
]


def gtranslate(text: str) -> str:
    stripped = text.strip()
    if not stripped or not re.search(r"[A-Za-z]", stripped):
        return text
    query = urllib.parse.quote(stripped)
    url = (
        "https://translate.googleapis.com/translate_a/single"
        f"?client=gtx&sl=en&tl=zh-CN&dt=t&q={query}"
    )
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=8, context=ctx) as response:
        data = json.loads(response.read().decode("utf-8"))
    translated = "".join(chunk[0] for chunk in data[0])
    if text.startswith(" "):
        translated = " " + translated
    if text.endswith(" "):
        translated = translated + " "
    return translated


def translate_brace_arg(command: str, src: str) -> str:
    pattern = re.compile(rf"(\\{command}(?:\[[^\]]*\])?\{{)([^{{}}]*)(\}})")

    def repl(match: re.Match[str]) -> str:
        return match.group(1) + gtranslate(match.group(2)) + match.group(3)

    return pattern.sub(repl, src)


def protect_line(text: str):
    slots: list[str] = []

    def repl(match: re.Match[str]) -> str:
        slots.append(match.group(0))
        return f"__SLOT_{len(slots) - 1}__"

    protected = text
    for pattern in PROTECT_PATTERNS:
        protected = re.sub(pattern, repl, protected)
    return protected, slots


def restore_line(text: str, slots: list[str]) -> str:
    restored = text
    for idx, slot in enumerate(slots):
        restored = restored.replace(f"__SLOT_{idx}__", slot)
    return restored


def should_skip_line(line: str) -> bool:
    return any(pattern.search(line) for pattern in SKIP_LINE_PATTERNS)


def translate_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for command in COMMANDS_TO_TRANSLATE:
        text = translate_brace_arg(command, text)

    output_lines = []
    for line in text.splitlines():
        if should_skip_line(line):
            output_lines.append(line)
            continue
        stripped = line.strip()
        if "&" in line and "\\\\" in line:
            output_lines.append(line)
            continue
        if stripped.startswith("\\") and " " not in stripped and "{" not in stripped:
            output_lines.append(line)
            continue
        protected, slots = protect_line(line)
        if re.search(r"[A-Za-z]{3,}", protected):
            try:
                translated = gtranslate(protected)
            except Exception:
                translated = protected
            output_lines.append(restore_line(translated, slots))
            time.sleep(0.05)
        else:
            output_lines.append(line)

    output_path = path.with_name(f"{path.stem}_zh.tex")
    output_path.write_text("\n".join(output_lines) + "\n", encoding="utf-8")
    print(output_path.name)


targets = sys.argv[1:] or FILES
for file_name in targets:
    translate_file(ROOT / file_name)
