---
tags: [mcp, server, build, bun, typescript, http, oauth, standalone]
concepts: [mcp-server-build, standalone-server, http-transport, tool-design]
requires: [mcp/README.md, global/topology.md, global/topology-profiles.md, js/topology-mcp.md]
feeds: [mcp/aiux.md, mcp/client-config.md]
feeds: [mcp/server-session.md, mcp/server-deploy.md]
related: [mcp/app-server.md, mcp/event-adapter.md, global/tools-and-scripts.md]
keywords: [mcp, server, build, bun, http, oauth, tool, transport, session, streamable-http]
layer: 3
---
# Building MCP Servers

> Standalone HTTP servers that expose tools to AI — Bun + TypeScript + MCP SDK

---

## When to Use

Standalone MCP servers are services that exist independently — not embedded in a desktop app via `--mcp`. They serve AI clients over HTTP with OAuth.

For `--mcp` flag in desktop apps, see [app-server.md](app-server.md).

## Topology

MCP servers follow the **mcp-server** profile (see [js/topology-mcp.md](../js/topology-mcp.md)):

| Layer | Maps to |
|---|---|
| adapter | `src/tools/` — tool handlers |
| core | `src/core/`, `src/registry.ts`, `src/scanner/` — business logic |
| gateway | `src/gateway/` — file IO, external APIs |
| pal | `src/auth/` — OAuth, transport, runtime |
| shared | `src/shared/` — error types, interfaces |

RULE: Tool handlers are adapter — they transform input/output, never contain business logic
RULE: Core has no knowledge of MCP protocol
RULE: Auth and transport are pal — platform infrastructure

## Server Structure

```typescript
// Entry point — one per server
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "my-server", version: "0.1.0" });
registerTools(server);  // adapter layer

Bun.serve({
  port: 3100,
  async fetch(req) {
    // /health — public
    // /.well-known/oauth-* — public
    // /mcp — bearer auth required → session → server.handle()
  },
});
```

RULE: One entry point (.ts file) per MCP server
RULE: Health endpoint at `/health` — always public, returns server name and session count
RULE: MCP endpoint at `/mcp` — bearer auth required
RULE: Use Bun.serve() — not Express, not Hono, not Fastify

## Transport

Streamable HTTP (not stdio). Handles POST (JSON-RPC), GET (SSE stream), DELETE (session close) on `/mcp`.

```
POST /mcp + Authorization: Bearer <token>
  → Create or reuse session (mcp-session-id header)
  → Route JSON-RPC to McpServer
  → Return response
```

RULE: Sessions tracked by `mcp-session-id` header — one McpServer + transport pair per session
RULE: Use WebStandardStreamableHTTPServerTransport from SDK
RULE: Streamable HTTP transport — not stdio for standalone servers
BANNED: stdio transport for standalone MCP servers — HTTP only

## Authentication

OAuth 2.1 with PKCE. Each server has its own auth provider and token store.

RULE: Each server manages its own tokens — no shared token database across servers
RULE: Token persistence to disk (JSON file) — survives server restart
RULE: OAuth metadata at `/.well-known/oauth-protected-resource`
BANNED: Hardcoded credentials in source code — use environment variables

## Tool Registration

Tools are registered through a central function in the adapter layer:

```typescript
// src/tools/index.ts — adapter
export function registerTools(server: McpServer): void {
  server.registerTool("tool_name", {
    description: "Short — what it does",
    inputSchema: {
      help: z.string().optional().describe("System overview"),
      manpage: z.string().optional().describe("Full tool documentation"),
      param: z.string().describe("What this param is"),
    },
  }, async (args) => {
    if (args.help !== undefined) return ok(SYSTEM_HELP);
    if (args.manpage !== undefined) return ok(TOOL_MANPAGE);
    // ... call core, return result
  });
}
```

RULE: All tools in one registration file per server — not scattered
RULE: Zod schemas for input validation — not manual parsing
RULE: Every tool has `help` and `manpage` params (see [aiux.md](aiux.md))
RULE: Tool descriptions are short (one line) — detail goes in manpage

## Multiple Servers

When a system has multiple MCP servers, each is an independent process:

- Separate entry point, separate port, separate auth store
- Shared code via imports (same src/core, src/auth)
- No cross-server session sharing

RULE: One server per domain concern — not one mega-server
RULE: Servers share code, not state
BANNED: Cross-server token validation
BANNED: Monolithic server with 50+ tools — split by domain

## SDK Dependencies

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.28.0",
    "zod": "^4.3.6"
  }
}
```

RULE: Use official MCP SDK — not custom protocol implementation
RULE: Zod for schema validation — matches SDK's inputSchema pattern
