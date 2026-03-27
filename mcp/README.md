---
tags: [mcp, integration, ai-access, ui]
concepts: [mcp]
related: [mcp/event-adapter.md, mcp/app-server.md, mcp/server-build.md, mcp/aiux.md]
layer: 6
---
# MCP — AI Integration Category

> Rules for exposing your app to AI assistants via the Model Context Protocol

---

## What This Category Covers

Three aspects of MCP:

1. **Building standalone servers** — HTTP MCP servers as independent services
2. **Embedding in apps** — `--mcp` flag to expose desktop apps to AI
3. **Client config** — how projects declare which MCP servers they need

## Files in This Category

| File | Layer | Description |
|------|-------|-------------|
| `server-build.md` | 3 | Building standalone MCP servers — Bun, HTTP, OAuth, tool registration |
| `aiux.md` | 3 | AIUX — pull-based help/manpage pattern for tool documentation |
| `event-adapter.md` | 3 | Adapter as the single event API — all input sources use the same named events |
| `server-session.md` | 3 | Session lifecycle and transparent recovery after restart |
| `server-deploy.md` | 4 | OpenRC service, Nginx proxy, new server checklist |
| `app-server.md` | 4 | MCP as `--mcp` flag in desktop apps — stdio transport, _ui layer |
| `client-config.md` | 2 | Per-project `.claude/mcp.json` — format, setup, CLI |
| `client-auth.md` | 2 | Dashboard tokens, Tailscale, env vars — auth for MCP clients |
| `client-templates.md` | 2 | mcp.json templates per project type |

## Key Principles

### Client (consuming MCP servers)
- **Per-project config**: Each project declares its own MCP servers in `.claude/mcp.json`
- **HTTP-only transport**: All servers use `streamable-http` — no stdio in project configs
- **Committed to repo**: `.claude/mcp.json` is part of the project — portable and reproducible
- **Minimal set**: Only declare servers the project actually uses

### Standalone Server (building MCP services)
- **Tools are adapter**: Tool handlers transform input/output — business logic lives in core
- **HTTP + OAuth**: Streamable HTTP transport with per-server OAuth 2.1
- **AIUX**: Pull-based help/manpage on every tool — AI asks when it needs
- **One server per domain**: Split by concern, not one mega-server

### Embedded Server (--mcp flag in apps)
- **MCP = another UI for AI**: AI gets exactly the same access as a human using the UI
- **Adapter events are the contract**: MCP tools are thin wrappers over Adapter events — no own logic
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
