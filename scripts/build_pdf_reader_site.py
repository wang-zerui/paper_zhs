#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from paper_catalog import REPO_ROOT, discover_paper_directories, repo_url


OUTPUT_ROOT = REPO_ROOT / "site"
PAPERS_ROOT = OUTPUT_ROOT / "papers"
PDFS_ROOT = OUTPUT_ROOT / "pdfs"
ASSET_SOURCE = REPO_ROOT / "scripts" / "pdf_reader_assets"
ASSET_DEST = OUTPUT_ROOT / "assets"


@dataclass(frozen=True)
class ReaderEntry:
    title: str
    slug: str
    source_path: Path
    repo_path: str
    pdf_file_name: str
    pdf_output_name: str
    detail_file_name: str
    detail_link: str
    pdf_link: str
    github_link: str
    badge: str
    compiler: str | None
    has_build_spec: bool
    has_zh_pdf: bool
    source_archives: tuple[str, ...]
    tracked_file_count: int
    pdf_size_bytes: int
    pdf_size_label: str


def human_size(num_bytes: int) -> str:
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} GB"


def discover_entries() -> list[ReaderEntry]:
    repo_base = repo_url()
    entries: list[ReaderEntry] = []

    for paper in discover_paper_directories():
        selected_pdf = paper.notebook_pdf
        selected_badge = paper.notebook_pdf_badge
        if not selected_pdf or not selected_badge:
            continue

        source_path = REPO_ROOT / selected_pdf
        if not source_path.exists():
            continue

        size_bytes = source_path.stat().st_size
        pdf_output_name = f"{paper.slug}{source_path.suffix.lower()}"
        entries.append(
            ReaderEntry(
                title=paper.title,
                slug=paper.slug,
                source_path=source_path,
                repo_path=selected_pdf,
                pdf_file_name=source_path.name,
                pdf_output_name=pdf_output_name,
                detail_file_name=f"{paper.slug}.html",
                detail_link=f"papers/{paper.slug}.html",
                pdf_link=f"pdfs/{pdf_output_name}",
                github_link=f"{repo_base}/blob/main/{selected_pdf}",
                badge=selected_badge,
                compiler=paper.compiler,
                has_build_spec=paper.has_build_spec,
                has_zh_pdf=paper.has_zh_pdf,
                source_archives=paper.source_archives,
                tracked_file_count=paper.tracked_file_count,
                pdf_size_bytes=size_bytes,
                pdf_size_label=human_size(size_bytes),
            )
        )

    return sorted(entries, key=lambda entry: entry.title.lower())


def clean_output_dir() -> None:
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    PAPERS_ROOT.mkdir(parents=True, exist_ok=True)
    PDFS_ROOT.mkdir(parents=True, exist_ok=True)
    ASSET_DEST.mkdir(parents=True, exist_ok=True)


def copy_assets() -> None:
    for path in ASSET_SOURCE.iterdir():
        destination = ASSET_DEST / path.name
        if path.is_dir():
            shutil.copytree(path, destination)
        else:
            shutil.copy2(path, destination)


def copy_pdfs(entries: list[ReaderEntry]) -> None:
    for entry in entries:
        shutil.copy2(entry.source_path, PDFS_ROOT / entry.pdf_output_name)


def make_document(*, title: str, description: str, body_class: str, body_attrs: dict[str, str], root_prefix: str, content: str, script_path: str) -> str:
    attrs = " ".join(
        f'{html.escape(key)}="{html.escape(value)}"' for key, value in body_attrs.items()
    )
    body_attr_segment = f" {attrs}" if attrs else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{html.escape(description)}">
    <meta name="theme-color" content="#0f172a">
    <title>{html.escape(title)}</title>
    <link rel="icon" href="{root_prefix}assets/icon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="{root_prefix}assets/styles.css">
    <script src="{script_path}" defer></script>
  </head>
  <body class="{html.escape(body_class)}"{body_attr_segment}>
{content}
  </body>
