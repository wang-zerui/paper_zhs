import json
import argparse
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BATCH_TARGET_CHARS = 3500

PREFACE_REPLACEMENTS = {
    r"\documentclass[10pt,logo,copyright]{nvidiatechreport}": r"\documentclass[10pt,logo,copyright]{nvidiatechreport_zh}",
    r"\input{packages}": r"\input{packages_zh}",
    r"\input{common.tex}": r"\input{common_zh.tex}",
    r"\title{Scalable Training of Mixture-of-Experts Models with Megatron Core\texorpdfstring{\\[0pt]{\large Technical Report}}{}}": r"\title{Megatron Core 上混合专家模型的可扩展训练\texorpdfstring{\\[0pt]{\large 技术报告}}{}}",
    r"\author{{\vspace{-10pt}\bfseries\large NVIDIA}\footnote{For the complete list of authors, please refer to the Contributions and Acknowledgments section. Corresponding authors: \texttt{\{zijiey, juney, jiajiey\}@nvidia.com}.}}": r"\author{{\vspace{-10pt}\bfseries\large NVIDIA}\footnote{完整作者列表请参见“贡献与致谢”一节。通讯作者：\texttt{\{zijiey, juney, jiajiey\}@nvidia.com}.}}",
}

EXTRA_PREFACE = "\\renewcommand{\\contentsname}{目录}\n\\renewcommand{\\tablename}{表}\n"

RAW_COMMANDS = {
    "cite", "citep", "citet", "citeauthor", "citeyear", "citeyearpar", "nocite",
    "ref", "pageref", "label", "url", "includegraphics", "bibliography",
    "bibliographystyle", "input", "include", "graphicspath", "documentclass",
    "usepackage", "begin", "end", "texttt", "lstinline", "verb", "figref",
    "Figref", "secref", "Secref", "eqref", "Eqref", "algref", "Algref",
    "partref", "Partref", "twofigref", "quadfigref", "twosecrefs", "secrefs",
    "twoalgref", "Twoalgref", "twopartref", "texorpdfstring", "textsuperscript",
    "footnotemark", "multirow", "cline", "toprule", "midrule", "bottomrule",
    "cmidrule", "labelitemi", "labelitemii", "labelitemiii", "labelitemiv",
    "vspace", "hspace", "rule", "raisebox", "makebox", "setlength", "addtolength",
}

COMMAND_ARG_MODES = {
    "section": ["translate"],
    "subsection": ["translate"],
    "subsubsection": ["translate"],
    "paragraph": ["translate"],
    "caption": ["translate"],
    "textbf": ["translate"],
    "textit": ["translate"],
    "emph": ["translate"],
    "footnote": ["translate"],
    "footnotetext": ["translate"],
    "href": ["raw", "translate"],
    "textcolor": ["raw", "translate"],
    "multicolumn": ["raw", "raw", "translate"],
    "fancyhead": ["translate"],
    "thanks": ["translate"],
    "makecell": ["translate"],
}

NO_TRANSLATE_ENVS = {
    "equation", "equation*", "align", "align*", "gather", "gather*", "multline",
    "multline*", "tikzpicture", "asciiart", "lstlisting", "verbatim", "comment",
}
NO_TRANSLATE_PATTERN = r"\\(?:begin|end)\{(?:" + "|".join(re.escape(env) for env in NO_TRANSLATE_ENVS) + r")\}"

SPECIAL_LINES = {
    r"\fancyhead[C]{\footerfont Scalable Training of Mixture-of-Experts Models with Megatron Core}":
    r"\fancyhead[C]{\footerfont Megatron Core 上混合专家模型的可扩展训练}",
}


def has_english(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))


def translate_request(text: str) -> str:
    query = urllib.parse.quote(text)
    url = (
        "https://translate.googleapis.com/translate_a/single"
        f"?client=gtx&sl=en&tl=zh-CN&dt=t&q={query}"
    )
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=20, context=ctx) as response:
        data = json.loads(response.read().decode("utf-8"))
    return "".join(chunk[0] for chunk in data[0])


@lru_cache(maxsize=10000)
def translate_text(text: str) -> str:
    if not text or not has_english(text):
        return text
    if text.strip().startswith("http"):
        return text
    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    core = text.strip()
    if not has_english(core):
        return text
    for attempt in range(6):
        try:
            translated = translate_request(core)
            return leading + translated + trailing
        except Exception:
            if attempt == 5:
                return text
            time.sleep(1.2 * (attempt + 1))
    return text


