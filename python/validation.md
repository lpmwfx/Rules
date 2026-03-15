---
tags: [python, validation, pydantic, beartype, runtime]
concepts: [runtime-checking, boundaries, validation, structured-types]
requires: [global/validation.md]
related: [js/validation.md, python/types.md]
keywords: [pydantic, beartype, BaseModel, model_validate, parse_obj, schema]
layer: 4
---
# Runtime Validation

> Pydantic/beartype at system boundaries — structured types everywhere

---

RULE: Validate at system boundaries (API responses, file I/O, user input, config)
RULE: Use `pydantic.BaseModel` for structured data from external sources
RULE: Use `beartype` for runtime enforcement of type hints on function parameters
RULE: Never pass raw `dict` across layer boundaries — wrap in a typed model

## Pydantic — Boundary Validation

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

# Parse + validate in one call — raises ValidationError on bad data
user = UserResponse.model_validate(raw_json_dict)
```

PATTERN: `Model.model_validate(data)` — raises `ValidationError` on invalid input
PATTERN: `Model.model_validate_json(text)` — parse JSON string directly
BANNED: `json.loads(response.text)` without model_validate — raw dict crosses boundary

## Exemption: tools/ directory

`json.loads()` and `response.json()` without pydantic are allowed in `tools/` files.
Build scripts and CLI tools parse data directly — they are not system boundaries.

## beartype — Function Parameter Enforcement

```python
from beartype import beartype

@beartype
def process_user(user: UserResponse, limit: int) -> list[str]:
    ...  # beartype enforces types at call site, not just statically
```

RULE: `@beartype` on all public functions that accept or return typed models
RULE: Use beartype in addition to mypy — beartype catches runtime type errors

## Automatic Structure

RULE: `@dataclass` or `BaseModel` for ALL multi-field data — never plain dicts
RULE: Field names and types defined once in the model — never repeated as dict keys
RULE: Pydantic models serialize/deserialize themselves — no manual marshal code

```python
# BANNED — raw dict with implicit structure:
def save_user(data: dict) -> None: ...

# CORRECT — explicit structure enforced at runtime:
def save_user(user: UserResponse) -> None: ...
```

## Config Files

RULE: Use pydantic `BaseSettings` for environment/config loading
RULE: All env vars parsed into typed fields — never `os.environ["KEY"]` inline

```python
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    db_url: str
    debug: bool = False
    max_retries: int = 3
```
