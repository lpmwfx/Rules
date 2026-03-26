---
tags: [mcp, client, config, claude-code, http, project-setup]
concepts: [mcp-client-config, per-project-mcp, http-transport]
requires: [mcp/README.md, global/initialize.md]
related: [mcp/app-server.md, project-files/project-file.md]
keywords: [mcp.json, claude-code, http, mcpServers, per-project, http-transport, oauth, headers]
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
RULE: All MCP servers use HTTP transport (`"type": "http"`) — no stdio in project configs
RULE: `.claude/mcp.json` is committed to the repo — it is part of the project
RULE: Only declare servers the project actually uses — no "include everything"

---

## Format

Claude Code reads `.claude/mcp.json` in the project root:

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

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | Transport — `"http"` for streamable HTTP, `"sse"` for SSE |
| `url` | Yes | HTTP endpoint — supports `${VAR}` interpolation |
| `headers` | No | Static auth headers — supports `${VAR}` interpolation |
| `headersHelper` | No | Shell command that outputs JSON headers (dynamic auth) |
| `oauth` | No | OAuth 2.0 configuration (browser login flow) |

---

## Authentication

### Recommended: Dashboard Token + Environment Variable

Each MCP server has a PWA dashboard where you generate a long-lived API token.
The token goes in an environment variable, referenced from `.mcp.json` via `${VAR}`.

**Flow:**
1. Open the system's PWA dashboard (e.g. `https://articles.lpmintra.com/dash`)
2. Log in → generate API token
3. Set env var: `export ARTICLES_TOKEN=ey...`
4. `.mcp.json` picks it up automatically

```json
{
  "mcpServers": {
    "articles": {
      "type": "http",
      "url": "https://articles.lpmintra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${ARTICLES_TOKEN}"
      }
    }
  }
}
```

Syntax: `${VAR}` expands at runtime. `${VAR:-default}` provides fallback.
Works in: `url`, `headers`, `command`, `args`, `env`.

Same pattern as GitHub Personal Access Tokens — generate in web UI, put in config.

**Server-side requirements:**
- `/dash` — PWA dashboard with login (password, magic link, etc.)
- Token generation — JWT or opaque token with expiry + scope
- Middleware on `/mcp` — validates `Authorization: Bearer` header
- Optional: `/token/refresh`, token revocation, TTL display in dashboard

RULE: Each MCP server provides its own dashboard for token management
RULE: Tokens are stored in environment variables, never in committed files
RULE: Dashboard shows token status, allows regeneration, and sets TTL

### Known Bug: `.mcp.json` headers

