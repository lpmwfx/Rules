---
tags: [install, publishing, dual-repo, ci-cd]
concepts: [publishing-flow, dual-repo, distribution]
related: [project-files/workflow.md, project-files/changelog-file.md]
keywords: [dual-repo, public-repo, identity]
layer: 2
---
# INSTALL File

> Publishing and setup — from private DEV to public install

---

Format: Plain text

## Local Setup

How to get the project running from source (for development).

```
# INSTALL

## Requirements
Python 3.11+

## Dependencies
pip install -e ".[dev]"

## Run
python -m project

## Test
pytest
```

## Dual-Repo Pattern

Most projects use two repositories:

```
Private DEV repo (~/REPO or ~/PROD)
  └── Full source, tests, dev tools, project files
  └── Git history with WIP commits
  └── .env, secrets references, infra config

Public repo (GitHub/Codeberg)
  └── Clean source only
  └── Squashed or curated commits
  └── README, LICENSE, CHANGELOG
  └── No dev tooling, no project files, no secrets
```

### What Gets Published

| Include | Exclude |
|---------|---------|
| src/ | PROJECT, TODO, DONE, FIXES, RAG, ISSUES |
| tests/ | .env, secrets, credentials |
| README.md | doc/project.md (internal) |
| LICENSE | UIUX (internal spec) |
| CHANGELOG | dev scripts, infra configs |
| pyproject.toml / package.json | .claude/ settings |

## Publishing Flow

```
1. DEV complete → all tests pass, phase done
2. Prepare public repo
   → Copy publishable files
   → Strip dev-only content
   → Verify no secrets leaked
3. Identity check
   → DEV app-id ≠ installed app-id (if applicable)
   → Version, name, paths match public identity
4. Push to public repo
5. CI/CD runs → automated tests + build
6. Package published (PyPI / npm / crates.io / etc)
7. Test install on clean machine
   → pipx install / npm install -g / cargo install
   → Run basic smoke test
   → Verify installed identity (not DEV identity)
```

## Identity Difference

DEV and installed versions may have different identities:

```
DEV:       app-name-dev, localhost paths, debug logging
Installed: app-name, standard paths, production logging
```

RULE: Test install must show installed identity, not DEV identity
RULE: Version number must match between CHANGELOG and package metadata

## CI/CD

```
On push to public repo:
  → Run tests
  → Build package
  → Publish to registry (on tag/release)
```

## Distribution Methods

| Language | Tool | Registry |
|----------|------|----------|
| Python | pipx / pip | PyPI |
| Node.js | npm / npx | npm registry |
| Rust | cargo install | crates.io |
| Go | go install | Go modules |

## Rules

RULE: Never publish project files (PROJECT, TODO, FIXES, etc) to public repo
RULE: Verify no secrets in public repo before every push
RULE: Test install from public repo on clean environment
RULE: DEV identity and installed identity must be distinct when applicable
RULE: CHANGELOG version must match package version on release
RULE: Keep local setup minimal and copy-pasteable
