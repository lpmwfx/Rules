# Private-to-Public Publishing

> Separate private dev repo from clean public release repo

---

## Repo Separation

RULE: Private repo holds ALL code — source, tests, proj/, docs, dev scripts
RULE: Public repo holds ONLY distributable content — source, build config, LICENSE, README
RULE: Public repo can be open-source OR private/commercial
BANNED: Institution files (proj/) in public repo
BANNED: Dev scripts, .claude/, doc/ in public repo
BANNED: Test suites in public repo (unless library with user-facing tests)

## Private (Development) Structure

```
ProjectName/                    # Private dev repo
├── src/                        # Source code
├── tests/                      # Test suite
├── bin/                        # Dev scripts (publish.sh)
├── proj/                       # Institution files
├── doc/                        # Design docs
├── .claude/                    # AI session config
├── .github/                    # Workflows (may sync to public)
├── build config                # CMakeLists.txt / pyproject.toml / etc.
├── LICENSE
└── README.md
```

## Public (Release) Structure

```
project-name/                   # Public release repo
├── src/                        # Source code (synced from private)
├── .github/workflows/          # CI/CD (builds + releases)
├── build config                # CMakeLists.txt / pyproject.toml / etc.
├── LICENSE
├── README.md
└── .gitignore
```

## Publish Script

RULE: Use `bin/publish.sh` to sync private to public repo
RULE: Script uses rsync with explicit excludes — no manual copying
RULE: Always review diff in public repo before committing

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="${SRC}/../ProjectName-publish"

rsync -av --delete \
    --exclude='.git' \
    --exclude='proj/' \
    --exclude='doc/' \
    --exclude='.claude/' \
    --exclude='bin/' \
    --exclude='tests/' \
    --exclude='__pycache__/' \
    --exclude='build/' \
    --exclude='.env' \
    "$SRC/" "$DST/"

echo "Synced to $DST — review diff before committing"
```

## Release Workflow

```
develop → test → publish.sh → review diff → commit → tag → push
```

1. Develop and test in private repo
2. Run `bin/publish.sh` to sync to public repo
3. Review diff in public repo (`git diff`)
4. Commit: `git add -A && git commit -m "Sync from dev"`
5. Tag: `git tag v{MAJOR}.{MINOR}.{PATCH}`
6. Push: `git push origin main --tags`
7. CI builds and publishes release artifacts

## Version Strategy

RULE: Use semantic versioning — `v{MAJOR}.{MINOR}.{PATCH}`
RULE: Tags trigger CI release builds (tag pattern: `v*`)
RULE: MAJOR = breaking changes, MINOR = new features, PATCH = fixes
RULE: First release is `v0.1.0` (pre-1.0 = unstable API)
BANNED: Untagged releases
BANNED: Manual version bumps in multiple places — single source of truth
