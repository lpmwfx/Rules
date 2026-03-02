---
tags: [uiux, overview, ui-paradigm, declarative, cross-platform, platform-ux]
concepts: [ui-paradigm, component-design, cross-platform-ui, platform-ux]
related: [uiux/components.md, uiux/file-structure.md, uiux/state-flow.md, uiux/theming.md, uiux/keyboard.md, uiux/checklist.md, uiux/help-about.md, global/topology.md, global/adapter-layer.md]
layer: 6
---
# UI/UX Rules

> Perfect UI per platform — structure, state flow, and platform behaviour

---

Two goals:
1. **Split UI code** so a change in one area cannot accidentally break another
2. **Correct UX per platform** — use native widgets, icons, and interaction patterns

Applies to all GUI types: WA, PWA, Desktop (GNOME, KDE, macOS, Windows), Mobile (Android, iOS), TUI.

## Paradigm — how to structure UI code

| File | Topic |
|------|-------|
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

1. **Isolated by default** — each UI area lives in its own folder; changes are contained
2. **One responsibility per file** — a fix touches exactly one file, nothing else breaks
3. **Stateless components** — state comes from Adapter, never lives in UI
4. **Platform-native** — use platform widgets, icons, and shortcuts; do not fight the OS
5. **Declarative** — describe what to show, never how to mutate
