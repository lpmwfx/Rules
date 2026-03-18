---
tags: [docs, documentation, rustdocumenter]
concepts: [documentation, public-api, discoverability]
requires: []
keywords: [doc-comment, triple-slash, export, component, callback, property, rustdocumenter]
layer: 2
---
# Slint Documentation Rules

> Every exported component, struct, enum, callback, and property MUST have a `///` doc comment — reported as **errors**, blocks build and commit

---

## Requirement

RULE: Every `export component`, `export struct`, `export enum` MUST have a `///` doc comment
RULE: Every `callback` declaration MUST have a `///` doc comment
RULE: Every `in property`, `out property`, `in-out property` MUST have a `///` doc comment
RULE: `private` properties are exempt

## Rule ID

`slint/docs/doc-required`

## Enforcement

Two enforcement layers — both report as **errors** (block build and commit):

| Tool | Trigger | Severity | Output |
|---|---|---|---|
| `rustdocumenter gen` | Manual | error | `man/` + `proj/ISSUES`, blocks build |
| `slintscan` (cargo build) | Automatic on `cargo build` | error | stderr, blocks build |

`rustdocumenter gen` walks all `.slint` files in `ui/` and generates `man/` documentation alongside `proj/ISSUES`.

Missing `///` doc comments are reported as **errors** and block `cargo build` and pre-commit hooks. Every exported item must be documented before code can be shipped.

## Format

```slint
/// Main editor window — hosts the sidebar, content panel, and toolbar.
export component EditorWindow inherits Window {

    /// Title shown in the window header bar.
    in property <string> window-title;

    /// Emitted when the user requests saving the current document.
    callback save-requested();
}
```

```slint
/// Data record for a single book entry in the library list.
export struct BookRecord {
    /// Unique identifier from the database.
    id: int,
    /// Display title shown in the sidebar.
    title: string,
}
```

## Minimal acceptable doc

One sentence is enough:

```slint
/// Displays a single card in the card browser grid.
export component CardTile inherits Rectangle { ... }
```

## BANNED

BANNED: Exported items with no `///` comment — they appear in `proj/ISSUES`:
```slint
// BAD
export component BooksPanel inherits Rectangle { ... }
```

BANNED: Only `//` comments (not picked up by rustdocumenter):
```slint
// BAD — not a doc comment
callback book-selected(id: int);
```

## Workflow

1. Run `rustdocumenter gen` to scan all `.slint` files → `proj/ISSUES` lists undocumented exports
2. Add `///` above each item listed in `proj/ISSUES`
3. Re-run `rustdocumenter gen` — `proj/ISSUES` shrinks or disappears
