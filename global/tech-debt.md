---
tags: [quality, tech-debt, todo, fixme, comments]
concepts: [code-quality, technical-debt]
layer: 1
keywords: [TODO, FIXME, HACK, NOCOMMIT, XXX, temp, workaround]
---
# Technical Debt Markers

> No debt markers in committed code — fix it or file a ticket

---

BANNED: `TODO` comments in committed code — create a ticket instead
BANNED: `FIXME` comments — fix before committing
BANNED: `HACK` or `WORKAROUND` comments — refactor instead
BANNED: `NOCOMMIT` — must never reach a commit
BANNED: `XXX` markers — use a ticket

PRINCIPLE: If it is not worth fixing now, it is not worth shipping
REASON: AI generates TODO markers as placeholders — they accumulate silently

## What to do instead

- Urgent: fix it before committing
- Important but deferred: create an entry in `proj/TODO` with a concrete description
- Won't fix: document the decision in `proj/PROJECT` with the reason

## Severity

`NOCOMMIT` and `HACK` → error (blocks commit)
`TODO`, `FIXME`, `XXX` → warning (shown in ISSUES, does not block)
