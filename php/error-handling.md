---
tags: [errors, exceptions, error-handling]
concepts: [error-taxonomy, recovery, custom-exceptions]
requires: [php/types.md, global/error-flow.md]
feeds: [php/testing.md]
keywords: [try-catch, exception, RuntimeException, DomainException]
layer: 3
---
# Error Handling

> Custom exceptions, specific catches, named recovery — never swallow errors

---

RULE: Custom exceptions inherit from a project-specific base (`AppException`)
RULE: Catch specific exception types — never bare `catch (\Exception $e)`
RULE: Every `catch` block has a named recovery action
RULE: See `global/error-flow.md` for taxonomy (Transient / UserError / SystemError / Bug)

```php
declare(strict_types=1);

abstract class AppException extends \RuntimeException {}

class ValidationException extends AppException {}

class NotFoundException extends AppException
{
    public static function forEntity(string $type, string|int $id): self
    {
        return new self("{$type} with ID {$id} not found");
    }
}

// Correct — specific catch + recovery action
try {
    $user = $this->userRepository->findOrFail($userId);
} catch (NotFoundException $e) {
    $user = $this->userFactory->createDefault($userId);  // named recovery
} catch (\PDOException $e) {
    throw new TransientException('Database unreachable', previous: $e);
}
```

BANNED: Bare `catch (\Exception $e)` without rethrowing
BANNED: Empty catch blocks — swallowing errors
BANNED: Throwing base `\Exception` — use typed subclasses
BANNED: Using `@` error suppression operator
