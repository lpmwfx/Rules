---
tags: [safety, security, input-validation]
concepts: [sql-injection, xss, deserialization, code-injection]
requires: [php/types.md, global/validation.md]
keywords: [eval, exec, shell-exec, sql-injection, xss, unserialize, prepared-statements]
layer: 4
---
# Safety & Security

> No eval, no raw SQL, no unserialize on untrusted data — sanitize at boundaries

---

RULE: Never use `eval()`, `exec()`, `system()`, or backtick operator
RULE: Parameterized queries only — never interpolate user input into SQL
RULE: `htmlspecialchars()` or templating engine escaping for all output
RULE: `unserialize()` only for trusted data — use `json_decode()` for untrusted
RULE: Input sanitization at system boundaries

```php
declare(strict_types=1);

// Safe database query — parameterized
$stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
$stmt->execute(['email' => $email]);

// Safe output — escaped
echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// Safe command execution — escapeshellarg
$output = shell_exec('git log --oneline ' . escapeshellarg($branch));

// Safe deserialization of untrusted input
$data = json_decode($userInput, true, 512, JSON_THROW_ON_ERROR);
```

BANNED: `eval()`, `exec()`, `system()`, `passthru()`, `shell_exec()` with unescaped input
BANNED: String interpolation in SQL queries
BANNED: `unserialize()` on untrusted data
BANNED: `extract()` on user input
BANNED: `$$variable` (variable variables) with user-controlled names
BANNED: `include`/`require` with user-controlled paths
