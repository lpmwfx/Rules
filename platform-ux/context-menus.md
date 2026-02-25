---
tags: [platform-ux, context-menus, right-click, ui]
concepts: [ui-patterns, interaction]
related: [platform-ux/keyboard.md]
keywords: [context-menu, right-click, actions]
layer: 5
---
# Context Menus

> Right-click menus, primary menu, and minimum required items

---

## General Rules

RULE: Right-click (secondary click) MUST show context menu if relevant actions exist
RULE: Context menu MUST also be accessible via `Shift+F10` or `Menu` key
RULE: Long press on touch = right-click equivalent
RULE: Menus should contain 3–12 items
RULE: Label commands with verbs: "Open", "Copy", "Delete"
RULE: Group related items with separators
RULE: Items must have access keys (underlined letter)
BANNED: Nested submenus — flat structure only

## Terminal Context Menu (Minimum Required)

| Item | Shortcut |
|---|---|
| Copy | `Ctrl+Shift+C` |
| Paste | `Ctrl+Shift+V` |
| --- | |
| Select All | |
| --- | |
| Clear Terminal | |

## File Tree Context Menu (Minimum Required)

| Item | Notes |
|---|---|
| Open | Default action |
| Open in Terminal | For directories |
| --- | |
| Copy Path | Absolute path to clipboard |
| Copy Relative Path | Relative path to clipboard |

## Primary Menu (Hamburger) Required Items

RULE: Every app MUST include in the primary menu:
- Keyboard Shortcuts (`Ctrl+?`)
- Preferences (`Ctrl+,`) — if app has settings
- Help (`F1`) with "Report Issue / Request Feature"
- About [AppName]

BANNED: Close/Quit in the primary menu
