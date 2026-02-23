# Goal Chain

> PROJECT Goal is the foundation — everything traces back to it

---

## Chain

```
PROJECT ## Goal      The vision — what we want to achieve (free text)
PHASES milestone:    Each phase achieves a piece of the Goal
PHASES delivers:     What the phase builds
TODO tasks:          Current work within the active phase
TODO pass:           Tests or product criteria — proves the milestone is reached
```

## Rules

RULE: Every milestone must trace to a sentence in PROJECT ## Goal
RULE: A phase without a milestone is just work — not progress
RULE: Goal text changes rarely. Milestones are set when phases are planned
RULE: `pass:` lives only in TODO — it is binary, you pass or you don't
RULE: When all `pass:` criteria pass → milestone done → phase done → DONE

## Example

```
PROJECT ## Goal says:
  "PraeO makes institution files visible and editable in a GUI"

PHASES Phase 2 milestone:
  "Institution files visible and editable in Project tab"

PHASES Phase 2 delivers:
  parser, viewmodel, blueprint UI, exchange layer

TODO pass:
  - PROJECT file parsed and phases shown in UI
  - Status change in UI persists back to file
  - Round-trip parse/render without data loss

> all pass > milestone done > phase done > recorded in DONE
```

## DONES Rule

DONES is the absolute dividing line in TODO and ISSUES.

- **Above DONES**: active, forward-looking
- **Below DONES**: completed, evaluated or classified as failure

## Status Transitions

Allowed:
```
TODO > DOING > DONE
DONE > FAIL      (requires: what failed, what was learned)
DONE > REFACTOR  (requires: what to improve, what to reuse)
```

Forbidden:
```
DOING > FAIL
TODO  > REFACTOR
DOING > ISSUES
```

RULE: Everything must pass through DONE first

## FAIL / REFACTOR Flow

1. An ISSUE is created
2. Issue placed right after DONES in FIFO queue
3. Must be handled in order — no skipping ahead
