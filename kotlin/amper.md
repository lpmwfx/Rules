---
tags: [kotlin, amper, build-system, configuration]
concepts: [build-system, configuration]
related: [kotlin/compose.md, kotlin/stability.md]
keywords: [amper, module-yaml, kmp]
layer: 4
---
# Amper Build System

> module.yaml — no Gradle for desktop, minimal config

---

RULE: `module.yaml` for configuration (no Gradle)
RULE: Minimal dependencies
RULE: Use JetBrains Compose dependencies (`$compose.*`)

## Installation

```bash
# Linux/macOS
curl -fsSL -o amper "https://packages.jetbrains.team/maven/p/amper/amper/org/jetbrains/amper/amper-cli/0.9.0/amper-cli-0.9.0-wrapper?download=true" && chmod +x amper
```

Update: `./amper update`
Docs: https://amper.org/

## Android App

```yaml
product: android/app

dependencies:
  - $compose.foundation
  - $compose.material3
  - $compose.uiTooling
  - androidx.activity:activity-compose:1.8.2
  - io.ktor:ktor-client-android:2.3.7

settings:
  android:
    namespace: eu.psid.app
    applicationId: eu.psid.app
    minSdk: 26
    targetSdk: 34
  compose: enabled
```

## Desktop App

```yaml
product: jvm/app

dependencies:
  - $compose.foundation
  - $compose.material3
  - $compose.desktop.currentOs
  - io.ktor:ktor-client-cio:2.3.7

settings:
  compose: enabled
```

## Shared Library

```yaml
product:
  type: lib
  platforms: [jvm, android]

dependencies:
  - io.ktor:ktor-client-core:2.3.7
  - org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3
  - org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2
```
