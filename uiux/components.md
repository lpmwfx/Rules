---
tags: [uiux, components, single-responsibility, composition, declarative, minimal]
concepts: [component-design, single-responsibility, declarative-ui, composition]
requires: [global/topology.md, global/file-limits.md, global/module-tree.md]
feeds: [uiux/state-flow.md]
related: [uiux/file-structure.md, global/app-model.md]
keywords: [component, view, widget, composable, template, single-file, minimal, size-limit, split, extract, responsibility]
layer: 2
---
# UI Component Rules

> One file, one component, one job — small by default

---

VITAL: Every UI component has exactly one responsibility
VITAL: Count lines before adding to a component file — at 80 lines plan the split, at 100 lines stop and split first
RULE: One component per file — file name matches component name
RULE: Compose via small components, never via deep nesting
RULE: Components are stateless by default — receive state in, emit events out
RULE: No business logic inside components — delegate to Adapter
BANNED: Components that render multiple independent UI concerns
BANNED: Inline conditional logic deeper than one level — extract to sub-component
BANNED: Side effects inside render / composable / template body

## Single Responsibility

A component does one thing. If you can describe it with "and", split it.

RULE: HomeScreen shows the home — not home AND sidebar AND header
RULE: Extract a sub-component whenever a section can be named independently
RULE: Formatting, conditional rendering, computed labels → computed property in Adapter — not in the component

```
// Too broad — split this
UserDashboard renders: user profile + activity feed + notification list

// Right — one responsibility each
UserProfile       renders user details
ActivityFeed      renders the scrollable event list
NotificationBadge renders the count bubble
```

## Size Limits

See [global/file-limits.md](../global/file-limits.md) for the authoritative numbers.

RULE: If you must scroll to understand a component → split it now
RULE: One screen component ≤ 3 levels of nesting visible at a glance
BANNED: God components that own multiple screens' worth of markup

## Naming

RULE: File name = component name, PascalCase (UserCard.tsx, UserCard.kt, user_card.py)
RULE: Screen/page entry points: `NameScreen` or `NamePage` — e.g. `HomeScreen`, `SettingsPage`
RULE: Reusable components: descriptive noun — `UserCard`, `ActionButton`, `LoadingSpinner`
RULE: Private sub-components may live in the same file only if they are ≤ 20 lines and used nowhere else

## Cross-Toolkit Examples

### React / SolidJS / Svelte

```tsx
// UserCard.tsx — one component, one file
export function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <div className="user-card" onClick={() => onSelect(user.id)}>
      <Avatar src={user.avatarUrl} alt={user.name} />
      <UserInfo name={user.name} role={user.role} />
    </div>
  )
}
// Avatar.tsx and UserInfo.tsx live in their own files
```

### Jetpack Compose / Compose Multiplatform

```kotlin
// UserCard.kt — one composable, one file
@Composable
fun UserCard(user: UserViewModel_adp, onSelect: (String) -> Unit) {
    Card(onClick = { onSelect(user.id) }) {
        Avatar(url = user.avatarUrl, name = user.name)
        UserInfo(name = user.name, role = user.role)
    }
}
```

### Qt / QML

```qml
// UserCard.qml — one item, one file
Item {
    required property var user
    signal selectRequested(string userId)

    MouseArea { onClicked: selectRequested(user.id) }
    Avatar     { source: user.avatarUrl }
    UserInfo   { name: user.name; role: user.role }
}
```

### GTK4 / Python (Adwaita)

```python
# user_card.py — one widget class, one file
@Gtk.Template(resource_path='/ui/user_card.ui')
class UserCard(Adw.ActionRow):
    __gsignals__ = {'select-requested': (GObject.SIGNAL_RUN_FIRST, None, (str,))}

    def on_clicked(self, *_):
        self.emit('select-requested', self._user.id)
```

### Slint

```slint
// UserCard.slint — one component, one file
component UserCard {
    in property <UserViewModel> user;
    callback select-requested(string);

    TouchArea { clicked => { select-requested(user.id); } }
    Avatar    { source: user.avatar-url; }
    UserInfo  { name: user.name; role: user.role; }
}
```

RESULT: Every component can be understood, tested, and replaced in isolation
REASON: Small, named, single-purpose components are the unit of UI composition
