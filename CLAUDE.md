# CLAUDE.md — Rules

Markdown coding standards for AI-assisted development. Part of Rules-dev superprojekt.

## Commands

```bash
cd Rules && python tools/build-register.py    # Rebuild metadata index
```

## Rule Files (`<category>/*.md`)

YAML frontmatter: `tags`, `concepts`, `keywords`, `layer` (1-6), `requires`, `feeds`, `related`.
Content markers: `RULE:`, `BANNED:`, `VITAL:` — extracted into `register.jsonl`.
Categories: `global`, `project-files`, `automation`, `devops`, `ipc`, `uiux`, `python`, `js`, `css`, `cpp`, `rust`, `kotlin`.

## Key Files

- `tools/build-register.py` — YAML parser + index generator
- `register.jsonl` — Pre-built search index (never edit by hand)
- `proj/rulestools.toml` — Scanner config for Rules repo itself

## Type Naming Convention

`TypeName_<tag>`: `_ui`, `_adp`, `_core`, `_pal`, `_gtw`, `_x`, `_sta`, `_cfg`, `_test`.

## Superprojekt

This repo is part of Rules-dev. See `../proj/PROJECT` for ecosystem overview and `../proj/TODO` for all tasks.
