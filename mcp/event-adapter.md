---
tags: [event, adapter, decoupling, input-sources, api-surface, mcp]
concepts: [event-flow, adapter-pattern, decoupling]
requires: [global/adapter-layer.md, global/topology.md]
feeds: [mcp/app-server.md]
keywords: [event, listener, dispatch, input, keyboard, button, mcp, on_save]
layer: 3
---
# Adapter Event API — Single Input Layer

> Every input source — button, keyboard shortcut, MCP tool — fires the same named event

---

VITAL: Adapter is the only place events are defined and exposed — one API surface per module
RULE: Events are named by intention, not by input source (`on_save` not `on_ctrl_s_pressed`)
RULE: All input sources (button, keyboard shortcut, MCP tool) register on the same named event
RULE: One logic callback per named event — never duplicated across input sources
RULE: Input sources know only the event name — they do not know each other
RULE: The logic layer is unaware of input source (full decoupling)
BANNED: Button handler calling Core directly — bypasses the Adapter event API
BANNED: Event names derived from input source (`on_ctrl_s`, `on_save_button_clicked`)
BANNED: Same logic implemented in both a button handler and an MCP tool

## Why One Event Surface

When all input sources converge on a single named event, adding a new input source (MCP tool,
voice command, scripting API) requires zero changes to Core or other input sources.
The Adapter event is the contract; callers are interchangeable.

## Sequence Diagram

```
Button click  ──────────────────────────────────┐
                                                 ▼
Ctrl+S shortcut  ──────────────────────────►  Adapter.on_save()  ──►  Core.save()
                                                 ▲
MCP tool `save`  ──────────────────────────────┘
```

All three paths are identical at the Adapter boundary. Core never sees where the call originated.

## Event Naming Examples

| Input | Wrong | Correct |
|-------|-------|---------|
| Save button | `on_save_button_clicked` | `on_save` |
| Ctrl+S | `on_ctrl_s_pressed` | `on_save` |
| MCP tool | `mcp_save` | `on_save` (same event) |
| New document | `on_new_button` | `on_new` |
| Close window | `on_close_x_clicked` | `on_close` |

RULE: When naming an event, ask "what does this *do*?" not "what triggered it?"
RULE: MCP tool names are derived from Adapter event names — they are not independent identifiers

## Platform Note

This pattern applies regardless of platform (Windows, macOS, Linux, Android, iOS).
The Adapter event surface is platform-neutral; platform-specific input binding is PAL's concern.
