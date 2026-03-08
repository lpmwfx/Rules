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
pip install --upgrade git+https://github.com/lpmwfx/RulesTools.git
pip install --upgrade git+https://github.com/lpmwfx/RulesToolsMCP.git
pip install --upgrade git+https://github.com/lpmwfx/Rules.git
```

## Update Workflow

```
edit files in local repo
  → git push
  → pip install --upgrade git+https://github.com/lpmwfx/...
  → restart Claude Code (MCP server reloads)
```

## Verification

After install, move or rename the source repo — MCP servers must stay up.
If any server dies: a runtime path dependency exists and must be fixed.

## BANNED

BANNED: `pip install -e .` (editable — creates runtime dependency on local path)
BANNED: `pip install .` from a local D:\ or C:\ path
BANNED: `sys.path.insert(0, "D:/REPO/...")` in any installed package
BANNED: Hardcoded local paths in `pyproject.toml`, `server.py`, or `scanner.py`
BANNED: `direct_url.json` referencing a local drive path after install

## Why

A local-path install ties the running MCP server to the filesystem layout of
one specific machine. If the repo moves, gets renamed, or the drive letter changes:
the server crashes. GitHub install is machine-independent and reproducible.
