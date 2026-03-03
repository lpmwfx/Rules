---
tags: [pal, platform, abstraction, stateless, trait, interface, cross-platform]
concepts: [platform-abstraction, trait-interface, multiple-implementations, dependency-inversion]
requires: [global/topology.md, global/app-model.md]
feeds: [pal/traits.md]
related: [gateway/io.md, core/design.md, uiux/theming.md]
keywords: [pal, trait, FilePal-pal, WindowPal-pal, AppearancePal-pal, platform, stateless, cfg-target-os, injection, implementation, Windows, macOS, Linux, iOS, Android, Web]
layer: 3
---
# PAL Design

> One trait per concern, one implementation per platform — platform code lives nowhere else

---

VITAL: PAL is stateless — it delegates to platform APIs, returns a result, holds nothing
VITAL: Platform-specific code (`#[cfg(target_os = ...)]`) lives ONLY inside PAL implementations
RULE: One trait interface per concern — `FilePal_pal`, `WindowPal_pal`, `AppearancePal_pal`
RULE: Core and Gateway receive PAL as `Arc<dyn SomePal_pal>` — never import concrete implementations
RULE: Each target platform has one PAL implementation struct tagged `_pal`
RULE: PAL implementations are the ONLY place that imports OS-specific crates (`winapi`, `objc2`, `libc`)
BANNED: `#[cfg(target_os)]` outside `src/pal/`
BANNED: PAL implementations holding mutable state — stateless delegate only
BANNED: Business logic or data transformation inside PAL — it executes, not decides
BANNED: `_pal` file importing a `_core` type — PAL must not know domain exists
BANNED: `_pal` file importing a `_adp` type — PAL must not know Adapter exists
BANNED: `_pal` file importing a `_ui` type — PAL must not know UI exists
BANNED: `_pal` file importing a `_gtw` type — PAL must not know Gateway exists

## Platform is an implementation detail

```
Trait (in src/pal/traits.rs)     Implementations (in src/pal/)
─────────────────────────────    ────────────────────────────────────
FilePal_pal                  →   WindowsFilePal_pal   (winapi paths)
                                 MacosFilePal_pal     (NSFileManager)
                                 LinuxFilePal_pal     (XDG base dirs)
                                 WebFilePal_pal       (localStorage / OPFS)

AppearancePal_pal            →   WindowsAppearancePal_pal  (registry)
                                 MacosAppearancePal_pal    (NSAppearance)
                                 LinuxAppearancePal_pal    (freedesktop portal)
```

RULE: Adding a new platform = adding one new `_pal` implementation struct — zero changes to Core or Gateway
RULE: iOS is a PAL implementation (`IosFilePal_pal`, `IosWindowPal_pal`) — not a separate architecture layer
RULE: Android is a PAL implementation — same pattern

## Injection pattern

```rust
// PAL constructed at startup, injected into Gateway and Core
fn main() {
    let pal: Arc<dyn FilePal_pal> = Arc::new(platform_pal());  // selects impl at compile time
    let (cfg, state) = GatewayState_gtw::init(pal.clone())?;
    let core = SchemaCore_core::new(pal.clone(), state.core);
    // ...
}

#[cfg(target_os = "windows")]
fn platform_pal() -> impl FilePal_pal { WindowsFilePal_pal::new() }

#[cfg(target_os = "macos")]
fn platform_pal() -> impl FilePal_pal { MacosFilePal_pal::new() }

#[cfg(target_os = "linux")]
fn platform_pal() -> impl FilePal_pal { LinuxFilePal_pal::new() }
```

RULE: Platform selection (`#[cfg]`) happens in `main.rs` — constructs the right PAL, injects via trait
RULE: After construction, the rest of the app sees only `Arc<dyn FilePal_pal>` — no platform conditionals

RESULT: The entire app compiles and runs on a new platform by adding one PAL implementation
REASON: Platform coupling is contained — everything else is portable
