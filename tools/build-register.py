#!/usr/bin/env python3
"""Build register.jsonl — JSONL index with RAG tags for Rules markdown files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RULES_DIR = Path(__file__).resolve().parent.parent
OUTPUT = RULES_DIR / "register.jsonl"

CATEGORIES = [
    "global",
    "project-files",
    "automation",
    "devops",
    "ipc",
    "platform-ux",
    "python",
    "js",
    "css",
    "cpp",
    "rust",
    "kotlin",
]

CONCEPT_MAP = {
    "startup": ["workflow", "initialization"],
    "memory": ["memory-management", "lifecycle"],
    "persistent-memory": ["knowledge-base", "ai-memory"],
    "types": ["type-safety", "type-checking"],
    "modules": ["encapsulation", "architecture"],
    "testing": ["tdd", "quality"],
    "validation": ["runtime-checking", "boundaries"],
    "nesting": ["code-style", "readability"],
    "errors": ["error-handling", "result-types"],
    "threading": ["concurrency", "async"],
    "naming": ["conventions", "readability"],
    "ownership": ["memory-management", "borrowing"],
    "compose": ["ui", "declarative"],
    "viewmodel": ["state-management", "mvvm"],
    "coroutines": ["concurrency", "async"],
    "ktor": ["http", "networking"],
    "amper": ["build-system", "configuration"],
    "stability": ["build-system", "ci"],
    "encapsulation": ["architecture", "privacy"],
    "result-pattern": ["error-handling", "result-types"],
    "cascade": ["css-architecture", "separation"],
    "themes": ["theming", "dark-mode"],
    "responsive": ["mobile-first", "breakpoints"],
    "typography": ["fonts", "spacing"],
    "separation": ["architecture", "concerns"],
    "custom-properties": ["design-tokens", "variables"],
    "posix": ["linux", "system-programming"],
    "build": ["cmake", "configuration"],
    "jsdoc": ["type-annotations", "documentation"],
    "eslint": ["linting", "code-quality"],
    "typescript-cli": ["type-checking", "jsconfig"],
    "philosophy": ["design-principles", "approach"],
    "consistency": ["cross-language", "patterns"],
    "versions": ["language-versions", "compatibility"],
    "secrets": ["security", "environment"],
    "diagrams": ["mermaid", "visualization"],
    "index-system": ["navigation", "codebase-index"],
    "project-file": ["project-state", "yaml"],
    "todo-file": ["tasks", "tracking"],
    "fixes-file": ["problem-solving", "ai-memory"],
    "rag-file": ["knowledge-base", "ai-memory"],
    "goal-chain": ["milestones", "traceability"],
    "workflow": ["process", "methodology"],
    "contract": ["protocol", "json-rpc"],
    "keyboard": ["shortcuts", "accessibility"],
    "context-menus": ["ui-patterns", "interaction"],
    "drag-drop": ["interaction", "file-management"],
    "pointer-touch": ["interaction", "accessibility"],
    "issue-reporter": ["bug-reporting", "crash-handling"],
    "checklist": ["verification", "shipping"],
    "safety": ["runtime-validation", "boundaries"],
    "distribution": ["packaging", "pipx"],
    "gtk": ["gtk4", "gui"],
    "verification": ["clippy", "testing"],
    "naming-suffix": ["naming", "collision-prevention"],
    "ack-pattern": ["result-types", "return-format"],
    "dependencies": ["libraries", "tooling"],
    "structure": ["file-organization", "architecture"],
    "quick-ref": ["reference", "summary"],
}

# ---------------------------------------------------------------------------
# Curated learning path layers (1 = read first, 6 = reference/index)
# ---------------------------------------------------------------------------

# Layer 1: Global foundations — understand the system
# Layer 2: Project methodology — how to organize work
# Layer 3: Language core — types, structure, errors, naming
# Layer 4: Language advanced — testing, tooling, nesting, platform
# Layer 5: Infrastructure — automation, devops, ipc, platform-ux
# Layer 6: Reference — quick-refs, READMEs, indexes

CORE_FILES = {"types", "structure", "modules", "errors", "ack-pattern",
              "result-pattern", "naming", "encapsulation", "ownership"}

ADVANCED_FILES = {"testing", "dependencies", "nesting", "build", "posix",
                  "threading", "coroutines", "ktor", "amper", "stability",
                  "compose", "viewmodel", "data-classes", "gtk",
                  "verification", "eslint", "jsdoc", "typescript-cli",
                  "validation", "philosophy", "safety", "distribution",
                  "cascade", "custom-properties", "themes", "separation",
                  "responsive", "typography", "naming-suffix"}

INFRA_CATEGORIES = {"automation", "devops", "ipc", "platform-ux"}


def assign_layer(category: str, stem: str, file_type: str) -> int:
    """Assign a learning path layer (1-6) based on category and file."""
    if file_type in ("readme", "quick-ref"):
        return 6
    if category == "global":
        return 1
    if category == "project-files":
        return 2
    if category in INFRA_CATEGORIES:
        return 5
    # Language-specific files
    if stem in CORE_FILES:
        return 3
    if stem in ADVANCED_FILES:
        return 4
    return 4  # Default for unknown language files


STOP_WORDS = frozenset([
    "the", "a", "an", "is", "are", "not", "and", "or", "for", "in",
    "on", "with", "to", "of", "by", "from", "at", "but", "vs", "it",
    "no", "do", "how", "why", "what", "when", "who", "than", "that",
    "its", "you", "be", "all",
])


# ---------------------------------------------------------------------------
# Frontmatter parser (no PyYAML dependency)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from text. Returns (metadata, remaining_content).

    Frontmatter must start at the very first line with '---'.
    Only supports: list[str] fields and int fields.
    Files without frontmatter return ({}, original_text).
    """
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    block = text[4:end]
    remaining = text[end + 5:]  # skip past closing ---\n

    meta: dict = {}
    for line in block.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        m = re.match(r"^(\w+):\s*(.*)$", line)
        if not m:
            continue

        key = m.group(1)
        value = m.group(2).strip()

        # list field: [item1, item2, ...]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                continue  # skip empty lists
            items = [item.strip().strip('"').strip("'") for item in inner.split(",")]
            meta[key] = [item for item in items if item]
        # int field
        elif value.isdigit():
            meta[key] = int(value)

    return meta, remaining


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
# Basic field extraction
# ---------------------------------------------------------------------------

