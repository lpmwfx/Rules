---
tags: [devops, cicd, github-actions, pipeline]
concepts: [ci-cd, automation]
related: [devops/publishing.md]
keywords: [github-actions, pipeline, workflow]
layer: 5
---
# CI/CD Pipeline

> Tag-triggered builds from clean checkout — artifacts go to release, never manual upload

---

## Core Principles

RULE: All release builds from clean CI checkout — no local state
RULE: Tag-triggered releases only (pattern: `v*`)
RULE: Matrix builds for all target platforms
RULE: Artifacts uploaded to release automatically
BANNED: Manual artifact uploads to releases
BANNED: Builds from dirty worktrees or local build/ directories
BANNED: Secrets in workflow files — use repository secrets only
BANNED: Skipping tests in release builds

## GitHub Actions Template

```yaml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-24.04
            platform: linux
          - os: windows-latest
            platform: windows
          - os: macos-latest
            platform: macos
    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      # --- Build step (project-specific) ---
      # CMake example:
      - name: Build
        run: |
          cmake -B build -DCMAKE_BUILD_TYPE=Release
          cmake --build build --config Release

      # --- Test step ---
      - name: Test
        run: ctest --test-dir build --output-on-failure

      # --- Package step (see packaging.md) ---
      - name: Package
        run: cd build && cpack

      # --- Upload to release ---
      - uses: softprops/action-gh-release@v2
        with:
          files: build/packages/*
```

## Platform Build Notes

### Linux
- Runner: `ubuntu-24.04`
- Packages: DEB + RPM + tar.gz via CPack or native tools
- Desktop apps: include `.desktop` file and icon in package

### Windows
- Runner: `windows-latest`
- Package: MSI via WiX Toolset v5 (open-source, modern)
- CLI tools: add to PATH during install
- GUI apps: Start Menu shortcut

### macOS
- Runner: `macos-latest`
- GUI: DMG with .app bundle
- CLI: tar.gz
- RULE: Code sign with Developer ID for distribution
- RULE: Notarize with `notarytool` before upload

### Android
- Build: Gradle with `assembleRelease` / `bundleRelease`
- Artifact: APK (sideload) + AAB (Play Store)
- RULE: Sign with release keystore (stored as repo secret)

### iOS
- Build: `xcodebuild archive` + `xcodebuild -exportArchive`
- Artifact: IPA
- RULE: Provisioning profile managed via CI secrets

## Qt-Specific Notes

```yaml
# Qt install via aqtinstall
- uses: jurplel/install-qt-action@v4
  with:
    version: '6.7.3'
    cache: true

# Set Qt path for CMake
- name: Build
  run: |
    cmake -B build -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_PREFIX_PATH=$Qt6_DIR
    cmake --build build --config Release
```

RULE: Pin Qt version — do not use `latest`
RULE: Cache Qt install (saves ~3 min per build)
RULE: Use platform deploy tools (`linuxdeployqt`, `windeployqt`, `macdeployqt`)

## Caching Strategy

RULE: Cache dependency installs (Qt, vcpkg, pip, npm)
RULE: Never cache build artifacts across releases
RULE: Use `actions/cache@v4` with version-pinned keys

## Release Naming

RULE: Release title = tag name (e.g., `v0.1.0`)
RULE: Artifact names include platform and version: `project-0.1.0-linux-amd64.deb`
BANNED: Generic artifact names like `build.zip` or `output.tar.gz`
