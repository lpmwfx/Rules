# Theme Switching

> Light on :root, dark on data-theme attribute

---

PATTERN: Light theme on `:root` (default)
PATTERN: Dark theme on `:root[data-theme="dark"]`
RULE: Toggle via `data-theme` attribute on `<html>`

## Example

```css
/* light-theme.css */
:root {
  --color-bg-1: #ffffff;
  --color-text-1: #111827;
}

/* dark-theme.css */
:root[data-theme="dark"] {
  --color-bg-1: #0f0f0f;
  --color-text-1: #f0f0f0;
}
```
