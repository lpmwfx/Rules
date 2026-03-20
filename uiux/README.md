---
tags: [uiux, ui-paradigm, declarative, cross-platform, platform-ux]
concepts: [ui-paradigm, component-design, cross-platform-ui, platform-ux]
related: [uiux/tokens.md, uiux/components.md, uiux/file-structure.md, uiux/state-flow.md, uiux/theming.md, uiux/keyboard.md, uiux/checklist.md, uiux/help-about.md, global/topology.md, global/adapter-layer.md, global/config-driven.md, global/persistent-state.md]
layer: 6
---
# UI/UX Rules

> Perfect UI per platform — structure, state flow, and platform behaviour

---

Three goals:
1. **Split UI code** so a change in one area cannot accidentally break another
2. **Correct UX per platform** — use native widgets, icons, and interaction patterns
3. **Declarative** — UI describes *what* to show; values, state, and behavior live outside components

Applies to all GUI types: WA, PWA, Desktop (GNOME, KDE, macOS, Windows), Mobile (Android, iOS), TUI.

## Core Invariants

VITAL: UI components contain **zero literal values** — every color, size, spacing is a named token
VITAL: UI components are **stateless** — state flows in from Adapter, events flow out
VITAL: All apps **persist state** on close and restore on launch — users return to where they left off
RULE: One file per concern — component, token group, state type, feature area each get their own file

## Paradigm — how to structure UI code

| File | Topic |
|------|-------|
| [mother-child.md](mother-child.md) | Mother owns all state and layout — children are stateless modules |
| [tokens.md](tokens.md) | Design tokens — no magic values in components |
| [components.md](components.md) | One file, one component, one responsibility |
| [file-structure.md](file-structure.md) | Folders by feature area — isolation by design |
| [state-flow.md](state-flow.md) | State in from Adapter, events out to Adapter |

## Menus — Rust + Slint per platform

| File | Topic |
|------|-------|
| [menus-slint.md](menus-slint.md) | Architecture: muda + shared menu definition |
| [menus-macos.md](menus-macos.md) | macOS — NSMenu via muda |
| [menus-windows.md](menus-windows.md) | Windows — Win32 menu via muda |
| [menus-gnome.md](menus-gnome.md) | GNOME — Slint HeaderBar + hamburger PopupMenu |
| [menus-kde.md](menus-kde.md) | KDE — hamburger default, optional global menu |

## Menus — Other toolkits and platforms

| File | Topic |
|------|-------|
| [menus-android.md](menus-android.md) | Android — Bottom Navigation + Top App Bar overflow (Compose) |
| [menus-ios.md](menus-ios.md) | iOS — TabView + toolbar items (SwiftUI) |
| [menus-qt6.md](menus-qt6.md) | Qt6 — QMenuBar / QML MenuBar, platform-adaptive |

## Platform behaviour — UX per target

| File | Topic |
|------|-------|
| [help-about.md](help-about.md) | About dialog, license, shortcuts window — per platform |
| [keyboard.md](keyboard.md) | Standard keyboard shortcuts and navigation |
| [context-menus.md](context-menus.md) | Context menus and primary menu |
| [drag-drop.md](drag-drop.md) | Drag and drop behaviour |
| [pointer-touch.md](pointer-touch.md) | Pointer and touch interaction |
| [theming.md](theming.md) | Auto light/dark system appearance |
| [issue-reporter.md](issue-reporter.md) | Issue reporter integration |
| [checklist.md](checklist.md) | Pre-ship verification checklist |

## Core Principles

1. **Mother–child** — one root owns all state and layout; children are stateless modules that fill their slot
2. **Token-only values** — components reference token names; token files hold all literal values
3. **Isolated by default** — each UI area lives in its own folder; changes are contained
4. **One responsibility per file** — a fix touches exactly one file, nothing else breaks
5. **Stateless components** — state comes from Adapter, never lives in UI
6. **Platform-native** — use platform widgets, icons, and shortcuts; do not fight the OS
7. **Declarative** — describe what to show; token and config files describe how it looks
8. **State persists** — window size, scroll, selection saved on close, restored on launch

State persistence: [global/persistent-state.md](../global/persistent-state.md)
Config-driven values: [global/config-driven.md](../global/config-driven.md)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
