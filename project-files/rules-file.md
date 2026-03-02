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

## Bootstrap — how to derive Active Rules for a new project

When proj/RULES is empty or missing, derive the active rule set as follows:

```
1. Read proj/PROJECT → extract:
   - Languages  (Rust, Kotlin, Python, JS…)
   - Platforms  (Windows, macOS, GNOME, KDE, Android, iOS, Web…)
   - Toolkit    (Slint, GTK4, Compose, React, Qt…)

2. Always load — every project:
   global/topology.md
   global/module-tree.md
   global/file-limits.md
   global/config-driven.md
   global/persistent-state.md

3. For each Language → load:
   <lang>/README.md        (e.g. rust/README.md, kotlin/README.md)

4. For each Platform → load the matching file (see full table in project-files/uiux-file.md):
   Windows      → uiux/menus-windows.md
   macOS        → uiux/menus-macos.md
   GNOME        → uiux/menus-gnome.md
   KDE          → uiux/menus-kde.md
   Web / PWA    → css/README.md
   Android      → uiux/help-about.md
   iOS          → uiux/theming.md
   Linux CLI    → skip (no desktop = no platform menu rules)

5. If project has a GUI → always add:
   uiux/tokens.md
   uiux/components.md
   uiux/state-flow.md
   uiux/file-structure.md
   uiux/help-about.md
   uiux/checklist.md

6. For Toolkit:
   Slint              → uiux/menus-slint.md
   GTK4               → uiux/gtk.md
   Compose/React/Vue  → already covered by Language + Platform steps
   Qt6 / SwiftUI      → uiux/theming.md

7. Write the collected paths to ## Active Rules in this file.
```

RULE: The resulting list must feel like it was written for THIS project — not a generic dump
RULE: Phase 1 (bootstrap): load global + language READMEs. Phase 2+ (active dev): load topic-specific files as work progresses.

## Format

```markdown
# RULES: project-name

## Active Rules
Exact file paths — load these via get_rule(file: "...") at session start.
Structured by category so the scope is immediately visible.

### Always
- global/topology.md
- global/module-tree.md
- global/file-limits.md
- global/config-driven.md
- global/persistent-state.md

### Language: Rust
- rust/README.md
- rust/ownership.md
- rust/errors.md
- rust/naming.md

### UI (Slint — Windows + macOS + GNOME)
- uiux/tokens.md
- uiux/components.md
- uiux/state-flow.md
- uiux/menus-slint.md
- uiux/menus-windows.md
- uiux/menus-macos.md
- uiux/menus-gnome.md
- uiux/help-about.md

## Project Rules
Conventions observed in this codebase. AI adds here; user may override.

- All API calls go through `src/gateway/client.rs` — never fetch in UI or Core
- Component names match their filename exactly — `FeedItem` lives in `FeedItem.slint`
- Error variants are defined in `src/shared/errors.rs` — never inline
- Token values declared in `src/ui/tokens/` — never in component .slint files

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
