---
tags: [topology, mcp, bun, layers, server]
concepts: [mcp-topology, layer-mapping-mcp, tools-as-adapter]
requires: [global/topology.md, global/topology-profiles.md]
related: [js/topology-cli.md, core/design.md, gateway/io.md, adapter/viewmodel.md]
keywords: [mcp, tools, server, bun, adapter, transport, session]
layer: 2
---
# MCP Server Topology

> 6-layer mapping for MCP servers in Bun TypeScript

---

| Layer | Tag | MCP server mapping |
|---|---|---|
| ui | — | Absent — MCP has no visual interface |
| adapter | `_adp` | `src/tools/` — MCP tool handlers (receive request, call core, return response) |
| core | `_core` | `src/core/` or `src/registry.ts`, `src/scanner/` — business logic |
| gateway | `_gtw` | `src/gateway/` — file IO, external APIs, database |
| pal | `_pal` | `src/auth/` — OAuth provider, runtime abstraction (Bun.serve, Bun.env) |
| shared | `_x` | `src/shared/` — error types, interfaces, cross-layer types |

## Tools ARE Adapter

MCP tools are the adapter layer — they are the bridge between the AI client and core logic:

- Receive structured input (Zod-validated)
- Call core functions
- Format results for the MCP response
- No business logic in tool handlers

```typescript
// src/tools/scan.ts — adapter
server.registerTool("scan_file", { ... }, async ({ path, content }) => {
    const issues = scanFile(path, content);  // core
    return { content: [{ type: "text", text: formatIssues(issues) }] };
});
```

## Transport is PAL

HTTP server setup, OAuth middleware, session management — these are platform concerns:

- `Bun.serve()` — runtime
- OAuth provider — authentication abstraction
- StreamableHTTPServerTransport — MCP protocol handling

RULE: Tool handlers are adapter — transform input/output, delegate to core
RULE: Transport and auth are pal — platform infrastructure, not business logic
RULE: Core has no knowledge of MCP protocol — it receives data, returns results
