---
tags: [multi-binary, cargo-install, workspace, pitfall]
concepts: [multi-binary-install, cargo-install-disambiguation]
requires: [rust/workspace.md]
related: [rust/init.md]
keywords: [cargo-install, multi-binary, workspace, crate-name, INSTALL, ambiguous, desktop, cli]
layer: 4
---
# Multi-Binary Install Pitfall

> `cargo install` in multi-binary workspaces requires an explicit crate name

---

When a workspace contains multiple binaries, `cargo install` requires an explicit crate name:

```bash
# WRONG — ambiguous in a multi-binary workspace
cargo install --git https://github.com/org/my-app

# CORRECT — specify the crate
cargo install --git https://github.com/org/my-app desktop
cargo install --git https://github.com/org/my-app cli
```

RULE: Document the exact `cargo install` command per binary in the project's INSTALL file
BANNED: `cargo install` without a crate name in multi-binary workspaces — it will fail or pick wrong binary

RESULT: Users always get the right binary with a copy-paste command
REASON: Ambiguous `cargo install` either fails silently or installs the wrong binary
