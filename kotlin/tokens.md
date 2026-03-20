---
tags: [tokens, compose, design-tokens, material-theme]
concepts: [compose-theming, material-design-tokens]
requires: [uiux/tokens.md]
related: [uiux/token-switching.md, uiux/theming.md]
keywords: [MaterialTheme, colorScheme, typography, AppTheme, darkTheme, isSystemInDarkTheme, Composable]
layer: 3
---
# Kotlin/Compose Token Implementation

> MaterialTheme as the token system — zero literal colors or sizes in composables

---

```kotlin
// tokens/AppTheme.kt — central theme entry point
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme,
        typography = AppTypography,
        content = content
    )
}

// Component uses MaterialTheme — zero literals
@Composable
fun PrimaryButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary  // token
        )
    ) {
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium         // token
        )
    }
}
```

RESULT: Compose uses MaterialTheme as the single token source — swap color scheme, entire app updates
REASON: Hardcoded Color() and TextStyle() values bypass the theme system and break dark mode


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
