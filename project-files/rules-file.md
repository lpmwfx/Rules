---
tags: [rules, project-rules, observations, conventions, project-files]
concepts: [project-rules, rule-observations, local-conventions]
related: [project-files/rag-file.md, project-files/fixes-file.md, project-files/project-file.md]
keywords: [rules, observations, conventions, local-rules, RULES, active-rules, project-specific]
layer: 2
---
# RULES File

> AI's rule observations for this project — active MCP rules + project-specific conventions

---

## Quick Reference

- **Location:** `proj/RULES`
- **Format:** Markdown — two sections: active MCP rules + project observations
- **Required:** All projects
- **Owner:** AI writes and maintains — user may add rules at any time

The AI writes here when it observes a pattern, derives a rule from a FIXES entry,
or notices a convention that is specific to this codebase.
Not global rules — those live in MCP. This is what makes *this* project different.

---

RULE: File lives at `proj/RULES`
RULE: AI reads proj/RULES at session start — immediately after proj/PROJECT
RULE: AI writes to proj/RULES when it discovers a project-specific convention
RULE: AI writes to proj/RULES when a FIXES entry implies a recurring rule
RULE: When a rule is superseded or wrong, AI updates it — proj/RULES is a living document
RULE: Active MCP rules (which files to load this phase) live here, not in proj/PROJECT
BANNED: Putting project-specific rules only in RAG — rules go in RULES, discoveries go in RAG
BANNED: Letting proj/RULES grow stale — if a rule no longer applies, remove it

## Format

```markdown
# RULES: project-name

## Active MCP Rules
Rules loaded this phase via get_rule(). Replace when phase changes.

- global/topology.md
- global/module-tree.md
- global/file-limits.md
- uiux/components.md
- rust/types.md

## Project Rules
Conventions observed in this codebase. AI adds here; user may override.

- All API calls go through `src/gateway/client.rs` — never fetch in UI or Core
- Component names match their filename exactly — `FeedItem` lives in `FeedItem.slint`
- Error variants are defined in `src/shared/errors.rs` — never inline
- CSS custom properties are declared in `tokens.css` — never in component files

## Derived from FIXES
Rules extracted from recurring problems — see proj/FIXES for full context.

- Never use `unwrap()` on network results — always propagate with `?` (bug: 2026-01-12)
- Modal state lives in AdapterState_sta, not local component state (bug: 2026-02-03)
```

## Difference from RAG and FIXES

| File | Contains | Written when |
|------|----------|--------------|
| RULES | Rules and conventions — what to always/never do | Pattern observed, FIXES implies a rule |
| RAG | Knowledge — links, discoveries, how things work | Something learned about the project/domain |
| FIXES | Problem → Cause → Solution — what went wrong | After fixing a bug or mistake |

RULE: If in doubt — a rule is a RULE, a fact is RAG, a bug story is FIXES
