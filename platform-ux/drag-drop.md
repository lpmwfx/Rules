---
tags: [platform-ux, drag-drop, interaction, files]
concepts: [interaction, file-management]
related: [platform-ux/pointer-touch.md]
keywords: [drag, drop, file-upload]
layer: 5
---
# Drag and Drop

> File-to-terminal path insertion, file tree, and external sources

---

## File → Terminal (MUST implement)

RULE: Dragging a file from file tree into terminal inserts the file path at cursor

### Path Logic

| Condition | Inserted Path |
|---|---|
| File inside terminal CWD | Relative path: `src/main.rs` |
| File outside terminal CWD | Absolute path: `/home/user/other/file.txt` |
| Path contains spaces | Quoted: `"my file.txt"` |
| Multiple files | Space-separated paths |

### Implementation

1. On drop, get absolute path of dropped file
2. Get terminal's current working directory (from VTE or OSC 7)
3. If file path starts with terminal CWD → compute relative path
4. Otherwise use absolute path
5. Escape or quote paths containing spaces/special characters
6. Insert the path string at terminal cursor position

## File Tree Drag and Drop

| Action | Behavior |
|---|---|
| Drag file → terminal pane | Insert path |
| Drag file → file tree folder | Move file |
| `Ctrl` + drag | Force copy |
| `Shift` + drag | Force move |
| `Escape` during drag | Cancel |

## External Drag and Drop

| Source → Target | Behavior |
|---|---|
| File manager → terminal | Insert absolute path |
| File manager → file tree | Copy/move to workspace |
| Text selection → terminal | Paste text |

## Visual Feedback

RULE: Drop targets MUST show visual feedback when drag hovers
RULE: GTK4: Use `:drop(active)` CSS pseudoclass
RULE: Invalid drop targets show "not allowed" cursor
RULE: Show drag icon representing what is being dragged

## Accessibility

RULE: Every drag-and-drop action MUST have a keyboard/menu alternative
- "Copy Path" in context menu = alternative to drag-to-terminal
- "Move to..." menu item = alternative to drag-to-folder
- Arrow keys + modifier for reordering = alternative to drag-reorder
