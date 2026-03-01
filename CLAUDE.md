# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a dual-project monorepo:
- **`Rules/`** — Multi-language coding standards in Markdown with YAML frontmatter
- **`RulesMCP/`** — Python MCP server that exposes rules to AI coding assistants

The MCP server in this repo is what powers the `mcp__rules__*` tools available in this Claude Code session.

## Commands

### Rules — Rebuild the metadata index

```bash
cd Rules
python tools/build-register.py
```

Parses all `.md` rule files, extracts YAML frontmatter, and regenerates `Rules/register.jsonl`. Run this after adding or modifying any rule file's frontmatter. CI auto-commits the result on push.

### RulesMCP — Install / develop

```bash
# Install from local source for development
cd RulesMCP
pip install -e .

# Run the MCP server directly (for testing)
python -m rules_mcp
```

Python 3.11+ required. Dependencies: `fastmcp>=2.0.0`, `gitpython>=3.1.0`, `platformdirs>=3.0.0`.

## Architecture

### Rule Files (`Rules/<category>/*.md`)

Each file has a YAML frontmatter block defining:
- `tags`, `concepts`, `keywords` — for weighted search
- `layer` — integer 1–6 controlling learning-path ordering (1=foundation, 6=reference)
- `requires`, `feeds`, `related` — graph edges to other rule files

Content uses `RULE:` and `BANNED:` marker lines that get extracted into `register.jsonl`.

Categories: `global`, `project-files`, `automation`, `devops`, `ipc`, `platform-ux`, `python`, `js`, `css`, `cpp`, `rust`, `kotlin`.

### Metadata Index (`Rules/register.jsonl`)

Pre-built index — one JSON line per rule file. Fields: `file`, `category`, `title`, `tags`, `concepts`, `keywords`, `layer`, `rules[]`, `banned[]`, `edges`. Never edit by hand; always regenerate via `build-register.py`.

### MCP Server (`RulesMCP/rules_mcp/`)

| File | Purpose |
|------|---------|
| `server.py` | FastMCP app, 7 tool definitions, lazy `_ensure_loaded()` init |
| `registry.py` | In-memory JSONL loader, weighted search, layer grouping |
| `repo.py` | Git clone/pull of the Rules repo into `~/.cache/rules-mcp/Rules` |
| `__main__.py` | Entry point (`mcp.run()`) |

**Search scoring**: file/title = 3, tags/concepts = 2, keywords = 1. Bidirectional substring match with stop-word filtering.

**Lazy loading**: On first tool call, `_ensure_loaded()` clones/pulls the upstream repo and builds the in-memory registry from `register.jsonl`.

### Type Naming Convention

All types follow `TypeName_<tag>` (defined in `name_convention.json`). Tag = architectural layer (1–4 lowercase chars): `pal`, `core`, `adp`, `db`, `ui`, `net`, `auth`, `cfg`, `gen`, `stub`, `test`, `x`.

## Key Files

- `Rules/tools/build-register.py` — YAML frontmatter parser + index generator (no PyYAML; parses manually)
- `Rules/proj/PROJECT` — Architectural goals and principles
- `Rules/proj/TODO` — Known issues: missing files, contradictions, register gaps
- `RulesMCP/pyproject.toml` — Package metadata and entry point
