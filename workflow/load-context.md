---
tags: [workflow, before, context, preparation, mcp-tools]
concepts: [pre-write, context-loading, file-analysis]
keywords: [context, file-limits, topology, language, layer, before-edit, preparation]
layer: 2
requires: [global/topology.md, global/file-limits.md, workflow/always-compliant.md]
feeds: [workflow/coding-discipline.md]
related: [global/file-limits.md, global/topology.md, workflow/always-compliant.md]
---

# BEFORE: Load Context Before Editing

## Goal

Know which rules apply to this file BEFORE you edit it.
Prevents violations by design, not by accident.

---

## Step 1: Identify File Context (5 seconds)

### New MCP Tool: `get_file_context(path)`

Call this tool with the file path you're about to edit:

```
get_file_context("src/core/engine.rs")
```

Returns structured output:

```
## File context: src/core/engine.rs

Language: rust
Topology layer: core
  Allowed imports: pal, shared (NOT adapter, gateway, ui, app)
  Public types must carry: _core suffix

Key rules:
- get_rule("global/file-limits.md") — max 300 lines per file
- get_rule("global/topology.md") — import DAG enforcement
- get_rule("rust/errors.md") — no unwrap, use ?
- get_rule("rust/naming.md") — _core suffix, bool prefixes
- get_rule("rust/types.md") — no &Vec/&String

Compliance checklist:
- [ ] File under 300 lines after changes?
- [ ] Only imports from pal/ or shared/?
- [ ] All pub types end in _core?
- [ ] No .unwrap() calls?
```

**Why this matters:** Before you write a single line, you know:
- What language rules apply
- What layer constraints apply
- What size limit you must respect
- Which key rules to reference

**Time cost:** 5 seconds per file (one-time lookup).

---

## Step 2: Alternative — Load Combo Rules

If you prefer a quick overview, use the existing MCP tool:

```
get_context([language], quick_ref: true)
```

Returns 3 files:
- `global/quick-ref.md` — startup + topology + file-limits
- `{language}/quick-ref.md` — language-specific combo (Rust, Python, JS, etc.)
- Optional: `{layer}/quick-ref.md` if category-specific rules exist

**Time cost:** 10 seconds to skim.

---

## Step 3: Check File Size BEFORE Editing

### Rule: Know the limit, don't exceed it

File size limits by language (from `global/file-limits.md`):

| Language | Limit | Action |
|----------|-------|--------|
| Rust | 300 lines | If ≥ 240 lines (80%), split BEFORE adding code |
| Python | 250 lines | If ≥ 200 lines (80%), split BEFORE adding code |
| JavaScript/TypeScript | 250 lines | If ≥ 200 lines (80%), split BEFORE adding code |
| Slint | 400 lines | If ≥ 320 lines (80%), split BEFORE adding code |
| C++ | 300 lines | If ≥ 240 lines (80%), split BEFORE adding code |
| Kotlin | 250 lines | If ≥ 200 lines (80%), split BEFORE adding code |

**VITAL:** Don't wait for the scanner to tell you a file is too large.
Count lines BEFORE you edit. If approaching 80% of limit → split the file first.

### How to count

```bash
wc -l src/core/engine.rs   # Linux/Mac/WSL
Get-Content src/core/engine.rs | Measure-Object -Line  # PowerShell
```

If the file is at 80% of limit:
- Create new module in same layer
- Move appropriate code to new module
- Update imports
- THEN make your changes

**RULE:** File size violations are preventable. Don't write code into a full file.

---

## Step 4: Topology Check — Layer Import Rules

### Know what this layer can import

From `global/topology.md`, import rules per layer:

```
app     → all (entry point)
adapter → core, gateway, pal, ui, shared
ui      → adapter, shared
core    → pal, shared
gateway → pal, shared
pal     → shared only
shared  → nothing (zero internal deps)
```

**Question:** What layer am I editing?
**Answer:** Check file path:
- `src/core/...` or `crates/core/...` → core layer
- `src/adapter/...` → adapter layer
- `src/gateway/...` → gateway layer
- `src/pal/...` → pal layer
- `src/shared/...` → shared layer

**Question:** What imports are allowed?
**Answer:** Find your layer in the table above.

**Violation:** Importing from a disallowed layer will be caught by scanner.
**Prevention:** Know the rules BEFORE you write the import.

### Type Suffix Convention

**Rule:** Public types must carry layer suffix (from `global/topology.md`).

If editing `src/core/engine.rs`:
- Public type names END with `_core`: `struct Engine_core`
- Private types: no suffix required
- Override suffixes allowed: `_cfg`, `_sta`, `_test`

**Common suffixes:**
- `_core` — core layer
- `_adp` — adapter layer
- `_gtw` — gateway layer
- `_pal` — platform abstraction layer
- `_x` — shared layer
- `_ui` — ui layer

---

## Step 5: Load Full Rules (if needed)

For deep understanding, call:

```
get_rule("global/file-limits.md")
get_rule("global/topology.md")
get_rule("rust/naming.md")        # if Rust file
get_rule("rust/errors.md")        # if Rust file
get_rule("rust/types.md")         # if Rust file
```

Or use combo:

```
get_context(["rust"])             # all Rust rules
```

**Time cost:** 2-5 minutes to read thoroughly (optional).

---

## BEFORE-Phase Checklist

- [ ] Identified file language? (Rust, Python, JS, etc.)
- [ ] Identified layer? (core, adapter, shared, etc.)
- [ ] Checked file size? (At 80% limit?)
- [ ] Know allowed imports? (No cross-layer cycles)
- [ ] Know type suffix? (_core, _adp, _x, etc.)
- [ ] Read key rule files? (optional but recommended)
- [ ] Ready to code? (Yes → proceed to DURING phase)

---

## FAQ

**Q: Do I need to call get_file_context() for every file?**

A: Yes. 5 seconds per file is worth it. Prevents violations by design.
For similar files in same layer, context is the same — cache mentally.

**Q: What if the file is new?**

A: Call get_file_context() anyway. Returns "language detected, layer not found" + global rules.

**Q: What if file spans multiple layers?**

A: Move code to appropriate layers. One file = one layer. If you're splitting across layers,
the file is too small or poorly placed. Investigate.

**Q: Can I skip this phase?**

A: No. Violations are preventable. The 5-second investment prevents 5-minute rework loops.

---

## Next: DURING Phase

Read `workflow/coding-discipline.md` to maintain compliance while coding.
