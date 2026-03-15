---
tags: [rust, slint, scanners, add-scanners, build-dependency, rustdocumenter, rustscanners, slintscanners, existing-project, setup]
concepts: [build-time-enforcement, documentation, zero-literal, project-setup]
requires: [rust/init.md]
related: [slint/init.md, rust/docs.md, slint/docs.md]
keywords: [add scanners, existing project, build-dependencies, build.rs, rustdocumenter, rustscanners, slintscanners, document_project, scan_project, cargo build]
layer: 2
---
# Add Scanners to an Existing Project

> Use this when a project exists but the scanner stack is missing or incomplete.
> For new projects start with `rust/init.md` instead.

---

VITAL: All three scanner calls must be present in build.rs — in this order
VITAL: rustdocumenter runs FIRST — it fills in missing docs before scanners validate them
RULE: Never add scanners in the wrong order — docs before checks

---

## The complete scanner stack

| Crate | What it does | Required for |
|---|---|---|
| `rustdocumenter` | AI generates `///` for undocumented pub items | All Rust projects |
| `rustscanners` | Zero-literal, unwrap, naming, threading, doc checks | All Rust projects |
| `slintscanners` | Zero-literal, tokens, structure, events | Projects with Slint UI |

---

## Step 1 — Add to Cargo.toml

### Rust-only project

```toml
[build-dependencies]
rustdocumenter = { git = "https://github.com/lpmwfx/RustDocumenter" }
rustscanners   = { git = "https://github.com/lpmwfx/RustScanners" }
```

### Rust + Slint project

```toml
[build-dependencies]
rustdocumenter = { git = "https://github.com/lpmwfx/RustDocumenter" }
rustscanners   = { git = "https://github.com/lpmwfx/RustScanners" }
slintscanners  = { git = "https://github.com/lpmwfx/SlintScanners" }
slint-build    = "1"
```

### Workspace projects

Add to the crate that owns Slint compilation (typically the `_adp` or `_ui` crate).
Only one crate in the workspace needs to drive the scanners.

---

## Step 2 — Update build.rs

### Rust-only

```rust
fn main() {
    rustdocumenter::document_project(); // AI: fills in missing /// doc comments
    rustscanners::scan_project();       // validates: zero-literal, naming, docs, etc.
}
```

### Rust + Slint

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    rustdocumenter::document_project(); // AI: fills in missing /// doc comments
    rustscanners::scan_project();       // validates: zero-literal, naming, docs, etc.
    slintscanners::scan_project();      // validates: tokens, structure, events, etc.

    slint_build::compile("ui/main.slint")?;
    Ok(())
}
```

---

## Step 3 — Run

```bash
cargo build
```

**First build:** rustdocumenter walks all `.rs` and `.slint` files, calls AI for each
undocumented pub item, and writes `///` comments directly into the source files.
The build then continues with the scanners validating the now-documented code.

**Subsequent builds:** docs are already present — rustdocumenter writes nothing,
scanners validate, build is fast.

---

## Step 4 — Verify

```bash
rustdocumenter check .
```

Exits 0 when all pub items have `///`. Exits 1 with a list of missing items if not.

---

## Diagnosing problems

**`cargo build` shows `rustdocumenter: 0 items documented` but missing docs exist:**
```bash
rustdocumenter diag
```
Tests Claude CLI and Codex CLI availability. Shows exact error if AI is unreachable.

**Scanner errors after first build:**
rustdocumenter only adds `///` comments — it does not fix zero-literal or other violations.
Fix those manually.

---

RULE: rustdocumenter must come before rustscanners in build.rs — docs must exist before the doc check runs
RULE: One build.rs per workspace drives all three scanners — don't split across crates
BANNED: Calling rustscanners before rustdocumenter — doc-required check will always fail on first build
