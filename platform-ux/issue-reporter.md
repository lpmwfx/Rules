---
tags: [platform-ux, issue-reporter, bug-reporting, crash]
concepts: [bug-reporting, crash-handling]
keywords: [crash-report, error-boundary, feedback]
layer: 5
---
# Issue Reporter Integration

> Separate process for crash survival — shared across all apps

---

## Principle

RULE: Issue Reporter runs as its own process, NOT embedded in the host app

### Why

1. **Crash survival** — if host app crashes, reporter must still work
2. **Full stdio** — reporter has own stdin/stdout/stderr
3. **Shared** — one reporter binary, every app launches it

## User-Initiated (Help Menu)

```
issue-reporter --app-id <app_id> --app-version <version> [--type bug|feature]
```

## On Crash (Automatic)

```
issue-reporter --app-id <app_id> --crash --crash-log <path_to_log>
```

## Context Passed to Reporter

| Field | Source | Purpose |
|---|---|---|
| `--app-id` | App's own ID | Identify which app |
| `--app-version` | Version string | Identify which version |
| `--type` | User choice or auto | Pre-select form type |
| `--crash` | Flag | Switch to crash report mode |
| `--crash-log` | Temp file | Pre-fill crash details |

## Platform Launch Methods

| Platform | Method |
|---|---|
| GNOME (GTK/GJS/Rust) | `GLib.spawn_async` or `std::process::Command` |
| KDE (Qt/QML) | `QProcess::startDetached` |
| Sailfish | `Qt.openUrlExternally` or `QProcess` |

RULE: Launch as detached process — must survive host crash