class LineTranslator:
    def __init__(self):
        self.current_envs = []
        self.in_math_display = False

    def translate(self, line: str) -> str:
        if line in SPECIAL_LINES:
            self._update_states(line)
            return SPECIAL_LINES[line]
        if self._skip_line(line):
            self._update_states(line)
            return line
        result, _ = self._process_span(line, 0, None)
        self._update_states(line)
        return result

    def translate_block(self, block: str) -> str:
        lines = block.splitlines(keepends=True)
        if not lines:
            return block

        if self.current_envs and self.current_envs[-1] in NO_TRANSLATE_ENVS:
            for line in lines:
                self._update_states(line.rstrip('\n'))
            return block

        if re.search(NO_TRANSLATE_PATTERN, block):
            translated = []
            for line in lines:
                if line.endswith('\n'):
                    translated.append(self.translate(line[:-1]) + '\n')
                else:
                    translated.append(self.translate(line))
            return ''.join(translated)

        translated, _ = self._process_span(block, 0, None)
        for line in lines:
            self._update_states(line.rstrip('\n'))
        return translated

    def _skip_line(self, line: str) -> bool:
        stripped = line.strip()
        if not stripped or stripped.startswith('%'):
            return True
        if self.in_math_display:
            return True
        if self.current_envs and self.current_envs[-1] in NO_TRANSLATE_ENVS:
            return True
        return False

    def _update_states(self, line: str) -> None:
        for env in re.findall(r"\\begin\{([^{}]+)\}", line):
            self.current_envs.append(env)
        for env in re.findall(r"\\end\{([^{}]+)\}", line):
            if env in self.current_envs[::-1]:
                idx = len(self.current_envs) - 1 - self.current_envs[::-1].index(env)
                self.current_envs.pop(idx)
        opens = len(re.findall(r"(?<!\\)\\\[", line))
        closes = len(re.findall(r"(?<!\\)\\\]", line))
        if opens > closes:
            self.in_math_display = True
        elif closes and self.in_math_display:
            self.in_math_display = False

    def _process_span(self, text: str, i: int, stop: str | None):
        out = []
        buf = []

        def flush_buffer():
            if buf:
                out.append(translate_text(''.join(buf)))
                buf.clear()

        while i < len(text):
            ch = text[i]
            if stop and ch == stop:
                flush_buffer()
                out.append(ch)
                return ''.join(out), i + 1

            if ch == '%':
                flush_buffer()
                newline = text.find('\n', i)
                if newline == -1:
                    out.append(text[i:])
                    return ''.join(out), len(text)
                out.append(text[i:newline + 1])
                i = newline + 1
                continue
            if ch == '&':
                flush_buffer()
                out.append('&')
                i += 1
                continue

            if text.startswith(r"\(", i):
                flush_buffer()
                end = text.find(r"\)", i + 2)
                if end == -1:
                    out.append(text[i:])
                    return ''.join(out), len(text)
                out.append(text[i:end + 2])
                i = end + 2
                continue
            if text.startswith(r"\[", i):
                flush_buffer()
                end = text.find(r"\]", i + 2)
                if end == -1:
                    out.append(text[i:])
                    return ''.join(out), len(text)
                out.append(text[i:end + 2])
                i = end + 2
                continue
            if ch == '$':
                flush_buffer()
                token, i = self._consume_math(text, i)
                out.append(token)
                continue
            if ch == '{':
                flush_buffer()
                out.append('{')
                inner, i = self._process_span(text, i + 1, '}')
                out.append(inner)
                continue
            if ch == '\\':
                flush_buffer()
                token, i = self._consume_command(text, i)
                out.append(token)
                continue
            buf.append(ch)
            i += 1

        flush_buffer()
        return ''.join(out), i

    def _consume_math(self, text: str, i: int):
        if text.startswith('$$', i):
            end = text.find('$$', i + 2)
            if end == -1:
                return text[i:], len(text)
            return text[i:end + 2], end + 2
        j = i + 1
        while j < len(text):
            if text[j] == '$' and text[j - 1] != '\\':
                return text[i:j + 1], j + 1
            j += 1
        return text[i:], len(text)

    def _consume_command(self, text: str, i: int):
        if i + 1 >= len(text):
            return text[i:], len(text)
        if text[i + 1] in r"\\{}%&#_$~^":
            return text[i:i + 2], i + 2
        if text.startswith(r"\,", i) or text.startswith(r"\;", i) or text.startswith(r"\!", i):
            return text[i:i + 2], i + 2

        j = i + 1
        if text[j].isalpha() or text[j] == '@':
            while j < len(text) and (text[j].isalpha() or text[j] == '@'):
                j += 1
            if j < len(text) and text[j] == '*':
                j += 1
        else:
            j += 1

        cmd_token = text[i:j]
        cmd_name = cmd_token[1:].rstrip('*')
        pieces = [cmd_token]

        while j < len(text) and text[j].isspace() and text[j] != '\n':
            pieces.append(text[j])
            j += 1

        while j < len(text) and text[j] == '[':
            group, j = self._consume_group(text, j, '[', ']')
            pieces.append(group)
            while j < len(text) and text[j].isspace() and text[j] != '\n':
                pieces.append(text[j])
                j += 1

        if cmd_name in RAW_COMMANDS:
            while j < len(text) and text[j] == '{':
                group, j = self._consume_group(text, j, '{', '}')
                pieces.append(group)
                while j < len(text) and text[j].isspace() and text[j] != '\n':
                    pieces.append(text[j])
                    j += 1
            if cmd_name == "begin":
                while j < len(text) and text[j] == '[':
                    group, j = self._consume_group(text, j, '[', ']')
                    pieces.append(group)
                    while j < len(text) and text[j].isspace() and text[j] != '\n':
                        pieces.append(text[j])
                        j += 1
            return ''.join(pieces), j

        modes = COMMAND_ARG_MODES.get(cmd_name)
        if modes:
            for mode in modes:
                if j >= len(text) or text[j] != '{':
                    break
                if mode == 'raw':
                    group, j = self._consume_group(text, j, '{', '}')
                    pieces.append(group)
                else:
                    pieces.append('{')
                    inner, j = self._process_span(text, j + 1, '}')
                    pieces.append(inner)
                while j < len(text) and text[j].isspace() and text[j] != '\n':
                    pieces.append(text[j])
                    j += 1
            return ''.join(pieces), j

        return ''.join(pieces), j

    def _consume_group(self, text: str, i: int, opener: str, closer: str):
        depth = 0
        j = i
        while j < len(text):
            if text[j] == opener:
                depth += 1
            elif text[j] == closer:
                depth -= 1
                if depth == 0:
                    return text[i:j + 1], j + 1
            elif text[j] == '\\' and j + 1 < len(text):
                j += 1
            j += 1
        return text[i:], len(text)


