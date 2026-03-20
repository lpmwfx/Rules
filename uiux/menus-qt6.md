---
tags: [uiux, menus, qt6, qml, cpp, menubar, qmainwindow]
concepts: [native-menus, qt-menus, qmenubar, qml-menubar, cross-platform]
related: [uiux/help-about.md, uiux/keyboard.md, uiux/theming.md]
keywords: [qt6, qml, menubar, qmainwindow, qmenu, qaction, macos, windows, linux, shortcuts, about, preferences]
layer: 4
---
# Qt6 Menus — C++ / QML

> QMenuBar on desktop — platform-native delivery on macOS and Windows automatically

---

VITAL: Use QMenuBar attached to QMainWindow — never a custom toolbar widget replacing the menu
VITAL: Qt6 automatically places About and Preferences in the macOS Application menu — let it
RULE: File > Preferences on Windows/Linux — Application menu on macOS (Qt handles this via QAction::ApplicationSpecificRole)
RULE: Use QKeySequence::StandardKey for all shortcuts — never hardcode platform-specific keys
RULE: QML: use MenuBar { Menu { Action {} } } — not custom-drawn overlays
RULE: About dialog must show: name, version, description, website, license
BANNED: Custom drawn menubar widget replacing QMenuBar / MenuBar
BANNED: Hardcoded key strings (e.g. "Ctrl+,") when QKeySequence::Preferences exists
BANNED: Separate About actions for macOS and non-macOS — set the role and Qt routes it

## Standard Menu Structure (Windows / Linux)

```
File          Edit          View          Help
────          ────          ────          ────
Preferences   Undo Ctrl+Z   Zoom In       Keyboard Shortcuts
───           Redo          Zoom Out      Help F1
Quit          ───           ───           Report Issue
              Cut           Full Screen   ───
              Copy          ───           About MyApp
              Paste         Sidebar
              Select All
```

macOS: Preferences and About are moved to the Application menu automatically via role.

## C++ Implementation

```cpp
// mainwindow.cpp
#include <QMainWindow>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QKeySequence>

void MainWindow::createMenus()
{
    // File menu
    QMenu *fileMenu = menuBar()->addMenu(tr("&File"));

    QAction *prefsAct = fileMenu->addAction(tr("&Preferences..."));
    prefsAct->setShortcut(QKeySequence::Preferences);
    prefsAct->setMenuRole(QAction::PreferencesRole);  // -> macOS Application menu
    connect(prefsAct, &QAction::triggered, this, &MainWindow::showPreferences);

    fileMenu->addSeparator();

    QAction *quitAct = fileMenu->addAction(tr("&Quit"));
    quitAct->setShortcut(QKeySequence::Quit);
    quitAct->setMenuRole(QAction::QuitRole);          // -> macOS Application menu
    connect(quitAct, &QAction::triggered, qApp, &QCoreApplication::quit);

    // Edit menu
    QMenu *editMenu = menuBar()->addMenu(tr("&Edit"));
    editMenu->addAction(tr("&Undo"), QKeySequence::Undo, this, &MainWindow::undo);
    editMenu->addAction(tr("&Redo"), QKeySequence::Redo, this, &MainWindow::redo);
    editMenu->addSeparator();
    editMenu->addAction(tr("Cu&t"),        QKeySequence::Cut,       this, &MainWindow::cut);
    editMenu->addAction(tr("&Copy"),       QKeySequence::Copy,      this, &MainWindow::copy);
    editMenu->addAction(tr("&Paste"),      QKeySequence::Paste,     this, &MainWindow::paste);
    editMenu->addAction(tr("Select &All"), QKeySequence::SelectAll, this, &MainWindow::selectAll);

    // Help menu
    QMenu *helpMenu = menuBar()->addMenu(tr("&Help"));
    helpMenu->addAction(tr("Keyboard Shortcuts..."),
        QKeySequence(tr("Ctrl+?")), this, &MainWindow::showShortcuts);
    helpMenu->addAction(tr("Help"), QKeySequence::HelpContents, this, &MainWindow::showHelp);
    helpMenu->addAction(tr("Report Issue..."), this, &MainWindow::reportIssue);
    helpMenu->addSeparator();

    QAction *aboutAct = helpMenu->addAction(tr("About %1").arg(qApp->applicationName()));
    aboutAct->setMenuRole(QAction::AboutRole);        // -> macOS Application menu
    connect(aboutAct, &QAction::triggered, this, &MainWindow::showAbout);
}
```