</html>
"""


def render_archive_list(paths: tuple[str, ...]) -> str:
    if not paths:
        return '<li class="muted">无</li>'
    return "\n".join(f'<li><code>{html.escape(path)}</code></li>' for path in paths)


def render_library_cards(entries: list[ReaderEntry]) -> str:
    cards: list[str] = []
    for entry in entries:
        title = html.escape(entry.title)
        repo_path = html.escape(entry.repo_path)
        badge = html.escape(entry.badge)
        github_link = html.escape(entry.github_link)
        cards.append(
            f"""        <article class="paper-card" data-card data-title="{html.escape(entry.title.lower())}" data-path="{html.escape(entry.repo_path.lower())}" data-badge="{html.escape(entry.badge.lower())}" data-slug="{entry.slug}">
          <div class="card-top">
            <span class="badge">{badge}</span>
            <span class="card-size">{entry.pdf_size_label}</span>
          </div>
          <h2>{title}</h2>
          <p class="card-path">{repo_path}</p>
          <div class="card-meta">
            <span>{'含中文版本' if entry.has_zh_pdf else '原文 / 其他'}</span>
            <span>{'已规范化' if entry.has_build_spec else '待补规范'}</span>
            <span>{entry.tracked_file_count} tracked</span>
          </div>
          <div class="card-actions">
            <a class="button primary" href="{entry.detail_link}">开始阅读</a>
            <a class="button" href="{entry.pdf_link}" target="_blank" rel="noopener noreferrer">打开 PDF</a>
            <a class="button" href="{github_link}" target="_blank" rel="noopener noreferrer">源文件</a>
          </div>
        </article>"""
        )
    return "\n".join(cards)


def write_index(entries: list[ReaderEntry]) -> str:
    zh_count = sum(1 for entry in entries if entry.has_zh_pdf)
    total_size = human_size(sum(entry.pdf_size_bytes for entry in entries))
    content = f"""    <header class="page-head shell">
      <section class="hero panel">
        <div>
          <p class="eyebrow">Static / GitHub Pages / PDF Reader</p>
          <h1>把这个仓库变成一个可以随处访问的 PDF 阅读器</h1>
          <p class="lede">
            站点会自动收集仓库里的候选主 PDF，生成一套可直接部署到 GitHub Pages 的静态阅读器：
            有搜索、有移动端目录、有单篇阅读页，也保留原始 PDF 和 GitHub 源文件入口。
          </p>
          <div class="hero-actions">
            <a class="button primary" href="{entries[0].detail_link if entries else 'index.html'}">从第一篇开始</a>
            <button class="button" type="button" data-random-open>随机打开</button>
          </div>
        </div>
        <dl class="stats-grid">
          <div>
            <dt>论文数</dt>
            <dd>{len(entries)}</dd>
          </div>
          <div>
            <dt>含中文 PDF</dt>
            <dd>{zh_count}</dd>
          </div>
          <div>
            <dt>PDF 总体积</dt>
            <dd>{total_size}</dd>
          </div>
          <div>
            <dt>部署方式</dt>
            <dd>GitHub Pages</dd>
          </div>
        </dl>
      </section>
    </header>

    <main class="shell page-main">
      <section class="toolbar panel">
        <label class="search-field">
          <span>搜索论文</span>
          <input data-library-search type="search" placeholder="搜索标题、路径、关键词；按 / 快速聚焦">
        </label>
        <div class="chip-row" role="group" aria-label="过滤器">
          <button class="chip is-active" type="button" data-filter-chip data-filter="all">全部</button>
          <button class="chip" type="button" data-filter-chip data-filter="中文 pdf">中文 PDF</button>
          <button class="chip" type="button" data-filter-chip data-filter="主论文">主论文</button>
          <button class="chip" type="button" data-filter-chip data-filter="pdf">其他 PDF</button>
        </div>
        <p class="toolbar-note" data-library-results>显示 {len(entries)} / {len(entries)} 篇</p>
      </section>

      <section class="library-grid" data-library-grid>
{render_library_cards(entries)}
      </section>
    </main>
