---
tags: [sid, meta-driven-ui, widget, composition, parser, motor, database]
concepts: [meta-driven-ui, widget-record, screen-composition, parser-boundary, double-entity]
requires: [sid-architecture/data-driven-runtime.md, sid-architecture/topology-as-data.md]
related: [sid-architecture/environments.md, sid-architecture/working-in-data.md]
keywords: [widget, record, composition, parser, motor, SID, screen, PWA, Svelte, database, disk, parameter-contract, granularity]
layer: 2
binding: false
status: prototype
---
# Meta-Driven UI

> The UI is not code that renders data. The UI *is* data interpreted by an engine.

---

VITAL: The engine is precompiled code; the UI is records in database; the parser is the link
VITAL: The widget catalog (all widget records) is the system's UI API, fully readable as data
RULE: The same engine can drive arbitrarily many UIs by pointing at different databases
RULE: A widget exists as a double entity: physical file on disk + record in database
RULE: Screen compositions contain only SIDs — no hardcoded strings or values
RULE: Granularity decisions are made at the data level without architecture revision

## Division of Labor

| Artifact | Lives where | Why |
|---|---|---|
| HTML skeleton | Server disk | Code. Rarely changed. Git-versioned. |
| JS engine + parser | Server disk | Code. Deliberate rebuilds. |
| Widget files | Server disk | Code. Editor tooling, precompilation. |
| Widget records | Database | Descriptions. Queryable. Changed more often. |
| Screen compositions | Database | Primary workspace for AI. |
| Content (labels, values) | Database | Changed constantly. |
| Runtime state | RAM | Transient. Neither code nor data. |

## Widget as Double Entity

**On disk:** physical implementation (HTML+JS, precompiled Svelte). Immutable after build.

**In database:** record with SID, contract (parameters, types, events, defaults), points to physical file.

```json
{
  "aK3qP9": {
    "canonical": "widget.text-label",
    "type": "widget_record",
    "implementation": "text-label.svelte",
    "params": {
      "text": { "type": "sid_or_string", "required": true },
      "size": { "type": "sid", "references": "typography.size", "default": "bM4nR7" }
    }
  }
}
```

## Screen Composition

```json
{
  "cP8wQ2": {
    "canonical": "screen.dashboard",
    "type": "screen_composition",
    "widgets": [
      { "widget": "aK3qP9", "params": { "text": "dR5tL1" } },
      { "widget": "eS8uP3", "params": { "source": "fT4vM2" } }
    ]
  }
}
```

All SIDs all the way. "Add a chart to the dashboard" = add a new item in the widgets array.

## PWA Flow

1. PWA starts — loads HTML skeleton + JS engine from disk
2. Requests screen composition from database
3. Parser reads composition, looks up widget records
4. Fetches widget files from disk, instantiates with SID parameters
5. Widget renders — ordinary component, unaware it is data-driven

## Why This Fits AI-Assisted Development

- **Topology-as-data** — screen compositions are rich structure AI reads best
- **SIDs as stable handles** — AI references UI elements without navigating code
- **Widget records as contract** — AI understands the entire UI system by reading the database

"Add a new screen with a table and two buttons" becomes database inserts, not code.

> Reference: `project-system`/TOP as running example


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
