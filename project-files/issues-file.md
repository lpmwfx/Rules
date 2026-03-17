---
tags: [issues, fifo, problem-queue, forgejo, mcp, ai-reported]
concepts: [issue-tracking, fifo, problem-resolution, remote-issues]
feeds: [project-files/fixes-file.md]
related: [project-files/todo-file.md, project-files/project-process.md, global/topology.md]
keywords: [fifo, open, committed, resolved, forgejo, report_issue, list_issues, close_issue, ai-reported, mcp]
layer: 2
---
# ISSUES — Local + Remote Issue Tracking

> Two systems, one workflow: local `proj/ISSUES` for scanner output, remote Forgejo for cross-project tracking

---

## Quick Reference

- **Local:** `proj/ISSUES` — scanner writes here automatically
- **Remote:** Forgejo at `https://git.lpmintra.com/lpmwfx/issues`
- **MCP tools:** `report_issue`, `list_issues`, `close_issue`
- **Labels:** component (scanner, documenter, mcp-tools, rules) + type (bug, debt, architecture, security) + source (ai-reported)

---

## 1. Local Issues (`proj/ISSUES`)

Scanner writes issues here automatically on every `rulestools scan`.
Format: `[NEW]` / `[KNOWN]` prefix + VSCode-compatible line format.

RULE: `proj/ISSUES` is written by the scanner — never edit by hand
RULE: Each issue line includes `[rule_file.md]` reference for lookup
RULE: `[NEW]` = first time seen, `[KNOWN]` = existed in previous scan
RULE: Fix errors top-down: TOPOLOGY → PURITY → MOTHER-CHILD → LITERALS → SAFETY → HYGIENE

```
# 11 issues

[NEW] src/main.rs:79:1: error rust/types/no-string-match: stringly-typed match "mica" [rust/types.md]
[KNOWN] src/main.rs:137:1: error rust/constants/no-magic-number: magic number 2 [rust/constants.md]
```

## 2. Remote Issues (Forgejo)

Cross-project issue tracking for the RulesTools ecosystem.
AI reports issues via MCP, tracks them across sessions.

RULE: Use `list_issues` before `report_issue` to avoid duplicates
RULE: `ai-reported` label is always added automatically
RULE: Add component label (scanner, documenter, mcp-tools, rules, man-viewer)
RULE: Add type label (bug, debt, architecture, security)
RULE: Close issues with `close_issue` when fixed — include comment

### MCP Tools

**report_issue** — report a new issue:
```
report_issue(
  title: "layer-violation false positive on same-layer imports",
  body: "adapter/ files importing other adapter/ files flagged as violation",
  labels: "bug,scanner"
)
→ Issue #4 created: https://git.lpmintra.com/lpmwfx/issues/issues/4
```

**list_issues** — check existing issues:
```
list_issues(state: "open")
→ #4 [open] layer-violation false positive  ai-reported, bug, scanner

list_issues(state: "all", labels: "scanner")
→ shows all scanner-related issues
```

**close_issue** — mark as fixed:
```
close_issue(number: 4, comment: "Fixed: same-layer imports now allowed")
→ Issue #4 closed
```

### Labels

| Category | Labels |
|----------|--------|
| Component | scanner, documenter, mcp-rules, mcp-tools, rules, man-viewer, slint-ui-templates |
| Type | bug, debt, architecture, security |
| Source | ai-reported (automatic) |

### Workflow

1. AI discovers problem during development
2. `list_issues(labels: "scanner")` — check if already reported
3. `report_issue(title, body, labels)` — report if new
4. Fix the issue in code
5. `close_issue(number, comment)` — close with explanation

BANNED: Reporting without checking for duplicates first
BANNED: Closing issues without a comment explaining the fix
BANNED: Manual editing of `proj/ISSUES` — scanner owns that file
