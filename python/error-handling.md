---
tags: [errors, exceptions, error-handling]
concepts: [error-taxonomy, recovery, custom-exceptions]
requires: [python/types.md, global/error-flow.md]
feeds: [python/testing.md]
keywords: [try-except, AppError, transient, user-error, system-error]
layer: 3
---
# Error Handling

> Custom exceptions, specific catches, named recovery — never swallow errors

---

RULE: Custom exceptions inherit from a project-specific base (`AppError`)
RULE: Catch specific exceptions — never bare `except:`
RULE: Every `except` has a named recovery action
RULE: See `global/error-flow.md` for taxonomy (Transient / UserError / SystemError / Bug)

```python
class AppError(Exception):
    """Base for all project exceptions."""

class ValidationError(AppError):
    """Input failed validation."""

class NotFoundError(AppError):
    """Requested resource does not exist."""

# Correct — specific catch + recovery action
try:
    user = fetch_user(user_id)
except NotFoundError:
    user = create_default_user(user_id)   # named recovery
except ConnectionError as e:
    raise TransientError("db unreachable") from e
```

BANNED: Bare `except:` without exception type
BANNED: `except Exception: pass` — swallowing errors
BANNED: Raising built-in `Exception` directly — use typed subclasses


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
