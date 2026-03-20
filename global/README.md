---
tags: [global, foundation]
concepts: [global-rules, foundation]
related: [global/startup.md, global/validation.md, global/consistency.md, global/read-before-write.md, global/know-before-change.md, global/persistent-memory.md, global/versions.md, global/secrets.md, global/diagrams.md, global/index-system.md, global/naming-suffix.md, global/app-model.md, global/nesting.md, global/topology.md, global/adapter-layer.md, global/config-driven.md, global/persistent-state.md, global/file-limits.md, global/module-tree.md, global/language.md, gateway/io.md, gateway/lifecycle.md, adapter/viewmodel.md, adapter/event-flow.md, core/design.md, core/state.md, pal/design.md, pal/traits.md]
layer: 6
---
# Global Rules

> Universal rules for all languages and all projects

---

Rules that apply to ALL code — Python, JavaScript, CSS, C++, Rust, Kotlin.
These are non-negotiable habits that make AI collaboration reliable.

## Files

| File | Topic |
|------|-------|
| [startup.md](startup.md) | Mandatory startup checklist |
| [persistent-memory.md](persistent-memory.md) | RAG + FIXES concept |
| [read-before-write.md](read-before-write.md) | Read before write rule |
| [know-before-change.md](know-before-change.md) | 90/10 understanding rule |
| [validation.md](validation.md) | Validation over abstraction |
| [consistency.md](consistency.md) | Cross-language consistency |
| [versions.md](versions.md) | Modern language versions |
| [secrets.md](secrets.md) | Secrets location |
| [diagrams.md](diagrams.md) | Mermaid diagrams only |
| [index-system.md](index-system.md) | Index.yaml system |
| [app-model.md](app-model.md) | Application architecture model |
| [nesting.md](nesting.md) | Max 3 levels, early returns |
| [topology.md](topology.md) | 6-layer hexagonal MVVM folder topology |
| [adapter-layer.md](adapter-layer.md) | Adapter as data exchange hub |
| [config-driven.md](config-driven.md) | No hardcoded values — config via Gateway |
| [persistent-state.md](persistent-state.md) | Per-layer state structs, Gateway disk IO |
| [file-limits.md](file-limits.md) | Max file sizes — check before writing, split when at limit |
| [module-tree.md](module-tree.md) | Module = file, nested = folder — never nested code in one file |
| [language.md](language.md) | English-only code and docs — ASCII source, English-first UI |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