"""
    document = make_document(
        title="Paper Reader",
        description="一个可以部署到 GitHub Pages、随处访问的仓库 PDF 阅读器。",
        body_class="library-page",
        body_attrs={"data-page": "index"},
        root_prefix="",
        content=content,
        script_path="assets/app.js",
    )
    output = OUTPUT_ROOT / "index.html"
    output.write_text(document, encoding="utf-8")
    return document


def render_sidebar(entries: list[ReaderEntry], current_slug: str) -> str:
    items: list[str] = []
    for entry in entries:
        active_class = " is-active" if entry.slug == current_slug else ""
        items.append(
            f"""            <li class="sidebar-item{active_class}" data-sidebar-item data-title="{html.escape(entry.title.lower())}" data-path="{html.escape(entry.repo_path.lower())}" data-badge="{html.escape(entry.badge.lower())}">
              <a class="sidebar-link{active_class}" href="../papers/{entry.detail_file_name}">
                <span class="sidebar-title">{html.escape(entry.title)}</span>
                <span class="sidebar-meta">{html.escape(entry.badge)} · {entry.pdf_size_label}</span>
              </a>
            </li>"""
        )
    return "\n".join(items)


def nav_button(entry: ReaderEntry | None, *, label: str, direction: str) -> str:
    if entry is None:
        return f'<span class="button is-disabled" aria-disabled="true">{label}</span>'
    return (
        f'<a class="button" data-nav-{direction} href="../papers/{entry.detail_file_name}">{label}</a>'
    )


def write_reader_pages(entries: list[ReaderEntry]) -> None:
    for index, entry in enumerate(entries):
        prev_entry = entries[index - 1] if index > 0 else None
        next_entry = entries[index + 1] if index + 1 < len(entries) else None
        compiler = entry.compiler or "未标注"
        title = html.escape(entry.title)
        repo_path = html.escape(entry.repo_path)
        badge = html.escape(entry.badge)
        github_link = html.escape(entry.github_link)
        compiler_text = html.escape(compiler)
        content = f"""    <div class="reader-shell">
      <aside class="reader-sidebar" data-reader-sidebar>
        <div class="sidebar-head">
          <a class="sidebar-home" href="../index.html">← 返回书架</a>
          <button class="icon-button mobile-only" type="button" data-drawer-toggle aria-label="关闭目录">✕</button>
        </div>
        <label class="search-field compact">
          <span>筛选目录</span>
          <input data-sidebar-search type="search" placeholder="搜索标题或路径">
        </label>
        <ul class="sidebar-list">
{render_sidebar(entries, entry.slug)}
        </ul>
      </aside>

      <main class="reader-main">
        <header class="reader-header panel">
          <div class="reader-heading">
            <div class="reader-heading-top">
              <button class="button mobile-only" type="button" data-drawer-toggle>目录</button>
              <a class="button" href="../index.html">全部论文</a>
              <span class="badge">{badge}</span>
            </div>
            <h1>{title}</h1>
            <p class="reader-path">{repo_path}</p>
          </div>
          <div class="reader-actions">
            {nav_button(prev_entry, label='上一篇', direction='prev')}
            {nav_button(next_entry, label='下一篇', direction='next')}
            <button class="button" type="button" data-copy-link>复制链接</button>
            <a class="button primary" href="../{entry.pdf_link}" target="_blank" rel="noopener noreferrer">打开 PDF</a>
            <a class="button" href="{github_link}" target="_blank" rel="noopener noreferrer">查看源文件</a>
          </div>
        </header>

        <section class="viewer-panel panel">
          <iframe
            class="viewer-frame"
            src="../{entry.pdf_link}#view=FitH"
            title="{title} PDF viewer"
            loading="lazy"
          ></iframe>
        </section>

        <section class="info-grid">
          <article class="info-card panel">
            <h2>阅读提示</h2>
            <ul>
              <li>浏览器不支持内嵌 PDF 时，可点击上方 <strong>打开 PDF</strong>。</li>
              <li>按 <kbd>/</kbd> 可以快速聚焦搜索框；按 <kbd>j</kbd> / <kbd>k</kbd> 可切换下一篇 / 上一篇。</li>
              <li>手机端可通过“目录”按钮打开左侧论文列表。</li>
            </ul>
          </article>

          <article class="info-card panel">
            <h2>文件信息</h2>
            <dl class="meta-list">
              <div><dt>仓库路径</dt><dd><code>{repo_path}</code></dd></div>
              <div><dt>部署后文件</dt><dd><code>{entry.pdf_link}</code></dd></div>
              <div><dt>PDF 大小</dt><dd>{entry.pdf_size_label}</dd></div>
              <div><dt>编译器</dt><dd>{compiler_text}</dd></div>
              <div><dt>规范状态</dt><dd>{'已存在 00README.json' if entry.has_build_spec else '尚未补齐 00README.json'}</dd></div>
            </dl>
          </article>

          <article class="info-card panel">
            <h2>相关资源</h2>
            <ul>
              <li><a href="../{entry.pdf_link}" target="_blank" rel="noopener noreferrer">直接打开 PDF</a></li>
              <li><a href="{github_link}" target="_blank" rel="noopener noreferrer">在 GitHub 查看文件</a></li>
              <li><a href="../index.html">返回整站书架</a></li>
            </ul>
          </article>

          <article class="info-card panel">
            <h2>源码包</h2>
            <ul class="archive-list">
{render_archive_list(entry.source_archives)}
            </ul>
          </article>
        </section>
      </main>
    </div>
    <div class="backdrop" data-backdrop data-drawer-toggle></div>
