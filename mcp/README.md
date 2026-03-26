---
tags: [mcp, integration, ai-access, ui]
concepts: [mcp]
related: [mcp/event-adapter.md, mcp/app-server.md]
layer: 6
---
# MCP — AI Integration Category

> Rules for exposing your app to AI assistants via the Model Context Protocol

---

## What This Category Covers

Two sides of MCP:

1. **Client config** — how your project declares which MCP servers it needs (`.claude/mcp.json`)
2. **Server building** — how your app exposes itself as an MCP server for AI assistants

## Files in This Category

| File | Layer | Description |
|------|-------|-------------|
| `client-config.md` | 2 | Per-project `.claude/mcp.json` — HTTP transport, server selection |
| `event-adapter.md` | 3 | Adapter as the single event API — all input sources use the same named events |
| `app-server.md` | 4 | MCP server as Gateway component — `--mcp` flag, dev workflow |

## Key Principles

### Client (consuming MCP servers)
- **Per-project config**: Each project declares its own MCP servers in `.claude/mcp.json`
- **HTTP-only transport**: All servers use `streamable-http` — no stdio in project configs
- **Committed to repo**: `.claude/mcp.json` is part of the project — portable and reproducible
- **Minimal set**: Only declare servers the project actually uses

### Server (building MCP servers)
- **MCP = another UI for AI**: AI gets exactly the same access as a human using the UI
- **Adapter events are the contract**: MCP tools are thin wrappers over Adapter events — no own logic
- **HTTP transport**: Servers expose HTTP endpoints — proxy translates to stdio where needed
- **Early adoption**: Introduce `--mcp` at project start so AI can test before UI is built

## Related Categories

- `global/topology.md` — folder/tag mapping (`_ui` = `src/ui/`)
- `global/adapter-layer.md` — Adapter event surface rules
- `ipc/contract.md` — JSON-RPC contract (Unix socket IPC, separate from MCP)


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
