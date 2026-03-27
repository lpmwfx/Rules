---
tags: [devops, environment, lxc, webhost, scanning, sync]
concepts: [dev-environment, scannable-environment, watcher-sync]
requires: [global/tools-and-scripts.md]
related: [devops/workflow.md, devops/cicd.md]
keywords: [lxc, container, webhost, shared-host, sync, watcher, rsync, development-environment, embedded, thin-host]
layer: 2
---
# Development Environment

> Develop where you can scan — sync to where you deploy

---

## Rule

All development happens in a full environment where code can be scanned, linted, tested, and built. Never develop directly on a target host that lacks tooling.

RULE: Development must happen in a scannable environment — never on a host that cannot run linters, scanners, and tests
RULE: Use an LXC container (or similar) as the development mirror for thin or restricted hosts

## Pattern

```
LXC container (full dev environment)
  ├── code, tools, scanner, linter, tests
  ├── watcher/sync script
  │   └── detects changes → syncs to target
  └── bun / node / php / cargo — full toolchain
        ↓ sync (rsync, fswatch, etc.)
Target host (webhost, embedded, shared host)
  └── production files only — no dev tooling
```

The watcher script is an owned script — it lives in `tools/` and runs on Bun (see [tools-and-scripts.md](../global/tools-and-scripts.md)).

## Why

Thin hosts (shared webhosts, embedded systems, minimal VPS) lack tooling. Developing directly on them means:
- No scanning — rule violations go undetected
- No linting — style and safety checks skipped
- No tests — changes are untested
- No AI assistance — AI tools need a full environment to work

An LXC container gives a full development environment for any target, no matter how restricted.

BANNED: Developing directly on a host that cannot run the project's scanner and linter
BANNED: Skipping scan/lint because "the host doesn't support it"
