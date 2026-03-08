---
tags: [csharp, dotnet, init, initialize, bootstrap, setup, new-project]
concepts: [project-initialization, project-setup]
requires: [global/initialize.md, csharp/modules.md, csharp/verification.md]
related: [csharp/README.md, project-files/project-file.md, project-files/rules-file.md]
keywords: [dotnet, csharp, init, sln, csproj, editorconfig, gitignore, analyzers, directory.build.props]
layer: 2
---
# C# / .NET Project Initialization

> Run this INSTEAD OF improvising — every C# project starts here

---

VITAL: Run this sequence top to bottom — no skipping, no reordering
VITAL: Ask the user for: project name, GUI or CLI/API, target platforms
VITAL: Do not create code files until proj/ is complete

---

## Step 0 — Decide structure (ask user)

```
Questions to ask before touching the filesystem:
1. Project name?          (e.g. MyApp)
2. Type?                  GUI (Uno Platform) / API / CLI / Library
3. Target platforms?      Windows / macOS / Linux / Android / iOS
4. Test framework?        xUnit (default) / NUnit / MSTest
```

---

## Step 1 — Scaffold solution

```bash
mkdir MyApp && cd MyApp

# Solution
dotnet new sln -n MyApp

# Core — domain logic, no UI/infra deps
dotnet new classlib -n MyApp.Core -o MyApp.Core --framework net9.0
dotnet sln add MyApp.Core/MyApp.Core.csproj

# Infrastructure — adapters, DB, file I/O
dotnet new classlib -n MyApp.Infrastructure -o MyApp.Infrastructure --framework net9.0
dotnet sln add MyApp.Infrastructure/MyApp.Infrastructure.csproj

# Entry point — choose one:
# CLI:
dotnet new console -n MyApp.Cli -o MyApp.Cli --framework net9.0
dotnet sln add MyApp.Cli/MyApp.Cli.csproj
# API:
dotnet new webapi -n MyApp.Api -o MyApp.Api --framework net9.0
dotnet sln add MyApp.Api/MyApp.Api.csproj
# GUI (Uno Platform):
# Install Uno templates first: dotnet new install Uno.Templates
dotnet new unoapp -n MyApp.UI -o MyApp.UI
dotnet sln add MyApp.UI/**/*.csproj

# Tests
dotnet new xunit -n MyApp.Tests -o MyApp.Tests --framework net9.0
dotnet sln add MyApp.Tests/MyApp.Tests.csproj

# Project references
dotnet add MyApp.Infrastructure/MyApp.Infrastructure.csproj reference MyApp.Core/MyApp.Core.csproj
dotnet add MyApp.Tests/MyApp.Tests.csproj reference MyApp.Core/MyApp.Core.csproj
```

---

## Step 2 — Directory.Build.props (applies to ALL projects)

Create `Directory.Build.props` in the solution root:

```xml
<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisMode>All</AnalysisMode>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <LangVersion>latest</LangVersion>
    <TargetFramework>net9.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="9.*">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Meziantou.Analyzer" Version="2.*">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

---

## Step 3 — .editorconfig

Create `.editorconfig` in the solution root:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
dotnet_sort_system_directives_first = true
dotnet_style_qualification_for_field = false
dotnet_style_qualification_for_property = false
csharp_style_namespace_declarations = file_scoped:error
csharp_prefer_braces = when_multiline:warning
csharp_style_prefer_primary_constructors = true:suggestion

[*.{csproj,props,targets}]
indent_size = 2
```

---

## Step 4 — .gitignore

```bash
dotnet new gitignore
```

Then add to `.gitignore`:
```
proj/
*.user
.vs/
```

---

## Step 5 — Install tools (once per machine)

```bash
dotnet tool install -g dotnet-format
dotnet tool install -g dotnet-reportgenerator-globaltool
```

---

## Step 6 — Verify build

```bash
dotnet build -warnaserror
dotnet test
dotnet format --verify-no-changes
```

All three must be GREEN before writing any domain code.

---

## Step 7 — Create proj/ files

Now run `global/initialize.md` steps 0, 3–8:
- `proj/PROJECT` — fill in name, stack (.NET 9 / C# 13), platforms, phase 1
- `proj/RULES` — active rules: `csharp/README.md` + topology + file-limits
- `proj/TODO` — first tasks: domain types, core logic, infrastructure adapters
- `proj/FIXES` — empty, ready for entries
- `proj/INSTALL` — document the build/run commands from steps 1–6 above
- `proj/UIUX` — ONLY if Uno Platform was chosen

---

## Folder layout after init

```
MyApp/
├── Directory.Build.props   ← global csproj settings
├── .editorconfig           ← formatting + style rules
├── .gitignore              ← includes proj/
├── MyApp.sln
├── MyApp.Core/
│   └── MyApp.Core.csproj
├── MyApp.Infrastructure/
│   └── MyApp.Infrastructure.csproj
├── MyApp.Cli/  (or Api/ or UI/)
│   └── MyApp.Cli.csproj
├── MyApp.Tests/
│   └── MyApp.Tests.csproj
└── proj/
    ├── PROJECT
    ├── RULES
    ├── TODO
    ├── FIXES
    └── INSTALL
```

---

## BANNED during init

BANNED: Writing any domain code before `dotnet build` is green
BANNED: Skipping `Directory.Build.props` — nullable and analyzers are non-negotiable
BANNED: One `.csproj` for everything — Core must be separate from Infrastructure
BANNED: Putting business logic in the entry point project (Cli/Api/UI)
BANNED: Skipping proj/ files — init is not done until all proj/ files exist
