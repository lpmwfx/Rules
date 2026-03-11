---
tags: [slint, globals, singletons, tokens, app-bridge, strings, theming]
concepts: [slint-globals, design-tokens, event-routing-global, localization]
requires: [slint/component-model.md, uiux/tokens.md]
feeds: [uiux/theming.md]
related: [slint/rust-bridge.md, global/config-driven.md, uiux/mother-child.md]
keywords: [global, singleton, Colors, Spacing, Type, Strings, AppBridge, in-property, ui-global, set-dark-mode, localization, per-instance, Theme, state-separation]
layer: 3
---
# Slint Globals

> One global per concern — tokens, strings, and bridge callbacks live in globals

---

RULE: Use globals for design tokens (`Theme`), localization strings (`Strings`), and shared event routing (`AppBridge`)
RULE: Each global is accessed from Rust via `ui.global::<GlobalName>()`
RULE: Globals are per-component-instance — re-register callbacks and re-inject values for each new window
RULE: Token globals use `out property` for computed values that read a single `in property` (e.g. `dark-mode`)
RULE: A consolidated `Theme` global is valid when it holds only design tokens — the test is "does it contain domain logic?"
BANNED: Domain state or business logic in globals — globals hold tokens, strings, and routing only

## Design token globals

See uiux/tokens.md for the full token system. Slint implementation uses one `global` per concern:

```slint
// ui/tokens/colors.slint
export global Colors {
    in property <bool>  dark-mode: false;            // Adapter injects via PAL on startup
    out property <color> bg-primary:   dark-mode ? #1a1a1a : #ffffff;
    out property <color> text-primary: dark-mode ? #f0f0f0 : #1a1a1a;
    out property <color> accent:       #4a90d9;
}

// ui/tokens/spacing.slint
export global Spacing {
    out property <length> xs:  4px;
    out property <length> sm:  8px;
    out property <length> md:  16px;
    out property <length> lg:  24px;
}
```

```rust
// Adapter injects dark-mode on startup (PAL reads OS preference)
ui.global::<Colors>().set_dark_mode(pal::appearance::is_dark_mode());
```

RULE: Only `Colors` global branches on `dark-mode` — components use `Colors.bg-primary`, never `if dark-mode`
RULE: Token files are the ONLY place literal hex/px values appear in `.slint` source

## Localization strings global

For apps with UI text, a `Strings` global lets Adapter inject the active language at startup:

```slint
// ui/tokens/strings.slint
export global Strings {
    in property <string> save:   "Gem";
    in property <string> cancel: "Annuller";
    in property <string> delete: "Slet";
}
```

```rust
// Adapter injects strings from language file (loaded by PAL/Gateway)
let lang = ui.global::<Strings>();
lang.set_save(strings.save.as_str().into());
lang.set_cancel(strings.cancel.as_str().into());
```

RULE: All user-visible UI text goes through `Strings` global — no hardcoded strings in components
RULE: Default values in `.slint` are the fallback language — always complete

## AppBridge — centralised event routing

`AppBridge` is a global that centralises all component callbacks in one place.
Components delegate to `AppBridge` instead of exposing callbacks up the tree.

```slint
// ui/globals/app-bridge.slint
export global AppBridge {
    callback collection-selected(string);   // collection id
    callback item-selected(string);         // item id
    callback save-requested(string);        // serialized payload
    callback delete-confirmed(string);      // item id
}

// In a component — delegate immediately, no logic:
Button {
    clicked => { AppBridge.save-requested(root.payload); }
}
```

```rust
// Adapter::init — register all AppBridge handlers in one place
let bridge = ui.global::<AppBridge>();

let ui_weak = ui.as_weak();
bridge.on_collection_selected(move |id| {
    if let Some(ui) = ui_weak.upgrade() {
        let items = core.load_items(id.as_str());
        ui.set_items(make_model(&items));
    }
});
```

RULE: `AppBridge` handlers are registered in `Adapter::init()` — same place as direct `ui.on_*()` handlers
RULE: Components delegate to `AppBridge` with a single call — no conditions, no logic in the callback body
RULE: All routing decisions live in the Adapter's `AppBridge` handlers, not in `.slint` files

RESULT: All event routing is in one Rust file — adding a new event means one handler, not a chain of re-exports
REASON: `AppBridge` eliminates callback bubbling through the component tree

## Globals and Mother–Child State Separation

Globals complement the mother-child pattern (see uiux/mother-child.md). The mother Window component owns state via `in-out property`, and the `Theme` global separates design tokens from layout — like CSS is separate from HTML.

```
ui/
├── globals/
│   └── theme.slint        ← design tokens (colors, spacing, sizes)
├── views/
│   ├── navbar.slint        ← stateless child (in property + callback)
│   └── workspace-view.slint
└── app-window.slint        ← mother (inherits Window, in-out property = state)
```

RULE: State (`in-out property`) lives only in the mother Window component
RULE: Design tokens (`out property`) live in globals — children reference `Theme.xyz`
RULE: Children never own state — they use `in property` to receive and `callback` to emit
RESULT: AI can edit a child file by reading only that file + the Theme global — no hidden state
REASON: Separating state (mother) from tokens (global) keeps both files small and focused
