# Ktor Client

> Single HttpClient instance, ContentNegotiation, error handling

---

RULE: Single HttpClient instance per app
RULE: ContentNegotiation for JSON
RULE: Proper error handling

```kotlin
object ApiClient {
    private val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                isLenient = true
            })
        }
        install(HttpTimeout) {
            requestTimeoutMillis = 30_000
        }
    }

    suspend inline fun <reified T> get(url: String): Result<T> {
        return try {
            Result.Success(client.get(url).body())
        } catch (e: Exception) {
            Result.Error("GET $url failed", e)
        }
    }
}
```
