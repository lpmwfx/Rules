---
tags: [devops, workflow, branching, git]
concepts: [git-workflow, branching]
related: [project-files/workflow.md]
keywords: [main-branch, feature-branch, pr]
layer: 5
---
# UI-First Workflow

> Start with UI, work backwards to endpoint — every step visible and testable

---

## Build Direction

```
Dialog UI → View wiring → ViewModel logic → Transport POST → Server → Storage
←── build direction ←──
```

## Steps (each must be visible/testable)

1. **Dialog UI** — Sketch and implement screen/dialog. Dummy data ok.
2. **View wiring** — Connect UI to views, routes, navigation. No backend dependency.
3. **ViewModel logic** — Add state, validation, local logic. Use stubs.
4. **Transport POST** — Define contract (payload/response), add transport layer.
5. **Server** — Implement endpoint and business logic. Follow contract from UI/VM.
6. **Storage** — Integrate storage/CI/repo artifacts as needed.

## Definition of Done (per step)

RULE: Visible result in UI (screen or flow can be demonstrated)
RULE: A test or manual reproducible checklist per step
RULE: Clear notes about next step and dependencies

## Collaboration Model (AI:DevOps)

- AI codes and implements solutions within agreed scope
- Human is system designer and architect: defines goals, flows, constraints, priorities
- The flow below is followed, where design and architecture drive implementation
