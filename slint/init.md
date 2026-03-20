---
tags: [init, initialize, bootstrap, setup, new-project, build-scanners, rulestools, scanner-install]
concepts: [project-initialization, project-setup, zero-literal, slint-build-scan, build-time-enforcement, documentation]
requires: [global/initialize.md, slint/states.md, slint/validation.md, uiux/tokens.md, rust/init.md]
related: [slint/README.md, slint/themes.md, slint/globals.md]
keywords: [init, cargo, build.rs, rustscanners, slintscanners, rustdocumenter, tokens, zero-literal, install, cargo-scan, build-scan, theme, globals, state, doc-comment, man, viewer]
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

## Step 1 — Unified Build Scanners

**CRITICAL: Build-time scanners run during `cargo build` — configure them before writing UI code**

The Rust scanners are now unified in the `RulesTools` workspace. Ensure `Cargo.toml` has:

```toml
[build-dependencies]
rulestools-documenter = { git = "https://github.com/lpmwfx/RulesTools" }
rulestools-scanner    = { git = "https://github.com/lpmwfx/RulesTools" }
slint-build           = "1"
```

Create or update `build.rs`:

```rust
// build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    rulestools_documenter::document_project(); // AI: auto-generates /// for undocumented pub items
    rulestools_scanner::scan_project();        // Rust + Slint: zero-literal, naming, tokens, etc.

    slint_build::compile("ui/main.slint")?;
    Ok(())
}
```

Ensure `proj/rulestools.toml` includes both languages:

```toml
[scan]
languages = ["rust", "slint"]
```

---

**VITAL RULE: Both scanners must be available before first `cargo build`**
RULE: `cargo build` must pass both scanners with zero violations
RULE: Both Rust and Slint checks run via `rulestools_scanner::scan_project()` in the same `build.rs`
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

Build should succeed with zero scanner warnings. If violations appear, fix them before writing more UI.

---

RULE: Steps 1–4 run in one session — do not leave initialization partial
RULE: Definition folders exist before any UI components are written
RULE: First `cargo build` after init must be clean (zero violations)
BANNED: Writing Slint components before rulestools scanner is configured
BANNED: Hardcoding colors, sizes, or durations in component files


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
