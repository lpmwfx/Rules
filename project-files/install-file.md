---
tags: [install, publishing, dual-repo, ci-cd]
concepts: [publishing-flow, dual-repo, distribution]
related: [project-files/workflow.md, project-files/changelog-file.md]
keywords: [dual-repo, public-repo, identity]
layer: 2
---
# INSTALL.md File

> Setup and publishing instructions — from private DEV to public install

---

## Quick Reference

- **Location:** `proj/INSTALL.md`
- **Format:** Markdown — `## Section` headings with commands and notes
- **Required:** Always
- **Owner:** User writes it — AI reads it for environment and publish steps

Documents how to run the project locally and how to publish it.
Not a task file — a reference for setup and release operations.

---

RULE: File lives at `proj/INSTALL.md`
RULE: Never publish `proj/` folder to public repo — it stays private
RULE: Verify no secrets in public repo before every push
RULE: Test install from public repo on a clean machine
RULE: DEV identity and installed identity must be distinct when applicable
RULE: CHANGELOG.md version must match package version on release
RULE: Keep local setup section minimal and copy-pasteable

## Format

```markdown
# INSTALL: project-name

## Requirements
- Python 3.11+
- Redis 7+ (for session storage)

## Dependencies
pip install -e ".[dev]"

## Run
python -m project

## Test
pytest

## Publish
- Registry: PyPI
- Tool: python -m build && twine upload dist/*
- Bump version in pyproject.toml before publishing
```

## Dual-Repo Pattern

Most projects use two repositories:

```
Private DEV repo (~/REPO)
  └── Full source, tests, dev tools
  └── proj/ (PROJECT.md, TODO.md, FIXES.md, etc.)
  └── .env, secrets references, infra config

Public repo (GitHub/Codeberg)
  └── Clean source only
  └── README.md, LICENSE, CHANGELOG.md
  └── No proj/, no .env, no dev tooling
```

### What Gets Published

| Include | Exclude |
|---------|---------|
| src/ | proj/ (all project management files) |
| tests/ | .env, secrets, credentials |
| README.md | doc/project.md (internal narrative) |
| LICENSE | dev scripts, infra configs |
| CHANGELOG.md | .claude/ settings |
| pyproject.toml / package.json / Cargo.toml | — |

## Publishing Flow

```
1. DEV complete → all tests pass, phase done
2. Prepare public repo
   → Copy publishable files (see table above)
   → Verify no proj/ or secrets in public
3. Identity check — DEV app-id ≠ installed app-id
4. Push to public repo
5. CI/CD runs → tests + build
6. Package published (PyPI / npm / crates.io)
7. Test install on clean machine — verify installed identity
```

## Distribution Methods

| Language | Tool | Registry |
|----------|------|----------|
| Python | pipx / pip | PyPI |
| Node.js | npm / npx | npm registry |
| Rust | cargo install | crates.io |
| Go | go install | Go modules |
