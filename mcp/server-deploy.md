---
tags: [mcp, deploy, openrc, nginx, service, subdomain]
concepts: [mcp-deploy, service-management, reverse-proxy]
requires: [mcp/server-build.md]
related: [mcp/server-session.md, devops/dev-environment.md]
keywords: [deploy, openrc, nginx, service, subdomain, proxy, ssl, log, port]
layer: 4
---
# MCP Server Deployment

> OpenRC service + Nginx reverse proxy + subdomain registration

---

## OpenRC Service

Each MCP server runs as an OpenRC service on the LXC container.

```sh
#!/sbin/openrc-run
name="{name}-mcp"
description="{Name} MCP Server (Bun)"
command="/usr/local/bin/bun"
command_args="run /opt/ai-gov/{name}.ts"
command_user="dev"
directory="/opt/ai-gov"
pidfile="/run/${RC_SVCNAME}.pid"
command_background=true
output_log="/var/log/{name}-mcp.log"
error_log="/var/log/{name}-mcp.err"

export {NAME}_PORT="{port}"
export AUTH_STORE_PATH="/home/dev/auth/{name}-mcp.json"
```

```bash
sudo chmod +x /etc/init.d/{name}-mcp
sudo touch /var/log/{name}-mcp.{log,err}
sudo chown dev:dev /var/log/{name}-mcp.{log,err}
sudo rc-update add {name}-mcp default
sudo rc-service {name}-mcp start
```

RULE: One service per MCP server
RULE: Logs to /var/log/{name}-mcp.log — owned by dev user
RULE: Auth store path via env var — never hardcoded

## Nginx Reverse Proxy

Each server gets a subdomain with Nginx proxying to localhost.

```nginx
server {
    listen 80;
    server_name {name}.lpmintra.com;

    location / {
        proxy_pass http://127.0.0.1:{port};
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

RULE: Buffering off — SSE streams must not be buffered
RULE: Timeout 86400s — long-lived MCP sessions
RULE: SSL terminates at VPS, not at container

## package.json Scripts

```json
"{name}": "bun run {name}.ts",
"dev:{name}": "bun run --watch {name}.ts"
```

## New Server Checklist

- [ ] Entry point: `{name}.ts` with session recovery
- [ ] Tools: `src/tools/{name}.ts` with AIUX
- [ ] SYSTEM_HELP + MANPAGES written
- [ ] package.json: scripts added
- [ ] Nginx: server block in `deploy/mcp-servers.conf`
- [ ] OpenRC: `/etc/init.d/{name}-mcp`
- [ ] Log files created and owned by dev
- [ ] Auth store: `/home/dev/auth/{name}-mcp.json`
- [ ] Subdomain registered
- [ ] Health check: `curl localhost:{port}/health`
- [ ] AIUX verified: help + manpage on all tools
- [ ] Session recovery: restart → tool call works
