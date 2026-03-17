---
tags: [catalog, library, rust, scanner, enforcement, topology, rulestools]
concepts: [library, static-analysis, code-quality, topology-enforcement]
type: library
name: rulestools
languages: [rust]
layers: [_core, _x]
related: [global/topology.md, global/mother-tree.md, global/stereotypes.md]
layer: 3
---
# rulestools — Unified Static Code Scanner

Enforces coding rules from the Rules repo across all languages.
One Rust workspace replacing 7 separate repos.

> Repo: `https://github.com/lpmwfx/RulesTools`

---

## What It Provides

| Component | Purpose |
|-----------|---------|
| `crates/scanner/` | 26 checks, severity resolver, grouped output |
| `crates/documenter/` | `///` doc parser + man/ generator |
| `apps/cli/` | `rulestools` binary (scan/check/list/detect/gen/issue) |
| `apps/mcp-rules/` | MCP server for rule lookup |
| `apps/mcp-tools/` | MCP server for scan/init (thin, delegates to CLI) |

---

## Usage

```bash
# Install from GitHub
cargo install --git https://github.com/lpmwfx/RulesTools rulestools

# Scan project
rulestools scan .

# Pre-commit check
rulestools check .

# Build.rs integration
rulestools_scanner::scan_project();
```

---

## ProjectKinds

Tool → CliApp → Library → SlintApp → Super

Scanner adapts severity per kind. Same checks, different enforcement.
