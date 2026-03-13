---
tags: [rust, init, initialize, bootstrap, setup, new-project, rustscanners]
concepts: [project-initialization, project-setup, zero-literal, rust-build-scan]
requires: [global/initialize.md, rust/constants.md, rust/modules.md]
related: [rust/README.md, project-files/project-file.md, project-files/rules-file.md]
keywords: [rust, init, cargo, build.rs, rustscanners, state, zero-literal, install, cargo-scan, build-scan]
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

## Step 2 — Install RustScanners

Zero-literal enforcement runs during every `cargo build`.

```bash
curl -sSf https://raw.githubusercontent.com/lpmwfx/RustScanners/main/install.sh | bash
```

This does three things:
1. Adds `rustscanners` as `[build-dependencies]` in `Cargo.toml`
2. Creates `build.rs` calling `rustscanners::scan_project()`
3. Creates `proj/rulestools.toml` with default scanner config

RULE: RustScanners is installed at project creation — not added later
RULE: `deny = false` during development, `deny = true` before release

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

## Step 4 — Install rustdocumenter

Documentation generator — scans `///` doc comments, writes `man/` + `proj/ISSUES`.

```bash
cargo install --force --git https://github.com/lpmwfx/RustDocumenter rustdocumenter
```

Then generate initial documentation (empty `man/` is normal at project start):

```bash
rustdocumenter gen .
```

`proj/ISSUES` is created whenever public items lack `///` doc comments.
`man/` contains one `.md` + `.json` per source file — readable by AI and the `rustdoc-viewer` GUI.

RULE: Add `///` doc comments to every `pub` item — see `rust/docs.md`
RULE: Run `rustdocumenter gen` after adding pub items to keep `man/` current

---

## Step 5 — Create .gitignore

```gitignore
/target
```

---

## Step 6 — Verify

```bash
cargo build
rustdocumenter check .
```

Both must succeed. `cargo build` must produce zero scanner violations. `rustdocumenter check` exits 0 only when all `pub` items have `///` doc comments.

---

RULE: Steps 1–6 run in one session — do not leave initialization partial
RULE: `src/state/` exists before any business logic is written
RULE: First `cargo build` after init must be clean (zero violations)
BANNED: Writing code before RustScanners is installed
BANNED: Hardcoding values in function bodies — use `src/state/` from day one
BANNED: Adding `pub` items without `///` doc comments
