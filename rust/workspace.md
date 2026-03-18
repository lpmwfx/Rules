---
tags: [workspace, cargo, cross-platform, multi-platform, crates, apps, desktop, mobile, pal, topology, virtual-workspace, multi-target, rulestools, scanner, build-rs, topology-config]
concepts: [workspace-topology, crate-layout, cross-platform-architecture, cargo-dag-enforcement, multi-target, scanner-topology, scan-root]
requires: [global/topology.md, rust/modules.md, pal/design.md]
feeds: [rust/init.md, pal/traits.md, rust/pal-structure.md, rust/multi-binary.md, rust/scanner-config.md]
related: [global/topology.md, global/mother-tree.md, pal/design.md, pal/traits.md, uiux/menus-kde.md, uiux/menus-gnome.md, uiux/menus-windows.md, uiux/menus-macos.md, uiux/menus-ios.md, uiux/menus-android.md]
keywords: [workspace, crates, apps, desktop, mobile, pal, virtual-workspace, member, workspace-dependencies, cargo-toml, cross-compile, binary, library]
layer: 2
binding: true
---
# Rust Workspace Topology

> Any Rust project with more than one target uses this layout — no exceptions

---

VITAL: Any project that targets more than one platform OR ships more than one binary MUST use this workspace topology
VITAL: The 6-layer topology from `global/topology.md` maps directly to crates — DAG is now enforced by Cargo, not convention
AXIOM: `apps/` contains surfaces (what users run). `crates/` contains logic (what apps build on)
RULE: Root `Cargo.toml` is a virtual workspace — it has no `[package]` section
RULE: `workspace.dependencies` is the single source of truth for all dependency versions
RULE: Desktop binaries go in `apps/desktop/` and `apps/cli/`. Mobile targets go in `apps/android/` and `apps/ios/`
BANNED: `#[cfg(target_os)]` outside `crates/pal/` — platform selection happens only in PAL
BANNED: Duplicate dependency versions — if two members need the same crate, it goes in `[workspace.dependencies]`
BANNED: A library crate in `crates/` depending on a crate in `apps/` — dependency only flows inward

---

## Folder Layout

```
my-app/                         ← virtual workspace root
├── Cargo.toml                  ← [workspace] only — no [package]
├── Cargo.lock
├── apps/
│   ├── desktop/                ← [[bin]] Slint GUI (Windows, KDE, GNOME, macOS, Steam, Sailfish)
│   ├── cli/                    ← [[bin]] CLI / MCP server
│   ├── android/                ← [lib] cdylib — JNI bridge, linked by Kotlin/Compose
│   └── ios/                    ← [lib] staticlib — C FFI bridge, linked by SwiftUI
└── crates/
    ├── adapter/                ← _adp hub — coordinates all layers
    ├── core/                   ← _core pure business logic
    ├── gateway/                ← _gtw IO: loads config+state, saves at shutdown
    ├── pal/                    ← _pal platform abstraction — traits + per-platform impls
    └── shared/                 ← _x errors, results, shared traits
```

---

## Virtual Workspace `Cargo.toml`

```toml
[workspace]
members = [
    "apps/desktop",
    "apps/cli",
    "apps/android",
    "apps/ios",
    "crates/adapter",
    "crates/core",
    "crates/gateway",
    "crates/pal",
    "crates/shared",
]
resolver = "2"

[workspace.dependencies]
# Single source of truth — members inherit with `{ workspace = true }`
tokio        = { version = "1", features = ["full"] }
serde        = { version = "1", features = ["derive"] }
slint        = { version = "1" }
anyhow       = "1"
tracing      = "0.1"
```

---

## Member Categories

Three distinct kinds of workspace members:

| Folder | `crate-type` | Layer | Role |
|---|---|---|---|
| `apps/desktop` | `[[bin]]` | `_ui` | Slint GUI binary — desktop surfaces |
| `apps/cli` | `[[bin]]` | `_ui` | CLI / MCP binary — AI or terminal surface |
| `apps/android` | `[lib]` `cdylib` | `_ui` | JNI library — Kotlin/Compose links this |
| `apps/ios` | `[lib]` `staticlib` | `_ui` | C FFI library — SwiftUI links this |
| `crates/adapter` | `[lib]` | `_adp` | Hub — the only crate that depends on all others |
| `crates/core` | `[lib]` | `_core` | Pure logic — no IO, no platform, no UI |
| `crates/gateway` | `[lib]` | `_gtw` | IO only — reads/writes config and state |
| `crates/pal` | `[lib]` | `_pal` | Platform traits + per-target implementations |
| `crates/shared` | `[lib]` | `_x` | Errors, results, shared types |

---

## DAG Enforced by Cargo

The 6-layer import DAG from `global/topology.md` is now enforced structurally — a crate that violates the DAG fails to compile.

```toml
# crates/core/Cargo.toml — GOOD: core knows nothing above it
[dependencies]
shared = { path = "../shared" }
pal    = { path = "../pal" }
# adapter is NOT listed — Cargo prevents the violation

# crates/adapter/Cargo.toml — hub: depends on all internal layers
[dependencies]
core    = { path = "../core" }
gateway = { path = "../gateway" }
pal     = { path = "../pal" }
shared  = { path = "../shared" }

# apps/desktop/Cargo.toml — surface: depends only on adapter
[dependencies]
adapter = { path = "../../crates/adapter" }
slint   = { workspace = true }
```

RULE: `apps/*` crates depend only on `crates/adapter` — never on core, gateway, or pal directly
RULE: `crates/core` depends only on `crates/pal` and `crates/shared`
RULE: `crates/gateway` depends only on `crates/pal` and `crates/shared`
RESULT: A dependency violation is a compile error, not a convention violation

PAL structure and mobile targets: [rust/pal-structure.md](pal-structure.md)
Multi-binary install pitfall: [rust/multi-binary.md](multi-binary.md)
Scanner configuration: [rust/scanner-config.md](scanner-config.md)

---

RESULT: All app surfaces (desktop GUI, CLI, MCP, Android, iOS) share identical Core, Gateway, and Adapter
REASON: Cargo-enforced DAG eliminates architecture drift — violations are compile errors, not code review findings
