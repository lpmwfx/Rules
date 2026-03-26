---
tags: [async, queues, fibers, concurrency]
concepts: [async-io, queue-processing, fibers]
requires: [php/error-handling.md]
keywords: [queue, fiber, amphp, reactphp, pcntl, worker]
layer: 4
---
# Concurrency & Queues

> Queues for background work, Fibers for async I/O — PHP is request-scoped

---

RULE: Use queues for long-running or background tasks — not inline execution
RULE: PHP 8.1+ Fibers for cooperative multitasking when needed
RULE: One job per class — single responsibility
RULE: Jobs must be idempotent — safe to retry on failure

```php
declare(strict_types=1);

// Queue job — idempotent, single responsibility
final class SendInvoiceEmail implements ShouldQueue
{
    public function __construct(
        private readonly int $invoiceId,
    ) {}

    public function handle(Mailer $mailer, InvoiceRepository $repo): void
    {
        $invoice = $repo->findOrFail($this->invoiceId);
        if ($invoice->emailSentAt !== null) {
            return;  // idempotent — already sent
        }

        $mailer->send(new InvoiceMail($invoice));
        $repo->markEmailSent($invoice);
    }
}
```

BANNED: Long-running tasks in HTTP request cycle
BANNED: `sleep()` in request handlers
BANNED: Non-idempotent queue jobs
