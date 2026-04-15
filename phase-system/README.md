---
tags: [phase-system, methodology, research-first, ai-signoff, parallelism, foundation]
concepts: [phase-management, one-product-per-phase, write-domains, split-mode]
keywords: [phase, orchestrator, part, product, usage-tests, signoff, folder-as-write-domain, session-resumption]
related: [project-files/phases-file.md, sid-architecture/README.md, workflow/dev-cycle.md]
layer: 6
---
# Phase System — research-first phases with AI-signoff

> JSON-schema methodology for breaking projects into phases that actually work before they close. Built to compose with [anti-scope-creep-rigging](https://git.lpmintra.com/ai/anti-scope-creep-rigging).

A phase is a unit of work that produces **one product** — a coherent usable thing, not a checklist. The phase opens with research, persists decisions, plans concretely, runs AI-executed usage-tests throughout, and never closes without explicit AI signoff.

---

## Structure

| File | Content |
|---|---|
| `methodology.md` | Core principles, 7-step workflow, lifecycle, anti-patterns |
| `folder-conventions.md` | `<n>-<label>/` layout, sub-folders as write-domains, parallelism rules |
| `references-syntax.md` | Read-graph paths, anchors, excerpts (v0.4) |
| `session-resumption.md` | `locked_session_log` + `claude --resume` recovery (v0.4) |
| `integration.md` | Composition with anti-scope-creep-rigging |
| `orchestrator-template.json` | `standard-phase-orchestrator.json` v4 template |
| `part-template.json` | `standard-phase-part.json` v4 template |

---

## Core principles

VITAL: One product per phase — a coherent usable experience, not a checklist of components
VITAL: AI must be able to demonstrate the product (`product.user_can[]` is concrete and AI-executable)
VITAL: Research before plan — no plan step written on guessed behavior
VITAL: No phase closes without AI signoff — `ai_verified=true` after a concrete "I did X, Y, Z and it works" statement
VITAL: User approval still required after AI signoff (separate step, user-only)

RULE: Decisions persist with candidates, answer, rationale, and `lands_in` (where the answer lives)
RULE: Every plan step has a testable `pass` criterion — outcome, not implementation
RULE: Failed verification blocks done — either fix, or move to a new phase with reasoning in `issues_logged`

---

## Quick start

```bash
# 1. Copy templates into your project
cp orchestrator-template.json your-project/proj/PHASE/1-<label>/p1.json
cp part-template.json your-project/proj/PHASE/1-<label>/<domain>/p1-<slug>.json   # split-mode only

# 2. Fill in order (see methodology.md)
identity → context → milestone → product
        → research (parallel sub-agents per topic)
        → decisions (close all open)
        → plan (steps with concrete pass criteria)
        → usage_tests (what AI must be able to do)
        → anti_creep_check + mcp_rules + data_layer_changes

# 3. status: planned → researching → ready → active → done
```

---

## Folder layout

```
proj/PHASE/
  1-fundament/                ← <n>-<label>/ per major phase
    p1.json                   ← orchestrator
    p1.5.json                 ← sub-orchestrator (split-mode index)
    pwa/                      ← sub-folder = write-domain (matches architecture layer)
      p1.5-oauth-fix.json
    research/
      p1.5-mistral.json
  2-ink-tools/
    p2.json
    ...
```

BANNED: Nested `<n.x>-<label>/` folders for x > 0 — sub-phases share the major's folder
BANNED: Generic `phase.json` filenames — collides across phases, always `p<n>-<slug>.json`
BANNED: `parts.items[].parallel_with` — v0.3 derives parallelism from folder placement

RULE: Every file in `<n>-<label>/` starts with `p<n>-` prefix
RULE: Sub-folder names match a layer (or sub-layer) in `proj/data/current/architecture.json`
RULE: Different sub-folders run parallel; same sub-folder is serial by default

---

## Status

v0.4 — adds `locked_session_log` for `claude --resume` recovery, reference excerpts, and auto-firing `close_protocol`. Source: `git.lpmintra.com/modules/phase-system`. Extracted from AiGame (`AIGame/authoring-system`).


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