## QML Implementation

```qml
// main.qml
import QtQuick.Controls 2.15

ApplicationWindow {
    id: root
    visible: true

    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")
            Action {
                text: qsTr("&Preferences...")
                shortcut: StandardKey.Preferences
                onTriggered: preferencesDialog.open()
            }
            MenuSeparator {}
            Action {
                text: qsTr("&Quit")
                shortcut: StandardKey.Quit
                onTriggered: Qt.quit()
            }
        }
        Menu {
            title: qsTr("&Edit")
            Action { text: qsTr("&Undo");      shortcut: StandardKey.Undo;      onTriggered: stack.undo() }
            Action { text: qsTr("&Redo");      shortcut: StandardKey.Redo;      onTriggered: stack.redo() }
            MenuSeparator {}
            Action { text: qsTr("Cu&t");        shortcut: StandardKey.Cut;       onTriggered: textField.cut() }
            Action { text: qsTr("&Copy");       shortcut: StandardKey.Copy;      onTriggered: textField.copy() }
            Action { text: qsTr("&Paste");      shortcut: StandardKey.Paste;     onTriggered: textField.paste() }
            Action { text: qsTr("Select &All"); shortcut: StandardKey.SelectAll; onTriggered: textField.selectAll() }
        }
        Menu {
            title: qsTr("&Help")
            Action { text: qsTr("Keyboard Shortcuts"); shortcut: "Ctrl+?"; onTriggered: shortcutsDialog.open() }
            Action { text: qsTr("Help");               shortcut: StandardKey.HelpContents; onTriggered: openHelp() }
            Action { text: qsTr("Report Issue...");    onTriggered: Qt.openUrlExternally(reportUrl) }
            MenuSeparator {}
            Action { text: qsTr("About %1").arg(Qt.application.name); onTriggered: aboutDialog.open() }
        }
    }
}
```

RULE: Always use `StandardKey.*` enum values — Qt maps them per platform automatically
RULE: `setMenuRole` / Action role routes items to the macOS Application menu without #ifdef

## About Dialog

```cpp
// C++ — QMessageBox::about or a custom dialog
void MainWindow::showAbout()
{
    QDialog *dlg = new QDialog(this);
    dlg->setWindowTitle(tr("About %1").arg(qApp->applicationName()));
    // ... populate with name, version, description, website, license
    dlg->setAttribute(Qt::WA_DeleteOnClose);
    dlg->exec();
}
```

```qml
// QML — Dialog
Dialog {
    id: aboutDialog
    title: qsTr("About %1").arg(Qt.application.name)
    modal: true

    Column {
        spacing: 8
        Label { text: Qt.application.name;    font.pixelSize: 20; font.bold: true }
        Label { text: Qt.application.version; color: palette.mid }
        Label { text: "Short description of the app."; wrapMode: Text.WordWrap }
        Label {
            text: '<a href="https://yoursite.example">yoursite.example</a>'
            onLinkActivated: Qt.openUrlExternally(link)
        }
        Label {
            text: '<a href="https://yoursite.example/license">GPL-3.0 License</a>'
            onLinkActivated: Qt.openUrlExternally(link)
        }
    }

    standardButtons: Dialog.Close
}
```

RULE: About shows: name, version, description, website link, license link
RULE: Website and license are clickable links via `onLinkActivated`


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
