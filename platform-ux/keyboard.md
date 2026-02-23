# Keyboard Shortcuts

> Standard shortcuts and navigation — GNOME HIG compliant

---

## Application Lifecycle

| Shortcut | Action | Notes |
|---|---|---|
| `Ctrl+Q` | Quit | Close app including all windows |
| `Ctrl+W` | Close | Close current tab/window |
| `F1` | Help | Open help documentation |
| `Ctrl+?` | Keyboard Shortcuts | Open shortcuts dialog |
| `Ctrl+,` | Preferences | Open preferences window |

## Clipboard & Editing (GUI Context)

| Shortcut | Action |
|---|---|
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+X` | Cut |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Ctrl+A` | Select All |

## Clipboard & Editing (Terminal Context)

RULE: Terminal emulators (VTE) intercept Ctrl+C/V — use Shift modifier

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+C` | Copy from terminal |
| `Ctrl+Shift+V` | Paste into terminal |

VITAL: Use GTK Actions + Accelerators (`app.set_accels_for_action`), NOT `EventControllerKey`, which won't fire while VTE has focus.

## Search

| Shortcut | Action |
|---|---|
| `Ctrl+F` | Find |
| `Ctrl+G` | Find Next |
| `Ctrl+Shift+G` | Find Previous |
| `Escape` | Close Search |

## View & Zoom

| Shortcut | Action |
|---|---|
| `Ctrl+Plus` | Zoom In |
| `Ctrl+Minus` | Zoom Out |
| `Ctrl+0` | Reset Zoom |
| `F9` | Toggle Sidebar |
| `F11` | Fullscreen |

## Tabs

| Shortcut | Action |
|---|---|
| `Ctrl+T` / `Ctrl+Shift+T` | New Tab |
| `Ctrl+Tab` | Next Tab |
| `Ctrl+Shift+Tab` | Previous Tab |
| `Ctrl+W` | Close Tab |
| `Ctrl+1`..`Ctrl+9` | Switch to Tab N |

## Navigation

| Shortcut | Action |
|---|---|
| `Alt+Left` | Back |
| `Alt+Right` | Forward |
| `Alt+Up` | Parent directory |
| `Alt+Home` | Home |

## Files & Content

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New |
| `Ctrl+O` | Open |
| `Ctrl+S` | Save |
| `Ctrl+Shift+S` | Save As |
| `Ctrl+P` | Print |

## Widget-Level Navigation

| Key | Action |
|---|---|
| `Tab` / `Shift+Tab` | Navigate focusable elements |
| `Return` / `Enter` | Activate focused control |
| `Space` | Toggle control state |
| Arrow keys | Navigate within composite widgets |
| `Escape` | Close transient containers |
| `F10` | Open primary/secondary menu |
| `Shift+F10` / `Menu` | Open context menu |

## System-Reserved Shortcuts (NEVER USE)

BANNED: `Super+*` — all Super combinations (GNOME Shell)
BANNED: `Alt+Tab` — window switching
BANNED: `Alt+F4` — close window
BANNED: `Alt+F6/F7/F8` — window management
BANNED: `Ctrl+Alt+Delete` — power off
BANNED: `PrintScreen` variants — screenshots
BANNED: Three/four-finger gestures — system gestures

## Shortcut Design Rules

RULE: Use `Ctrl+Letter` as primary pattern
RULE: Use `Ctrl+Shift+Letter` for reverse/extended functions
RULE: Make shortcuts mnemonic (Ctrl+F = Find, Ctrl+S = Save)
RULE: App-specific shortcuts use `Ctrl+Shift+` prefix
RULE: Only assign shortcuts to commonly-used actions
RULE: Always use the standard shortcut if the function matches
BANNED: `Alt+Letter` for shortcuts — conflicts with access keys
BANNED: `Super` — reserved for GNOME Shell

## Shortcut Discoverability

RULE: Menu items show shortcut labels automatically via GTK/Qt actions
RULE: Tooltips on buttons mention shortcuts: `"Zen Mode (Ctrl+Shift+Z)"`
RULE: Context menus expose actions for right-click users
RULE: Shortcuts dialog (`Ctrl+?`) lists all available shortcuts
RULE: Header bar menu includes "Keyboard Shortcuts" entry
