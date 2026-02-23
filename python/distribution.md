# Clean Distribution Policy

> Separate private monorepo from public release repo

---

RULE: Separate private monorepo from public release repo
RULE: Public repo contains ONLY installable package (no tests, scripts, config)

## Private (Development) Structure

```
ProjectName/                    # Private monorepo
├── package_name/               # Python package
├── tests/                      # Test suite
├── scripts/                    # Dev scripts
├── proj/                       # Institution files
├── rules/                      # Project rules
└── pyproject.toml              # Dev config
```

## Public (Release) Structure

```
package-name/                   # Public release repo
├── package_name/               # Python package ONLY
├── pyproject.toml              # With [build-system]
├── LICENSE
├── README.md
└── .gitignore
```

## Required pyproject.toml for pipx

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [...]

[project.scripts]
cli-command = "package_name.__main__:main"

[tool.hatch.build.targets.wheel]
packages = ["package_name"]
```

## Workflow

1. Develop in private monorepo
2. Copy `package_name/` to public repo when releasing
3. Bump version in public pyproject.toml
4. Push to public repo
5. Users install: `pipx install git+https://codeberg.org/ORG/package-name.git`

BANNED: Tests, scripts, dev config in public release repo
BANNED: `__pycache__`, `.env`, local paths in public repo
RULE: Public repo is minimal — only what's needed to install
