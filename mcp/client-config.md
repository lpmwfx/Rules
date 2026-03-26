---
tags: [mcp, client, config, claude-code, http, project-setup]
concepts: [mcp-client-config, per-project-mcp, http-transport]
requires: [mcp/README.md, global/initialize.md]
related: [mcp/app-server.md, project-files/project-file.md]
keywords: [mcp.json, claude-code, streamable-http, mcpServers, per-project, http-transport]
layer: 2
---
# MCP Client Configuration

> Per-project `.claude/mcp.json` — each project declares which MCP servers it needs

---

## Why Per-Project

Each project has different MCP needs. A Laravel project needs different tools than a Rust CLI.
Per-project config means:

- No global server bloat — only load what this project uses
- Portable — clone the repo, MCP servers are declared
- Reproducible — every developer/AI session gets the same tools
- HTTP-only — no subprocess management, no binary path issues

RULE: Every project MUST have `.claude/mcp.json` declaring its MCP servers
RULE: All MCP servers use HTTP transport (`streamable-http`) — no stdio in project configs
RULE: `.claude/mcp.json` is committed to the repo — it is part of the project
RULE: Only declare servers the project actually uses — no "include everything"

---

## Format

Claude Code reads `.claude/mcp.json` in the project root:

```json
{
  "mcpServers": {
    "server-name": {
      "type": "streamable-http",
      "url": "http://host:port/path"
    }
  }
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Transport — always `"streamable-http"` |
| `url` | Yes | HTTP endpoint for the MCP server |
| `headers` | No | Auth headers — `{"Authorization": "Bearer ..."}` |

RULE: Use `streamable-http` transport — not `sse`, not `stdio`
RULE: URLs must use hostname, not IP — use Tailscale hostnames or localhost
RULE: No secrets in mcp.json — use environment variable references where supported

---

## Available Servers

### Core — every project

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `rules` | `http://localhost:PORT/rules` | Rule lookup, search, context | 7 tools |
| `rulestools` | `http://localhost:PORT/tools` | Scan, setup, init, publish | 16 tools |

### Development

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `issuesmcp` | `http://localhost:PORT/issues` | Forgejo/GitHub issue CRUD | 8 tools |

### Content & Publishing

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `articles` | `http://HOST/articles` | Article publish pipeline | 15 tools |
| `audience` | `http://HOST/audience` | Audience intelligence, SEO | 18 tools |

### Desktop & Automation

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `gui-mcp` | `http://localhost:PORT/gui` | Windows GUI automation | 15 tools |
| `carussel` | `http://localhost:PORT/carussel` | Badge injection | 3 tools |

---

## Project Type Templates

### Rust CLI / Library

```json
{
  "mcpServers": {
    "rules": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/rules"
    },
    "rulestools": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/tools"
    },
    "issuesmcp": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/issues"
    }
  }
}
```

### Rust GUI (Slint)

```json
{
  "mcpServers": {
    "rules": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/rules"
    },
    "rulestools": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/tools"
    },
    "issuesmcp": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/issues"
    },
    "gui-mcp": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/gui"
    }
  }
}
```

### Laravel Web Application

```json
{
  "mcpServers": {
    "rules": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/rules"
    },
    "rulestools": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/tools"
    },
    "issuesmcp": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/issues"
    }
  }
}
```

### Content Site (articles + audience)

```json
{
  "mcpServers": {
    "rules": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/rules"
    },
    "rulestools": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/tools"
    },
    "articles": {
      "type": "streamable-http",
      "url": "http://HOST/articles"
    },
    "audience": {
      "type": "streamable-http",
      "url": "http://HOST/audience"
    }
  }
}
```

### Python CLI / Service

```json
{
  "mcpServers": {
    "rules": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/rules"
    },
    "rulestools": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/tools"
    },
    "issuesmcp": {
      "type": "streamable-http",
      "url": "http://localhost:PORT/issues"
    }
  }
}
```

---

## Integration with Project Initialization

During `global/initialize.md` step 0, after `rulestools setup .`:

```
0b. CREATE .claude/mcp.json
    → Detect project type from proj/PROJECT stack
    → Select template (see Project Type Templates above)
    → Write .claude/mcp.json with correct URLs
    → Verify: all declared servers respond to health check
```

RULE: `.claude/mcp.json` is created during project initialization — not ad-hoc
RULE: URLs are filled from environment or Tailscale — never hardcoded IPs
RULE: After creation, verify each server responds before continuing

---

## Server Discovery

MCP server URLs come from these sources, in priority order:

1. **Tailscale** — `tailscale status` for remote hosts (production MCP servers)
2. **localhost** — for locally running servers during development
3. **Environment** — `MCP_RULES_URL`, `MCP_TOOLS_URL` etc. for CI/CD

RULE: Use Tailscale hostnames for servers on other machines
RULE: Use localhost for servers on the dev machine
RULE: Never hardcode IP addresses — they change

---

## Security

RULE: No API keys or tokens in `.claude/mcp.json` — use env vars or auth middleware
RULE: MCP servers behind Tailscale do not need additional auth — network is the perimeter
RULE: Public-facing MCP endpoints MUST require authentication headers
RULE: `.claude/mcp.json` is safe to commit — it contains URLs, not secrets

BANNED: Hardcoded Bearer tokens in mcp.json
BANNED: MCP servers exposed on 0.0.0.0 without authentication
BANNED: Storing secrets in `.claude/` directory
