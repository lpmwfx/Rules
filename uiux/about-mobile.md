---
tags: [uiux, about, mobile, android, ios, compose, swiftui]
concepts: [about-screen-mobile, mobile-about]
requires: [uiux/help-about.md]
related: [uiux/menus-android.md, uiux/menus-ios.md, kotlin/tokens.md]
keywords: [AboutScreen, AboutView, Composable, SwiftUI, List, Section, LabeledContent, navigation-drawer, settings]
layer: 4
---
# About — Mobile Platforms (Android + iOS)

> Dedicated About screen reached from navigation drawer or Settings

---

### Android / Jetpack Compose

**About:** Dedicated `AboutScreen` composable — reached from navigation drawer or Settings.

```kotlin
@Composable
fun AboutScreen() {
    Column {
        Text("MyApp", style = MaterialTheme.typography.headlineMedium)
        Text("Version 1.2.0")
        Text("© 2024–2026 Your Name")
        TextButton(onClick = { openUrl("https://yoursite.example") }) {
            Text("yoursite.example")
        }
        TextButton(onClick = { openUrl(licenseUrl) }) {
            Text("License: GPL-3.0")
        }
    }
}
```

**Shortcuts:** Not applicable for touch-primary apps. Show gesture guide instead if needed.

---

### iOS / SwiftUI

**About:** Settings screen or dedicated About view in app navigation.

```swift
struct AboutView: View {
    var body: some View {
        List {
            Section {
                LabeledContent("Version", value: appVersion)
                LabeledContent("Developer", value: "Your Name")
                Link("Website", destination: URL(string: "https://yoursite.example")!)
                Link("License", destination: URL(string: licenseUrl)!)
            }
        }
        .navigationTitle("About")
    }
}
```

**Shortcuts:** Not applicable. Document gestures in a dedicated help view if complex.

RESULT: Mobile users find About via standard navigation (drawer, settings) — no hidden discovery
REASON: Mobile apps without About/license information fail app store review and user trust
