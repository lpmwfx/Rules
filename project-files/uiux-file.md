---
tags: [uiux, gui, user-flows, accessibility]
concepts: [ui-specification, user-flows, accessibility]
related: [project-files/todo-file.md]
keywords: [layout, interaction, flow]
layer: 2
---
# UIUX File

> UI/UX specification — what the user sees and experiences

---

Format: Plain text / Markdown

REQUIRED for GUI projects. Not applicable for CLI tools or libraries.

```
# UIUX

## User Flows

### Primary Flow: [Name]
1. User opens app → sees dashboard
2. User clicks "New" → form appears
3. User fills form → validation inline
4. User submits → confirmation + redirect to list

### Secondary Flow: [Name]
1. ...

## Layout

### Main Screen
- Header: logo, nav, user menu
- Sidebar: section navigation (collapsible)
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

## Rules

RULE: Describe WHAT the user experiences, not HOW it is implemented
RULE: User flows are numbered sequences — testable step by step
RULE: Layout describes structure, not CSS/styling details
RULE: Interaction patterns are consistent across the entire app
RULE: Accessibility is not optional — include from the start
RULE: Update UIUX when user-facing behavior changes
RULE: AI reads UIUX before any GUI work — no guessing at layout or flow
