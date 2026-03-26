---
tags: [modules, namespaces, autoloading, psr-4]
concepts: [module-structure, encapsulation, autoloading]
requires: [global/module-tree.md, global/topology.md]
keywords: [namespace, psr-4, composer, autoload, use-statement]
layer: 3
---
# Modules & Namespaces

> One class per file — PSR-4 autoloading, namespace maps to directory

---

RULE: One class/interface/enum per file — file name matches class name
RULE: PSR-4 autoloading — namespace maps directly to directory structure
RULE: Private by default — use `private` visibility, promote to `protected`/`public` only when needed
RULE: Group `use` statements: PHP classes, then third-party, then project

```php
declare(strict_types=1);

namespace App\Domain\Invoice;

use DateTimeImmutable;
use Vendor\Money\Money;
use App\Domain\Shared\Entity;

final class Invoice extends Entity
{
    // One focused responsibility
}
```

## Directory-to-Namespace Mapping

```
src/
├── Domain/
│   ├── Invoice/
│   │   ├── Invoice.php          → App\Domain\Invoice\Invoice
│   │   ├── InvoiceLine.php      → App\Domain\Invoice\InvoiceLine
│   │   └── InvoiceRepository.php
│   └── User/
│       └── User.php             → App\Domain\User\User
├── Infrastructure/
│   └── Persistence/
│       └── EloquentInvoiceRepository.php
└── Http/
    └── Controllers/
        └── InvoiceController.php
```

BANNED: Multiple classes in one file
BANNED: Global functions outside `helpers.php`
BANNED: Circular namespace dependencies
