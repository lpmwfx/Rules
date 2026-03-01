---
tags: [uiux, gui, user-flows, accessibility]
concepts: [ui-specification, user-flows, accessibility]
related: [project-files/todo-file.md]
keywords: [layout, interaction, flow]
layer: 2
---
# UIUX.md File

> UI/UX specification — what the user sees and experiences

---

## Quick Reference

- **Location:** `proj/UIUX.md`
- **Format:** Markdown — structured sections with numbered flows and bullet lists
- **Required:** GUI projects only (TUI, WA, PWA, Desktop, Mobile) — not CLI or libraries
- **Owner:** User defines UI/UX — AI reads before any GUI work

Describes user flows, layout structure, and interaction patterns.
AI reads this before any GUI work — no guessing at layout or flow.

---

RULE: File lives at `proj/UIUX.md`
RULE: Create UIUX.md for GUI projects — skip for CLI tools and libraries
RULE: AI reads UIUX.md before any GUI work — no exceptions
RULE: Describe WHAT the user experiences, not HOW it is implemented
RULE: User flows are numbered sequences — testable step by step
RULE: Accessibility is not optional — include from the start
RULE: Update UIUX.md when user-facing behavior changes

## Format

```markdown
# UIUX: project-name

## User Flows

### Primary Flow: Login
1. User opens app → sees login screen
2. User enters credentials → inline validation
3. User submits → redirect to dashboard
4. Invalid credentials → error message inline, no redirect

### Secondary Flow: Create Item
1. User clicks "New" → modal opens
2. User fills form → validation on blur
3. User submits → item appears in list, modal closes

## Layout

### Main Screen
- Header: logo, nav, user menu
- Sidebar: section navigation (collapsible on mobile)
- Content: primary workspace
- Footer: status bar

### Detail Screen
- Breadcrumb: Home > Section > Item
- Content: form or display
- Actions: save, cancel, delete (bottom-right)

## Interaction Patterns

- Forms: inline validation, submit on Enter
- Lists: click to select, double-click to edit
- Modals: confirm before destructive actions
- Loading: skeleton screens, not spinners
- Errors: inline near source, toast for global

## Accessibility

- Keyboard navigation for all actions
- Tab order follows visual order
- Focus visible on all interactive elements
- ARIA labels on non-text elements
- Minimum contrast ratio: 4.5:1
```
