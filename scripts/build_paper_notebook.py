#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOT = REPO_ROOT / "notebook"
PAPERS_DIR = BOOK_ROOT / "papers"
THEME_DIR = BOOK_ROOT / "theme" / "styles"
DEFAULT_REPO_URL = "https://github.com/wang-zerui/paper_zhs"
IGNORED_TOP_LEVEL = {".git", ".github", ".vscode", ".argos_config", "pdf", "_book", "notebook"}
IGNORED_DIR_NAMES = {
    "figures",
    "figs",
    "imgs",
    "image",
    "images",
    "logo",
    "logos",
    "chapters",
    "ims",
    "assets",
}
BAD_NAME_TOKENS = {
    "badge",
    "badges",
    "logo",
    "poster",
    "appendix",
    "supp",
    "supplementary",
}
PRIMARY_NAME_TOKENS = {
    "main",
    "paper",
    "arxiv",
    "conference",
    "reference",
    "viewer",
    "latex",
    "turbo",
}
TITLE_OVERRIDES = {
    "2307.08691": "FlashAttention-2",
    "2501.01005": "FlashInfer",
    "2601.06002": "Paper 2601.06002",
    "2602.15322": "Google Main",
    "2602.15763": "GLM-5",
    "BaichuanM3": "Baichuan M3",
    "ByteCheckpoint": "ByteCheckpoint",
    "Elastic Attention": "Elastic Attention",
    "GatedAttn": "GatedAttn",
    "LLM-viewer": "LLM Viewer",
    "MinerU_latex_RA11338001-DSPGB200-ReferenceArch_2027704574230851584": "MinerU Reference Architecture",
    "Pangu_ultra": "Pangu Ultra",
    "Step3.5": "Step3.5 Turbo 2026",
}


@dataclass(frozen=True)
class PaperEntry:
    title: str
    slug: str
    source_path: Path
    repo_path: str
    pdf_file_name: str
    pdf_output_name: str
    detail_markdown: str
    detail_link: str
    pdf_link: str
    badge: str


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def repo_url() -> str:
    try:
        remote = run_git("remote", "get-url", "origin")
    except subprocess.CalledProcessError:
        return DEFAULT_REPO_URL
    if remote.startswith("git@github.com:"):
        return "https://github.com/" + remote.removeprefix("git@github.com:").removesuffix(".git")
    if remote.startswith("https://github.com/"):
        return remote.removesuffix(".git")
    return DEFAULT_REPO_URL


def tracked_pdfs() -> list[Path]:
    output = run_git("ls-files", "*.pdf")
    paths = [Path(line) for line in output.splitlines() if line.strip()]
    return [path for path in paths if path.parts and path.parts[0] not in IGNORED_TOP_LEVEL]


def score_pdf(path: Path) -> int:
    parts = path.parts
    base = path.name.lower()
    stem = path.stem.lower()
    score = 0

    if len(parts) == 2:
        score += 90
    elif len(parts) == 3 and parts[1].lower() == "src":
        score += 60
    else:
        score -= 80

    if any(part.lower() in IGNORED_DIR_NAMES for part in parts[1:-1]):
        score -= 160

    if any(token in stem for token in BAD_NAME_TOKENS):
        score -= 220

    if "zh" in stem:
        score += 120

    if any(token in stem for token in PRIMARY_NAME_TOKENS):
        score += 110

    if re.fullmatch(r"\d+\.\d+", parts[0]):
        score += 20

    normalized_top = re.sub(r"[\W_]+", "", parts[0].lower())
    normalized_stem = re.sub(r"[\W_]+", "", stem)
    if normalized_top and normalized_top in normalized_stem:
        score += 20

    return score


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "paper"


def humanize_name(name: str) -> str:
    if name in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[name]
    if re.fullmatch(r"\d+\.\d+", name):
        return f"Paper {name}"
    text = name.replace("_", " ").replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text.title()


def pdf_badge(path: Path) -> str:
    stem = path.stem.lower()
    if "zh" in stem:
        return "中文 PDF"
    if "main" in stem or "paper" in stem:
        return "主论文"
    return "PDF"


def discover_entries() -> list[PaperEntry]:
    grouped: dict[str, list[Path]] = {}
    for pdf in tracked_pdfs():
        grouped.setdefault(pdf.parts[0], []).append(pdf)

    entries: list[PaperEntry] = []
    for top_level, pdfs in sorted(grouped.items()):
        best = max(pdfs, key=score_pdf)
        if score_pdf(best) < 0:
            continue

        title = humanize_name(top_level)
        slug = slugify(top_level)
        detail_markdown = f"{slug}.md"
        pdf_output_name = f"{slug}{best.suffix.lower()}"
        entries.append(
            PaperEntry(
                title=title,
                slug=slug,
                source_path=REPO_ROOT / best,
                repo_path=best.as_posix(),
                pdf_file_name=best.name,
                pdf_output_name=pdf_output_name,
                detail_markdown=detail_markdown,
                detail_link=f"./papers/{detail_markdown}",
                pdf_link=f"./pdfs/{pdf_output_name}",
                badge=pdf_badge(best),
            )
        )
    return entries


