---
tags: [rust, safety, unsafe, ffi, memory]
concepts: [memory-safety, unsafe-code, ffi, invariant-documentation]
requires: [rust/errors.md, rust/ownership.md]
related: [rust/threading.md, global/topology.md]
keywords: [unsafe, SAFETY, ffi, raw-pointer, transmute, invariant, comment, pal]
layer: 4
---
# Unsafe Code — Safety Documentation

> Every `unsafe` block documents its invariants — no silent unsafety

---

VITAL: Every `unsafe` block and `unsafe fn` MUST have a `// SAFETY:` comment on the preceding line
RULE: `// SAFETY:` comment explains WHY it is safe — what invariant is upheld
RULE: Unsafe code only in `pal/` layer — platform abstraction, FFI, raw hardware access
RULE: Minimize unsafe scope — wrap unsafe in safe abstractions as small as possible
RULE: No `unsafe` in `core/`, `adapter/`, `ui/` — these layers are 100% safe Rust

BANNED: `unsafe` block without `// SAFETY:` comment
BANNED: `unsafe` outside `pal/` layer (except when wrapping C FFI in a safe API)
BANNED: `transmute` without exhaustive justification
BANNED: Raw pointer arithmetic without bounds proof in comment

---

## Format

```rust
// SAFETY: pointer is valid for the lifetime of the struct,
// guaranteed by the Drop impl that releases the handle.
unsafe { CloseHandle(self.handle) }
```

```rust
// SAFETY: alignment checked at construction time,
// size verified by static_assert in build.rs.
unsafe fn read_aligned(ptr: *const u8) -> u32 {
    ptr.cast::<u32>().read()
}
```

## Where Unsafe Belongs

| Layer | Unsafe Allowed | Why |
|-------|---------------|-----|
| `pal/` | Yes | FFI, syscalls, hardware access |
| `gateway/` | Rare | Only if wrapping an unsafe C library |
| `core/` | No | Pure business logic — always safe |
| `adapter/` | No | Data routing — always safe |
| `ui/` | No | Rendering — always safe |
| `shared/` | No | Reusable — must be safe for all consumers |

## Scanner Check

`rust/safety/unsafe-needs-comment` — errors on any `unsafe` block or `unsafe fn`
without a `// SAFETY:` comment within 3 lines above.
