---
tags: [workflow, verify, commit, discipline, pre-commit]
concepts: [proactive-compliance, pre-commit-gate, verification]
keywords: [commit, verify, pre-commit, check-staged, scan-tree, [NEW], [KNOWN]]
layer: 3
requires: [workflow/always-compliant.md, workflow/coding-discipline.md, workflow/read-violations.md]
feeds: []
related: [workflow/read-violations.md, global/file-limits.md, global/topology.md]
---

# VERIFY: Commit Clean

## Goal

Ensure only clean code gets committed.
Use the pre-commit gate as your final checkpoint.

---

## Step 1: Check Staged Files Before Commit

### Rule: Call `check_staged()` before every commit

```
check_staged()
```

Returns violations in staged files only.

**Output format:**
```
Staged violations:

[NEW] TOPOLOGY/layer-violation: src/core/engine.rs:12
[NEW] SAFETY/no-unwrap: src/core/config.rs:45
[KNOWN] HYGIENE/file-limits: src/gateway/http.rs:1
  (This violation exists, but was not introduced by this commit)

Result: FAIL — [NEW] errors present
```

**Meaning:**
- `[NEW]`: Violation introduced in this commit (blocks commit)
- `[KNOWN]`: Violation that existed before (doesn't block)

---

## Step 2: Handle [NEW] Violations

### If `check_staged()` returns [NEW] errors:

1. **Don't bypass.** Never use `--no-verify` or `--no-gpg-sign`.
   Bypass defeats the purpose of compliance-first.

2. **Fix the violations** (using `workflow/read-violations.md` guide):
   - Call `scan_file(path)` for the affected file
   - Read violation group + Q&A
   - Fix the violation
   - Re-scan to confirm

3. **Re-stage the fix**:
   ```
   git add src/core/engine.rs
   ```

4. **Re-run check_staged()**:
   ```
   check_staged()
   ```

5. **Commit** when check_staged() returns PASS.

---

## Step 3: Understand [KNOWN] Violations

`[KNOWN]` violations don't block commits. They were already there.

### Option A: Fix them in this commit (recommended)

```
1. Fix the violation (using workflow/read-violations.md guide)
2. Re-stage
3. Commit (now both [NEW] and fixed [KNOWN] are clean)
```

### Option B: Defer to next sprint

If it's a large refactor, you can defer:

```
1. Just commit with [KNOWN] violations present
2. Create ticket to fix them later
3. Track in proj/TODO
```

**Best practice:** If you can fix a [KNOWN] violation in 2-3 minutes, do it now.
Otherwise, defer and track.

---

## Step 4: Scan Entire Project Before PR

Before creating a pull request, get full visibility:

```
scan_tree()
```

Returns all violations in the project (not just staged).

**Output:**
```
Project violations:

[NEW] TOPOLOGY/layer-violation: src/core/engine.rs:12
[NEW] SAFETY/no-unwrap: src/core/config.rs:45
[KNOWN] HYGIENE/file-limits: src/gateway/http.rs:1
  (150 more violations...)

Summary: 2 [NEW], 152 [KNOWN]
```

**Action:**
- [NEW] violations in your commit: MUST FIX before PR
- [KNOWN] violations from other commits: OK to ignore (pre-existing)

---

## When Pre-Commit Hook Blocks You

### Scenario: You try to commit, hook fails

```bash
$ git commit -m "Add feature X"
✗ Pre-commit check failed
  [NEW] SAFETY/no-unwrap: src/core/engine.rs:45
  Fix violations and re-stage.
```

### What happened?

The hook ran `check_staged()` and found [NEW] errors.
Commit was rejected. (Intentional.)

### What to do?

1. **Understand the violation**:
   ```
   scan_file("src/core/engine.rs")
   ```

2. **Fix it** (using `workflow/read-violations.md`):
   - Read violation group
   - Call `get_rule(file)` for rule details
   - Apply fix strategy

3. **Re-stage**:
   ```
   git add src/core/engine.rs
   ```

4. **Retry commit**:
   ```
   git commit -m "Add feature X"
   ```

5. **If still failing**, repeat steps 1-4.

### Never use `--no-verify`

**BANNED:** `git commit --no-verify`

This bypasses the pre-commit hook and violates compliance-first discipline.
If the hook blocks you, it's because your code has violations.
Fix them instead of bypassing.

**Why?** Because:
- Violations pushed to main are visible to everyone
- Every team member sees [NEW] errors and has to deal with them
- It normalizes broken code
- It defeats the purpose of compliance-first

---

## Commit Discipline: The Full Loop

```
1. load-context() — BEFORE editing
2. Code with discipline — DURING editing
3. scan_file() (optional) — catch violations immediately
4. check_staged() — BEFORE committing
5. If [NEW] errors: fix + re-stage + retry (loop until clean)
6. Commit when check_staged() = PASS
7. scan_tree() (before PR) — full project visibility
8. Create PR
```

**Time cost per commit:** 30-60 seconds (mostly already spent in coding).

---

## proj/ISSUES — Tracking Violations

When you run `scan_tree()`, a file `proj/ISSUES` is written:

```
[NEW] TOPOLOGY/layer-violation: src/core/engine.rs:12
[KNOWN] HYGIENE/file-limits: src/gateway/http.rs:1
  (more violations...)
```

**[NEW]:** Violations in commits not yet pushed.
**[KNOWN]:** Violations from main branch (pre-existing).

**Interpretation:**
- If you introduce a [NEW] violation, fix it before committing
- [KNOWN] violations are tracked for refactoring later (not your responsibility now)

---

## Severity Resolver: [ERROR] vs [WARN]

Same check, different enforcement by ProjectKind:

| ProjectKind | Behavior |
|---|---|
| SlintApp | All checks: [ERROR] (full enforcement) |
| CliApp | Most checks: [WARN], topology: [ERROR] |
| Library | Most checks: [WARN], errors: [ERROR] |
| Tool | Few checks: [ERROR], mostly [WARN] |

**Meaning:**
- [ERROR]: Blocks commit (in pre-commit hook)
- [WARN]: Noted, doesn't block, but should fix

**Your job:** Fix [ERROR] violations before committing.

---

## FAQ

**Q: Can I commit with [KNOWN] violations?**

A: Yes. They existed before your commit. But if you can fix them in 2-3 min, do it.

**Q: Can I commit with [WARN] violations?**

A: Yes, they don't block commits. But fix them in next sprint.

**Q: What if I disagree with a violation?**

A: 1) Read the rule file (`get_rule(file)`)
2) Understand the rationale
3) If still disagree, discuss with team
4) Consider override suffixes or suppression (if supported)

**Q: What if pre-commit hook is broken?**

A: Don't bypass with --no-verify. Debug:
1. Run `check_staged()` manually to see violations
2. Fix violations
3. Re-run `check_staged()` to confirm
4. Try commit again

**Q: Can I split this into multiple commits?**

A: Yes. Fix violations → stage → commit → repeat.
Each commit should pass `check_staged()`.

---

## Glossary

- **[NEW]:** Violation introduced in current commit
- **[KNOWN]:** Violation that existed before
- **[ERROR]:** Blocks commit
- **[WARN]:** Doesn't block, should fix
- **check_staged():** Pre-commit gate — scans staged files only
- **scan_tree():** Full project scan — all violations
- **Rework loop:** Fix → re-stage → retry (N iterations)
- **Pre-commit hook:** Automatic gate that runs before commit

---

## Next

You've mastered compliance-first workflow:
- ✓ BEFORE: `load-context()`
- ✓ DURING: `coding-discipline`
- ✓ VERIFY: `check-staged()` + `scan-tree()`

Read all workflow files to internalize the discipline.
Apply these habits to every commit.
Make violations the exception, not the norm.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
