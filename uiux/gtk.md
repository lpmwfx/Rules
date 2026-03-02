---
tags: [uiux, rust, gtk4, gui, relm4, linux]
concepts: [native-menus, gtk4, gui]
related: [uiux/menus-gnome.md, uiux/menus-kde.md, uiux/state-flow.md]
keywords: [relm4, gtk4-rs, widget, glib, clone, composite-template, signal-handler, weak-ref]
layer: 4
---
# GTK4 — Rust + gtk-rs

> glib::clone!, composite templates, weak refs, signal handlers

---

RULE: `glib::clone!` for closures capturing Rc/Arc — prevents strong-reference cycles in signal handlers
RULE: Composite templates for complex widgets — keep widget tree in .ui XML, not in Rust code
RULE: Weak references in signal handlers — never hold strong refs from signals
RULE: Actions for keyboard shortcuts — use `gio::SimpleAction`, not manual key handlers
RULE: State lives in a central `AppState_sta` struct — widgets only render, never own state

```rust
use gtk::prelude::*;
use glib::clone;
use std::rc::Rc;
use std::cell::RefCell;

let state = Rc::new(RefCell::new(0));
button.connect_clicked(clone!(@weak state => move |_| {
    *state.borrow_mut() += 1;
}));
```

## Stateless Widgets

VITAL: Widgets are stateless — all state lives in the Adapter layer, widgets only display
RULE: Widget callbacks emit events up — they do not mutate state directly
RULE: State mutations happen in the Adapter, results flow back to widgets via property bindings

```rust
// ❌ WRONG — widget owns state
struct MyWidget { count: i32 }

// ✓ CORRECT — widget renders state, emits events
struct MyWidget {}
impl MyWidget {
    fn render(&self, state: &AppState_sta) { /* display only */ }
    fn on_click(&self) { self.emit_event(UiEvent::Increment); }
}
```

## Composite Templates

RULE: One `.ui` file per widget — keeps the Rust file focused on behaviour only
RULE: Template children via `#[template_child]` — no manual widget lookup by ID

```rust
#[derive(CompositeTemplate, Default)]
#[template(resource = "/com/example/myapp/ui/main_window.ui")]
pub struct MainWindow {
    #[template_child]
    pub label: TemplateChild<gtk::Label>,
}
```

## Dependencies (Cargo.toml)

```toml
[dependencies]
gtk = { version = "0.9", package = "gtk4" }
glib = "0.20"
gio = "0.20"
thiserror = "2"
anyhow = "1"
serde = { version = "1", features = ["derive"] }
toml = "0.8"
tracing = "0.1"
tracing-subscriber = "0.3"

[dev-dependencies]
tempfile = "3"
```
