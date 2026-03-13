---
tags: [slint, init, initialize, bootstrap, setup, new-project, slintscanners]
concepts: [project-initialization, project-setup, zero-literal, slint-build-scan]
requires: [global/initialize.md, slint/states.md, slint/validation.md, uiux/tokens.md]
related: [slint/README.md, rust/init.md, slint/themes.md, slint/globals.md]
keywords: [slint, init, cargo, build.rs, slintscanners, tokens, zero-literal, install, cargo-scan, build-scan, theme, globals, state]
layer: 2
---
# Slint Project Initialization

> Run this for every Rust project that uses Slint UI

---

VITAL: Run this AFTER `rust/init.md` — Rust scaffolding must exist first
VITAL: Ask the user for: app name, window title, theme approach (light/dark/system)
VITAL: Do not create UI files until the definition folders exist

---

## Step 0 — Decide structure (ask user)

```
Questions to ask:
1. App window title?
2. Theme?              Light / Dark / System-follows
3. Custom design tokens? Yes / No (use defaults)
```

---

## Step 1 — Install SlintScanners

Zero-literal enforcement for Slint files, runs during `cargo build`.

```bash
curl -sSf https://raw.githubusercontent.com/lpmwfx/SlintScanners/main/install.sh | bash
```

This does three things:
1. Adds `slintscanners` as `[build-dependencies]` in `Cargo.toml`
2. Patches `build.rs` to call `slintscanners::scan_project()`
3. Adds `[slintscanners]` section to `proj/rulestools.toml`

RULE: SlintScanners is installed at project creation — not added later
RULE: Both RustScanners and SlintScanners coexist in the same `build.rs`

---

## Step 1b — Install rustdocumenter

Documentation generator — scans `///` doc comments in `.rs` and `.slint` files, writes `man/` + `proj/ISSUES`.

```bash
cargo install --force --git https://github.com/lpmwfx/RustDocumenter rustdocumenter
```

Generate initial documentation after scaffolding:

```bash
rustdocumenter gen .
```

`proj/ISSUES` lists every exported component, callback, and property that lacks a `///` doc comment.
`man/` has one `.md` + `.json` per source file — see `slint/docs.md`.

RULE: Add `///` doc comments to every `export component`, callback, and `in/out property` — see `slint/docs.md`

---

## Step 2 — Create definition folders

All named values live in these folders. Components reference them, never define literals.

```bash
mkdir -p ui/globals ui/tokens ui/theme ui/state ui/views ui/components
```

```slint
// ui/globals/theme.slint
export global Theme {
    // Colors
    in property <brush> background: #1a1a2e;
    in property <brush> surface: #16213e;
    in property <brush> primary: #0f3460;
    in property <brush> accent: #e94560;
    in property <brush> text-primary: #ffffff;
    in property <brush> text-secondary: #a0a0b0;
}
```

```slint
// ui/tokens/sizes.slint
export global Sizes {
    in property <length> spacing-xs: 4px;
    in property <length> spacing-sm: 8px;
    in property <length> spacing-md: 16px;
    in property <length> spacing-lg: 24px;
    in property <length> spacing-xl: 32px;
    in property <length> border-radius: 8px;
}
```

```slint
// ui/tokens/durations.slint
export global Durations {
    in property <duration> fast: 150ms;
    in property <duration> normal: 300ms;
    in property <duration> slow: 500ms;
}
```

RULE: One global per concern — don't mix colors with sizes
RULE: `globals/` for theme, `tokens/` for design values, `state/` for app state
RULE: Components import from these globals — never hardcode values

---

## Step 3 — Create main.slint

```slint
// ui/main.slint
import { Theme } from "globals/theme.slint";
import { Sizes } from "tokens/sizes.slint";

export component AppWindow inherits Window {
    title: "My App";
    width: 800px;
    height: 600px;
    background: Theme.background;
}
```

RULE: Only the Window component (mother) owns state
RULE: All children are stateless — they receive data via `in property`

---

## Step 4 — Verify

```bash
cargo build
```

Build should succeed with zero SlintScanners warnings. If violations appear, fix them before writing more UI.

---

RULE: Steps 1–4 run in one session — do not leave initialization partial
RULE: Definition folders exist before any UI components are written
RULE: First `cargo build` after init must be clean (zero violations)
BANNED: Writing Slint components before SlintScanners is installed
BANNED: Hardcoding colors, sizes, or durations in component files
