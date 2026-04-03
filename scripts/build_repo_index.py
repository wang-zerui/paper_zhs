#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from paper_catalog import REPO_ROOT, discover_paper_directories, repo_url, top_level_archives


INDEX_JSON = REPO_ROOT / "repo_index.json"
INDEX_MD = REPO_ROOT / "REPO_INDEX.md"


def human_size(num_bytes: int) -> str:
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GB"


def summarize(papers: list) -> dict[str, int]:
    return {
        "paper_dirs": len(papers),
        "with_build_spec": sum(1 for paper in papers if paper.has_build_spec),
        "with_preferred_pdf": sum(1 for paper in papers if paper.preferred_pdf),
        "with_zh_pdf": sum(1 for paper in papers if paper.has_zh_pdf),
        "with_source_archives": sum(1 for paper in papers if paper.source_archives),
        "with_tracked_files": sum(1 for paper in papers if paper.tracked_file_count > 0),
        "local_only_dirs": sum(1 for paper in papers if paper.tracked_file_count == 0),
    }


def write_json(papers: list) -> None:
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repo_url": repo_url(),
        "summary": summarize(papers),
        "papers": [asdict(paper) for paper in papers],
        "standalone_archives": [
            {
                "path": path.relative_to(REPO_ROOT).as_posix(),
                "size_bytes": path.stat().st_size,
            }
            for path in top_level_archives()
        ],
    }
    INDEX_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def format_bool(value: bool) -> str:
    return "✅" if value else "—"


def basename(path: str | None) -> str:
    return Path(path).name if path else "—"


def archives_cell(paths: tuple[str, ...]) -> str:
    if not paths:
        return "—"
    return "<br>".join(Path(path).name for path in paths)


def write_markdown(papers: list) -> None:
    stats = summarize(papers)
    missing_spec = [paper.name for paper in papers if not paper.has_build_spec]
    local_only = [paper.name for paper in papers if paper.tracked_file_count == 0]
    notebook_missing = [paper.name for paper in papers if not paper.preferred_pdf]

    lines = [
        "# Repo Index",
        "",
        f"> 自动生成于 {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}。这个索引面向本地工作区，会扫描所有论文目录；`notebook/` 默认使用每个目录里的候选主 PDF。",
        "",
        "## Summary",
        "",
        f"- 论文目录：{stats['paper_dirs']}",
        f"- 含 `00README.json`：{stats['with_build_spec']}",
        f"- 有本地候选 PDF：{stats['with_preferred_pdf']}",
        f"- 含中文 PDF：{stats['with_zh_pdf']}",
        f"- 带源码包：{stats['with_source_archives']}",
        f"- 含 tracked files 的目录：{stats['with_tracked_files']}",
        f"- 纯本地目录（tracked files = 0）：{stats['local_only_dirs']}",
        "",
        "## Triage",
        "",
        f"- 缺少 `00README.json`：{', '.join(missing_spec) if missing_spec else '无'}",
        f"- 缺少候选 PDF 的目录：{', '.join(notebook_missing) if notebook_missing else '无'}",
        f"- 当前纯本地目录：{', '.join(local_only) if local_only else '无'}",
        "",
        "## Papers",
        "",
        "| 目录 | 标题 | 规范 | 主 tex | 本地 PDF | Tracked PDF | 中文 PDF | 源码包 | tracked files |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | ---: |",
    ]

    for paper in papers:
        lines.append(
            "| {name} | {title} | {spec} | {top_tex} | {preferred_pdf} | {notebook_pdf} | {zh_pdf} | {archives} | {tracked} |".format(
                name=paper.name,
                title=paper.title,
                spec=format_bool(paper.has_build_spec),
                top_tex=paper.top_level_tex or "—",
                preferred_pdf=basename(paper.preferred_pdf),
                notebook_pdf=basename(paper.notebook_pdf),
                zh_pdf=format_bool(paper.has_zh_pdf),
                archives=archives_cell(paper.source_archives),
                tracked=paper.tracked_file_count,
            )
        )

    lines.extend(
        [
            "",
            "## Standalone source archives",
            "",
            "| 文件 | 大小 |",
            "| --- | ---: |",
        ]
    )

    for archive in top_level_archives():
        lines.append(f"| {archive.name} | {human_size(archive.stat().st_size)} |")

    lines.extend(
        [
            "",
            "## Commands",
            "",
            "- 刷新仓库索引：`python3 scripts/build_repo_index.py`",
            "- 构建新的静态 PDF 阅读器：`python3 scripts/build_pdf_reader_site.py`",
            "- 刷新 notebook 源文件：`python3 scripts/build_paper_notebook.py`",
            "- 构建 notebook 站点：`npm run build:notebook`",
            "",
            "> 需要完整字段时，请查看同目录下的 `repo_index.json`。",
        ]
    )

    INDEX_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    papers = discover_paper_directories()
    write_json(papers)
    write_markdown(papers)


if __name__ == "__main__":
    main()
