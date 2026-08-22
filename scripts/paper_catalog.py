#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOT = REPO_ROOT / "notebook"
DEFAULT_REPO_URL = "https://github.com/wang-zerui/paper_zhs"
INFRA_TOP_LEVEL = {
    ".git",
    ".github",
    ".vscode",
    ".argos_config",
    ".cache",
    ".local",
    ".vendor",
    "notebook",
    "pdf",
    "site",
    "_book",
    "scripts",
    "node_modules",
    "rong_chen_pub_downloads",
}
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
    "artworks",
    "tables",
    "table",
    "auto",
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
    "2203.15556": "Paper 2203.15556",
    "2307.08691": "FlashAttention-2",
    "2412.17246": "Paper 2412.17246",
    "2203-15556": "Paper 2203.15556",
    "training-compute-optimal-large-language-models": "Training Compute-Optimal Large Language Models",
    "2501.01005": "FlashInfer",
    "2506.10470": "Paper 2506.10470",
    "2412-17246": "Paper 2412.17246",
    "blitzscale": "BlitzScale",
    "2506-10470": "Paper 2506.10470",
    "td-pipe": "TD-Pipe",
    "2510.04371": "Paper 2510.04371",
    "2510-04371": "Paper 2510.04371",
    "speculative-actions-lossless-framework-for-faster-agentic-systems": "Speculative Actions: A Lossless Framework for Faster Agentic Systems",
    "2601.06002": "Paper 2601.06002",
    "2602.15322": "Google Main",
    "2602.15763": "GLM-5",
    "2603.07685": "Scalable Training of Mixture-of-Experts Models with Megatron Core",
    "2603.15202": "Paper 2603.15202",
    "2603-15202": "Paper 2603.15202",
    "ICLR_camera_ready_v0": "FlexRL: Scaling VLM RL Training via Efficient Load Balancing",
    "lmetric": "LMetric",
    "ARL-Tangram": "ARL Tangram",
    "arl-tangram": "ARL Tangram",
    "BaichuanM3": "Baichuan M3",
    "baichuan-m3": "Baichuan M3",
    "ByteCheckpoint": "ByteCheckpoint",
    "byte-checkpoint": "ByteCheckpoint",
    "Colossal-Auto": "Colossal Auto",
    "colossal-auto": "Colossal Auto",
    "computerrl": "ComputerRL: Scaling End-to-End Online Reinforcement Learning for Computer Use Agents",
    "CONCUR": "CONCUR",
    "concur": "CONCUR",
    "EAGLE-3": "EAGLE-3",
    "eagle-3": "EAGLE-3",
    "EAGLE Speculative Sampling Requires Rethinking Feature Uncertainty": "EAGLE Speculative Sampling Requires Rethinking Feature Uncertainty",
    "eagle-feature-uncertainty": "EAGLE Speculative Sampling Requires Rethinking Feature Uncertainty",
    "Elastic Attention": "Elastic Attention",
    "elastic-attention": "Elastic Attention",
    "FA2": "FlashAttention-2",
    "flashattention-2": "FlashAttention-2",
    "FastMTP Accelerating LLM Inference with Enhanced Multi-Token Prediction": "FastMTP",
    "fastmtp": "FastMTP",
    "FlashAttention4": "FlashAttention4",
    "flashattention-4": "FlashAttention4",
    "FlashInfe": "FlashInfer",
    "flashinfer": "FlashInfer",
    "GatedAttn": "GatedAttn",
    "gated-attn": "GatedAttn",
    "GLM5": "GLM5",
    "glm-5": "GLM5",
    "gui-actor": "GUI-Actor",
    "HyperParallel": "HyperParallel",
    "hyper-parallel": "HyperParallel",
    "DualPath": "DualPath",
    "dualpath": "DualPath",
    "darwin-godel-machine": "Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents",
    "KVPR": "KVPR",
    "kvpr": "KVPR",
    "LLM-viewer": "LLM Viewer",
    "llm-viewer": "LLM Viewer",
    "MinerU_latex_RA11338001-DSPGB200-ReferenceArch_2027704574230851584": "MinerU Reference Architecture",
    "nvidia-superpod": "NVIDIA SuperPOD",
    "Magma": "Magma",
    "magma": "Magma",
    "megascale-moe": "MegaScale-MoE",
    "Mirage": "Mirage",
    "mirage": "Mirage",
    "MPK": "MPK",
    "mpk": "MPK",
    "Multi-stage Flow Scheduling for LLM Serving": "Multi-stage Flow Scheduling for LLM Serving",
    "multi-stage-flow-scheduling": "Multi-stage Flow Scheduling for LLM Serving",
    "NVIDIASuperPOD": "NVIDIA SuperPOD",
    "Pangu_ultra": "Pangu Ultra",
    "pangu-ultra": "Pangu Ultra",
    "PhyPrompt": "PhyPrompt",
    "phyprompt": "PhyPrompt",
    "PivotRL": "PivotRL",
    "pivot-rl": "PivotRL",
    "RollArt": "RollArt",
    "roll-art": "RollArt",
    "SageSched": "SageSched",
    "sage-sched": "SageSched",
    "Speculative Actions：用于更快智能体系统的无损框架": "Speculative Actions",
    "speculative-actions": "Speculative Actions",
    "Step-GUI": "Step-GUI",
    "step-gui": "Step-GUI",
    "Step3.5": "Step3.5 Turbo 2026",
    "step-3-5": "Step3.5 Turbo 2026",
    "ThunderAgent": "ThunderAgent",
    "thunderagent": "ThunderAgent",
    "The Molecular Structure of Thought: Mapping the Topology of Long Chain-of-Thought Reasonin": "The Molecular Structure of Thought",
    "molecular-structure-of-thought": "The Molecular Structure of Thought",
    "The Workload-Router-Pool Architecture for LLM Inference Optimization: A Vision Paper from the vLLM Semantic Router Project": "Workload Router Pool",
    "workload-router-pool": "Workload Router Pool",
    "waferllm": "WaferLLM: Large Language Model Inference at Wafer Scale",
    "VISTA-Gym": "VISTA-Gym",
    "vista-gym": "VISTA-Gym",
    "Why Low-Precision Transformer Training Fails - An Analysis on Flash Attention": "Why Low-Precision Transformer Training Fails",
    "low-precision-flash-attention": "Why Low-Precision Transformer Training Fails",
    "enterpriseops-gym": "EnterpriseOps-Gym: Environments and Evaluations for Stateful Agentic Planning and Tool Use in Enterprise Settings",
    "tlt-adaptive-drafter": "Taming the Long-Tail: Efficient Reasoning RL Training with Adaptive Drafter",
    "clawmark": "ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents",
    "agentic-harness-engineering": "Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses",
}
ARCHIVE_ALIASES = {
    "td-pipe": (
        "2506.10470",
    ),
    "workload-router-pool": (
        "The Workload-Router-Pool Architecture for LLM Inference Optimization: A Vision Paper from the vLLM Semantic Router Project",
    ),
}


