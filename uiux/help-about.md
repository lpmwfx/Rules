---
tags: [uiux, help, about, shortcuts-window, license, platform-ux]
concepts: [help-system, about-dialog, shortcuts-window, discoverability]
requires: [uiux/keyboard.md, uiux/context-menus.md]
related: [uiux/checklist.md, uiux/issue-reporter.md]
keywords: [about, help, license, shortcuts, author, website, F1, Ctrl+question, AdwAboutDialog, NSAboutPanel, platform-native]
layer: 4
---
# Help, About, and Shortcuts

> Every GUI app must have About, a license, and a shortcuts overview — delivered natively per platform

---

VITAL: Every GUI app ships with an About dialog, a license, and a keyboard shortcuts overview
VITAL: Use the platform-native mechanism — never a custom dialog where a standard one exists
RULE: About is reached from the primary menu (hamburger) → "About [AppName]"
RULE: Shortcuts overview is reached via `Ctrl+?` and from the primary menu
RULE: Help is reached via `F1` — minimum: opens shortcuts window or a help view
RULE: About must contain: app name, version, short description, author name, website, license
BANNED: Shipping without About, license, or shortcuts overview
BANNED: Custom About dialog on platforms that provide a standard one (GNOME, macOS, KDE)

## Minimum Content — About

Every About dialog must show at minimum:

| Field | Example |
|-------|---------|
| App name | MyApp |
| Version | 1.2.0 |
| Short description | 1–2 sentences |
| Author / developer | Your Name |
| Website | https://yoursite.example |
| License | GPL-3.0 / MIT / EUPL-1.2 |
| Copyright year | © 2024–2026 |

Optional but recommended: source code link, issue tracker link, release notes.

## Minimum Content — Shortcuts Window

Shows all app-specific shortcuts grouped by category.
Platform-standard shortcuts (Ctrl+C, Ctrl+Q) may be omitted — users know them.

```
Navigation          Search              View
───────────         ───────             ────
Alt+Left  Back      Ctrl+F  Find        F9   Sidebar
Alt+Right Forward   Ctrl+G  Next        F11  Fullscreen
                    Esc     Close

[App-specific shortcuts grouped here]
```

RULE: Group shortcuts by function area, not by key
RULE: List only app-specific shortcuts — skip universal ones unless they are non-obvious
RULE: Update shortcuts window whenever a shortcut is added or removed

---

## Platform Delivery

### GNOME / GTK4 + libadwaita

**About:** `AdwAboutDialog` — the standard. Fill all fields.

```python
dialog = Adw.AboutDialog(
    application_name="MyApp",
    application_icon="com.example.MyApp",
    version="1.2.0",
    comments=_("Short description"),
    developer_name="Your Name",
    website="https://yoursite.example",
    issue_url="https://github.com/you/myapp/issues",
    license_type=Gtk.License.GPL_3_0,
    copyright="© 2024–2026 Your Name",
)
dialog.add_link(_("Source Code"), "https://github.com/you/myapp")
dialog.present(self)
```

**Shortcuts:** `GtkShortcutsWindow` — defined in Blueprint/UI file, opened via `Ctrl+?`.

```xml
<!-- shortcuts.ui -->
<object class="GtkShortcutsWindow">
  <child>
    <object class="GtkShortcutsSection">
      <child>
        <object class="GtkShortcutsGroup" title="Navigation">
          <child>
            <object class="GtkShortcutsShortcut"
                    title="Go Back" accelerator="&lt;alt&gt;Left"/>
          </child>
        </object>
      </child>
    </object>
  </child>
</object>
```

```python
app.set_accels_for_action("win.show-help-overlay", ["&lt;ctrl&gt;question"])
```

**Help (`F1`):** Opens the shortcuts window. Full help docs are optional for small apps.

---

### macOS / SwiftUI + AppKit

**About:** `NSApp.orderFrontStandardAboutPanel()` — free, reads from `Info.plist`.

```swift
// Info.plist keys (set in Xcode target):
// CFBundleShortVersionString → version shown
// NSHumanReadableCopyright   → copyright line

// Trigger from menu:
Button("About MyApp") {
    NSApp.orderFrontStandardAboutPanel(nil)
}

// Custom fields:
NSApp.orderFrontStandardAboutPanel(withOptions: [
    .applicationName: "MyApp",
    .credits: NSAttributedString(string: "yoursite.example"),
])
```

**Shortcuts:** Custom `SwiftUI` view shown as a sheet, triggered by `⌘?` (`Cmd+?`).

```swift
.keyboardShortcut("?", modifiers: .command)
```

**Help menu:** Standard macOS Help menu — `NSHelpManager` for searchable help (optional).

---

### Windows / WinUI 3

**About:** `ContentDialog` with app info — no system standard, implement consistently.

```csharp
var dialog = new ContentDialog {
    Title = "About MyApp",
    Content = new AboutPage(),   // custom UserControl
    CloseButtonText = "Close",
    XamlRoot = this.XamlRoot,
};
await dialog.ShowAsync();
```

**Shortcuts:** `ContentDialog` or a dedicated settings page with shortcut table.

**Help:** `F1` opens shortcuts dialog or a help `ContentDialog`.

---

### KDE / Qt 6 + QML

**About:** `KAboutApplicationDialog` (KDE Frameworks) or `QMessageBox::aboutQt`-style.

```cpp
KAboutData aboutData("myapp", i18n("MyApp"), "1.2.0",
    i18n("Short description"), KAboutLicense::GPL_V3,
    i18n("© 2024–2026 Your Name"), QString(),
    "https://yoursite.example");
aboutData.addAuthor(i18n("Your Name"), QString(), "you@example.com");
KAboutData::setApplicationData(aboutData);
// Dialog:
auto *dialog = new KAboutApplicationDialog(KAboutData::applicationData(), parent);
dialog->show();
```

**Shortcuts:** `KShortcutsDialog` — lists all registered `QAction` shortcuts automatically.

```cpp
KShortcutsDialog::showDialog(actionCollection(), KShortcutsEditor::LetterShortcuts, this);
```

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

---

### Web / PWA

**About:** Modal dialog or `/about` route.

**Shortcuts:** Overlay triggered by `?` key — show app-specific shortcuts only.

```js
document.addEventListener('keydown', e => {
    if (e.key === '?' && !e.ctrlKey && !e.metaKey) showShortcutsOverlay()
})
```

---

## Checklist

Add to [checklist.md](checklist.md):

- [ ] About dialog opens from primary menu
- [ ] About contains: name, version, description, author, website, license
- [ ] Shortcuts window opens via `Ctrl+?` (desktop) or `?` (web)
- [ ] Shortcuts window lists all app-specific shortcuts grouped by category
- [ ] `F1` opens help or shortcuts (desktop platforms)
- [ ] License text accessible from About dialog

RESULT: Users can always discover what the app is, who made it, and how to use it efficiently
REASON: About + shortcuts are platform citizenship requirements — not optional polish
