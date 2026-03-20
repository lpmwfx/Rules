---
tags: [scanner, rulestools, build-rs, topology, workspace, flat]
concepts: [scanner-topology, scan-root, two-tier-scanning]
requires: [rust/workspace.md]
related: [global/topology.md]
keywords: [rulestools-toml, topology-flat, topology-workspace, scan-root, build-rs, rulestools-scanner, scan-project, cargo-build, deny]
layer: 3
binding: true
---
# Scanner Configuration — `proj/rulestools.toml`

> Workspace topology declared in config so scanners know how to walk the project

---

Workspace topology must be declared explicitly so scanners know how to walk the project.
Every member with Rust code has its own `build.rs` — this ensures that building a single crate
(e.g. `cargo build -p core`) still triggers scanning of that crate's source.

```toml
# proj/rulestools.toml — at workspace root (shared by all members)

[scan]
languages = ["rust", "slint"]

[project]
# Each member's build.rs reads this file.
# Library crates use "flat" — they scan only their own src/.
# The scan root (apps/desktop) uses "workspace" — it also scans the full workspace.
# topology is set per-crate by overriding in the member's own proj/rulestools.toml,
# or the workspace root value is used as default.

[scan]
deny = false             # set true before release
```

**What `topology` controls:**

| Value | Rust files | Slint files |
|---|---|---|
| `"flat"` (default) | scans own `src/` only | scans own `ui/` or `src/` only |
| `"workspace"` | scans all `apps/*/src/` + `crates/*/src/` | scans all `apps/*/ui/` + `apps/*/src/` |

**Two-tier scanning — flat + workspace are additive, not exclusive:**

```
cargo build -p core
  └─ crates/core/build.rs → topology = "flat" → scans crates/core/src/ only

cargo build -p desktop
  └─ apps/desktop/build.rs → topology = "workspace" → scans entire workspace

cargo build (full)
  └─ all build.rs files run:
       crates/core/build.rs    → flat → scans itself
       crates/adapter/build.rs → flat → scans itself
       crates/pal/build.rs     → flat → scans itself
       crates/gateway/build.rs → flat → scans itself
       apps/desktop/build.rs   → workspace → scans everything (cross-crate checks)
       apps/cli/build.rs       → flat → scans itself
```

RULE: Every member crate that contains Rust source code has its own `build.rs` calling `rulestools_scanner::scan_project()`
RULE: Library crates (`crates/*`) use `topology = "flat"` — they scan only their own `src/`
RULE: The scan root (`apps/desktop`) uses `topology = "workspace"` — it supplements flat scans with cross-workspace visibility
RULE: `apps/desktop` is always the scan root — it is always built as part of `cargo build`
BANNED: A member crate with Rust source and no `build.rs` — building it individually would skip all scanning

```rust
// crates/core/build.rs — flat: scans only crates/core/src/
fn main() {
    rulestools_scanner::scan_project();   // reads proj/rulestools.toml, topology = "flat"
}

// apps/desktop/build.rs — workspace: scans all members + slint files
fn main() {
    rulestools_scanner::scan_project();   // topology = "workspace" → sees entire workspace
    rulestools_scanner::scan_project();  // topology = "workspace" → finds all .slint files
}
```

The scan root's `proj/rulestools.toml` sets `topology = "workspace"`. All other members either have
their own `proj/rulestools.toml` with `topology = "flat"`, or rely on the default (`"flat"`).

RESULT: Building any single crate scans its source; building the scan root scans everything
REASON: Without per-member build.rs, `cargo build -p core` would compile without any rule enforcement


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
