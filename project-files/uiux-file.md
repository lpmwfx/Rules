---
tags: [uiux, gui, user-flows, accessibility, project-files, platform-ux, os-gui]
concepts: [ui-specification, user-flows, accessibility, platform-ux, os-gui-experience]
requires: [uiux/components.md, uiux/state-flow.md]
related: [uiux/README.md, uiux/file-structure.md, project-files/project-file.md, project-files/rules-file.md]
keywords: [layout, interaction, flow, uiux-file, UIUX, gui, platform, os, toolkit, component-conventions, accessibility]
layer: 2
---
# UIUX File

> UI/UX source of truth for this project — platform, architecture, flows, and conventions

---

## Quick Reference

- **Location:** `proj/UIUX`
- **Required:** ALL GUI projects — TUI, WA, PWA, Desktop, Mobile — no exceptions
- **Owner:** User defines vision — AI reads before any GUI work, writes conventions as discovered
- **Read by AI:** Before touching any UI file, every session

VITAL: No GUI work without reading proj/UIUX first — no exceptions
VITAL: proj/UIUX is the UI/UX source of truth — not code comments, not README, not memory
RULE: AI reads proj/UIUX at session start alongside proj/PROJECT and proj/RULES
RULE: AI updates proj/UIUX when UI/UX decisions are made or conventions discovered
RULE: User defines the vision sections — AI never changes Goal, Platform, or Flows without approval
RULE: When proj/UIUX contradicts a UI file, fix the UI file — UIUX wins
BANNED: Making UI layout or UX decisions not grounded in proj/UIUX
BANNED: Skipping proj/UIUX because "it's a small change" — all GUI changes require it

---

## Format

```markdown
# UIUX: project-name

## Goal
The UI/UX vision — what the user experience should feel like.
Platform-native, fast, accessible. 2-4 sentences. User defines this.

## Platform
Target OS and toolkit — determines which platform rules apply.

- OS: GNOME (Linux) / macOS / Windows / Android / iOS / Web
- Toolkit: GTK4 + libadwaita / SwiftUI / WinUI3 / Jetpack Compose / Qt6 / React
- Icons: Adwaita / SF Symbols / Fluent / Material You

## UI Foundation Rules
Always active — load these via get_rule() before any UI work.

| Rule | What it enforces |
|------|-----------------|
| uiux/tokens.md | Zero literal values in components — all values are named tokens |
| uiux/components.md | One file per component, one responsibility |
| uiux/file-structure.md | Folders by feature area — changes stay contained |
| uiux/state-flow.md | State-in from Adapter, events-out — no domain logic in UI |
| uiux/theming.md | System light/dark — live switching, token-based |
| uiux/keyboard.md | Standard shortcuts, keyboard navigation — platform HIG |
| uiux/help-about.md | About dialog, license, shortcuts window — per platform |
| uiux/checklist.md | Pre-ship verification — all items must pass |

## Platform Rules
Copy the matching rows to proj/RULES → ## Active Rules → ### UI.

| Platform / Toolkit | Load these rule files |
|--------------------|-----------------------|
| Windows            | uiux/menus-windows.md |
| macOS              | uiux/menus-macos.md |
| GNOME              | uiux/menus-gnome.md |
| KDE                | uiux/menus-kde.md |
| Slint              | uiux/menus-slint.md |
| GTK4               | uiux/gtk.md |
| Web / PWA          | css/README.md |
| Android            | uiux/help-about.md |
| iOS                | uiux/theming.md |
| Qt6 / QML          | uiux/theming.md |
| React/Svelte/Vue   | covered by js/README.md + Web/PWA row |
| Compose Android    | covered by kotlin/README.md |
| Compose Desktop    | covered by kotlin/README.md + Windows/macOS rows |

RULE: A project targeting 3 platforms loads exactly 3 platform files — not "uiux/ (all)"
NOTE: Android/iOS/Qt6 have dedicated files planned (TODO #25–27) — current entries are interim

## UI Architecture
How UI is structured in this project.

- Toolkit: GTK4 / libadwaita (Rust + Blueprint)
- Entry point: src/ui/app.rs
- Component root: src/ui/
- Shared components: src/ui/shared/
- Feature folders: src/ui/dashboard/, src/ui/settings/, src/ui/auth/
- State: AdapterState_sta in src/adapter/ — UI reads, never writes directly

## Component Conventions
Project-specific UI conventions. AI adds here as patterns are discovered.

- All components use Blueprint (.ui) for layout, Rust for logic
- Component names: PascalCase, match filename exactly (FeedItem → feed_item.ui + feed_item.rs)
- Shared button style: use AdwButtonRow, never plain GtkButton for primary actions
- Error display: AdwStatusPage with icon — never inline text labels

## User Flows

### Primary Flow: [Name]
1. User does X → sees Y
2. User does A → result B
3. Edge case: if Z → then W

### Secondary Flow: [Name]
1. ...

## Layout

### Main Window
- Header: AdwHeaderBar with title + primary action
- Content: AdwNavigationView with sidebar
- Sidebar: AdwOverlaySplitView (collapsible on narrow)
- Status: AdwStatusPage for empty/error/loading states

### [Screen Name]
- ...

## Interaction Patterns
Project-specific UX decisions.

- Loading: AdwSpinner in header — never block the whole view
- Errors: AdwToast for transient, AdwStatusPage for permanent
- Confirmation: AdwAlertDialog before destructive actions
- Forms: validate on focus-out, submit on Enter, disable button while loading

## Accessibility
- All interactive elements reachable by keyboard
- Tab order follows visual order top-to-bottom, left-to-right
- Focus ring always visible (never hidden with CSS)
- All icons have accessible labels
- Minimum contrast: 4.5:1 for text, 3:1 for UI components
```

## Why UIUX Is Fundamental

A GUI project without proj/UIUX produces:
- Inconsistent UX across screens (each screen invented independently)
- Wrong platform conventions (non-native widgets, wrong icons, missing shortcuts)
- AI making layout decisions from context instead of specification
- Components that grow because there is no defined structure to follow

proj/UIUX gives every GUI session a shared ground truth — platform, toolkit, conventions, flows.
AI reads it first, follows it throughout, and updates it as conventions emerge.
