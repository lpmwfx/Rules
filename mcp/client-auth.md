---
tags: [mcp, client, auth, tokens, oauth, tailscale, security]
concepts: [mcp-auth, dashboard-tokens, network-auth]
requires: [mcp/client-config.md]
related: [mcp/server-build.md]
keywords: [auth, token, bearer, oauth, tailscale, dashboard, env-var, security]
layer: 2
---
# MCP Client Authentication

> Dashboard token in env var — or Tailscale network as perimeter

---

## Dashboard Token (recommended)

Each MCP server has a PWA dashboard for token management. Token goes in an env var.

**Flow:**
1. Open server dashboard (e.g. `https://articles.lpmintra.com/dash`)
2. Log in → generate API token
3. Set env var: `export ARTICLES_TOKEN=ey...`
4. `.mcp.json` picks it up via `${VAR}`

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

RULE: Each MCP server provides its own dashboard for token management
RULE: Tokens stored in environment variables, never in committed files
RULE: `${VAR}` syntax for interpolation — `${VAR:-default}` for fallback

## Tailscale Network (no auth needed)

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
RULE: Public-facing servers (`*.lpmintra.com`) MUST use auth headers

## OAuth 2.0 (not recommended yet)

Claude Code has OAuth support via DCR but has multiple open bugs — browser auth flow doesn't always trigger. Use dashboard tokens until OAuth stabilizes.

## Server Discovery Priority

1. **Public VPS** — `*.lpmintra.com` (auth required)
2. **Tailscale MagicDNS** — internal hostnames (no auth)
3. **localhost** — dev machine
4. **Environment variables** — `MCP_RULES_URL` etc. for CI/CD

RULE: Never hardcode IP addresses — they change
BANNED: MCP servers exposed on 0.0.0.0 without token validation
BANNED: Plaintext secrets in `.claude/mcp.json`
