---
tags: [secrets, env, security]
concepts: [security, environment]
related: [devops/publishing.md, devops/cicd.md]
layer: 1
---
# Secrets Location

> Central secrets, never copied into projects

---

PATH: ~/.env/ — central secrets folder
RULE: Use directly from ~/.env/ — never copy secrets into projects
RULE: Reference via symlink or env var, not duplication
BANNED: Copying .env files into project folders
BANNED: Secrets in git repos (even gitignored copies)
