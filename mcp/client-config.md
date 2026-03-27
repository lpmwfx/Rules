---
tags: [mcp, client, config, claude-code, http, project-setup]
concepts: [mcp-client-config, per-project-mcp, http-transport]
requires: [mcp/README.md, global/initialize.md]
feeds: [mcp/client-auth.md, mcp/client-templates.md]
related: [mcp/server-build.md, project-files/project-file.md]
keywords: [mcp.json, claude-code, http, mcpServers, per-project, http-transport]
layer: 2
---
# MCP Client Configuration

> Per-project `.claude/mcp.json` — each project declares which MCP servers it needs

---

## Why Per-Project

Each project has different MCP needs. Per-project config means:

- No global server bloat — only load what this project uses
- Portable — clone the repo, MCP servers are declared
- Reproducible — every developer/AI session gets the same tools

RULE: Every project MUST have `.claude/mcp.json` declaring its MCP servers
RULE: All MCP servers use HTTP transport (`"type": "http"`) — no stdio in project configs
RULE: `.claude/mcp.json` is committed to the repo
RULE: Only declare servers the project actually uses

## Format

```json
{
  "mcpServers": {
    "server-name": {
      "type": "http",
      "url": "https://host/mcp"
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | `"http"` for streamable HTTP, `"sse"` for SSE |
| `url` | Yes | HTTP endpoint — supports `${VAR}` interpolation |
| `headers` | No | Static auth headers — supports `${VAR}` |
| `oauth` | No | OAuth 2.0 config (not recommended yet — bugs) |

## Integration with Project Init

During `global/initialize.md` step 0:

1. Detect project type from proj/PROJECT stack
2. Select template (see [client-templates.md](client-templates.md))
3. Write `.claude/mcp.json`
4. Verify: all declared servers respond

RULE: `.claude/mcp.json` is created during project initialization
RULE: URLs use env var interpolation with sensible defaults
RULE: After creation, verify each server responds

## CLI Management

```bash
claude mcp add --transport http articles https://articles.lpmintra.com/mcp
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}"
claude mcp list
claude mcp remove articles
```

BANNED: Hardcoded Bearer tokens in committed mcp.json
BANNED: `"type": "stdio"` in project mcp.json — HTTP only
BANNED: Storing secrets in `.claude/` directory
