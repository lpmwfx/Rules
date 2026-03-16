---
tags: [uiux, about, desktop, gnome, macos, windows, kde, platform-native]
concepts: [about-dialog-desktop, platform-native-about]
requires: [uiux/help-about.md]
related: [uiux/menus-gnome.md, uiux/menus-macos.md, uiux/menus-windows.md, uiux/menus-kde.md]
keywords: [AdwAboutDialog, NSAboutPanel, ContentDialog, KAboutApplicationDialog, GtkShortcutsWindow, KShortcutsDialog, about, shortcuts, F1, Ctrl-question]
layer: 4
---
# About and Shortcuts — Desktop Platforms

> Use the platform-native mechanism — GNOME, macOS, Windows, KDE

---

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

**Shortcuts:** Custom `SwiftUI` view shown as a sheet, triggered by `Cmd+?`.

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

RESULT: Each desktop platform uses its native About/Shortcuts mechanism — zero custom dialogs where standards exist
REASON: Custom About dialogs look out of place and miss platform features (license display, action search)
