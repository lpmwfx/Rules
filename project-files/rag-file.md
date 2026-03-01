---
tags: [rag, knowledge-base, ai-memory]
concepts: [knowledge-base, ai-memory]
related: [project-files/fixes-file.md, global/persistent-memory.md]
layer: 2
---
# RAG.md File

> Project knowledge base — discoveries, links, patterns

---

## Quick Reference

- **Location:** `proj/RAG.md`
- **Format:** Markdown — `## Category` sections with bullet lists
- **Required:** Always
- **Purpose:** Freeform knowledge — what AI has learned about this project

Grows organically as AI discovers facts, patterns, and useful links.
Not a task list — a lookup reference. Short, precise entries only.

---

RULE: File lives at `proj/RAG.md`
RULE: Organized by category — one `##` heading per topic area
RULE: Short, precise entries — lookup reference, not prose
RULE: AI writes discoveries here during work
RULE: AI reads RAG.md for context before starting new areas

## Format

```markdown
# RAG: project-name

## API Endpoints
- POST /auth/login → returns JWT in body (not header)
- GET /items?page=N → paginated, max 50 per page
- Docs: http://localhost:8000/docs (dev only)

## Database
- PostgreSQL 15, schema in src/db/schema.sql
- Migrations: alembic, run `alembic upgrade head`
- Connection string in ~/.env/db.env

## Deployment
- Host: vps.example.com, user: deploy
- Path: /var/www/project/
- Command: `./scripts/deploy.sh`

## Known Gotchas
- Safari does not support CSS subgrid without prefix — see FIXES 2026-01-20
- Auth token expires after 30 min — refresh via /auth/refresh
```

## Rules

RULE: Only write facts that are true now — remove stale entries
RULE: Link to FIXES.md for problems already solved (`see FIXES YYYY-MM-DD`)
