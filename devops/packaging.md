# Package Formats

> Platform-specific packaging — DEB, RPM, MSI, DMG, tar.gz, APK, IPA

---

## General Rules

RULE: One package = one app (no bundling unrelated tools)
RULE: Package name lowercase with hyphens: `my-app`
RULE: Include LICENSE in every package format
RULE: Version from git tag — single source of truth
BANNED: Hardcoded versions in package metadata (derive from tag)
BANNED: Packages without uninstall capability

## DEB (Debian/Ubuntu)

```
my-app_0.1.0_amd64.deb
└── DEBIAN/
│   ├── control              # Package metadata
│   └── postinst             # Post-install script (optional)
├── usr/bin/my-app           # Binary
├── usr/share/applications/my-app.desktop  # Desktop entry (GUI)
├── usr/share/icons/hicolor/scalable/apps/my-app.svg  # Icon (GUI)
└── usr/share/doc/my-app/copyright  # License
```

### control file

```
Package: my-app
Version: 0.1.0
Section: utils
Priority: optional
Architecture: amd64
Depends: libqt6widgets6 (>= 6.5)
Maintainer: Name <email@example.com>
Description: Short one-line description
 Longer description paragraph indented with single space.
```

RULE: Install binaries to `/usr/bin/`
RULE: Desktop entries to `/usr/share/applications/`
RULE: Icons to `/usr/share/icons/hicolor/{size}/apps/`
RULE: App data to `/usr/share/{package-name}/`
BANNED: Files in `/usr/local/` (reserved for manual installs)
BANNED: Files in `/opt/` unless self-contained bundle with justification

## RPM (Fedora/RHEL)

### spec file skeleton

```spec
Name:           my-app
Version:        0.1.0
Release:        1%{?dist}
Summary:        Short one-line description
License:        EUPL-1.2
URL:            https://github.com/org/my-app

%description
Longer description paragraph.

%install
mkdir -p %{buildroot}/usr/bin
cp -a my-app %{buildroot}/usr/bin/

%files
/usr/bin/my-app
/usr/share/applications/my-app.desktop
/usr/share/icons/hicolor/scalable/apps/my-app.svg
```

RULE: Same install paths as DEB (`/usr/bin/`, `/usr/share/`)
RULE: Use CPack for dual DEB+RPM generation from same build

## MSI (Windows)

RULE: Use WiX Toolset v5 (modern, open-source)
RULE: GUI apps get Start Menu shortcut
RULE: CLI apps add install dir to PATH

```xml
<!-- WiX v5 minimal example -->
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Package Name="MyApp" Version="0.1.0"
           Manufacturer="Org" UpgradeCode="GUID-HERE">
    <MajorUpgrade DowngradeErrorMessage="Newer version installed." />
    <Feature Id="Main">
      <ComponentGroupRef Id="AppFiles" />
    </Feature>
  </Package>
</Wix>
```

RULE: Set `UpgradeCode` GUID once — never change it
RULE: Use `MajorUpgrade` for clean version upgrades
BANNED: Installers without uninstall support
BANNED: Writing to `C:\Program Files` without proper permissions

## tar.gz (Portable)

```
my-app-0.1.0-linux-amd64.tar.gz
└── my-app-0.1.0/
    ├── bin/my-app            # Binary
    ├── README.md
    └── LICENSE
```

RULE: Top-level directory named `{name}-{version}/`
RULE: Binary in `bin/` subdirectory
RULE: Always include README and LICENSE
BANNED: Tar bombs (files extracted to current directory without wrapper dir)

## DMG (macOS)

```
MyApp-0.1.0.dmg
└── MyApp.app/
    └── Contents/
        ├── MacOS/MyApp       # Binary
        ├── Resources/        # Icons, assets
        └── Info.plist        # Bundle metadata
```

RULE: GUI apps use `.app` bundle inside DMG
RULE: CLI tools use tar.gz instead
RULE: Code sign with `codesign --deep --strict`
RULE: Notarize with `xcrun notarytool submit`
BANNED: Unsigned DMGs for distribution (Gatekeeper blocks them)

## APK / AAB (Android)

RULE: Build with Gradle (`assembleRelease` / `bundleRelease`)
RULE: AAB for Play Store, APK for sideload/direct distribution
RULE: Sign with release keystore (never debug keystore)
RULE: Set `minSdk` and `targetSdk` explicitly in `build.gradle.kts`

```kotlin
android {
    defaultConfig {
        applicationId = "com.org.myapp"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.1.0"
    }
    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("KEYSTORE_PATH"))
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
}
```

BANNED: Debug keystore in release builds
BANNED: Hardcoded signing credentials in build files

## IPA (iOS)

RULE: Build with `xcodebuild archive` then `xcodebuild -exportArchive`
RULE: Use provisioning profile for distribution (App Store or Ad Hoc)
RULE: Manage certificates and profiles via CI secrets
BANNED: Manual code signing on developer machine for releases

```bash
# CI build example
xcodebuild archive \
    -project MyApp.xcodeproj \
    -scheme MyApp \
    -archivePath build/MyApp.xcarchive

xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportPath build/export \
    -exportOptionsPlist ExportOptions.plist
```
