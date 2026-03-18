---
tags: [testing, xunit, testcontainers, arrange-act-assert]
concepts: [unit-testing, integration-testing, test-naming, test-isolation]
requires: [csharp/types.md, csharp/errors.md]
feeds: [csharp/verification.md]
keywords: [xunit, testcontainers, fact, theory, assert, mock, arrange-act-assert]
layer: 4
---
# Testing

> xUnit with real dependencies — no mock objects for data, containers for integration

---

RULE: xUnit for test framework — `[Fact]` for single cases, `[Theory]` for parameterized
RULE: Real databases via TestContainers or EF Core in-memory provider — not mocked repositories
RULE: One test class per system-under-test: `ConfigLoaderTests`, `UserServiceTests`
RULE: Test name format: `MethodName_Scenario_ExpectedResult`
RULE: Arrange-Act-Assert pattern — separated by blank lines

```csharp
// GOOD: Real dependency, clear naming, AAA pattern
public class ConfigLoaderTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _db = new PostgreSqlBuilder().Build();

    public Task InitializeAsync() => _db.StartAsync();
    public Task DisposeAsync() => _db.DisposeAsync().AsTask();

    [Fact]
    public async Task LoadAsync_MissingFile_ReturnsFailResult()
    {
        // Arrange
        var loader = new ConfigLoader(_db.GetConnectionString());

        // Act
        var result = await loader.LoadAsync("missing.toml", CancellationToken.None);

        // Assert
        Assert.IsType<Result<Config_cfg>.FailResult>(result);
    }

    [Theory]
    [InlineData("dev.toml", "Development")]
    [InlineData("prod.toml", "Production")]
    public async Task LoadAsync_ValidEnvFile_ReturnsCorrectEnvironment(
        string file, string expected)
    {
        var loader = new ConfigLoader(_db.GetConnectionString());
        var result = await loader.LoadAsync(file, CancellationToken.None);
        var ok = Assert.IsType<Result<Config_cfg>.OkResult>(result);
        Assert.Equal(expected, ok.Value.Environment);
    }
}
```

BANNED: Mock objects for data layer — use TestContainers or in-memory providers
BANNED: Tests that depend on external services without containers
BANNED: `[Fact]` methods without assertions
BANNED: Test names that don't describe the scenario (`Test1`, `ItWorks`)