@dataclass(frozen=True)
class PaperDirectory:
    name: str
    title: str
    slug: str
    repo_dir: str
    has_build_spec: bool
    top_level_tex: str | None
    compiler: str | None
    preferred_pdf: str | None
    preferred_pdf_badge: str | None
    notebook_pdf: str | None
    notebook_pdf_badge: str | None
    has_zh_tex: bool
    has_zh_pdf: bool
    tex_count: int
    pdf_count: int
    source_archives: tuple[str, ...]
    tracked_file_count: int


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


@lru_cache(maxsize=1)
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


@lru_cache(maxsize=1)
def tracked_files() -> frozenset[str]:
    try:
        output = run_git("ls-files")
    except subprocess.CalledProcessError:
        return frozenset()
    return frozenset(line for line in output.splitlines() if line.strip())


@lru_cache(maxsize=1)
def tracked_pdfs() -> frozenset[str]:
    return frozenset(path for path in tracked_files() if path.lower().endswith(".pdf"))


@lru_cache(maxsize=1)
def tracked_top_level_counts() -> dict[str, int]:
    counts: defaultdict[str, int] = defaultdict(int)
    for path in tracked_files():
        counts[Path(path).parts[0]] += 1
    return dict(counts)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "paper"


def humanize_name(name: str) -> str:
    if name in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[name]
    if re.fullmatch(r"\d+\.\d+", name):
        return f"Paper {name}"
    if re.fullmatch(r"\d+-\d+", name):
        return f"Paper {name.replace('-', '.')}"
    text = re.sub(r"\s+", " ", name.replace("_", " ").replace("-", " ")).strip()
    if any(ord(ch) > 127 for ch in text) or any(ch.isupper() for ch in name):
        return text
    return text.title()


def pdf_badge(path: Path | str) -> str:
    stem = Path(path).stem.lower()
    if "zh" in stem:
        return "中文 PDF"
    if "main" in stem or "paper" in stem:
        return "主论文"
    return "PDF"


def score_pdf(path: Path) -> int:
    parts = path.parts
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

    normalized_top = normalize_name(parts[0])
    normalized_stem = normalize_name(stem)
    if normalized_top and normalized_top in normalized_stem:
        score += 20

    return score


def normalize_name(text: str) -> str:
    return re.sub(r"[\W_]+", "", text).lower()


def archive_key(name: str) -> str:
    base = name
    for suffix in (".tar.gz", ".tar"):
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    base = re.sub(r"[-_]?source$", "", base, flags=re.IGNORECASE)
    return normalize_name(base)


