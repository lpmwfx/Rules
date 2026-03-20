---
tags: [threading, jthread, concurrency]
concepts: [concurrency, async]
requires: [cpp/memory.md]
keywords: [jthread, mutex, atomic, stop-token]
layer: 4
---
# Threading

> Automatic via jthread — auto-join, stop tokens

---

RULE: `std::jthread` for threads — auto-joins on destruction
RULE: `std::stop_token` for cancellation — built into jthread
RULE: `std::mutex` + `std::scoped_lock` for synchronization
RULE: `std::atomic` for simple shared state
RULE: Thread pool for task-based parallelism

```cpp
// GOOD: Auto-joining thread
std::jthread worker([](std::stop_token st) {
    while (!st.stop_requested()) {
        // work
    }
});
// Thread automatically joins when worker goes out of scope

// GOOD: Scoped locking
std::mutex mtx;
{
    std::scoped_lock lock(mtx);
    // protected access
}  // automatically unlocks

// GOOD: Atomic for simple counters
std::atomic<int> counter{0};
counter.fetch_add(1);
```


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
