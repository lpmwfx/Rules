---
tags: [uiux, file-structure, folder-by-feature, organisation, ui-layout]
concepts: [file-organisation, feature-folders, ui-structure]
requires: [global/topology.md, uiux/components.md]
related: [uiux/state-flow.md]
keywords: [folder, feature, screen, area, file, organisation, src-ui, shared, co-locate, promote]
layer: 2
---
# UI File Structure

> Folders by feature — each folder is a UI area, each file is one component

---

VITAL: UI files are organised in folders per feature/screen area — not by type
RULE: One folder per UI area or screen
RULE: One component per file — never dump multiple components in one file
RULE: Folder name matches the area or screen it represents
RULE: Sub-components used only in one area live in that area's folder
RULE: Shared components used in 2+ areas live in `src/ui/shared/`
BANNED: Flat `ui/` folder with all components at the same level
BANNED: Type-based folders (`src/ui/buttons/`, `src/ui/cards/`) — use feature folders
BANNED: Multiple independent components in one file

## Canonical Layout

```
src/ui/
├── shared/              ← reusable components (used in 2+ areas)
│   ├── Avatar.*
│   ├── LoadingSpinner.*
│   └── ActionButton.*
├── home/                ← feature area
│   ├── HomeScreen.*     ← top-level screen entry point
│   ├── FeedList.*       ← sub-component, home only
│   └── FeedItem.*       ← sub-component, home only
├── settings/
│   ├── SettingsScreen.*
│   ├── ThemeSection.*
│   └── ProfileSection.*
└── auth/
    ├── LoginScreen.*
    └── PasswordField.*
```

RULE: Screen file is the entry point — it composes from sub-components in its folder
RULE: When a component is needed in a second area → move it to `shared/`
RULE: Depth max 2: `src/ui/<area>/<file>` — no deeper nesting of folders

## Promotion Rule

```
Step 1 — component lives in one area:
  src/ui/home/Avatar.*

Step 2 — settings/ also needs it → promote:
  src/ui/shared/Avatar.*

No duplication — one canonical location at all times.
```

BANNED: Copying a component into a second folder — promote to shared instead

## File Extensions by Toolkit

| Toolkit | Component file |
|---------|---------------|
| React / SolidJS | `UserCard.tsx` |
| Svelte | `UserCard.svelte` |
| Compose | `UserCard.kt` |
| QML | `UserCard.qml` |
| GTK4 / Python | `user_card.py` + `user_card.ui` |
| Slint | `UserCard.slint` |
| SwiftUI | `UserCard.swift` |

RULE: Toolkit template files (`.ui`, `.blueprint`) co-locate with their code file — same folder
RULE: File name = component name — no suffix like `UserCardComponent` or `UserCardView`

RESULT: Any developer can find `SettingsScreen` in `src/ui/settings/` without searching
REASON: Feature folders make the UI structure self-documenting — the folder IS the navigation map
