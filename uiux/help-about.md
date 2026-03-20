---
tags: [uiux, help, about, shortcuts-window, license, platform-ux]
concepts: [help-system, about-dialog, shortcuts-window, discoverability]
requires: [uiux/keyboard.md, uiux/context-menus.md]
feeds: [uiux/about-desktop.md, uiux/about-mobile.md, uiux/about-web.md]
related: [uiux/checklist.md, uiux/issue-reporter.md]
keywords: [about, help, license, shortcuts, author, website, F1, Ctrl+question, platform-native]
layer: 4
---
# Help, About, and Shortcuts

> Every GUI app must have About, a license, and a shortcuts overview — delivered natively per platform

---

VITAL: Every GUI app ships with an About dialog, a license, and a keyboard shortcuts overview
VITAL: Use the platform-native mechanism — never a custom dialog where a standard one exists
RULE: About is reached from the primary menu (hamburger) → "About [AppName]"
RULE: Shortcuts overview is reached via `Ctrl+?` and from the primary menu
RULE: Help is reached via `F1` — minimum: opens shortcuts window or a help view
RULE: About must contain: app name, version, short description, author name, website, license
BANNED: Shipping without About, license, or shortcuts overview
BANNED: Custom About dialog on platforms that provide a standard one (GNOME, macOS, KDE)

## Minimum Content — About

Every About dialog must show at minimum:

| Field | Example |
|-------|---------|
| App name | MyApp |
| Version | 1.2.0 |
| Short description | 1-2 sentences |
| Author / developer | Your Name |
| Website | https://yoursite.example |
| License | GPL-3.0 / MIT / EUPL-1.2 |
| Copyright year | © 2024-2026 |

Optional but recommended: source code link, issue tracker link, release notes.

## Minimum Content — Shortcuts Window

Shows all app-specific shortcuts grouped by category.
Platform-standard shortcuts (Ctrl+C, Ctrl+Q) may be omitted — users know them.

```
Navigation          Search              View
───────────         ───────             ────
Alt+Left  Back      Ctrl+F  Find        F9   Sidebar
Alt+Right Forward   Ctrl+G  Next        F11  Fullscreen
                    Esc     Close

[App-specific shortcuts grouped here]
```

RULE: Group shortcuts by function area, not by key
RULE: List only app-specific shortcuts — skip universal ones unless they are non-obvious
RULE: Update shortcuts window whenever a shortcut is added or removed

Platform implementations: [uiux/about-desktop.md](about-desktop.md) | [uiux/about-mobile.md](about-mobile.md) | [uiux/about-web.md](about-web.md)

## Checklist

Add to [checklist.md](checklist.md):

- [ ] About dialog opens from primary menu
- [ ] About contains: name, version, description, author, website, license
- [ ] Shortcuts window opens via `Ctrl+?` (desktop) or `?` (web)
- [ ] Shortcuts window lists all app-specific shortcuts grouped by category
- [ ] `F1` opens help or shortcuts (desktop platforms)
- [ ] License text accessible from About dialog

RESULT: Users can always discover what the app is, who made it, and how to use it efficiently
REASON: About + shortcuts are platform citizenship requirements — not optional polish


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
