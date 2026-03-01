---
tags: [changelog, release-notes, versioning]
concepts: [release-management, versioning]
related: [project-files/install-file.md, project-files/done-file.md]
layer: 2
---
# CHANGELOG.md File

> User-facing release notes — NOT for internal task tracking

---

## Quick Reference

- **Location:** `proj/CHANGELOG.md`
- **Format:** Markdown — `## vX.Y.Z - YYYY-MM-DD` sections, newest first
- **Required:** Always
- **Write rule:** Append only — update on release, never retroactively edit

User-facing record of what changed in each release. Not a task log —
summarize what users will notice. Published to the public repo.

---

RULE: File lives at `proj/CHANGELOG.md`
RULE: Only update CHANGELOG.md on release/deploy — not during development
RULE: Summarize what users see and experience — not implementation details
RULE: Newest release at TOP — append-only
RULE: Use semantic versioning (vMAJOR.MINOR.PATCH)
RULE: CHANGELOG.md version must match package metadata version on release
RULE: CHANGELOG.md is published to the public repo — DONE.md stays private

## Format

```markdown
# CHANGELOG: project-name

## v1.2.0 - 2026-01-24

- Dark mode now works correctly across all screens
- Improved mobile navigation — hamburger menu added
- Added job postings section to dashboard

## v1.1.0 - 2026-01-20

- New translation system — supports EN, DA, DE
- Better SEO — meta tags on all pages

## v1.0.0 - 2026-01-01

- Initial release
```

## DONE.md vs CHANGELOG.md

| Aspect | DONE.md | CHANGELOG.md |
|--------|---------|--------------|
| Audience | Developers | Users |
| Content | All tasks, phase details | Features and fixes users notice |
| Granularity | Every task | Summarized per release |
| Published | No (stays in proj/) | Yes (goes to public repo) |
