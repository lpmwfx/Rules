---
tags: [license, project-files, legal, open-source, proprietary]
concepts: [project-license, legal-compliance, distribution]
related: [project-files/project-file.md, project-files/changelog-file.md]
keywords: [LICENSE, license, EUPL, MIT, proprietary, copyright, legal]
layer: 2
---
# LICENSE File

> Legal license for the project — determines distribution and usage rights

---

## Quick Reference

RULE: Every project MUST have a LICENSE file in the project root.
RULE: LICENSE has no file extension — it is a plain text file.
RULE: License type is declared in `proj/rulestools.toml` under `[publish].license`.

---

## Format

Plain text — the full license text. No YAML frontmatter, no Markdown formatting.

## Supported Licenses

| License | Use case |
|---------|----------|
| EUPL-1.2 | Default for open source (European Union Public Licence) |
| MIT | Permissive open source |
| proprietary | Closed source — "All rights reserved" |

## Generation

`rulestools` generates LICENSE automatically from `[publish].license` config:

```toml
[publish]
license = "EUPL-1.2"
author = "TwistedBrain"
```

BANNED: Committing code without a LICENSE file.
BANNED: Using a license that contradicts project dependencies.
