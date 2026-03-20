---
tags: [pal, traits, FilePal, WindowPal, AppearancePal, interface, api]
concepts: [pal-traits, platform-interface, file-api, window-api, appearance-api]
requires: [pal/design.md]
related: [gateway/io.md, uiux/theming.md, slint/globals.md]
keywords: [FilePal-pal, WindowPal-pal, AppearancePal-pal, config-path, state-path, read-file, write-file, is-dark-mode, watch-appearance, window-size, window-position]
layer: 4
---
# PAL Traits

> The contracts between Core/Gateway and the platform — implement once per target

---

RULE: Every PAL trait method returns `Result<T, AppError_x>` — platform calls can always fail
RULE: Trait methods are narrow — one operation, no overloaded concerns
RULE: PAL traits live in `src/pal/traits.rs` — implementations in `src/pal/<platform>.rs`
RULE: Core and Gateway only call methods on these traits — never call OS APIs directly

## FilePal_pal — paths and IO

```rust
pub trait FilePal_pal: Send + Sync {
    /// Resolved path to a config file — e.g. ~/.config/<app>/config/<name>
    fn config_path(&self, name: &str) -> Result<PathBuf, AppError_x>;

    /// Resolved path to a state file — e.g. ~/.config/<app>/state/<name>
    fn state_path(&self, name: &str) -> Result<PathBuf, AppError_x>;

    fn read_file(&self, path: &Path)           -> Result<String, AppError_x>;
    fn write_file(&self, path: &Path, content: &str) -> Result<(), AppError_x>;
    fn file_exists(&self, path: &Path)         -> bool;
    fn create_dir_all(&self, path: &Path)      -> Result<(), AppError_x>;
}
```

## WindowPal_pal — window state

```rust
pub trait WindowPal_pal: Send + Sync {
    fn window_size(&self)               -> (u32, u32);
    fn window_position(&self)           -> (i32, i32);
    fn set_window_size(&self, w: u32, h: u32);
    fn set_window_position(&self, x: i32, y: i32);
    fn is_maximized(&self)              -> bool;
}
```

## AppearancePal_pal — system dark/light mode

```rust
pub trait AppearancePal_pal: Send + Sync {
    /// Read current system preference
    fn is_dark_mode(&self) -> bool;

    /// Subscribe to OS appearance changes — sends bool (is_dark) on change
    fn watch_appearance(&self, tx: std::sync::mpsc::Sender<bool>);
}
```

RULE: `watch_appearance` runs in its own thread — sends changes via channel, Adapter posts to UI via `invoke_from_event_loop` (see slint/threading.md)

## Test double pattern

```rust
// src/pal/test_pal.rs — used in Core unit tests
pub struct TestFilePal_pal {
    files: RefCell<HashMap<PathBuf, String>>,
}

impl FilePal_pal for TestFilePal_pal {
    fn config_path(&self, name: &str) -> Result<PathBuf, AppError_x> {
        Ok(PathBuf::from(format!("/test/config/{name}")))
    }
    fn read_file(&self, path: &Path) -> Result<String, AppError_x> {
        self.files.borrow().get(path)
            .cloned()
            .ok_or(AppError_x::FileNotFound(path.to_path_buf()))
    }
    fn write_file(&self, path: &Path, content: &str) -> Result<(), AppError_x> {
        self.files.borrow_mut().insert(path.to_path_buf(), content.to_string());
        Ok(())
    }
    // ...
}
```

RULE: Unit tests for Core and Gateway use `TestFilePal_pal` — no real disk, no platform dependency
RULE: Test doubles live in `src/pal/` alongside real implementations

RESULT: Core and Gateway are fully testable without a real OS or filesystem
REASON: `TestFilePal_pal` is a PAL implementation like any other — the trait makes it interchangeable


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