"""
        document = make_document(
            title=f"{entry.title} · Paper Reader",
            description=f"在浏览器中阅读 {entry.title}，并可直接打开 PDF 或跳转 GitHub 源文件。",
            body_class="reader-page",
            body_attrs={"data-page": "reader", "data-current-slug": entry.slug},
            root_prefix="../",
            content=content,
            script_path="../assets/app.js",
        )
        (PAPERS_ROOT / entry.detail_file_name).write_text(document, encoding="utf-8")


def write_catalog(entries: list[ReaderEntry]) -> None:
    catalog = [
        {
            "title": entry.title,
            "slug": entry.slug,
            "repo_path": entry.repo_path,
            "pdf_output_name": entry.pdf_output_name,
            "detail_link": entry.detail_link,
            "pdf_link": entry.pdf_link,
            "github_link": entry.github_link,
            "badge": entry.badge,
            "compiler": entry.compiler,
            "has_build_spec": entry.has_build_spec,
            "has_zh_pdf": entry.has_zh_pdf,
            "source_archives": list(entry.source_archives),
            "tracked_file_count": entry.tracked_file_count,
            "pdf_size_bytes": entry.pdf_size_bytes,
            "pdf_size_label": entry.pdf_size_label,
        }
        for entry in entries
    ]
    (OUTPUT_ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_support_files(index_document: str) -> None:
    (OUTPUT_ROOT / ".nojekyll").write_text("\n", encoding="utf-8")
    (OUTPUT_ROOT / "404.html").write_text(index_document, encoding="utf-8")


def main() -> None:
    entries = discover_entries()
    clean_output_dir()
    copy_assets()
    copy_pdfs(entries)
    index_document = write_index(entries)
    write_reader_pages(entries)
    write_catalog(entries)
    write_support_files(index_document)
    print(f"Generated {len(entries)} reader pages in {OUTPUT_ROOT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
