---
tags: [threading, dispatchers, structured-concurrency, channels]
concepts: [concurrency, structured-concurrency, dispatcher-selection, channels]
requires: [kotlin/coroutines.md, kotlin/errors.md]
keywords: [dispatcher, GlobalScope, channel, flow, withContext, supervisorJob]
layer: 4
---
# Threading

> Structured concurrency — every coroutine has a scope owner

---

RULE: `Dispatchers.IO` for blocking I/O — never `Dispatchers.Main`
RULE: `Dispatchers.Default` for CPU-bound work
RULE: Structured concurrency — every coroutine has a scope owner
RULE: `Channel` or `Flow` for producer-consumer patterns
RULE: `withContext` for dispatcher switching — never manual thread management

```kotlin
class ImageProcessor_adp(private val scope: CoroutineScope) {

    fun processImages(paths: List<String>): Flow<ProcessResult> = channelFlow {
        paths.forEach { path ->
            launch {
                val result = withContext(Dispatchers.Default) {
                    decodeAndResize(path)   // CPU-bound
                }
                val saved = withContext(Dispatchers.IO) {
                    saveToDisk(result)       // I/O-bound
                }
                send(ProcessResult.Done(saved))
            }
        }
    }
}
```

BANNED: `GlobalScope.launch` — use structured scope
BANNED: `runBlocking` on main thread
BANNED: `Thread()` / `Executors` — use coroutines


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
