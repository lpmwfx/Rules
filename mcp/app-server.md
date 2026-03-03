---
tags: [mcp, gateway, stdio, subprocess, app-server, dev-testing, ai-access]
concepts: [mcp, gateway, stdio, dev-workflow]
requires: [global/topology.md, mcp/event-adapter.md]
related: [ipc/contract.md, global/app-model.md]
keywords: [mcp, stdio, subprocess, gateway, flag, --mcp, claude, dev, testing]
layer: 4
---
# MCP App Server — Gateway Component

> `app --mcp` gives AI the same access as a human user — via Adapter events

---

VITAL: MCP server is `_gtw` — lives in `src/gateway/`
VITAL: MCP exposes only Adapter events as tools — no operations of its own
RULE: App supports `--mcp` CLI flag to start in MCP-only mode
RULE: In `--mcp` mode only Gateway + Adapter + Core are initialised — no UI layer
RULE: MCP uses stdio transport — the app is launched as a subprocess by the AI client
RULE: MCP tool names map directly to Adapter event names
RULE: MCP server is introduced early in the project — gives AI test access before UI exists
RULE: `--mcp` flag is parsed in main/PAL — before any UI initialisation
RULE: MCP reads application state from `AdapterState_sta` — same source as UI
BANNED: MCP server calling Core directly — must go via Adapter events
BANNED: MCP tool without a corresponding Adapter event
BANNED: UI initialisation in MCP mode
BANNED: Business logic in the MCP Gateway module

## Startup Modes

```
app(.exe)          ──►  GUI mode    (UI + Adapter + Core + Gateway + PAL)
app(.exe) --mcp    ──►  MCP mode   (Gateway + Adapter + Core — no UI)
```

The `--mcp` flag is parsed before UI init so no UI framework is ever loaded in MCP mode.
This applies on all platforms: Windows, macOS, Linux, Android, iOS.

## Transport

MCP uses **stdio** transport (MCP spec 2025-06-18).
The AI client (Claude Code, Claude Desktop, etc.) launches the app as a subprocess and
communicates via stdin/stdout. No Unix sockets, no TCP sockets, no platform-specific IPC.

RULE: Do not implement MCP over Unix sockets or TCP — stdio is the required transport
RULE: One MCP server instance per app process — started by the `--mcp` flag

## Gateway Placement

The MCP server module is `_gtw` because it handles external IO (the stdio protocol).
It follows the same import rules as all Gateway modules:

RULE: MCP `_gtw` module imports Adapter (`_adp`) to fire events — this is the only allowed direction
BANNED: MCP `_gtw` module importing Core (`_core`) directly
BANNED: MCP `_gtw` module importing UI (`_ui`) — UI is not initialised in MCP mode

## Dev Workflow

Introduce the MCP server at project start, before the full UI is built.
This lets an AI assistant drive 90 % of build-and-test through the MCP interface:

1. Scaffold `src/gateway/mcp_server_gtw.*` with `--mcp` entry point
2. Expose every Adapter event as an MCP tool (one-to-one mapping)
3. AI can now call `save`, `open`, `close`, `export`, etc. without a running UI
4. UI can be built and iterated while tests run via MCP in parallel

RULE: MCP tool list and Adapter event list must stay in sync — a missing tool is an architecture gap
RULE: MCP tool descriptions reflect Adapter event semantics — not UI label text

## State and Observability Access

MCP is an external AI UI — it gets the same visibility as a human user, plus full observability.
MCP tools may read any data the Gateway layer can access:

RULE: MCP tools may read `AdapterState_sta` — same source as UI
RULE: MCP tools may expose log output, console output, and diagnostic files as tool results
RULE: MCP tools may read arbitrary files via Gateway's existing file-access surface
RULE: MCP tool results reflect the real app state after the event has been processed
BANNED: MCP tools caching state independently of `AdapterState_sta`

The principle: AI sees everything a human can see, plus structured access to logs and files
that a human would have to open manually. This is the full "external AI UI" contract.
