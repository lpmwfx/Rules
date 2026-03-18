---
tags: [csharp, safety, unsafe, nullable, span, memory]
concepts: [memory-safety, unsafe-code, nullable-reference-types, stack-allocation]
requires: [csharp/types.md, csharp/threading.md]
feeds: [csharp/verification.md]
related: [rust/safety.md, js/safety.md, python/safety.md]
keywords: [unsafe, span, stackalloc, nullable, dynamic, pointer, pal-layer]
layer: 4
---
# Safety

> Nullable always enabled, `unsafe` only in PAL — `Span<T>` over raw pointers

---

RULE: Nullable reference types always enabled — `<Nullable>enable</Nullable>` in every `.csproj`
RULE: `unsafe` blocks only in PAL layer — document the invariant being upheld
RULE: `Span<T>` and `Memory<T>` over raw pointers for performance-critical code
RULE: `stackalloc` only with bounded, known-small sizes — never user-controlled length

```csharp
// GOOD: Span<T> for zero-allocation parsing (no unsafe needed)
public static int CountLines(ReadOnlySpan<char> text)
{
    int count = 0;
    foreach (var line in text.EnumerateLines())
        count++;
    return count;
}

// GOOD: stackalloc with bounded size
Span<byte> buffer = stackalloc byte[256];
int bytesRead = stream.Read(buffer);

// GOOD: unsafe only in PAL layer with documented invariant
// SAFETY: hwnd is guaranteed valid by the Win32 CreateWindowEx contract
// and is not accessed after DestroyWindow.
unsafe void SetWindowTitle_pal(nint hwnd, string title)
{
    fixed (char* ptr = title)
        SetWindowTextW(hwnd, ptr);
}

// BAD: dynamic in domain code — no type safety
dynamic config = LoadConfig();  // compiler can't help you
```

BANNED: `unsafe` outside PAL layer without documented reason and safety invariant
BANNED: Suppressing nullable warnings (`null!`) without a comment explaining why
BANNED: `dynamic` type in domain code — use generics, interfaces, or pattern matching
BANNED: `stackalloc` with user-controlled or unbounded size — stack overflow risk
BANNED: Raw pointer arithmetic when `Span<T>` would work