def format_cards(entries: Iterable[PaperEntry], repo_base: str) -> str:
    cards = []
    for entry in entries:
        repo_link = f"{repo_base}/blob/main/{entry.repo_path}"
        cards.append(
            f"""<a class="paper-card" href="{entry.detail_link}">
  <span class="paper-card__badge">{html.escape(entry.badge)}</span>
  <strong>{html.escape(entry.title)}</strong>
  <span>{html.escape(entry.repo_path)}</span>
  <span class="paper-card__actions">
    <span>Notebook</span>
    <span>PDF</span>
    <span>GitHub</span>
  </span>
  <span class="paper-card__links">
    <span>{html.escape(entry.detail_link)}</span>
    <span>{html.escape(entry.pdf_link)}</span>
    <span>{html.escape(repo_link)}</span>
  </span>
</a>"""
        )
    return "\n".join(cards)


def write_readme(entries: list[PaperEntry], repo_base: str) -> None:
    cards_html = format_cards(entries, repo_base)
    content = f"""# Paper Notebook

> 一个面向论文 PDF 阅读的 GitBook notebook。内容由仓库中已跟踪的主论文 PDF 自动生成。

<section class="notebook-hero">
  <div>
    <p class="eyebrow">GitHub Pages / HonKit / PDF notebook</p>
    <h1>在一个侧边栏里浏览这批论文</h1>
    <p class="lede">这里会自动收集仓库中每个论文目录的主 PDF，并为它生成单独的阅读页、仓库源文件链接和直接打开 PDF 的入口。</p>
  </div>
  <dl class="stats">
    <div><dt>Papers</dt><dd>{len(entries)}</dd></div>
    <div><dt>Source</dt><dd>Tracked PDFs</dd></div>
    <div><dt>Deploy</dt><dd>GitHub Pages</dd></div>
  </dl>
</section>

## Library

<div class="paper-grid">
{cards_html}
</div>

## 使用方式

1. 左侧目录直接进入单篇论文阅读页。
2. 每个阅读页都内嵌浏览器 PDF viewer，同时保留原始 PDF 打开入口。
3. 新增论文后运行 `python3 scripts/build_paper_notebook.py`，再执行 `npm run build:notebook` 即可刷新站点。
"""
    (BOOK_ROOT / "README.md").write_text(content, encoding="utf-8")


def write_summary(entries: list[PaperEntry]) -> None:
    lines = ["# Summary", "", "* [首页](README.md)"]
    for entry in entries:
        lines.append(f"* [{entry.title}](papers/{entry.detail_markdown})")
    (BOOK_ROOT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_paper_pages(entries: list[PaperEntry], repo_base: str) -> None:
    if PAPERS_DIR.exists():
        for markdown_file in PAPERS_DIR.glob("*.md"):
            markdown_file.unlink()
    else:
        PAPERS_DIR.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        repo_link = f"{repo_base}/blob/main/{entry.repo_path}"
        page = f"""# {entry.title}

<section class="viewer-shell">
  <div class="viewer-toolbar">
    <span class="viewer-badge">{html.escape(entry.badge)}</span>
    <span class="viewer-path">{html.escape(entry.repo_path)}</span>
    <a href="../pdfs/{entry.pdf_output_name}" target="_blank" rel="noopener noreferrer">Open PDF</a>
    <a href="{repo_link}" target="_blank" rel="noopener noreferrer">View On GitHub</a>
  </div>
  <iframe
    class="viewer-frame"
    src="../pdfs/{entry.pdf_output_name}#view=FitH"
    title="{html.escape(entry.title)} PDF viewer"
    loading="lazy"
  ></iframe>
</section>

## Notes

- 源文件：`{entry.repo_path}`
- 直链：[`../pdfs/{entry.pdf_output_name}`](../pdfs/{entry.pdf_output_name})
- 仓库页：[{repo_link}]({repo_link})

> 如果浏览器不支持内嵌 PDF，点击上方 `Open PDF` 即可在新标签页打开。
"""
        (PAPERS_DIR / entry.detail_markdown).write_text(page, encoding="utf-8")


def copy_pdfs(entries: list[PaperEntry], destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        shutil.copy2(entry.source_path, destination / entry.pdf_output_name)


def write_catalog(entries: list[PaperEntry]) -> None:
    catalog = [
        {
            "title": entry.title,
            "slug": entry.slug,
            "repo_path": entry.repo_path,
            "pdf_file_name": entry.pdf_file_name,
            "pdf_output_name": entry.pdf_output_name,
            "badge": entry.badge,
        }
        for entry in entries
    ]
    (BOOK_ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def ensure_layout_dirs() -> None:
    THEME_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a HonKit notebook for tracked paper PDFs.")
    parser.add_argument("--copy-pdfs-to", type=Path, help="Copy selected PDFs into the target directory.")
    args = parser.parse_args()

    ensure_layout_dirs()
    entries = discover_entries()
    repo_base = repo_url()
    write_readme(entries, repo_base)
    write_summary(entries)
    write_paper_pages(entries, repo_base)
    write_catalog(entries)
    if args.copy_pdfs_to:
        destination = args.copy_pdfs_to
        if not destination.is_absolute():
            destination = REPO_ROOT / destination
        copy_pdfs(entries, destination)


if __name__ == "__main__":
    main()
