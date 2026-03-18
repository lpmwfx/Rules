---
tags: [proc-macro, exemption, tool-router, async-trait, fn-count]
concepts: [proc-macro-exemption, bundling-macros, thin-delegation]
requires: [uiux/mother-child.md, global/file-limits.md]
related: [rust/modules.md, rust/workspace.md]
keywords: [tool_router, async_trait, tonic, rmcp, impl-block, fn-count, delegation, scanner-exempt, proc-macro]
layer: 3
---
# Proc-Macro Exemption (Rust)

> When a macro requires all fns in one impl block, the fn-count limit is waived — delegation required

---

Some proc macros require all handler functions in a single `impl` block — this is a compiler constraint,
not a design choice. The fn-count limit is waived for these cases.

RULE: When a proc macro requires all functions in one impl block, the fn-count limit does not apply —
      PROVIDED each fn body is a thin delegation (max ~5 lines) forwarding to a child module.
RULE: The impl block itself stays in the mother file — only the logic moves to children.
REASON: The macro is the constraint. Splitting the impl would break compilation. The developer
        has no choice — enforcing the limit here would be counterproductive.

Known bundling macros (scanner-exempt):
- `#[tool_router]` — rmcp MCP server tool dispatch (all tool handlers in one impl)
- `#[async_trait]` — trait impl with async methods (async-trait crate requirement)
- `#[tonic::async_trait]` — gRPC service impl (tonic framework requirement)

```rust
// lib.rs — MOTHER: tool router stays here (macro requires it), logic goes to children
#[tool_router]
impl MyMcpServer {
    #[tool(description = "Get selection")]
    async fn get_selection(&self, ...) -> ... {
        selection_ui::get(&self.state).await  // thin delegation: 1-2 lines
    }

    #[tool(description = "Insert block")]
    async fn insert_block(&self, ...) -> ... {
        build_block_ui::insert(&self.state, params).await  // thin delegation
    }
}

// src/ui/selection_ui.rs — CHILD: all logic here
pub async fn get(state: &AppState) -> Result<...> {
    // real implementation
}
```

BANNED: Tool handler fn bodies with business logic — delegate to a child module
BANNED: Tool handler fn bodies longer than ~5 lines — that is logic leaking into the router

RESULT: Macro-constrained impl blocks stay compilable while logic lives in focused child modules
REASON: Splitting the impl would break the macro — the exemption is mechanical, not a loophole
