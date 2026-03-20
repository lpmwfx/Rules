---
tags: [install, architecture, site-packages, github, mandatory, infrastructure]
concepts: [install-architecture, deployment]
requires: [global/rules-repo-scope.md]
related: [global/secrets.md]
keywords: [pip install, site-packages, github, editable, D drive, REPO, local path, git+https]
layer: 1
---
# Install Architecture — Locked

> Packages install from GitHub — never from local paths

---

VITAL: No runtime or install-time dependency on any local drive path (D:, C:\REPO, etc.)
VITAL: All packages install from GitHub via `pip install git+https://...`
VITAL: After install, the package is 100% self-contained in site-packages
VITAL: Moving or deleting the source repo must NOT affect any running MCP server

---

## Canonical Install Commands

```bash
cargo install --git https://github.com/lpmwfx/RulesTools rulestools
```

For build.rs integration (scanner + documenter as library crates):

```toml
[build-dependencies]
rulestools-scanner    = { git = "https://github.com/lpmwfx/RulesTools" }
rulestools-documenter = { git = "https://github.com/lpmwfx/RulesTools" }
```

## Update Workflow

```
edit files in local repo
  → git push
  → cargo install --git https://github.com/lpmwfx/RulesTools rulestools --force
  → restart Claude Code (MCP server reloads)
```

## Verification

After install, move or rename the source repo — MCP servers must stay up.
If any server dies: a runtime path dependency exists and must be fixed.

## BANNED

BANNED: `path = "..."` dependencies in Cargo.toml (creates build-time dependency on local path)
BANNED: Hardcoded local paths in Cargo.toml, build.rs, or any installed binary
BANNED: `cargo install --path .` from a local D:\ or C:\ path for production use

## Why

A local-path install ties the running MCP server to the filesystem layout of
one specific machine. If the repo moves, gets renamed, or the drive letter changes:
the server crashes. GitHub install is machine-independent and reproducible.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
