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

### 1. Environment Variable Interpolation (recommended)

Secrets stay in environment, not in committed files:

```json
{
  "mcpServers": {
    "articles": {
      "type": "http",
      "url": "https://articles.lpmintra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_ARTICLES_TOKEN}"
      }
    }
  }
}
```

Syntax: `${VAR}` expands at runtime. `${VAR:-default}` provides fallback.
Works in: `url`, `headers`, `command`, `args`, `env`.

### 2. Static Headers (simple, non-secret environments)

```json
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://api.internal.com/mcp",
      "headers": {
        "X-API-Key": "fixed-key"
      }
    }
  }
}
```

RULE: Only use static headers for non-secret values or Tailscale-internal servers

### 3. Headers Helper (dynamic tokens)

Shell command runs on each connection, outputs JSON headers to stdout:

```json
{
  "mcpServers": {
    "secure-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headersHelper": "get-mcp-token.sh"
    }
  }
}
```

The command must:
- Output valid JSON: `{"Authorization": "Bearer xyz"}`
- Complete within 10 seconds
- Dynamic headers override static `headers` with same name

### 4. OAuth 2.0 (browser login flow)

For servers supporting OAuth — user authenticates via browser:

```json
{
  "mcpServers": {
    "cloud-service": {
      "type": "http",
      "url": "https://mcp.service.com/mcp",
      "oauth": {
        "clientId": "your-client-id",
        "callbackPort": 8080
      }
    }
  }
}
```

After adding: run `/mcp` in Claude Code → follow browser login → tokens stored in keychain.

Override metadata discovery for OIDC:
```json
"oauth": {
  "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
}
```

### 5. Tailscale Network (no auth needed)

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

RULE: Tailscale-internal servers skip auth — MagicDNS hostname is sufficient
RULE: Public-facing servers (VPS, cloud) MUST use one of the auth methods above

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

### Content & Publishing (public VPS — auth required)

| Server | URL | Purpose | Tools |
|--------|-----|---------|-------|
| `articles` | `https://articles.lpmintra.com/mcp` | Article publish pipeline | 15 |
| `audience` | `https://audienceintelligence.lpmintra.com/mcp` | SEO, web intelligence, inspiration | 18 |

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
        "Authorization": "Bearer ${MCP_ARTICLES_TOKEN}"
      }
    },
    "audience": {
      "type": "http",
      "url": "https://audienceintelligence.lpmintra.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_AUDIENCE_TOKEN}"
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

RULE: No plaintext secrets in `.claude/mcp.json` — use `${VAR}` interpolation or `headersHelper`
RULE: Tailscale-internal servers do not need additional auth
RULE: Public-facing MCP endpoints MUST require authentication
RULE: `.claude/mcp.json` is safe to commit — URLs and `${VAR}` references are not secrets
RULE: OAuth tokens are stored in system keychain — never in config files

BANNED: Hardcoded Bearer tokens in committed mcp.json
BANNED: MCP servers exposed on 0.0.0.0 without authentication
BANNED: Storing secrets in `.claude/` directory
BANNED: Using `"type": "stdio"` in project mcp.json — HTTP only
