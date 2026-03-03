---
tags: [uiux, menus, ios, swiftui, tabview, toolbar, navigation]
concepts: [native-menus, ios-navigation, hig, tabview, navigationstack]
related: [uiux/help-about.md, uiux/theming.md, uiux/state-flow.md]
keywords: [ios, swiftui, tabview, navigationstack, toolbar, toolbaritem, sheet, contextmenu, about, settings]
layer: 4
---
# iOS Navigation — SwiftUI

> No menubar on iOS — TabView for primary nav, toolbar items for secondary actions

---

VITAL: iOS has no menubar — use TabView for top-level navigation, NavigationStack for hierarchy
VITAL: TabView max 5 items — use "More" pattern or restructure if more destinations needed
RULE: Secondary actions go in .toolbar { ToolbarItem } — not in a custom overlay
RULE: About is presented as a sheet or pushed NavigationLink
RULE: Settings belong in a dedicated Settings screen pushed via NavigationLink
RULE: Use .contextMenu for long-press actions on list items
RULE: Back navigation is automatic via NavigationStack — no custom back button on standard screens
BANNED: Custom menubar widget on iOS
BANNED: TabView with more than 5 tabs without restructuring
BANNED: Putting app settings inside an alert or sheet — use a full NavigationLink screen

## iOS Navigation Structure

```
TabView (primary navigation — max 5 tabs)
┌─────────────────────────────────────┐
│  NavigationStack                    │
│  ┌─────────────────────────────┐    │
│  │ Navigation Bar              │    │
│  │  Title              [⊕][⋯] │    │  ← ToolbarItems
│  └─────────────────────────────┘    │
│                                     │
│  (content)                          │
│                                     │
├─────────────────────────────────────┤
│  [Home]  [Search]  [Browse]  [You]  │  ← Tab bar
└─────────────────────────────────────┘
```

Toolbar overflow (ellipsis menu or explicit items):
```
Settings
Help
Share...
─────────
About
```

## SwiftUI Implementation

```swift
// Root app structure
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        TabView {
            HomeTab()
                .tabItem { Label("Home", systemImage: "house") }
            SearchTab()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
            LibraryTab()
                .tabItem { Label("Library", systemImage: "books.vertical") }
            ProfileTab()
                .tabItem { Label("Profile", systemImage: "person") }
        }
    }
}
```

```swift
// Screen with toolbar
struct HomeTab: View {
    @State private var showSettings = false
    @State private var showAbout = false

    var body: some View {
        NavigationStack {
            List { /* content */ }
                .navigationTitle("Home")
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button(action: { /* primary action */ }) {
                            Image(systemName: "plus")
                        }
                    }
                    ToolbarItem(placement: .secondaryAction) {
                        Menu {
                            Button("Settings") { showSettings = true }
                            Button("Help") { /* open help URL */ }
                            Divider()
                            Button("About") { showAbout = true }
                        } label: {
                            Image(systemName: "ellipsis.circle")
                        }
                    }
                }
                .sheet(isPresented: $showSettings) { SettingsView() }
                .sheet(isPresented: $showAbout)    { AboutView() }
        }
    }
}
```

## Settings Screen

```swift
// Settings as a sheet or NavigationLink destination
struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @AppStorage("notifications_enabled") private var notificationsEnabled = true

    var body: some View {
        NavigationStack {
            Form {
                Section("Notifications") {
                    Toggle("Enable notifications", isOn: $notificationsEnabled)
                }
                Section("Appearance") {
                    // theme settings
                }
            }
            .navigationTitle("Settings")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
```

RULE: Use `@AppStorage` for simple persistent settings — no manual UserDefaults
RULE: Present settings as a sheet (modal) from toolbar — not a tab item

## About View

```swift
struct AboutView: View {
    @Environment(\.dismiss) private var dismiss
    let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "?"

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {
                Image("AppIcon")
                    .resizable().frame(width: 80, height: 80).clipShape(RoundedRectangle(cornerRadius: 18))
                Text("MyApp")
                    .font(.largeTitle.bold())
                Text("Version \(version)")
                    .foregroundStyle(.secondary)
                Text("Short description of what the app does.")
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
                Divider()
                Link("yoursite.example", destination: URL(string: "https://yoursite.example")!)
                Link("GPL-3.0 License",  destination: URL(string: "https://yoursite.example/license")!)
            }
            .padding()
            .navigationTitle("About")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
```

RULE: About shows: app icon, name, version, description, website link, license link
RULE: Use `Link` for website and license — tappable, opens in Safari

## Context Menus

```swift
// Long-press context menu on list items
List(items) { item ->
    ItemRow(item: item)
        .contextMenu {
            Button { share(item) } label: { Label("Share", systemImage: "square.and.arrow.up") }
            Button { favorite(item) } label: { Label("Favorite", systemImage: "star") }
            Divider()
            Button(role: .destructive) { delete(item) } label: {
                Label("Delete", systemImage: "trash")
            }
        }
}
```

RULE: Destructive context menu actions must use `role: .destructive`
