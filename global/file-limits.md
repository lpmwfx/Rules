---
tags: [file-limits, file-size, split, refactor, global, enforcement]
concepts: [file-size, code-splitting, single-responsibility, maintainability]
requires: [global/topology.md]
feeds: [global/module-tree.md]
related: [global/read-before-write.md, global/know-before-change.md, uiux/components.md, uiux/file-structure.md]
keywords: [file-size, line-count, split, too-large, oversized, max-lines, css, ui, component, refactor, before-write]
layer: 1
---
# File Size Limits

> Size follows encapsulation — when a file has one job, it stays small naturally

---

VITAL: One file, one encapsulated module — if the file is growing, it has taken on a second job
VITAL: Size limits exist because AI loses context above ~200 lines — not for style reasons
VITAL: Before adding code to any existing file, count its lines — if near the limit, split the module first
RULE: After splitting, update all imports and references before moving on
BANNED: Adding to a file that is already at its limit
BANNED: "I'll split it later" — split at the trigger, not when it becomes a crisis

## Limits by File Type

| File type | AI comprehension limit | Action when approaching |
|-----------|----------------------|------------------------|
| Slint component | 200 lines | Split — AI loses property graph, bugs guaranteed |
| UI component (JS/TS/Kotlin/Swift) | 200 lines | Extract sub-component to own file |
| CSS / SCSS per file | 150 lines | Split by component or section |
| Python module | 250 lines | Extract class or function group |
| JS / TS module | 250 lines | Extract to new module file |
| Rust module (`mod`) | 300 lines | Split into submodules |
| C++ source file | 350 lines | Extract to new translation unit |

RULE: "Approaching" means within 20% of the limit — plan the split before hitting it
RULE: Slint is the strictest — declarative markup gives AI no way to skip or summarise sections

RULE: Soft limit = warning, start planning the split
RULE: Hard limit = stop, split before writing a single new line
RULE: README, spec, and documentation files are exempt — content drives length

## The Check (do this every time)

```
Before writing to existing-file.ext:
  1. Count lines: wc -l existing-file.ext
  2. If count >= hard limit → split first
  3. If count >= soft limit → plan the split, do it before the file grows further
  4. Then write the new code
```

RULE: "Count before you write" is the habit — not a suggestion

## How to Split

### UI / Component

```
Before (HomeScreen.tsx — 130 lines):
  HomeScreen
    ├── header markup (30 lines)
    ├── feed list + items (60 lines)
    └── sidebar (40 lines)

After:
  HomeScreen.tsx      (20 lines — composes the three below)
  HomeHeader.tsx      (30 lines)
  HomeFeed.tsx        (35 lines)
  HomeFeedItem.tsx    (25 lines)
  HomeSidebar.tsx     (40 lines)
```

### CSS

```
Before (main.css — 200 lines):
  variables + reset + header + cards + forms + footer

After:
  tokens.css    (variables, reset)
  header.css    (header component)
  cards.css     (card component)
  forms.css     (form component)
  footer.css    (footer component)
```

### Python / JS / Rust module

```
Before (adapter.py — 280 lines):
  class UserAdapter + class ItemAdapter + class SearchAdapter

After:
  adapter/
  ├── __init__.py   (re-exports)
  ├── user.py       (UserAdapter)
  ├── item.py       (ItemAdapter)
  └── search.py     (SearchAdapter)
```

## Why This Rule Exists

A file that is too large guarantees that a fix in one area will touch lines from another area.
That is how one change breaks unrelated behaviour — not because the logic is wrong, but because
everything is in the same file.

RESULT: Small files make changes local — a fix in `HomeFeed.tsx` cannot touch `HomeSidebar.tsx`
REASON: File boundary = change boundary; keeping files small keeps changes contained
