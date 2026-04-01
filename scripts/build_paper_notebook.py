#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from paper_catalog import BOOK_ROOT, REPO_ROOT, discover_paper_directories, repo_url


PAPERS_DIR = BOOK_ROOT / "papers"
THEME_DIR = BOOK_ROOT / "theme" / "styles"


@dataclass(frozen=True)
class NotebookEntry:
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


def discover_entries() -> list[NotebookEntry]:
    entries: list[NotebookEntry] = []
    for paper in discover_paper_directories():
        selected_pdf = paper.notebook_pdf or paper.preferred_pdf
        selected_badge = paper.notebook_pdf_badge or paper.preferred_pdf_badge
        if not selected_pdf or not selected_badge:
            continue

        source_path = REPO_ROOT / selected_pdf
        detail_markdown = f"{paper.slug}.md"
        pdf_output_name = f"{paper.slug}{source_path.suffix.lower()}"
        entries.append(
            NotebookEntry(
                title=paper.title,
                slug=paper.slug,
                source_path=source_path,
                repo_path=selected_pdf,
                pdf_file_name=source_path.name,
                pdf_output_name=pdf_output_name,
                detail_markdown=detail_markdown,
                detail_link=f"./papers/{detail_markdown}",
                pdf_link=f"./pdfs/{pdf_output_name}",
                badge=selected_badge,
            )
        )
    return entries


def format_cards(entries: Iterable[NotebookEntry], repo_base: str) -> str:
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


def write_readme(entries: list[NotebookEntry], repo_base: str) -> None:
    cards_html = format_cards(entries, repo_base)
    content = f"""# Paper Notebook

> 一个面向论文 PDF 阅读的 GitBook notebook。内容由仓库中论文目录里的候选主 PDF 自动生成。

<section class="notebook-hero">
  <div>
    <p class="eyebrow">GitHub Pages / HonKit / PDF notebook</p>
    <h1>在一个侧边栏里浏览这批论文</h1>
    <p class="lede">这里会自动收集仓库中每个论文目录的主 PDF，并为它生成单独的阅读页、仓库源文件链接和直接打开 PDF 的入口。</p>
  </div>
  <dl class="stats">
    <div><dt>Papers</dt><dd>{len(entries)}</dd></div>
    <div><dt>Source</dt><dd>Workspace PDFs</dd></div>
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


def write_summary(entries: list[NotebookEntry]) -> None:
    lines = ["# Summary", "", "* [首页](README.md)"]
    for entry in entries:
        lines.append(f"* [{entry.title}](papers/{entry.detail_markdown})")
    (BOOK_ROOT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_paper_pages(entries: list[NotebookEntry], repo_base: str) -> None:
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


def copy_pdfs(entries: list[NotebookEntry], destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        shutil.copy2(entry.source_path, destination / entry.pdf_output_name)


def write_catalog(entries: list[NotebookEntry]) -> None:
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
