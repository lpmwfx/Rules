#!/usr/bin/env python3
"""Build register.jsonl — JSONL index with RAG tags for Rules markdown files.

Mother file: imports children (register_config, register_parse) and composes.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(format="%(message)s", level=logging.INFO)

from register_config import CATEGORIES, assign_layer
from register_parse import (
    parse_frontmatter,
    extract_title,
    extract_subtitle,
    extract_sections,
    extract_rules,
    extract_banned,
    extract_axioms,
    extract_refs,
    extract_code_languages,
    extract_keywords,
    derive_concepts,
    build_tags,
    compute_reverse_edges,
    validate_edges,
)

RULES_DIR = Path(__file__).resolve().parent.parent
OUTPUT = RULES_DIR / "register.jsonl"


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files() -> list[tuple[str, Path]]:
    """Collect all .md files in ordered categories."""
    files: list[tuple[str, Path]] = []

    root_readme = RULES_DIR / "README.md"
    if root_readme.exists():
        files.append(("root", root_readme))

    for cat in CATEGORIES:
        dir_path = RULES_DIR / cat
        if not dir_path.is_dir():
            continue
        md_files = sorted(dir_path.glob("*.md"), key=lambda f: f.name)
        readme = dir_path / "README.md"
        ordered: list[Path] = []
        if readme.exists():
            ordered.append(readme)
        ordered.extend(f for f in md_files if f.name != "README.md")
        for f in ordered:
            files.append((cat, f))

    return files


# ---------------------------------------------------------------------------
# Parse a single file into a register entry
# ---------------------------------------------------------------------------

def parse_file(category: str, filepath: Path) -> dict:
    """Parse a single markdown file into a register entry."""
    text = filepath.read_text(encoding="utf-8")
    rel_path = filepath.relative_to(RULES_DIR).as_posix()

    fm, content = parse_frontmatter(text)
    lines = content.split("\n")

    if filepath.name == "README.md":
        file_type = "readme"
    elif filepath.name == "quick-ref.md":
        file_type = "quick-ref"
    else:
        file_type = "content"

    title = extract_title(lines)
    subtitle = extract_subtitle(lines)
    sections = extract_sections(lines)
    rules = extract_rules(lines)
    banned = extract_banned(lines)
    axioms = extract_axioms(lines)
    refs = extract_refs(content)
    code_languages = extract_code_languages(content)
    has_examples = bool(re.search(r"```\w+", content))

    if "tags" in fm:
        tags = sorted(fm["tags"])
    else:
        auto_keywords = extract_keywords(content)
        auto_concepts = derive_concepts(title, sections, filepath.stem)
        tags = build_tags(title, code_languages, auto_concepts, auto_keywords)

    if "concepts" in fm:
        concepts = sorted(fm["concepts"])
    else:
        concepts = derive_concepts(title, sections, filepath.stem)

    if "keywords" in fm:
        keywords = sorted(fm["keywords"])
    else:
        keywords = extract_keywords(content)

    if "layer" in fm:
        layer = fm["layer"]
    else:
        layer = assign_layer(category, filepath.stem, file_type)

    binding = bool(fm.get("binding", False))

    edges: dict[str, list[str]] = {}
    for edge_type in ("requires", "feeds", "related"):
        if edge_type in fm and fm[edge_type]:
            edges[edge_type] = fm[edge_type]
    edges.setdefault("requires", [])
    edges.setdefault("required_by", [])
    edges.setdefault("feeds", [])
    edges.setdefault("fed_by", [])
    edges.setdefault("related", [])

    return {
        "file": rel_path,
        "category": category,
        "type": file_type,
        "layer": layer,
        "binding": binding,
        "title": title,
        "subtitle": subtitle,
        "sections": sections,
        "rules": rules,
        "banned": banned,
        "axioms": axioms,
        "refs": refs,
        "code_languages": code_languages,
        "has_examples": has_examples,
        "keywords": keywords,
        "tags": tags,
        "concepts": concepts,
        "edges": edges,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    files = collect_files()
    entries: list[dict] = []

    for category, filepath in files:
        entry = parse_file(category, filepath)
        entries.append(entry)

    compute_reverse_edges(entries)
    warnings = validate_edges(entries)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    total_rules = sum(len(e["rules"]) for e in entries)
    total_banned = sum(len(e["banned"]) for e in entries)
    total_tags = sum(len(e["tags"]) for e in entries)

    with_edges = sum(
        1 for e in entries
        if any(e.get("edges", {}).get(k, []) for k in ["requires", "feeds", "related"])
    )
    total_edges = sum(
        len(e.get("edges", {}).get(k, []))
        for e in entries
        for k in ["requires", "feeds", "related", "required_by", "fed_by"]
    )

    logging.info("Wrote %d entries to register.jsonl", len(entries))
    logging.info(
        "  %d entries, %d rules, %d banned, %d total tags",
        len(entries), total_rules, total_banned, total_tags,
    )
    logging.info("  %d/%d files with edges, %d edges total", with_edges, len(entries), total_edges)

    if warnings:
        logging.warning("\nEdge warnings (%d):", len(warnings))
        for w in warnings:
            logging.warning(w)
        sys.exit(1)


if __name__ == "__main__":
    main()
