---
tags: [rust, workspace, cargo, cross-platform, multi-platform, crates, apps, desktop, mobile, pal, topology, android, ios, kde, gnome, windows, macos, steam, sailfish, virtual-workspace, multi-target, rulestools, scanner, build-rs, topology-config]
concepts: [workspace-topology, crate-layout, cross-platform-architecture, platform-abstraction, cargo-dag-enforcement, multi-target, scanner-topology, scan-root]
requires: [global/topology.md, rust/modules.md, pal/design.md]
feeds: [rust/init.md, pal/traits.md]
related: [global/topology.md, global/mother-tree.md, pal/design.md, pal/traits.md, uiux/menus-kde.md, uiux/menus-gnome.md, uiux/menus-windows.md, uiux/menus-macos.md, uiux/menus-ios.md, uiux/menus-android.md]
keywords: [workspace, crates, apps, desktop, mobile, android, ios, kde, gnome, windows, macos, steam, sailfish, pal, cdylib, jni, ffi, cfg, features, virtual-workspace, member, multi-binary, workspace-dependencies, cargo-toml, cross-compile, binary, library, rulestools-toml, topology-flat, topology-workspace, scan-root, build-rs, rustscanners, slintscanners]
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

---

## PAL — Multi-Platform Structure

All platform-specific code lives in `crates/pal/`. Traits are defined once; implementations are per-platform.

```
crates/pal/src/
├── mod.rs              ← pub use traits; selects implementation via #[cfg]
├── traits.rs           ← FilePal_pal, WindowPal_pal, AppearancePal_pal, NotifyPal_pal
├── desktop/
│   ├── windows.rs      ← #[cfg(target_os = "windows")]
│   ├── kde.rs          ← #[cfg(all(target_os = "linux", feature = "kde"))]
│   ├── gnome.rs        ← #[cfg(all(target_os = "linux", feature = "gnome"))]
│   ├── macos.rs        ← #[cfg(target_os = "macos")]
│   ├── steam.rs        ← #[cfg(feature = "steam")]
│   └── sailfish.rs     ← #[cfg(target_os = "nemo")]
├── android.rs          ← #[cfg(target_os = "android")]
├── ios.rs              ← #[cfg(target_os = "ios")]
└── test_pal.rs         ← in-memory test double — used by Core + Gateway unit tests
```

Platform selection happens once in each app's `main.rs` (or `lib.rs` for mobile):

```rust
// apps/desktop/src/main.rs
fn main() {
    let pal = Arc::new(platform_pal());
    // inject into gateway, core, adapter...
}

#[cfg(target_os = "windows")]
fn platform_pal() -> impl FilePal_pal { WindowsFilePal_pal::new() }

#[cfg(all(target_os = "linux", feature = "kde"))]
fn platform_pal() -> impl FilePal_pal { KdeFilePal_pal::new() }

#[cfg(all(target_os = "linux", feature = "gnome"))]
fn platform_pal() -> impl FilePal_pal { GnomeFilePal_pal::new() }

#[cfg(target_os = "macos")]
fn platform_pal() -> impl FilePal_pal { MacosFilePal_pal::new() }
```

RULE: Adding a new platform target = adding one PAL implementation + one `#[cfg]` arm in the app's entry point
RULE: Zero changes to `crates/core`, `crates/gateway`, or `crates/adapter` when adding a platform
BANNED: `#[cfg(target_os)]` in any crate other than `crates/pal` and app entry points

---

## Mobile Targets (Android + iOS)

Mobile targets are library crates, not binaries. The Rust workspace compiles to a native library; the mobile UI (Kotlin/Compose or SwiftUI) links against it via FFI.

```toml
# apps/android/Cargo.toml
[lib]
crate-type = ["cdylib"]   # .so for Android JNI

[dependencies]
adapter = { path = "../../crates/adapter" }
jni     = "0.21"

# apps/ios/Cargo.toml
[lib]
crate-type = ["staticlib"]  # .a for iOS linking

[dependencies]
adapter = { path = "../../crates/adapter" }
```

