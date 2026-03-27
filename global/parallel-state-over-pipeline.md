---
tags: [architecture, pipeline, parallel, state-machine, concurrency, database, performance]
concepts: [parallel-state-machine, shift-register, state-per-operation, crash-recovery]
requires: [global/persistent-state.md, global/topology.md]
feeds: []
related: [global/persistent-state.md, global/app-model.md]
keywords: [parallel, pipeline, state machine, concurrent, database, resumable, speedup, plc, sfc]
layer: 1
---
# Parallel State Over Pipeline

> Uafhængige operationer køres parallelt via state machines — aldrig sekventielt

---

RULE: Kør IKKE sekventiel pipeline når operationerne er uafhængige af hinanden
RULE: Brug skifteregister med parallelle state machines — én per operation
RULE: Hver operations state persisteres i database — ikke i hukommelsen
RULE: Hver operation kører simultant med de øvrige
RULE: Crash-recovery sker via database-state — operationen genoptages, ikke genstarter
RULE: State transitions er intern puls — ingen ekstern watchdog nødvendig
BANNED: Sekventiel pipeline hvor operationer ikke har data-afhængighed af hinanden
BANNED: State i hukommelse for operationer der skal overleve crash

## Hvornår gælder dette

```
Sekventiel pipeline er kun lovlig når:
  - Step B kræver output fra Step A (ægte data-afhængighed)
  - En delt ressource forhindrer parallelitet (dokumenteret undtagelse)

Ellers: parallel state machine
```

RULE: Hvis operationerne kan defineres uafhængigt af hinanden → de KAN køres parallelt → de SKAL køres parallelt

## Struktur

Hver operation har:
- **Egen tilstand** i databasen (`operation_id`, `status`, `payload`, `updated_at`)
- **Simultant forløb** med alle øvrige operationer
- **Genoptagelighed** — crash efterlader state i DB, næste run fortsætter
- **Intern puls** via state transitions (`pending → processing → done`)

```
DB-tabel: operations
┌─────────────┬────────────┬────────────┬──────────────────┐
│ operation_id│ status     │ payload    │ updated_at       │
├─────────────┼────────────┼────────────┼──────────────────┤
│ lang:da     │ done       │ {...}      │ 2026-03-27 ...   │
│ lang:de     │ processing │ {...}      │ 2026-03-27 ...   │
│ lang:en     │ pending    │ {...}      │ 2026-03-27 ...   │
│ ...         │ ...        │ ...        │ ...              │
└─────────────┴────────────┴────────────┴──────────────────┘
```

## Bevis

**Artikel-pipeline: 29 sprog × rå markdown → HTML**

| Tilgang | Tid | Model |
|---|---|---|
| Sekventiel pipeline | ~2 minutter | Mistral small |
| Parallel state machine | ~5 sekunder | Mistral small |

**24x speedup — ren arkitekturgevinst, ingen modelskift**

Samme model, samme API, samme output. Forskellen er udelukkende arkitektur.

## Analogi: PLC SFC

PLC Structured Function Charts kører aldrig sekventielt hvad der kan køre parallelt.
Uafhængige operationer = uafhængige steps i SFC.

```
Sekventiel (forkert):    Parallel (korrekt):
[op:da] → [op:de] →     [op:da]
[op:en] → ...            [op:de]  ← alle simultant
                         [op:en]
                         [...]
```

REASON: Sekventiel pipeline af uafhængige operationer er en arkitekturfejl, ikke en ressourcebegrænsning


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