@lru_cache(maxsize=1)
def top_level_archives() -> tuple[Path, ...]:
    archives = []
    for path in REPO_ROOT.iterdir():
        if path.is_file() and (path.name.endswith(".tar") or path.name.endswith(".tar.gz")):
            archives.append(path)
    return tuple(sorted(archives, key=lambda item: item.name.lower()))


def list_paper_directories() -> list[Path]:
    paper_dirs: list[Path] = []
    for path in sorted(REPO_ROOT.iterdir(), key=lambda item: item.name.lower()):
        if not path.is_dir():
            continue
        if path.name.startswith("."):
            continue
        if path.name in INFRA_TOP_LEVEL:
            continue
        paper_dirs.append(path)
    return paper_dirs


def parse_build_spec(paper_dir: Path) -> tuple[bool, str | None, str | None]:
    spec_path = paper_dir / "00README.json"
    if not spec_path.exists():
        return False, None, None
    try:
        data = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return True, None, None

    top_level_tex = None
    for item in data.get("sources", []):
        if isinstance(item, dict) and item.get("usage") == "toplevel":
            candidate = item.get("filename")
            if isinstance(candidate, str):
                top_level_tex = candidate
                break

    compiler = None
    process = data.get("process")
    if isinstance(process, dict):
        value = process.get("compiler")
        if isinstance(value, str):
            compiler = value
    return True, top_level_tex, compiler


def candidate_pdfs(paper_dir: Path, tracked_only: bool = False) -> list[Path]:
    candidates: list[Path] = []
    for path in paper_dir.rglob("*.pdf"):
        rel = path.relative_to(REPO_ROOT)
        rel_str = rel.as_posix()
        if tracked_only and rel_str not in tracked_pdfs():
            continue
        candidates.append(rel)
    return candidates


def choose_best_pdf(paper_dir: Path, tracked_only: bool = False) -> Path | None:
    candidates = candidate_pdfs(paper_dir, tracked_only=tracked_only)
    if not candidates:
        return None
    best = max(candidates, key=score_pdf)
    if score_pdf(best) < 0:
        return None
    return best


def collect_source_archives(paper_dir: Path) -> tuple[str, ...]:
    archives: list[str] = []
    for path in sorted(paper_dir.glob("*.tar*"), key=lambda item: item.name.lower()):
        if path.name.endswith(".tar") or path.name.endswith(".tar.gz"):
            archives.append(path.relative_to(REPO_ROOT).as_posix())

    candidate_keys = {normalize_name(paper_dir.name)}
    for alias in ARCHIVE_ALIASES.get(paper_dir.name, ()):
        candidate_keys.add(normalize_name(alias))
    for archive in top_level_archives():
        if archive_key(archive.name) in candidate_keys:
            archive_rel = archive.relative_to(REPO_ROOT).as_posix()
            if archive_rel not in archives:
                archives.append(archive_rel)
    return tuple(archives)


def has_zh_variant(paths: list[Path]) -> bool:
    return any("zh" in path.stem.lower() for path in paths)


def discover_paper_directories() -> list[PaperDirectory]:
    tracked_counts = tracked_top_level_counts()
    papers: list[PaperDirectory] = []

    for paper_dir in list_paper_directories():
        tex_files = sorted(paper_dir.rglob("*.tex"))
        pdf_files = candidate_pdfs(paper_dir, tracked_only=False)
        preferred_pdf = choose_best_pdf(paper_dir, tracked_only=False)
        notebook_pdf = choose_best_pdf(paper_dir, tracked_only=True)
        has_build_spec, top_level_tex, compiler = parse_build_spec(paper_dir)

        papers.append(
            PaperDirectory(
                name=paper_dir.name,
                title=humanize_name(paper_dir.name),
                slug=slugify(paper_dir.name),
                repo_dir=paper_dir.name,
                has_build_spec=has_build_spec,
                top_level_tex=top_level_tex,
                compiler=compiler,
                preferred_pdf=preferred_pdf.as_posix() if preferred_pdf else None,
                preferred_pdf_badge=pdf_badge(preferred_pdf) if preferred_pdf else None,
                notebook_pdf=notebook_pdf.as_posix() if notebook_pdf else None,
                notebook_pdf_badge=pdf_badge(notebook_pdf) if notebook_pdf else None,
                has_zh_tex=has_zh_variant([path.relative_to(REPO_ROOT) for path in tex_files]),
                has_zh_pdf=has_zh_variant(pdf_files),
                tex_count=len(tex_files),
                pdf_count=len(pdf_files),
                source_archives=collect_source_archives(paper_dir),
                tracked_file_count=tracked_counts.get(paper_dir.name, 0),
            )
        )

    return papers