```rust
// apps/android/src/lib.rs
#[no_mangle]
pub extern "C" fn Java_com_example_app_RustBridge_init(env: JNIEnv, _: JClass) {
    // initialize adapter, gateway, pal — expose events via JNI
}
```

RULE: Android and iOS app crates are `_ui` layer — they surface Adapter state to native UI
RULE: The native mobile UI (Kotlin/Swift) is never part of the Rust workspace — it lives in a separate project that links the compiled library
RULE: Mobile PAL implementations (`android.rs`, `ios.rs`) handle platform paths, appearance, notifications

---

## Multi-Binary Install Pitfall

When a workspace contains multiple binaries, `cargo install` requires an explicit crate name:

```bash
# WRONG — ambiguous in a multi-binary workspace
cargo install --git https://github.com/org/my-app

# CORRECT — specify the crate
cargo install --git https://github.com/org/my-app desktop
cargo install --git https://github.com/org/my-app cli
```

RULE: Document the exact `cargo install` command per binary in the project's INSTALL file
BANNED: `cargo install` without a crate name in multi-binary workspaces — it will fail or pick wrong binary

---

## Scanner Configuration — `proj/rulestools.toml`

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

[rustscanners]
deny = false             # set true before release

[slintscanners]
deny = false
```

**What `topology` controls:**

| Value | RustScanners | SlintScanners |
|---|---|---|
| `"flat"` (default) | scans own `src/` only | scans own `ui/` or `src/` only |
| `"workspace"` | scans all `apps/*/src/` + `crates/*/src/` | scans all `apps/*/ui/` + `apps/*/src/` |

**Two-tier scanning — flat + workspace are additive, not exclusive:**

```
cargo build -p core
  └─ crates/core/build.rs → topology = "flat" → scans crates/core/src/ only ✓

cargo build -p desktop
  └─ apps/desktop/build.rs → topology = "workspace" → scans entire workspace ✓

cargo build (full)
  └─ all build.rs files run:
       crates/core/build.rs    → flat → scans itself ✓
       crates/adapter/build.rs → flat → scans itself ✓
       crates/pal/build.rs     → flat → scans itself ✓
       crates/gateway/build.rs → flat → scans itself ✓
       apps/desktop/build.rs   → workspace → scans everything (cross-crate checks) ✓
       apps/cli/build.rs       → flat → scans itself ✓
```

RULE: Every member crate that contains Rust source code has its own `build.rs` calling `rustscanners::scan_project()`
RULE: Library crates (`crates/*`) use `topology = "flat"` — they scan only their own `src/`
RULE: The scan root (`apps/desktop`) uses `topology = "workspace"` — it supplements flat scans with cross-workspace visibility
RULE: `apps/desktop` is always the scan root — it is always built as part of `cargo build`
BANNED: A member crate with Rust source and no `build.rs` — building it individually would skip all scanning

```rust
// crates/core/build.rs — flat: scans only crates/core/src/
fn main() {
    rustscanners::scan_project();   // reads proj/rulestools.toml, topology = "flat"
}

// apps/desktop/build.rs — workspace: scans all members + slint files
fn main() {
    rustscanners::scan_project();   // topology = "workspace" → sees entire workspace
    slintscanners::scan_project();  // topology = "workspace" → finds all .slint files
}
```

The scan root's `proj/rulestools.toml` sets `topology = "workspace"`. All other members either have
their own `proj/rulestools.toml` with `topology = "flat"`, or rely on the default (`"flat"`).

---

RESULT: Platform support scales by adding PAL implementations — the shared crates are untouched
RESULT: All app surfaces (desktop GUI, CLI, MCP, Android, iOS) share identical Core, Gateway, and Adapter
REASON: Cargo-enforced DAG eliminates architecture drift — violations are compile errors, not code review findings
