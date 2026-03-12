---
tags: [file-limits, file-size, split, refactor, global, enforcement]
concepts: [file-size, code-splitting, single-responsibility, maintainability]
requires: [global/topology.md]
feeds: [global/module-tree.md]
related: [global/mother-tree.md, global/read-before-write.md, global/know-before-change.md, uiux/components.md, uiux/file-structure.md, uiux/mother-child.md]
keywords: [file-size, line-count, split, too-large, oversized, max-lines, css, ui, component, refactor, before-write]
layer: 1
---
# File Size Limits

> Size follows encapsulation — when a file has one job, it stays small naturally

---

VITAL: One file, one encapsulated module — if the file is growing, it has taken on a second job
VITAL: Size limits exist because AI loses context above ~200 lines — not for style reasons
VITAL: Before adding code to any existing file, count its lines — if near the limit, split the module first
VITAL: A split is NOT moving code sideways — it creates a mother/child folder cascade (see uiux/mother-child.md)
VITAL: The split IS the solution — modular structure is the goal, not a workaround for hitting the limit
RULE: After splitting, update all imports and references before moving on
BANNED: Adding to a file that is already at its limit
BANNED: "I'll split it later" — split at the trigger, not when it becomes a crisis
BANNED: Moving code to a sibling file as a "split" — that is relocation, not decomposition
BANNED: Compressing, removing whitespace, or condensing code to stay under the line limit — the limit is a design signal, not a quota to game
BANNED: Asking to raise or adjust the limit — the correct response to hitting the limit is always to split
BANNED: Treating the split as a penalty — modular structure is the preferred design, the limit enforces what good architecture already demands

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

## The Mother/Child Cascade — The Only Correct Split Pattern

When a file reaches its limit, the split always produces a **folder cascade**:

```
feature.py                   →   feature/
                                 ├── __init__.py   ← mother: composes + re-exports children
                                 ├── child_a.py    ← child: one job
                                 └── child_b.py    ← child: one job
```

The mother file has **one job**: compose and expose its children. It contains no logic of its own.
The children each have **one job**: one class, one function group, one concern.

RULE: A split always produces a folder + a mother file — never just a new sibling in the same directory
RULE: The mother file re-exports everything the old single file exposed — callers change nothing
RULE: Children are named after their single responsibility, not after the feature they came from
RULE: The folder name matches the original file name — `feature.py` becomes `feature/`
BANNED: Creating a flat cluster of siblings with no mother — there is always a single composition point

This is the mother-child pattern (see uiux/mother-child.md): a module is a tree, not a flat list.
The file boundary enforces the tree — each node is either a leaf (stateless child) or a compositor (mother).
The mother owns the subtree, children are independently understandable, siblings never know each other.

## How to Split — Examples

### UI / Component

```
Before (HomeScreen.tsx — 130 lines):
  HomeScreen
    ├── header markup (30 lines)
    ├── feed list + items (60 lines)
    └── sidebar (40 lines)

After (mother/child folder cascade):
  HomeScreen/
  ├── index.tsx       (20 lines — mother: composes the three below, no logic)
  ├── Header.tsx      (30 lines — child: only header)
  ├── Feed.tsx        (35 lines — child: only feed list)
  ├── FeedItem.tsx    (25 lines — child: only feed item)
  └── Sidebar.tsx     (40 lines — child: only sidebar)
```

### CSS

```
Before (main.css — 200 lines):
  variables + reset + header + cards + forms + footer

After (mother/child cascade):
  main.css          (mother: @import children only — no rules of its own)
  ├── tokens.css    (child: variables + reset)
  ├── header.css    (child: header component)
  ├── cards.css     (child: card component)
  ├── forms.css     (child: form component)
  └── footer.css    (child: footer component)
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
