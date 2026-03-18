---
tags: [validation, boundary, newtype, tryfrom]
concepts: [boundary-validation, parse-dont-validate, typed-construction]
requires: [rust/types.md, rust/errors.md, global/validation.md]
feeds: [rust/safety.md]
keywords: [validate, boundary, TryFrom, newtype, parse, gateway, adapter, builder, ValidationError, Port, Email, NonEmpty]
layer: 4
---
# Runtime Validation

> Validate at the boundary, trust typed values inside — parse, don't validate

---

RULE: Validate at Gateway/Adapter boundary — Core trusts typed inputs
RULE: Newtype + `TryFrom` for validated types (`Port`, `Email`, `NonEmpty<T>`)
RULE: Builder pattern with `build() -> Result<T, ValidationError>` for complex construction
RULE: `parse, don't validate` — turn unstructured data into typed values at the boundary

```rust
// Newtype with TryFrom — validated at construction, trusted everywhere else
pub struct Port(u16);

impl TryFrom<u16> for Port {
    type Error = ValidationError_x;

    fn try_from(value: u16) -> Result<Self, Self::Error> {
        if value == 0 {
            return Err(ValidationError_x::InvalidPort(value));
        }
        Ok(Port(value))
    }
}

// Builder for complex construction
pub struct ServerConfigBuilder { port: Option<Port>, host: Option<String> }

impl ServerConfigBuilder {
    pub fn port(mut self, p: u16) -> Result<Self, ValidationError_x> {
        self.port = Some(Port::try_from(p)?);
        Ok(self)
    }
    pub fn build(self) -> Result<ServerConfig, ValidationError_x> {
        Ok(ServerConfig {
            port: self.port.ok_or(ValidationError_x::MissingField("port"))?,
            host: self.host.ok_or(ValidationError_x::MissingField("host"))?,
        })
    }
}
```

BANNED: Manual validation scattered through business logic
BANNED: Stringly-typed APIs in domain code — use newtypes
BANNED: Constructing domain types without validation (`Port(0)` directly)
BANNED: Re-validating inside Core what was already validated at the boundary
