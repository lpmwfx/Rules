"""Register parse — frontmatter parser, field extractors, edge computation."""

from __future__ import annotations

import re

from register_config import CONCEPT_MAP, STOP_WORDS


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
        # bool field
        elif value in ("true", "false"):
            meta[key] = value == "true"
        # int field
        elif value.isdigit():
            meta[key] = int(value)

    return meta, remaining


# ---------------------------------------------------------------------------
# Field extractors
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


def extract_axioms(lines: list[str]) -> list[str]:
    """Lines starting with AXIOM: or VITAL: — strip prefix. These are non-negotiable constraints."""
    result: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("AXIOM: "):
            result.append(s[7:])
        elif s.startswith("VITAL: "):
            result.append(s[7:])
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
    for marker in ["VITAL", "PREFER", "FORMAT", "PATTERN", "NOTE"]:
        pattern = rf"^{marker}:\s+(.+)"
        for m in re.finditer(pattern, text, re.MULTILINE):
            words = re.findall(r"[a-zA-Z][-a-zA-Z]+", m.group(1))
            for w in words:
                w_lower = w.lower()
                if len(w_lower) > 3 and w_lower not in STOP_WORDS:
                    keywords.add(w_lower)
    return sorted(keywords)[:20]


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

        for target in edges.get("related", []):
            if target in file_map:
                target_edges = file_map[target].setdefault("edges", {})
                rel = target_edges.setdefault("related", [])
                if src not in rel:
                    rel.append(src)


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
