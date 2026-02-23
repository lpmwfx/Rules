# Modular Architecture

> One file per component — self-contained modules

---

RULE: Each component/module has its own CSS file
RULE: File name matches component name (`nav.css` for `.nav-*`)
RULE: Module CSS is SELF-CONTAINED — no dependencies on other modules
RULE: Modules can be added/removed without breaking others

## File Structure

```
css/
├── base/
│   ├── reset.css       # Reset only
│   └── typography.css  # Base typography
├── components/
│   ├── nav.css         # .nav-* classes
│   ├── card.css        # .card-* classes
│   ├── button.css      # .btn-* classes
│   └── form.css        # .form-* classes
├── layout/
│   ├── site.css        # .site-* structure
│   └── container.css   # .container-* wrappers
└── themes/
    ├── light.css       # Light theme variables
    └── dark.css        # Dark theme overrides
```

RULE: Each module file starts with its block prefix
RULE: No module should style another module's classes
RULE: Shared styles go in `base/` (typography, reset)
RULE: Import order: reset → base → layout → components → themes

BANNED: Cross-module selectors (`.nav .card-title`)
BANNED: Styles for multiple components in one file
BANNED: Generic class names without module prefix
