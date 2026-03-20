---
tags: [threading, async, cancellation, channels]
concepts: [concurrency, async-await, task]
requires: [csharp/types.md]
keywords: [async, await, task, cancellationtoken, channel, mutex]
layer: 4
---
# Threading

> async/await everywhere — CancellationToken mandatory, no blocking on async paths

---

RULE: All I/O operations are async — no `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` on async paths
RULE: `CancellationToken` parameter on every async public method
RULE: `System.Threading.Channels` for producer/consumer pipelines
RULE: `SemaphoreSlim` for async-safe mutual exclusion
RULE: `IProgress<T>` for progress reporting — not events from background threads
RULE: All spawned tasks must be stoppable via CancellationToken

```csharp
// GOOD: CancellationToken on every async method
public async Task<User_core?> LoadUserAsync(UserId id, CancellationToken ct)
{
    await using var conn = await _db.OpenAsync(ct);
    return await conn.QueryFirstOrDefaultAsync<User_core>(sql, new { id }, ct);
}

// GOOD: Channel-based producer/consumer
var channel = Channel.CreateBounded<Event_x>(capacity: 100);

// Producer
await channel.Writer.WriteAsync(evt, ct);

// Consumer
await foreach (var evt in channel.Reader.ReadAllAsync(ct))
    await ProcessAsync(evt, ct);
```

## Uno Platform / UI Thread

RULE: UI updates only on dispatcher thread — use `DispatcherQueue.TryEnqueue()`
RULE: Never block the UI thread — `await` all async work

```csharp
// GOOD: Marshal result back to UI thread
var result = await LoadDataAsync(ct);
_dispatcherQueue.TryEnqueue(() => ViewModel.Items = result);
```

BANNED: `.Result` or `.Wait()` on a `Task` inside async context — causes deadlocks
BANNED: `Thread.Sleep` — use `await Task.Delay(ms, ct)`
BANNED: `async void` — use `async Task` except for event handlers (document why)
BANNED: Fire-and-forget `Task.Run(...)` without storing and cancelling the task
BANNED: Shared mutable state without synchronization primitive


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
