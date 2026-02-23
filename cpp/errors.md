# Error Handling

> Result types, no exceptions — same ACK pattern as Python/JS

---

RULE: `std::expected<T, E>` (C++23) or custom `Result<T>`
RULE: NO exceptions — disabled via `-fno-exceptions`
RULE: Same ACK pattern as Python/JS

```cpp
// Result type (matches Python/JS ACK pattern)
template<typename T>
struct Result {
    bool success;
    T data;
    std::string error;

    static Result ok(T value) { return {true, std::move(value), ""}; }
    static Result fail(std::string msg) { return {false, {}, std::move(msg)}; }
};

// Usage
Result<Config> load_config(const std::string& path) {
    if (!file_exists(path)) {
        return Result<Config>::fail("File not found: " + path);
    }
    // ...
    return Result<Config>::ok(config);
}

// Caller checks success first (same as Python/JS)
auto result = load_config("app.conf");
if (!result.success) {
    log_error(result.error);
    return;
}
use(result.data);
```

BANNED: Exceptions (use Result types)