def extract_title(lines: list[str]) -> str:
    """First H1 heading."""
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_subtitle(lines: list[str]) -> str:
    """First blockquote after H1."""
    found_h1 = False
    parts: list[str] = []
    for line in lines:
        if not found_h1 and line.startswith("# "):
            found_h1 = True
            continue
        if found_h1:
            if line.startswith("> "):
                parts.append(line[2:].strip())
            elif parts:
                break
            elif line.strip() == "":
                continue
            else:
                break
    return " ".join(parts)


def extract_sections(lines: list[str]) -> list[str]:
    """All ## and ### headings."""
    sections: list[str] = []
    for line in lines:
        m = re.match(r"^(#{2,3})\s+(.+)", line)
        if m:
            sections.append(m.group(2).strip())
    return sections


def extract_rules(lines: list[str]) -> list[str]:
    """Lines starting with RULE: — strip prefix."""
    result: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("RULE: "):
            result.append(s[6:])
    return result


def extract_banned(lines: list[str]) -> list[str]:
    """Lines starting with BANNED: — strip prefix."""
    result: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("BANNED: "):
            result.append(s[8:])
    return result


def extract_refs(text: str) -> list[str]:
    """Cross-referenced .md filenames from markdown links."""
    refs = re.findall(r"\[.*?\]\(([^)]+\.md)\)", text)
    seen: set[str] = set()
    unique: list[str] = []
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            unique.append(ref)
    return unique


def extract_code_languages(text: str) -> list[str]:
    """Language tags from fenced code blocks."""
    langs = re.findall(r"^```(\w+)", text, re.MULTILINE)
    return sorted(set(langs))


def extract_keywords(text: str) -> list[str]:
    """Domain-specific keywords from the content."""
    keywords: set[str] = set()
    # Match VITAL:, PREFER:, FORMAT:, PATTERN:, NOTE: markers
    for marker in ["VITAL", "PREFER", "FORMAT", "PATTERN", "NOTE"]:
        pattern = rf"^{marker}:\s+(.+)"
        for m in re.finditer(pattern, text, re.MULTILINE):
            words = re.findall(r"[a-zA-Z][-a-zA-Z]+", m.group(1))
            for w in words:
                w_lower = w.lower()
                if len(w_lower) > 3 and w_lower not in STOP_WORDS:
                    keywords.add(w_lower)
    return sorted(keywords)[:20]  # Cap at 20 keywords


# ---------------------------------------------------------------------------
# Concepts and tags
# ---------------------------------------------------------------------------

def derive_concepts(title: str, sections: list[str], stem: str) -> list[str]:
    """Derive semantic concepts from filename stem and headings."""
    concepts: set[str] = set()
    key = stem.lower()
    if key in CONCEPT_MAP:
        concepts.update(CONCEPT_MAP[key])
    for word in re.findall(r"[a-z][-a-z]+", title.lower()):
        if word in CONCEPT_MAP:
            concepts.update(CONCEPT_MAP[word])
    for section in sections:
        for word in re.findall(r"[a-z][-a-z]+", section.lower()):
            if word in CONCEPT_MAP:
                concepts.update(CONCEPT_MAP[word])
    return sorted(concepts)


