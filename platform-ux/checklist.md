# New App Checklist

> Verify before shipping — all platform UX requirements

---

## Pre-Ship Verification

- [ ] All standard keyboard shortcuts implemented
- [ ] No system-reserved shortcuts used
- [ ] Shortcuts are discoverable (dialog, tooltips, menu labels)
- [ ] Terminal context menu has minimum items
- [ ] File tree context menu has minimum items
- [ ] Primary menu has required items (Shortcuts, Preferences, Help, About)
- [ ] File → terminal drag-and-drop works with relative/absolute paths
- [ ] Drop targets show visual feedback
- [ ] All drag-drop actions have keyboard alternatives
- [ ] Context menus accessible via keyboard (Shift+F10)
- [ ] No hover-only interactions
- [ ] "Report Issue / Request Feature" in Help menu launches Issue Reporter
- [ ] Crash handler spawns Issue Reporter with crash log
- [ ] Issue Reporter launches as detached process (survives host crash)

## Toolkit Implementation

### GTK4 / GJS / Rust

```
// Register shortcuts via actions
app.set_accels_for_action("win.copy", &["<Ctrl><Shift>c"]);
app.set_accels_for_action("win.paste", &["<Ctrl><Shift>v"]);

// Context menu via GestureClick
let gesture = gtk::GestureClick::new();
gesture.set_button(gdk::BUTTON_SECONDARY);

// Drag-and-drop via DropTarget
let drop = gtk::DropTarget::new(gio::File::static_type(), gdk::DragAction::COPY);
drop.connect_drop(|target, value, x, y| { ... });
```

### Qt / QML

```qml
// Shortcuts via Actions
Action { shortcut: "Ctrl+Shift+C"; onTriggered: App.copy() }

// Context menu via MouseArea
MouseArea {
    acceptedButtons: Qt.RightButton
    onClicked: contextMenu.popup()
}

// Drag-and-drop via DropArea
DropArea {
    onDropped: (drop) => {
        if (drop.hasUrls) App.insertPaths(drop.urls)
    }
}
```
