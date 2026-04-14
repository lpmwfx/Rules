---
tags: [sid, working-in-data, ai-native, workspace, css-analogy]
concepts: [data-workspace, ai-native-area, css-analogy, 50-50-split]
requires: [sid-architecture/code-free-of-mutables.md, sid-architecture/data-driven-runtime.md]
related: [sid-architecture/topology-as-data.md, sid-architecture/meta-driven-ui.md]
keywords: [workspace, data-layer, AI, native, CSS, 50-percent, conversation-based, structure, topology]
layer: 1
binding: false
status: prototype
---
# Working in Data

> About 50% of development work in a mature SID-based system happens in data — not in code.

---

VITAL: The data layer is a self-contained workspace — like CSS is for styling, but for *everything* that can be data
VITAL: The more structure that is explicit in data, the easier it is for AI to reason about the system
RULE: Value changes never touch code files; structure changes never touch data files
RULE: Principle 02 ensures code is clean enough; Principle 03 ensures changes reach the running system

## The CSS Analogy

When a web developer needs to change colors, sizes, spacing — they open the CSS file. They don't touch HTML, don't touch JavaScript. CSS is a well-defined workspace.

The data layer in a SID-based system is the same — but for *everything* that can be data. Not just styling, but labels, rules, widget compositions, event routing, thresholds, structures.

## AI's Native Area

Humans have cognitive load limitations. Keeping the system's full topology in your head is hard.

AI does not have the same limitation. The more structure that is **explicit in data**, the easier it is for AI. A flat SID table without relations is *harder* for AI. A rich table with explicit topology relations is **easier**.

The data area is the form of representation AI works best with. It is what makes conversation-based development possible as a real practice.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