def build_tags(
    title: str,
    code_languages: list[str],
    concepts: list[str],
    keywords: list[str],
) -> list[str]:
    """Build merged, deduplicated, sorted tag set."""
    tags: set[str] = set()
    for word in re.findall(r"[a-zA-Z][-a-zA-Z]+", title):
        w = word.lower()
        if len(w) > 2 and w not in STOP_WORDS:
            tags.add(w)
    tags.update(code_languages)
    tags.update(concepts)
    tags.update(keywords[:10])
    return sorted(tags)


# ---------------------------------------------------------------------------
# Edge computation
# ---------------------------------------------------------------------------

def compute_reverse_edges(entries: list[dict]) -> None:
    """Compute required_by and fed_by reverse edges across all entries."""
    file_map: dict[str, dict] = {e["file"]: e for e in entries}

    for entry in entries:
        edges = entry.get("edges")
        if not edges:
            continue

        src = entry["file"]

        for target in edges.get("requires", []):
            if target in file_map:
                target_edges = file_map[target].setdefault("edges", {})
                rb = target_edges.setdefault("required_by", [])
                if src not in rb:
                    rb.append(src)

        for target in edges.get("feeds", []):
            if target in file_map:
                target_edges = file_map[target].setdefault("edges", {})
                fb = target_edges.setdefault("fed_by", [])
                if src not in fb:
                    fb.append(src)


def validate_edges(entries: list[dict]) -> list[str]:
    """Warn about edges pointing to non-existent files. Returns warnings."""
    known_files = {e["file"] for e in entries}
    warnings: list[str] = []

    for entry in entries:
        edges = entry.get("edges")
        if not edges:
            continue
        src = entry["file"]
        for edge_type in ("requires", "feeds", "related"):
            for target in edges.get(edge_type, []):
                if target not in known_files:
                    warnings.append(f"  {src} -> {edge_type} -> {target} (NOT FOUND)")

    return warnings


# ---------------------------------------------------------------------------
# Main parse
# ---------------------------------------------------------------------------

def parse_file(category: str, filepath: Path) -> dict:
    """Parse a single markdown file into a register entry."""
    text = filepath.read_text(encoding="utf-8")
    rel_path = filepath.relative_to(RULES_DIR).as_posix()

    # Parse frontmatter (must be very first line)
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
    refs = extract_refs(content)
    code_languages = extract_code_languages(content)
    has_examples = bool(re.search(r"```\w+", content))

    # Frontmatter overrides auto-generated values when present
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

    # Build edges from frontmatter
    edges: dict[str, list[str]] = {}
    for edge_type in ("requires", "feeds", "related"):
        if edge_type in fm and fm[edge_type]:
            edges[edge_type] = fm[edge_type]
    # Always include reverse-edge slots (filled later by compute_reverse_edges)
    if edges or True:  # always include edges dict for consistency
        edges.setdefault("requires", [])
        edges.setdefault("required_by", [])
        edges.setdefault("feeds", [])
        edges.setdefault("fed_by", [])
        edges.setdefault("related", [])

    entry = {
        "file": rel_path,
        "category": category,
        "type": file_type,
        "layer": layer,
        "title": title,
        "subtitle": subtitle,
        "sections": sections,
        "rules": rules,
        "banned": banned,
        "refs": refs,
        "code_languages": code_languages,
        "has_examples": has_examples,
        "keywords": keywords,
        "tags": tags,
        "concepts": concepts,
        "edges": edges,
    }

    return entry


def main() -> None:
    files = collect_files()
    entries: list[dict] = []

    for category, filepath in files:
        entry = parse_file(category, filepath)
        entries.append(entry)

    # Compute reverse edges
    compute_reverse_edges(entries)

    # Validate edges
    warnings = validate_edges(entries)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    total_rules = sum(len(e["rules"]) for e in entries)
    total_banned = sum(len(e["banned"]) for e in entries)
    total_tags = sum(len(e["tags"]) for e in entries)

    # Edge statistics
    with_edges = sum(
        1 for e in entries
        if any(e.get("edges", {}).get(k, []) for k in ["requires", "feeds", "related"])
    )
    total_edges = sum(
        len(e.get("edges", {}).get(k, []))
        for e in entries
        for k in ["requires", "feeds", "related", "required_by", "fed_by"]
    )

    print(f"Wrote {len(entries)} entries to register.jsonl")
    print(
        f"  {len(entries)} entries, "
        f"{total_rules} rules, {total_banned} banned, "
        f"{total_tags} total tags"
    )
    print(f"  {with_edges}/{len(entries)} files with edges, {total_edges} edges total")

    if warnings:
        print(f"\nEdge warnings ({len(warnings)}):")
        for w in warnings:
            print(w)
        sys.exit(1)


if __name__ == "__main__":
    main()
