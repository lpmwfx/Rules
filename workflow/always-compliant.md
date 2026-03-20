---
tags: [workflow, compliance, proactive, process]
concepts: [proactive-compliance, ai-workflow, preparation]
keywords: [compliant, before, during, verify, mcp, context, violations]
layer: 2
requires: [global/startup.md, global/topology.md]
feeds: [workflow/load-context.md, workflow/coding-discipline.md]
related: [global/file-limits.md, global/topology.md, workflow/read-violations.md, workflow/commit-clean.md]
---

# Proactive Compliance — BEFORE, DURING, VERIFY

## The Problem

Violations are discovered AFTER code is written. AI agents loop: write → scan → fix → re-commit.
This is reactive compliance — violations are the normal case, rework is expected.

## The Solution

**Compliance-first mindset:** Work WITHIN rules from the start.
Violations become the exception, not the norm.
Zero rework loops.

---

## Three Phases: AI Compliance Workflow

### PHASE 1: BEFORE you edit a file

**Goal:** Know which rules apply to this file before you write any code.

1. **Identify file context** (3-5 seconds)
   - Call `get_file_context(path)` (new MCP tool)
   - Returns: language, topology layer, import rules, key rule files
   - Alternative: `get_context([language], quick_ref: true)` for combo rules

2. **Check file size limits** (1 second)
   - Reference: `global/file-limits.md`
   - Know the max lines for this file type BEFORE editing
   - If file is 80% of limit → you must split it FIRST, before adding code

3. **Know the topology constraints** (1 second)
   - What can this layer import?
   - Where must public types go?
   - What suffix must public types carry?
   - Reference: `global/topology.md`

4. **Load key rules** (optional but recommended)
   - Get full rule files for your language/layer
   - `get_context([language])` → all rules for this language
   - Skim the quick-ref for 30 seconds

**Time cost:** 5 minutes once, then 10 seconds per file (cached context).

---

### PHASE 2: DURING coding

**Goal:** Write code that is correct by default, not by accident.

**Topology awareness:**
- Import only allowed layers (no cycles)
- Place new types in correct modules
- Use correct layer suffix on public types

**Naming discipline:**
- Constants: always named (never magic numbers)
- Booleans: correct prefix (`is_`, `has_`, `can_`)
- Functions: no noise names (`do_thing`, `helper`)

**Size discipline:**
- Count lines mentally as you write
- If approaching limit → split BEFORE you hit it
- Don't wait for scanner to tell you file is too large

**Error discipline:**
- Use `?` and Result types (no `.unwrap()` in non-test code)
- No stringly-typed matches (use enums)
- No magic numbers or hardcoded strings

**Scanning during development** (optional but recommended):
- Call `scan_file(path)` after each logical edit
- PostToolUse hook runs `scan_file` automatically after Edit/Write
- Read violations IMMEDIATELY — fix them before continuing
- Reference: `workflow/read-violations.md` for violation Q&A

---

### PHASE 3: VERIFY before commit

**Goal:** Ensure only clean code gets staged.

1. **Check staged files** (1 second)
   - Call `check_staged()` before committing
   - Shows violations in staged code only
   - If any [NEW] errors → fix and re-stage (do not bypass)

2. **Scan entire project** (before pull request)
   - Call `scan_tree()` for full visibility
   - Check proj/ISSUES [NEW] vs [KNOWN]
   - [NEW] errors must be fixed before PR

3. **Understand: when pre-commit blocks you**
   - `check_staged()` blocks commit if [NEW] errors exist
   - This is intentional — never use `--no-verify`
   - Fix violations, stage again, commit
   - Violation → fix → re-stage → commit (no bypass)

**Time cost:** 30 seconds per commit.

---

## Why This Matters

**Reactive compliance:**
```
write code → scan finds 5 violations → fix each one → re-stage → commit (1 rework loop)
```

**Proactive compliance:**
```
load context → write code → check_staged() passes → commit (0 rework loops)
```

Rework loops compound:
- Each fix requires re-reading the violation
- Each re-stage requires re-running the scan
- Each violation adds cognitive load

**Proactive compliance eliminates rework:** Work correctly the first time.

---

## MCP Tools Activated at Each Phase

| Phase | Tool | Purpose |
|-------|------|---------|
| BEFORE | `get_file_context(path)` | Load language + layer + rules |
| BEFORE | `get_context([lang], quick_ref: true)` | Load compact combo rules |
| BEFORE | `get_rule(file)` | Deep dive into specific rule |
| DURING | `scan_file(path)` | Immediate feedback on violations |
| DURING | `get_rule(file)` | Understand violation (via rule hint links) |
| VERIFY | `check_staged()` | Pre-commit gate |
| VERIFY | `scan_tree()` | Full project visibility |

---

## Discipline Requirements

### For AI Agents (Claude, etc.)

- **VITAL:** Always call `get_file_context()` BEFORE editing a file
- **VITAL:** Always call `check_staged()` BEFORE committing
- **RULE:** Fix violations in order: TOPOLOGY > MOTHER-CHILD > SAFETY > HYGIENE > LITERALS
- **RULE:** Never ignore `check_staged()` violations — understand and fix them
- **BANNED:** Committing code with [NEW] violations

### For Humans

- Read `workflow/load-context.md` to understand BEFORE phase
- Read `workflow/coding-discipline.md` for naming/size/error conventions
- Read `workflow/read-violations.md` for violation Q&A
- Read `workflow/commit-clean.md` for pre-commit discipline

---

## Learning Path

Start here → read → apply:

1. **BEFORE phase:** `workflow/load-context.md`
2. **DURING phase:** `workflow/coding-discipline.md`
3. **Understand violations:** `workflow/read-violations.md`
4. **VERIFY phase:** `workflow/commit-clean.md`

---

## Glossary

- **Compliance:** Code that passes all 50 scanner checks
- **[NEW] error:** Violation introduced in current commit
- **[KNOWN] error:** Violation that existed before
- **Rework loop:** Write → scan → fix → re-stage → commit (N > 0 iterations)
- **Proactive:** Know rules BEFORE writing
- **Reactive:** Discover violations AFTER writing

---

## Next Steps

- Read `workflow/load-context.md` — implement BEFORE phase
- Read `workflow/coding-discipline.md` — internalize naming/size/error rules
- Read `workflow/read-violations.md` — learn violation Q&A
- Read `workflow/commit-clean.md` — pre-commit discipline


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
