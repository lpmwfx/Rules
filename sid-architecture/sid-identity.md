---
tags: [sid, identity, identifier, generator, unique, opaque, foundation]
concepts: [sid-identity, unique-identifier, atom-model, identity-is-value]
requires: []
feeds: [sid-architecture/code-free-of-mutables.md, sid-architecture/data-driven-runtime.md]
related: [global/naming-suffix.md]
keywords: [SID, 6-char, generator, alphanumeric, case-sensitive, resolve, canonical, fields, registry, unique]
layer: 1
binding: false
status: prototype
---
# SID Identity

> A SID is a 6-character identifier starting with a letter followed by alphanumeric characters. It is the value itself, not a pointer to a value.

---

VITAL: The SID *is* the entity — name, type, value, relations are fields added afterwards
VITAL: All addressable points in the system are SIDs — constants, variables, declarations, widgets, rules
RULE: Format is 6 characters, first char `[a-zA-Z]`, chars 2-6 `[a-zA-Z0-9]`, case-sensitive
RULE: SIDs are purely opaque — no prefix, no type indicator, no scope marker
RULE: Generation via simple generator: random string → uniqueness check → return
RULE: Codebase + data files + datastore together *are* the registry — no separate authoritative source
BANNED: Literal values in code that carry domain meaning — everything is a SID
BANNED: Names as identifiers — names are mutable fields on the SID

## Format

- **52 x 62^5 ≈ 47.6 billion** possible SIDs
- Valid: `aK3qP9`, `Zm4nR8`, `bQ5tLx`, `Hp7wN2`
- Invalid (starts with digit): `0qB5tL`, `7aKq2W`
- First character is a letter so SIDs are valid identifiers in all mainstream languages

## SID Is the Value

Code works with `aK3qP9` **as if it is** the value. The resolver layer is an implementation detail.

Parallels: Atoms in Erlang, Git SHAs, IRIs in RDF, Objects in Smalltalk.

## Declaration vs. Local Use

RULE: Declarations are always SIDs — module-level constants, struct fields, properties, field names, events
RULE: Local bindings in functions may have ordinary names if the value is fully derived from SID lookups
RULE: UI markup follows stricter rule — no local-binding exception in markup
BANNED: Local bindings with literal values not derived from SIDs

```typescript
function validateEmail(eK5mN3: SID) {
  const pattern = resolve(eK5mN3);   // OK — derived from SID
  const maxLen = resolve(fP8qW4);    // OK
  const limit = threshold * 2;       // VIOLATION — "2" is a literal
}
```

## Fields on a SID

Minimum: `canonical` (human name), `type` (domain), `value` (current value).
Typically also: `created_at`, `relations` (explicit connections to other SIDs).

## Three Operations

1. **View** — given a SID, show name, type, value, usage in code and data
2. **Lookup** — given a name or fragment, find matching SIDs
3. **Traverse** — given a SID, show related SIDs via relation fields

## SIDs Are Found, Not Designed

A SID has no meaning in itself. Renaming, reclassifying, moving does not touch the SID. Names are mutable fields; the SID is stable.


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
