---
tags: [slint, scanners, add-scanners, build-dependency, rulestools, existing-project, setup]
concepts: [build-time-enforcement, documentation, zero-literal, project-setup]
requires: [rust/init.md]
related: [rust/docs.md]
keywords: [add scanners, existing project, build-dependencies, build.rs, rulestools-documenter, rustscanners, slintscanners, document_project, scan_project, cargo build]
layer: 2
---
# Add Scanners to an Existing Project

> Use this when a project exists but the scanner stack is missing or incomplete.
> For new projects start with `rust/init.md` instead.

---

VITAL: All three scanner calls must be present in build.rs — in this order
VITAL: rulestools-documenter runs FIRST — it fills in missing docs before scanners validate them
RULE: Never add scanners in the wrong order — docs before checks

---

## The unified scanner stack

| Crate | What it does | Required for |
|---|---|---|
| `rulestools-documenter` | AI generates `///` for undocumented pub items | All Rust projects |
| `rulestools-scanner` | Zero-literal, unwrap, naming, threading, doc checks + Slint checks | All Rust projects |

Both crates live in the unified `RulesTools` workspace on GitHub.

---

## Step 1 — Add to Cargo.toml

### Rust-only project

```toml
[build-dependencies]
rulestools-documenter = { git = "https://github.com/lpmwfx/RulesTools" }
rulestools-scanner    = { git = "https://github.com/lpmwfx/RulesTools" }
```

### Rust + Slint project

```toml
[build-dependencies]
rulestools-documenter = { git = "https://github.com/lpmwfx/RulesTools" }
rulestools-scanner    = { git = "https://github.com/lpmwfx/RulesTools" }
slint-build           = "1"
```

### Workspace projects

Add to the crate that owns Slint compilation (typically the `_adp` or `_ui` crate).
Only one crate in the workspace needs to drive the scanners.

---

## Step 2 — Update build.rs

### Rust-only

```rust
fn main() {
    rulestools_documenter::document_project(); // AI: fills in missing /// doc comments
    rulestools_scanner::scan_project();        // validates: zero-literal, naming, docs, etc.
}
```

### Rust + Slint

```rust
fn main() -> Result<(), Box<dyn std::error::Error>> {
    rulestools_documenter::document_project(); // AI: fills in missing /// doc comments
    rulestools_scanner::scan_project();        // validates: zero-literal, naming, docs, Slint tokens, etc.

    slint_build::compile("ui/main.slint")?;
    Ok(())
}
```

---

## Step 3 — Run

```bash
cargo build
```

**First build:** rulestools-documenter walks all `.rs` and `.slint` files, calls AI for each
undocumented pub item, and writes `///` comments directly into the source files.
The build then continues with the scanners validating the now-documented code.

**Subsequent builds:** docs are already present — rulestools-documenter writes nothing,
scanners validate, build is fast.

---

## Step 4 — Verify

```bash
rulestools-documenter check .
```

Exits 0 when all pub items have `///`. Exits 1 with a list of missing items if not.

---

## Diagnosing problems

**`cargo build` shows `rulestools-documenter: 0 items documented` but missing docs exist:**
```bash
rulestools-documenter diag
```
Tests Claude CLI and Codex CLI availability. Shows exact error if AI is unreachable.

**Scanner errors after first build:**
rulestools-documenter only adds `///` comments — it does not fix zero-literal or other violations.
Fix those manually.

---

RULE: rulestools-documenter must come before rulestools-scanner in build.rs — docs must exist before the doc check runs
RULE: One build.rs per workspace drives the scanners — don't split across crates
BANNED: Calling rulestools-scanner before rulestools-documenter — doc-required check will always fail on first build


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
