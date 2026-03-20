---
tags: [persona, readme, ai-roles, workflow]
concepts: [persona, ai-developer, role-based-ai]
feeds: [personas/aidevops.md]
keywords: [persona, ai-role, pre-prompt, rules-bundle]
layer: 6
---
# Personas

> Pre-prompt definitions for specialized AI developer roles.
> Each persona = behavioral spec + workflow rules + referenced rule files.

---

Load a persona via: `get_rule("personas/<name>.md")`

## Available Personas

| File | Role | Description |
|------|------|-------------|
| [aidevops.md](aidevops.md) | AIDevOps | OPS/DEV mode switching — phase-driven, test-per-commit, branch discipline |
| [dev.md](dev.md) | Dev | Pure execution — reads TODO, commits tested tasks, asks before advancing phase |
| [ops.md](ops.md) | OPS | Pure collaborative planning — project documentation and iterative paradigm development |

## What a Persona Contains

- **Identity** — who this AI is and how it behaves
- **Modes** — distinct operating modes with clear entry/exit conditions
- **Workflow** — the exact sequence of actions for each mode
- **Git discipline** — branching, commit, and merge rules
- **RULE/VITAL/BANNED** — enforceable constraints
- **Required rules** — which rule files to load alongside this persona

## How to Use

1. Load the persona: `get_rule("personas/aidevops.md")`
2. Load its required rules (listed in frontmatter `requires:`)
3. Paste persona text as system prompt or first context block
4. The AI now operates under the persona's constraints for the session


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
