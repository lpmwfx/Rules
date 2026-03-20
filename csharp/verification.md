---
tags: [verification, analyzers, testing, dotnet]
concepts: [testing, static-analysis, code-quality]
requires: [csharp/types.md]
keywords: [roslyn, analyzer, dotnet-format, xunit, coverlet]
layer: 4
---
# Verification Stack

> Gating levels — local, merge, release

---

## Install Once

```bash
dotnet tool install -g dotnet-format
dotnet tool install -g dotnet-reportgenerator-globaltool
```

Add to `.csproj` (all projects):
```xml
<PropertyGroup>
  <Nullable>enable</Nullable>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  <AnalysisMode>All</AnalysisMode>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
</PropertyGroup>
```

## Level 0 — Local Build Gate

- `dotnet format --verify-no-changes`
- `dotnet build -warnaserror`
- `dotnet test`

## Level 1 — Merge Gate

- All Level 0 checks
- `dotnet test --collect:"XPlat Code Coverage"`
- Coverage threshold enforced in CI (min 80% for new code)
- `dotnet list package --vulnerable` (no known vulnerabilities)

## Level 2 — Release Gate

- All Level 0 + 1 checks
- `dotnet publish -c Release` succeeds without warnings
- Integration tests pass against real dependencies (DB, APIs)
- Platform smoke tests: Windows, macOS, Linux, (Android/iOS via Uno)

## Definitions

- **Green build**: Level 0 passed
- **Green merge**: Level 0 + 1 passed
- **Green release**: Level 0 + 1 + 2 passed

## Recommended Analyzers

| Package | Purpose |
|---------|---------|
| `Microsoft.CodeAnalysis.NetAnalyzers` | Built-in (enabled via `AnalysisMode`) |
| `StyleCop.Analyzers` | Style enforcement |
| `SonarAnalyzer.CSharp` | Bug and smell detection |
| `Meziantou.Analyzer` | Best practices, async patterns |


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
