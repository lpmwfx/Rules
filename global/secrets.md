---
tags: [secrets, env, security]
concepts: [security, environment]
keywords: [secrets, password, api-key, token, credential, env, security]
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


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
