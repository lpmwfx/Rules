---
tags: [platform-ux, pointer, touch, interaction]
concepts: [interaction, accessibility]
related: [platform-ux/drag-drop.md]
keywords: [pointer-events, touch, gesture]
layer: 5
---
# Pointer and Touch

> Click behavior, hover rules, touch interaction

---

## Click Behavior

RULE: Single click to activate — GNOME does not use double-click for primary actions
RULE: Click targets must be large enough for comfortable use
BANNED: Simultaneous multi-button presses
BANNED: Referencing specific devices in UI text (no "click", use "select"/"activate")

## Hover

RULE: Hover MUST NOT reveal essential actions or information (inaccessible on touch)
RULE: Tooltips are acceptable (supplementary info only)
BANNED: Hover-only menus or buttons

## Touch

RULE: Long press = right-click (context menu)
RULE: Two-finger gestures available for app use (pinch zoom, two-finger scroll)
BANNED: Three/four-finger gestures — reserved for system
