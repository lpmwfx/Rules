---
tags: [module-tree, encapsulation, file-split, architecture, gui, ui, global, slint, js, html]
concepts: [module-design, encapsulation, file-splitting, tree-structure, single-responsibility, ai-comprehension]
requires: [global/file-limits.md]
related: [uiux/components.md, uiux/file-structure.md, global/nesting.md, uiux/mother-child.md]
keywords: [module, nested, encapsulation, split, folder, file, tree, slint, js, html, import, export, comprehension, 200-lines, dealbreaker]
layer: 1
---
# Module Tree

> One encapsulated module = one file. "Nested modules" means a folder of files — never nested code in one file.

---

VITAL: One module = one file — the file boundary IS the encapsulation boundary
VITAL: Every level of nesting in the UI tree = a separate file — no exceptions
VITAL: A file must be independently comprehensible — if it requires scrolling to understand, it is too large
VITAL: In JS/HTML/Slint: splitting is not style — it is what makes the code work and what lets AI reason about it
RULE: "Nested modules" = a parent folder containing child files — not nested code inside one file
RULE: A module may be 50 lines or 200 lines — size follows naturally from encapsulation
RULE: When a module spawns sub-modules, it becomes a folder; its own code moves to an index/root file
BANNED: Multiple independent modules in one file regardless of line count
BANNED: A "central" file that grows as the project grows — central files are architectural debt
BANNED: Interpreting "nested module" as adding nested classes or sections inside one file

## The Primary Rule: Encapsulation

Size is not the constraint — encapsulation is. A well-encapsulated module is naturally small.
When a file grows large, it is a signal that multiple modules have been merged into one file.

```
Signal: file is growing → ask "does this file have one clear job?"
  YES → it may grow, but consider splitting when AI comprehension suffers
  NO  → it already contains multiple modules — split now along responsibility lines
```

## Why File Size Matters for AI

An AI working on a 2000-line file cannot hold the full context in working memory.
It will make changes that break other sections of the same file — not because the logic is wrong,
but because it lost track of what else is in there.

```
200-line file:  AI can hold the whole module in context — safe to edit
500-line file:  AI loses the bottom half while editing the top — risky
2000-line file: AI is effectively editing blind — guaranteed unintended side effects
```

RULE: The working limit for reliable AI edits is ~200 lines per file
RULE: A file that causes AI context loss will produce bugs — split it before that happens

## JS / HTML — Structural Requirement

In JavaScript and HTML, one-module-per-file is not a preference — it is how the module system works.
Mixing modules in one file breaks imports, tree-shaking, and hot reload.

```js
// WRONG — two modules in one file, both exported
// UserCard.js
export class UserCard { ... }      // module 1
export class UserAvatar { ... }    // module 2 — belongs in Avatar.js

// RIGHT — one module per file
// UserCard.js
import { UserAvatar } from './UserAvatar.js'
export class UserCard { ... }

// UserAvatar.js
export class UserAvatar { ... }
```

RULE: Each ES module export that stands alone is its own file
RULE: Named re-exports belong in an index.js — not mixed with implementation
BANNED: Barrel files that also contain implementation code

## Slint — Hard Limit

Slint is declarative. The AI cannot skip or summarise declarative markup — it must read every line
to understand the visual tree. A 2000-line Slint file is a dealbreaker: the AI will produce
incorrect layouts, wrong property bindings, and broken signal connections.

```slint
// WRONG — one central App.slint growing with every feature
component App {
    // navigation (200 lines)
    // dashboard (400 lines)
    // settings (300 lines)
    // modals (500 lines)
    // ...
}

// RIGHT — one component per file, App.slint composes them
// App.slint (40 lines — wires navigation + pages)
// NavigationBar.slint (80 lines)
// DashboardPage.slint (120 lines)
// SettingsPage.slint (100 lines)
// ConfirmModal.slint (60 lines)
```

VITAL: In Slint, 200 lines per file is a practical hard limit — AI loses the property graph above that
RULE: Every named Slint component lives in its own `.slint` file
RULE: App-level wiring (routing, modal management) is the only code allowed in the root component file
BANNED: Growing a central `.slint` file — split on the first sign of a second independent component

## The Folder Pattern

When a module grows sub-modules, it becomes a folder:

```
Before — HomeScreen.tsx at 180 lines, growing:
  home/
  └── HomeScreen.tsx

After — HomeScreen spawns sub-modules:
  home/
  ├── HomeScreen.tsx     ← now only composes: FeedList + Sidebar (40 lines)
  ├── FeedList.tsx       ← extracted (90 lines)
  ├── FeedItem.tsx       ← extracted (70 lines)
  └── Sidebar.tsx        ← extracted (80 lines)
```

RULE: The parent file after a split is a composer — it imports and arranges, adds no new logic
RULE: Sub-modules are named after what they do, not what they contain

## Module Tree IS Mother–Child

The folder pattern described here is the same as the mother-child pattern (see uiux/mother-child.md):

- The parent/index file = **mother** — composes children, owns no logic of its own
- Each sub-module file = **child** — stateless, one job, independently understandable
- The folder boundary = **ownership boundary** — mother owns the subtree

This applies at every level: UI components, Rust modules, Python packages, JS modules.
When a file splits into a folder, it becomes a mother. Its children are stateless leaves.

RULE: A split always follows mother-child — the parent file is a compositor, children are stateless
BANNED: A flat cluster of sibling files with no compositor — there is always one mother

RESULT: Each file is a unit of change and a unit of AI comprehension — one edit, one file, no surprises
REASON: The encapsulation boundary and the file boundary are the same thing — they must stay aligned
