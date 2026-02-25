---
tags: [rust, gtk4, gui, relm4]
concepts: [gtk4, gui]
requires: [rust/ownership.md]
keywords: [relm4, gtk4-rs, widget]
layer: 4
---
# GTK4 (gtk-rs)

> glib::clone!, composite templates, weak refs

---

RULE: `glib::clone!` for closures capturing Rc/Arc
RULE: Composite templates for complex widgets
RULE: Weak references in signal handlers
RULE: Actions for keyboard shortcuts

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