def build_preface(preface: str) -> str:
    for old, new in PREFACE_REPLACEMENTS.items():
        preface = preface.replace(old, new)
    anchor = "\\date{\\today} % Or specify a date like December 2024\n"
    if anchor in preface and EXTRA_PREFACE not in preface:
        preface = preface.replace(anchor, anchor + EXTRA_PREFACE, 1)
    return preface


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("limit", nargs="?", type=int, default=None)
    parser.add_argument("--source", default="main.tex")
    parser.add_argument("--target", default="main_zh.tex")
    parser.add_argument("--body-only", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    source = ROOT / args.source
    target = ROOT / args.target
    max_blocks = args.limit
    text = source.read_text(encoding='utf-8')
    if args.body_only:
        preface = ""
        body = text
    else:
        if r"\begin{document}" not in text:
            raise SystemExit('Could not find \\begin{document} in source file')
        preface, body = text.split(r"\begin{document}", 1)
        preface = build_preface(preface)
    translator = LineTranslator()
    parts = re.split(r"(\n\s*\n)", body)
    units = []
    for idx in range(0, len(parts), 2):
        block = parts[idx]
        sep = parts[idx + 1] if idx + 1 < len(parts) else ""
        if block or sep:
            units.append(block + sep)

    with target.open('w', encoding='utf-8') as fh:
        if args.body_only:
            fh.write("")
        else:
            fh.write(preface + r"\begin{document}" + "\n")
        fh.flush()
        print("wrote preface", flush=True)

        translated_blocks = 0
        batch = ""

        def maybe_report():
            if translated_blocks % 5 == 0:
                fh.flush()
                print(f"translated {translated_blocks} blocks", flush=True)
                time.sleep(0.1)

        def flush_batch():
            nonlocal batch, translated_blocks
            if not batch:
                return
            fh.write(translator.translate_block(batch))
            batch = ""
            translated_blocks += 1
            maybe_report()
        for unit in units:
            if not unit:
                continue
            if re.search(NO_TRANSLATE_PATTERN, unit):
                flush_batch()
                fh.write(translator.translate_block(unit))
                translated_blocks += 1
                maybe_report()
            elif batch and len(batch) + len(unit) > BATCH_TARGET_CHARS:
                flush_batch()
                batch = unit
            else:
                batch += unit

            if max_blocks is not None and translated_blocks >= max_blocks:
                break

        if max_blocks is None or translated_blocks < max_blocks:
            flush_batch()
        if not body.endswith('\n'):
            fh.write('\n')
    print(target.name)


if __name__ == '__main__':
    main()
