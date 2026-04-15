---
tags: [phase-system, folder-layout, write-domains, parallelism, structural-rules]
concepts: [folder-as-write-domain, parallelism-derivation, layer-mapping]
keywords: [folder, write-domain, sub-folder, architecture-layer, parallel_with, p1, slug, label]
requires: [phase-system/methodology.md]
feeds: [phase-system/references-syntax.md]
related: [phase-system/session-resumption.md]
layer: 2
---

# Folder conventions (v0.3)

Phase-system v0.3 makes parallelism **structural** instead of **declarative**: the folder a part-file lives in is its write-domain. Parts in different folders can run concurrently; parts in the same folder are serial by default. No `parallel_with` field needed — placement is the declaration.

This document explains the folder rules, how to map folders to your project's architecture, and the anti-patterns to avoid.

## The three rules

### Rule 1 — One folder per major phase, named `<n>-<label>/`

```
proj/PHASE/
  1-fundament/   ← all of p1, p1.5, p1.6, p1.7… live here
  2-ink-tools/   ← all of p2, p2.5… live here
```

The `<label>` after `<n>-` is free — `data`, `setup`, `fundament`, `ink-tools`, `voice-pipeline`. Pick what aids `ls`-scanning. The orchestrator's `identity.title` is the canonical title; the label is navigation.

`<n.x>-<label>/` for x > 0 is **forbidden**. Sub-phases are sub-orchestrators inside their major's folder, not separate folders.

Migration from earlier conventions: `1-data/` is fully valid as a label — keep it if you have it. New phases can use semantic labels for clarity.

### Rule 2 — `p<n>-` filename prefix

Every file in `<n>-data/` starts with `p<n>-` (orchestrator: just `p<n>.json`; parts: `p<n>-<slug>.json`; sub-orchs: `p<n>.5.json`, etc.).

`phase.json` is **forbidden** — it collides across phases and gives the file system no parallelism affordance.

### Rule 3 — Sub-folders are write-domains

Inside `<n>-data/`, organize parts into sub-folders that match write-domains. Two parts in different sub-folders are assumed to have disjoint write-sets and can run concurrently. Two parts in the same sub-folder are assumed to conflict and run sequentially.

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

## Mapping folders to architecture layers

The folder names should mirror layers (or sub-layers) in your project's `proj/data/current/architecture.json` from anti-scope-creep-rigging. This couples the two methodologies through shared vocabulary.

Example: AiGame's `architecture.json` has layers `frontend`, `backend`, `wire`, `external`. Sub-layers like `frontend.editor`, `backend.dal`, `external.mistral`. Phase folders pick from this list:

| Architecture layer/sub-layer | Phase sub-folder |
|---|---|
| `frontend.editor`, `frontend.preview` | `pwa/` (or `pwa/editor/`, `pwa/preview/` if finer split needed) |
| `backend.dal`, `backend.services` | `server/` |
| `backend.database` | `data-layer/` |
| `wire.mcp` | `wire/` |
| `external.mistral` | `external/` |
| (cross-cutting research, no single layer) | `research/` |
| (deploy, infra, systemd, secrets) | `ops/` |
| (architecture/spec work) | `design/` |

`research/`, `ops/`, and `design/` are commonly added even though they don't always match a single layer — they capture work-types that cut across layers.

### Validation check

A simple grep verifies folders map to layers:

```bash
# Phase folders: must start with <n>-
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

## When to split a folder

If two parts in the same folder genuinely don't conflict (different files, different services), the folder is too coarse. Split it:

```
1-data/pwa/                     →  1-data/pwa/auth/
                                   1-data/pwa/editor/
```

Don't add a `parallel_with` exception — refactor the folder structure instead. The structural property (folder = write-domain) is what makes the system reliable.

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

For **awareness without sequencing** (this part reads from that part but can run in parallel), use `references[]` (see [references-syntax.md](references-syntax.md)).

## Anti-patterns

### Folder named after a part-slug

```
1-data/p1.5-oauth-fix/         ❌
  p1.5-oauth-fix.json
```

The folder should name the **write-domain** (`pwa/`), not repeat the slug. One folder, many parts that write to the same domain.

### Folder that doesn't map to a layer

```
1-data/cool-stuff/             ❌
  p1.5-experiments.json
```

If `cool-stuff` isn't in `architecture.json`, either add it as a layer (and explain why in arch's $hint) or rename the folder. Ad-hoc folders defeat the structural-mapping property.

### Sub-orchestrator inside a folder

```
1-data/research/p1.5.json      ❌
```

Sub-orchestrators are **cross-folder** (they coordinate parts across multiple write-domains). They live in the root of `<n>-data/`, not inside a folder.

### Same-folder parts pretending to be parallel

```
1-data/pwa/
  p1.5-oauth-fix.json          ─┐
  p1.5-tiptap-init.json        ─┴ both touch src/pwa/src/, claimed parallel
```

If you can't refactor them into sub-folders, they're not actually parallel — accept that they're serial. The system's safety comes from honoring the structural rule.

## Migrating existing phases to v0.3

If you have v0.2 phases with `<n.x>-data/` folders or `parallel_with` declarations:

1. Move all `<n.x>-data/<file>` to `<n>-data/<folder>/<file>` where `<folder>` matches a write-domain
2. Delete empty `<n.x>-data/` folders
3. Remove `parallel_with` from all part-files and orchestrator entries
4. Add `folder` field to part-files' `part_meta` and orchestrator's `parts.items[]`
5. Update path references in `parts.items[].file` to include folder prefix
6. Add `references[]` blocks where parts read from outside their folder
