---
tags: [done, archive, completed-phases]
concepts: [phase-completion, archive]
requires: [project-files/todo-file.md, project-files/phases-file.md]
layer: 2
---
# DONES Folder

> Completed TODO files — append-only archive folder

---

## Quick Reference

- **Location:** `proj/DONES/` (folder)
- **Files:** One file per completed TODO — dumped as-is when done
- **Naming:** `<TODO-NAME>-<phase>-<id>.md` or descriptive name
- **Required:** Always (folder must exist)
- **Write rule:** Drop files in — never edit files already in DONES/

When a TODO file is fully complete, move it into `proj/DONES/` unchanged.
Create a new TODO for the next batch of work.

---

RULE: Folder lives at `proj/DONES/`
RULE: Each file in DONES/ is a completed TODO file dropped in as-is
RULE: Never edit files already in DONES/ — the folder is append-only
RULE: DONES/ grows forever — it is the project history
RULE: Naming: use the original TODO filename plus phase/date for disambiguation

## Format

```
proj/
└── DONES/
    ├── TODO-phase1-rules-quality.md      ← completed primary TODO
    ├── TOOL-TODO-phase1-scanner.md       ← completed parallel workstream
    └── AUT-TODO-phase2-automation.md     ← another completed workstream
```

Each file is the original TODO content — no transformation required.

## Rules

RULE: Do not summarize or transform TODO content when archiving — dump the file as-is
RULE: If a TODO was only partially done when replaced, note `archived:` date at top


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
