---
tags: [topology, cli, bun, node, layers, command-line]
concepts: [cli-topology, layer-mapping-cli]
requires: [global/topology.md, global/topology-profiles.md]
related: [js/project-structure.md, global/tools-and-scripts.md, core/design.md, gateway/io.md]
keywords: [cli, command-line, args, stdio, bun, node, typescript]
layer: 2
---
# CLI Topology

> 6-layer mapping for command-line tools in Bun/Node TypeScript

---

| Layer | Tag | CLI mapping |
|---|---|---|
| ui | — | Absent — CLI has no visual interface |
| adapter | `_adp` | `src/adapter/` — args parser, stdio formatter, command router |
| core | `_core` | `src/core/` — business logic, transforms, domain rules |
| gateway | `_gtw` | `src/gateway/` — file IO, network, database, external APIs |
| pal | `_pal` | `src/pal/` — OS abstractions (paths, env, signals) |
| shared | `_x` | `src/shared/` — error types, result types, cross-layer enums |

## Adapter in CLI

Adapter is not a viewmodel — it is the stdio interface:

- Parses command-line arguments
- Routes to the correct core function
- Formats core results for stdout/stderr
- Handles exit codes

```typescript
#!/usr/bin/env bun
// src/adapter/cli.ts
import { parseArgs } from "util";
import { runScan } from "../core/scanner.ts";
import { loadConfig } from "../gateway/config.ts";

const { values } = parseArgs({ options: { path: { type: "string" } } });
const config = await loadConfig();
const result = await runScan(values.path!, config);
console.log(formatResult(result));
process.exit(result.errors > 0 ? 1 : 0);
```

RULE: Adapter owns args parsing and output formatting — core never touches stdio
RULE: Core is pure — receives data, returns results, no process.exit or console.log
