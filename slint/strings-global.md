---
tags: [strings, localization, global, i18n]
concepts: [localization-strings, slint-strings-global]
requires: [slint/globals.md]
related: [slint/string-comparisons.md, slint/rust-bridge.md]
keywords: [Strings, localization, in-property, language, save, cancel, delete, fallback, inject, Adapter]
layer: 3
---
# Slint Strings Global — Localization

> All user-visible UI text goes through `Strings` global — no hardcoded strings in components

---

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

RESULT: Language switch = re-inject Strings from a different file — zero component changes
REASON: Hardcoded strings in components make localization a search-and-replace nightmare
