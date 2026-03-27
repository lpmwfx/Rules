---
tags: [mcp, client, templates, project-type]
concepts: [mcp-templates, per-project-servers]
requires: [mcp/client-config.md, mcp/client-auth.md]
related: [global/topology-profiles.md]
keywords: [template, rust, laravel, python, content, gui, cli, mcp.json]
layer: 2
---
# MCP Client Templates

> One template per project type — select during initialization

---

## Available Servers

### Core — every project

| Server | Purpose |
|---|---|
| `rules` | Rule lookup, search, context |
| `rulestools` | Scan, setup, init, publish |

### Development

| Server | Purpose |
|---|---|
| `issuesmcp` | Forgejo/GitHub issue CRUD |

### Content & Publishing (public VPS, auth required)

| Server | Purpose |
|---|---|
| `articles` | Article publish pipeline |
| `audience` | SEO, web intelligence |

## Templates

### Rust CLI / Library

```json
{
  "mcpServers": {
    "rules": { "type": "http", "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}" },
    "rulestools": { "type": "http", "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}" },
    "issuesmcp": { "type": "http", "url": "${MCP_ISSUES_URL:-http://localhost:PORT/issues}" }
  }
}
```

### Rust GUI (Slint)

Same as CLI + `gui-mcp` for Windows GUI automation.

### Laravel Web Application

Same as Rust CLI template — rules + rulestools + issues.

### Content Site

Rules + rulestools + articles (auth) + audience (auth).

```json
{
  "mcpServers": {
    "rules": { "type": "http", "url": "${MCP_RULES_URL:-http://localhost:PORT/rules}" },
    "rulestools": { "type": "http", "url": "${MCP_TOOLS_URL:-http://localhost:PORT/tools}" },
    "articles": {
      "type": "http",
      "url": "https://articles.lpmintra.com/mcp",
      "headers": { "Authorization": "Bearer ${ARTICLES_TOKEN}" }
    },
    "audience": {
      "type": "http",
      "url": "https://audienceintelligence.lpmintra.com/mcp",
      "headers": { "Authorization": "Bearer ${AUDIENCE_TOKEN}" }
    }
  }
}
```

RULE: Replace PORT placeholders with actual ports during init
RULE: Verify each server responds before continuing
