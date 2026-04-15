---
tags: [phase-system, folder-layout, write-domains, parallelism, structural-rules]
concepts: [folder-as-write-domain, parallelism-derivation, layer-mapping]
keywords: [folder, write-domain, sub-folder, architecture-layer, parallel_with, p1, slug, label]
requires: [phase-system/methodology.md]
feeds: [phase-system/references-syntax.md]
related: [phase-system/session-resumption.md]
layer: 2
---
# Folder conventions (v0.3+)

> Parallelism is **structural**, not declarative. The folder a part-file lives in is its write-domain. Parts in different folders can run concurrently; same-folder parts are serial.

No `parallel_with` field — placement is the declaration.

---

## The three rules

### Rule 1 — One folder per major phase, named `<n>-<label>/`

```
proj/PHASE/
  1-fundament/    ← all of p1, p1.5, p1.6, p1.7… live here
  2-ink-tools/    ← all of p2, p2.5… live here
```

RULE: `<label>` after `<n>-` is free — `data`, `setup`, `fundament`, `ink-tools`, `voice-pipeline`. Pick what aids `ls`-scanning.
RULE: Orchestrator's `identity.title` is the canonical title; the folder label is navigation.

BANNED: `<n.x>-<label>/` folders for x > 0 — sub-phases are sub-orchestrators inside the major's folder, not separate folders
BANNED: Ad-hoc folder names like `cool-stuff/` that don't map to an architecture layer

Migration: `1-data/` is fully valid as a label — keep it if you have it. New phases may use semantic labels.

### Rule 2 — `p<n>-` filename prefix

RULE: Every file in `<n>-<label>/` starts with `p<n>-` (orchestrator: `p<n>.json`; parts: `p<n>-<slug>.json`; sub-orchs: `p<n>.5.json`, etc.)

BANNED: `phase.json` — collides across phases, gives the filesystem no parallelism affordance

### Rule 3 — Sub-folders are write-domains

Inside `<n>-<label>/`, organize parts into sub-folders that match write-domains.

RULE: Two parts in different sub-folders can run concurrently — assumed disjoint write-sets
RULE: Two parts in the same sub-folder run serially — assumed write-conflict

```
1-data/
  p1.json                      ← orchestrator (root, cross-domain)
  p1.5.json                    ← sub-orch (root, cross-domain)
  pwa/                         ← write-domain
    p1.5-oauth-fix.json
  server/                      ← write-domain
    p1.5-dal-extension.json
  research/                    ← write-domain
    p1.5-mistral.json
    p1.6-ink-as-surreal-json.json   ← serial with p1.5-mistral.json (same folder)
```

---

## Mapping folders to architecture layers

VITAL: Sub-folder names mirror layers (or sub-layers) from your project's `proj/data/current/architecture.json` — couples phase-system to anti-scope-creep-rigging through shared vocabulary

Example: AiGame's `architecture.json` has layers `frontend`, `backend`, `wire`, `external`, with sub-layers like `frontend.editor`, `backend.dal`, `external.mistral`:

| Architecture layer/sub-layer | Phase sub-folder |
|---|---|
| `frontend.editor`, `frontend.preview` | `pwa/` (or `pwa/editor/`, `pwa/preview/`) |
| `backend.dal`, `backend.services` | `server/` |
| `backend.database` | `data-layer/` |
| `wire.mcp` | `wire/` |
| `external.mistral` | `external/` |
| (cross-cutting research) | `research/` |
| (deploy, infra, systemd, secrets) | `ops/` |
| (architecture/spec work) | `design/` |

RULE: `research/`, `ops/`, `design/` are commonly added as cross-cutting work-types even though they don't map to a single architecture layer

### Validation check

```bash
# Phase folders: must start with <n>-<label>
for d in proj/PHASE/*/; do
  name=$(basename "$d")
  [[ "$name" =~ ^[0-9]+(\.[0-9]+)?-[a-z0-9-]+$ ]] || echo "WARN: phase folder $d doesn't match <n>-<label>"
done

# Sub-folders inside phase folders: write-domain, should match arch layer
for d in proj/PHASE/*/*/; do
  folder=$(basename "$d")
  if ! grep -q "\"$folder\"" proj/data/current/architecture.json && \
     [[ "$folder" != "research" && "$folder" != "ops" && "$folder" != "design" ]]; then
    echo "WARN: write-domain folder $d doesn't match an architecture layer"
  fi
done
```

---

## When to split a folder

If two parts in the same folder genuinely don't conflict (different files, different services), the folder is too coarse. Split it:

```
1-data/pwa/    →   1-data/pwa/auth/
                   1-data/pwa/editor/
```

BANNED: Adding a `parallel_with` exception instead of refactoring the folder structure — the structural property (folder = write-domain) is what makes the system reliable

---

## Cross-folder logical dependencies

Folder placement handles **write-conflicts**. For **logical sequencing** (this part needs that part's result, even though they're in different folders), use `concurrency.runs_after`:

```json
"concurrency": {
  "runs_after": ["mistral"],
  "blocks": [],
  "locked_by_session": null,
  "locked_at": null
}
```

For **awareness without sequencing** (this part reads from that part but can run in parallel), use `references[]` — see [references-syntax.md](references-syntax.md).

---

## Anti-patterns

BANNED: Folder named after a part-slug (`1-data/p1.5-oauth-fix/p1.5-oauth-fix.json`) — folder names a write-domain, not repeats the slug
BANNED: Folder that doesn't map to a layer in `architecture.json` — either add the layer (with `$hint`) or rename the folder
BANNED: Sub-orchestrator inside a sub-folder (`1-data/research/p1.5.json`) — sub-orchestrators are cross-folder coordinators, they live in the root of `<n>-<label>/`
BANNED: Same-folder parts claimed as parallel because "they won't really conflict" — if you can't refactor into sub-folders, accept they're serial

---

## Migrating from v0.2

1. Move all `<n.x>-data/<file>` to `<n>-<label>/<folder>/<file>` where `<folder>` matches a write-domain
2. Delete empty `<n.x>-data/` folders
3. Remove `parallel_with` from all part-files and orchestrator entries
4. Add `folder` field to part-files' `part_meta` and orchestrator's `parts.items[]`
5. Update path references in `parts.items[].file` to include folder prefix
6. Add `references[]` blocks where parts read from outside their folder


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
