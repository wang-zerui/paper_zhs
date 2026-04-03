#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

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


def raw_file_url(repo_base: str, repo_path: str) -> str:
    encoded_path = quote(repo_path, safe="/")
    if repo_base.startswith("https://github.com/"):
        raw_base = repo_base.replace("https://github.com/", "https://raw.githubusercontent.com/", 1)
        return f"{raw_base}/main/{encoded_path}"
    return f"{repo_base}/blob/main/{encoded_path}"


def format_cards(entries: list[NotebookEntry], repo_base: str) -> str:
    lines: list[str] = []
    for entry in entries:
        repo_link = f"{repo_base}/blob/main/{entry.repo_path}"
        pdf_link = raw_file_url(repo_base, entry.repo_path)
        lines.append(
            f"- [{entry.title}]({entry.detail_link}) · {entry.badge} · [PDF]({pdf_link}) · [GitHub]({repo_link})"
        )
    return "\n".join(lines)


def write_readme(entries: list[NotebookEntry], repo_base: str) -> None:
    cards_markdown = format_cards(entries, repo_base)
    content = f"""# Paper Notebook

> 一个面向 GitBook Sync 的论文目录。内容由仓库中论文目录里的候选主 PDF 自动生成。

## Overview

- Papers: **{len(entries)}**
- Source: 仓库里的 tracked PDF
- Mode: GitBook Sync / GitHub repo integration

## 使用方式

1. 在 GitBook 中连接这个 GitHub 仓库。
2. 将文档根目录设置为 `notebook/`。
3. 左侧目录进入单篇论文页，点击文件块或 PDF 链接阅读。

> GitBook 更适合做“文档索引 + PDF 打开入口”；PDF 会通过文件块或链接打开，而不是像静态站那样用 iframe 内嵌阅读。

## Library

{cards_markdown}
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
        raw_pdf_link = raw_file_url(repo_base, entry.repo_path)
        page = f"""# {entry.title}

> {entry.badge} · `{entry.repo_path}`

{{% file src="{raw_pdf_link}" %}}
{entry.title} PDF
{{% endfile %}}

## Notes

- 源文件：`{entry.repo_path}`
- PDF 直链：[{entry.pdf_file_name}]({raw_pdf_link})
- 仓库页：[{repo_link}]({repo_link})
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
    parser = argparse.ArgumentParser(description="Generate GitBook-friendly notebook pages for tracked paper PDFs.")
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
