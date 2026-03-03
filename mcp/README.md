---
tags: [mcp, overview, integration, ai-access, ui]
concepts: [mcp, overview]
related: [mcp/event-adapter.md, mcp/app-server.md]
layer: 6
---
# MCP — AI Integration Category

> Rules for exposing your app to AI assistants via the Model Context Protocol

---

## What This Category Covers

MCP (Model Context Protocol) integration gives an AI assistant the same access to your app
as a human user — via the existing Adapter event surface. No separate API, no duplicated logic.

The MCP server is a UI component (`_ui`) that lives in `src/ui/`.
It is the AI's user interface — parallel to the GUI, not a bus or gateway.
It is activated by the `--mcp` CLI flag and communicates via stdio transport.

## Files in This Category

| File | Layer | Description |
|------|-------|-------------|
| `event-adapter.md` | 3 | Adapter as the single event API — all input sources use the same named events |
| `app-server.md` | 4 | MCP server as Gateway component — `--mcp` flag, stdio transport, dev workflow |

## Key Principles

- **MCP = another UI for AI**: AI gets exactly the same access as a human using the UI
- **Adapter events are the contract**: MCP tools are thin wrappers over Adapter events — no own logic
- **stdio transport**: App is launched as a subprocess; no Unix sockets, no TCP
- **Early adoption**: Introduce `--mcp` at project start so AI can test before UI is built
- **Cross-platform**: stdio transport works on Windows, macOS, Linux, Android, and iOS

## Related Categories

- `global/topology.md` — folder/tag mapping (`_ui` = `src/ui/`)
- `global/adapter-layer.md` — Adapter event surface rules
- `ipc/contract.md` — JSON-RPC contract (Unix socket IPC, separate from MCP)
