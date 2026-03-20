---
tags: [async, threading, concurrency, asyncio]
concepts: [async-io, thread-pool, GIL, event-loop]
requires: [python/error-handling.md]
keywords: [asyncio, concurrent-futures, ThreadPoolExecutor, await, GIL]
layer: 4
---
# Threading & Async

> asyncio for I/O-bound, ThreadPoolExecutor for CPU-bound — never block the loop

---

RULE: `asyncio` for I/O-bound concurrency
RULE: `concurrent.futures.ThreadPoolExecutor` for CPU-bound with GIL release
RULE: Never block the event loop — use `await` or `run_in_executor`
RULE: `async with` for resource management in async context

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# I/O-bound — use asyncio
async def fetch_all(urls: list[str]) -> list[bytes]:
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# CPU-bound — offload to thread pool
async def compress(data: bytes) -> bytes:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, zlib.compress, data)
```

BANNED: `time.sleep()` in async code — use `asyncio.sleep()`
BANNED: Fire-and-forget tasks — always await or track


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
