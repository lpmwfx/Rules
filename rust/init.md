---
tags: [rust, init, initialize, bootstrap, setup, new-project, build-scanners, rustscanners, slintscanners, rustdocumenter, scanner-install]
concepts: [project-initialization, project-setup, zero-literal, rust-build-scan, build-time-enforcement, documentation]
requires: [global/initialize.md, rust/constants.md, rust/modules.md]
related: [rust/README.md, project-files/project-file.md, project-files/rules-file.md, slint/init.md]
keywords: [rust, init, cargo, build.rs, rustscanners, slintscanners, rustdocumenter, state, zero-literal, install, cargo-scan, build-scan, doc-comment, man, viewer]
layer: 2
---
# Rust Project Initialization

> Run this INSTEAD OF improvising — every Rust project starts here

---

VITAL: Run this sequence top to bottom — no skipping, no reordering
VITAL: Ask the user for: project name, binary or library, GUI framework (if any)
VITAL: Do not create code files until proj/ is complete

---

## Step 0 — Decide structure (ask user)

```
Questions to ask before touching the filesystem:
1. Project name?          (e.g. my-app)
2. Type?                  Binary / Library / Workspace
3. GUI framework?         Slint / egui / none
4. Async runtime?         tokio / async-std / none
```

---

## Step 1 — Scaffold project

```bash
cargo init my-app && cd my-app
# or: cargo new my-app --lib
```

---

## Step 2 — Set up Build Scanners

**CRITICAL: Build-time scanners run during `cargo build` — configure them before writing code**

### 2.1 — Add scanner crates to Cargo.toml

```toml
[build-dependencies]
rustscanners  = { git = "https://github.com/lpmwfx/RustScanners" }
slintscanners = { git = "https://github.com/lpmwfx/SlintScanners" }  # if using Slint UI
```

### 2.2 — Install RustDocumenter binary

```bash
cargo install --git https://github.com/lpmwfx/RustDocumenter rustdocumenter
```

### 2.3 — Create build.rs

```rust
// build.rs
fn main() {
    rustscanners::scan_project();   // Rust: zero-literal, unwrap, naming, threading, doc-comments, etc.
    slintscanners::scan_project();  // Slint: zero-literal, tokens, structure, events (if using Slint)
}
```

### 2.4 — Create proj/rulestools.toml

```toml
[scan]
languages = ["rust", "slint"]   # remove "slint" if not using Slint UI

[project]
deny = false                     # Set to true before release
```

---

**VITAL RULE: All scanners must be installed before first `cargo build`**
RULE: `deny = false` during development, `deny = true` before release
RULE: `cargo build` must pass all scanners with zero violations
RULE: Never commit code that violates scanner rules

---

## Step 3 — Create state folder

All named values live in `src/state/` — one file per concern.

```bash
mkdir -p src/state
```

```rust
// src/state/mod.rs
pub mod sizes;
pub mod durations;
pub mod limits;
pub mod paths;
```

```rust
// src/state/sizes.rs
pub const BUF_SIZE: usize = 1024;
```

```rust
// src/state/durations.rs
pub const CONNECT_TIMEOUT_SECS: u64 = 30;
pub const RETRY_DELAY_MS: u64 = 500;
```

```rust
// src/state/limits.rs
pub const MAX_RETRIES: u32 = 3;
```

```rust
// src/state/paths.rs
pub const CONFIG_FILE: &str = "config.toml";
```

RULE: Format is open — `.rs` with `const`, `.toml`, `.json`, `.yaml` all valid
RULE: One file per concern — don't mix sizes with durations
RULE: Gateway loads non-Rust formats into `_cfg` structs

---

## Step 5 — Create .gitignore

```gitignore
/target
```

---

## Step 6 — Verify

```bash
cargo build
rustdocumenter        # AI auto-generates /// doc comments for all undocumented pub items
rustdocumenter check .
```

`cargo build` must produce zero scanner violations. `rustdocumenter` (no args) auto-generates missing `///` docs via AI. `rustdocumenter check` exits 0 only when all `pub` items have `///` doc comments.

---

RULE: Steps 1–6 run in one session — do not leave initialization partial
RULE: `src/state/` exists before any business logic is written
RULE: First `cargo build` after init must be clean (zero violations)
BANNED: Writing code before RustScanners is installed
BANNED: Hardcoding values in function bodies — use `src/state/` from day one
BANNED: Adding `pub` items without `///` doc comments
