---
tags: [pal, cross-platform, multi-platform, android, ios, windows, macos, kde, gnome, steam, sailfish]
concepts: [platform-abstraction, cross-platform-architecture, mobile-targets]
requires: [rust/workspace.md, global/topology.md]
feeds: [pal/traits.md]
related: [pal/design.md, rust/modules.md]
keywords: [pal, platform, cfg, target_os, android, ios, windows, macos, kde, gnome, steam, sailfish, cdylib, staticlib, jni, ffi, FilePal, WindowPal, test_pal]
layer: 3
---
# PAL — Multi-Platform Structure

> All platform-specific code lives in `crates/pal/` — traits defined once, implementations per-platform

---

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

RESULT: Platform support scales by adding PAL implementations — shared crates are untouched
REASON: `#[cfg]` outside PAL scatters platform knowledge and breaks the abstraction boundary


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
