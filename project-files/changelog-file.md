---
tags: [changelog, release-notes, versioning]
concepts: [release-management, versioning]
related: [project-files/install-file.md, project-files/done-file.md]
layer: 2
---
# CHANGELOG File

> User-facing release notes — NOT for internal task tracking

---

Format: Plain text

```
# CHANGELOG

## v1.2.0 - 2026-01-24

- Dark mode now works correctly
- Improved mobile navigation
- Added job postings section

## v1.1.0 - 2026-01-20

- New translation system
- Better SEO optimization
```

## DONE vs CHANGELOG

| Aspect | DONE | CHANGELOG |
|--------|------|-----------|
| Audience | Developers | Users |
| Content | All tasks, phases | Features, fixes per version |
| Granularity | Every task | Summarized changes |
| Format | YAML (structured) | Text (readable) |

## Rules

RULE: Only update on release/deploy
RULE: Summarize what users see (not how it was built)
RULE: Use semantic versioning if applicable