As of Claude Code v2.1.84, there is a bug (#28293) where `headers` defined in
`.mcp.json` may not be forwarded on tool-call POST requests. Headers added via
`claude mcp add --header` CLI command DO work reliably.

**Workaround** if `.mcp.json` headers fail:
```bash
claude mcp add --transport http articles https://articles.lpmintra.com/mcp \
  --header "Authorization: Bearer $ARTICLES_TOKEN"
```

### Tailscale Network (no auth needed)

Servers behind Tailscale need no additional auth — the network is the perimeter:

```json
{
  "mcpServers": {
    "internal-tool": {
      "type": "http",
      "url": "http://mimer:PORT/mcp"
    }
  }
}
```

### OAuth 2.0 (not recommended yet)

Claude Code has OAuth support via DCR (Dynamic Client Registration), but it has
multiple open bugs (#11585, #38102) — pre-registered client IDs are often ignored,
and the browser auth flow does not always trigger. Use dashboard tokens instead
until OAuth stabilizes in Claude Code.

RULE: Tailscale-internal servers skip auth — MagicDNS hostname is sufficient
RULE: Public-facing servers (VPS) use dashboard token + `${VAR}` pattern

---

## Available Servers

### Core — every project

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `rules` | Tailscale / localhost | Rule lookup, search, context | 7 |
| `rulestools` | Tailscale / localhost | Scan, setup, init, publish | 16 |

### Development

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `issuesmcp` | Tailscale / localhost | Forgejo/GitHub issue CRUD | 8 |

### Content & Publishing (public VPS)

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `articles` | `https://articles.lpmintra.com/mcp` | Article publish pipeline | 15 |
| `audience` | `https://audienceintelligence.lpmintra.com/mcp` | SEO, web intelligence, inspiration | 18 |

Auth: Bearer token from each system's PWA dashboard (`/dash`). Token → env var → `${VAR}` in mcp.json.

### Desktop & Automation

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `gui-mcp` | localhost | Windows GUI automation | 15 |
| `carussel` | localhost | Badge injection | 3 |

---

## Project Type Templates

### Rust CLI / Library

```json
{
  "mcpServers": {
    "rules": {
      "type": "http",
      "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}"
    },
    "rulestools": {
      "type": "http",
      "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}"
    },
    "issuesmcp": {
      "type": "http",
      "url": "${MCP_ISSUES_URL:-http://localhost:PORT/issues}"
    }
  }
}
```

### Rust GUI (Slint)

```json
{
  "mcpServers": {
    "rules": {
      "type": "http",
      "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}"
    },
    "rulestools": {
      "type": "http",
      "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}"
    },
    "issuesmcp": {
      "type": "http",
      "url": "${MCP_ISSUES_URL:-http://localhost:PORT/issues}"
    },
    "gui-mcp": {
      "type": "http",
      "url": "${MCP_GUI_URL:-http://localhost:PORT/gui}"
    }
  }
}
```

### Laravel Web Application

```json
{
  "mcpServers": {
    "rules": {
      "type": "http",
      "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}"
    },
    "rulestools": {
      "type": "http",
      "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}"
    },
    "issuesmcp": {
      "type": "http",
      "url": "${MCP_ISSUES_URL:-http://localhost:PORT/issues}"
    }
  }
}
```

### Content Site (articles + audience)

```json
{
  "mcpServers": {
    "rules": {
      "type": "http",
      "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}"
    },
    "rulestools": {
      "type": "http",
      "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}"
    },
    "articles": {
      "type": "http",
      "url": "https://articles.lpmintra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${ARTICLES_TOKEN}"
      }
    },
    "audience": {
      "type": "http",
      "url": "https://audienceintelligence.lpmintra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${AUDIENCE_TOKEN}"
      }
    }
  }
}
```

### Python CLI / Service

```json
{
  "mcpServers": {
    "rules": {
      "type": "http",
      "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}"
    },
    "rulestools": {
      "type": "http",
      "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}"
    },
    "issuesmcp": {
      "type": "http",
      "url": "${MCP_ISSUES_URL:-http://localhost:PORT/issues}"
    }
  }
}
```

---

## CLI Management

```bash
# Add a server
claude mcp add --transport http articles https://articles.lpmintra.com/mcp

# Add with auth header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer ${TOKEN}"

# Add with OAuth
claude mcp add --transport http cloud-svc https://mcp.service.com/mcp \
  --client-id my-client-id --callback-port 8080

# List configured servers
claude mcp list

# Remove a server
claude mcp remove articles

# Authenticate / clear auth
/mcp   # inside Claude Code session
```

---

## Integration with Project Initialization

During `global/initialize.md` step 0, after `rulestools setup .`:

```
0b. CREATE .claude/mcp.json
    → Detect project type from proj/PROJECT stack
    → Select template (see Project Type Templates above)
    → Replace PORT placeholders with actual ports
    → Write .claude/mcp.json
    → Verify: all declared servers respond
```

RULE: `.claude/mcp.json` is created during project initialization — not ad-hoc
RULE: URLs use env var interpolation with sensible defaults
RULE: After creation, verify each server responds before continuing

---

## Server Discovery

MCP server URLs come from these sources, in priority order:

1. **Public VPS** — `*.lpmintra.com` for public-facing MCP services (auth required)
2. **Tailscale MagicDNS** — internal hostnames for private services (no auth needed)
3. **localhost** — for locally running servers during development
4. **Environment variables** — `MCP_RULES_URL`, `MCP_TOOLS_URL` etc. for CI/CD

RULE: Public VPS servers (`*.lpmintra.com`) MUST use auth headers with `${VAR}` tokens
RULE: Tailscale-internal servers use MagicDNS hostnames — no auth needed
RULE: Use localhost for servers on the dev machine
RULE: Never hardcode IP addresses — they change

---

## Security

RULE: No plaintext secrets in `.claude/mcp.json` — use `${VAR}` interpolation
RULE: Tailscale-internal servers do not need additional auth
RULE: Public-facing MCP endpoints MUST validate Bearer token from dashboard
RULE: `.claude/mcp.json` is safe to commit — URLs and `${VAR}` references are not secrets
RULE: Each public MCP server manages its own tokens via its PWA dashboard

BANNED: Hardcoded Bearer tokens in committed mcp.json
BANNED: MCP servers exposed on 0.0.0.0 without token validation
BANNED: Storing secrets in `.claude/` directory
BANNED: Using `"type": "stdio"` in project mcp.json — HTTP only
